#!/usr/bin/env bash
# Script de sauvegarde automatique quotidienne PostgreSQL BANTUDEVLAB
# Chiffrement AES-256 via GPG et archivage sur stockage objet souverain (Systalink S3)
set -euo pipefail

BACKUP_DIR="/var/backups/bantudevlab"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DUMP_FILE="${BACKUP_DIR}/bantudevlab_backup_${TIMESTAMP}.sql.gz"
ENC_FILE="${DUMP_FILE}.gpg"
RETENTION_DAYS=30

mkdir -p "${BACKUP_DIR}"

echo "[INFO] Debut du dump PostgreSQL..."
pg_dump -h "${POSTGRES_HOST:-db}" -U "${POSTGRES_USER:-bantudevlab_admin}" -d "${POSTGRES_DB:-bantudevlab}" | gzip -9 > "${DUMP_FILE}"

echo "[INFO] Chiffrement GPG de la sauvegarde..."
if [ -n "${GPG_RECIPIENT:-}" ]; then
    gpg --batch --yes --encrypt --recipient "${GPG_RECIPIENT}" --output "${ENC_FILE}" "${DUMP_FILE}"
    rm -f "${DUMP_FILE}"
else
    # Chiffrement symetrique avec cle d'archive
    gpg --batch --yes --symmetric --cipher-algo AES256 --passphrase "${BACKUP_ENCRYPTION_KEY:-sovereign_backup_secret_2026}" --output "${ENC_FILE}" "${DUMP_FILE}"
    rm -f "${DUMP_FILE}"
fi

echo "[INFO] Sauvegarde chiffree terminee : ${ENC_FILE}"

# Replicate to Sovereign S3 compatible object storage if configured
if command -v aws >/dev/null 2>&1 && [ -n "${S3_BACKUP_BUCKET:-}" ]; then
    echo "[INFO] Synchronisation vers le bucket S3 souverain..."
    aws s3 cp "${ENC_FILE}" "s3://${S3_BACKUP_BUCKET}/backups/${TIMESTAMP}/" --endpoint-url "${S3_ENDPOINT:-https://s3.systalink.africa}"
fi

# Clean backups older than retention policy
find "${BACKUP_DIR}" -type f -name "*.gpg" -mtime +"${RETENTION_DAYS}" -delete
echo "[SUCCESS] Rotation effectuee. Sauvegardes de plus de ${RETENTION_DAYS} jours supprimees."
