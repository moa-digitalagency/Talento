import os
from app import create_app, db
from app.models import User, Talent, UserTalent, Country, City

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Talent': Talent,
        'UserTalent': UserTalent,
        'Country': Country,
        'City': City
    }

@app.template_filter('format_code')
def format_code_filter(code):
    """Return code without dashes"""
    return code

def ensure_admin_user():
    """Garantir que le compte admin existe à chaque démarrage"""
    with app.app_context():
        from app.models.location import Country, City
        
        admin_email = 'admin@talento.com'
        admin_code = 'MARAB0001N'
        admin_password = os.environ.get('ADMIN_PASSWORD', '@4dm1n')
        
        admin = User.query.filter(
            (User.email == admin_email) | (User.unique_code == admin_code)
        ).first()
        
        if not admin:
            print("👤 Création du compte admin au démarrage...")
            morocco = Country.query.filter_by(code='MA').first()
            rabat = City.query.filter_by(code='RAB').first()
            
            if morocco and rabat:
                admin = User(
                    email=admin_email,
                    first_name='Admin',
                    last_name='Talento',
                    unique_code=admin_code,
                    is_admin=True,
                    account_active=True,
                    country_id=morocco.id,
                    city_id=rabat.id,
                    gender='N'
                )
                admin.set_password(admin_password)
                admin.phone = '+212600000000'
                db.session.add(admin)
                try:
                    db.session.commit()
                    print(f"✅ Admin créé: {admin_email} / {admin_code}")
                except Exception as e:
                    db.session.rollback()
                    print(f"⚠️  Erreur création admin: {e}")
        else:
            if not admin.check_password(admin_password):
                admin.set_password(admin_password)
                db.session.commit()
                print(f"🔐 Mot de passe admin mis à jour")
            if not admin.is_admin:
                admin.is_admin = True
                db.session.commit()
                print(f"👑 Droits admin activés")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_admin_user()
    app.run(host='0.0.0.0', port=5000, debug=True)
