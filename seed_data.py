from app import create_app, db
from app.models.user import User
from app.models.talent import Talent
from app.models.location import Country, City

app = create_app()

with app.app_context():
    db.create_all()
    
    print("Seeding countries...")
    countries_data = [
        {'name': 'Maroc', 'code': 'MA'},
        {'name': 'France', 'code': 'FR'},
        {'name': 'Sénégal', 'code': 'SN'},
        {'name': 'Algérie', 'code': 'DZ'},
        {'name': 'Tunisie', 'code': 'TN'},
        {'name': 'Belgique', 'code': 'BE'},
        {'name': 'Canada', 'code': 'CA'},
    ]
    
    for data in countries_data:
        if not Country.query.filter_by(code=data['code']).first():
            country = Country(**data)
            db.session.add(country)
    
    print("Seeding cities...")
    cities_data = [
        {'name': 'Rabat', 'code': 'RAB'},
        {'name': 'Casablanca', 'code': 'CAS'},
        {'name': 'Tanger', 'code': 'TNG'},
        {'name': 'Marrakech', 'code': 'MAR'},
        {'name': 'Fès', 'code': 'FES'},
        {'name': 'Agadir', 'code': 'AGA'},
        {'name': 'Meknès', 'code': 'MEK'},
        {'name': 'Oujda', 'code': 'OUJ'},
        {'name': 'Tétouan', 'code': 'TET'},
    ]
    
    for data in cities_data:
        if not City.query.filter_by(code=data['code']).first():
            city = City(**data)
            db.session.add(city)
    
    print("Seeding talents...")
    talents_data = [
        {'name': 'Cuisine', 'emoji': '🍳', 'category': 'Restauration'},
        {'name': 'Ménage', 'emoji': '🧹', 'category': 'Services'},
        {'name': 'Modèle photo', 'emoji': '📸', 'category': 'Artistique'},
        {'name': 'Mannequinat', 'emoji': '🧵', 'category': 'Artistique'},
        {'name': 'Informatique', 'emoji': '💻', 'category': 'Technologie'},
        {'name': 'Maçonnerie', 'emoji': '🧱', 'category': 'Construction'},
        {'name': 'Musique', 'emoji': '🎶', 'category': 'Artistique'},
        {'name': 'Plomberie', 'emoji': '🔧', 'category': 'Technique'},
        {'name': 'Électricité', 'emoji': '⚡', 'category': 'Technique'},
        {'name': 'Bricolage', 'emoji': '🛠️', 'category': 'Technique'},
        {'name': 'Chauffeur', 'emoji': '🚗', 'category': 'Transport'},
        {'name': 'Formation', 'emoji': '👩‍🏫', 'category': 'Éducation'},
        {'name': 'Pâtisserie', 'emoji': '🧑‍🍳', 'category': 'Restauration'},
        {'name': 'Design', 'emoji': '🧑‍🎨', 'category': 'Créatif'},
        {'name': 'Rédaction', 'emoji': '📝', 'category': 'Communication'},
        {'name': 'Community Management', 'emoji': '📣', 'category': 'Marketing'},
        {'name': 'Dév. web', 'emoji': '🖥️', 'category': 'Technologie'},
        {'name': 'Dév. mobile', 'emoji': '📱', 'category': 'Technologie'},
        {'name': 'Vidéo', 'emoji': '🎥', 'category': 'Médias'},
        {'name': 'Graphisme', 'emoji': '🖌️', 'category': 'Créatif'},
        {'name': 'SEO/SEA', 'emoji': '🌐', 'category': 'Marketing'},
        {'name': 'Data/BI', 'emoji': '📊', 'category': 'Technologie'},
        {'name': 'IA/ML', 'emoji': '🤖', 'category': 'Technologie'},
        {'name': 'Animation/Événementiel', 'emoji': '🎭', 'category': 'Événements'},
    ]
    
    for data in talents_data:
        if not Talent.query.filter_by(name=data['name']).first():
            talent = Talent(**data)
            db.session.add(talent)
    
    print("Creating admin user...")
    if not User.query.filter_by(email='admin@talento.app').first():
        admin = User()
        admin.first_name = 'Admin'
        admin.last_name = 'Talento'
        admin.email = 'admin@talento.app'
        admin.set_password('admin123')
        admin.phone = '+212600000000'
        admin.whatsapp = '+212600000000'
        admin.gender = 'N'
        admin.is_admin = True
        admin.unique_code = 'MA' + 'RAB' + '0001' + 'N'
        admin.country_id = 1
        admin.city_id = 1
        db.session.add(admin)
    
    db.session.commit()
    print("Seed data created successfully!")
