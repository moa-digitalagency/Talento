"""
Service unifié pour gérer différents fournisseurs d'IA
Supporte: OpenRouter, Perplexity, OpenAI, Google Gemini
"""

import os
import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)


class AIProviderService:
    """Service pour gérer différents fournisseurs d'IA de manière unifiée"""
    
    @staticmethod
    def get_ai_config():
        """
        Récupère la configuration du fournisseur d'IA actif
        
        Returns:
            dict: Configuration avec provider, api_key, model
        """
        from app.models import AppSettings
        
        provider = AppSettings.get('ai_provider', 'openrouter')
        
        config = {
            'provider': provider,
            'api_key': None,
            'model': None,
            'endpoint': None
        }
        
        if provider == 'openrouter':
            config['api_key'] = AppSettings.get('openrouter_api_key') or os.environ.get('OPENROUTER_API_KEY')
            config['model'] = AppSettings.get('openrouter_model', 'google/gemini-2.0-flash-001:free')
            config['endpoint'] = 'https://openrouter.ai/api/v1/chat/completions'
        
        elif provider == 'perplexity':
            config['api_key'] = AppSettings.get('perplexity_api_key')
            config['model'] = AppSettings.get('perplexity_model', 'sonar')
            config['endpoint'] = 'https://api.perplexity.ai/chat/completions'
        
        elif provider == 'openai':
            config['api_key'] = AppSettings.get('openai_api_key')
            config['model'] = AppSettings.get('openai_model', 'gpt-4o-mini')
            config['endpoint'] = 'https://api.openai.com/v1/chat/completions'
        
        elif provider == 'gemini':
            config['api_key'] = AppSettings.get('gemini_api_key')
            config['model'] = AppSettings.get('gemini_model', 'gemini-2.0-flash-exp')
            config['endpoint'] = 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        
        return config
    
    @staticmethod
    def call_ai(prompt, system_message=None, temperature=0.3, timeout=60):
        """
        Appelle le fournisseur d'IA configuré avec un prompt
        
        Args:
            prompt: Le prompt à envoyer
            system_message: Message système (optionnel)
            temperature: Température pour la génération (0.0-1.0)
            timeout: Timeout en secondes
            
        Returns:
            dict: {'success': bool, 'content': str, 'error': str}
        """
        config = AIProviderService.get_ai_config()
        
        if not config['api_key']:
            return {
                'success': False,
                'content': '',
                'error': f"Clé API {config['provider']} non configurée"
            }
        
        try:
            if config['provider'] == 'gemini':
                return AIProviderService._call_gemini(config, prompt, system_message, temperature, timeout)
            else:
                return AIProviderService._call_openai_compatible(config, prompt, system_message, temperature, timeout)
        
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à {config['provider']}: {e}")
            return {
                'success': False,
                'content': '',
                'error': str(e)
            }
    
    @staticmethod
    def _call_openai_compatible(config, prompt, system_message, temperature, timeout):
        """
        Appelle une API compatible OpenAI (OpenRouter, Perplexity, OpenAI)
        """
        headers = {
            'Authorization': f'Bearer {config["api_key"]}',
            'Content-Type': 'application/json'
        }
        
        # Headers spécifiques selon le provider
        if config['provider'] == 'openrouter':
            headers['HTTP-Referer'] = 'https://taalentio.com'
            headers['X-Title'] = 'taalentio.com'
        
        messages = []
        if system_message:
            messages.append({
                'role': 'system',
                'content': system_message
            })
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        data = {
            'model': config['model'],
            'messages': messages,
            'temperature': temperature
        }
        
        response = requests.post(
            config['endpoint'],
            headers=headers,
            json=data,
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return {
                'success': True,
                'content': content,
                'error': ''
            }
        else:
            error_msg = f"Erreur API {config['provider']}: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                'success': False,
                'content': '',
                'error': error_msg
            }
    
    @staticmethod
    def _call_gemini(config, prompt, system_message, temperature, timeout):
        """
        Appelle l'API Google Gemini (format différent)
        """
        endpoint = config['endpoint'].format(model=config['model'])
        url = f"{endpoint}?key={config['api_key']}"
        
        # Gemini utilise un format différent
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        data = {
            'contents': [{
                'parts': [{
                    'text': full_prompt
                }]
            }],
            'generationConfig': {
                'temperature': temperature,
                'maxOutputTokens': 2048
            }
        }
        
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=data,
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            return {
                'success': True,
                'content': content,
                'error': ''
            }
        else:
            error_msg = f"Erreur API Gemini: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return {
                'success': False,
                'content': '',
                'error': error_msg
            }
