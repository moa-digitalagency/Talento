"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Service d'analyse intelligente de CV et profils
Utilise OpenRouter AI pour analyser les CV et générer des scores
"""
import os
import json
import requests
from datetime import datetime
from flask import current_app

class CVAnalyzerService:
    """Service d'analyse de CV avec IA"""
    
    @staticmethod
    def analyze_cv(cv_path, user_data=None):
        """
        Analyser un CV et générer un score de profil
        
        Args:
            cv_path: Chemin vers le fichier CV
            user_data: Données utilisateur (optionnel)
            
        Returns:
            dict: Résultats de l'analyse avec score et recommandations
        """
        api_key = os.environ.get('OPENROUTER_API_KEY')
        
        if not api_key:
            return {
                'success': False,
                'error': 'OPENROUTER_API_KEY non configurée',
                'score': 0
            }
        
        try:
            cv_text = CVAnalyzerService._extract_cv_text(cv_path)
            
            if not cv_text:
                return {
                    'success': False,
                    'error': 'Impossible d\'extraire le texte du CV',
                    'score': 0
                }
            
            analysis_prompt = CVAnalyzerService._build_analysis_prompt(cv_text, user_data)
            
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': os.environ.get('REPLIT_DEV_DOMAIN', 'http://localhost:5004'),
                },
                json={
                    'model': 'meta-llama/llama-3.1-8b-instruct:free',
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'Tu es un expert RH qui analyse des CV et profils professionnels. Réponds toujours en JSON valide.'
                        },
                        {
                            'role': 'user',
                            'content': analysis_prompt
                        }
                    ],
                    'temperature': 0.3,
                    'max_tokens': 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                analysis = CVAnalyzerService._parse_ai_response(ai_response)
                
                return {
                    'success': True,
                    'score': analysis.get('score', 50),
                    'strengths': analysis.get('strengths', []),
                    'weaknesses': analysis.get('weaknesses', []),
                    'recommendations': analysis.get('recommendations', []),
                    'skills_detected': analysis.get('skills_detected', []),
                    'experience_years': analysis.get('experience_years', 0),
                    'analyzed_at': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'Erreur API: {response.status_code}',
                    'score': 0
                }
                
        except Exception as e:
            current_app.logger.error(f"Erreur analyse CV: {e}")
            return {
                'success': False,
                'error': str(e),
                'score': 0
            }
    
    @staticmethod
    def _extract_cv_text(cv_path):
        """Extraire le texte d'un fichier CV (PDF, DOCX, etc.)"""
        import PyPDF2
        import docx
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'cvs', cv_path)
        
        if not os.path.exists(file_path):
            return None
        
        ext = os.path.splitext(cv_path)[1].lower()
        
        try:
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
            current_app.logger.error(f"Erreur extraction CV: {e}")
            return None
    
    @staticmethod
    def _build_analysis_prompt(cv_text, user_data=None):
        """Construire le prompt d'analyse pour l'IA"""
        user_info = ""
        if user_data:
            user_info = f"""
Informations du profil:
- Nom: {user_data.get('name', 'N/A')}
- Talents déclarés: {', '.join(user_data.get('talents', []))}
- Localisation: {user_data.get('location', 'N/A')}
"""
        
        prompt = f"""Analyse ce CV professionnel et fournis une évaluation détaillée.

{user_info}

Contenu du CV:
{cv_text[:3000]}

Réponds UNIQUEMENT avec un objet JSON valide au format suivant:
{{
    "score": <nombre entre 0 et 100>,
    "strengths": ["point fort 1", "point fort 2", "point fort 3"],
    "weaknesses": ["point faible 1", "point faible 2"],
    "recommendations": ["recommandation 1", "recommandation 2", "recommandation 3"],
    "skills_detected": ["compétence 1", "compétence 2", "compétence 3"],
    "experience_years": <nombre d'années d'expérience estimées>
}}

Critères d'évaluation du score (0-100):
- Clarté et structure: 20 points
- Expérience pertinente: 25 points
- Compétences techniques: 25 points
- Formation et certifications: 15 points
- Réalisations mesurables: 15 points"""
        
        return prompt
    
    @staticmethod
    def _parse_ai_response(ai_response):
        """Parser la réponse JSON de l'IA"""
        try:
            ai_response = ai_response.strip()
            
            if '```json' in ai_response:
                ai_response = ai_response.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response:
                ai_response = ai_response.split('```')[1].split('```')[0].strip()
            
            return json.loads(ai_response)
        except json.JSONDecodeError:
            return {
                'score': 50,
                'strengths': ['Profil enregistré'],
                'weaknesses': ['Analyse détaillée non disponible'],
                'recommendations': ['Compléter le profil'],
                'skills_detected': [],
                'experience_years': 0
            }
    
    @staticmethod
    def calculate_profile_score(user):
        """
        Calculer le score du profil basé sur la complétude
        
        Args:
            user: Instance du modèle User
            
        Returns:
            int: Score entre 0 et 100
        """
        score = 0
        
        if user.first_name and user.last_name:
            score += 5
        
        if user.email:
            score += 5
        
        if user.phone_encrypted:
            score += 5
        
        if user.date_of_birth:
            score += 5
        
        if user.country_id:
            score += 5
        
        if user.city_id:
            score += 5
        
        if user.photo_filename:
            score += 10
        
        if user.cv_filename:
            score += 20
        
        if user.portfolio_url:
            score += 10
        
        if user.bio:
            score += 10
        
        if user.talents and len(user.talents) > 0:
            score += 15
        
        social_media_count = sum([
            1 for field in ['linkedin', 'instagram', 'twitter', 'facebook', 'github']
            if getattr(user, f'{field}_encrypted', None)
        ])
        score += min(social_media_count * 3, 15)
        
        return min(score, 100)
