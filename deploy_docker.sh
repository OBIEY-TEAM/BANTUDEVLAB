#!/usr/bin/env bash
# =========================================================================
#  BANTUDEVLAB - Script Bash de Deploiement Automatique Docker
# =========================================================================

set -euo pipefail

echo "[1/3] Verification des prerequis Docker..."
if ! command -v docker >/dev/null 2>&1; then
    echo "ERREUR: Docker n'est pas installe ou pas accessible dans le PATH." >&2
    exit 1
fi

echo "[2/3] Construction et demarrage des conteneurs BANTUDEVLAB..."
docker compose up -d --build

echo "[3/3] Deploiement termine avec succes !"
echo ""
echo "========================================================================="
echo " SERVICES BANTUDEVLAB DISPONIBLES :"
echo "========================================================================="
echo " - Portail BantuDevLab : http://localhost:8001/"
echo " - Connexion Gitea     : http://localhost:3002/user/login"
echo " - Moteur Forge Git    : http://localhost:3001/"
echo ""
echo " Provisionnement des comptes :"
echo " - Administrateur : defini via variables d'environnement (BANTU_ADMIN_USER, BANTU_ADMIN_PASSWORD)"
echo " - Demonstration CADEV 2026 : compte 'cadev_evaluator' (authentification ZKP sans mot de passe)"
echo "========================================================================="
