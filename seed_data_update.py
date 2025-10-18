from app import create_app, db
from app.models.location import Country, City

app = create_app()

with app.app_context():
    # Supprimer les anciennes données
    City.query.delete()
    Country.query.delete()
    
    print("Mise à jour des pays africains (ordre alphabétique)...")
    countries_data = [
        {'name': 'Afrique du Sud', 'code': 'ZA'},
        {'name': 'Algérie', 'code': 'DZ'},
        {'name': 'Angola', 'code': 'AO'},
        {'name': 'Bénin', 'code': 'BJ'},
        {'name': 'Botswana', 'code': 'BW'},
        {'name': 'Burkina Faso', 'code': 'BF'},
        {'name': 'Burundi', 'code': 'BI'},
        {'name': 'Cameroun', 'code': 'CM'},
        {'name': 'Cap-Vert', 'code': 'CV'},
        {'name': 'Comores', 'code': 'KM'},
        {'name': 'Congo', 'code': 'CG'},
        {'name': 'Côte d\'Ivoire', 'code': 'CI'},
        {'name': 'Djibouti', 'code': 'DJ'},
        {'name': 'Égypte', 'code': 'EG'},
        {'name': 'Érythrée', 'code': 'ER'},
        {'name': 'Eswatini', 'code': 'SZ'},
        {'name': 'Éthiopie', 'code': 'ET'},
        {'name': 'Gabon', 'code': 'GA'},
        {'name': 'Gambie', 'code': 'GM'},
        {'name': 'Ghana', 'code': 'GH'},
        {'name': 'Guinée', 'code': 'GN'},
        {'name': 'Guinée-Bissau', 'code': 'GW'},
        {'name': 'Guinée Équatoriale', 'code': 'GQ'},
        {'name': 'Kenya', 'code': 'KE'},
        {'name': 'Lesotho', 'code': 'LS'},
        {'name': 'Liberia', 'code': 'LR'},
        {'name': 'Libye', 'code': 'LY'},
        {'name': 'Madagascar', 'code': 'MG'},
        {'name': 'Malawi', 'code': 'MW'},
        {'name': 'Mali', 'code': 'ML'},
        {'name': 'Maroc', 'code': 'MA'},
        {'name': 'Maurice', 'code': 'MU'},
        {'name': 'Mauritanie', 'code': 'MR'},
        {'name': 'Mozambique', 'code': 'MZ'},
        {'name': 'Namibie', 'code': 'NA'},
        {'name': 'Niger', 'code': 'NE'},
        {'name': 'Nigéria', 'code': 'NG'},
        {'name': 'Ouganda', 'code': 'UG'},
        {'name': 'RD Congo', 'code': 'CD'},
        {'name': 'République Centrafricaine', 'code': 'CF'},
        {'name': 'Rwanda', 'code': 'RW'},
        {'name': 'São Tomé-et-Príncipe', 'code': 'ST'},
        {'name': 'Sénégal', 'code': 'SN'},
        {'name': 'Seychelles', 'code': 'SC'},
        {'name': 'Sierra Leone', 'code': 'SL'},
        {'name': 'Somalie', 'code': 'SO'},
        {'name': 'Soudan', 'code': 'SD'},
        {'name': 'Soudan du Sud', 'code': 'SS'},
        {'name': 'Tanzanie', 'code': 'TZ'},
        {'name': 'Tchad', 'code': 'TD'},
        {'name': 'Togo', 'code': 'TG'},
        {'name': 'Tunisie', 'code': 'TN'},
        {'name': 'Zambie', 'code': 'ZM'},
        {'name': 'Zimbabwe', 'code': 'ZW'},
    ]
    
    for data in countries_data:
        country = Country(**data)
        db.session.add(country)
    
    print("Ajout de toutes les villes marocaines...")
    cities_data = [
        {'name': 'Agadir', 'code': 'AGA'},
        {'name': 'Al Hoceima', 'code': 'HOC'},
        {'name': 'Asilah', 'code': 'ASI'},
        {'name': 'Azrou', 'code': 'AZR'},
        {'name': 'Beni Mellal', 'code': 'BEN'},
        {'name': 'Berkane', 'code': 'BER'},
        {'name': 'Casablanca', 'code': 'CAS'},
        {'name': 'Chefchaouen', 'code': 'CHE'},
        {'name': 'Dakhla', 'code': 'DAK'},
        {'name': 'El Jadida', 'code': 'ELJ'},
        {'name': 'Errachidia', 'code': 'ERR'},
        {'name': 'Essaouira', 'code': 'ESS'},
        {'name': 'Fès', 'code': 'FES'},
        {'name': 'Guelmim', 'code': 'GUE'},
        {'name': 'Ifrane', 'code': 'IFR'},
        {'name': 'Kénitra', 'code': 'KEN'},
        {'name': 'Khémisset', 'code': 'KHE'},
        {'name': 'Khouribga', 'code': 'KHO'},
        {'name': 'Ksar El Kebir', 'code': 'KSA'},
        {'name': 'Larache', 'code': 'LAR'},
        {'name': 'Laâyoune', 'code': 'LAA'},
        {'name': 'Marrakech', 'code': 'MAR'},
        {'name': 'Meknès', 'code': 'MEK'},
        {'name': 'Mohammedia', 'code': 'MOH'},
        {'name': 'Nador', 'code': 'NAD'},
        {'name': 'Ouarzazate', 'code': 'OUA'},
        {'name': 'Oujda', 'code': 'OUJ'},
        {'name': 'Rabat', 'code': 'RAB'},
        {'name': 'Safi', 'code': 'SAF'},
        {'name': 'Salé', 'code': 'SAL'},
        {'name': 'Sefrou', 'code': 'SEF'},
        {'name': 'Settat', 'code': 'SET'},
        {'name': 'Sidi Ifni', 'code': 'SID'},
        {'name': 'Sidi Kacem', 'code': 'SIK'},
        {'name': 'Tanger', 'code': 'TNG'},
        {'name': 'Taroudant', 'code': 'TAR'},
        {'name': 'Taza', 'code': 'TAZ'},
        {'name': 'Témara', 'code': 'TEM'},
        {'name': 'Tétouan', 'code': 'TET'},
        {'name': 'Tiznit', 'code': 'TIZ'},
    ]
    
    for data in cities_data:
        city = City(**data)
        db.session.add(city)
    
    db.session.commit()
    print("Mise à jour terminée !")
