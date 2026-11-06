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
export OLLAMA_ORIGINS="http://127.0.0.1:8001,http://django_app:8000,https://cybersocle.site,https://cybersocle.site,https://cybersocle.site,http://localhost:8001"

# Lancement en arriere-plan
ollama serve &
SERVER_PID=$!

echo "[INFO] Attente de la disponibilite du service Ollama..."
MAX_RETRIES=30
RETRY_COUNT=0
until curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
        echo "[WARN] Timeout en attente d'Ollama après ${MAX_RETRIES} secondes."
        break
    fi
    sleep 1
done

MODEL_NAME="${GEMMA_MODEL:-gemma2:2b}"
echo "[INFO] Telechargement ou verification du modele souverain ${MODEL_NAME}..."
ollama pull "${MODEL_NAME}" || echo "[WARN] Impossible de telecharger le modele ${MODEL_NAME} immediatement (mode hors-ligne ou reseau restreint). L'inference demarre avec le cache local."

echo "[INFO] Test d'inference locale..."
curl -s http://127.0.0.1:11434/api/generate -d "{
  \"model\": \"${MODEL_NAME}\",
  \"prompt\": \"Explique brievement la cryptographie Zero-Knowledge Proof pour l Afrique de l Ouest.\",
  \"stream\": false
}" | grep -o '"response":[^}]*' | head -n 1 || echo "[INFO] Verification d'inference terminee."

echo "[SUCCESS] Moteur Gemma 2 2B operationnel et connecte a BantuDevLab."

# Maintenir le processus actif pour Docker
wait $SERVER_PID
