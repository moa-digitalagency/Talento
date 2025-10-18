from app import create_app, db
from app.models.location import Country, City

app = create_app()

with app.app_context():
    print("Ajout des nouvelles villes marocaines...")
    new_cities = [
        {'name': 'Al Hoceima', 'code': 'HOC'},
        {'name': 'Asilah', 'code': 'ASI'},
        {'name': 'Azrou', 'code': 'AZR'},
        {'name': 'Beni Mellal', 'code': 'BEN'},
        {'name': 'Berkane', 'code': 'BER'},
        {'name': 'Chefchaouen', 'code': 'CHE'},
        {'name': 'Dakhla', 'code': 'DAK'},
        {'name': 'Errachidia', 'code': 'ERR'},
        {'name': 'Essaouira', 'code': 'ESS'},
        {'name': 'Guelmim', 'code': 'GUE'},
        {'name': 'Ifrane', 'code': 'IFR'},
        {'name': 'Khémisset', 'code': 'KHE'},
        {'name': 'Khouribga', 'code': 'KHO'},
        {'name': 'Ksar El Kebir', 'code': 'KSA'},
        {'name': 'Larache', 'code': 'LAR'},
        {'name': 'Laâyoune', 'code': 'LAA'},
        {'name': 'Mohammedia', 'code': 'MOH'},
        {'name': 'Nador', 'code': 'NAD'},
        {'name': 'Ouarzazate', 'code': 'OUA'},
        {'name': 'Safi', 'code': 'SAF'},
        {'name': 'Sefrou', 'code': 'SEF'},
        {'name': 'Settat', 'code': 'SET'},
        {'name': 'Sidi Ifni', 'code': 'SID'},
        {'name': 'Sidi Kacem', 'code': 'SIK'},
        {'name': 'Taroudant', 'code': 'TAR'},
        {'name': 'Taza', 'code': 'TAZ'},
        {'name': 'Témara', 'code': 'TEM'},
        {'name': 'Tiznit', 'code': 'TIZ'},
    ]
    
    for data in new_cities:
        if not City.query.filter_by(code=data['code']).first():
            city = City(**data)
            db.session.add(city)
            print(f"  Ajouté: {data['name']}")
    
    db.session.commit()
    print("Villes ajoutées avec succès!")
    
    print(f"\nTotal villes: {City.query.count()}")
    print(f"Total pays: {Country.query.count()}")
