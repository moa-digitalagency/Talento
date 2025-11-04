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
            api_key: (Déprécié) Clé API - utilise maintenant le fournisseur IA configuré
            
        Returns:
            Liste de dictionnaires contenant les candidats matchés avec leurs scores et raisons
        """
        try:
            from app.services.ai_provider_service import AIProviderService
            
            # Vérifier qu'un fournisseur IA est configuré
            config = AIProviderService.get_ai_config()
            if not config['api_key']:
                logger.error(f"Clé API {config['provider']} non configurée")
                return {
                    'success': False,
                    'message': f"Clé API {config['provider']} non configurée. Veuillez configurer la clé dans les paramètres système."
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
                        None  # api_key is now handled by AIProviderService
                    )
                    
                    # Accepter tous les résultats avec un score >= 0 (y compris 0 pour voir pourquoi ça ne matche pas)
                    # Mais en production, on pourrait filtrer sur score >= 10 ou 20
                    if match_result and match_result.get('score', 0) >= 0:
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
            'pays_origine': user.country.name if user.country else 'Non spécifié',
            'nationalite': user.nationality or 'Non spécifiée',
            'ville': user.city.name if user.city else 'Non spécifiée',
            'pays': user.country.name if user.country else 'Non spécifié',
            'ville_residence': user.residence_city.name if user.residence_city else 'Non spécifiée',
            'pays_residence': user.residence_country.name if user.residence_country else 'Non spécifié',
            'disponibilite': user.availability or 'Non spécifiée',
            'mode_travail': user.work_mode or 'Non spécifié',
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
Pays d'origine: {profile_data['pays_origine']}
Nationalité: {profile_data['nationalite']}
Localisation actuelle: {profile_data['ville_residence']}, {profile_data['pays_residence']}
Disponibilité: {profile_data['disponibilite']}
Mode de travail: {profile_data['mode_travail']}
Talents/Compétences déclarés: {', '.join(profile_data['talents']) if profile_data['talents'] else 'Aucun'}

{"COMPÉTENCES EXTRAITES DU CV:" if profile_data['competences_cv'] else ""}
{profile_data['competences_cv'] if profile_data['competences_cv'] else "CV non disponible"}

INSTRUCTIONS:
1. Analyse TOUS les critères de la description du poste (localisation, nationalité, compétences, disponibilité, mode de travail, etc.)
2. Attribue un score de matching de 0 à 100 (0 = pas du tout adapté, 100 = parfaitement adapté)
3. Si plusieurs critères correspondent même partiellement, donne un score > 0
4. Fournis une explication détaillée en français expliquant pourquoi ce candidat correspond ou non
5. Liste les points forts et faibles

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
            api_key: (Déprécié) Clé API - utilise maintenant le fournisseur IA configuré
            
        Returns:
            Liste de dictionnaires contenant les candidats matchés avec leurs scores et raisons
        """
        try:
            from app.services.ai_provider_service import AIProviderService
            
            # Vérifier qu'un fournisseur IA est configuré
            config = AIProviderService.get_ai_config()
            if not config['api_key']:
                logger.error(f"Clé API {config['provider']} non configurée")
                return {
                    'success': False,
                    'message': f"Clé API {config['provider']} non configurée. Veuillez configurer la clé dans les paramètres système."
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
                        None  # api_key is now handled by AIProviderService
                    )
                    
                    # Accepter tous les résultats avec un score >= 0 (y compris 0 pour voir pourquoi ça ne matche pas)
                    # Mais en production, on pourrait filtrer sur score >= 10 ou 20
                    if match_result and match_result.get('score', 0) >= 0:
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
            'pays_origine': talent.country_of_origin or 'Non spécifié',
            'nationalite': talent.nationality or 'Non spécifiée',
            'ville': talent.city_of_residence or 'Non spécifiée',
            'pays': talent.country_of_residence or 'Non spécifié',
            'age': talent.age if talent.age else 'Non spécifié',
            'genre': 'Homme' if talent.gender == 'M' else 'Femme' if talent.gender == 'F' else 'Autre',
            'taille': f"{talent.height} cm" if talent.height else 'Non spécifiée',
            'poids': f"{talent.weight} kg" if talent.weight else 'Non spécifié',
            'teint': talent.skin_tone or 'Non spécifié',
            'couleur_yeux': talent.eye_color or 'Non spécifiée',
            'couleur_cheveux': talent.hair_color or 'Non spécifiée',
            'type_cheveux': talent.hair_type or 'Non spécifié',
            'corpulence': talent.build or 'Non spécifiée',
            'ethnicites': json.loads(talent.ethnicities) if talent.ethnicities else [],
            'types_talents': json.loads(talent.talent_types) if talent.talent_types else [],
            'autres_talents': json.loads(talent.other_talents) if talent.other_talents else [],
            'langues': json.loads(talent.languages_spoken) if talent.languages_spoken else [],
            'competences': json.loads(talent.skills) if talent.skills else [],
            'experience': talent.experience_years if talent.experience_years else 0,
            'bio': talent.bio or 'Non renseignée'
        }
        
        return profile_data
    
    @staticmethod
    def _analyze_single_cinema_talent(job_description, profile_data, talent, api_key):
        """Analyse un talent cinéma individuel par rapport à la description de rôle"""
        try:
            from app.services.ai_provider_service import AIProviderService
            import json
            
            # Construire les listes de talents et compétences
            talents_list = []
            if profile_data['types_talents']:
                talents_list.extend(profile_data['types_talents'])
            if profile_data['autres_talents']:
                talents_list.extend(profile_data['autres_talents'])
            
            prompt = f"""Tu es un directeur de casting professionnel. Analyse le profil du talent suivant par rapport à cette description de rôle et détermine s'il correspond au casting.

DESCRIPTION DU RÔLE:
{job_description}

PROFIL DU TALENT:
Nom: {profile_data['nom']}
Code: {profile_data['code']}
Âge: {profile_data['age']}
Genre: {profile_data['genre']}
Pays d'origine: {profile_data['pays_origine']}
Nationalité: {profile_data['nationalite']}
Résidence actuelle: {profile_data['ville']}, {profile_data['pays']}

CARACTÉRISTIQUES PHYSIQUES:
Taille: {profile_data['taille']}
Poids: {profile_data['poids']}
Teint de peau: {profile_data['teint']}
Couleur des yeux: {profile_data['couleur_yeux']}
Couleur des cheveux: {profile_data['couleur_cheveux']}
Type de cheveux: {profile_data['type_cheveux']}
Corpulence: {profile_data['corpulence']}

ORIGINES ET TALENTS:
Ethnicités: {', '.join(profile_data['ethnicites']) if profile_data['ethnicites'] else 'Non spécifié'}
Talents artistiques: {', '.join(talents_list) if talents_list else 'Non spécifié'}
Langues parlées: {', '.join(profile_data['langues']) if profile_data['langues'] else 'Non spécifié'}
Compétences spéciales: {', '.join(profile_data['competences']) if profile_data['competences'] else 'Aucune'}

EXPÉRIENCE:
Années d'expérience: {profile_data['experience']} ans
Bio: {profile_data['bio']}

INSTRUCTIONS:
1. Analyse TOUS les critères de la description du rôle (genre, âge, nationalité, caractéristiques physiques, compétences, etc.)
2. Attribue un score de matching de 0 à 100 (0 = pas du tout adapté, 100 = parfaitement adapté)
3. Si plusieurs critères correspondent même partiellement, donne un score > 0
4. Fournis une explication détaillée en français expliquant pourquoi ce talent correspond ou non
5. Liste les points forts et faibles

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
