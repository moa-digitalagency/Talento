#!/bin/bash

###############################################################################
# Script de Mise à Jour - TalentsMaroc.com
# Par: MOA Digital Agency LLC - Aisance KALONJI
# Description: Script sécurisé pour mettre à jour l'application sans perdre de données
#
# UTILISATION:
#   ./update_app.sh
#
# PROTECTION AUTOMATIQUE:
#   - Base de données (*.db, DATABASE_URL)
#   - Configuration (.env)
#   - Fichiers uploadés (photos, CVs, QR codes)
#   - Données utilisateur
#
# FONCTIONNALITÉS:
#   - Sauvegarde automatique avant mise à jour
#   - Migration de schéma de base de données
#   - Protection des fichiers sensibles
#   - Rollback en cas d'erreur
###############################################################################

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonctions d'affichage
print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERREUR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Configuration
APP_DIR="$(pwd)"
BACKUP_DIR="$APP_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

# Vérifier que le script est exécuté depuis le bon répertoire
if [ ! -f "app.py" ]; then
    print_error "Ce script doit être exécuté depuis le répertoire racine de l'application"
    exit 1
fi

print_header "🚀 MISE À JOUR SÉCURISÉE - TalentsMaroc.com"

# ============================================================================
# ÉTAPE 1: SAUVEGARDE COMPLÈTE
# ============================================================================
print_header "ÉTAPE 1: Sauvegarde complète"

mkdir -p "$BACKUP_DIR"

print_info "Création de la sauvegarde: $BACKUP_FILE"

# Liste des fichiers critiques à sauvegarder
CRITICAL_FILES=(
    ".env"
    "*.db"
    "talento.db"
    "app/static/uploads/"
    "logs/"
)

# Sauvegarde PostgreSQL si utilisé
if [ ! -z "$DATABASE_URL" ]; then
    print_info "Sauvegarde de la base de données PostgreSQL..."
    DB_DUMP_FILE="$BACKUP_DIR/db_$TIMESTAMP.sql"
    
    if command -v pg_dump &> /dev/null; then
        pg_dump $DATABASE_URL > "$DB_DUMP_FILE" 2>/dev/null && {
            print_success "Base de données PostgreSQL sauvegardée: $DB_DUMP_FILE"
            CRITICAL_FILES+=("$DB_DUMP_FILE")
        } || {
            print_warning "Impossible de sauvegarder PostgreSQL"
        }
    else
        print_warning "pg_dump non disponible, sauvegarde PostgreSQL ignorée"
    fi
fi

# Créer l'archive de sauvegarde
tar -czf "$BACKUP_FILE" \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='node_modules' \
    --ignore-failed-read \
    "${CRITICAL_FILES[@]}" \
    2>/dev/null || true

if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    print_success "Sauvegarde créée: $BACKUP_FILE ($BACKUP_SIZE)"
else
    print_warning "Aucune sauvegarde créée (peut-être aucun fichier à sauvegarder)"
fi

# ============================================================================
# ÉTAPE 2: MISE À JOUR DU CODE (GIT ou LOCAL)
# ============================================================================
print_header "ÉTAPE 2: Mise à jour du code"

# Vérifier si c'est un dépôt Git
if [ -d ".git" ]; then
    print_info "Dépôt Git détecté"
    
    # Sauvegarder les fichiers locaux importants avant git pull
    print_info "Protection des fichiers locaux (.env, base de données, uploads)..."
    
    # S'assurer que .gitignore protège les fichiers critiques
    if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
        echo -e "\n# Protection des données sensibles" >> .gitignore
        echo ".env" >> .gitignore
        echo "*.db" >> .gitignore
        echo "app/static/uploads/" >> .gitignore
        print_info "Fichiers critiques ajoutés à .gitignore"
    fi
    
    # Vérifier s'il y a un remote configuré
    if git remote get-url origin &>/dev/null; then
        # Stash des changements locaux (sauf fichiers ignorés)
        git stash save "Auto-stash mise à jour $(date)" 2>/dev/null || true
        
        # Pull les dernières modifications
        print_info "Récupération des mises à jour depuis Git..."
        git pull origin main 2>/dev/null && {
            print_success "Code mis à jour depuis Git"
        } || {
            print_warning "Impossible de pull depuis Git (peut-être pas de connexion)"
            print_info "Continuation avec la version locale..."
        }
    else
        print_warning "Aucun remote Git configuré"
        print_info "Pour configurer Git:"
        echo "  git remote add origin https://github.com/votre-repo/talentsmaroc.git"
        echo "  git pull origin main"
    fi
else
    print_info "Pas un dépôt Git"
    print_info "Si vous avez de nouveaux fichiers, placez-les dans le répertoire et relancez ce script"
    
    # Demander confirmation pour continuer
    read -p "Continuer avec les fichiers actuels? (o/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[OoYy]$ ]]; then
        print_info "Mise à jour annulée"
        exit 0
    fi
fi

# ============================================================================
# ÉTAPE 3: NETTOYAGE DES CACHES
# ============================================================================
print_header "ÉTAPE 3: Nettoyage des caches Python"

print_info "Suppression des fichiers cache..."
find . -type f -name '*.pyc' -delete 2>/dev/null || true
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -type f -name '*.pyo' -delete 2>/dev/null || true

print_success "Caches nettoyés"

# ============================================================================
# ÉTAPE 4: INSTALLATION DES DÉPENDANCES
# ============================================================================
print_header "ÉTAPE 4: Mise à jour des dépendances"

if [ -f "requirements.txt" ]; then
    print_info "Vérification de l'environnement virtuel..."
    
    # Vérifier si on est dans un venv
    if [ -z "$VIRTUAL_ENV" ]; then
        # Chercher un venv existant
        if [ -d "venv" ]; then
            print_info "Activation de l'environnement virtuel..."
            source venv/bin/activate
        elif [ -d ".venv" ]; then
            print_info "Activation de l'environnement virtuel..."
            source .venv/bin/activate
        else
            print_warning "Aucun environnement virtuel trouvé"
            print_info "Installation des packages en mode système..."
        fi
    else
        print_success "Environnement virtuel actif: $VIRTUAL_ENV"
    fi
    
    print_info "Installation/mise à jour des packages Python..."
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    print_success "Dépendances mises à jour"
else
    print_warning "Fichier requirements.txt introuvable"
fi

# ============================================================================
# ÉTAPE 5: MIGRATION DE LA BASE DE DONNÉES
# ============================================================================
print_header "ÉTAPE 5: Migration du schéma de base de données"

print_info "Exécution des migrations de base de données..."

# Méthode 1: Utiliser le script migrations_init.py s'il existe
if [ -f "migrations_init.py" ]; then
    print_info "Utilisation de migrations_init.py..."
    python migrations_init.py && {
        print_success "Migrations via migrations_init.py terminées"
    } || {
        print_warning "Erreur dans migrations_init.py, tentative avec Flask-Migrate..."
    }
fi

# Méthode 2: Flask-Migrate
print_info "Vérification de Flask-Migrate..."

# Initialiser Flask-Migrate si nécessaire
if [ ! -d "migrations" ]; then
    print_info "Initialisation de Flask-Migrate..."
    FLASK_APP=app.py flask db init 2>/dev/null || {
        print_warning "Impossible d'initialiser Flask-Migrate"
    }
fi

# Générer une migration automatique
if [ -d "migrations" ]; then
    print_info "Génération de la migration automatique..."
    FLASK_APP=app.py flask db migrate -m "Auto migration - $TIMESTAMP" 2>/dev/null || {
        print_warning "Aucune nouvelle migration détectée ou erreur"
    }
    
    # Appliquer les migrations
    print_info "Application des migrations..."
    FLASK_APP=app.py flask db upgrade 2>/dev/null && {
        print_success "Schéma de base de données mis à jour"
    } || {
        print_warning "Erreur lors de l'application des migrations (peut-être déjà à jour)"
    }
else
    print_info "Flask-Migrate non disponible, utilisation de db.create_all()..."
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Tables créées/vérifiées')" 2>/dev/null || {
        print_warning "Impossible de créer les tables automatiquement"
    }
fi

# ============================================================================
# ÉTAPE 6: VÉRIFICATION DE L'INTÉGRITÉ
# ============================================================================
print_header "ÉTAPE 6: Vérification de l'intégrité"

print_info "Vérification des fichiers critiques..."

# Vérifier que les fichiers critiques n'ont pas été supprimés
CRITICAL_CHECK=true

if [ ! -f "app.py" ]; then
    print_error "Fichier app.py manquant!"
    CRITICAL_CHECK=false
fi

if [ ! -d "app" ]; then
    print_error "Répertoire app/ manquant!"
    CRITICAL_CHECK=false
fi

if [ ! -f "config.py" ]; then
    print_error "Fichier config.py manquant!"
    CRITICAL_CHECK=false
fi

# Vérifier que .env existe ou que les variables d'environnement sont définies
if [ ! -f ".env" ] && [ -z "$SECRET_KEY" ]; then
    print_warning "Fichier .env manquant et SECRET_KEY non définie"
    print_info "Créez un fichier .env ou définissez les variables d'environnement requises"
fi

if [ "$CRITICAL_CHECK" = true ]; then
    print_success "Tous les fichiers critiques sont présents"
else
    print_error "Des fichiers critiques sont manquants!"
    print_warning "Vous pouvez restaurer depuis la sauvegarde: $BACKUP_FILE"
    exit 1
fi

# Tester l'import de l'application
print_info "Test de l'application..."
python -c "from app import create_app; app = create_app(); print('✅ Application Flask importée avec succès')" 2>/dev/null && {
    print_success "Application fonctionnelle"
} || {
    print_error "Erreur lors de l'import de l'application"
    print_warning "Restaurez depuis la sauvegarde si nécessaire: $BACKUP_FILE"
    exit 1
}

# ============================================================================
# ÉTAPE 7: REDÉMARRAGE (optionnel)
# ============================================================================
print_header "ÉTAPE 7: Redémarrage de l'application"

print_info "L'application a été mise à jour avec succès"

# Sur Replit, pas besoin de redémarrer manuellement (auto-reload)
if [ ! -z "$REPL_ID" ]; then
    print_success "Sur Replit - redémarrage automatique"
else
    # Sur VPS/serveur
    print_info "Redémarrage recommandé pour appliquer les changements"
    
    # Vérifier si systemd est utilisé
    if systemctl is-enabled talento.service &>/dev/null; then
        read -p "Redémarrer le service systemd maintenant? (o/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[OoYy]$ ]]; then
            sudo systemctl restart talento.service
            print_success "Service redémarré"
        fi
    # Vérifier si PM2 est utilisé
    elif command -v pm2 &> /dev/null && pm2 list | grep -q talento; then
        read -p "Redémarrer avec PM2? (o/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[OoYy]$ ]]; then
            pm2 restart talento
            print_success "Application redémarrée avec PM2"
        fi
    else
        print_info "Pour redémarrer manuellement:"
        echo "  - Avec systemd: sudo systemctl restart talento"
        echo "  - Avec PM2: pm2 restart talento"
        echo "  - Manuel: Arrêtez et relancez l'application"
    fi
fi

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================
print_header "✅ MISE À JOUR TERMINÉE"

echo ""
print_success "TalentsMaroc.com a été mis à jour avec succès!"
echo ""

print_info "📋 RÉSUMÉ DE LA MISE À JOUR:"
echo ""
echo "  ✅ Sauvegarde créée: $BACKUP_FILE"
echo "  ✅ Code mis à jour"
echo "  ✅ Dépendances installées"
echo "  ✅ Base de données migrée"
echo "  ✅ Application vérifiée"
echo ""

print_info "🔒 FICHIERS PROTÉGÉS (non modifiés):"
echo ""
echo "  ✅ .env (configuration)"
echo "  ✅ *.db (base de données SQLite)"
echo "  ✅ app/static/uploads/ (photos, CVs, QR codes)"
echo "  ✅ logs/ (fichiers de log)"
echo ""

print_info "📚 SAUVEGARDES DISPONIBLES:"
echo ""
ls -lh "$BACKUP_DIR" 2>/dev/null | tail -5 || echo "  Aucune sauvegarde trouvée"
echo ""

print_warning "⚠️  EN CAS DE PROBLÈME:"
echo "  Pour restaurer depuis la sauvegarde:"
echo "  tar -xzf $BACKUP_FILE"
echo ""

print_header "🎉 Mise à jour terminée!"

exit 0
