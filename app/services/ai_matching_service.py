"""
taalentio.com
Service d'analyse IA pour le matching talents/emplois
"""

import logging
import os
import requests
from app.models import User
from flask import current_app

logger = logging.getLogger(__name__)


class AIMatchingService:
    """Service pour analyser les profils et trouver les meilleurs candidats via IA"""
    
    @staticmethod
    def analyze_job_description(job_description, user_profiles, api_key=None):
        """
        Analyse une description de poste et trouve les meilleurs candidats
        
        Args:
            job_description: Texte de la description du poste
            user_profiles: Liste des utilisateurs à analyser
            api_key: Clé API OpenRouter (optionnelle, utilise les settings si non fournie)
            
        Returns:
            Liste de dictionnaires contenant les candidats matchés avec leurs scores et raisons
        """
        try:
            if not api_key:
                from app.models import AppSettings
                api_key = AppSettings.get('openrouter_api_key')
            
            if not api_key:
                logger.error("Clé API OpenRouter non configurée")
                return {
                    'success': False,
                    'message': 'Clé API OpenRouter non configurée. Veuillez configurer la clé dans les paramètres système.'
                }
            
            if not job_description or not job_description.strip():
                return {
                    'success': False,
                    'message': 'La description de poste est vide.'
                }
            
            if not user_profiles or len(user_profiles) == 0:
                return {
                    'success': False,
                    'message': 'Aucun profil à analyser.'
                }
            
            matched_candidates = []
            
            for user in user_profiles:
                try:
                    profile_data = AIMatchingService._extract_profile_data(user)
                    
                    match_result = AIMatchingService._analyze_single_candidate(
                        job_description,
                        profile_data,
                        user,
                        api_key
                    )
                    
                    if match_result and match_result.get('score', 0) > 0:
                        matched_candidates.append(match_result)
                
                except Exception as e:
                    logger.warning(f"Erreur lors de l'analyse du profil {user.formatted_code}: {e}")
                    continue
            
            matched_candidates.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            return {
                'success': True,
                'candidates': matched_candidates,
                'total_analyzed': len(user_profiles),
                'total_matched': len(matched_candidates)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de la description de poste: {e}")
            return {
                'success': False,
                'message': f'Erreur lors de l\'analyse: {str(e)}'
            }
    
    @staticmethod
    def _extract_profile_data(user):
        """Extrait les données du profil utilisateur incluant le CV"""
        profile_data = {
            'code': user.formatted_code,
            'nom': user.full_name,
            'email': user.email,
            'ville': user.city.name if user.city else None,
            'pays': user.country.name if user.country else None,
            'disponibilite': user.availability,
            'mode_travail': user.work_mode,
            'talents': [],
            'competences_cv': None
        }
        
        if user.user_talents:
            profile_data['talents'] = [ut.talent.name for ut in user.user_talents]
        
        if user.cv_file:
            cv_text = AIMatchingService._extract_cv_text(user.cv_file)
            if cv_text:
                profile_data['competences_cv'] = cv_text[:3000]
        
        return profile_data
    
    @staticmethod
    def _extract_cv_text(cv_filename):
        """Extrait le texte d'un fichier CV en réutilisant la logique de cv_analyzer"""
        try:
            import PyPDF2
            import docx
            
            file_path = os.path.join(
                current_app.root_path,
                current_app.config.get('UPLOAD_FOLDER', 'static/uploads'),
                'cvs',
                cv_filename
            )
            
            if not os.path.exists(file_path):
                logger.warning(f"Fichier CV non trouvé: {file_path}")
                return None
            
            ext = os.path.splitext(cv_filename)[1].lower()
            
            if ext == '.pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in pdf_reader.pages:
                        text += page.extract_text() + '\n'
                    return text
            
            elif ext in ['.doc', '.docx']:
                doc = docx.Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                return text
            
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    return file.read()
                
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du CV {cv_filename}: {e}")
            return None
    
    @staticmethod
    def _analyze_single_candidate(job_description, profile_data, user, api_key):
        """Analyse un candidat individuel par rapport à la description de poste"""
        try:
            prompt = f"""Tu es un expert en recrutement. Analyse le profil du candidat suivant par rapport à cette description de poste et détermine s'il est un bon candidat.

DESCRIPTION DU POSTE:
{job_description}

PROFIL DU CANDIDAT:
Nom: {profile_data['nom']}
Code: {profile_data['code']}
Localisation: {profile_data['ville']}, {profile_data['pays']}
Disponibilité: {profile_data['disponibilite']}
Mode de travail: {profile_data['mode_travail']}
Talents/Compétences déclarés: {', '.join(profile_data['talents']) if profile_data['talents'] else 'Aucun'}

{"COMPÉTENCES EXTRAITES DU CV:" if profile_data['competences_cv'] else ""}
{profile_data['competences_cv'] if profile_data['competences_cv'] else "CV non disponible"}

INSTRUCTIONS:
1. Attribue un score de matching de 0 à 100 (0 = pas du tout adapté, 100 = parfaitement adapté)
2. Fournis une explication détaillée en français expliquant pourquoi ce candidat correspond ou non au poste
3. Liste les points forts du candidat pour ce poste
4. Liste les points faibles ou manques éventuels

Réponds UNIQUEMENT avec ce format JSON (pas de texte avant ou après):
{{
    "score": <nombre entre 0 et 100>,
    "explication": "<explication détaillée>",
    "points_forts": ["<point 1>", "<point 2>", ...],
    "points_faibles": ["<point 1>", "<point 2>", ...]
}}"""

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://taalentio.com',
                'X-Title': 'taalentio.com - AI Matching'
            }
            
            data = {
                'model': 'google/gemini-2.0-flash-001:free',
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'temperature': 0.3
            }
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                
                import json
                if ai_response.startswith('```json'):
                    ai_response = ai_response[7:]
                if ai_response.startswith('```'):
                    ai_response = ai_response[3:]
                if ai_response.endswith('```'):
                    ai_response = ai_response[:-3]
                ai_response = ai_response.strip()
                
                match_data = json.loads(ai_response)
                
                return {
                    'user': user,
                    'profile_data': profile_data,
                    'score': match_data.get('score', 0),
                    'explication': match_data.get('explication', ''),
                    'points_forts': match_data.get('points_forts', []),
                    'points_faibles': match_data.get('points_faibles', [])
                }
            else:
                logger.error(f"Erreur API OpenRouter: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du candidat: {e}")
            return None
