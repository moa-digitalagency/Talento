"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com

Service pour la recherche de films via OMDB API
"""
import requests
import os

OMDB_BASE_URL = 'http://www.omdbapi.com/'

def search_movies(query, page=1):
    """
    Recherche des films sur OMDB
    
    Args:
        query: Terme de recherche
        page: Numéro de page (défaut: 1)
        
    Returns:
        dict: Résultats de recherche ou erreur
    """
    from app.models.settings import AppSettings
    
    OMDB_API_KEY = AppSettings.get('omdb_api_key', '') or os.environ.get('OMDB_API_KEY', '')
    
    if not OMDB_API_KEY:
        return {'error': 'OMDB API key not configured'}
    
    if not query or len(query.strip()) < 2:
        return {'results': []}
    
    try:
        # Search for both movies and series to match TMDb functionality
        all_results = []
        total_count = 0
        
        for search_type in ['movie', 'series']:
            params = {
                'apikey': OMDB_API_KEY,
                's': query,
                'page': page,
                'type': search_type
            }
            
            response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('Response') != 'False':
                for item in data.get('Search', []):
                    # Map OMDB type to display format
                    if item.get('Type') == 'movie':
                        display_type = 'Film'
                    elif item.get('Type') == 'series':
                        display_type = 'Série TV'
                    else:
                        display_type = item.get('Type', 'Film').title()
                    
                    all_results.append({
                        'id': item.get('imdbID'),
                        'title': item.get('Title', ''),
                        'year': item.get('Year', ''),
                        'type': display_type,
                        'poster_url': item.get('Poster') if item.get('Poster') != 'N/A' else '',
                        'tmdb_id': item.get('imdbID')
                    })
                
                total_count += int(data.get('totalResults', 0))
        
        # Limit to 10 results like the original TMDb implementation
        all_results = all_results[:10]
        
        return {'results': all_results, 'total': total_count}
        
    except requests.RequestException as e:
        return {'error': f'Erreur de recherche: {str(e)}'}
    except Exception as e:
        return {'error': f'Erreur interne: {str(e)}'}
