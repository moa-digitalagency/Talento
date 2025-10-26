#!/bin/bash

###############################################################################
# Script de Déploiement VPS - TalentsMaroc.com
# Par: MOA Digital Agency LLC - Aisance KALONJI
# Description: Script automatisé pour déployer l'application sur un VPS
###############################################################################

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions d'affichage
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
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
APP_NAME="talentsmaroc"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="$APP_DIR/backups"
GIT_REPO_URL="https://github.com/votre-username/talentsmaroc.git"  # À modifier
BRANCH="main"  # ou "production"
PYTHON_VERSION="python3.11"

# Vérifier que le script est exécuté depuis le bon répertoire
if [ ! -f "app.py" ]; then
    print_error "Ce script doit être exécuté depuis le répertoire racine de l'application"
    exit 1
fi

# ============================================================================
# ÉTAPE 1: SAUVEGARDE (si la base de données existe)
# ============================================================================
print_header "ÉTAPE 1: Sauvegarde de l'existant"

if [ -f "$APP_DIR/talento.db" ] || [ ! -z "$DATABASE_URL" ]; then
    # Créer le répertoire de sauvegarde
    mkdir -p "$BACKUP_DIR"
    
    BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/backup_$BACKUP_DATE.tar.gz"
    
    print_info "Création de la sauvegarde: $BACKUP_FILE"
    
    # Sauvegarder la base de données et les uploads
    if [ ! -z "$DATABASE_URL" ]; then
        # PostgreSQL backup
        pg_dump $DATABASE_URL > "$BACKUP_DIR/db_$BACKUP_DATE.sql" 2>/dev/null || true
    fi
    
    # Archiver les fichiers importants
    tar -czf "$BACKUP_FILE" \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='*.pyc' \
        "app/static/uploads/" \
        "*.db" \
        ".env" \
        2>/dev/null || true
    
    print_success "Sauvegarde créée: $BACKUP_FILE"
else
    print_info "Aucune base de données existante à sauvegarder"
fi

# ============================================================================
# ÉTAPE 2: MISE À JOUR DU CODE DEPUIS GIT
# ============================================================================
print_header "ÉTAPE 2: Mise à jour du code depuis Git"

# Vérifier si c'est un dépôt Git
if [ -d ".git" ]; then
    print_info "Mise à jour depuis Git..."
    
    # Sauvegarder les modifications locales (si nécessaire)
    git stash save "Auto-stash avant déploiement $(date)" || true
    
    # Récupérer les dernières modifications
    git fetch origin
    
    # Merger ou reset selon votre stratégie
    print_info "Fusion des modifications..."
    git pull origin $BRANCH || {
        print_error "Impossible de récupérer les modifications"
        print_warning "Tentative de récupération des changements stashés..."
        git stash pop || true
        exit 1
    }
    
    # Restaurer les modifications locales si nécessaire
    # git stash pop || true
    
    print_success "Code mis à jour depuis Git"
else
    print_warning "Le répertoire n'est pas un dépôt Git"
    print_info "Pour initialiser Git:"
    echo "  git init"
    echo "  git remote add origin $GIT_REPO_URL"
    echo "  git pull origin $BRANCH"
fi

# ============================================================================
# ÉTAPE 3: ENVIRONNEMENT VIRTUEL PYTHON
# ============================================================================
print_header "ÉTAPE 3: Configuration de l'environnement virtuel Python"

# Vérifier Python
if ! command -v $PYTHON_VERSION &> /dev/null; then
    print_error "Python 3.11+ n'est pas installé"
    print_info "Installation de Python 3.11:"
    echo "  sudo apt update"
    echo "  sudo apt install python3.11 python3.11-venv python3.11-dev -y"
    exit 1
fi

print_info "Python trouvé: $($PYTHON_VERSION --version)"

# Créer ou réactiver l'environnement virtuel
if [ ! -d "$VENV_DIR" ]; then
    print_info "Création de l'environnement virtuel..."
    $PYTHON_VERSION -m venv "$VENV_DIR"
    print_success "Environnement virtuel créé"
else
    print_info "Environnement virtuel existant trouvé"
fi

# Activer l'environnement virtuel
print_info "Activation de l'environnement virtuel..."
source "$VENV_DIR/bin/activate"

# Mettre à jour pip
print_info "Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

print_success "Environnement virtuel activé"

# ============================================================================
# ÉTAPE 4: INSTALLATION DES DÉPENDANCES
# ============================================================================
print_header "ÉTAPE 4: Installation des dépendances Python"

if [ -f "requirements.txt" ]; then
    print_info "Installation des packages depuis requirements.txt..."
    pip install -r requirements.txt
    print_success "Dépendances installées avec succès"
else
    print_error "Fichier requirements.txt introuvable"
    exit 1
fi

# ============================================================================
# ÉTAPE 5: VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT
# ============================================================================
print_header "ÉTAPE 5: Vérification de la configuration"

if [ ! -f ".env" ]; then
    print_warning "Fichier .env introuvable"
    print_info "Création d'un fichier .env template..."
    
    cat > .env << 'EOF'
# Configuration TalentsMaroc.com
# IMPORTANT: Modifiez ces valeurs en production!

# Obligatoires
SECRET_KEY=changez-cette-cle-secrete-en-production-utilisez-une-chaine-aleatoire-longue
DATABASE_URL=postgresql://user:password@localhost:5432/talentsmaroc
ENCRYPTION_KEY=generez-avec-cryptography-fernet-generatekey

# Optionnelles (API Keys - configurables via l'interface admin)
SENDGRID_API_KEY=
SENDGRID_FROM_EMAIL=noreply@talentsmaroc.com
OPENROUTER_API_KEY=
TMDB_API_KEY=

# Admin par défaut
ADMIN_PASSWORD=@4dm1n

# Flask Environment
FLASK_ENV=production
EOF
    
    print_success "Fichier .env template créé"
    print_warning "⚠️  IMPORTANT: Éditez le fichier .env et configurez les variables obligatoires!"
    print_info "Pour générer ENCRYPTION_KEY:"
    echo "  python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
fi

# Charger les variables d'environnement
set -a
[ -f .env ] && . .env
set +a

# Vérifier les variables critiques
print_info "Vérification des variables d'environnement..."

missing_vars=()
[ -z "$SECRET_KEY" ] && missing_vars+=("SECRET_KEY")
[ -z "$DATABASE_URL" ] && missing_vars+=("DATABASE_URL")
[ -z "$ENCRYPTION_KEY" ] && missing_vars+=("ENCRYPTION_KEY")

if [ ${#missing_vars[@]} -gt 0 ]; then
    print_error "Variables d'environnement manquantes:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    print_info "Éditez le fichier .env et relancez le script"
    exit 1
fi

print_success "Configuration vérifiée"

# ============================================================================
# ÉTAPE 6: BASE DE DONNÉES
# ============================================================================
print_header "ÉTAPE 6: Initialisation de la base de données"

# Vérifier si PostgreSQL est installé (si DATABASE_URL pointe vers PostgreSQL)
if [[ $DATABASE_URL == postgresql://* ]] || [[ $DATABASE_URL == postgres://* ]]; then
    if ! command -v psql &> /dev/null; then
        print_warning "PostgreSQL client non trouvé"
        print_info "Installation de PostgreSQL:"
        echo "  sudo apt install postgresql postgresql-contrib libpq-dev -y"
    fi
fi

# Exécuter le script de migration/initialisation
print_info "Exécution des migrations de base de données..."

if [ -f "migrations_init.py" ]; then
    python migrations_init.py || {
        print_error "Échec de l'initialisation de la base de données"
        exit 1
    }
    print_success "Base de données initialisée"
else
    print_warning "Script migrations_init.py introuvable"
    print_info "Tentative d'initialisation via Flask-Migrate..."
    
    # Initialiser Flask-Migrate si nécessaire
    if [ ! -d "migrations" ]; then
        flask db init || true
    fi
    
    # Générer et appliquer les migrations
    flask db migrate -m "Auto migration - déploiement $(date +%Y%m%d)" || true
    flask db upgrade || true
fi

# Créer les répertoires nécessaires
print_info "Création des répertoires de stockage..."
mkdir -p app/static/uploads/photos
mkdir -p app/static/uploads/cvs
mkdir -p app/static/uploads/qrcodes
mkdir -p app/static/uploads/cinema
mkdir -p logs
mkdir -p backups

print_success "Répertoires créés"

# ============================================================================
# ÉTAPE 7: CONFIGURATION DU SERVICE SYSTEMD (optionnel)
# ============================================================================
print_header "ÉTAPE 7: Configuration du service systemd (optionnel)"

read -p "Voulez-vous configurer un service systemd pour démarrer automatiquement l'application? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
    
    print_info "Création du fichier de service systemd..."
    
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=TalentsMaroc.com Flask Application
After=network.target postgresql.service

[Service]
Type=notify
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --bind 0.0.0.0:5000 --reuse-port --workers 4 --timeout 120 app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
    
    print_success "Fichier de service créé: $SERVICE_FILE"
    
    # Recharger systemd et activer le service
    print_info "Activation du service..."
    sudo systemctl daemon-reload
    sudo systemctl enable "${APP_NAME}.service"
    
    print_success "Service systemd configuré et activé"
    print_info "Commandes utiles:"
    echo "  - Démarrer: sudo systemctl start $APP_NAME"
    echo "  - Arrêter: sudo systemctl stop $APP_NAME"
    echo "  - Redémarrer: sudo systemctl restart $APP_NAME"
    echo "  - Statut: sudo systemctl status $APP_NAME"
    echo "  - Logs: sudo journalctl -u $APP_NAME -f"
fi

# ============================================================================
# ÉTAPE 8: CONFIGURATION NGINX (optionnel)
# ============================================================================
print_header "ÉTAPE 8: Configuration NGINX (optionnel)"

read -p "Voulez-vous configurer NGINX comme reverse proxy? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    if ! command -v nginx &> /dev/null; then
        print_warning "NGINX n'est pas installé"
        print_info "Installation de NGINX:"
        echo "  sudo apt install nginx -y"
    else
        read -p "Nom de domaine (ex: talentsmaroc.com): " DOMAIN_NAME
        
        NGINX_CONF="/etc/nginx/sites-available/$APP_NAME"
        
        print_info "Création de la configuration NGINX..."
        
        sudo tee "$NGINX_CONF" > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;
    
    # Logs
    access_log /var/log/nginx/${APP_NAME}_access.log;
    error_log /var/log/nginx/${APP_NAME}_error.log;
    
    # Upload size limit
    client_max_body_size 10M;
    
    # Proxy vers Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    # Fichiers statiques
    location /static {
        alias $APP_DIR/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Fichiers uploads
    location /uploads {
        alias $APP_DIR/app/static/uploads;
        expires 7d;
    }
}
EOF
        
        # Activer le site
        sudo ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/
        
        # Tester la configuration
        sudo nginx -t && {
            print_success "Configuration NGINX créée et testée"
            
            # Recharger NGINX
            sudo systemctl reload nginx
            print_success "NGINX rechargé"
            
            print_info "Configuration SSL avec Certbot (Let's Encrypt):"
            echo "  sudo apt install certbot python3-certbot-nginx -y"
            echo "  sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
        } || {
            print_error "Erreur dans la configuration NGINX"
        }
    fi
fi

# ============================================================================
# ÉTAPE 9: TESTS ET VÉRIFICATIONS
# ============================================================================
print_header "ÉTAPE 9: Tests et vérifications"

print_info "Vérification de l'application..."

# Test d'import Python
python -c "from app import create_app; app = create_app(); print('✅ Application Flask OK')" || {
    print_error "Erreur lors de l'import de l'application"
    exit 1
}

# Vérifier les ports
print_info "Vérification du port 5000..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    print_warning "Le port 5000 est déjà utilisé"
    print_info "Processus utilisant le port 5000:"
    lsof -i :5000 || true
else
    print_success "Port 5000 disponible"
fi

# ============================================================================
# ÉTAPE 10: DÉMARRAGE DE L'APPLICATION
# ============================================================================
print_header "ÉTAPE 10: Démarrage de l'application"

read -p "Comment voulez-vous démarrer l'application? (1=Systemd, 2=Manuel Gunicorn, 3=Développement Flask, 4=Ne pas démarrer): " -n 1 -r
echo

case $REPLY in
    1)
        if systemctl is-enabled "${APP_NAME}.service" &>/dev/null; then
            print_info "Démarrage via systemd..."
            sudo systemctl restart "${APP_NAME}.service"
            sleep 3
            sudo systemctl status "${APP_NAME}.service" --no-pager
            print_success "Application démarrée via systemd"
            print_info "Logs en direct: sudo journalctl -u $APP_NAME -f"
        else
            print_error "Service systemd non configuré"
        fi
        ;;
    2)
        print_info "Démarrage manuel avec Gunicorn..."
        print_warning "L'application tournera en arrière-plan"
        nohup gunicorn --bind 0.0.0.0:5000 --reuse-port --workers 4 --timeout 120 app:app > logs/gunicorn.log 2>&1 &
        sleep 2
        print_success "Gunicorn démarré (PID: $!)"
        print_info "Logs: tail -f logs/gunicorn.log"
        ;;
    3)
        print_info "Démarrage en mode développement Flask..."
        print_warning "Ceci est destiné au développement uniquement!"
        python app.py
        ;;
    4)
        print_info "Application non démarrée"
        print_info "Pour démarrer manuellement:"
        echo "  source venv/bin/activate"
        echo "  gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"
        ;;
    *)
        print_warning "Choix invalide"
        ;;
esac

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================
print_header "DÉPLOIEMENT TERMINÉ"

echo ""
print_success "TalentsMaroc.com a été déployé avec succès!"
echo ""

print_info "📋 INFORMATIONS IMPORTANTES:"
echo ""
echo "  🌐 URL de l'application:"
if [ ! -z "$DOMAIN_NAME" ]; then
    echo "     http://$DOMAIN_NAME"
else
    echo "     http://$(hostname -I | awk '{print $1}'):5000"
fi
echo ""

echo "  👤 Compte Administrateur:"
echo "     Email: admin@talento.com"
echo "     Code: MAN0001RAB"
echo "     Mot de passe: @4dm1n"
echo "     ⚠️  CHANGEZ LE MOT DE PASSE après la première connexion!"
echo ""

echo "  📂 Répertoires importants:"
echo "     - Application: $APP_DIR"
echo "     - Environnement virtuel: $VENV_DIR"
echo "     - Sauvegardes: $BACKUP_DIR"
echo "     - Logs: $APP_DIR/logs"
echo "     - Uploads: $APP_DIR/app/static/uploads"
echo ""

echo "  🔧 Commandes utiles:"
echo "     - Activer venv: source venv/bin/activate"
echo "     - Logs app: tail -f logs/gunicorn.log"
echo "     - Redémarrer: sudo systemctl restart $APP_NAME"
echo "     - Sauvegarde: ./deploy_vps.sh (ÉTAPE 1 uniquement)"
echo ""

echo "  📚 Documentation:"
echo "     - README.md - Guide utilisateur"
echo "     - docs/TECHNICAL_DOCUMENTATION.md - Documentation technique"
echo "     - api_docs/ - Documentation API REST"
echo ""

print_warning "⚠️  N'OUBLIEZ PAS:"
echo "  1. Configurer les clés API dans .env ou via l'interface admin"
echo "  2. Configurer SSL/HTTPS avec Certbot pour la production"
echo "  3. Mettre en place des sauvegardes automatiques (cron)"
echo "  4. Changer le mot de passe admin par défaut"
echo "  5. Surveiller les logs régulièrement"
echo ""

print_header "🎉 Bon déploiement!"

deactivate 2>/dev/null || true

exit 0
