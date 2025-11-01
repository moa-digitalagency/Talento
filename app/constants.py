"""
Constantes de l'application taalentio.com
Définit toutes les options standards utilisées dans l'application
"""

AVAILABILITY_OPTIONS = {
    'Temps plein': {
        'label': 'Temps plein (35-40h/semaine)',
        'emoji': '⏰',
        'color': 'green'
    },
    'Temps partiel': {
        'label': 'Temps partiel (15-30h/semaine)',
        'emoji': '🕐',
        'color': 'yellow'
    },
    'Mi-temps': {
        'label': 'Mi-temps (20h/semaine)',
        'emoji': '⏳',
        'color': 'yellow'
    },
    'Flexible': {
        'label': 'Flexible',
        'emoji': '🔄',
        'color': 'blue'
    },
    'Occasionnel': {
        'label': 'Occasionnel / Mission',
        'emoji': '📅',
        'color': 'purple'
    },
    'Week-end uniquement': {
        'label': 'Week-end uniquement',
        'emoji': '📅',
        'color': 'indigo'
    },
    'Soir uniquement': {
        'label': 'Soir uniquement',
        'emoji': '🌙',
        'color': 'indigo'
    },
    'Ponctuel': {
        'label': 'Ponctuel / Missions courtes',
        'emoji': '📌',
        'color': 'purple'
    },
    'Indisponible': {
        'label': 'Actuellement indisponible',
        'emoji': '❌',
        'color': 'red'
    }
}

WORK_MODE_OPTIONS = {
    'remote': {
        'label': 'Télétravail',
        'emoji': '🏠'
    },
    'on_site': {
        'label': 'Sur site',
        'emoji': '🏢'
    },
    'hybrid': {
        'label': 'Hybride',
        'emoji': '🔄'
    }
}

def get_availability_display(value):
    """
    Retourne les informations d'affichage pour une disponibilité
    
    Args:
        value: Valeur de disponibilité
        
    Returns:
        dict: Informations d'affichage ou None
    """
    if not value:
        return None
    return AVAILABILITY_OPTIONS.get(value, {
        'label': value,
        'emoji': '❓',
        'color': 'gray'
    })

def get_work_mode_display(value):
    """
    Retourne les informations d'affichage pour un mode de travail
    
    Args:
        value: Valeur du mode de travail
        
    Returns:
        dict: Informations d'affichage ou None
    """
    if not value:
        return None
    return WORK_MODE_OPTIONS.get(value, {
        'label': value,
        'emoji': '❓'
    })

LANGUAGES_CINEMA = [
    {'name': 'Afrikaans', 'flag': '🇿🇦'},
    {'name': 'Albanais', 'flag': '🇦🇱'},
    {'name': 'Allemand', 'flag': '🇩🇪'},
    {'name': 'Amazigh (Berbère)', 'flag': 'ⵣ'},
    {'name': 'Amharique', 'flag': '🇪🇹'},
    {'name': 'Anglais', 'flag': '🇬🇧'},
    {'name': 'Arabe', 'flag': '🇸🇦'},
    {'name': 'Arménien', 'flag': '🇦🇲'},
    {'name': 'Bambara', 'flag': '🇲🇱'},
    {'name': 'Bengali', 'flag': '🇧🇩'},
    {'name': 'Bulgare', 'flag': '🇧🇬'},
    {'name': 'Catalan', 'flag': '🇪🇸'},
    {'name': 'Chinois (Cantonais)', 'flag': '🇭🇰'},
    {'name': 'Chinois (Mandarin)', 'flag': '🇨🇳'},
    {'name': 'Coréen', 'flag': '🇰🇷'},
    {'name': 'Créole', 'flag': '🇭🇹'},
    {'name': 'Danois', 'flag': '🇩🇰'},
    {'name': 'Dioula', 'flag': '🇨🇮'},
    {'name': 'Espagnol', 'flag': '🇪🇸'},
    {'name': 'Estonien', 'flag': '🇪🇪'},
    {'name': 'Finnois', 'flag': '🇫🇮'},
    {'name': 'Français', 'flag': '🇫🇷'},
    {'name': 'Grec', 'flag': '🇬🇷'},
    {'name': 'Haoussa', 'flag': '🇳🇬'},
    {'name': 'Hébreu', 'flag': '🇮🇱'},
    {'name': 'Hindi', 'flag': '🇮🇳'},
    {'name': 'Hongrois', 'flag': '🇭🇺'},
    {'name': 'Igbo', 'flag': '🇳🇬'},
    {'name': 'Indonésien', 'flag': '🇮🇩'},
    {'name': 'Italien', 'flag': '🇮🇹'},
    {'name': 'Japonais', 'flag': '🇯🇵'},
    {'name': 'Kikuyu', 'flag': '🇰🇪'},
    {'name': 'Kinyarwanda', 'flag': '🇷🇼'},
    {'name': 'Lingala', 'flag': '🇨🇩'},
    {'name': 'Malgache', 'flag': '🇲🇬'},
    {'name': 'Malinké', 'flag': '🇬🇳'},
    {'name': 'Néerlandais', 'flag': '🇳🇱'},
    {'name': 'Norvégien', 'flag': '🇳🇴'},
    {'name': 'Oromo', 'flag': '🇪🇹'},
    {'name': 'Peul', 'flag': '🇸🇳'},
    {'name': 'Polonais', 'flag': '🇵🇱'},
    {'name': 'Portugais', 'flag': '🇵🇹'},
    {'name': 'Roumain', 'flag': '🇷🇴'},
    {'name': 'Russe', 'flag': '🇷🇺'},
    {'name': 'Sango', 'flag': '🇨🇫'},
    {'name': 'Serbe', 'flag': '🇷🇸'},
    {'name': 'Somali', 'flag': '🇸🇴'},
    {'name': 'Soninké', 'flag': '🇲🇱'},
    {'name': 'Suédois', 'flag': '🇸🇪'},
    {'name': 'Swahili', 'flag': '🇰🇪'},
    {'name': 'Tamoul', 'flag': '🇱🇰'},
    {'name': 'Tchèque', 'flag': '🇨🇿'},
    {'name': 'Tigrinya', 'flag': '🇪🇷'},
    {'name': 'Turc', 'flag': '🇹🇷'},
    {'name': 'Ukrainien', 'flag': '🇺🇦'},
    {'name': 'Wolof', 'flag': '🇸🇳'},
    {'name': 'Xhosa', 'flag': '🇿🇦'},
    {'name': 'Yoruba', 'flag': '🇳🇬'},
    {'name': 'Zoulou', 'flag': '🇿🇦'},
    {'name': 'Autre', 'flag': '🌐'}
]

TALENT_CATEGORIES = [
    {
        'name': 'Arts de la scène',
        'emoji': '🎭',
        'tag': 'cinema',
        'talents': [
            'Acteur/Actrice', 'Chanteur', 'Danseur', 'Comédien de doublage',
            'Humoriste', 'Présentateur/Animateur', 'Conteur'
        ]
    },
    {
        'name': 'Arts visuels',
        'emoji': '🎨',
        'tag': 'general',
        'talents': [
            'Photographe', 'Peintre', 'Sculpteur', 'Illustrateur',
            'Designer graphique', 'Maquilleur', 'Tatoueur'
        ]
    },
    {
        'name': 'Musique',
        'emoji': '🎵',
        'tag': 'general',
        'talents': [
            'Musicien', 'Compositeur', 'DJ', 'Producteur musical',
            'Ingénieur du son', 'Beatmaker'
        ]
    },
    {
        'name': 'Sports & Arts martiaux',
        'emoji': '⚽',
        'tag': 'general',
        'talents': [
            'Cascadeur', 'Arts martiaux', 'Acrobate', 'Équitation',
            'Sports de combat', 'Natation', 'Plongée', 'Parkour',
            'Gymnastique', 'Danse sportive', 'Autres sports'
        ]
    },
    {
        'name': 'Techniques & Créatives',
        'emoji': '🎬',
        'tag': 'cinema',
        'talents': [
            'Chorégraphe', 'Metteur en scène', 'Réalisateur',
            'Scénariste', 'Monteur vidéo', 'Cadreur/Opérateur'
        ]
    },
    {
        'name': 'Autres',
        'emoji': '✨',
        'tag': 'general',
        'talents': [
            'Mannequin', 'Magicien', 'Ventriloque', 'Mime',
            'Jongleur', 'Clown', 'Marionnettiste', 'Autre'
        ]
    }
]

# Types de talents pour CINEMA (choix multiples)
CINEMA_TALENT_TYPES = [
    'Acteur/Actrice Principal(e)',
    'Acteur/Actrice Secondaire',
    'Figurant(e)',
    'Silhouette',
    'Doublure',
    'Doublure Lumière',
    'Cascadeur/Cascadeuse',
    'Mannequin',
    'Voix Off',
    'Figurant Spécialisé',
    'Choriste',
    'Danseur/Danseuse de fond',
    'Autre'
]

# Couleurs des yeux
EYE_COLORS = [
    'Marron foncé',
    'Marron',
    'Marron clair',
    'Noisette',
    'Vert',
    'Vert clair',
    'Bleu',
    'Bleu clair',
    'Gris',
    'Ambre',
    'Noir',
    'Vairons (deux couleurs)'
]

# Couleurs de cheveux
HAIR_COLORS = [
    'Noir',
    'Brun foncé',
    'Brun',
    'Châtain foncé',
    'Châtain',
    'Châtain clair',
    'Blond foncé',
    'Blond',
    'Blond platine',
    'Roux',
    'Auburn',
    'Poivre et sel',
    'Gris',
    'Blanc',
    'Colorés/Fantaisie',
    'Chauve/Rasé'
]

# Types de cheveux
HAIR_TYPES = [
    'Raides',
    'Ondulés',
    'Bouclés',
    'Frisés',
    'Crépus',
    'Afro',
    'Tressés',
    'Locks/Dreadlocks',
    'Rasés',
    'Chauve'
]

# Teints de peau
SKIN_TONES = [
    'Très clair',
    'Clair',
    'Moyen clair',
    'Moyen',
    'Olivâtre',
    'Mat',
    'Bronzé',
    'Foncé',
    'Très foncé',
    'Noir profond'
]

# Morphologies
BUILD_TYPES = [
    'Très mince',
    'Mince',
    'Svelte',
    'Athlétique',
    'Musclé',
    'Moyen',
    'Fort',
    'Rond',
    'Corpulent',
    'Imposant'
]

# Mapping pays (code ISO) → monnaie (code ISO 4217)
COUNTRY_CURRENCIES = {
    'MA': {'code': 'MAD', 'symbol': 'MAD', 'name': 'Dirham marocain'},
    'DZ': {'code': 'DZD', 'symbol': 'DZD', 'name': 'Dinar algérien'},
    'TN': {'code': 'TND', 'symbol': 'TND', 'name': 'Dinar tunisien'},
    'LY': {'code': 'LYD', 'symbol': 'LYD', 'name': 'Dinar libyen'},
    'EG': {'code': 'EGP', 'symbol': 'EGP', 'name': 'Livre égyptienne'},
    'MR': {'code': 'MRU', 'symbol': 'MRU', 'name': 'Ouguiya mauritanien'},
    'ML': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'SN': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'GM': {'code': 'GMD', 'symbol': 'GMD', 'name': 'Dalasi gambien'},
    'GW': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'GN': {'code': 'GNF', 'symbol': 'GNF', 'name': 'Franc guinéen'},
    'SL': {'code': 'SLL', 'symbol': 'SLL', 'name': 'Leone sierra-léonais'},
    'LR': {'code': 'LRD', 'symbol': 'LRD', 'name': 'Dollar libérien'},
    'CI': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'GH': {'code': 'GHS', 'symbol': 'GHS', 'name': 'Cedi ghanéen'},
    'TG': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'BJ': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'NG': {'code': 'NGN', 'symbol': 'NGN', 'name': 'Naira nigérian'},
    'NE': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'BF': {'code': 'XOF', 'symbol': 'FCFA', 'name': 'Franc CFA (BCEAO)'},
    'CM': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'TD': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'CF': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'GQ': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'GA': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'CG': {'code': 'XAF', 'symbol': 'FCFA', 'name': 'Franc CFA (BEAC)'},
    'CD': {'code': 'CDF', 'symbol': 'CDF', 'name': 'Franc congolais'},
    'AO': {'code': 'AOA', 'symbol': 'AOA', 'name': 'Kwanza angolais'},
    'SD': {'code': 'SDG', 'symbol': 'SDG', 'name': 'Livre soudanaise'},
    'SS': {'code': 'SSP', 'symbol': 'SSP', 'name': 'Livre sud-soudanaise'},
    'ET': {'code': 'ETB', 'symbol': 'ETB', 'name': 'Birr éthiopien'},
    'ER': {'code': 'ERN', 'symbol': 'ERN', 'name': 'Nakfa érythréen'},
    'DJ': {'code': 'DJF', 'symbol': 'DJF', 'name': 'Franc djiboutien'},
    'SO': {'code': 'SOS', 'symbol': 'SOS', 'name': 'Shilling somalien'},
    'KE': {'code': 'KES', 'symbol': 'KES', 'name': 'Shilling kényan'},
    'UG': {'code': 'UGX', 'symbol': 'UGX', 'name': 'Shilling ougandais'},
    'RW': {'code': 'RWF', 'symbol': 'RWF', 'name': 'Franc rwandais'},
    'BI': {'code': 'BIF', 'symbol': 'BIF', 'name': 'Franc burundais'},
    'TZ': {'code': 'TZS', 'symbol': 'TZS', 'name': 'Shilling tanzanien'},
    'MW': {'code': 'MWK', 'symbol': 'MWK', 'name': 'Kwacha malawite'},
    'MZ': {'code': 'MZN', 'symbol': 'MZN', 'name': 'Metical mozambicain'},
    'ZW': {'code': 'ZWL', 'symbol': 'ZWL', 'name': 'Dollar zimbabwéen'},
    'ZM': {'code': 'ZMW', 'symbol': 'ZMW', 'name': 'Kwacha zambien'},
    'BW': {'code': 'BWP', 'symbol': 'BWP', 'name': 'Pula botswanais'},
    'NA': {'code': 'NAD', 'symbol': 'NAD', 'name': 'Dollar namibien'},
    'ZA': {'code': 'ZAR', 'symbol': 'ZAR', 'name': 'Rand sud-africain'},
    'LS': {'code': 'LSL', 'symbol': 'LSL', 'name': 'Loti lesothan'},
    'SZ': {'code': 'SZL', 'symbol': 'SZL', 'name': 'Lilangeni'},
    'MG': {'code': 'MGA', 'symbol': 'MGA', 'name': 'Ariary malgache'},
    'MU': {'code': 'MUR', 'symbol': 'MUR', 'name': 'Roupie mauricienne'},
    'KM': {'code': 'KMF', 'symbol': 'KMF', 'name': 'Franc comorien'},
    'SC': {'code': 'SCR', 'symbol': 'SCR', 'name': 'Roupie seychelloise'},
    'CV': {'code': 'CVE', 'symbol': 'CVE', 'name': 'Escudo cap-verdien'},
    'ST': {'code': 'STN', 'symbol': 'STN', 'name': 'Dobra santoméen'},
    'FR': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'BE': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'IT': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'ES': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'PT': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'DE': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'NL': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'AT': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'GR': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'IE': {'code': 'EUR', 'symbol': '€', 'name': 'Euro'},
    'GB': {'code': 'GBP', 'symbol': '£', 'name': 'Livre sterling'},
    'US': {'code': 'USD', 'symbol': '$', 'name': 'Dollar américain'},
    'CA': {'code': 'CAD', 'symbol': 'CAD', 'name': 'Dollar canadien'},
    'CH': {'code': 'CHF', 'symbol': 'CHF', 'name': 'Franc suisse'},
    'CN': {'code': 'CNY', 'symbol': '¥', 'name': 'Yuan chinois'},
    'JP': {'code': 'JPY', 'symbol': '¥', 'name': 'Yen japonais'},
    'IN': {'code': 'INR', 'symbol': '₹', 'name': 'Roupie indienne'},
    'BR': {'code': 'BRL', 'symbol': 'R$', 'name': 'Real brésilien'},
    'MX': {'code': 'MXN', 'symbol': 'MXN', 'name': 'Peso mexicain'},
    'RU': {'code': 'RUB', 'symbol': '₽', 'name': 'Rouble russe'},
    'TR': {'code': 'TRY', 'symbol': '₺', 'name': 'Livre turque'},
    'SA': {'code': 'SAR', 'symbol': 'SAR', 'name': 'Riyal saoudien'},
    'AE': {'code': 'AED', 'symbol': 'AED', 'name': 'Dirham des EAU'},
}

def get_currency_for_country(country_code):
    """
    Retourne la monnaie pour un code pays donné
    
    Args:
        country_code: Code pays ISO-2 (ex: 'MA', 'CD', 'FR')
        
    Returns:
        dict: Informations sur la monnaie {code, symbol, name} ou MAD par défaut
    """
    return COUNTRY_CURRENCIES.get(country_code, {'code': 'MAD', 'symbol': 'MAD', 'name': 'Dirham marocain'})
