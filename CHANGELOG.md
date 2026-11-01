# Changelog

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) - versionnement sémantique.

## [Non publié] - préparation CADEV 2026

### Sécurité
- API : `IsAuthenticated` par défaut ; routes publiques déclarées explicitement ; `BasicAuthentication` retirée ; création d'organisations réservée aux administrateurs.
- Configuration : plus de secret par défaut (`DJANGO_SECRET_KEY`, webhook, mot de passe PostgreSQL), `DEBUG=False` par défaut, `ALLOWED_HOSTS` explicite.
- Production : HTTPS forcé, HSTS (preload), cookies `Secure`, `COOP`, limite de taille des requêtes.
- ZKP : consommation atomique des défis, défi obligatoire pour l'émission de tokens Git (correction d'un rejeu), validation stricte des paramètres (type, taille, `permissions`, `validity_days`), validation du `username` et du `country_code`, throttle d'inscription.
- Webhook Gitea : désactivé sans secret (503), limite de taille.
- Client Gitea : timeouts, redirections désactivées, validation `owner/repo`, circuit breaker.
- IA : limite de taille, throttle, masquage des secrets avant persistance, erreurs génériques en streaming.
- Audit : chaîne de hachage transactionnelle, vérification par lots.
- Docker : PostgreSQL et Redis non exposés (réseau interne), Redis protégé par mot de passe, `no-new-privileges`, `cap_drop: ALL`, healthchecks.
- Toasts : messages insérés via `textContent` (anti-XSS).

### Ajouté
- Icônes SVG auto-hébergées (`{% icon %}`, `{% flag %}`) en remplacement de tous les emojis ; contrôle `scripts/check_no_emoji.py`.
- Endpoints `/healthz` et `/readyz`.
- Pagination de la liste des organisations ; suppression d'un N+1.
- Documentation : README, SECURITY, CONTRIBUTING, architecture, modèle de menaces, spécification cryptographique, exploitation, pitch CADEV 2026.
- Tests de durcissement sécurité et des icônes.

### Modifié
- Pied de page : année 2026, accessibilité (focus visible, `prefers-reduced-motion`).
- `.env.example` : valeurs `CHANGE_ME`.

## [1.0.0] - 2025

- Forge souveraine initiale : Gitea, ZKP, scanner SARIF, assistant Gemma, tableau de bord, CI/CD (PR #1 à #8).
