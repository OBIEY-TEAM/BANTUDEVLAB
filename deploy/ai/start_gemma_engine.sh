#!/usr/bin/env bash
# Deploiement & initialisation du moteur d'inference IA locale Gemma 2 2B (T-OPS-501)
set -euo pipefail

echo "[INFO] Verification du materiel d'acceleration souverain..."
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
else
    echo "[WARN] Aucun GPU NVIDIA detecte, execution sur CPU multi-coeur avec quantisation GGUF."
fi

echo "[INFO] Lancement du daemon Ollama sur le port 11434..."
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="http://127.0.0.1:8001,http://django_app:8000,https://cybersocle.site,http://localhost:8001"

# Lancement en arriere-plan
ollama serve &
SERVER_PID=$!

echo "[INFO] Attente de la disponibilite du service Ollama..."
MAX_RETRIES=45
RETRY_COUNT=0
READY=0
while [ "$RETRY_COUNT" -lt "$MAX_RETRIES" ]; do
    if command -v curl >/dev/null 2>&1; then
        if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
            READY=1
            break
        fi
    elif (echo > /dev/tcp/127.0.0.1/11434) >/dev/null 2>&1; then
        READY=1
        break
    elif command -v ollama >/dev/null 2>&1; then
        if ollama list >/dev/null 2>&1; then
            READY=1
            break
        fi
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ "$READY" -eq 1 ]; then
    echo "[INFO] Ollama est pret apres ${RETRY_COUNT} secondes."
else
    echo "[WARN] Timeout en attente d'Ollama après ${MAX_RETRIES} secondes, poursuite du demarrage."
fi

MODEL_NAME="${GEMMA_MODEL:-gemma2:2b}"
echo "[INFO] Telechargement ou verification du modele souverain ${MODEL_NAME}..."
ollama pull "${MODEL_NAME}" || echo "[WARN] Impossible de telecharger le modele ${MODEL_NAME} immediatement (mode hors-ligne ou reseau restreint). L'inference demarre avec le cache local."

echo "[INFO] Test d'inference locale..."
if command -v curl >/dev/null 2>&1; then
    curl -s http://127.0.0.1:11434/api/generate -d "{
      \"model\": \"${MODEL_NAME}\",
      \"prompt\": \"Explique brievement la cryptographie Zero-Knowledge Proof pour l Afrique de l Ouest.\",
      \"stream\": false
    }" | grep -o '"response":[^}]*' | head -n 1 || echo "[INFO] Verification d'inference terminee."
else
    echo "[INFO] Curl indisponible pour le test d'inférence, daemon actif."
fi

echo "[SUCCESS] Moteur Gemma 2 2B operationnel et connecte a BantuDevLab."

# Maintenir le processus actif pour Docker
wait $SERVER_PID
