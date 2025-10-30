"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

from app.models.settings import AppSettings

class SEOService:
    
    DEFAULT_SETTINGS = {
        'seo_site_name': 'Taalentio - Valorisation des Talents',
        'seo_site_description': 'Plateforme de gestion et de valorisation des talents pour l\'industrie du cinéma et de la production audiovisuelle.',
        'seo_keywords': 'talents, cinéma, production, audiovisuel, gestion talents, casting, maroc, taalentio',
        'seo_author': 'MOA Digital Agency LLC',
        'seo_og_type': 'website',
        'seo_og_image': '/static/img/logo-full.png',
        'seo_twitter_card': 'summary_large_image',
        'seo_twitter_handle': '@taalentio',
        'seo_robots': 'index, follow',
        'seo_canonical_url': 'https://taalentio.com',
        'seo_language': 'fr',
        'seo_region': 'MA'
    }
    
    @staticmethod
    def get_all_settings():
        settings = {}
        for key, default_value in SEOService.DEFAULT_SETTINGS.items():
            settings[key] = AppSettings.get(key, default_value)
        return settings
    
    @staticmethod
    def get_setting(key):
        default_value = SEOService.DEFAULT_SETTINGS.get(key, '')
        return AppSettings.get(key, default_value)
    
    @staticmethod
    def update_settings(settings_dict):
        for key, value in settings_dict.items():
            if key in SEOService.DEFAULT_SETTINGS:
                AppSettings.set(key, value)
        return True
    
    @staticmethod
    def reset_to_defaults():
        for key, default_value in SEOService.DEFAULT_SETTINGS.items():
            AppSettings.set(key, default_value)
        return True
    
    @staticmethod
    def get_meta_tags():
        settings = SEOService.get_all_settings()
        return {
            'title': settings['seo_site_name'],
            'description': settings['seo_site_description'],
            'keywords': settings['seo_keywords'],
            'author': settings['seo_author'],
            'robots': settings['seo_robots'],
            'og_title': settings['seo_site_name'],
            'og_description': settings['seo_site_description'],
            'og_image': settings['seo_og_image'],
            'og_type': settings['seo_og_type'],
            'twitter_card': settings['seo_twitter_card'],
            'twitter_handle': settings['seo_twitter_handle'],
            'canonical': settings['seo_canonical_url'],
            'language': settings['seo_language'],
            'region': settings['seo_region']
        }
