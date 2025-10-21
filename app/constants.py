"""
Constantes de l'application TalentsMaroc.com
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
        'talents': [
            'Acteur/Actrice', 'Chanteur', 'Danseur', 'Comédien de doublage',
            'Humoriste', 'Présentateur/Animateur', 'Conteur'
        ]
    },
    {
        'name': 'Arts visuels',
        'emoji': '🎨',
        'talents': [
            'Photographe', 'Peintre', 'Sculpteur', 'Illustrateur',
            'Designer graphique', 'Maquilleur', 'Tatoueur'
        ]
    },
    {
        'name': 'Musique',
        'emoji': '🎵',
        'talents': [
            'Musicien', 'Compositeur', 'DJ', 'Producteur musical',
            'Ingénieur du son', 'Beatmaker'
        ]
    },
    {
        'name': 'Sports & Arts martiaux',
        'emoji': '⚽',
        'talents': [
            'Cascadeur', 'Arts martiaux', 'Acrobate', 'Équitation',
            'Sports de combat', 'Natation', 'Plongée', 'Parkour',
            'Gymnastique', 'Danse sportive', 'Autres sports'
        ]
    },
    {
        'name': 'Techniques & Créatives',
        'emoji': '🎬',
        'talents': [
            'Chorégraphe', 'Metteur en scène', 'Réalisateur',
            'Scénariste', 'Monteur vidéo', 'Cadreur/Opérateur'
        ]
    },
    {
        'name': 'Autres',
        'emoji': '✨',
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
