# Exploitation

## Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Oui (prod) | Clé secrète Django, longue et aléatoire |
| `DEBUG` | Non | `False` par défaut |
| `ALLOWED_HOSTS` | Oui (prod) | Hôtes séparés par des virgules |
| `CSRF_TRUSTED_ORIGINS` | Si HTTPS | Origines `https://...` de confiance |
| `SECURE_SSL_REDIRECT` | Non | `True` par défaut ; `False` derrière un proxy qui redirige déjà |
| `POSTGRES_PASSWORD` | Oui | Mot de passe de la base |
| `REDIS_PASSWORD` | Oui (Compose) | Mot de passe Redis |
| `GITEA_WEBHOOK_SECRET` | Oui | Secret HMAC des webhooks (sinon 503) |
| `GITEA_ADMIN_TOKEN` | Non | Jeton d'API Gitea |
| `GEMMA_API_URL`, `GEMMA_MODEL_NAME` | Non | Moteur IA local |

## Déploiement

```bash
cp .env.example .env     # remplir toutes les valeurs CHANGE_ME
docker compose up -d --build
docker compose ps        # tous les services doivent être "healthy"
docker compose exec django_app python manage.py check --deploy
```

Placez un reverse proxy TLS (Caddy, Nginx, Traefik) devant le port 8000 et transmettez `X-Forwarded-Proto`.

## Santé et supervision

- `/healthz` : processus vivant.
- `/readyz` : base de données et cache joignables (200, sinon 503).
- Journal d'audit : vérifier l'intégrité périodiquement :

```bash
docker compose exec django_app python manage.py shell -c "from apps.core.audit import AuditTrail; print(AuditTrail.verify_chain_integrity())"
```

## Sauvegarde et restauration PostgreSQL

```bash
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > backup-$(date +%F).sql.gz
gunzip -c backup-AAAA-MM-JJ.sql.gz | docker compose exec -T db psql -U "$POSTGRES_USER" "$POSTGRES_DB"
```

Testez la restauration régulièrement sur un environnement séparé.

## Rotation des secrets

1. Générer la nouvelle valeur (`python -c "import secrets; print(secrets.token_urlsafe(64))"`).
2. Mettre à jour `.env` (et le webhook côté Gitea pour `GITEA_WEBHOOK_SECRET`).
3. `docker compose up -d` pour recréer les services.
4. `DJANGO_SECRET_KEY` : invalide les sessions existantes (attendu).

## Runbook d'incident

| Symptôme | Vérifications | Action |
|---|---|---|
| `/readyz` renvoie 503 | `docker compose ps`, journaux `db` et `redis` | Redémarrer le service défaillant, restaurer si corruption |
| Pages lentes, Gitea down | `docker compose logs gitea` ; le circuit breaker se ferme seul après 30 s | Redémarrer Gitea |
| 429 sur les routes ZKP | Normal sous attaque ; consulter les journaux | Ajuster `DEFAULT_THROTTLE_RATES` si trafic légitime |
| Suspicion de compromission | Journal d'audit, tokens Git actifs | Faire tourner tous les secrets, désactiver les tokens, informer (SECURITY.md) |
| Chaîne d'audit invalide | `verify_chain_integrity()` retourne `False` | Isoler, comparer avec la dernière sauvegarde, ouvrir une enquête |
