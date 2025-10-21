"""
Service pour la recherche de films via TMDb API
"""
import requests
import os

TMDB_API_KEY = os.environ.get('TMDB_API_KEY', '')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w200'

def search_movies(query, page=1):
    """
    Recherche des films sur TMDb
    
    Args:
        query: Terme de recherche
        page: Numéro de page (défaut: 1)
        
    Returns:
        dict: Résultats de recherche ou erreur
    """
    if not TMDB_API_KEY:
        return {'error': 'TMDb API key not configured'}
    
    if not query or len(query.strip()) < 2:
        return {'results': []}
    
    try:
        url = f'{TMDB_BASE_URL}/search/multi'
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'page': page,
            'language': 'fr-FR'
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        for item in data.get('results', [])[:10]:
            media_type = item.get('media_type')
            
            if media_type not in ['movie', 'tv']:
                continue
            
            title = item.get('title') or item.get('name', '')
            year = ''
            if item.get('release_date'):
                year = item.get('release_date')[:4]
            elif item.get('first_air_date'):
                year = item.get('first_air_date')[:4]
            
            poster_path = item.get('poster_path')
            poster_url = f'{TMDB_IMAGE_BASE}{poster_path}' if poster_path else ''
            
            results.append({
                'id': item.get('id'),
                'title': title,
                'year': year,
                'type': 'Film' if media_type == 'movie' else 'Série TV',
                'poster_url': poster_url,
                'tmdb_id': item.get('id')
            })
        
        return {'results': results, 'total': data.get('total_results', 0)}
        
    except requests.RequestException as e:
        return {'error': f'Erreur de recherche: {str(e)}'}
    except Exception as e:
        return {'error': f'Erreur interne: {str(e)}'}
