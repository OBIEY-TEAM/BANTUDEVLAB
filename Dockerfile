# Dockerfile multi-stage pour la surcouche souveraine BANTUDEVLAB
FROM python:3.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Installation des dependances systeme necessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation des dependances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Creation d'un utilisateur et groupe non-root pour le durcissement du conteneur
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/bash -m appuser

# Copie du code applicatif et attribution des permissions a appuser
COPY --chown=appuser:appgroup . /app/
RUN mkdir -p /app/staticfiles /app/forge_data/repos && \
    python manage.py collectstatic --no-input && \
    chown -R appuser:appgroup /app

# Bascule vers l'utilisateur non-root
USER appuser

# Ports exposes (8000 pour Django, 3001 pour Forge Server)
EXPOSE 8000 3001

# Variable d'environnement pour le dimensionnement dynamique des workers et repertoire temporaire
ENV WEB_CONCURRENCY=4 \
    XDG_RUNTIME_DIR=/tmp

# Lancement haute performance via Gunicorn avec workers asynchrones Uvicorn (PERF-05)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py init_sovereign_admin && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers ${WEB_CONCURRENCY:-4} --timeout 120 --worker-tmp-dir /tmp --no-control-socket --access-logfile - --error-logfile -"]
