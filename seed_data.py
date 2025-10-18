from app import create_app, db
from app.models.user import User
from app.models.talent import Talent
from app.models.location import Country, City

app = create_app()

with app.app_context():
    db.create_all()
    
    print("Seeding African countries...")
    countries_data = [
        {'name': 'Maroc', 'code': 'MA'},
        {'name': 'Algérie', 'code': 'DZ'},
        {'name': 'Tunisie', 'code': 'TN'},
        {'name': 'Libye', 'code': 'LY'},
        {'name': 'Égypte', 'code': 'EG'},
        {'name': 'Mauritanie', 'code': 'MR'},
        {'name': 'Mali', 'code': 'ML'},
        {'name': 'Sénégal', 'code': 'SN'},
        {'name': 'Gambie', 'code': 'GM'},
        {'name': 'Guinée-Bissau', 'code': 'GW'},
        {'name': 'Guinée', 'code': 'GN'},
        {'name': 'Sierra Leone', 'code': 'SL'},
        {'name': 'Liberia', 'code': 'LR'},
        {'name': 'Côte d\'Ivoire', 'code': 'CI'},
        {'name': 'Ghana', 'code': 'GH'},
        {'name': 'Togo', 'code': 'TG'},
        {'name': 'Bénin', 'code': 'BJ'},
        {'name': 'Nigéria', 'code': 'NG'},
        {'name': 'Niger', 'code': 'NE'},
        {'name': 'Burkina Faso', 'code': 'BF'},
        {'name': 'Cameroun', 'code': 'CM'},
        {'name': 'Tchad', 'code': 'TD'},
        {'name': 'République Centrafricaine', 'code': 'CF'},
        {'name': 'Guinée Équatoriale', 'code': 'GQ'},
        {'name': 'Gabon', 'code': 'GA'},
        {'name': 'Congo', 'code': 'CG'},
        {'name': 'RD Congo', 'code': 'CD'},
        {'name': 'Angola', 'code': 'AO'},
        {'name': 'Soudan', 'code': 'SD'},
        {'name': 'Soudan du Sud', 'code': 'SS'},
        {'name': 'Éthiopie', 'code': 'ET'},
        {'name': 'Érythrée', 'code': 'ER'},
        {'name': 'Djibouti', 'code': 'DJ'},
        {'name': 'Somalie', 'code': 'SO'},
        {'name': 'Kenya', 'code': 'KE'},
        {'name': 'Ouganda', 'code': 'UG'},
        {'name': 'Rwanda', 'code': 'RW'},
        {'name': 'Burundi', 'code': 'BI'},
        {'name': 'Tanzanie', 'code': 'TZ'},
        {'name': 'Malawi', 'code': 'MW'},
        {'name': 'Mozambique', 'code': 'MZ'},
        {'name': 'Zimbabwe', 'code': 'ZW'},
        {'name': 'Zambie', 'code': 'ZM'},
        {'name': 'Botswana', 'code': 'BW'},
        {'name': 'Namibie', 'code': 'NA'},
        {'name': 'Afrique du Sud', 'code': 'ZA'},
        {'name': 'Lesotho', 'code': 'LS'},
        {'name': 'Eswatini', 'code': 'SZ'},
        {'name': 'Madagascar', 'code': 'MG'},
        {'name': 'Maurice', 'code': 'MU'},
        {'name': 'Comores', 'code': 'KM'},
        {'name': 'Seychelles', 'code': 'SC'},
        {'name': 'Cap-Vert', 'code': 'CV'},
        {'name': 'São Tomé-et-Príncipe', 'code': 'ST'},
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
        {'name': 'Salé', 'code': 'SAL'},
        {'name': 'Kenitra', 'code': 'KEN'},
        {'name': 'El Jadida', 'code': 'ELJ'},
    ]
    
    for data in cities_data:
        if not City.query.filter_by(code=data['code']).first():
            city = City(**data)
            db.session.add(city)
    
    print("Seeding talents...")
    talents_data = [
        # Construction
        {'name': 'Maçonnerie', 'emoji': '🧱', 'category': 'Construction'},
        {'name': 'Carrelage', 'emoji': '⬜', 'category': 'Construction'},
        {'name': 'Plomberie', 'emoji': '🔧', 'category': 'Construction'},
        {'name': 'Électricité', 'emoji': '⚡', 'category': 'Construction'},
        {'name': 'Menuiserie', 'emoji': '🪚', 'category': 'Construction'},
        {'name': 'Peinture', 'emoji': '🎨', 'category': 'Construction'},
        {'name': 'Soudure', 'emoji': '🔥', 'category': 'Construction'},
        {'name': 'Ferronnerie', 'emoji': '⚒️', 'category': 'Construction'},
        {'name': 'Charpenterie', 'emoji': '🪵', 'category': 'Construction'},
        {'name': 'Toiture', 'emoji': '🏠', 'category': 'Construction'},
        {'name': 'Isolation', 'emoji': '🧰', 'category': 'Construction'},
        {'name': 'Climatisation', 'emoji': '❄️', 'category': 'Construction'},
        
        # Restauration
        {'name': 'Cuisine', 'emoji': '🍳', 'category': 'Restauration'},
        {'name': 'Pâtisserie', 'emoji': '🧁', 'category': 'Restauration'},
        {'name': 'Boulangerie', 'emoji': '🥖', 'category': 'Restauration'},
        {'name': 'Serveur', 'emoji': '🍽️', 'category': 'Restauration'},
        {'name': 'Barista', 'emoji': '☕', 'category': 'Restauration'},
        {'name': 'Chef cuisine', 'emoji': '👨‍🍳', 'category': 'Restauration'},
        
        # Technologie
        {'name': 'Développement Web', 'emoji': '🖥️', 'category': 'Technologie'},
        {'name': 'Développement Mobile', 'emoji': '📱', 'category': 'Technologie'},
        {'name': 'Data Science', 'emoji': '📊', 'category': 'Technologie'},
        {'name': 'IA/ML', 'emoji': '🤖', 'category': 'Technologie'},
        {'name': 'Cybersécurité', 'emoji': '🔒', 'category': 'Technologie'},
        {'name': 'DevOps', 'emoji': '⚙️', 'category': 'Technologie'},
        {'name': 'Maintenance IT', 'emoji': '💻', 'category': 'Technologie'},
        {'name': 'Réseaux', 'emoji': '🌐', 'category': 'Technologie'},
        
        # Créatif & Design
        {'name': 'Graphisme', 'emoji': '🖌️', 'category': 'Créatif'},
        {'name': 'UI/UX Design', 'emoji': '📐', 'category': 'Créatif'},
        {'name': 'Illustration', 'emoji': '✏️', 'category': 'Créatif'},
        {'name': 'Animation 3D', 'emoji': '🎬', 'category': 'Créatif'},
        {'name': 'Motion Design', 'emoji': '🎞️', 'category': 'Créatif'},
        
        # Médias & Communication
        {'name': 'Photographie', 'emoji': '📸', 'category': 'Médias'},
        {'name': 'Vidéographie', 'emoji': '🎥', 'category': 'Médias'},
        {'name': 'Montage vidéo', 'emoji': '🎬', 'category': 'Médias'},
        {'name': 'Rédaction', 'emoji': '📝', 'category': 'Médias'},
        {'name': 'Journalisme', 'emoji': '📰', 'category': 'Médias'},
        
        # Marketing
        {'name': 'Community Management', 'emoji': '📣', 'category': 'Marketing'},
        {'name': 'SEO/SEA', 'emoji': '🔍', 'category': 'Marketing'},
        {'name': 'Marketing digital', 'emoji': '📈', 'category': 'Marketing'},
        {'name': 'Content Marketing', 'emoji': '✍️', 'category': 'Marketing'},
        {'name': 'Email Marketing', 'emoji': '📧', 'category': 'Marketing'},
        
        # Artistique
        {'name': 'Musique', 'emoji': '🎶', 'category': 'Artistique'},
        {'name': 'Chant', 'emoji': '🎤', 'category': 'Artistique'},
        {'name': 'Danse', 'emoji': '💃', 'category': 'Artistique'},
        {'name': 'Théâtre', 'emoji': '🎭', 'category': 'Artistique'},
        {'name': 'Mannequinat', 'emoji': '👗', 'category': 'Artistique'},
        {'name': 'Comédie', 'emoji': '😂', 'category': 'Artistique'},
        
        # Services
        {'name': 'Ménage', 'emoji': '🧹', 'category': 'Services'},
        {'name': 'Jardinage', 'emoji': '🌱', 'category': 'Services'},
        {'name': 'Garde d\'enfants', 'emoji': '👶', 'category': 'Services'},
        {'name': 'Aide à domicile', 'emoji': '🏡', 'category': 'Services'},
        {'name': 'Coiffure', 'emoji': '💇', 'category': 'Services'},
        {'name': 'Esthétique', 'emoji': '💅', 'category': 'Services'},
        
        # Transport
        {'name': 'Chauffeur', 'emoji': '🚗', 'category': 'Transport'},
        {'name': 'Livreur', 'emoji': '🏍️', 'category': 'Transport'},
        {'name': 'Taxi', 'emoji': '🚕', 'category': 'Transport'},
        
        # Éducation
        {'name': 'Enseignant', 'emoji': '👩‍🏫', 'category': 'Éducation'},
        {'name': 'Formation professionnelle', 'emoji': '📚', 'category': 'Éducation'},
        {'name': 'Cours particuliers', 'emoji': '✏️', 'category': 'Éducation'},
        {'name': 'Coaching', 'emoji': '🎯', 'category': 'Éducation'},
        
        # Santé
        {'name': 'Infirmier', 'emoji': '💉', 'category': 'Santé'},
        {'name': 'Aide-soignant', 'emoji': '🩺', 'category': 'Santé'},
        {'name': 'Pharmacien', 'emoji': '💊', 'category': 'Santé'},
        
        # Commerce
        {'name': 'Vente', 'emoji': '🛍️', 'category': 'Commerce'},
        {'name': 'Commerce', 'emoji': '🏪', 'category': 'Commerce'},
        {'name': 'Caissier', 'emoji': '💰', 'category': 'Commerce'},
        
        # Événementiel
        {'name': 'Organisation événements', 'emoji': '🎉', 'category': 'Événementiel'},
        {'name': 'Animation', 'emoji': '🎈', 'category': 'Événementiel'},
        {'name': 'DJ', 'emoji': '🎧', 'category': 'Événementiel'},
        
        # Bureautique
        {'name': 'Secrétariat', 'emoji': '📋', 'category': 'Bureautique'},
        {'name': 'Comptabilité', 'emoji': '🧮', 'category': 'Bureautique'},
        {'name': 'Ressources Humaines', 'emoji': '👥', 'category': 'Bureautique'},
        {'name': 'Gestion de projet', 'emoji': '📊', 'category': 'Bureautique'},
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
