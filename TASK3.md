# TASK3.md — BANTUDEVLAB : Plan de Transition en Production Industrielle & Plateforme Panafricaine de Collaboration Développeurs avec Intégration GitLab

Ce document constitue le référentiel d'ingénierie exhaustif pour **sortir définitivement du mode démonstration** et opérer **BANTUDEVLAB** en environnement de production souverain (Datacenters Tier-3 Abidjan, Dakar, Nairobi, Kigali).

L'objectif central est de délivrer une **plateforme complète de collaboration pour les développeurs africains**, intégrant nativement la puissance du moteur **GitLab CE/EE**, tout en conservant l'ADN souverain et la touche personnelle existante de BantuDevLab :
1. **Authentification Zero-Trust sans mot de passe par preuve à divulgation nulle de connaissance (ZKP Schnorr)**.
2. **Scanner de sécurité SAST & Score de souveraineté panafricain (SARIF 2.1.0)**.
3. **Assistant d'ingénierie et de revue de code IA local (Gemma 5B fine-tuné sur les cadres légaux africains)**.
4. **Interface utilisateur vectorielle 100% SVG native, sans aucun CDN tiers ni emoji**.
5. **Chaîne d'audit immuable SHA-256 conforme à la Convention de Malabo sur la cybersécurité**.

---

## 1. Analyse Exhaustive de Chaque Fichier du Projet : État Démo vs Cible Production

L'audit complet du référentiel met en lumière les écarts entre les comportements de simulation/démo et les exigences d'une plateforme de production à haute disponibilité :

### 1.1 Architecture Applicative Backend (`apps/`)

| Fichier / Module | État Démo Résiduel | Transition Requise pour la Production Industrielle |
|---|---|---|
| `apps/core/models.py` | Modèles `SovereignOrganization` et `AuditTrailLog`. Audit trail dépendant du dernier enregistrement sans verrou de transaction en écriture concurrente. | Mettre en place un verrouillage transactionnel strict (`select_for_update`) ou contrainte d'unicité `UNIQUE(previous_hash)` pour garantir l'intégrité de la chaîne cryptographique sous forte concurrence. |
| `apps/core/views.py` | `avg_sovereignty = 98` calculé avec valeur de secours par défaut en l'absence de scans réels. Requêtes directes de listing vers Gitea/GitLab pouvant bloquer le thread de rendu. | Découpler complètement le rendu HTML des appels API distants. Servir les données de projets et de dépôts exclusivement via le cache Redis (`stale-while-revalidate`), synchronisé par des workers Celery périodiques. |
| `apps/core/audit.py` | La méthode `verify_chain_integrity` itère sur l'ensemble de la table en mémoire sans pagination ni curseur. | Implémenter un itérateur par batchs (curseurs `iterator(chunk_size=1000)`) et déporter la vérification d'intégrité dans une tâche Celery planifiée (`verify_audit_chain_task`). |
| `apps/core/middleware.py` | En-têtes de sécurité de base configurés mais directives CSP tolérant des éléments de test. | Verrouiller la CSP en `Content-Security-Policy` stricte sans `'unsafe-inline'` avec hashes SRI / nonces cryptographiques générés par requête. |
| `apps/core/templatetags/icons.py` | Rendu SVG auto-hébergé sans aucun emoji externe (conforme). | Ajouter la mise en cache locale des symboles SVG et supporter les badges dynamiques de statut de pipeline GitLab CI. |
| `apps/zkp_auth/crypto.py` | Groupe RFC 3526 MODP 2048 bits avec génération de clé Schnorr et Fiat-Shamir. Les opérations `pow(g, x, p)` sont exécutées en pur Python sur le thread CPU. | Intégrer une extension C/Rust ou bibliothèque optimisée (`gmpy2`/`cryptography`) pour accélérer l'arithmétique modulaire grand entier et résister aux attaques par canaux auxiliaires (timing attacks). |
| `apps/zkp_auth/models.py` | `ZKPChallenge` et `SovereignIdentity`. Nettoyage des nonces expirés déclenché manuellement. | Automatiser la purge des challenges non consommés après 5 minutes via Celery Beat pour éviter la saturation de la base de données. |
| `apps/zkp_auth/tokens.py` | `GitTokenService` générant des tokens préfixés `bnt_` hachés en SHA-256. | Ajouter la rotation obligatoire des jetons de service, la restriction d'adresses IP autorisées (IP pinning) et le support des scopes granulaires GitLab (`api`, `read_repository`, `write_repository`). |
| `apps/zkp_auth/views.py` | Gestion d'authentification ZKP avec endpoints de challenge, vérification et tokens. | Implémenter un rate-limiting dynamique (Redis Leaky Bucket) par adresse IP et empreinte de clé pour immuniser l'API contre les attaques de déni de service distribuées. |
| `apps/security_scanner/engine.py` | Scanner SAST regex détectant secrets et appels risqués (`eval`, `exec`). | Compléter les règles par analyse syntaxique AST (`tree-sitter` / `ast`), analyse d'entropie Shannon pour la détection de tokens masqués et validation des licences logicielles souveraines. |
| `apps/security_scanner/tasks.py` | Tâche Celery asynchrone `async_scan_code`. | Connecter la tâche aux hooks de pre-receive et post-commit de GitLab pour bloquer automatiquement tout commit contenant des clés privées non chiffrées (Sovereignty Security Gate). |
| `apps/security_scanner/serializers.py` | Format SARIF 2.1.0 OASIS standardisé. | Assurer l'intégration bidirectionnelle avec le panneau de sécurité GitLab Security Dashboard via l'ingestion d'artefacts `gl-sast-report.json`. |
| `apps/ai_assistant/gemma.py` | Mock de repli local si Ollama/vLLM n'est pas joignable. | Déployer le cluster d'inférence GPU vLLM avec modèle Gemma 5B 4-bit GGUF, réplication de workers et gestionnaire de file d'attente prioritaire pour les revues de code critiques. |
| `apps/ai_assistant/views.py` | Streaming SSE de la revue de code. | Ajouter une validation de taille maximale de diff (max 500 Ko) et un filtre d'anonymisation PII pour éliminer toute fuite de données nominatives dans le prompt d'inférence. |
| `apps/gitlab_client/client.py` | Client Python GitLab v4 officiel avec fallback HTTP. | Ajouter un pool de connexions persistant, un circuit breaker résilient (seuil d'échec 5 requêtes, timeout 30s) et le support complet des Merge Requests et commentaires en ligne. |
| `apps/gitlab_client/views.py` | Récepteur de webhook avec validation de signature `X-Gitlab-Token`. | Déclencher l'analyse différentielle complète, poster un commentaire enrichi directement sur la Merge Request GitLab et notifier les relecteurs assignés. |
| `apps/gitea_client/` | Client et synchroniseur bidirectionnel Gitea v1. | Maintenir le pont de compatibilité pour les dépôts existants tout en assurant la migration transparente des projets vers le cluster GitLab unifié. |

### 1.2 Configuration et Infrastructure (`config/`, `deploy/`, `gitlab/`)

| Fichier / Module | État Démo Résiduel | Transition Requise pour la Production Industrielle |
|---|---|---|
| `config/settings.py` | Clé secrète de secours activée en mode test (`TESTING = True`). | Forcer l'arrêt immédiat au démarrage (`django.core.exceptions.ImproperlyConfigured`) si `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD` ou `REDIS_PASSWORD` ne sont pas définis avec une entropie suffisante (>256 bits). |
| `Dockerfile` | Image multi-stage avec non-root user `appuser:1000`. | Activer le verrouillage en lecture seule du système de fichiers racine (`read_only: true`), configurer un cache de dépendances pip interne et signer cryptographiquement l'image avec Sigstore/Cosign. |
| `docker-compose.yml` | Ports exposés directement sur la machine hôte en local (3000, 2222, 8000). | Supprimer l'exposition des ports internes de bases de données et de cache. Faire transiter tout le trafic entrant via le reverse-proxy Nginx avec terminaison TLS 1.3. |
| `gitlab/config/gitlab.rb` | URL configurée sur `http://localhost:3001` avec provider OmniAuth ZKP pointant sur `http://127.0.0.1:8001`. | Basculer sur les domaines de production réels (`git.bantudevlab.africa` et `auth.bantudevlab.africa`) avec certificats Let's Encrypt / PKI souveraine, SSL strict et PostgreSQL distant avec PgBouncer. |
| `gitlab/lib/gitlab/auth/bantu_zkp.rb` | Stratégie OmniAuth Ruby interagissant avec l'API Bantu ZKP. | Ajouter la validation mutuelle TLS (mTLS) entre le nœud GitLab et le micro-service d'authentification BantuDevLab. |
| `gitlab/lib/gitlab/security/sovereignty_scanner.rb` | Blocage conditionnel des commits si le score est inférieur à 70. | Intégrer les exceptions approuvées par les responsables de sécurité des organisations africaines avec double validation ZKP. |
| `gitlab/lib/gitlab/ci/gemma_review_service.rb` | Publication automatique de notes sur les Merge Requests. | Formater les retours avec suggestions applicables en un clic (`GitLab Suggestion Blocks`) pour corriger immédiatement les failles. |
| `deploy/nginx/bantudevlab.conf` | Configuration de reverse proxy Nginx HTTP/2 et TLS 1.3. | Activer les en-têtes HSTS avec preload, la compression gzip/brotli, le rate-limiting Nginx par zone IP et le tamponnage des flux SSE. |
| `deploy/pgbouncer/pgbouncer.ini` | Limite de pool transactionnel à 100 connexions. | Calibrer le dimensionnement du pool pour absorber jusqu'à 500 connexions concurrentes réparties sur les nœuds régionaux. |
| `deploy/monitoring/prometheus.yml` & `loki-config.yml` | Exportateurs configurés pour Postgres, Redis et Django. | Configurer des alertes Prometheus (Alertmanager) par SMS/Webhook sécurisé en cas d'anomalie cryptographique ou de tentative de force brute. |
| `forge_server.py` | Serveur mock HTTP simulant les protocoles Git et l'API GitLab v4 pour les tests locaux hors conteneurs. | Conserver uniquement pour les bancs de tests CI et basculer l'infrastructure de production sur le véritable moteur GitLab CE Omnibus. |

---

## 2. Objectif Central : Plateforme de Collaboration Panafricaine des Développeurs

BANTUDEVLAB a pour vocation de devenir le **GitHub/GitLab souverain du continent africain**, conçu pour les banques centrales, ministères, agences de sécurité, universités et startups tech régionales.

```
+----------------------------------------------------------------------------------------------------+
|                                    BANTUDEVLAB SOVEREIGN FORGE                                     |
|                                                                                                    |
|  [ Interface Panafricaine ]       [ Authentification ZKP ]         [ Revue IA Locale Gemma 5B ]    |
|   - Design System Neutre           - Clé publique uniquement        - Inférence GPU dédiée         |
|   - 100% SVG natif sans emoji      - Preuve Schnorr NIZKP           - Détection de failles         |
|   - Multilingue (FR, EN, SW, PT)   - Zéro mot de passe stocké       - Recommandations souveraines  |
|          |                                   |                                   |                 |
|          +-----------------------------------+-----------------------------------+                 |
|                                              |                                                     |
|                                              v                                                     |
|                         +-----------------------------------------+                                |
|                         |      PASSERELLE D'INTÉGRATION GITLAB    |                                |
|                         |    (OmniAuth ZKP + Webhooks Signés)     |                                |
|                         +-----------------------------------------+                                |
|                                              |                                                     |
|                 +----------------------------+----------------------------+                        |
|                 v                                                         v                        |
|  +------------------------------+                          +------------------------------+        |
|  |       MOTEUR GITLAB CE       |                          |    SURCOUCHE BANTUDEVLAB     |        |
|  | - Gestion des Merge Requests |                          | - Scanner de Souveraineté    |        |
|  | - Discussions & Code Review  |                          | - Score Panafricain (SARIF)  |        |
|  | - GitLab CI/CD Runners       |                          | - Registre Multi-Tenancy     |        |
|  | - Issues, Milestones, Wikis  |                          | - Chaîne d'Audit Malabo      |        |
|  +------------------------------+                          +------------------------------+        |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Matrice Opérationnelle des Tâches de Développement, Sécurité, Docker & Tests

### Axe 1 : Développement Collaboratif & Espaces Développeurs (DEV-COL)

- [ ] **T-COL-101 : Portail Collaboratif Unifié Développeur**
  - Fusionner dans le tableau de bord BantuDevLab la vue unifiée des projets, Merge Requests assignées, revues de code en attente et issues ouvertes issues de GitLab.
  - Offrir une navigation contextuelle fluide entre l'interface web de BantuDevLab et les espaces de travail GitLab.
- [ ] **T-COL-102 : Système de Merge Requests Souveraines avec Double Approbation ZKP**
  - Implémenter le workflow d'approbation cryptographique des Merge Requests : un relecteur ne signe pas par un simple clic, mais génère une signature ZKP prouvant son habilitation sans exposer sa clé privée.
  - Bloquer la fusion (`merge`) si le quorum de signatures souveraines n'est pas atteint.
- [ ] **T-COL-103 : Discussions en Ligne et Suggestions de Code Assistées par Gemma 5B**
  - Connecter l'assistant IA local Gemma 5B aux commentaires de revues de code de GitLab via le service `gitlab/lib/gitlab/ci/gemma_review_service.rb`.
  - Fournir des blocs de suggestion directement fusionnables en un clic pour corriger les non-conformités détectées.
- [ ] **T-COL-104 : Gestion Multi-Tenancy des Organisations et Équipes Régionales**
  - Étendre le modèle `SovereignOrganization` pour synchroniser automatiquement les Groupes et Sous-groupes GitLab (`GitLab Groups & Namespaces`).
  - Permettre l'isolation stricte des projets entre entités souveraines (ministères, banques, universités).

### Axe 2 : Sécurité Industrielle, Zero-Trust & Conformité Panafricaine (SEC-PROD)

- [ ] **T-SEC-201 : Gestion Centralisée des Secrets (BantuDevLab Vault / KMS)**
  - Supprimer tout fichier d'environnement contenant des valeurs secrètes sur les nœuds de production.
  - Intégrer un coffre-fort numérique souverain (HashiCorp Vault auto-hébergé ou service KMS HSM sur site) pour injecter dynamiquement `DJANGO_SECRET_KEY`, les clés de signature Webhook et les credentials de base de données.
- [ ] **T-SEC-202 : Durcissement Cryptographique ZKP & Résistance aux Attaques Temporelles**
  - Valider l'intégrité de toutes les conversions hexadécimales avec limitation stricte de taille (max 512 octets) pour éviter les attaques DoS mémoire.
  - Implémenter des calculs modulaires à temps constant pour éliminer tout risque d'attaque par canal auxiliaire sur les clés privées des développeurs.
- [ ] **T-SEC-203 : Conformité Légale Panafricaine & Convention de Malabo**
  - Conserver les journaux d'audit cryptographiques (`AuditTrailLog`) pendant une durée minimale de 1 an dans un stockage WORM (Write Once, Read Many).
  - Fournir une commande d'audit légal `python manage.py export_malabo_compliance_report` certifiant la conformité du code et de l'hébergement aux normes de souveraineté africaine.
- [ ] **T-SEC-204 : Durcissement des Politiques de Sécurité Web (CSP Niveau 3 & HSTS Preload)**
  - Configurer une politique CSP stricte sans `'unsafe-inline'` ni `'unsafe-eval'`.
  - Forcer HSTS avec `max-age=63072000; includeSubDomains; preload` et restreindre les cookies de session avec l'attribut `SameSite=Strict; Secure`.

### Axe 3 : Intégration GitLab & Hybridation de la Forge (GITLAB-INT)

- [ ] **T-GIT-301 : Authentification Unique OmniAuth Bantu ZKP sur GitLab CE**
  - Finaliser l'intégration de la stratégie `Gitlab::Auth::BantuZkp` dans `gitlab/config/gitlab.rb` pour permettre la connexion instantanée à GitLab sans aucun mot de passe, via le wizard ZKP existant.
  - Mapper automatiquement les rôles et appartenances d'organisations lors du premier provisionnement d'utilisateur.
- [ ] **T-GIT-302 : Enregistrement et Isolation des GitLab CI/CD Runners Panafricains**
  - Déployer des GitLab Runners conteneurisés en environnement sécurisé (Docker-in-Docker avec isolation gVisor ou microVM Firecracker).
  - Associer des tags souverains (`sovereign-abidjan`, `sovereign-gpu-gemma`, `tier1-runner`) pour garantir que les builds ne quittent jamais le sol africain.
- [ ] **T-GIT-303 : Webhooks Bidirectionnels Sécurisés à Haute Disponibilité**
  - Développer un mécanisme de retry asynchrone avec backoff exponentiel pour la transmission des événements de push, merge request et pipeline de GitLab vers BantuDevLab.
  - Valider cryptographiquement l'en-tête `X-Gitlab-Token` avec rotation dynamique des secrets.
- [ ] **T-GIT-304 : Intégration du Scanner SAST dans la GitLab Security Tab (SARIF Ingestion)**
  - Publier les rapports du scanner de souveraineté sous forme d'artefacts compatibles avec la spécification GitLab SAST (`gl-sast-report.json`).
  - Bloquer automatiquement le merge si une vulnérabilité critique ou une violation de souveraineté est détectée.

### Axe 4 : Conteneurisation Docker & Infrastructure de Production (DOCKER-PROD)

- [ ] **T-DOC-401 : Déploiement du Cluster GitLab CE Omnibus Durci via Docker**
  - Rédiger la composition de production `docker-compose.production.yml` incluant le service officiel GitLab CE (`gitlab/gitlab-ce:16.11-ce.0`), configuré avec les paramètres de souveraineté de `gitlab/config/gitlab.rb`.
  - Configurer les volumes persistants avec chiffrement LUKS au repos.
- [ ] **T-DOC-402 : Sécurité Rootless & Minimisation de la Surface d'Attaque des Conteneurs**
  - Configurer tous les conteneurs avec `security_opt: [no-new-privileges:true]`, `cap_drop: [ALL]` et `read_only: true` avec répertoires `/tmp` montés en `tmpfs`.
  - Séparer strictement les réseaux : `frontend_net` (Nginx), `app_net` (Django, GitLab) et `backend_net` (Postgres, Redis, sans accès sortant).
- [ ] **T-DOC-403 : Pooler de Connexions PgBouncer et Clustering Redis**
  - Déployer PgBouncer en mode transaction pour mutualiser les connexions de Django et GitLab vers la base PostgreSQL 16.
  - Déployer Redis en mode Sentinel ou Cluster avec mot de passe robuste et persistance AOF activée.
- [ ] **T-DOC-404 : Automatisation des Sauvegardes Chiffrées et Plan de Reprise d'Activité (PRA)**
  - Industrialiser le script `scripts/backup_database.sh` avec chiffrement asymétrique GPG des dumps PostgreSQL et des dépôts Git.
  - Synchroniser les sauvegardes chiffrées vers deux datacenters africains distincts (Abidjan et Kigali) pour une reprise d'activité en moins de 15 minutes.

### Axe 5 : Tests Supplémentaires, Fuzzing & Qualification Industrielle (QA-TESTS)

- [ ] **T-TST-501 : Suite Complète de Tests d'Intégration GitLab v4**
  - Consolider la suite `tests/test_gitlab_client.py` en ajoutant des simulations de pannes réseau, de timeouts de webhook et de synchronisations de branches volumineuses.
  - Valider l'interopérabilité complète des API entre le frontal BantuDevLab et le backend GitLab.
- [ ] **T-TST-502 : Fuzzing Cryptographique & Tests de Résilience Mathématique**
  - Étendre `tests/test_zkp_fuzzing.py` avec des générateurs Hypothesis produisant des nonces malformés, des clés hors limites modulaires et des preuves forgées pour garantir le rejet absolu de toute tentative d'usurpation.
- [ ] **T-TST-503 : Tests End-to-End (E2E) Playwright du Workflow Collaboratif**
  - Enrichir `tests/test_e2e_playwright.py` avec le parcours complet du développeur :
    1. Inscription ZKP et sauvegarde du trousseau.
    2. Création d'une organisation souveraine et d'un projet.
    3. Push de code via le token Git émis.
    4. Déclenchement automatique de la revue Gemma 5B et de l'audit de sécurité.
    5. Validation visuelle de l'interface en thème clair et sombre.
- [ ] **T-TST-504 : Tests de Charge Locust Haute Performance (> 1 000 requêtes/seconde)**
  - Étendre `tests/locustfile.py` pour tester simultanément 1 000 utilisateurs concurrents effectuant des requêtes de clone Git Smart HTTP, de génération de challenge ZKP et de scan de code.
  - Vérifier que le temps de réponse p95 reste inférieur à 250 ms.
- [ ] **T-TST-505 : Validation Continue 100% Sans Emoji & Accessibilité WCAG 2.2 AA**
  - Maintenir l'exécution obligatoire du script `scripts/check_no_emoji.py` dans le pipeline de pré-commit et la CI.
  - Vérifier la conformité de tous les gabarits HTML aux exigences d'accessibilité WCAG 2.2 AA (ratios de contraste, navigation clavier, attributs ARIA).

---

## 4. Procédure Immédiate de Déploiement en Production

```bash
# 1. Cloner le référentiel sur le serveur sécurisé
git clone https://git.bantudevlab.africa/bantudevlab/bantu-platform.git /opt/bantudevlab
cd /opt/bantudevlab

# 2. Configurer les variables d'environnement de production
cp .env.production.example .env
# Éditer .env avec des secrets cryptographiques générés aléatoirement

# 3. Lancer l'infrastructure complète de production (Django + GitLab CE + Postgres + Redis + Nginx)
docker compose -f docker-compose.yml up -d --build

# 4. Appliquer les migrations de base de données
docker compose exec django_app python manage.py migrate

# 5. Collecter les ressources statiques optimisées
docker compose exec django_app python manage.py collectstatic --noinput

# 6. Exécuter la suite complète de validation
docker compose exec django_app python -m pytest
docker compose exec django_app python scripts/check_no_emoji.py
```

---

## 5. Définition du Terminé (Definition of Done — Prod Ready)

1. **Aucun Secret par Défaut :** L'application refuse de démarrer si une variable secrète est manquante ou utilise une valeur d'exemple.
2. **Couverture de Tests ≥ 95% :** La suite pytest stricte passe avec succès sur l'ensemble des modules critiques.
3. **Zéro Échec aux Audits de Sécurité :** Aucun avertissement détecté par `bandit` et `ruff`.
4. **Intégration GitLab Validée :** Authentification ZKP opérationnelle sur GitLab CE, runners CI panafricains actifs et webhooks signés traités sans perte.
5. **UI 100% Panafricaine & Vectorielle :** Aucune ressource tierce externe (zéro CDN), aucun emoji, thème clair/sombre persistant et conformité multilingue.
