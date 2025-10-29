"""
taalentio.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Script de migration pour convertir les anciennes valeurs de disponibilité
vers les nouvelles valeurs harmonisées
"""
from app import create_app, db
from app.models.user import User

def migrate_availability():
    """Migrer les valeurs de disponibilité des anciennes vers les nouvelles"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Migration des valeurs de disponibilité...")
        
        mapping = {
            'available': 'Temps plein',
            'partially_available': 'Temps partiel',
            'unavailable': 'Indisponible'
        }
        
        updated_count = 0
        
        for old_value, new_value in mapping.items():
            users = User.query.filter_by(availability=old_value).all()
            for user in users:
                user.availability = new_value
                updated_count += 1
            
            if users:
                print(f"  ✓ Migré {len(users)} utilisateurs: '{old_value}' → '{new_value}'")
        
        if updated_count > 0:
            db.session.commit()
            print(f"✅ Migration terminée : {updated_count} utilisateurs mis à jour")
        else:
            print("ℹ️  Aucune migration nécessaire")

if __name__ == '__main__':
    migrate_availability()
