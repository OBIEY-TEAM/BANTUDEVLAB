#!/usr/bin/env bash
# =========================================================================
#  BANTUDEVLAB - Script de Mise a Jour VPS (Production Docker)
#  Met a jour le deploiement existant sans ecraser .env.production ni les volumes.
# =========================================================================

set -euo pipefail

BRANCH="${1:-docker-cadev26}"
export ENV_FILE="${ENV_FILE:-.env.production}"
COMPOSE_FILE="docker-compose.production.yml"

echo "[1/5] Verification des prerequis..."
if ! command -v docker >/dev/null 2>&1; then
    echo "ERREUR: Docker n'est pas installe ou accessible." >&2
    exit 1
fi

DOCKER_CMD="docker"
if ! docker info >/dev/null 2>&1; then
    if command -v sudo >/dev/null 2>&1 && sudo -n docker info >/dev/null 2>&1; then
        DOCKER_CMD="sudo docker"
    elif command -v sudo >/dev/null 2>&1; then
        echo "INFO: Permission requise sur /var/run/docker.sock, utilisation de sudo..."
        DOCKER_CMD="sudo docker"
    else
        echo "ERREUR: Permission refusee sur /var/run/docker.sock." >&2
        echo "Executez avec sudo ou ajoutez votre utilisateur au groupe docker :" >&2
        echo "  sudo usermod -aG docker \$USER && newgrp docker" >&2
        exit 1
    fi
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "ERREUR: Fichier '$ENV_FILE' introuvable." >&2
    echo "Copiez .env.production.example vers $ENV_FILE et renseignez vos secrets locaux." >&2
    exit 1
fi

echo "[2/5] Mise a jour du code depuis la branche '$BRANCH'..."
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

echo "[3/5] Validation de la configuration Docker Compose..."
$DOCKER_CMD compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" config -q

echo "[4/5] Reconstruction et redemarrage des conteneurs (sans perte de volumes)..."
$DOCKER_CMD compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --pull
$DOCKER_CMD compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --remove-orphans

echo "[5/5] Verification de sante des services..."
sleep 5
$DOCKER_CMD compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" ps

if command -v curl >/dev/null 2>&1; then
    if curl -fsS http://127.0.0.1:8000/healthz >/dev/null 2>&1; then
        echo "OK: Portail Django (/healthz) operationnel."
    else
        echo "INFO: /healthz pas encore pret (migrations/demarrage en cours). Verifiez avec: $DOCKER_CMD compose -f $COMPOSE_FILE logs -f django_app"
    fi
fi

echo "Mise a jour VPS terminee."
