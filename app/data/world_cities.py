"""
Villes principales par pays pour le formulaire CINEMA
Liste des principales villes pour les pays les plus utilisés
"""

WORLD_CITIES = {
    # Maroc (MA)
    'MA': [
        'Agadir', 'Casablanca', 'Essaouira', 'Fès', 'Marrakech',
        'Meknès', 'Oujda', 'Rabat', 'Tanger', 'Tétouan'
    ],
    
    # France (FR)
    'FR': [
        'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice',
        'Nantes', 'Bordeaux', 'Lille', 'Strasbourg', 'Rennes'
    ],
    
    # États-Unis (US)
    'US': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Francisco'
    ],
    
    # Canada (CA)
    'CA': [
        'Toronto', 'Montréal', 'Vancouver', 'Calgary', 'Ottawa',
        'Edmonton', 'Winnipeg', 'Québec', 'Hamilton', 'Kitchener'
    ],
    
    # Royaume-Uni (GB)
    'GB': [
        'Londres', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow',
        'Liverpool', 'Newcastle', 'Sheffield', 'Bristol', 'Édimbourg'
    ],
    
    # Allemagne (DE)
    'DE': [
        'Berlin', 'Munich', 'Hambourg', 'Cologne', 'Francfort',
        'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig'
    ],
    
    # Espagne (ES)
    'ES': [
        'Madrid', 'Barcelone', 'Valence', 'Séville', 'Saragosse',
        'Malaga', 'Murcie', 'Palma de Majorque', 'Las Palmas', 'Bilbao'
    ],
    
    # Italie (IT)
    'IT': [
        'Rome', 'Milan', 'Naples', 'Turin', 'Palerme',
        'Gênes', 'Bologne', 'Florence', 'Bari', 'Catane'
    ],
    
    # Belgique (BE)
    'BE': [
        'Bruxelles', 'Anvers', 'Gand', 'Charleroi', 'Liège',
        'Bruges', 'Namur', 'Louvain', 'Mons', 'Malines'
    ],
    
    # Suisse (CH)
    'CH': [
        'Zurich', 'Genève', 'Bâle', 'Lausanne', 'Berne',
        'Winterthour', 'Lucerne', 'St-Gall', 'Lugano', 'Bienne'
    ],
    
    # Pays-Bas (NL)
    'NL': [
        'Amsterdam', 'Rotterdam', 'La Haye', 'Utrecht', 'Eindhoven',
        'Groningue', 'Tilburg', 'Almere', 'Breda', 'Nimègue'
    ],
    
    # Algérie (DZ)
    'DZ': [
        'Alger', 'Oran', 'Constantine', 'Annaba', 'Blida',
        'Batna', 'Sétif', 'Sidi Bel Abbès', 'Biskra', 'Tébessa'
    ],
    
    # Tunisie (TN)
    'TN': [
        'Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte',
        'Gabès', 'Ariana', 'Gafsa', 'Monastir', 'Ben Arous'
    ],
    
    # Sénégal (SN)
    'SN': [
        'Dakar', 'Touba', 'Thiès', 'Kaolack', 'Saint-Louis',
        'Ziguinchor', 'Diourbel', 'Louga', 'Tambacounda', 'Mbour'
    ],
    
    # Côte d\'Ivoire (CI)
    'CI': [
        'Abidjan', 'Yamoussoukro', 'Bouaké', 'Daloa', 'San-Pédro',
        'Korhogo', 'Man', 'Divo', 'Gagnoa', 'Abengourou'
    ],
    
    # Cameroun (CM)
    'CM': [
        'Douala', 'Yaoundé', 'Garoua', 'Bamenda', 'Bafoussam',
        'Nkongsamba', 'Ngaoundéré', 'Bertoua', 'Maroua', 'Kumba'
    ],
    
    # Nigéria (NG)
    'NG': [
        'Lagos', 'Kano', 'Ibadan', 'Abuja', 'Port Harcourt',
        'Benin City', 'Kaduna', 'Maiduguri', 'Zaria', 'Aba'
    ],
    
    # Ghana (GH)
    'GH': [
        'Accra', 'Kumasi', 'Tamale', 'Sekondi-Takoradi', 'Ashaiman',
        'Sunyani', 'Cape Coast', 'Obuasi', 'Teshie', 'Tema'
    ],
    
    # Kenya (KE)
    'KE': [
        'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret',
        'Ruiru', 'Kikuyu', 'Kangundo-Tala', 'Malindi', 'Naivasha'
    ],
    
    # Afrique du Sud (ZA)
    'ZA': [
        'Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth',
        'Bloemfontein', 'East London', 'Polokwane', 'Nelspruit', 'Kimberley'
    ],
    
    # Égypte (EG)
    'EG': [
        'Le Caire', 'Alexandrie', 'Gizeh', 'Shubra El-Kheima', 'Port-Saïd',
        'Suez', 'Louxor', 'Mansourah', 'El-Mahalla El-Kubra', 'Tanta'
    ],
    
    # Émirats arabes unis (AE)
    'AE': [
        'Dubaï', 'Abou Dabi', 'Charjah', 'Al Aïn', 'Ajman',
        'Ras el Khaïmah', 'Fujaïrah', 'Umm al Qaïwaïn', 'Khor Fakkan', 'Dibba Al-Fujairah'
    ],
    
    # Arabie saoudite (SA)
    'SA': [
        'Riyad', 'Djeddah', 'La Mecque', 'Médine', 'Dammam',
        'Taëf', 'Tabuk', 'Buraydah', 'Khobar', 'Khamis Mushait'
    ],
    
    # Brésil (BR)
    'BR': [
        'São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza',
        'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre'
    ],
    
    # Chine (CN)
    'CN': [
        'Pékin', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu',
        'Tianjin', 'Wuhan', 'Hangzhou', 'Chongqing', 'Xi\'an'
    ],
    
    # Inde (IN)
    'IN': [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad',
        'Chennai', 'Kolkata', 'Surat', 'Pune', 'Jaipur'
    ],
    
    # Japon (JP)
    'JP': [
        'Tokyo', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo',
        'Fukuoka', 'Kobe', 'Kyoto', 'Kawasaki', 'Saitama'
    ],
    
    # Australie (AU)
    'AU': [
        'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adélaïde',
        'Gold Coast', 'Canberra', 'Newcastle', 'Wollongong', 'Logan City'
    ],
    
    # Mexique (MX)
    'MX': [
        'Mexico', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana',
        'León', 'Juárez', 'Zapopan', 'Mérida', 'San Luis Potosí'
    ],
    
    # Argentine (AR)
    'AR': [
        'Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata',
        'San Miguel de Tucumán', 'Mar del Plata', 'Salta', 'Santa Fe', 'San Juan'
    ],
    
    # Turquie (TR)
    'TR': [
        'Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Adana',
        'Gaziantep', 'Konya', 'Antalya', 'Kayseri', 'Mersin'
    ],
}

def get_cities_by_country(country_code):
    """
    Récupère la liste des villes pour un pays donné
    
    Args:
        country_code: Code ISO-2 du pays (ex: 'MA', 'FR', 'US')
    
    Returns:
        Liste des villes ou liste vide si le pays n'a pas de villes définies
    """
    return WORLD_CITIES.get(country_code, [])
