"""
Constantes de l'application Talento
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
    'Afrikaans', 'Allemand', 'Amazigh (Berbère)', 'Anglais', 'Arabe', 'Arménien',
    'Chinois (Mandarin)', 'Chinois (Cantonais)', 'Coréen', 'Créole', 'Espagnol',
    'Français', 'Grec', 'Haoussa', 'Hébreu', 'Hindi', 'Italien', 'Japonais',
    'Néerlandais', 'Norvégien', 'Polonais', 'Portugais', 'Roumain', 'Russe',
    'Suédois', 'Swahili', 'Turc', 'Ukrainien', 'Wolof', 'Yoruba', 'Zoulou', 'Autre'
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
