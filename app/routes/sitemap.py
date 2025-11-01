"""
Route pour générer le sitemap.xml dynamique
"""

from flask import Blueprint, Response, url_for
from datetime import datetime

bp = Blueprint('sitemap', __name__)

@bp.route('/sitemap.xml')
def sitemap():
    """Génère un sitemap XML pour le référencement SEO"""
    
    pages = []
    
    # Pages statiques principales
    static_pages = [
        ('main.index', 1.0, 'daily'),
        ('auth.login', 0.8, 'monthly'),
        ('auth.register', 0.8, 'monthly'),
        ('legal.about', 0.6, 'monthly'),
        ('legal.privacy', 0.6, 'monthly'),
        ('legal.terms', 0.6, 'monthly'),
        ('legal.mentions', 0.5, 'yearly'),
        ('legal.cookies', 0.5, 'yearly'),
    ]
    
    for route, priority, changefreq in static_pages:
        try:
            pages.append({
                'loc': url_for(route, _external=True),
                'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
                'changefreq': changefreq,
                'priority': priority
            })
        except:
            pass
    
    # Pages Cinema si le module est actif
    try:
        cinema_pages = [
            ('cinema.talents', 0.9, 'daily'),
            ('cinema.projects', 0.9, 'daily'),
            ('cinema.productions', 0.9, 'daily'),
        ]
        
        for route, priority, changefreq in cinema_pages:
            try:
                pages.append({
                    'loc': url_for(route, _external=True),
                    'lastmod': datetime.utcnow().strftime('%Y-%m-%d'),
                    'changefreq': changefreq,
                    'priority': priority
                })
            except:
                pass
    except:
        pass
    
    # Générer le XML
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        sitemap_xml += '  <url>\n'
        sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
        sitemap_xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
        sitemap_xml += '  </url>\n'
    
    sitemap_xml += '</urlset>'
    
    return Response(sitemap_xml, mimetype='application/xml')

@bp.route('/robots.txt')
def robots():
    """Génère le fichier robots.txt pour les moteurs de recherche"""
    
    robots_txt = """User-agent: *
Allow: /
Allow: /auth/login
Allow: /auth/register
Allow: /legal/
Disallow: /admin/
Disallow: /profile/
Disallow: /api/

Sitemap: {sitemap_url}
""".format(sitemap_url=url_for('sitemap.sitemap', _external=True))
    
    return Response(robots_txt, mimetype='text/plain')
