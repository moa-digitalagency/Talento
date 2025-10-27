#!/bin/bash

###############################################################################
# Script de Nettoyage du Cache - TalentsMaroc.com
# Nettoyage rapide des caches Python et redémarrage de l'application
###############################################################################

set -e

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  🧹 Nettoyage du Cache - TalentsMaroc.com${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Nettoyage des fichiers cache Python
echo -e "\n📁 Suppression des fichiers .pyc et __pycache__..."
find . -type f -name '*.pyc' -delete 2>/dev/null || true
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -type f -name '*.pyo' -delete 2>/dev/null || true

echo -e "${GREEN}✅ Cache Python nettoyé${NC}"

# Redémarrer PM2 si installé
if command -v pm2 &> /dev/null; then
    echo -e "\n🔄 Redémarrage de PM2..."
    pm2 restart all 2>/dev/null || pm2 restart talento 2>/dev/null || true
    pm2 save 2>/dev/null || true
    echo -e "${GREEN}✅ PM2 redémarré${NC}"
    
    # Afficher le statut PM2
    echo -e "\n📊 Statut PM2:"
    pm2 list
fi

# Redémarrer le service systemd si configuré
if systemctl is-enabled talentsmaroc.service &>/dev/null; then
    echo -e "\n🔄 Redémarrage du service systemd..."
    sudo systemctl restart talentsmaroc.service
    echo -e "${GREEN}✅ Service systemd redémarré${NC}"
    
    # Afficher le statut
    echo -e "\n📊 Statut du service:"
    sudo systemctl status talentsmaroc.service --no-pager -n 5
fi

# Si ni PM2 ni systemd ne sont configurés
if ! command -v pm2 &> /dev/null && ! systemctl is-enabled talentsmaroc.service &>/dev/null; then
    echo -e "\n⚠️  Ni PM2 ni systemd détectés - redémarrez manuellement"
    echo -e "   Commandes:"
    echo -e "   - Trouver processus: ps aux | grep gunicorn"
    echo -e "   - Tuer processus: pkill -9 -f gunicorn"
    echo -e "   - Relancer: gunicorn --bind 0.0.0.0:5004 --workers 4 app:app"
fi

echo -e "\n${GREEN}🎉 Nettoyage terminé !${NC}"
echo -e "\n💡 Pour vider le cache navigateur:"
echo -e "   - Chrome/Firefox: Ctrl+Shift+R (ou Cmd+Shift+R sur Mac)"
echo -e "   - Ou: F12 > Onglet Network > Cocher 'Disable cache'\n"
