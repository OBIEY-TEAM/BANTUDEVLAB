#!/usr/bin/env bash
# Deploiement & initialisation du moteur d'inference IA locale Gemma 5B
set -euo pipefail

echo "[INFO] Verification du GPU souverain NVIDIA..."
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
else
    echo "[WARN] Aucun GPU NVIDIA detecte, execution sur CPU multi-coeur avec quantisation."
fi

echo "[INFO] Lancement du daemon Ollama sur le port 11434..."
export OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_ORIGINS="http://127.0.0.1:8001,https://bantudevlab.africa"

# Lancement en arriere-plan
ollama serve &
sleep 5

echo "[INFO] Telechargement du modele de code souverain gemma:5b..."
ollama pull gemma:5b

echo "[INFO] Test d'inference locale..."
curl -s http://127.0.0.1:11434/api/generate -d '{
  "model": "gemma:5b",
  "prompt": "Explique brievement la cryptographie Zero-Knowledge Proof pour l Afrique de l Ouest.",
  "stream": false
}' | grep -o '"response":[^}]*' | head -n 1

echo "[SUCCESS] Moteur Gemma 5B operationnel et connecte a BantuDevLab."
