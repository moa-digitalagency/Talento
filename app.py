import os
from app import create_app, db
from app.models import User, Talent, UserTalent, Country, City, Production

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Talent': Talent,
        'UserTalent': UserTalent,
        'Country': Country,
        'City': City,
        'Production': Production
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

def ensure_demo_productions():
    """Créer 2 productions démo au démarrage si elles n'existent pas"""
    with app.app_context():
        from datetime import date
        
        # Vérifier si des productions existent déjà
        existing_count = Production.query.count()
        if existing_count > 0:
            print(f"📊 {existing_count} production(s) déjà présente(s)")
            return
        
        print("🎬 Création des productions démo...")
        
        # Production 1: Film marocain
        prod1 = Production(
            title="Les Étoiles du Désert",
            original_title="Les Étoiles du Désert",
            production_type="Film",
            genre="Drame",
            director="Nabil Ayouch",
            producer="Ali N'Productions",
            production_company="Morocco Films Production",
            country="Maroc",
            language="Arabe, Français",
            production_year=2024,
            release_date=date(2024, 11, 15),
            start_date=date(2024, 3, 1),
            end_date=date(2024, 6, 30),
            synopsis="L'histoire captivante d'une famille berbère qui traverse les défis du désert marocain pour réaliser leurs rêves. Une exploration poétique de la résilience, de l'identité et de l'espoir dans un contexte moderne.",
            description="Ce film dramatique suit le parcours de Fatima, une jeune femme berbère qui rêve de devenir réalisatrice. Entre traditions ancestrales et aspirations contemporaines, elle doit naviguer les attentes familiales tout en poursuivant sa passion. Tourné dans les magnifiques paysages du Sahara marocain, le film offre une réflexion profonde sur l'identité culturelle et l'émancipation.",
            budget="3 millions USD",
            box_office="8.5 millions USD",
            poster_url="https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800",
            duration=125,
            rating="Tous publics",
            status="Sortie",
            website="https://example.com/etoiles-desert"
        )
        
        # Production 2: Série TV
        prod2 = Production(
            title="Casablanca Chronicles",
            original_title="Chroniques de Casablanca",
            production_type="Série",
            genre="Thriller, Drame",
            director="Laïla Marrakchi",
            producer="Hassan El Fad",
            production_company="Royal TV Productions",
            country="Maroc",
            language="Arabe, Français, Anglais",
            production_year=2025,
            release_date=date(2025, 2, 1),
            start_date=date(2024, 9, 1),
            end_date=date(2024, 12, 20),
            synopsis="Une série palpitante qui plonge dans les mystères et intrigues de Casablanca moderne. Entre crime organisé, corruption politique et relations familiales complexes, cette série révèle les dessous d'une métropole en mutation.",
            description="Casablanca Chronicles suit plusieurs personnages dont les destins s'entrelacent dans la ville blanche. Un inspecteur de police dévoué, une avocate ambitieuse, et un entrepreneur visionnaire se retrouvent au cœur d'une conspiration qui pourrait changer le visage de la ville. La série explore les tensions entre modernité et tradition, justice et pouvoir, dans le Maroc contemporain.",
            budget="12 millions USD (Saison 1)",
            poster_url="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800",
            duration=55,
            rating="-16",
            status="En production",
            website="https://example.com/casablanca-chronicles"
        )
        
        try:
            db.session.add(prod1)
            db.session.add(prod2)
            db.session.commit()
            print("✅ 2 productions démo créées avec succès!")
            print(f"   - {prod1.title} ({prod1.production_type})")
            print(f"   - {prod2.title} ({prod2.production_type})")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️  Erreur lors de la création des productions démo: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_admin_user()
        ensure_demo_productions()
    app.run(host='0.0.0.0', port=5000, debug=True)
