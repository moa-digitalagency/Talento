"""
taalentio.com
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
    

    # République centrafricaine (CF)
    "CF": ["Bangui", "Bimbo", "Berbérati", "Carnot", "Bambari", "Bouar", "Bossangoa", "Bria", "Bangassou", "Nola"],
    
    # Pakistan (PK)
    'PK': [
        'Karachi', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Multan',
        'Hyderabad', 'Gujranwala', 'Peshawar', 'Quetta', 'Islamabad',
        'Bahawalpur', 'Sargodha', 'Sialkot', 'Sukkur', 'Larkana'
    ],
    
    # Bangladesh (BD)
    'BD': [
        'Dhaka', 'Chittagong', 'Khulna', 'Rajshahi', 'Sylhet',
        'Rangpur', 'Barisal', 'Comilla', 'Narayanganj', 'Gazipur',
        'Mymensingh', 'Cox\'s Bazar', 'Jessore', 'Bogra', 'Dinajpur'
    ],
    
    # Russie (RU)
    'RU': [
        'Moscou', 'Saint-Pétersbourg', 'Novossibirsk', 'Ekaterinbourg', 'Kazan',
        'Nijni Novgorod', 'Tcheliabinsk', 'Samara', 'Omsk', 'Rostov-sur-le-Don',
        'Oufa', 'Krasnoïarsk', 'Voronej', 'Perm', 'Volgograd'
    ],
    
    # Iran (IR)
    'IR': [
        'Téhéran', 'Mashhad', 'Isfahan', 'Karaj', 'Tabriz',
        'Shiraz', 'Qom', 'Ahvaz', 'Kermanshah', 'Rasht',
        'Kerman', 'Orumiyeh', 'Zahedan', 'Hamedan', 'Yazd'
    ],
    
    # Irak (IQ)
    'IQ': [
        'Bagdad', 'Bassorah', 'Mossoul', 'Erbil', 'Souleïmaniye',
        'Kirkouk', 'Nadjaf', 'Kerbala', 'Hilla', 'Nasiriya',
        'Amarah', 'Diwaniya', 'Ramadi', 'Falloujah', 'Dahuk'
    ],
    
    # Syrie (SY)
    'SY': [
        'Damas', 'Alep', 'Homs', 'Hama', 'Lattaquié',
        'Deir ez-Zor', 'Raqqa', 'Idlib', 'Daraa', 'Al-Hasakah',
        'Qamishli', 'Tartous', 'Sweida', 'Manbij', 'Palmyre'
    ],
    
    # Afghanistan (AF)
    'AF': [
        'Kaboul', 'Kandahar', 'Herat', 'Mazar-e-Charif', 'Jalalabad',
        'Kunduz', 'Lashkar Gah', 'Taloqan', 'Puli Khumri', 'Ghazni',
        'Khost', 'Farah', 'Zaranj', 'Gardez', 'Bamyan'
    ],
    
    # Libye (LY)
    'LY': [
        'Tripoli', 'Benghazi', 'Misrata', 'Tobrouk', 'Sebha',
        'Syrte', 'Ajdabiya', 'Zaouïa', 'Al Marj', 'Derna',
        'Bayda', 'Zliten', 'Koufra', 'Gharyan', 'Toukra'
    ],
    
    # Soudan (SD)
    'SD': [
        'Khartoum', 'Omdurman', 'Khartoum Nord', 'Nyala', 'Port-Soudan',
        'El-Obeid', 'Kassala', 'Wad Madani', 'El Geneina', 'El Fasher',
        'Atbara', 'Gedaref', 'Kosti', 'Sennar', 'Dongola'
    ],
    
    # Ukraine (UA)
    'UA': [
        'Kiev', 'Kharkiv', 'Odessa', 'Dnipro', 'Donetsk',
        'Zaporijjia', 'Lviv', 'Kryvyï Rih', 'Mykolaïv', 'Marioupol',
        'Louhansk', 'Vinnytsia', 'Sébastopol', 'Simferopol', 'Kherson'
    ],
    
    # Maroc (déjà présent - ajouté plus haut)
    
    # Sri Lanka (LK)
    'LK': [
        'Colombo', 'Dehiwala-Mount Lavinia', 'Moratuwa', 'Negombo', 'Kandy',
        'Kalmunai', 'Vavuniya', 'Galle', 'Trincomalee', 'Batticaloa',
        'Jaffna', 'Katunayake', 'Dambulla', 'Kururenegala', 'Anuradhapura'
    ],
    
    # Myanmar (Birmanie) (MM)
    'MM': [
        'Rangoun', 'Mandalay', 'Naypyidaw', 'Mawlamyine', 'Bago',
        'Pathein', 'Monywa', 'Meiktila', 'Myeik', 'Sittwe',
        'Taunggyi', 'Magway', 'Lashio', 'Pyay', 'Hpa-An'
    ],
    
    # Népal (NP)
    'NP': [
        'Katmandou', 'Pokhara', 'Patan', 'Biratnagar', 'Birgunj',
        'Bharatpur', 'Dharan', 'Butwal', 'Hetauda', 'Janakpur',
        'Itahari', 'Bhaktapur', 'Dhangadhi', 'Lalitpur', 'Nepalgunj'
    ],
    
    # Kazakhstan (KZ)
    'KZ': [
        'Almaty', 'Astana', 'Chimkent', 'Aktobe', 'Taraz',
        'Pavlodar', 'Ust-Kamenogorsk', 'Karaganda', 'Semey', 'Atyrau',
        'Kostanay', 'Petropavl', 'Aktau', 'Temirtau', 'Turkestan'
    ],
    
    # Ouzbékistan (UZ)
    'UZ': [
        'Tachkent', 'Samarcande', 'Namangan', 'Andijan', 'Boukhara',
        'Noukous', 'Fergana', 'Karchi', 'Kokand', 'Margilan',
        'Tchirtchik', 'Navoï', 'Djizak', 'Ourguentch', 'Termez'
    ],
    
    # Azerbaïdjan (AZ)
    'AZ': [
        'Bakou', 'Gandja', 'Soumgaït', 'Mingatchevir', 'Khankendi',
        'Lankaran', 'Nakhitchevan', 'Sheki', 'Yevlakh', 'Shirvan',
        'Agdam', 'Qusar', 'Balakan', 'Qazax', 'Astara'
    ],
    
    # Géorgie (GE)
    'GE': [
        'Tbilissi', 'Koutaïssi', 'Batoumi', 'Roustavi', 'Zougdidi',
        'Gori', 'Poti', 'Soukhoumi', 'Khashuri', 'Samtredia',
        'Tskaltubo', 'Kobuleti', 'Telavi', 'Ozurgeti', 'Akhaltsikhe'
    ],
    
    # Arménie (AM)
    'AM': [
        'Erevan', 'Gyumri', 'Vanadzor', 'Vagharshapat', 'Hrazdan',
        'Abovyan', 'Kapan', 'Armavir', 'Gavar', 'Artashat',
        'Goris', 'Ashtarak', 'Sevan', 'Ijevan', 'Charentsavan'
    ],
    
    # Israël (IL)
    'IL': [
        'Jérusalem', 'Tel Aviv', 'Haïfa', 'Rishon LeZion', 'Petah Tikva',
        'Ashdod', 'Netanya', 'Beer Sheva', 'Holon', 'Bnei Brak',
        'Ramat Gan', 'Ashkelon', 'Rehovot', 'Bat Yam', 'Herzliya'
    ],
    
    # Palestine (PS)
    'PS': [
        'Gaza', 'Khan Younès', 'Rafah', 'Jabalia', 'Hébron',
        'Naplouse', 'Ramallah', 'Bethléem', 'Jéricho', 'Tulkarem',
        'Qalqilya', 'Jenine', 'Deir el-Balah', 'Beit Lahia', 'Beit Hanoun'
    ],
    
    # Yémen (YE)
    'YE': [
        'Sanaa', 'Aden', 'Taïz', 'Hodeïda', 'Ibb',
        'Dhamar', 'Mukalla', 'Saïoun', 'Zinjibar', 'Hajjah',
        'Amran', 'Saada', 'Marib', 'Al Bayda', 'Ataq'
    ],
    
    # Oman (OM)
    'OM': [
        'Mascate', 'Salala', 'Sohar', 'Nizwa', 'Sur',
        'Ibri', 'Barka', 'Rustaq', 'Al Buraimi', 'Saham',
        'Khasab', 'Bahla', 'Ibra', 'Suwaiq', 'Shinas'
    ],
    
    # Bahreïn (BH)
    'BH': [
        'Manama', 'Muharraq', 'Riffa', 'Hamad Town', 'Isa Town',
        'Sitra', 'Budaiya', 'Jidhafs', 'Al-Malikiyah', 'Dar Kulayb'
    ],
    
    # Bolivie (BO)
    'BO': [
        'La Paz', 'Santa Cruz de la Sierra', 'Cochabamba', 'Sucre', 'Oruro',
        'Tarija', 'Potosí', 'Sacaba', 'Montero', 'Trinidad',
        'El Alto', 'Quillacollo', 'Riberalta', 'Yacuiba', 'Warnes'
    ],
    
    # Paraguay (PY)
    'PY': [
        'Asunción', 'Ciudad del Este', 'San Lorenzo', 'Luque', 'Capiatá',
        'Lambaré', 'Fernando de la Mora', 'Limpio', 'Ñemby', 'Encarnación',
        'Mariano Roque Alonso', 'Pedro Juan Caballero', 'Itauguá', 'Villa Elisa', 'Caaguazú'
    ],
    
    # Uruguay (UY)
    'UY': [
        'Montevideo', 'Salto', 'Ciudad de la Costa', 'Paysandú', 'Las Piedras',
        'Rivera', 'Maldonado', 'Tacuarembó', 'Melo', 'Mercedes',
        'Artigas', 'Minas', 'San José de Mayo', 'Durazno', 'Florida'
    ],
    
    # Cuba (CU)
    'CU': [
        'La Havane', 'Santiago de Cuba', 'Camagüey', 'Holguín', 'Santa Clara',
        'Guantánamo', 'Las Tunas', 'Bayamo', 'Cienfuegos', 'Pinar del Río',
        'Matanzas', 'Ciego de Ávila', 'Sancti Spíritus', 'Manzanillo', 'Cárdenas'
    ],
    
    # Jamaïque (JM)
    'JM': [
        'Kingston', 'Spanish Town', 'Portmore', 'Montego Bay', 'May Pen',
        'Mandeville', 'Old Harbour', 'Savanna-la-Mar', 'Port Antonio', 'Linstead'
    ],
    
    # Panama (PA)
    'PA': [
        'Panama City', 'San Miguelito', 'Tocumen', 'David', 'Arraiján',
        'Colón', 'La Chorrera', 'Pacora', 'Santiago', 'Las Cumbres',
        'Vista Alegre', 'Chitré', 'Penonomé', 'Changuinola', 'Aguadulce'
    ],
    
    # Costa Rica (CR)
    'CR': [
        'San José', 'Limón', 'Alajuela', 'Heredia', 'Puntarenas',
        'Cartago', 'Liberia', 'Paraíso', 'Curridabat', 'San Isidro de El General',
        'Quesada', 'Desamparados', 'Pérez Zeledón', 'Goicoechea', 'Purral'
    ],
    
    # Nicaragua (NI)
    'NI': [
        'Managua', 'León', 'Masaya', 'Matagalpa', 'Chinandega',
        'Granada', 'Estelí', 'Tipitapa', 'Puerto Cabezas', 'Juigalpa',
        'Jinotepe', 'Bluefields', 'Nueva Guinea', 'Rivas', 'Ocotal'
    ],
    
    # Honduras (HN)
    'HN': [
        'Tegucigalpa', 'San Pedro Sula', 'La Ceiba', 'El Progreso', 'Choluteca',
        'Comayagua', 'Puerto Cortés', 'La Lima', 'Danlí', 'Siguatepeque',
        'Juticalpa', 'Tocoa', 'Olanchito', 'Cofradía', 'Villanueva'
    ],
    
    # Salvador (SV)
    'SV': [
        'San Salvador', 'Santa Ana', 'San Miguel', 'Mejicanos', 'Soyapango',
        'Santa Tecla', 'Apopa', 'Delgado', 'Ilopango', 'Sonsonate',
        'San Martín', 'Usulután', 'Cojutepeque', 'Ahuachapán', 'Chalatenango'
    ],
    
    # Guatemala (GT)
    'GT': [
        'Guatemala City', 'Mixco', 'Villa Nueva', 'Petapa', 'San Juan Sacatepéquez',
        'Quetzaltenango', 'Villa Canales', 'Escuintla', 'Chinautla', 'Chimaltenango',
        'Huehuetenango', 'Amatitlán', 'Totonicapán', 'Santa Lucía Cotzumalguapa', 'Puerto Barrios'
    ],
    
    # Haïti (HT)
    'HT': [
        'Port-au-Prince', 'Carrefour', 'Delmas', 'Cap-Haïtien', 'Pétionville',
        'Gonaïves', 'Saint-Marc', 'Les Cayes', 'Verrettes', 'Jacmel',
        'Port-de-Paix', 'Jérémie', 'Hinche', 'Léogâne', 'Petit-Goâve'
    ],
    
    # République Dominicaine (DO)
    'DO': [
        'Saint-Domingue', 'Santiago de los Caballeros', 'Santo Domingo Este', 'Santo Domingo Oeste', 'San Pedro de Macorís',
        'La Romana', 'San Cristóbal', 'Puerto Plata', 'San Francisco de Macorís', 'Higüey',
        'La Vega', 'Baní', 'Bonao', 'Moca', 'San Juan de la Maguana'
    ],
    
    # Trinité-et-Tobago (TT)
    'TT': [
        'Port of Spain', 'Chaguanas', 'San Fernando', 'Arima', 'Marabella',
        'Point Fortin', 'Tunapuna', 'San Juan', 'Couva', 'Scarborough'
    ],
    
    # Albanie (AL)
    'AL': [
        'Tirana', 'Durrës', 'Vlorë', 'Elbasan', 'Shkodër',
        'Fier', 'Korçë', 'Berat', 'Lushnjë', 'Kavajë',
        'Pogradec', 'Laç', 'Kukës', 'Gjirokastër', 'Sarandë'
    ],
    
    # Macédoine du Nord (MK)
    'MK': [
        'Skopje', 'Bitola', 'Kumanovo', 'Prilep', 'Tetovo',
        'Veles', 'Ohrid', 'Gostivar', 'Strumica', 'Štip',
        'Kavadarci', 'Struga', 'Kičevo', 'Radoviš', 'Gevgelija'
    ],
    
    # Bosnie-Herzégovine (BA)
    'BA': [
        'Sarajevo', 'Banja Luka', 'Tuzla', 'Zenica', 'Mostar',
        'Bijeljina', 'Brčko', 'Bihać', 'Prijedor', 'Trebinje',
        'Doboj', 'Cazin', 'Bugojno', 'Velika Kladuša', 'Visoko'
    ],
    
    # Serbie (RS)
    'RS': [
        'Belgrade', 'Novi Sad', 'Niš', 'Kragujevac', 'Subotica',
        'Zrenjanin', 'Pančevo', 'Čačak', 'Novi Pazar', 'Kruševac',
        'Leskovac', 'Valjevo', 'Šabac', 'Smederevo', 'Užice'
    ],
    
    # Croatie (HR)
    'HR': [
        'Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar',
        'Slavonski Brod', 'Pula', 'Sesvete', 'Karlovac', 'Varaždin',
        'Šibenik', 'Sisak', 'Dubrovnik', 'Bjelovar', 'Velika Gorica'
    ],
    
    # Slovénie (SI)
    'SI': [
        'Ljubljana', 'Maribor', 'Celje', 'Kranj', 'Velenje',
        'Koper', 'Novo Mesto', 'Ptuj', 'Trbovlje', 'Kamnik',
        'Jesenice', 'Nova Gorica', 'Domžale', 'Murska Sobota', 'Škofja Loka'
    ],
    
    # Slovaquie (SK)
    'SK': [
        'Bratislava', 'Košice', 'Prešov', 'Žilina', 'Nitra',
        'Banská Bystrica', 'Trnava', 'Martin', 'Trenčín', 'Poprad',
        'Prievidza', 'Zvolen', 'Považská Bystrica', 'Michalovce', 'Nové Zámky'
    ],
    
    # Bulgarie (BG)
    'BG': [
        'Sofia', 'Plovdiv', 'Varna', 'Burgas', 'Ruse',
        'Stara Zagora', 'Pleven', 'Sliven', 'Dobrich', 'Shumen',
        'Pernik', 'Yambol', 'Haskovo', 'Pazardzhik', 'Blagoevgrad'
    ],
    
    # Lituanie (LT)
    'LT': [
        'Vilnius', 'Kaunas', 'Klaipėda', 'Šiauliai', 'Panevėžys',
        'Alytus', 'Marijampolė', 'Mažeikiai', 'Jonava', 'Utena',
        'Kėdainiai', 'Telšiai', 'Visaginas', 'Tauragė', 'Ukmergė'
    ],
    
    # Lettonie (LV)
    'LV': [
        'Riga', 'Daugavpils', 'Liepāja', 'Jelgava', 'Jūrmala',
        'Ventspils', 'Rēzekne', 'Valmiera', 'Jēkabpils', 'Ogre',
        'Tukums', 'Salaspils', 'Cēsis', 'Kuldīga', 'Olaine'
    ],
    
    # Estonie (EE)
    'EE': [
        'Tallinn', 'Tartu', 'Narva', 'Pärnu', 'Kohtla-Järve',
        'Viljandi', 'Rakvere', 'Maardu', 'Sillamäe', 'Kuressaare',
        'Võru', 'Valga', 'Haapsalu', 'Jõhvi', 'Paide'
    ],
    
    # Islande (IS)
    'IS': [
        'Reykjavik', 'Kópavogur', 'Hafnarfjörður', 'Akureyri', 'Reykjanesbær',
        'Garðabær', 'Mosfellsbær', 'Selfoss', 'Akranes', 'Vestmannaeyjar'
    ],
    
    # Luxembourg (LU)
    'LU': [
        'Luxembourg', 'Esch-sur-Alzette', 'Differdange', 'Dudelange', 'Ettelbruck',
        'Diekirch', 'Wiltz', 'Echternach', 'Rumelange', 'Grevenmacher'
    ],
    
    # Malte (MT)
    'MT': [
        'Birkirkara', 'Qormi', 'Mosta', 'Żabbar', 'San Pawl il-Baħar',
        'Fgura', 'Żejtun', 'Sliema', 'Naxxar', 'La Valette'
    ],
    
    # Chypre (CY)
    'CY': [
        'Nicosie', 'Limassol', 'Larnaca', 'Strovolos', 'Famagouste',
        'Paphos', 'Kyrenia', 'Protaras', 'Ayia Napa', 'Polis'
    ],
    
    # Mongolie (MN)
    'MN': [
        'Oulan-Bator', 'Erdenet', 'Darkhan', 'Choibalsan', 'Mörön',
        'Khovd', 'Ölgii', 'Tsetserleg', 'Ulaangom', 'Baruun-Urt'
    ],
    
    # Laos (LA)
    'LA': [
        'Vientiane', 'Paksé', 'Savannakhet', 'Luang Prabang', 'Thakhek',
        'Xam Neua', 'Phonsavan', 'Xaignabouri', 'Attapeu', 'Salavan'
    ],
    
    # Cambodge (KH)
    'KH': [
        'Phnom Penh', 'Siem Reap', 'Battambang', 'Sihanoukville', 'Poipet',
        'Kampong Cham', 'Ta Khmau', 'Pursat', 'Kampot', 'Prey Veng'
    ],
    
    # Brunei (BN)
    'BN': [
        'Bandar Seri Begawan', 'Kuala Belait', 'Seria', 'Tutong', 'Bangar',
        'Muara', 'Lumut', 'Jerudong', 'Kilanas', 'Mentiri'
    ],
    
    # Timor oriental (TL)
    'TL': [
        'Dili', 'Baucau', 'Maliana', 'Suai', 'Lospalos',
        'Aileu', 'Same', 'Viqueque', 'Manatuto', 'Gleno'
    ],
    
    # Papouasie-Nouvelle-Guinée (PG)
    'PG': [
        'Port Moresby', 'Lae', 'Arawa', 'Mount Hagen', 'Popondetta',
        'Madang', 'Goroka', 'Wewak', 'Kimbe', 'Rabaul'
    ],
    
    # Fidji (FJ)
    'FJ': [
        'Suva', 'Lautoka', 'Nadi', 'Labasa', 'Ba',
        'Sigatoka', 'Nausori', 'Tavua', 'Levuka', 'Savusavu'
    ],
    
    # Vanuatu (VU)
    'VU': [
        'Port-Vila', 'Luganville', 'Norsup', 'Isangel', 'Sola',
        'Lakatoro', 'Port-Olry', 'Saratamata', 'Lenakel', 'Longana'
    ],
    
    # Samoa (WS)
    'WS': [
        'Apia', 'Vaitele', 'Faleula', 'Siusega', 'Vaiusu',
        'Malie', 'Safotu', 'Leulumoega', 'Faleasiu', 'Satapuala'
    ],
    
    # Andorre (AD)
    'AD': ['Andorre-la-Vieille', 'Escaldes-Engordany', 'Encamp'],
    
    # Antigua-et-Barbuda (AG)
    'AG': ['Saint John\'s', 'All Saints', 'Liberta'],
    
    # Bahamas (BS)
    'BS': ['Nassau', 'Freeport', 'West End'],
    
    # Barbade (BB)
    'BB': ['Bridgetown', 'Speightstown', 'Oistins'],
    
    # Biélorussie (BY)
    'BY': ['Minsk', 'Gomel', 'Moguilev', 'Vitebsk', 'Grodno', 'Brest'],
    
    # Belize (BZ)
    'BZ': ['Belize City', 'San Ignacio', 'Orange Walk'],
    
    # Bhoutan (BT)
    'BT': ['Thimphou', 'Phuentsholing', 'Punakha'],
    
    # Burundi (BI)
    'BI': ['Bujumbura', 'Gitega', 'Muyinga', 'Ngozi', 'Ruyigi'],
    
    # Cap-Vert (CV)
    'CV': ['Praia', 'Mindelo', 'Santa Maria'],
    
    # Comores (KM)
    'KM': ['Moroni', 'Mutsamudu', 'Fomboni'],
    
    # Corée du Nord (KP)
    'KP': ['Pyongyang', 'Hamhung', 'Chongjin'],
    
    # Djibouti (DJ)
    'DJ': ['Djibouti', 'Ali Sabieh', 'Tadjourah'],
    
    # Dominique (DM)
    'DM': ['Roseau', 'Portsmouth', 'Marigot'],
    
    # Érythrée (ER)
    'ER': ['Asmara', 'Keren', 'Massaoua'],
    
    # Eswatini (SZ)
    'SZ': ['Mbabane', 'Manzini', 'Lobamba'],
    
    # Gabon (GA)
    'GA': ['Libreville', 'Port-Gentil', 'Franceville', 'Oyem', 'Moanda'],
    
    # Gambie (GM)
    'GM': ['Banjul', 'Serekunda', 'Brikama'],
    
    # Grenade (GD)
    'GD': ['Saint-Georges', 'Gouyave', 'Grenville'],
    
    # Guinée-Bissau (GW)
    'GW': ['Bissau', 'Bafatá', 'Gabú'],
    
    # Guinée équatoriale (GQ)
    'GQ': ['Malabo', 'Bata', 'Ebebiyin'],
    
    # Guyana (GY)
    'GY': ['Georgetown', 'Linden', 'New Amsterdam'],
    
    # Kirghizistan (KG)
    'KG': ['Bichkek', 'Osh', 'Jalal-Abad', 'Karakol', 'Tokmok'],
    
    # Kiribati (KI)
    'KI': ['Tarawa-Sud', 'Betio', 'Bikenibeu'],
    
    # Lesotho (LS)
    'LS': ['Maseru', 'Teyateyaneng', 'Mafeteng'],
    
    # Libéria (LR)
    'LR': ['Monrovia', 'Gbarnga', 'Kakata'],
    
    # Liechtenstein (LI)
    'LI': ['Vaduz', 'Schaan', 'Balzers'],
    
    # Malawi (MW)
    'MW': ['Lilongwe', 'Blantyre', 'Mzuzu', 'Zomba', 'Mangochi'],
    
    # Maldives (MV)
    'MV': ['Malé', 'Addu City', 'Fuvahmulah'],
    
    # Maurice (MU)
    'MU': ['Port-Louis', 'Beau-Bassin', 'Vacoas-Phoenix', 'Curepipe', 'Quatre Bornes'],
    
    # Micronésie (FM)
    'FM': ['Palikir', 'Weno', 'Kolonia'],
    
    # Monaco (MC)
    'MC': ['Monaco', 'Monte-Carlo', 'La Condamine'],
    
    # Nauru (NR)
    'NR': ['Yaren', 'Denigomodu', 'Aiwo'],
    
    # Palaos (PW)
    'PW': ['Ngerulmud', 'Koror', 'Melekeok'],
    
    # Saint-Christophe-et-Niévès (KN)
    'KN': ['Basseterre', 'Charlestown', 'Dieppe Bay Town'],
    
    # Saint-Marin (SM)
    'SM': ['Saint-Marin', 'Serravalle', 'Borgo Maggiore'],
    
    # Saint-Vincent-et-les-Grenadines (VC)
    'VC': ['Kingstown', 'Georgetown', 'Barrouallie'],
    
    # Sainte-Lucie (LC)
    'LC': ['Castries', 'Vieux Fort', 'Micoud'],
    
    # Seychelles (SC)
    'SC': ['Victoria', 'Anse Boileau', 'Beau Vallon'],
    
    # Singapour (SG)
    'SG': ['Singapour'],
    
    # Îles Salomon (SB)
    'SB': ['Honiara', 'Gizo', 'Auki'],
    
    # Suriname (SR)
    'SR': ['Paramaribo', 'Lelydorp', 'Nieuw Nickerie'],
    
    # Tonga (TO)
    'TO': ['Nuku\'alofa', 'Neiafu', 'Haveluloto'],
    
    # Trinité-et-Tobago (TT)
    'TT': ['Port-d\'Espagne', 'San Fernando', 'Chaguanas', 'Arima', 'Point Fortin'],
    
    # Tuvalu (TV)
    'TV': ['Funafuti', 'Vaiaku', 'Asau'],
    
    # Vatican (VA)
    'VA': ['Vatican'],
}

def get_cities_by_country(country_code):
    """
    Récupère la liste des villes pour un pays donné
    
    Args:
        country_code: Code ISO-2 du pays (ex: 'MA', 'FR', 'US')
    
    Returns:
        Liste des villes ou liste avec "Autre" si le pays n'a pas de villes définies
    """
    # Retourne les villes si elles existent, sinon retourne une liste avec "Autre" pour permettre la saisie manuelle
    return WORLD_CITIES.get(country_code, ["Autre (saisir manuellement)"])

