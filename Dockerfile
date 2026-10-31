# Dockerfile multi-stage pour la surcouche souveraine BANTUDEVLAB
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code applicatif
COPY . /app/

# Port exposé
EXPOSE 8000

# Variable d'environnement pour le dimensionnement dynamique des workers
ENV WEB_CONCURRENCY=4

# Lancement haute performance via Gunicorn avec workers asynchrones Uvicorn (PERF-05)
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers ${WEB_CONCURRENCY:-4} --timeout 120 --access-logfile - --error-logfile -"]
