"""
Liste complète de tous les pays du monde avec codes ISO-2 et nationalités
Basé sur la norme ISO 3166-1 (2025) - 195 pays reconnus par l'ONU
"""

WORLD_COUNTRIES = [
    # A
    {'name': 'Afghanistan', 'code': 'AF', 'nationality': 'Afghane'},
    {'name': 'Afrique du Sud', 'code': 'ZA', 'nationality': 'Sud-africaine'},
    {'name': 'Albanie', 'code': 'AL', 'nationality': 'Albanaise'},
    {'name': 'Algérie', 'code': 'DZ', 'nationality': 'Algérienne'},
    {'name': 'Allemagne', 'code': 'DE', 'nationality': 'Allemande'},
    {'name': 'Andorre', 'code': 'AD', 'nationality': 'Andorrane'},
    {'name': 'Angola', 'code': 'AO', 'nationality': 'Angolaise'},
    {'name': 'Antigua-et-Barbuda', 'code': 'AG', 'nationality': 'Antiguaise'},
    {'name': 'Arabie saoudite', 'code': 'SA', 'nationality': 'Saoudienne'},
    {'name': 'Argentine', 'code': 'AR', 'nationality': 'Argentine'},
    {'name': 'Arménie', 'code': 'AM', 'nationality': 'Arménienne'},
    {'name': 'Australie', 'code': 'AU', 'nationality': 'Australienne'},
    {'name': 'Autriche', 'code': 'AT', 'nationality': 'Autrichienne'},
    {'name': 'Azerbaïdjan', 'code': 'AZ', 'nationality': 'Azerbaïdjanaise'},
    
    # B
    {'name': 'Bahamas', 'code': 'BS', 'nationality': 'Bahamienne'},
    {'name': 'Bahreïn', 'code': 'BH', 'nationality': 'Bahreïnienne'},
    {'name': 'Bangladesh', 'code': 'BD', 'nationality': 'Bangladaise'},
    {'name': 'Barbade', 'code': 'BB', 'nationality': 'Barbadienne'},
    {'name': 'Bélarus', 'code': 'BY', 'nationality': 'Biélorusse'},
    {'name': 'Belgique', 'code': 'BE', 'nationality': 'Belge'},
    {'name': 'Belize', 'code': 'BZ', 'nationality': 'Bélizienne'},
    {'name': 'Bénin', 'code': 'BJ', 'nationality': 'Béninoise'},
    {'name': 'Bhoutan', 'code': 'BT', 'nationality': 'Bhoutanaise'},
    {'name': 'Bolivie', 'code': 'BO', 'nationality': 'Bolivienne'},
    {'name': 'Bosnie-Herzégovine', 'code': 'BA', 'nationality': 'Bosnienne'},
    {'name': 'Botswana', 'code': 'BW', 'nationality': 'Botswanaise'},
    {'name': 'Brésil', 'code': 'BR', 'nationality': 'Brésilienne'},
    {'name': 'Brunei', 'code': 'BN', 'nationality': 'Brunéienne'},
    {'name': 'Bulgarie', 'code': 'BG', 'nationality': 'Bulgare'},
    {'name': 'Burkina Faso', 'code': 'BF', 'nationality': 'Burkinabè'},
    {'name': 'Burundi', 'code': 'BI', 'nationality': 'Burundaise'},
    
    # C
    {'name': 'Cambodge', 'code': 'KH', 'nationality': 'Cambodgienne'},
    {'name': 'Cameroun', 'code': 'CM', 'nationality': 'Camerounaise'},
    {'name': 'Canada', 'code': 'CA', 'nationality': 'Canadienne'},
    {'name': 'Cap-Vert', 'code': 'CV', 'nationality': 'Cap-verdienne'},
    {'name': 'Chili', 'code': 'CL', 'nationality': 'Chilienne'},
    {'name': 'Chine', 'code': 'CN', 'nationality': 'Chinoise'},
    {'name': 'Chypre', 'code': 'CY', 'nationality': 'Chypriote'},
    {'name': 'Colombie', 'code': 'CO', 'nationality': 'Colombienne'},
    {'name': 'Comores', 'code': 'KM', 'nationality': 'Comorienne'},
    {'name': 'Congo', 'code': 'CG', 'nationality': 'Congolaise'},
    {'name': 'Corée du Nord', 'code': 'KP', 'nationality': 'Nord-coréenne'},
    {'name': 'Corée du Sud', 'code': 'KR', 'nationality': 'Sud-coréenne'},
    {'name': 'Costa Rica', 'code': 'CR', 'nationality': 'Costaricienne'},
    {'name': "Côte d'Ivoire", 'code': 'CI', 'nationality': 'Ivoirienne'},
    {'name': 'Croatie', 'code': 'HR', 'nationality': 'Croate'},
    {'name': 'Cuba', 'code': 'CU', 'nationality': 'Cubaine'},
    
    # D
    {'name': 'Danemark', 'code': 'DK', 'nationality': 'Danoise'},
    {'name': 'Djibouti', 'code': 'DJ', 'nationality': 'Djiboutienne'},
    {'name': 'Dominique', 'code': 'DM', 'nationality': 'Dominiquaise'},
    
    # E
    {'name': 'Égypte', 'code': 'EG', 'nationality': 'Égyptienne'},
    {'name': 'Émirats arabes unis', 'code': 'AE', 'nationality': 'Émirienne'},
    {'name': 'Équateur', 'code': 'EC', 'nationality': 'Équatorienne'},
    {'name': 'Érythrée', 'code': 'ER', 'nationality': 'Érythréenne'},
    {'name': 'Espagne', 'code': 'ES', 'nationality': 'Espagnole'},
    {'name': 'Estonie', 'code': 'EE', 'nationality': 'Estonienne'},
    {'name': 'Eswatini', 'code': 'SZ', 'nationality': 'Swazie'},
    {'name': 'États-Unis', 'code': 'US', 'nationality': 'Américaine'},
    {'name': 'Éthiopie', 'code': 'ET', 'nationality': 'Éthiopienne'},
    
    # F
    {'name': 'Fidji', 'code': 'FJ', 'nationality': 'Fidjienne'},
    {'name': 'Finlande', 'code': 'FI', 'nationality': 'Finlandaise'},
    {'name': 'France', 'code': 'FR', 'nationality': 'Française'},
    
    # G
    {'name': 'Gabon', 'code': 'GA', 'nationality': 'Gabonaise'},
    {'name': 'Gambie', 'code': 'GM', 'nationality': 'Gambienne'},
    {'name': 'Géorgie', 'code': 'GE', 'nationality': 'Géorgienne'},
    {'name': 'Ghana', 'code': 'GH', 'nationality': 'Ghanéenne'},
    {'name': 'Grèce', 'code': 'GR', 'nationality': 'Grecque'},
    {'name': 'Grenade', 'code': 'GD', 'nationality': 'Grenadienne'},
    {'name': 'Guatemala', 'code': 'GT', 'nationality': 'Guatémaltèque'},
    {'name': 'Guinée', 'code': 'GN', 'nationality': 'Guinéenne'},
    {'name': 'Guinée-Bissau', 'code': 'GW', 'nationality': 'Bissau-guinéenne'},
    {'name': 'Guinée équatoriale', 'code': 'GQ', 'nationality': 'Équato-guinéenne'},
    {'name': 'Guyana', 'code': 'GY', 'nationality': 'Guyanienne'},
    
    # H
    {'name': 'Haïti', 'code': 'HT', 'nationality': 'Haïtienne'},
    {'name': 'Honduras', 'code': 'HN', 'nationality': 'Hondurienne'},
    {'name': 'Hongrie', 'code': 'HU', 'nationality': 'Hongroise'},
    
    # I
    {'name': 'Inde', 'code': 'IN', 'nationality': 'Indienne'},
    {'name': 'Indonésie', 'code': 'ID', 'nationality': 'Indonésienne'},
    {'name': 'Irak', 'code': 'IQ', 'nationality': 'Irakienne'},
    {'name': 'Iran', 'code': 'IR', 'nationality': 'Iranienne'},
    {'name': 'Irlande', 'code': 'IE', 'nationality': 'Irlandaise'},
    {'name': 'Islande', 'code': 'IS', 'nationality': 'Islandaise'},
    {'name': 'Israël', 'code': 'IL', 'nationality': 'Israélienne'},
    {'name': 'Italie', 'code': 'IT', 'nationality': 'Italienne'},
    
    # J
    {'name': 'Jamaïque', 'code': 'JM', 'nationality': 'Jamaïcaine'},
    {'name': 'Japon', 'code': 'JP', 'nationality': 'Japonaise'},
    {'name': 'Jordanie', 'code': 'JO', 'nationality': 'Jordanienne'},
    
    # K
    {'name': 'Kazakhstan', 'code': 'KZ', 'nationality': 'Kazakhstanaise'},
    {'name': 'Kenya', 'code': 'KE', 'nationality': 'Kényane'},
    {'name': 'Kirghizistan', 'code': 'KG', 'nationality': 'Kirghize'},
    {'name': 'Kiribati', 'code': 'KI', 'nationality': 'Kiribatienne'},
    {'name': 'Koweït', 'code': 'KW', 'nationality': 'Koweïtienne'},
    
    # L
    {'name': 'Laos', 'code': 'LA', 'nationality': 'Laotienne'},
    {'name': 'Lesotho', 'code': 'LS', 'nationality': 'Lésothane'},
    {'name': 'Lettonie', 'code': 'LV', 'nationality': 'Lettone'},
    {'name': 'Liban', 'code': 'LB', 'nationality': 'Libanaise'},
    {'name': 'Libéria', 'code': 'LR', 'nationality': 'Libérienne'},
    {'name': 'Libye', 'code': 'LY', 'nationality': 'Libyenne'},
    {'name': 'Liechtenstein', 'code': 'LI', 'nationality': 'Liechtensteinoise'},
    {'name': 'Lituanie', 'code': 'LT', 'nationality': 'Lituanienne'},
    {'name': 'Luxembourg', 'code': 'LU', 'nationality': 'Luxembourgeoise'},
    
    # M
    {'name': 'Macédoine du Nord', 'code': 'MK', 'nationality': 'Macédonienne'},
    {'name': 'Madagascar', 'code': 'MG', 'nationality': 'Malgache'},
    {'name': 'Malaisie', 'code': 'MY', 'nationality': 'Malaisienne'},
    {'name': 'Malawi', 'code': 'MW', 'nationality': 'Malawienne'},
    {'name': 'Maldives', 'code': 'MV', 'nationality': 'Maldivienne'},
    {'name': 'Mali', 'code': 'ML', 'nationality': 'Malienne'},
    {'name': 'Malte', 'code': 'MT', 'nationality': 'Maltaise'},
    {'name': 'Maroc', 'code': 'MA', 'nationality': 'Marocaine'},
    {'name': 'Maurice', 'code': 'MU', 'nationality': 'Mauricienne'},
    {'name': 'Mauritanie', 'code': 'MR', 'nationality': 'Mauritanienne'},
    {'name': 'Mexique', 'code': 'MX', 'nationality': 'Mexicaine'},
    {'name': 'Micronésie', 'code': 'FM', 'nationality': 'Micronésienne'},
    {'name': 'Moldavie', 'code': 'MD', 'nationality': 'Moldave'},
    {'name': 'Monaco', 'code': 'MC', 'nationality': 'Monégasque'},
    {'name': 'Mongolie', 'code': 'MN', 'nationality': 'Mongole'},
    {'name': 'Monténégro', 'code': 'ME', 'nationality': 'Monténégrine'},
    {'name': 'Mozambique', 'code': 'MZ', 'nationality': 'Mozambicaine'},
    {'name': 'Myanmar', 'code': 'MM', 'nationality': 'Birmane'},
    
    # N
    {'name': 'Namibie', 'code': 'NA', 'nationality': 'Namibienne'},
    {'name': 'Nauru', 'code': 'NR', 'nationality': 'Nauruane'},
    {'name': 'Népal', 'code': 'NP', 'nationality': 'Népalaise'},
    {'name': 'Nicaragua', 'code': 'NI', 'nationality': 'Nicaraguayenne'},
    {'name': 'Niger', 'code': 'NE', 'nationality': 'Nigérienne'},
    {'name': 'Nigéria', 'code': 'NG', 'nationality': 'Nigériane'},
    {'name': 'Norvège', 'code': 'NO', 'nationality': 'Norvégienne'},
    {'name': 'Nouvelle-Zélande', 'code': 'NZ', 'nationality': 'Néo-zélandaise'},
    
    # O
    {'name': 'Oman', 'code': 'OM', 'nationality': 'Omanaise'},
    {'name': 'Ouganda', 'code': 'UG', 'nationality': 'Ougandaise'},
    {'name': 'Ouzbékistan', 'code': 'UZ', 'nationality': 'Ouzbèke'},
    
    # P
    {'name': 'Pakistan', 'code': 'PK', 'nationality': 'Pakistanaise'},
    {'name': 'Palaos', 'code': 'PW', 'nationality': 'Paluane'},
    {'name': 'Palestine', 'code': 'PS', 'nationality': 'Palestinienne'},
    {'name': 'Panama', 'code': 'PA', 'nationality': 'Panaméenne'},
    {'name': 'Papouasie-Nouvelle-Guinée', 'code': 'PG', 'nationality': 'Papouane'},
    {'name': 'Paraguay', 'code': 'PY', 'nationality': 'Paraguayenne'},
    {'name': 'Pays-Bas', 'code': 'NL', 'nationality': 'Néerlandaise'},
    {'name': 'Pérou', 'code': 'PE', 'nationality': 'Péruvienne'},
    {'name': 'Philippines', 'code': 'PH', 'nationality': 'Philippine'},
    {'name': 'Pologne', 'code': 'PL', 'nationality': 'Polonaise'},
    {'name': 'Portugal', 'code': 'PT', 'nationality': 'Portugaise'},
    
    # Q
    {'name': 'Qatar', 'code': 'QA', 'nationality': 'Qatarienne'},
    
    # R
    {'name': 'RD Congo', 'code': 'CD', 'nationality': 'Congolaise'},
    {'name': 'République centrafricaine', 'code': 'CF', 'nationality': 'Centrafricaine'},
    {'name': 'République dominicaine', 'code': 'DO', 'nationality': 'Dominicaine'},
    {'name': 'Roumanie', 'code': 'RO', 'nationality': 'Roumaine'},
    {'name': 'Royaume-Uni', 'code': 'GB', 'nationality': 'Britannique'},
    {'name': 'Russie', 'code': 'RU', 'nationality': 'Russe'},
    {'name': 'Rwanda', 'code': 'RW', 'nationality': 'Rwandaise'},
    
    # S
    {'name': 'Saint-Kitts-et-Nevis', 'code': 'KN', 'nationality': 'Kittitienne'},
    {'name': 'Sainte-Lucie', 'code': 'LC', 'nationality': 'Sainte-lucienne'},
    {'name': 'Saint-Marin', 'code': 'SM', 'nationality': 'Saint-marinaise'},
    {'name': 'Saint-Vincent-et-les-Grenadines', 'code': 'VC', 'nationality': 'Vincentaise'},
    {'name': 'Salomon', 'code': 'SB', 'nationality': 'Salomonienne'},
    {'name': 'Salvador', 'code': 'SV', 'nationality': 'Salvadorienne'},
    {'name': 'Samoa', 'code': 'WS', 'nationality': 'Samoane'},
    {'name': 'Sao Tomé-et-Principe', 'code': 'ST', 'nationality': 'Santoméenne'},
    {'name': 'Sénégal', 'code': 'SN', 'nationality': 'Sénégalaise'},
    {'name': 'Serbie', 'code': 'RS', 'nationality': 'Serbe'},
    {'name': 'Seychelles', 'code': 'SC', 'nationality': 'Seychelloise'},
    {'name': 'Sierra Leone', 'code': 'SL', 'nationality': 'Sierra-leonaise'},
    {'name': 'Singapour', 'code': 'SG', 'nationality': 'Singapourienne'},
    {'name': 'Slovaquie', 'code': 'SK', 'nationality': 'Slovaque'},
    {'name': 'Slovénie', 'code': 'SI', 'nationality': 'Slovène'},
    {'name': 'Somalie', 'code': 'SO', 'nationality': 'Somalienne'},
    {'name': 'Soudan', 'code': 'SD', 'nationality': 'Soudanaise'},
    {'name': 'Soudan du Sud', 'code': 'SS', 'nationality': 'Sud-soudanaise'},
    {'name': 'Sri Lanka', 'code': 'LK', 'nationality': 'Sri-lankaise'},
    {'name': 'Suède', 'code': 'SE', 'nationality': 'Suédoise'},
    {'name': 'Suisse', 'code': 'CH', 'nationality': 'Suisse'},
    {'name': 'Suriname', 'code': 'SR', 'nationality': 'Surinamaise'},
    {'name': 'Syrie', 'code': 'SY', 'nationality': 'Syrienne'},
    
    # T
    {'name': 'Tadjikistan', 'code': 'TJ', 'nationality': 'Tadjike'},
    {'name': 'Tanzanie', 'code': 'TZ', 'nationality': 'Tanzanienne'},
    {'name': 'Tchad', 'code': 'TD', 'nationality': 'Tchadienne'},
    {'name': 'Tchéquie', 'code': 'CZ', 'nationality': 'Tchèque'},
    {'name': 'Thaïlande', 'code': 'TH', 'nationality': 'Thaïlandaise'},
    {'name': 'Timor oriental', 'code': 'TL', 'nationality': 'Est-timoraise'},
    {'name': 'Togo', 'code': 'TG', 'nationality': 'Togolaise'},
    {'name': 'Tonga', 'code': 'TO', 'nationality': 'Tonguienne'},
    {'name': 'Trinité-et-Tobago', 'code': 'TT', 'nationality': 'Trinidadienne'},
    {'name': 'Tunisie', 'code': 'TN', 'nationality': 'Tunisienne'},
    {'name': 'Turkménistan', 'code': 'TM', 'nationality': 'Turkmène'},
    {'name': 'Turquie', 'code': 'TR', 'nationality': 'Turque'},
    {'name': 'Tuvalu', 'code': 'TV', 'nationality': 'Tuvaluane'},
    
    # U
    {'name': 'Ukraine', 'code': 'UA', 'nationality': 'Ukrainienne'},
    {'name': 'Uruguay', 'code': 'UY', 'nationality': 'Uruguayenne'},
    
    # V
    {'name': 'Vanuatu', 'code': 'VU', 'nationality': 'Vanuatuane'},
    {'name': 'Vatican', 'code': 'VA', 'nationality': 'Vaticane'},
    {'name': 'Venezuela', 'code': 'VE', 'nationality': 'Vénézuélienne'},
    {'name': 'Viêt Nam', 'code': 'VN', 'nationality': 'Vietnamienne'},
    
    # Y
    {'name': 'Yémen', 'code': 'YE', 'nationality': 'Yéménite'},
    
    # Z
    {'name': 'Zambie', 'code': 'ZM', 'nationality': 'Zambienne'},
    {'name': 'Zimbabwe', 'code': 'ZW', 'nationality': 'Zimbabwéenne'},
]

# Fonction pour convertir un code ISO en emoji drapeau
def code_to_flag(code):
    """Convertit un code pays ISO-2 en emoji drapeau"""
    if not code or len(code) != 2:
        return ''
    return ''.join(chr(127397 + ord(char)) for char in code.upper())

# Dictionnaire de correspondance rapide code -> nationalité
NATIONALITIES_BY_CODE = {country['code']: country['nationality'] for country in WORLD_COUNTRIES}

# Liste des nationalités uniquement (triée alphabétiquement)
NATIONALITIES = sorted(set(country['nationality'] for country in WORLD_COUNTRIES))

# Liste des nationalités avec drapeaux (pour affichage dans les dropdowns)
# Structure: [{'nationality': 'Marocaine', 'flag': '🇲🇦'}, ...]
NATIONALITIES_WITH_FLAGS = []
nationality_to_flag = {}

# Construire le dictionnaire nationalité -> drapeau
for country in WORLD_COUNTRIES:
    nat = country['nationality']
    if nat not in nationality_to_flag:
        nationality_to_flag[nat] = code_to_flag(country['code'])

# Créer la liste avec nationalités et drapeaux (triée alphabétiquement)
for nationality in NATIONALITIES:
    NATIONALITIES_WITH_FLAGS.append({
        'nationality': nationality,
        'flag': nationality_to_flag.get(nationality, '')
    })
