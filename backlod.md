# BACKLOG BANTUDEVLAB — Plan d'amélioration avant la CADEV 2026

> Basé sur l'analyse de 14 commits / 8 PR (Initial → PR #8) et des fichiers : `config/settings.py`, `apps/{core,zkp_auth,gitea_client,security_scanner,ai_assistant}`, `templates/`, `static/css/style.css`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml`, `.env.example`, `finetuning/`, `tests/`.
> Priorités : **P0** bloquant / critique · **P1** important · **P2** souhaitable. Effort : S (<½ j) · M (1 j) · L (2-3 j).
> À réaliser **dans l'ordre** des phases (chaque phase débloque la suivante).

## Constats clés de l'audit

| # | Constat | Fichier(s) | Gravité |
|---|---|---|---|
| 1 | `SECRET_KEY` par défaut en dur, `DEBUG=True` et `ALLOWED_HOSTS=*` par défaut | `config/settings.py` | Critique |
| 2 | `DEFAULT_PERMISSION_CLASSES = AllowAny` : API ouvertes (création d'organisations, scan, IA, validation de tokens) sans authentification | `config/settings.py`, `apps/core/views.py` | Critique |
| 3 | Secret webhook et mot de passe PostgreSQL par défaut en dur (`sovereign_pass_2025`), identiques dans `.env.example` | `settings.py`, `.env.example` | Critique |
| 4 | CSP avec `'unsafe-inline'` + dépendance à `cdnjs.cloudflare.com` (contredit la souveraineté) ; pas de HSTS / `SECURE_SSL_REDIRECT` / cookies `Secure` | `settings.py`, `middleware.py` | Haute |
| 5 | ZKP : défi `get` + `save` non atomique (course possible), `int(...,16)` non protégé dans verify, `validity_days` non borné, `permissions` non validées, hash de seed sans KDF lent (Argon2/scrypt), pas de limite de taille d'entrée | `zkp_auth/*` | Haute |
| 6 | Enregistrement ZKP sans throttle ni anti-spam (création de comptes illimitée) ; pas de preuve de possession de la clé à l'inscription | `zkp_auth/views.py` | Haute |
| 7 | Endpoint IA : le code utilisateur est injecté dans le prompt (prompt injection), GET avec `code` en query string (fuite dans les logs, limite d'URL), erreurs internes renvoyées (`str(e)`), pas de limite de taille, pas de throttle | `ai_assistant/views.py`, `gemma.py` | Haute |
| 8 | Le scanner n'utilise que des regex ligne à ligne (faux positifs/négatifs) ; pas de limite de taille de fichier | `security_scanner/engine.py` | Moyenne |
| 9 | Requêtes Gitea synchrones ; `GiteaClient().list_repositories()` appelé dans les vues d'accueil/dashboard (latence + panne en cascade) ; pas de circuit breaker | `core/views.py`, `gitea_client/client.py` | Haute |
| 10 | `AuditTrail.record_event` lit le dernier enregistrement sans verrou → rupture de chaîne en concurrence ; `verify_chain_integrity` charge toute la table en mémoire | `core/audit.py` | Moyenne |
| 11 | Listes non paginées (organisations, audits) ; N+1 `org.repositories.count()` | `core/views.py` | Moyenne |
| 12 | Cache `cache_page` sur `metrics`, mais pas de fingerprinting/compression des statiques ; CSS monolithique (16 Ko) ; JS inline dans les templates (login 17 Ko) | `templates/`, `static/` | Moyenne |
| 13 | Beaucoup d'emojis utilisés comme icônes (`dashboard.html`, `home.html`, `metrics.html`, `login.html`, `base.html`) y compris drapeaux et statuts toast | templates | Design |
| 14 | Problèmes d'encodage (caractères corrompus, `\a` dans le footer `base.html`, `©` mal encodé, README avec caractères cassés) | `base.html`, `README.md`, `settings.py` | Moyenne |
| 15 | Accessibilité : pas de `aria-*`, contrastes non vérifiés, pas de mode réduit de mouvement, pas de navigation clavier testée | templates, CSS | Moyenne |
| 16 | CI : pas de scan de dépendances (pip-audit), pas de scan d'image (Trivy), pas de seuil de couverture, pas de CD ; `requirements.txt` non épinglé, outils de dev et prod mélangés | `ci.yml`, `requirements.txt` | Moyenne |
| 17 | Docker : ports Postgres/Redis exposés sur l'hôte, pas de healthcheck applicatif ni de limites de ressources, pas de reverse proxy TLS | `docker-compose.yml` | Haute |
| 18 | Documentation : README unique, pas de guide de contribution, d'architecture (ADR), de modèle de menace, de runbook ni de CHANGELOG ; tests nommés par « axes » plutôt que par module | racine, `tests/` | Moyenne |
| 19 | Données de repli (mock) Gitea/Gemma masquent les pannes et affichent « READY » statique ; score de souveraineté `98` par défaut factice | `client.py`, `ai_assistant/views.py`, `core/views.py` | Moyenne |
| 20 | Fine-tuning : dataset de 2,6 Ko seulement, évaluation minimale | `finetuning/` | Moyenne |

---

## PHASE 0 — Fondations & hygiène (1 j)

- [ ] **T-001 (P0, S)** Corriger l'encodage UTF-8 de tous les fichiers (README, templates, settings, commentaires) et le caractère `\a` du footer `base.html`; ajouter `.editorconfig` + `charset = utf-8`.
- [ ] **T-002 (P0, S)** Créer une branche `release/cadev-2026` et protéger `main` (revue obligatoire, CI verte).
- [ ] **T-003 (P1, S)** Scinder `requirements.txt` en `requirements/base.txt`, `dev.txt`, `prod.txt`; épingler les versions (pip-compile) et mettre à jour le Dockerfile/CI.
- [ ] **T-004 (P1, S)** Renommer les tests par module (`test_sec_axes.py` → `tests/security/…`) et regrouper avec des marqueurs pytest (`unit`, `e2e`, `security`, `perf`).
- [ ] **T-005 (P1, S)** Ajouter `pre-commit` (ruff, ruff-format, bandit, detect-secrets, end-of-file-fixer).

## PHASE 1 — Sécurité (P0 d'abord) (4-5 j)

### 1A. Configuration et secrets
- [ ] **T-010 (P0, S)** Supprimer toute valeur secrète par défaut (`SECRET_KEY`, `GITEA_WEBHOOK_SECRET`, `POSTGRES_PASSWORD`) : lever `ImproperlyConfigured` si absents quand `DEBUG=False`.
- [ ] **T-011 (P0, S)** `DEBUG=False` par défaut, `ALLOWED_HOSTS` explicite (fini `*`), `.env.example` avec placeholders `CHANGE_ME` et génération documentée (`python -c "import secrets…"`).
- [ ] **T-012 (P1, M)** Scinder les settings : `config/settings/{base,dev,prod,test}.py` (remplace le test `"test" in sys.argv`).
- [ ] **T-013 (P1, M)** Gestion des secrets : Docker secrets / Vault (cohérent avec le message du scanner « BantuDevLab Vault »).

### 1B. Authentification & autorisations
- [ ] **T-020 (P0, M)** Passer `DEFAULT_PERMISSION_CLASSES` à `IsAuthenticated` ; ouvrir explicitement uniquement : challenge, verify, register, health, home, login.
- [ ] **T-021 (P0, M)** Protéger `SovereignOrganizationListCreateView.post`, `ScannerView`, `GemmaCodeReviewView`, `GitTokenValidateView` (auth utilisateur ou token de service) + permissions par rôle (admin d'organisation).
- [ ] **T-022 (P0, S)** Retirer `BasicAuthentication` des classes d'authentification par défaut.
- [ ] **T-023 (P1, M)** Authentification par token Git : `permissions` restreintes à `read|write|admin`, `validity_days` borné (1–365), endpoint de **révocation** et de listage des tokens, limite de tokens par utilisateur.

### 1C. Protocole ZKP
- [ ] **T-030 (P0, S)** Rendre le consommation du défi **atomique** (`select_for_update` + `transaction.atomic`, ou `UPDATE … WHERE is_used=False`) pour supprimer la course au rejeu.
- [ ] **T-031 (P0, S)** Garder `int(public_key_y, 16)` et les paramètres hex (`try/except`, longueur maximale 600 caractères) dans `verify`, `register`, `GitTokenService`.
- [ ] **T-032 (P1, M)** Inscription : exiger une **preuve de possession** de la clé (Schnorr sur le nom d'utilisateur + nonce) + throttle `zkp_register` + validation du `username` (regex, longueur) et du `country_code` (liste ISO).
- [ ] **T-033 (P1, M)** Dérivation du seed : remplacer SHA-256 par scrypt/Argon2id avec sel ; documenter la phrase de 12 mots (BIP-39 ou liste vérifiée).
- [ ] **T-034 (P1, S)** Lier le défi à `username + expires_at + usage` dans le hash Fiat-Shamir (séparation de domaine) ; encodage canonique de longueur préfixée pour `hash_to_int`.
- [ ] **T-035 (P1, M)** Verrouillage progressif après N échecs (par IP et par utilisateur), durcir le throttle `zkp` (clé = IP+username) ; supprimer les challenges expirés (tâche Celery).
- [ ] **T-036 (P2, L)** Audit cryptographique externe / revue par un pair ; évaluer un passage à une courbe elliptique (Ristretto255 / secp256k1) pour réduire les temps de calcul.

### 1D. Entrées, en-têtes et transport
- [ ] **T-040 (P0, M)** CSP stricte : supprimer `'unsafe-inline'`, externaliser le JS/CSS inline (nonces ou fichiers statiques), héberger **localement** les icônes/polices (plus de `cdnjs`).
- [ ] **T-041 (P0, S)** Activer en production : `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`(+preload), `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_PROXY_SSL_HEADER`, `Permissions-Policy`, `Cross-Origin-Opener-Policy`.
- [ ] **T-042 (P1, S)** Remplacer `X-XSS-Protection` (obsolète) par la CSP ; ajouter `CSRF_TRUSTED_ORIGINS` ; cookies avec préfixe `__Host-`.
- [ ] **T-043 (P1, M)** Endpoint IA : POST uniquement (supprimer le GET avec `code` en query), limite de taille (ex. 20 Ko), throttle `ai`, nettoyage/échappement du contexte, délimiteurs anti prompt-injection, messages d'erreur génériques (ne plus renvoyer `str(e)`).
- [ ] **T-044 (P1, M)** Validation par **serializers DRF** pour toutes les entrées (organisations, scan, IA, tokens) + schéma OpenAPI associé.
- [ ] **T-045 (P1, S)** Webhook Gitea : vérifier la signature **avant** de parser le JSON, limiter la taille, ajouter une fenêtre anti-rejeu (header de livraison unique), journaliser les rejets.
- [ ] **T-046 (P1, S)** Client Gitea : `timeout` systématiques, `verify=True` configurable, interdire les redirections vers des hôtes non autorisés (SSRF), masquer le token dans les logs.

### 1E. Audit, données et chaîne d'approvisionnement
- [ ] **T-050 (P1, M)** `AuditTrail` : transaction + verrou (ou `UNIQUE(previous_hash)`) pour une chaîne cohérente en concurrence ; vérification de l'intégrité par lots (itérateur) ; commande `manage.py verify_audit_chain` et tâche planifiée.
- [ ] **T-051 (P1, S)** Ne pas stocker de code sensible dans `AIInteractionLog.prompt_snippet` : masquer secrets (réutiliser les regex du scanner) et fixer une rétention.
- [ ] **T-052 (P1, M)** CI : `pip-audit`, Trivy (image + dépôt), `gitleaks`, SBOM (CycloneDX), Dependabot/Renovate.
- [ ] **T-053 (P1, M)** Docker : ne plus publier PostgreSQL/Redis sur l'hôte, réseau interne, `read_only`, `cap_drop: ALL`, `no-new-privileges`, image figée par digest, Redis avec mot de passe.
- [ ] **T-054 (P1, M)** Moteur du scanner : ajouter règles Bandit/Semgrep (analyse AST), limite de taille/ nombre de fichiers, détection d'entropie des secrets, tests de ReDoS sur les regex.
- [ ] **T-055 (P2, M)** Authentification multi-appareils : rotation de clé et révocation d'identité (récupération du compte).
- [ ] **T-056 (P2, M)** Rédiger le **modèle de menace (STRIDE)** et un plan de réponse aux incidents (voir Phase 5).

## PHASE 2 — Performance & résilience (3 j)

- [ ] **T-060 (P0, M)** Sortir les appels Gitea des vues de rendu : mettre les dépôts en cache (stale-while-revalidate) via Celery beat, avec dégradation gracieuse affichée à l'utilisateur.
- [ ] **T-061 (P1, M)** Circuit breaker + retry exponentiel avec jitter pour Gitea et Gemma ; pool `requests.Session` partagé.
- [ ] **T-062 (P1, S)** Pagination DRF globale (`PageNumberPagination`, 20) et `annotate(Count("repositories"))` pour éliminer le N+1 ; `select_related`/`prefetch_related`.
- [ ] **T-063 (P1, S)** Index base de données : `AuditTrailLog(id, hash)`, `ZKPChallenge(user, challenge_nonce, is_used)`, `SecurityAuditReport(scanned_at)`, `GitAccessToken(token_hash)`.
- [ ] **T-064 (P1, M)** Statiques : `ManifestStaticFilesStorage`/WhiteNoise (compression + hash), CSS découpé (`base`, `components`, `pages`), minification, cache long.
- [ ] **T-065 (P1, S)** Cache : clés versionnées, invalidation à l'écriture, `Vary` correct ; `CONN_MAX_AGE`/pool de connexions PostgreSQL (psycopg3 pool).
- [ ] **T-066 (P1, M)** Streaming IA : annulation côté client, délai d'inactivité, file d'attente avec concurrence limitée (éviter la saturation du modèle local) ; mise en cache des revues identiques (hash du code).
- [ ] **T-067 (P1, M)** Scans : exécution via Celery avec suivi de progression (polling/SSE) et `task_id` ; résultats paginés.
- [ ] **T-068 (P2, M)** Benchmarks reproductibles (Locust/k6) : objectifs **p95 < 300 ms** sur pages, **< 150 ms** sur `challenge`, 200 req/s ; intégrer à la CI nocturne.
- [ ] **T-069 (P2, S)** Observabilité : `/healthz` + `/readyz`, logs JSON, métriques Prometheus (`django-prometheus`), Sentry auto-hébergé ; remplacer le « READY » statique de `GemmaStatusView` par un vrai ping.
- [ ] **T-070 (P2, S)** Supprimer les valeurs factices (`avg_sovereignty = 98` par défaut, mocks silencieux) ; afficher un état « Démo » explicite.

## PHASE 3 — Design, UX et accessibilité (4 j)

### 3A. Remplacement des emojis par de vraies icônes
- [ ] **T-080 (P0, S)** Choisir une bibliothèque SVG libre et **auto-hébergée** : *Lucide* (recommandé) ou Phosphor / Tabler. Pas de CDN (souveraineté + CSP).
- [ ] **T-081 (P0, M)** Créer un sprite SVG `static/icons/sprite.svg` + un template tag `{% icon "shield" size=20 %}` (`aria-hidden="true"` par défaut, `title` si l'icône porte du sens).
- [ ] **T-082 (P0, M)** Remplacer les emojis, fichier par fichier, selon la table :

| Emplacement | Actuel | Icône cible |
|---|---|---|
| `base.html` logo/nav | emoji | `landmark` / `layout-dashboard` |
| `home.html` — Moteur Git | emoji | `git-branch` |
| `home.html` — Auth ZKP | emoji | `key-round` / `shield-check` |
| `home.html` — IA Gemma | emoji | `bot` / `sparkles` |
| `home.html` — dépôts, étoiles, forks, niveau | emoji | `folder-git-2`, `star`, `git-fork`, `shield` |
| `dashboard.html` — Audit / Avis Gemma | emoji | `scan-search`, `message-square-code` |
| `dashboard.html` — aucune vulnérabilité | emoji | `circle-check` |
| `metrics.html` — latence, nœuds, localisation, ZKP, IA | emoji | `activity`, `server`, `map-pin`, `lock-keyhole`, `cpu` |
| `login.html` — étapes, régénérer, télécharger, enregistrer, prouver | emoji | `wand-sparkles`, `refresh-cw`, `download`, `save`, `fingerprint` |
| Toasts (`base.html`) succès / alerte / erreur | emoji | `circle-check`, `triangle-alert`, `circle-x` |
| Flèches « → » dans les boutons | caractère | `arrow-right` |

- [ ] **T-083 (P1, M)** **Drapeaux** (CIV, SEN, NGA, KEN, RWA) : les emojis de drapeaux ne s'affichent pas sous Windows → utiliser des SVG (`flag-icons`, auto-hébergé) dans `metrics.html` (JS `flag:`) et `login.html` (`<option>` : remplacer par un sélecteur personnalisé).
- [ ] **T-084 (P1, S)** Test automatisé : un script CI échoue si une plage d'emojis Unicode est détectée dans `templates/`, `static/` et `*.py` des vues (`scripts/check_no_emoji.py`).
- [ ] **T-085 (P1, S)** Faire de même pour le README et la documentation (badges SVG à la place des emojis).

### 3B. Système de design
- [ ] **T-090 (P1, M)** Formaliser des **design tokens** (CSS variables : couleurs, espacements, rayons, ombres, typographie) ; palette inspirée du panafricanisme (vert, or, rouge, noir) validée WCAG AA.
- [ ] **T-091 (P1, M)** Bibliothèque de composants (boutons, cartes, badges, toasts, tableaux, formulaires, modales, états vides, squelettes de chargement) + page `/design-system/` (visible en dev).
- [ ] **T-092 (P1, M)** Polices auto-hébergées (Inter / Sora) en `woff2` avec `font-display: swap`.
- [ ] **T-093 (P1, M)** Refonte de `login.html` : assistant 3 étapes sans JS inline, barre de progression, états d'erreur lisibles, copie sécurisée de la phrase de 12 mots, avertissement de sauvegarde obligatoire.
- [ ] **T-094 (P1, M)** Dashboard : graphiques (score de souveraineté, sévérités), tableaux triables/paginés, squelettes de chargement, état vide soigné ; stream IA avec rendu Markdown assaini.
- [ ] **T-095 (P2, M)** Mode clair/sombre (`prefers-color-scheme`) + bascule persistante.
- [ ] **T-096 (P2, M)** Internationalisation FR / EN (+ Swahili/Portugais en option) via `gettext` ; `LANGUAGE_CODE` configurable.
- [ ] **T-097 (P2, S)** Favicon, `manifest.webmanifest`, balises Open Graph, page 404/500 personnalisées.

### 3C. Accessibilité (WCAG 2.2 AA)
- [ ] **T-100 (P1, M)** Rôles/ARIA, `aria-live` pour les toasts et le flux IA, `label` associés, focus visible, lien « Aller au contenu », navigation clavier complète.
- [ ] **T-101 (P1, S)** Respect de `prefers-reduced-motion` ; contrastes ≥ 4,5:1 ; cibles tactiles ≥ 44 px ; design responsive mobile-first (testé à 360 px).
- [ ] **T-102 (P1, S)** Audit automatisé : axe-core via Playwright + Lighthouse CI (objectifs : Accessibilité ≥ 95, Performance ≥ 90, Best Practices ≥ 95).

## PHASE 4 — Qualité, tests et CI/CD (3 j)

- [ ] **T-110 (P1, M)** Couverture minimale 85 % imposée en CI (`--cov-fail-under=85`), badge dans le README.
- [ ] **T-111 (P1, M)** Tests de sécurité manquants : accès non authentifié (401/403) sur chaque route, rejeu concurrent du défi, SSRF, prompt injection, payloads surdimensionnés, headers de production.
- [ ] **T-112 (P1, M)** Tests e2e Playwright : parcours complet inscription → connexion → scan → revue IA, captures d'écran en CI, vérification des icônes SVG (aucun emoji).
- [ ] **T-113 (P1, S)** Fuzzing étendu (Hypothesis) du ZKP et du scanner (ReDoS) ; tests de propriété sur `AuditTrail`.
- [ ] **T-114 (P1, M)** Pipeline CD : build image signée (cosign), publication GHCR, déploiement de préproduction automatique, rollback.
- [ ] **T-115 (P1, S)** Healthchecks Docker de l'application, du worker Celery et de Gitea ; `depends_on: condition: service_healthy`.
- [ ] **T-116 (P2, M)** Migrations : vérifier `makemigrations --check` en CI ; stratégie de sauvegarde/restauration PostgreSQL (script + test).
- [ ] **T-117 (P2, M)** Fine-tuning Gemma : étendre le dataset (> 1 000 exemples validés, sources africaines : OHADA, RGPD africain/Convention de Malabo), métriques d'évaluation chiffrées, version du modèle publiée avec sa carte.

## PHASE 5 — Documentation (3 j)

- [ ] **T-120 (P0, M)** Réécrire `README.md` (UTF-8, sans emojis) : proposition de valeur, captures d'écran, démarrage en 5 minutes, schéma d'architecture, badges (CI, couverture, licence).
- [ ] **T-121 (P1, M)** `docs/architecture.md` (C4 : contexte, conteneurs, composants) + diagrammes Mermaid + ADR (`docs/adr/0001-gitea-hybride.md`, `0002-zkp-schnorr.md`, `0003-gemma-local.md`).
- [ ] **T-122 (P1, M)** `docs/security/threat-model.md` (STRIDE), `SECURITY.md` (divulgation responsable), `docs/security/crypto-spec.md` (spécification précise du protocole ZKP, paramètres, limites).
- [ ] **T-123 (P1, S)** `docs/api.md` + publication de l'OpenAPI (drf-spectacular) avec exemples cURL et codes d'erreur.
- [ ] **T-124 (P1, S)** `docs/operations/` : déploiement, variables d'environnement, sauvegardes, supervision, runbook d'incident, rotation des secrets.
- [ ] **T-125 (P1, S)** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, modèles d'issues/PR, `CHANGELOG.md` (Keep a Changelog), choix et fichier `LICENSE`.
- [ ] **T-126 (P2, M)** Guide utilisateur : tutoriels pas à pas (créer l'identité, pousser du code avec un token Git, lancer un audit) en FR/EN, avec captures.
- [ ] **T-127 (P2, S)** Documentation de la souveraineté : cartographie des données, juridictions, conformité (Convention de Malabo, lois nationales de protection des données).

## PHASE 6 — Pitch professionnel de 10 minutes pour la CADEV 2026 (3 j, en parallèle de la phase 5)

> Pré-requis : phases 1 (P0) et 3A terminées, démonstration stable.

- [ ] **T-130 (P0, S)** Définir l'audience, l'objectif (financement, partenariat, adoption), le message unique : « Le code de l'Afrique, hébergé, sécurisé et assisté en Afrique ».
- [ ] **T-131 (P0, M)** Rédiger le script minuté (voir trame) et un **diaporama de 12 diapositives maximum** (sans emojis, icônes SVG cohérentes).
- [ ] **T-132 (P0, M)** Préparer une **démo en direct de 3 min** + **vidéo de secours** (screencast 3 min) + environnement offline pré-chargé (jeu de données de démonstration `manage.py seed_demo`).
- [ ] **T-133 (P1, S)** Chiffres de preuve : couverture de tests, p95, nombre de règles du scanner, score de souveraineté, coût comparé à GitHub/GitLab SaaS (à documenter avec sources).
- [ ] **T-134 (P1, S)** Fiche « one-pager » PDF + QR code vers la démo/dépôt ; kit presse (logo, visuels).
- [ ] **T-135 (P1, S)** Préparer 10 questions/réponses probables (sécurité ZKP, modèle économique, concurrence, licence Gitea, hébergement, conformité, scalabilité, gouvernance).
- [ ] **T-136 (P1, S)** Trois répétitions chronométrées (dont une devant un public externe) ; ajuster pour **9 min 30** maximum.
- [ ] **T-137 (P2, S)** Check-list jour J : adaptateurs HDMI, secours hors ligne, 2 copies du diaporama (PDF + PPTX), horaire et salle confirmés.

### Trame du pitch (10 minutes)

| Temps | Section | Contenu | Support visuel |
|---|---|---|---|
| 0:00–0:45 | Accroche | Histoire d'un développeur africain dont le code dépend de plateformes étrangères ; chiffre-choc sur la dépendance | Diapo 1–2 |
| 0:45–1:45 | Problème | Dépendance, risques juridiques, latence, coût en devises, vol de propriété intellectuelle | Diapo 3 |
| 1:45–2:45 | Solution | BANTUDEVLAB : forge souveraine = Gitea + surcouche Django + ZKP + scanner + IA locale | Diapo 4–5 (architecture) |
| 2:45–6:00 | Démo live (3 min 15) | 1) Inscription ZKP sans mot de passe 2) Push avec token Git 3) Audit de sécurité d'un dépôt 4) Revue IA Gemma en streaming 5) Tableau de bord de souveraineté | Application + vidéo de secours |
| 6:00–7:00 | Technologie & sécurité | Preuve à divulgation nulle, chaîne d'audit inviolable, CSP stricte, tests, CI/CD | Diapo 6–7 |
| 7:00–8:00 | Marché & impact | Développeurs, banques, ministères, universités ; cas d'usage par pays | Diapo 8 |
| 8:00–8:45 | Modèle économique & feuille de route | Hébergement souverain, support, formation ; jalons 2026-2027 | Diapo 9–10 |
| 8:45–9:30 | Équipe & traction | Équipe OBIEY-TEAM, partenaires (Systalink Cloud), chiffres | Diapo 11 |
| 9:30–10:00 | Appel à l'action | Pilotes avec 3 institutions, partenaires d'hébergement, financement ; QR code | Diapo 12 |

## PHASE 7 — Clôture et livraison (1 j)

- [ ] **T-140 (P0, S)** Revue finale : exécuter la suite complète (`pytest`, `ruff`, `bandit`, `pip-audit`, Lighthouse, axe) et corriger les régressions.
- [ ] **T-141 (P0, S)** Geler `release/cadev-2026` (tag `v1.0.0-cadev`), publier le CHANGELOG et l'image Docker signée.
- [ ] **T-142 (P1, S)** Déploiement de préproduction sur Systalink Cloud (TLS, domaine, sauvegardes) et test de charge final.
- [ ] **T-143 (P1, S)** Rétrospective et classement des tâches P2 restantes dans le backlog post-CADEV.

---

## Récapitulatif de l'ordre d'exécution

1. **Phase 0** → hygiène (T-001 à T-005)
2. **Phase 1** → sécurité P0 (T-010, 011, 020–022, 030, 031, 040, 041) puis P1/P2
3. **Phase 2** → performance (T-060 en premier)
4. **Phase 3** → icônes (T-080 à T-085) puis design system et accessibilité
5. **Phase 4** → tests/CI/CD pour verrouiller les acquis
6. **Phase 5 et 6** → documentation et pitch (en parallèle)
7. **Phase 7** → gel, déploiement, rétrospective

## Critères d'acceptation globaux (Definition of Done CADEV 2026)

- Aucune route sensible accessible sans authentification ; aucun secret par défaut en production.
- `bandit`, `pip-audit`, Trivy et gitleaks sans alerte haute/critique.
- Aucun emoji dans l'interface ; icônes SVG auto-hébergées ; aucune ressource tierce (CDN).
- Lighthouse : Performance ≥ 90, Accessibilité ≥ 95, Best Practices ≥ 95.
- Couverture ≥ 85 % ; e2e Playwright verts.
- Documentation complète (README, architecture, sécurité, API, opérations, contribution).
- Pitch de 10 minutes répété 3 fois, démo live + vidéo de secours prêtes.
