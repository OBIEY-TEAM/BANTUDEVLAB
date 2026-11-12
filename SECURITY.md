# Politique de sécurité

## Versions supportées

| Version | Support sécurité |
|---|---|
| `main` / `release/cadev-2026` | Oui |
| Autres branches | Non |

## Signaler une vulnérabilité

**Ne créez pas d'issue publique.** Écrivez à `security@bantudevlab.africa` avec :

- une description et l'impact estimé ;
- les étapes de reproduction (requêtes, payloads, version) ;
- si possible, une suggestion de correctif.

Engagements : accusé de réception sous 72 h, évaluation sous 7 jours, correctif ou plan de remédiation sous 30 jours pour les failles critiques ou hautes. Nous créditons les rapporteurs qui le souhaitent.

## Périmètre

Dans le périmètre : API Django (`/api/*`), authentification ZKP, émission de tokens Git, webhook Gitea, scanner, assistant IA, configuration Docker.
Hors périmètre : déni de service volumétrique, ingénierie sociale, vulnérabilités de composants tiers déjà publiques sans exploit propre à ce projet (signalez-les en amont).

## Mesures en place

Voir le [README](README.md#sécurité), le [modèle de menaces](docs/security/threat-model.md) et la [spécification cryptographique](docs/security/crypto-spec.md).

## Pour les opérateurs

- Ne jamais déployer avec `DEBUG=True`.
- Générer des secrets uniques (`DJANGO_SECRET_KEY`, `GITEA_WEBHOOK_SECRET`, `POSTGRES_PASSWORD`, `REDIS_PASSWORD`) et les faire tourner régulièrement.
- Terminer TLS devant l'application (reverse proxy) et conserver `SECURE_SSL_REDIRECT=True`.
- Exécuter `python manage.py check --deploy` avant chaque mise en production.
