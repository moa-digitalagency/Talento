"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

import os
from app import create_app, db
from app.models import User, Talent, UserTalent, Country, City, Production, Project, ProjectTalent

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
        'Production': Production,
        'Project': Project,
        'ProjectTalent': ProjectTalent
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
        admin_code = 'MAN0001RAB'
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
    """Créer 2 boîtes de production démo au démarrage si elles n'existent pas"""
    with app.app_context():
        import json
        
        # Vérifier si des boîtes de production existent déjà
        existing_count = Production.query.count()
        if existing_count > 0:
            print(f"🏢 {existing_count} boîte(s) de production déjà présente(s)")
            return
        
        print("🏢 Création des boîtes de production démo...")
        
        # Boîte de production 1: Morocco Films Production
        company1 = Production(
            name="Morocco Films Production",
            description="Société de production cinématographique spécialisée dans les films et séries de haute qualité. Leader dans la production audiovisuelle au Maroc depuis plus de 15 ans.",
            specialization="Films de cinéma, Séries TV, Documentaires",
            address="123 Boulevard Mohammed V",
            city="Casablanca",
            country="Maroc",
            postal_code="20000",
            phone="+212 522 123 456",
            email="contact@moroccofilms.ma",
            website="https://www.moroccofilms.ma",
            facebook="moroccofilms",
            instagram="@moroccofilms",
            linkedin="morocco-films-production",
            twitter="@moroccofilms",
            founded_year=2008,
            ceo="Nabil Ayouch",
            employees_count=45,
            productions_count=28,
            notable_productions=json.dumps([
                "Les Étoiles du Désert",
                "Casablanca by Night",
                "Le Jardin des Oliviers",
                "Atlas Dreams"
            ], ensure_ascii=False),
            services=json.dumps([
                "Production cinématographique",
                "Post-production",
                "Casting",
                "Location de matériel"
            ], ensure_ascii=False),
            equipment="Caméras RED, ARRI Alexa, Drones DJI, Studios d'enregistrement",
            studios="2 studios de tournage (500m² et 800m²), Studio de post-production",
            certifications=json.dumps([
                "ISO 9001",
                "CCM (Centre Cinématographique Marocain)"
            ], ensure_ascii=False),
            awards=json.dumps([
                "Prix du Meilleur Producteur - Festival de Marrakech 2022",
                "Grand Prix - Festival National du Film 2021"
            ], ensure_ascii=False),
            is_active=True,
            is_verified=True
        )
        
        # Boîte de production 2: Atlas Studios Production
        company2 = Production(
            name="Atlas Studios Production",
            description="Spécialiste de la production de films internationaux et de séries TV. Nous offrons des services complets de production, de la pré-production à la post-production.",
            specialization="Films internationaux, Séries TV, Publicités, Clips musicaux",
            address="Avenue des Forces Armées Royales, Zone Industrielle",
            city="Ouarzazate",
            country="Maroc",
            postal_code="45000",
            phone="+212 524 888 777",
            email="info@atlasstudios.ma",
            website="https://www.atlasstudios.ma",
            facebook="atlasstudios",
            instagram="@atlasstudios_ma",
            linkedin="atlas-studios-production",
            founded_year=2012,
            ceo="Laïla Marrakchi",
            employees_count=62,
            productions_count=42,
            notable_productions=json.dumps([
                "Kingdom of Heaven",
                "Game of Thrones (Saisons 3-6)",
                "The Mummy Returns",
                "Babel"
            ], ensure_ascii=False),
            services=json.dumps([
                "Production cinématographique",
                "Services de plateau",
                "Location de décors",
                "Coordination de tournage",
                "Post-production",
                "Effets spéciaux"
            ], ensure_ascii=False),
            equipment="Caméras ARRI, RED, Sony Venice, Grues, Drones professionnels, Équipement d'éclairage complet",
            studios="Studios Atlas: 20 hectares, 8 plateaux de tournage, Backlots variés (désert, médina, forteresse)",
            certifications=json.dumps([
                "ISO 9001:2015",
                "CCM Agrément",
                "Film Commission Morocco"
            ], ensure_ascii=False),
            memberships=json.dumps([
                "Association des Producteurs de Films Marocains",
                "Mediterranean Film Institute"
            ], ensure_ascii=False),
            awards=json.dumps([
                "Meilleure Collaboration Internationale - 2023",
                "Prix de l'Excellence Technique - Festival de Cannes 2020"
            ], ensure_ascii=False),
            is_active=True,
            is_verified=True
        )
        
        try:
            db.session.add(company1)
            db.session.add(company2)
            db.session.commit()
            print("✅ 2 boîtes de production démo créées avec succès!")
            print(f"   - {company1.name} ({company1.city})")
            print(f"   - {company2.name} ({company2.city})")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️  Erreur lors de la création des boîtes de production démo: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_admin_user()
        ensure_demo_productions()
    app.run(host='0.0.0.0', port=5004, debug=True)
