#!/usr/bin/env bash
# BantuDevLab - Sauvegarde Automatisee Souveraine de Gitea (T-ADM-703)
# Effectue un dump complet (BDD, depots Git, configurations) avec chiffrement GPG

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/backups/gitea}"
GITEA_CONF="${GITEA_CONF:-custom/conf/app.ini}"
GPG_RECIPIENT="${GPG_RECIPIENT:-backup@bantudevlab.africa}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="gitea-dump-${TIMESTAMP}.zip"
ENCRYPTED_ARCHIVE="${BACKUP_DIR}/${ARCHIVE_NAME}.gpg"

mkdir -p "${BACKUP_DIR}"

echo "[INFO] Demarrage de la sauvegarde Gitea dump..."
gitea dump --config "${GITEA_CONF}" --file "${BACKUP_DIR}/${ARCHIVE_NAME}"

if command -v gpg >/dev/null 2>&1; then
    echo "[INFO] Chiffrement GPG de l'archive..."
    gpg --batch --yes --encrypt --recipient "${GPG_RECIPIENT}" --output "${ENCRYPTED_ARCHIVE}" "${BACKUP_DIR}/${ARCHIVE_NAME}"
    rm -f "${BACKUP_DIR}/${ARCHIVE_NAME}"
    echo "[SUCCESS] Archive chiffree avec succes : ${ENCRYPTED_ARCHIVE}"
else
    echo "[WARN] GPG indisponible. L'archive reste au format zip."
fi

# Nettoyage des anciennes sauvegardes selon retention
find "${BACKUP_DIR}" -type f -name "gitea-dump-*.zip*" -mtime +"${RETENTION_DAYS}" -delete
echo "[INFO] Nettoyage de retention effectue."
