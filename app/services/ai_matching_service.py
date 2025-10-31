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
            from app.services.ai_provider_service import AIProviderService
            import json
            
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

            system_message = 'Tu es un expert RH qui analyse des profils et des CV. Réponds toujours en JSON valide.'
            
            ai_result = AIProviderService.call_ai(prompt, system_message=system_message, temperature=0.3, timeout=60)
            
            if not ai_result['success']:
                logger.error(f"Erreur IA: {ai_result['error']}")
                return None
            
            ai_response = ai_result['content'].strip()
            
            # Nettoyer la réponse
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
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du candidat: {e}")
            return None
    
    @staticmethod
    def analyze_cinema_talents(job_description, cinema_talent_profiles, api_key=None):
        """
        Analyse une description de rôle cinéma et trouve les meilleurs talents
        
        Args:
            job_description: Texte de la description du rôle
            cinema_talent_profiles: Liste des talents cinéma à analyser
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
                    'message': 'La description de rôle est vide.'
                }
            
            if not cinema_talent_profiles or len(cinema_talent_profiles) == 0:
                return {
                    'success': False,
                    'message': 'Aucun profil cinéma à analyser.'
                }
            
            matched_candidates = []
            
            for talent in cinema_talent_profiles:
                try:
                    profile_data = AIMatchingService._extract_cinema_profile_data(talent)
                    
                    match_result = AIMatchingService._analyze_single_cinema_talent(
                        job_description,
                        profile_data,
                        talent,
                        api_key
                    )
                    
                    if match_result and match_result.get('score', 0) > 0:
                        matched_candidates.append(match_result)
                
                except Exception as e:
                    logger.warning(f"Erreur lors de l'analyse du talent {talent.unique_code if talent.unique_code else talent.id}: {e}")
                    continue
            
            matched_candidates.sort(key=lambda x: x.get('score', 0), reverse=True)
            
            return {
                'success': True,
                'candidates': matched_candidates,
                'total_analyzed': len(cinema_talent_profiles),
                'total_matched': len(matched_candidates)
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de la description de rôle cinéma: {e}")
            return {
                'success': False,
                'message': f'Erreur lors de l\'analyse: {str(e)}'
            }
    
    @staticmethod
    def _extract_cinema_profile_data(talent):
        """Extrait les données du profil d'un talent cinéma"""
        import json
        
        profile_data = {
            'code': talent.unique_code if talent.unique_code else f'ID-{talent.id}',
            'nom': f"{talent.first_name} {talent.last_name}",
            'email': talent.email,
            'ville': talent.city_of_residence,
            'pays': talent.country_of_residence,
            'age': talent.age,
            'genre': 'Homme' if talent.gender == 'M' else 'Femme' if talent.gender == 'F' else 'Autre',
            'taille': f"{talent.height} cm" if talent.height else None,
            'poids': f"{talent.weight} kg" if talent.weight else None,
            'teint': talent.skin_tone,
            'couleur_yeux': talent.eye_color,
            'couleur_cheveux': talent.hair_color,
            'type_cheveux': talent.hair_type,
            'corpulence': talent.build,
            'ethnicites': json.loads(talent.ethnicities) if talent.ethnicities else [],
            'types_talents': json.loads(talent.talent_types) if talent.talent_types else [],
            'langues': json.loads(talent.languages_spoken) if talent.languages_spoken else [],
            'competences': json.loads(talent.skills) if talent.skills else [],
            'experience': talent.experience_years,
            'bio': talent.bio
        }
        
        return profile_data
    
    @staticmethod
    def _analyze_single_cinema_talent(job_description, profile_data, talent, api_key):
        """Analyse un talent cinéma individuel par rapport à la description de rôle"""
        try:
            from app.services.ai_provider_service import AIProviderService
            import json
            
            prompt = f"""Tu es un directeur de casting professionnel. Analyse le profil du talent suivant par rapport à cette description de rôle et détermine s'il correspond au casting.

DESCRIPTION DU RÔLE:
{job_description}

PROFIL DU TALENT:
Nom: {profile_data['nom']}
Code: {profile_data['code']}
Âge: {profile_data['age']} ans
Genre: {profile_data['genre']}
Localisation: {profile_data['ville']}, {profile_data['pays']}
Taille: {profile_data['taille']}
Poids: {profile_data['poids']}
Teint de peau: {profile_data['teint']}
Couleur des yeux: {profile_data['couleur_yeux']}
Couleur des cheveux: {profile_data['couleur_cheveux']}
Type de cheveux: {profile_data['type_cheveux']}
Corpulence: {profile_data['corpulence']}
Ethnicités: {', '.join(profile_data['ethnicites']) if profile_data['ethnicites'] else 'Non spécifié'}
Types de talents: {', '.join(profile_data['types_talents']) if profile_data['types_talents'] else 'Non spécifié'}
Langues parlées: {', '.join(profile_data['langues']) if profile_data['langues'] else 'Non spécifié'}
Compétences spéciales: {', '.join(profile_data['competences']) if profile_data['competences'] else 'Aucune'}
Années d'expérience: {profile_data['experience']} ans
Bio: {profile_data['bio'] if profile_data['bio'] else 'Non renseignée'}

INSTRUCTIONS:
1. Attribue un score de matching de 0 à 100 (0 = pas du tout adapté, 100 = parfaitement adapté)
2. Fournis une explication détaillée en français expliquant pourquoi ce talent correspond ou non au rôle
3. Liste les points forts du talent pour ce rôle (caractéristiques physiques, compétences, expérience)
4. Liste les points faibles ou manques éventuels

Réponds UNIQUEMENT avec ce format JSON (pas de texte avant ou après):
{{
    "score": <nombre entre 0 et 100>,
    "explication": "<explication détaillée>",
    "points_forts": ["<point 1>", "<point 2>", ...],
    "points_faibles": ["<point 1>", "<point 2>", ...]
}}"""

            system_message = 'Tu es un directeur de casting professionnel qui évalue des talents pour le cinéma. Réponds toujours en JSON valide.'
            
            ai_result = AIProviderService.call_ai(prompt, system_message=system_message, temperature=0.3, timeout=60)
            
            if not ai_result['success']:
                logger.error(f"Erreur IA: {ai_result['error']}")
                return None
            
            ai_response = ai_result['content'].strip()
            
            # Nettoyer la réponse
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:]
            if ai_response.startswith('```'):
                ai_response = ai_response[3:]
            if ai_response.endswith('```'):
                ai_response = ai_response[:-3]
            ai_response = ai_response.strip()
            
            match_data = json.loads(ai_response)
            
            return {
                'talent': talent,
                'profile_data': profile_data,
                'score': match_data.get('score', 0),
                'explication': match_data.get('explication', ''),
                'points_forts': match_data.get('points_forts', []),
                'points_faibles': match_data.get('points_faibles', [])
            }
                
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse du talent cinéma: {e}")
            return None
