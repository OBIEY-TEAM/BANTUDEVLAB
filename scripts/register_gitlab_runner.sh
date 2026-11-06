#!/usr/bin/env bash
# Enregistrement officiel du GitLab Runner Souverain BANTUDEVLAB
set -euo pipefail

GITLAB_URL="${GITLAB_URL:-https://cybersocle.site}"
REGISTRATION_TOKEN="${REGISTRATION_TOKEN:-bantu_runner_registration_token_2026}"
RUNNER_NAME="bantu-sovereign-runner-abidjan"

echo "[INFO] Enregistrement du GitLab Runner sur ${GITLAB_URL}..."

gitlab-runner register \
  --non-interactive \
  --url "${GITLAB_URL}" \
  --registration-token "${REGISTRATION_TOKEN}" \
  --executor "docker" \
  --docker-image "python:3.12-slim" \
  --description "${RUNNER_NAME}" \
  --tag-list "sovereign,docker,python,systalink,sovereign-abidjan,sovereign-gpu-gemma,tier1-runner" \
  --run-untagged="true" \
  --locked="false" \
  --access-level="not_protected"

echo "[SUCCESS] GitLab Runner enregistre avec succes sous le nom ${RUNNER_NAME}"
