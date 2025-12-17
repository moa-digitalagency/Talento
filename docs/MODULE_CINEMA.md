# Module CINEMA - Documentation Complete

**Guide detaille du module cinematographique de taalentio.com**
**Version 2.0 | Decembre 2024**

---

## Table des matieres

1. [Presentation du module](#presentation-du-module)
2. [Inscription des talents](#inscription-des-talents)
3. [Gestion des productions](#gestion-des-productions)
4. [Gestion des projets](#gestion-des-projets)
5. [Systeme de presences](#systeme-de-presences)
6. [Recherche et casting](#recherche-et-casting)
7. [Notifications et communications](#notifications-et-communications)
8. [Equipe technique](#equipe-technique)

---

## Presentation du module

Le module CINEMA de taalentio.com est concu specifiquement pour l'industrie audiovisuelle africaine. Il permet de gerer l'ensemble du cycle de vie d'un projet cinematographique : recrutement de talents, gestion des productions, suivi des projets et enregistrement des presences.

### Acces au module

Le module CINEMA est accessible :
- Via la page d'accueil pour l'inscription publique
- Via le menu principal apres connexion (utilisateurs avec droits)

### Composants principaux

1. **Talents CINEMA** - Base de donnees des acteurs, figurants, cascadeurs
2. **Productions** - Societes de production cinematographiques
3. **Projets** - Films, series, publicites en cours
4. **Presences** - Suivi des heures de travail sur les tournages

---

## Inscription des talents

### Formulaire d'inscription

L'inscription CINEMA se fait en 9 sections progressives.

#### Section 1 : Identite

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Prenom | Texte | Oui | 100 caracteres max |
| Nom | Texte | Oui | 100 caracteres max |
| Genre | Selection | Oui | Homme (M) / Femme (F) |
| Date de naissance | Date | Oui | Format JJ/MM/AAAA |

#### Section 2 : Piece d'identite

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Type de document | Selection | Oui | CIN, Passeport, Carte sejour |
| Numero | Texte | Oui | Chiffre (donnee securisee) |

#### Section 3 : Origines

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Ethnicites | Multi-selection | Non | Choix multiples |
| Pays d'origine | Selection | Non | Liste 54 pays |
| Nationalite | Selection | Oui | 190+ nationalites |

#### Section 4 : Residence

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Pays de residence | Selection | Oui | Liste 54 pays |
| Ville de residence | Selection | Oui | Chargement dynamique |

#### Section 5 : Langues et experience

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Langues parlees | Multi-selection | Non | 60+ langues avec drapeaux |
| Annees d'experience | Nombre | Non | 0 a 50 ans |

#### Section 6 : Caracteristiques physiques

| Champ | Options | Description |
|-------|---------|-------------|
| Couleur des yeux | Marron fonce, Marron, Marron clair, Noisette, Vert, Vert clair, Bleu, Bleu clair, Gris, Ambre, Noir, Vairons | 12 options |
| Couleur de cheveux | Noir, Brun fonce, Brun, Chatain fonce, Chatain, Chatain clair, Blond fonce, Blond, Blond platine, Roux, Auburn, Poivre et sel, Gris, Blanc, Colores/Fantaisie, Chauve/Rase | 16 options |
| Type de cheveux | Raides, Ondules, Boucles, Frises, Crepus, Afro, Tresses, Locks/Dreadlocks, Rases, Chauve | 10 options |
| Taille | Nombre | En centimetres (ex: 175) |
| Teint de peau | Tres clair, Clair, Moyen clair, Moyen, Olivatre, Mat, Bronze, Fonce, Tres fonce, Noir profond | 10 options |
| Morphologie | Tres mince, Mince, Svelte, Athletique, Muscle, Moyen, Fort, Rond, Corpulent, Imposant | 10 options |

#### Section 7 : Types de talents

**Choix multiples parmi 13 categories :**

| Type | Description |
|------|-------------|
| Acteur/Actrice Principal(e) | Roles principaux |
| Acteur/Actrice Secondaire | Roles secondaires |
| Figurant(e) | Apparitions en arriere-plan |
| Silhouette | Apparitions breves |
| Doublure | Remplacement acteur principal |
| Doublure Lumiere | Tests d'eclairage |
| Cascadeur/Cascadeuse | Scenes d'action |
| Mannequin | Photographie, mode |
| Voix Off | Narration, doublage |
| Figurant Specialise | Competences specifiques |
| Choriste | Chant de groupe |
| Danseur/Danseuse de fond | Scenes de danse |
| Autre | Autres specialites |

#### Section 8 : Competences additionnelles

**Categories de competences :**

- **Talents artistiques** : Danse, chant, dessin, musique, calligraphie
- **Sports** : Arts martiaux, yoga, gymnastique, equitation, natation
- **Competences manuelles** : Couture, jardinage, cuisine, poterie
- **Competences sociales** : Multilinguisme, animation, leadership
- **Competences techniques** : Montage video, graphisme, reseaux sociaux

#### Section 9 : Contact et reseaux sociaux

| Champ | Securite |
|-------|----------|
| Email | Non chiffre (identifiant) |
| Telephone | Chiffre |
| WhatsApp | Chiffre |
| Site web | Non chiffre |
| Facebook | Chiffre |
| Instagram | Chiffre |
| LinkedIn | Chiffre |
| Twitter | Chiffre |
| YouTube | Chiffre |
| TikTok | Chiffre |
| Snapchat | Chiffre |
| Telegram | Chiffre |
| IMDb | Chiffre |
| Threads | Chiffre |

### Code unique CINEMA

**Format : PPVVVNNNNNNG** (12 caracteres)

- **PP** : Code pays ISO-2 (MA, SN, CI, etc.)
- **VVV** : 3 premieres lettres de la ville (CAS, DAK, ABJ)
- **NNNNNN** : Numero sequentiel a 6 chiffres
- **G** : Genre (M ou F)

**Exemple** : MACAS000042F
- MA = Maroc
- CAS = Casablanca
- 000042 = 42eme inscription
- F = Femme

### Photo de profil et galerie

**Specifications photos :**
- Formats acceptes : PNG, JPG, JPEG
- Taille maximale : 5 Mo par image
- Resolution recommandee : 800x800 pixels minimum
- Galerie : Jusqu'a 10 photos supplementaires

---

## Gestion des productions

### Creation d'une production

Les administrateurs peuvent creer des fiches de societes de production.

#### Informations de base

| Champ | Description |
|-------|-------------|
| Nom | Nom de la societe |
| Logo | Image PNG/JPG |
| Description | Presentation de la societe |
| Specialisation | Films, Series, Documentaires, Publicites |

#### Coordonnees

| Champ | Description |
|-------|-------------|
| Adresse | Siege social |
| Ville | Ville |
| Pays | Pays |
| Code postal | Code postal |

#### Contact

| Champ | Description |
|-------|-------------|
| Telephone | Numero principal |
| Email | Email de contact |
| Site web | URL du site |

#### Reseaux sociaux

- Facebook
- Instagram
- LinkedIn
- Twitter/X

#### Informations entreprise

| Champ | Description |
|-------|-------------|
| Annee de fondation | Annee de creation |
| Directeur/CEO | Nom du dirigeant |
| Nombre d'employes | Effectif |
| Productions realisees | Nombre de productions |
| Productions notables | Liste des oeuvres connues |

#### Services et equipements

| Champ | Description |
|-------|-------------|
| Services | Production, Post-production, Distribution |
| Equipements | Description du materiel |
| Studios | Description des studios |

#### Certifications

| Champ | Description |
|-------|-------------|
| Certifications | Agrements professionnels |
| Affiliations | Syndicats, associations |
| Prix | Recompenses obtenues |

### Statut de verification

Les productions peuvent etre marquees comme "verifiees" par les administrateurs apres validation des informations.

---

## Gestion des projets

### Creation d'un projet

Un projet represente une production specifique (film, serie, publicite).

#### Informations projet

| Champ | Type | Description |
|-------|------|-------------|
| Nom | Texte | Titre du projet |
| Type | Selection | Film, Serie, Publicite, Documentaire, Clip |
| Societe de production | Selection | Lien vers Production |
| Pays d'origine | Texte | Nationalite du projet |
| Lieux de tournage | Texte | Localisation(s) |
| Date de debut | Date | Debut tournage |
| Date de fin | Date | Fin tournage |
| Statut | Selection | Preparation, Tournage, Post-production, Termine |

### Statuts de projet

| Statut | Description |
|--------|-------------|
| En preparation | Pre-production, casting |
| En tournage | Production en cours |
| Post-production | Montage, effets |
| Termine | Projet clos |

### Assignation de talents

Pour assigner un talent a un projet :

1. Ouvrir le detail du projet
2. Cliquer sur "Ajouter un talent"
3. Entrer le code unique du talent CINEMA
4. Selectionner le type de role
5. Ajouter une description (optionnel)
6. Valider

**Code projet genere automatiquement** : PRJ-XXX-YYY

### Badges projet

Pour chaque talent assigne, un badge personnalise peut etre genere :
- Format PDF
- Contient : Photo, nom, code, projet, role
- QR code d'identification
- Telechargeable et imprimable

### Envoi de notifications

Bouton "Envoyer emails" pour notifier tous les talents assignes :
- Email de confirmation de selection
- Details du projet
- Informations de la production
- Lien vers le badge

---

## Systeme de presences

### Acces

Le systeme de presences est accessible aux utilisateurs avec le role "presence" ou administrateur.

### Enregistrement des presences

#### Vue par projet

1. Selectionner un projet
2. Voir la liste des talents assignes
3. Scanner le QR code ou entrer le code manuellement
4. Le systeme enregistre :
   - Premier scan : Heure d'arrivee
   - Deuxieme scan : Heure de depart

#### Actions groupees

- **Pointer tous presents** : Marque l'arrivee de tous les talents
- **Pointer tous partis** : Marque le depart de tous les talents presents

### Calcul des heures

Le systeme calcule automatiquement :
- Duree de presence par jour
- Total d'heures par talent
- Total d'heures par projet

### Historique

Pour chaque talent, historique consultable :
- Jours travailles
- Heures par projet
- Total cumule

### Export

Export des presences en Excel :
- Par jour
- Par semaine
- Par mois
- Par periode personnalisee

---

## Recherche et casting

### Filtres de recherche

La recherche de talents CINEMA offre 12 criteres :

| Filtre | Type | Description |
|--------|------|-------------|
| Nom | Texte | Recherche par nom/prenom |
| Type de talent | Selection | 13 categories |
| Genre | Selection | Homme/Femme |
| Age | Tranche | 18-25, 26-35, 36-50, 51+ |
| Ethnicite | Selection | Origines multiples |
| Couleur des yeux | Selection | 12 couleurs |
| Couleur de cheveux | Selection | 16 couleurs |
| Teint | Selection | 10 teintes |
| Taille | Intervalle | Min/Max en cm |
| Pays | Selection | 54 pays |
| Langues | Multi-selection | 60+ langues |
| Experience | Selection | Debutant, 1-5 ans, 5-10 ans, 10+ ans |

### Casting IA

Le casting par intelligence artificielle permet de :

1. **Decrire le role recherche** (texte libre ou upload de fichier)
2. **Specifier des criteres** :
   - Age approximatif
   - Caracteristiques physiques
   - Competences requises
   - Langues necessaires

3. **Obtenir des resultats classes** :
   - Score de correspondance (0-100%)
   - Justification du match
   - Points forts du candidat
   - Points d'amelioration

### Export des resultats

Les resultats de recherche/casting sont exportables en :
- Excel
- PDF avec photos

---

## Notifications et communications

### Emails automatiques

#### A l'inscription

**Template : cinema_talent_registration**

Contenu :
- Bienvenue sur le module CINEMA
- Code unique attribue
- Lien vers le profil public
- Instructions de connexion

#### A la selection

**Template : project_selection**

Contenu :
- Nom du projet
- Type de production
- Role attribue
- Coordonnees de la production
- Lien vers le badge

#### Matching IA

**Template : ai_cinema_match**

Contenu :
- Description du role recherche
- Score de correspondance
- Raison du match
- Instructions de suivi

### Recapitulatif hebdomadaire

Chaque dimanche, email automatique a l'administrateur :
- Nombre de nouveaux talents CINEMA
- Tableau detaille des inscriptions
- Liens vers les profils

---

## Equipe technique

### Roles disponibles

| Role | Droits |
|------|--------|
| Administrateur | Acces complet au module CINEMA |
| Presence | Gestion des presences uniquement |

### Gestion de l'equipe

Les administrateurs peuvent :
- Ajouter des membres
- Modifier les roles
- Activer/desactiver les comptes
- Supprimer des membres

### Ajout d'un membre

1. Prenom, nom, email
2. Mot de passe temporaire
3. Attribution du role (admin ou presence)
4. Activation du compte

---

## Statistiques CINEMA

### Metriques disponibles

| Metrique | Description |
|----------|-------------|
| Total talents | Nombre total de talents inscrits |
| Par type | Repartition par categorie |
| Par genre | Homme vs Femme |
| Par pays | Distribution geographique |
| Par langue | Langues parlees |
| Avec photo | Pourcentage avec photo |
| Experience | Niveaux d'experience |

### Dashboard

Le tableau de bord CINEMA affiche :
- Nombre de productions actives
- Nombre de talents actifs
- Nombre de projets en cours
- Membres de l'equipe

---

*Documentation par MOA Digital Agency LLC - www.myoneart.com*
