"""
TalentsMaroc.com
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
"""

"""
Villes principales par pays pour le formulaire CINEMA
Liste des principales villes pour les pays les plus utilisés
"""

WORLD_CITIES = {
    # Maroc (MA)
    'MA': [
        'Agadir', 'Al Hoceïma', 'Beni Mellal', 'Casablanca', 'Chefchaouen', 
        'El Jadida', 'Essaouira', 'Fès', 'Ifrane', 'Kénitra',
        'Khouribga', 'Larache', 'Marrakech', 'Meknès', 'Mohammedia',
        'Nador', 'Ouarzazate', 'Oujda', 'Rabat', 'Safi',
        'Salé', 'Tanger', 'Taroudant', 'Taza', 'Tétouan'
    ],
    
    # France (FR)
    'FR': [
        'Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice',
        'Nantes', 'Bordeaux', 'Lille', 'Strasbourg', 'Rennes',
        'Reims', 'Le Havre', 'Saint-Étienne', 'Toulon', 'Grenoble',
        'Dijon', 'Angers', 'Nîmes', 'Villeurbanne', 'Clermont-Ferrand',
        'Le Mans', 'Aix-en-Provence', 'Brest', 'Tours', 'Amiens'
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
        'Batna', 'Sétif', 'Sidi Bel Abbès', 'Biskra', 'Tébessa',
        'Djelfa', 'Béjaïa', 'Tlemcen', 'Tiaret', 'Béchar',
        'Skikda', 'Chlef', 'Mostaganem', 'El Oued', 'Bordj Bou Arreridj'
    ],
    
    # Tunisie (TN)
    'TN': [
        'Tunis', 'Sfax', 'Sousse', 'Kairouan', 'Bizerte',
        'Gabès', 'Ariana', 'Gafsa', 'Monastir', 'Ben Arous',
        'Nabeul', 'Médenine', 'Kasserine', 'La Marsa', 'Hammamet',
        'Tozeur', 'Mahdia', 'Béja', 'Jendouba', 'Kébili'
    ],
    
    # Sénégal (SN)
    'SN': [
        'Dakar', 'Touba', 'Thiès', 'Kaolack', 'Saint-Louis',
        'Ziguinchor', 'Diourbel', 'Louga', 'Tambacounda', 'Mbour',
        'Rufisque', 'Kolda', 'Richard-Toll', 'Sédhiou', 'Matam',
        'Fatick', 'Kaffrine', 'Kédougou', 'Linguère', 'Podor'
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
        'Gaziantep', 'Konya', 'Antalya', 'Kayseri', 'Mersin',
        'Eskişehir', 'Diyarbakır', 'Samsun', 'Denizli', 'Şanlıurfa'
    ],
    
    # Mali (ML)
    'ML': [
        'Bamako', 'Sikasso', 'Mopti', 'Koutiala', 'Kayes',
        'Ségou', 'Gao', 'Tombouctou', 'Kidal', 'Kati'
    ],
    
    # Burkina Faso (BF)
    'BF': [
        'Ouagadougou', 'Bobo-Dioulasso', 'Koudougou', 'Ouahigouya', 'Banfora',
        'Dédougou', 'Kaya', 'Tenkodogo', 'Fada N\'gourma', 'Houndé'
    ],
    
    # Niger (NE)
    'NE': [
        'Niamey', 'Zinder', 'Maradi', 'Agadez', 'Tahoua',
        'Dosso', 'Diffa', 'Tillabéri', 'Arlit', 'Tessaoua'
    ],
    
    # Tchad (TD)
    'TD': [
        'N\'Djamena', 'Moundou', 'Abéché', 'Sarh', 'Kélo',
        'Koumra', 'Pala', 'Am Timan', 'Bongor', 'Doba'
    ],
    
    # Mauritanie (MR)
    'MR': [
        'Nouakchott', 'Nouadhibou', 'Néma', 'Kaédi', 'Rosso',
        'Zouérat', 'Kiffa', 'Atar', 'Sélibaby', 'Aleg'
    ],
    
    # Guinée (GN)
    'GN': [
        'Conakry', 'Nzérékoré', 'Kankan', 'Kindia', 'Labé',
        'Kamsar', 'Guéckédou', 'Kissidougou', 'Macenta', 'Mamou'
    ],
    
    # Bénin (BJ)
    'BJ': [
        'Cotonou', 'Porto-Novo', 'Parakou', 'Djougou', 'Bohicon',
        'Kandi', 'Abomey', 'Lokossa', 'Ouidah', 'Savalou'
    ],
    
    # Togo (TG)
    'TG': [
        'Lomé', 'Sokodé', 'Kara', 'Kpalimé', 'Atakpamé',
        'Bassar', 'Tsévié', 'Aného', 'Sansanné-Mango', 'Dapaong'
    ],
    
    # Rwanda (RW)
    'RW': [
        'Kigali', 'Butare', 'Gitarama', 'Ruhengeri', 'Gisenyi',
        'Byumba', 'Cyangugu', 'Kibungo', 'Kibuye', 'Nyanza'
    ],
    
    # Éthiopie (ET)
    'ET': [
        'Addis-Abeba', 'Dire Dawa', 'Mekele', 'Gondar', 'Bahir Dar',
        'Awasa', 'Dessie', 'Jimma', 'Jijiga', 'Harar'
    ],
    
    # Ouganda (UG)
    'UG': [
        'Kampala', 'Gulu', 'Lira', 'Mbarara', 'Jinja',
        'Mbale', 'Mukono', 'Kasese', 'Masaka', 'Entebbe'
    ],
    
    # Tanzanie (TZ)
    'TZ': [
        'Dar es Salaam', 'Mwanza', 'Dodoma', 'Arusha', 'Mbeya',
        'Morogoro', 'Tanga', 'Zanzibar', 'Kigoma', 'Tabora'
    ],
    
    # Madagascar (MG)
    'MG': [
        'Antananarivo', 'Toamasina', 'Antsirabe', 'Fianarantsoa', 'Mahajanga',
        'Toliara', 'Antsiranana', 'Ambovombe', 'Morondava', 'Manakara'
    ],
    
    # Congo-Brazzaville (CG)
    'CG': [
        'Brazzaville', 'Pointe-Noire', 'Dolisie', 'Nkayi', 'Owando',
        'Ouesso', 'Impfondo', 'Sibiti', 'Madingou', 'Kinkala'
    ],
    
    # RDC (CD)
    'CD': [
        'Kinshasa', 'Lubumbashi', 'Mbuji-Mayi', 'Kananga', 'Kisangani',
        'Bukavu', 'Tshikapa', 'Kolwezi', 'Likasi', 'Goma'
    ],
    
    # Angola (AO)
    'AO': [
        'Luanda', 'Huambo', 'Lobito', 'Benguela', 'Lubango',
        'Kuito', 'Malanje', 'Namibe', 'Soyo', 'Cabinda'
    ],
    
    # Mozambique (MZ)
    'MZ': [
        'Maputo', 'Matola', 'Beira', 'Nampula', 'Chimoio',
        'Quelimane', 'Tete', 'Nacala', 'Pemba', 'Inhambane'
    ],
    
    # Zimbabwe (ZW)
    'ZW': [
        'Harare', 'Bulawayo', 'Chitungwiza', 'Mutare', 'Gweru',
        'Kwekwe', 'Kadoma', 'Masvingo', 'Chinhoyi', 'Norton'
    ],
    
    # Zambie (ZM)
    'ZM': [
        'Lusaka', 'Kitwe', 'Ndola', 'Kabwe', 'Chingola',
        'Mufulira', 'Livingstone', 'Luanshya', 'Kasama', 'Chipata'
    ],
    
    # Botswana (BW)
    'BW': [
        'Gaborone', 'Francistown', 'Molepolole', 'Maun', 'Selebi-Phikwe',
        'Serowe', 'Kanye', 'Mochudi', 'Mahalapye', 'Palapye'
    ],
    
    # Liban (LB)
    'LB': [
        'Beyrouth', 'Tripoli', 'Sidon', 'Tyr', 'Zahlé',
        'Jounieh', 'Baalbek', 'Nabatieh', 'Baabda', 'Byblos'
    ],
    
    # Jordanie (JO)
    'JO': [
        'Amman', 'Zarqa', 'Irbid', 'Aqaba', 'Russeifa',
        'Wadi Musa', 'Madaba', 'Jerash', 'Salt', 'Karak'
    ],
    
    # Qatar (QA)
    'QA': [
        'Doha', 'Al Rayyan', 'Umm Salal Mohammed', 'Al Wakrah', 'Al Khor',
        'Al Shamal', 'Dukhan', 'Mesaieed', 'Al Shahaniya', 'Madinat ash Shamal'
    ],
    
    # Koweït (KW)
    'KW': [
        'Koweït City', 'Hawalli', 'Salmiya', 'Sabah Al Salem', 'Al Farwaniyah',
        'Al Ahmadi', 'Al Jahra', 'Fintas', 'Fahaheel', 'Mangaf'
    ],
    
    # Portugal (PT)
    'PT': [
        'Lisbonne', 'Porto', 'Amadora', 'Braga', 'Setúbal',
        'Coimbra', 'Funchal', 'Aveiro', 'Faro', 'Viseu'
    ],
    
    # Pologne (PL)
    'PL': [
        'Varsovie', 'Cracovie', 'Łódź', 'Wrocław', 'Poznań',
        'Gdańsk', 'Szczecin', 'Bydgoszcz', 'Lublin', 'Katowice'
    ],
    
    # Roumanie (RO)
    'RO': [
        'Bucarest', 'Cluj-Napoca', 'Timișoara', 'Iași', 'Constanța',
        'Craiova', 'Brașov', 'Galați', 'Ploiești', 'Oradea'
    ],
    
    # Grèce (GR)
    'GR': [
        'Athènes', 'Thessalonique', 'Patras', 'Héraklion', 'Larissa',
        'Volos', 'Rhodes', 'Ioannina', 'Chania', 'Chalcis'
    ],
    
    # Suède (SE)
    'SE': [
        'Stockholm', 'Göteborg', 'Malmö', 'Uppsala', 'Västerås',
        'Örebro', 'Linköping', 'Helsingborg', 'Norrköping', 'Jönköping'
    ],
    
    # Norvège (NO)
    'NO': [
        'Oslo', 'Bergen', 'Stavanger', 'Trondheim', 'Drammen',
        'Fredrikstad', 'Kristiansand', 'Sandnes', 'Tromsø', 'Sarpsborg'
    ],
    
    # Danemark (DK)
    'DK': [
        'Copenhague', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg',
        'Randers', 'Kolding', 'Horsens', 'Vejle', 'Roskilde'
    ],
    
    # Finlande (FI)
    'FI': [
        'Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Oulu',
        'Turku', 'Jyväskylä', 'Lahti', 'Kuopio', 'Pori'
    ],
    
    # Autriche (AT)
    'AT': [
        'Vienne', 'Graz', 'Linz', 'Salzbourg', 'Innsbruck',
        'Klagenfurt', 'Villach', 'Wels', 'Sankt Pölten', 'Dornbirn'
    ],
    
    # Irlande (IE)
    'IE': [
        'Dublin', 'Cork', 'Limerick', 'Galway', 'Waterford',
        'Drogheda', 'Dundalk', 'Swords', 'Bray', 'Navan'
    ],
    
    # République Tchèque (CZ)
    'CZ': [
        'Prague', 'Brno', 'Ostrava', 'Plzeň', 'Liberec',
        'Olomouc', 'České Budějovice', 'Hradec Králové', 'Ústí nad Labem', 'Pardubice'
    ],
    
    # Hongrie (HU)
    'HU': [
        'Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pécs',
        'Győr', 'Nyíregyháza', 'Kecskemét', 'Székesfehérvár', 'Szombathely'
    ],
    
    # Thaïlande (TH)
    'TH': [
        'Bangkok', 'Nonthaburi', 'Pak Kret', 'Hat Yai', 'Chiang Mai',
        'Khon Kaen', 'Udon Thani', 'Nakhon Ratchasima', 'Pattaya', 'Phuket'
    ],
    
    # Vietnam (VN)
    'VN': [
        'Hô Chi Minh-Ville', 'Hanoï', 'Hai Phong', 'Da Nang', 'Bien Hoa',
        'Nha Trang', 'Hue', 'Can Tho', 'Vung Tau', 'Buon Ma Thuot'
    ],
    
    # Philippines (PH)
    'PH': [
        'Manille', 'Quezon City', 'Davao', 'Caloocan', 'Cebu',
        'Zamboanga', 'Antipolo', 'Pasig', 'Taguig', 'Cagayan de Oro'
    ],
    
    # Malaisie (MY)
    'MY': [
        'Kuala Lumpur', 'George Town', 'Ipoh', 'Shah Alam', 'Petaling Jaya',
        'Johor Bahru', 'Malacca', 'Kota Kinabalu', 'Kuching', 'Seremban'
    ],
    
    # Singapour (SG)
    'SG': [
        'Singapour', 'Jurong West', 'Woodlands', 'Tampines', 'Bedok',
        'Sengkang', 'Hougang', 'Yishun', 'Ang Mo Kio', 'Bukit Batok'
    ],
    
    # Indonésie (ID)
    'ID': [
        'Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang',
        'Palembang', 'Makassar', 'Tangerang', 'Bekasi', 'Depok'
    ],
    
    # Corée du Sud (KR)
    'KR': [
        'Séoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon',
        'Gwangju', 'Suwon', 'Ulsan', 'Goyang', 'Yongin'
    ],
    
    # Nouvelle-Zélande (NZ)
    'NZ': [
        'Auckland', 'Wellington', 'Christchurch', 'Hamilton', 'Tauranga',
        'Napier-Hastings', 'Dunedin', 'Palmerston North', 'Nelson', 'Rotorua'
    ],
    
    # Chili (CL)
    'CL': [
        'Santiago', 'Valparaíso', 'Concepción', 'La Serena', 'Antofagasta',
        'Temuco', 'Rancagua', 'Talca', 'Arica', 'Chillán'
    ],
    
    # Colombie (CO)
    'CO': [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
        'Cúcuta', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Ibagué'
    ],
    
    # Pérou (PE)
    'PE': [
        'Lima', 'Arequipa', 'Trujillo', 'Chiclayo', 'Piura',
        'Iquitos', 'Cusco', 'Huancayo', 'Tacna', 'Ica'
    ],
    
    # Équateur (EC)
    'EC': [
        'Guayaquil', 'Quito', 'Cuenca', 'Santo Domingo', 'Machala',
        'Durán', 'Manta', 'Portoviejo', 'Loja', 'Ambato'
    ],
    
    # Venezuela (VE)
    'VE': [
        'Caracas', 'Maracaibo', 'Valencia', 'Barquisimeto', 'Maracay',
        'Ciudad Guayana', 'Barcelona', 'Maturín', 'San Cristóbal', 'Ciudad Bolívar'
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
