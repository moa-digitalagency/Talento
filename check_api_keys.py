"""
Script de diagnostic pour vérifier les clés API
Exécutez ce script pour voir si vos clés API sont correctement configurées
"""

import os
os.environ['SKIP_AUTO_MIGRATION'] = '1'

from app import create_app, db
from app.models import AppSettings

def check_api_keys():
    """Vérifie toutes les clés API configurées"""
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("🔍 VÉRIFICATION DES CLÉS API")
        print("="*70)
        print()
        
        # Fournisseur actif
        ai_provider = AppSettings.get('ai_provider', 'openrouter')
        print(f"🎯 Fournisseur AI actif: {ai_provider.upper()}")
        print()
        
        # Vérifier chaque clé API
        api_keys = {
            'OpenRouter': AppSettings.get('openrouter_api_key'),
            'Perplexity': AppSettings.get('perplexity_api_key'),
            'OpenAI': AppSettings.get('openai_api_key'),
            'Gemini': AppSettings.get('gemini_api_key'),
            'SendGrid': AppSettings.get('sendgrid_api_key'),
            'OMDB': AppSettings.get('omdb_api_key')
        }
        
        for provider, key in api_keys.items():
            status = "❌ NON CONFIGURÉE"
            details = ""
            
            if key:
                key = key.strip()
                if len(key) > 0:
                    # Masquer la clé pour la sécurité
                    masked = key[:4] + '*' * (len(key) - 8) + key[-4:] if len(key) > 8 else '****'
                    status = "✅ CONFIGURÉE"
                    details = f"({len(key)} caractères) - {masked}"
                    
                    # Vérifications spécifiques
                    if key.startswith('*'):
                        status = "⚠️  MASQUÉE (valeur non enregistrée)"
                        details = "La clé semble être la valeur masquée, pas la vraie clé"
                    elif ' ' in key:
                        status = "⚠️  CONTIENT DES ESPACES"
                        details = f"La clé contient des espaces (à corriger)"
            
            print(f"{provider:15} : {status} {details}")
        
        print()
        
        # Modèles configurés
        print("📊 MODÈLES CONFIGURÉS:")
        models = {
            'OpenRouter': AppSettings.get('openrouter_model', 'N/A'),
            'Perplexity': AppSettings.get('perplexity_model', 'N/A'),
            'OpenAI': AppSettings.get('openai_model', 'N/A'),
            'Gemini': AppSettings.get('gemini_model', 'N/A')
        }
        
        for provider, model in models.items():
            marker = "🎯" if provider.lower() == ai_provider else "  "
            print(f"{marker} {provider:15} : {model}")
        
        print()
        print("="*70)
        print()
        
        # Recommandations
        if ai_provider == 'perplexity':
            pplx_key = api_keys.get('Perplexity')
            pplx_model = models.get('Perplexity')
            
            print("💡 RECOMMANDATIONS PERPLEXITY:")
            if not pplx_key:
                print("   ❌ Clé API Perplexity manquante")
                print("   → Ajoutez votre clé sur: https://www.perplexity.ai/settings/api")
            elif pplx_key and pplx_key.strip().startswith('*'):
                print("   ⚠️  La clé semble être masquée")
                print("   → Re-saisissez la clé complète (pplx-...)")
            
            if pplx_model:
                print(f"   ✅ Modèle: {pplx_model}")
                if 'llama-3.1' in pplx_model:
                    print("   ⚠️  Modèle déprécié! Utilisez 'sonar' ou 'sonar-pro'")
            
            print()
            print("   Modèles valides 2025:")
            print("   • sonar (rapide, recherche web)")
            print("   • sonar-pro (avancé)")
            print("   • sonar-reasoning (raisonnement)")
            print()

if __name__ == '__main__':
    check_api_keys()
