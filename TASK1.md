# 🌍 BANTUDEVLAB — AUDIT CRITIQUE EXHAUSTIF & PLAN D'ACTION STRATÉGIQUE (TASK1)

> **Document de Référence Technique & Feuille de Route d'Ingénierie Industrielle**
> *Statut : Validation Technique & Spécifications de Production (Grade PRO)*
> *Date : Mai 2025*
> *Cible : Forge Logicielle Panafricaine Souveraine (Hybrid Gitea CE + Django Sovereign Layer + ZKP + Gemma 5B)*

---

# TABLE DES MATIÈRES

1. [SYNTHÈSE EXÉCUTIVE & VISION STRATÉGIQUE](#1-synthèse-exécutive--vision-stratégique)
2. [ANALYSE CRITIQUE FICHIER PAR FICHIER & DIAGNOSTIC DÉTAILLÉ](#2-analyse-critique-fichier-par-fichier--diagnostic-détaillé)
   - [2.1 Configuration Système, Environnement & Déploiement](#21-configuration-système-environnement--déploiement)
   - [2.2 Module Cryptographique & Authentification Zero-Trust (`apps/zkp_auth`)](#22-module-cryptographique--authentification-zero-trust-appszkp_auth)
   - [2.3 Module d'Intégration Forge Git Gitea (`apps/gitea_client`)](#23-module-dintégration-forge-git-gitea-appsgitea_client)
   - [2.4 Module Scanner de Sécurité & Souveraineté (`apps/security_scanner`)](#24-module-scanner-de-sécurité--souveraineté-appssecurity_scanner)
   - [2.5 Module d'Assistant IA Local Gemma 5B (`apps/ai_assistant`)](#25-module-dassistant-ia-local-gemma-5b-appsai_assistant)
   - [2.6 Module Core & Vues Applicatives (`apps/core`)](#26-module-core--vues-applicatives-appscore)
   - [2.7 Interfaces Utilisateurs & Design System (`templates/` & `static/`)](#27-interfaces-utilisateurs--design-system-templates--static)
   - [2.8 Pipeline de Fine-Tuning Gemma 5B (`finetuning/`)](#28-pipeline-de-fine-tuning-gemma-5b-finetuning)
   - [2.9 Suite de Tests & Assurance Qualité (`tests/` & CI/CD)](#29-suite-de-tests--assurance-qualité-tests--cicd)
3. [MATRICE DES TÂCHES OPÉRATIONNELLES PRO (TASK1)](#3-matrice-des-tâches-opérationnelles-pro-task1)
   - [Axe 1 : Sécurité Maximale & Zero-Trust Durci (SEC)](#axe-1--sécurité-maximale--zero-trust-durci-sec)
   - [Axe 2 : Performance, Scalabilité & Résilience (PERF)](#axe-2--performance-scalabilité--résilience-perf)
   - [Axe 3 : Développement & Architecture Cœur de Forge (DEV)](#axe-3--développement--architecture-cœur-de-forge-dev)
   - [Axe 4 : Design System, Interface Graphique & UX Moderne (UI/UX)](#axe-4--design-system-interface-graphique--ux-moderne-uiux)
   - [Axe 5 : Souveraineté Numérique & Conformité Panafricaine (SOUV)](#axe-5--souveraineté-numérique--conformité-panafricaine-souv)
   - [Axe 6 : Qualité Logicielle, Tests & Intégration Continue (QA/TEST)](#axe-6--qualité-logicielle-tests--intégration-continue-qatest)
4. [ROADMAP D'EXÉCUTION & CRITÈRES D'ACCEPTATION (DOD)](#4-roadmap-dexécution--critères-dacceptation-dod)

---

# 1. SYNTHÈSE EXÉCUTIVE & VISION STRATÉGIQUE

BANTUDEVLAB incarne une rupture majeure dans le paysage technologique africain : transformer le continent d'un simple consommateur d'infrastructures étrangères (soumises au Cloud Act, aux sanctions extraterritoriales et aux coupures de câbles sous-marins internationaux) en un acteur souverain hébergeant son propre patrimoine logiciel critique.

### Points Forts Constatés :
1. **Socle conceptuel solide** : Le choix d'une architecture hybride articulant un moteur Git ultra-éprouvé (**Gitea CE**) et une surcouche souveraine en **Python/Django** permet d'avoir simultanément la richesse fonctionnelle de Git et un contrôle strict sur la gouvernance.
2. **Innovation cryptographique réelle** : Implémentation fonctionnelle d'un protocole d'authentification **Schnorr / Sigma NIZKP (Non-Interactive Zero-Knowledge Proof)** avec défi Fiat-Shamir, éliminant les vecteurs classiques de vol d'identifiants.
3. **Pipeline d'IA locale maîtrisé** : Présence d'un pipeline complet de fine-tuning QLoRA 4-bit pour Gemma 5B orienté vers la conformité panafricaine et l'ingénierie sécurisée.
4. **Excellente base de tests** : Suite automatisée sous Django Test Framework avec 100% de réussite sur les scénarios initiaux.

### Défis Critiques pour le Passage au Niveau Professionnel (PRO) :
- **Absence de persistance et synchronisation asynchrone** : Les scans de sécurité et appels IA sont synchrones et bloquants, rendant le système vulnérable aux dénis de service (DoS).
- **Sécurisation incomplète des points d'intégration** : Absence de validation cryptographique HMAC sur les webhooks Gitea entrants, pas de rate-limiting (throttling), et secrets d'environnement par défaut non sécurisés en mode production.
- **Interface utilisateur embryonnaire** : UI basée sur du CSS monolithique basique sans interactivité moderne, composants asynchrones ni gestion d'état réactive (absence de WebSockets, notifications temps réel ou dashboard interactif complet).
- **Multi-tenancy et gestion des organisations non branchés** : La surcouche ne reflète pas encore la structure multi-organisations, multi-équipes et dépôts privés de Gitea de manière unifiée.

---

# 2. ANALYSE CRITIQUE FICHIER PAR FICHIER & DIAGNOSTIC DÉTAILLÉ

---

## 2.1 Configuration Système, Environnement & Déploiement

### `config/settings.py`
- **Rôle** : Cœur de configuration du projet Django (bases de données, middlewares, apps installées, paramètres tiers).
- **Forces** :
  - Détection dynamique de l'environnement (`DEBUG`, `ALLOWED_HOSTS`, `DB_ENGINE`).
  - Prise en charge transparente de PostgreSQL avec bascule SQLite pour le développement local et les tests.
- **Faiblesses & Risques Critiques** :
  - `SECRET_KEY` dispose d'une valeur par défaut en clair dans le code (`bantudevlab-sovereign-secret-key-insecure-dev-only-2025`), ce qui expose les sessions si le fichier `.env` est manquant en production.
  - `ALLOWED_HOSTS` par défaut fixé à `*` si non spécifié, vulnérable aux attaques par falsification d'en-tête `Host`.
  - Absence de middlewares de sécurité de production : pas de configuration `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`.
  - `REST_FRAMEWORK` autorise `AllowAny` globalement sans stratégie de limitation de débit (`DEFAULT_THROTTLE_CLASSES` absent).
  - Aucune couche de cache configurée (Redis/Memcached).
- **Améliorations requises** :
  - Lever une exception bloquante si `SECRET_KEY` n'est pas fourni quand `DEBUG=False`.
  - Intégrer `django-redis` pour le caching et la gestion des sessions distribuées.
  - Configurer `django-ratelimit` ou les throttles DRF sur les endpoints sensibles (ZKP challenge, scan de sécurité).

### `config/urls.py`
- **Rôle** : Routage global du backend.
- **Forces** : Découpage clair et modulaire par préfixes d'API (`/api/zkp/`, `/api/forge/`, `/api/security/`, `/api/ai/`).
- **Faiblesses** :
  - Absence de documentation Swagger / OpenAPI native (ex: `drf-spectacular`).
  - Absence de page d'erreur personnalisée (404, 500, 403) conforme à la charte souveraine.
  - Pas de vérification d'état globale de santé (`/healthz` et `/readyz` pour orchestrateurs Kubernetes ou Docker Swarm).
- **Améliorations requises** :
  - Ajouter les endpoints d'observabilité standard (`/health/`, `/metrics/` Prometheus).
  - Intégrer `drf-spectacular` pour générer automatiquement la spécification OpenAPI v3.

### `config/wsgi.py`
- **Rôle** : Point d'entrée WSGI pour les serveurs HTTP Python.
- **Forces** : Conforme aux standards Django.
- **Faiblesses** : Pas de point d'entrée ASGI (`config/asgi.py` absent), empêchant le support natif des WebSockets (Django Channels) pour les alertes de scan et revues IA en streaming.
- **Améliorations requises** :
  - Créer `config/asgi.py` et configurer Django Channels pour les notifications push temps réel.

### `Dockerfile`
- **Rôle** : Conteneurisation de la surcouche Django.
- **Forces** : Image légère basée sur `python:3.12-slim`, nettoyage du cache APT (`rm -rf /var/lib/apt/lists/*`).
- **Faiblesses & Risques** :
  - L'image s'exécute sous l'utilisateur `root`, ce qui viole les règles fondamentales de sécurité en conteneur (risque d'évasion de conteneur).
  - Le `CMD` lance `python manage.py runserver 0.0.0.0:8000`, serveur de développement Django formellement déconseillé en production (pas de serveur WSGI/ASGI de production comme Gunicorn ou Uvicorn).
  - Les migrations sont lancées directement dans le `CMD`, ce qui peut générer des verrous concurrents si plusieurs réplicas sont déployés.
- **Améliorations requises** :
  - Créer et utiliser un utilisateur non-privilégié (`RUN useradd -m bantudev && USER bantudev`).
  - Remplacer le serveur de développement par Gunicorn avec workers Uvicorn (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker config.asgi:application`).
  - Séparer le script d'entrypoint pour la migration ordonnée.

### `docker-compose.yml`
- **Rôle** : Orchestration multi-services (PostgreSQL 16, Gitea 1.23-rootless, Surcouche Django).
- **Forces** :
  - Utilisation d'un réseau dédié isolé (`sovereign_net`).
  - Gitea configuré en mode `rootless` (sécurité renforcée).
  - Persistance des données via volumes Docker nommés (`postgres_data`, `gitea_data`).
- **Faiblesses** :
  - Pas de service de cache et file de messages (Redis manquant).
  - Absence de service d'inférence locale conteneurisé (ex: conteneur Ollama ou vLLM pour faire tourner Gemma 5B sans dépendre de l'hôte physique).
  - Pas de vérification d'état (`healthcheck`) sur le conteneur PostgreSQL avant le démarrage de Django ou Gitea.
- **Améliorations requises** :
  - Ajouter un conteneur `redis:7-alpine`.
  - Ajouter un service `ollama` avec profil GPU/CPU.
  - Ajouter des blocs `healthcheck` pour PostgreSQL et Gitea avec clause `condition: service_healthy` dans `depends_on`.

### `.env.example`
- **Rôle** : Modèle de configuration des secrets et endpoints.
- **Forces** : Présentation claire des variables requises.
- **Faiblesses** : Mot de passe par défaut faible (`sovereign_pass_2025`), token Gitea laissé vide sans guide de génération automatique.
- **Améliorations requises** :
  - Ajouter des générateurs de tokens aléatoires dans la documentation.
  - Définir des variables pour Redis, Celery, et les clés de chiffrement de stockage.

---

## 2.2 Module Cryptographique & Authentification Zero-Trust (`apps/zkp_auth`)

### `apps/zkp_auth/crypto.py`
- **Rôle** : Implémentation de la cryptographie à divulgation nulle de connaissance (Schnorr Sigma NIZKP via Fiat-Shamir).
- **Forces** :
  - Utilisation d'un groupe MODP 2048-bit standardisé (RFC 3526 Group 14).
  - Utilisation de `secrets.randbelow` pour garantir l'aléa cryptographique CSPRNG sur les nonces éphémères $v$.
  - Fonction `verify_proof` mathématiquement exacte : $(g^s \cdot y^c) \pmod p = t$.
- **Faiblesses & Risques Mathématiques/Cryptographiques** :
  - **Sensibilité aux attaques par canal auxiliaire (Timing Attacks)** : La méthode `pow(base, exp, mod)` en Python n'est pas garantie en temps constant pour tous les chemins.
  - **Fragilité du hachage Fiat-Shamir** : La méthode `hash_to_int` concatène les chaînes sans séparateurs stricts de longueur fixe ni préfixe de domaine (Domain Separation Tag - DST), ce qui peut théoriquement prêter le flanc à des attaques par glissement de frontière ou d'ambiguïté de concaténation.
  - **Absence de protection contre les sous-groupes invalides** : La fonction `verify_proof` ne valide pas que $y^{(p-1)/2} \equiv 1 \pmod p$ (vérification que la clé publique $y$ appartient bien au sous-groupe de premier ordre d'ordre $q$).
- **Améliorations requises** :
  - Ajouter une validation formelle d'appartenance au sous-groupe pour toute clé publique enregistrée ($y^q \pmod p == 1$).
  - Implémenter un Domain Separation Tag structuré (`BANTUDEVLAB_SCHNORR_V1_HASH`).
  - Utiliser `hmac.compare_digest` ou un opérateur à temps constant pour la comparaison finale.

### `apps/zkp_auth/models.py`
- **Rôle** : Modélisation des identités souveraines et des jetons de challenge anti-rejeu.
- **Forces** :
  - Modèle `SovereignIdentity` lié au compte Django `User` sans persistance de mot de passe.
  - Modèle `ZKPChallenge` avec horodatage d'expiration (`expires_at`) et drapeau d'utilisation (`is_used`) pour bloquer le rejeu.
- **Faiblesses** :
  - Pas de nettoyage automatique des challenges expirés (accumulation de lignes inutiles en base).
  - Pas d'index sur `expires_at` ou `is_used` (ralentissement potentiel sous fort trafic).
  - Pas de trace d'audit sur l'adresse IP cliente ou le User-Agent ayant demandé ou consommé le challenge.
- **Améliorations requises** :
  - Ajouter des index composites `[('user', 'challenge_nonce'), ('expires_at', 'is_used')]`.
  - Ajouter des champs d'auditabilité (`ip_address`, `user_agent`, `failure_count`).
  - Implémenter une tâche planifiée (Celery Beat) pour purger les challenges expirés.

### `apps/zkp_auth/views.py`
- **Rôle** : Endpoints DRF pour l'enregistrement (`/register/`), la demande de défi (`/challenge/`) et la vérification (`/verify/`).
- **Forces** :
  - Validation du format hexadécimal de la clé publique.
  - Désactivation explicite des mots de passe avec `user.set_unusable_password()`.
  - Invalidation immédiate du nonce après tentative (`challenge.is_used = True`).
- **Faiblesses & Risques** :
  - **Énumération d'utilisateurs** : Dans `ZKPChallengeView`, si l'utilisateur n'existe pas, la vue renvoie explicitement `HTTP 404 'Utilisateur introuvable'`, permettant à un attaquant de scanner la base des noms d'utilisateurs.
  - **Absence de Rate Limiting** : Un attaquant peut spammer `/api/zkp/challenge/` pour saturer la base de données ou mener une attaque par force brute sur les identités.
  - **Session Django classique uniquement** : La vue `login(request, user)` génère un cookie de session, mais aucun jeton moderne (ex: Sovereign JWT ou Token OAuth2) n'est renvoyé pour les clients CLI Git ou les intégrations externes.
- **Améliorations requises** :
  - Renvoyer un code neutre ou un faux challenge si l'utilisateur n'existe pas afin de neutraliser l'énumération.
  - Appliquer un rate-limiting strict (ex: 5 requêtes/minute par IP sur les endpoints ZKP).
  - Générer un jeton d'accès sécurisé pour l'interaction avec le CLI Git (`bantu-cli`).

---

## 2.3 Module d'Intégration Forge Git Gitea (`apps/gitea_client`)

### `apps/gitea_client/client.py`
- **Rôle** : Connecteur d'API REST vers le moteur Gitea CE.
- **Forces** :
  - Mode dégradé / simulation sovereign fallback intelligent, permettant à l'application de fonctionner même si Gitea est en cours de redémarrage ou en mode démo déconnecté.
  - Méthodes propres d'abstraction (`list_repositories`, `create_repository`, `get_repository_commits`, `get_server_version`).
- **Faiblesses** :
  - Timeout court et rigide (`timeout=5`) sans stratégie de retry exponentiel en cas de latence réseau.
  - Pas de support pour la pagination complète des dépôts Gitea (paramètre `limit=50` en dur sans curseur de page).
  - Gestion d'authentification limitée : utilisation exclusive d'un token admin statique, sans prise en charge des tokens OAuth2 délégués par développeur.
- **Améliorations requises** :
  - Implémenter une politique de retry avec `urllib3.util.retry.Retry`.
  - Ajouter la gestion de la pagination avec pagination DRF conforme.
  - Permettre l'exécution des opérations au nom de l'utilisateur connecté via jeton d'accès personnel (PAT) ou SSO.

### `apps/gitea_client/views.py`
- **Rôle** : Exposition des dépôts et réception des webhooks Gitea.
- **Forces** :
  - Cache automatique des dépôts créés dans la table locale `SovereignRepository`.
  - Réception préparée des événements de push et de PR dans `GiteaWebhookReceiverView`.
- **Faiblesses & Risques de Sécurité Majeurs** :
  - **Vulnérabilité Webhook sans signature** : L'endpoint `/api/forge/webhook/` accepte n'importe quelle requête HTTP POST sans vérifier la signature secrète HMAC (`X-Gitea-Signature`). N'importe qui sur Internet peut forger un faux webhook pour déclencher des scans ou altérer les métriques.
  - Traitement synchrone du webhook : Si le webhook devait lancer immédiatement le scanner de sécurité et l'IA Gemma 5B, la requête HTTP Gitea tomberait en timeout (au-delà de 10s).
- **Améliorations requises** :
  - Valider obligatoirement la signature `X-Gitea-Signature` avec `hmac.compare_digest`.
  - Déléguer l'exécution du scan et de la revue IA à une tâche asynchrone d'arrière-plan.

### `apps/gitea_client/models.py`
- **Rôle** : Table de réplication et métadonnées de souveraineté des dépôts.
- **Forces** : Modèle simple et lisible associant nom, propriétaire, URLs Git et score de souveraineté.
- **Faiblesses** : Pas de relation de clé étrangère avec les organisations souveraines ou les utilisateurs Django. Pas de suivi des branches protégées ni des licences de code.
- **Améliorations requises** :
  - Ajouter les champs `default_branch`, `license_spdx`, `stars_count`, `forks_count`, `is_archived`.
  - Lier optionnellement à l'utilisateur Django propriétaire.

---

## 2.4 Module Scanner de Sécurité & Souveraineté (`apps/security_scanner`)

### `apps/security_scanner/engine.py`
- **Rôle** : Moteur d'analyse statique de code source (SAST) et de conformité de souveraineté numérique.
- **Forces** :
  - Détection efficace des motifs critiques (clés AWS, tokens GitHub/Gitea, clés privées RSA/SSH, JWTs).
  - Détection des vulnérabilités de haut niveau (`eval`, `exec`, `pickle.load`, injection SQL par concaténation, commandes OS).
  - Concept pionnier et unique de **Score de Souveraineté Numérique** (pénalités pour fuites de télémétrie étrangère vers Google APIs, AWS US/EU ou trackers).
- **Faiblesses & Limites Techniques** :
  - **Analyse purement regex** : L'utilisation exclusive d'expressions régulières génère des faux positifs (ex: mentions dans des commentaires ou de la documentation) et des faux négatifs (ex: injections SQL via formatage f-strings multi-lignes ou variables intermédiaires).
  - Absence d'analyse par arbre syntaxique abstrait (AST) pour le langage Python (`ast.parse`).
  - Scan mono-fichier : Impossible à ce stade de scanner une archive Git complète (.zip ou tarball) ou un commit multi-fichiers en une seule passe.
- **Améliorations requises** :
  - Coupler le scanner regex avec un analyseur basé sur l'AST (`ast.NodeVisitor`) pour analyser le flux de données réel en Python.
  - Détecter les secrets avec calcul d'entropie de Shannon pour repérer les chaînes aléatoires de haute entropie non couvertes par les regex standards.
  - Ajouter le support de scan récursif de répertoires ou de diffs de Pull Requests.

### `apps/security_scanner/models.py` & `views.py`
- **Rôle** : Historisation des audits et API de déclenchement de scan.
- **Forces** : Sauvegarde détaillée des rapports dans `SecurityAuditReport` avec champ `JSONField` pour stocker les occurrences brutes.
- **Faiblesses** :
  - `ScanCodeView` exécute le scan de manière synchrone. Pour un fichier de 50 000 lignes ou un commit massif, cela bloquera le worker Django.
  - Pas de filtrage par sévérité ni de pagination sur `SecurityAuditHistoryView` (renvoie arbitrairement les 20 derniers).
- **Améliorations requises** :
  - Ajouter la pagination DRF et les filtres de recherche (`repository_name`, `severity`, date).
  - Exporter les rapports sous format standardisé SARIF (Static Analysis Results Interchange Format) pour une intégration native avec Gitea Actions.

---

## 2.5 Module d'Assistant IA Local Gemma 5B (`apps/ai_assistant`)

### `apps/ai_assistant/gemma.py`
- **Rôle** : Client d'inférence vers le modèle Gemma 5B hébergé localement (Ollama/vLLM) avec moteur de secours hors-ligne déterministe.
- **Forces** :
  - **Prompt système panafricain inspiré et contextualisé** (BANTU-AI).
  - **Sovereign Fallback Engine exemplaire** : Même sans GPU ni serveur Ollama démarré, le système analyse syntaxiquement le code et produit des recommandations de sécurité structurées et contextualisées.
  - Paramètres de génération adaptés (`temperature: 0.2` pour limiter les hallucinations de code).
- **Faiblesses** :
  - Pas de streaming de la réponse (les réponses complètes de LLM peuvent prendre plusieurs secondes, entraînant un gel de l'UI si non streamées).
  - Découpage de contexte absent : Pas de chunking pour les fichiers de code volumineux dépassant la fenêtre de contexte de Gemma 5B.
  - Pas de mise en cache sémantique des prompts identiques.
- **Améliorations requises** :
  - Implémenter le Server-Sent Events (SSE) ou WebSockets pour streamer la génération mot à mot.
  - Ajouter un cache de réponses basé sur le hash SHA-256 du code analysé pour réduire la charge GPU.
  - Prendre en charge les embeddings via `GEMMA_EMBEDDINGS_URL` pour implémenter un RAG (Retrieval-Augmented Generation) sur les dépôts de code et la documentation technique souveraine.

### `apps/ai_assistant/views.py` & `models.py`
- **Rôle** : Endpoint d'analyse IA et journalisation des interactions dans `AIInteractionLog`.
- **Forces** : Historique persistant des requêtes et réponses générées.
- **Faiblesses** :
  - Tronquage brutal du prompt à 500 caractères dans la création du log (`prompt_snippet=code_snippet[:500]`), ce qui tronque les informations d'audit pour les requêtes longues.
  - Pas d'authentification requise sur l'endpoint `/api/ai/review/` (risque d'abus et de déni de service sur le GPU).
- **Améliorations requises** :
  - Restreindre l'accès à l'API IA aux utilisateurs authentifiés via ZKP.
  - Utiliser un champ `TextField` complet pour archiver le prompt avec hashing d'anonymisation des secrets potentiels.

---

## 2.6 Module Core & Vues Applicatives (`apps/core`)

### `apps/core/views.py` & `urls.py`
- **Rôle** : Contrôleurs pour la page d'accueil (`/`), le tableau de bord (`/dashboard/`) et la page des métriques (`/sovereignty-metrics/`).
- **Forces** : Agrégation intelligente des données provenant des différents modules (repos Gitea, identités ZKP, audits de sécurité, statistiques IA).
- **Faiblesses** :
  - Calcul direct de la moyenne en mémoire : `round(sum(a.sovereignty_score for a in audits) / len(audits))` au lieu d'utiliser l'agrégation de base de données Django ORM (`audits.aggregate(Avg('sovereignty_score'))`).
  - Pas de mise en cache HTTP des pages statistiques qui changent peu souvent.
- **Améliorations requises** :
  - Utiliser `django.db.models.Avg` pour optimiser la charge SQL.
  - Ajouter un décorateur de cache `@cache_page(60)` sur la page des métriques.

---

## 2.7 Interfaces Utilisateurs & Design System (`templates/` & `static/`)

### `static/css/style.css`
- **Rôle** : Feuille de style principale du portail.
- **Forces** :
  - Palette de couleurs soignée et identitaire (Or Panafricain `#f59e0b`, Émeraude `#10b981`, Terre Cuite `#dc2626`, Fond Sombre `#0b0f19`).
  - Variables CSS bien définies en racine (`:root`).
- **Faiblesses** :
  - Design statique non réactif aux interactions modernes (pas d'animations fluides, pas de micro-interactions, pas de squelettes de chargement `skeleton loaders`).
  - Absence de support natif pour le mode clair (dark mode exclusif et non configurable).
  - Absence de modularité CSS (un seul fichier monolithique de 150 lignes).
- **Améliorations requises** :
  - Structurer le CSS avec des variables avancées pour l'accessibilité (contraste WCAG AAA).
  - Ajouter des états de chargement animés (`spinners`, barres de progression) pour les actions cryptographiques ZKP et les analyses IA.

### `templates/base.html`
- **Rôle** : Squelette HTML principal.
- **Forces** : En-tête sémantique, barre de navigation claire, pied de page enrichi.
- **Faiblesses** :
  - Absence de gestion des messages flash Django (`messages` framework).
  - Lien externe Gitea codé en dur vers `http://localhost:3000` au lieu de s'adapter à la variable dynamique `GITEA_EXTERNAL_URL`.
  - Absence d'icônes SVG optimisées (utilisation d'emojis qui rendent différemment selon les OS).
- **Améliorations requises** :
  - Intégrer un système de notifications Toast / Alertes dynamiques.
  - Injecter `GITEA_EXTERNAL_URL` via un processeur de contexte de template.
  - Remplacer les emojis par des icônes SVG vectorielles modernes (Lucide / Heroicons).

### `templates/zkp_auth/login.html`
- **Rôle** : Interface de génération de clés et d'authentification client-side ZKP.
- **Forces** :
  - **Prouesse technique client-side** : Implémentation en JavaScript natif de l'exponentiation modulaire BigInt (`modPow`) et du protocole Fiat-Shamir dans le navigateur. Le secret ne quitte véritablement jamais le navigateur !
  - Console de log interactive affichant chaque étape mathématique en direct.
- **Faiblesses** :
  - Valeurs pré-remplies par défaut en clair dans les champs (`kouame_dev`, `cle_secrete_panafricaine_2025`), adaptées à une démo mais à sécuriser pour la production.
  - En cas d'échec de vérification, pas de message d'aide guidant le développeur.
  - Pas de sauvegarde locale sécurisée de la clé publique (ex: `localStorage` chiffré ou WebAuthn/Passkey integration).
- **Améliorations requises** :
  - Supprimer les valeurs pré-remplies et ajouter un bouton de génération de seed sécurisée aléatoire (12-24 mots BIP-39).
  - Proposer l'export/import d'un fichier d'identité souverain (`.bantu-key.json`).
  - Rediriger automatiquement vers le tableau de bord avec session active dès la validation de la preuve.

### `templates/core/dashboard.html`
- **Rôle** : Hub de commande de la forge.
- **Forces** : Workbench intégré permettant de tester en direct le scanner et l'assistant IA sur un extrait de code.
- **Faiblesses** :
  - Pas de coloration syntaxique dans la zone de code (simple élément `<textarea>` noir sans numérotation de lignes ni coloration Prism.js ou Monaco Editor).
  - Les résultats de scan sont affichés en JSON brut (`JSON.stringify(data, null, 2)`), peu lisible pour un utilisateur non-technique.
- **Améliorations requises** :
  - Intégrer un éditeur de code web léger avec coloration syntaxique (Prism.js ou CodeMirror).
  - Remplacer le rendu JSON brut par des cartes visuelles interactives classées par sévérité avec badges de remédiation cliquables.

---

## 2.8 Pipeline de Fine-Tuning Gemma 5B (`finetuning/`)

### `finetuning/dataset_preparation.py`
- **Rôle** : Génération du jeu de données d'apprentissage d'instructions souveraines (`sovereign_instruct_dataset.jsonl`).
- **Forces** :
  - Formatage parfait pour Gemma (`<bos><start_of_turn>user ... <start_of_turn>model`).
  - Exemples hautement pertinents pour l'ingénierie financière et télécom africaine (USSD, Mobile Money, ZKP Schnorr, conformité Union Africaine).
- **Faiblesses** :
  - Volume d'échantillons très limité (seulement 4 exemples codés en dur). Un fine-tuning efficace nécessite au minimum 1 000 à 5 000 exemples d'instructions diversifiés.
- **Améliorations requises** :
  - Élargir le générateur de dataset avec des modules d'augmentation de données synthétiques générant des variations de vulnérabilités réelles et de protocoles africains.
  - Ajouter la validation de schéma JSON et la déduplication automatique.

### `finetuning/train_lora.py`
- **Rôle** : Script d'entraînement avec quantification QLoRA 4-bit (NF4).
- **Forces** :
  - Configuration de pointe : bitsandbytes NF4, bfloat16, double quantification, cibles LoRA exhaustives (`q_proj`, `k_proj`, `v_proj`, `o_proj`, etc.).
  - Présence du flag `--dry_run` permettant de valider l'intégrité du code même sur des machines sans carte graphique NVIDIA.
- **Faiblesses** :
  - Dépendances lourdes non conteneurisées dans une image Docker dédiée pour l'IA (exécution tributaire des packages Python du système hôte).
  - Absence de journalisation vers un outil de suivi d'expériences (comme Weights & Biases ou MLflow souverain).
- **Améliorations requises** :
  - Créer un `Dockerfile.training` dédié avec support CUDA 12 et PyTorch préinstallé.
  - Ajouter un export automatique du modèle fusionné aux formats GGUF (pour exécution Ollama/vLLM) et Safetensors.

### `finetuning/evaluate.py`
- **Rôle** : Script d'évaluation de la qualité du modèle après fine-tuning.
- **Forces** : Vérification des mots-clés de conformité sur les cas d'usage ZKP et injection SQL.
- **Faiblesses** : Évaluation déterministe basée sur une simulation de mots-clés en mode dry-run sans calcul réel de métriques NLP standard (BLEU, ROUGE, perplexité).
- **Améliorations requises** :
  - Intégrer le calcul de métriques réelles (BLEU score, Perplexité, exactitude fonctionnelle de code via test unitaire unittests).

---

## 2.9 Suite de Tests & Assurance Qualité (`tests/` & CI/CD)

### `tests/`
- **Rôle** : Validation fonctionnelle des modules ZKP, Scanner, Client Gitea, Assistant IA et Vues DRF.
- **Forces** :
  - 20 tests couvrant l'ensemble des modules, exécutés en moins d'une seconde.
  - Excellents tests mathématiques sur les cas d'erreurs ZKP (rejet de preuve altérée, rejet de rejeu de nonce).
- **Faiblesses** :
  - Pas de tests de charge ni de stress sur la vérification modulaire 2048-bit.
  - Pas de tests d'interface utilisateur de bout en bout (E2E) automatisés avec Playwright.
  - Pas de calcul de couverture de code configuré en standard (absence de rapport `pytest-cov` ou `coverage.py`).
- **Améliorations requises** :
  - Ajouter une cible de couverture de code minimale (> 95%) avec rapport HTML.
  - Ajouter des tests Playwright automatisés validant le formulaire de login ZKP et le dashboard.

### `.github/workflows/ci.yml`
- **Rôle** : Pipeline d'intégration et de déploiement continus.
- **Forces** :
  - Pipeline complet et robuste : validation des dépendances, vérifications système Django, tests unitaires, validation syntaxique du dossier `finetuning/`, et build de l'image Docker.
- **Faiblesses** :
  - Pas d'étape de scan de sécurité sur le pipeline lui-même (ex: Bandit, Safety ou Trivy pour les conteneurs).
  - Pas d'analyse de formatage statique (`black`, `flake8` ou `ruff`).
- **Améliorations requises** :
  - Intégrer un linter ultra-rapide (`ruff check .` et `ruff format --check .`).
  - Ajouter un scan de vulnérabilités Docker avec Trivy.

---

# 3. MATRICE DES TÂCHES OPÉRATIONNELLES PRO (TASK1)

---

## Axe 1 : Sécurité Maximale & Zero-Trust Durci (SEC)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **SEC-01** | **Validation HMAC des Webhooks Gitea** | Implémenter l'interception et la vérification cryptographique de l'en-tête `X-Gitea-Signature` avec un secret partagé fort via `hmac.compare_digest`. Rejeter immédiatement toute requête non signée. | **P0** | `apps/gitea_client/views.py`, `config/settings.py` |
| **SEC-02** | **Validation du Sous-Groupe Cryptographique ZKP** | Durcir `apps/zkp_auth/crypto.py` en vérifiant impérativement que la clé publique reçue $y$ appartient au sous-groupe premier d'ordre $q$ ($y^q \equiv 1 \pmod p$ et $1 < y < p - 1$) pour éliminer les attaques de petits sous-groupes (Small Subgroup Attacks). | **P0** | `apps/zkp_auth/crypto.py`, `apps/zkp_auth/views.py` |
| **SEC-03** | **Protection contre l'Énumération d'Utilisateurs** | Harmoniser le temps de réponse et masquer les messages d'erreur sur `/api/zkp/challenge/` afin d'empêcher les attaquants de deviner si un compte existe ou non. | **P0** | `apps/zkp_auth/views.py` |
| **SEC-04** | **Rate Limiting & Throttling Adaptatif** | Configurer des quotas stricts sur les requêtes ZKP et de scan de code (ex: 5 req/min sur ZKP challenge/verify, 10 req/min sur l'API de scan) via Django REST Framework Throttling. | **P1** | `config/settings.py`, `apps/zkp_auth/views.py`, `apps/security_scanner/views.py` |
| **SEC-05** | **Durcissement des En-têtes HTTP & Cookies** | Activer `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = 'DENY'`, CSP (Content Security Policy) stricte et flags `HttpOnly` / `SameSite=Lax` sur tous les cookies. | **P1** | `config/settings.py` |
| **SEC-06** | **Journal d'Audit Immuable (Audit Trail)** | Créer un modèle d'audit infalsifiable avec hash en chaîne (Merkle Tree / Blockchain-like hashing) enregistrant chaque connexion ZKP, chaque création de repo et chaque scan de vulnérabilité. | **P2** | `apps/core/models.py`, `apps/core/audit.py` |

---

## Axe 2 : Performance, Scalabilité & Résilience (PERF)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **PERF-01** | **File de Tâches Asynchrones (Celery / Redis)** | Découpler les scans de sécurité volumineux et les appels d'inférence à Gemma 5B du cycle de requête HTTP de Django en introduisant Celery avec Redis en broker. | **P0** | `docker-compose.yml`, `config/celery.py`, `apps/security_scanner/tasks.py`, `apps/ai_assistant/tasks.py` |
| **PERF-02** | **Streaming d'Inférence IA (Server-Sent Events)** | Remplacer la réponse HTTP synchrone de `/api/ai/review/` par un flux de streaming SSE (Server-Sent Events) permettant l'affichage mot à mot de l'analyse Gemma 5B sans bloquer le navigateur. | **P1** | `apps/ai_assistant/views.py`, `apps/ai_assistant/gemma.py`, `templates/core/dashboard.html` |
| **PERF-03** | **Optimisation des Requêtes SQL & Indexation** | Ajouter des index de base de données explicites (`db_index=True`, `indexes=[models.Index(...)]`) sur les champs critiques : `scanned_at`, `repository_name`, `challenge_nonce`, `expires_at`. Remplacer les boucles d'agrégation Python par `models.Avg`. | **P1** | `apps/zkp_auth/models.py`, `apps/security_scanner/models.py`, `apps/core/views.py` |
| **PERF-04** | **Couche de Cache Distribué (Redis Caching)** | Mettre en cache les listes de dépôts Gitea et les métriques de souveraineté pendant 60 secondes pour soulager la base PostgreSQL et l'API Gitea. | **P2** | `config/settings.py`, `apps/gitea_client/client.py`, `apps/core/views.py` |
| **PERF-05** | **Serveur Web Haute Performance (Gunicorn + Uvicorn)** | Modifier le `Dockerfile` pour utiliser Gunicorn avec des workers asynchrones Uvicorn et un dimensionnement dynamique selon le nombre de cœurs CPU (`WEB_CONCURRENCY`). | **P1** | `Dockerfile`, `docker-compose.yml` |

---

## Axe 3 : Développement & Architecture Cœur de Forge (DEV)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **DEV-01** | **Synchronisation Bidirectionnelle Gitea** | Développer un service de synchronisation automatique synchronisant les statuts de Pull Requests, les commits et les branches entre Gitea et BantuDevLab via l'API REST v1. | **P0** | `apps/gitea_client/client.py`, `apps/gitea_client/sync.py` |
| **DEV-02** | **Support Multi-Tenancy & Organisations Africaines** | Créer le modèle `SovereignOrganization` pour regrouper les développeurs et dépôts par entité souveraine (ex: banques centrales, ministères, universités, startups tech régionales). | **P1** | `apps/core/models.py`, `apps/gitea_client/models.py`, `apps/core/views.py` |
| **DEV-03** | **Générateur et Validateur de Tokens d'Accès CLI Git** | Fournir aux développeurs un mécanisme de génération de tokens Git personnalisés validés via ZKP pour cloner et pousser du code sur Gitea via HTTPS sans mot de passe standard. | **P1** | `apps/zkp_auth/tokens.py`, `apps/zkp_auth/views.py` |
| **DEV-04** | **Documentation API Interactive (OpenAPI / Swagger)** | Intégrer `drf-spectacular` avec interface Swagger UI accessible sur `/api/docs/` documentant l'ensemble des endpoints ZKP, Forge, Scanner et Assistant IA. | **P2** | `config/settings.py`, `config/urls.py`, `requirements.txt` |
| **DEV-05** | **Export des Rapports de Sécurité au Format SARIF** | Implémenter la sérialisation des vulnérabilités au standard SARIF 2.1.0 afin que Gitea et les runners CI/CD puissent afficher les annotations de failles directement dans les diffs de code. | **P2** | `apps/security_scanner/serializers.py`, `apps/security_scanner/views.py` |

---

## Axe 4 : Design System, Interface Graphique & UX Moderne (UI/UX)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **UI-01** | **Éditeur de Code Web avec Coloration & Numérotation** | Intégrer Monaco Editor ou CodeMirror sur le workbench du dashboard avec coloration syntaxique, détection d'erreurs et affichage fluide des snippets analysés. | **P0** | `templates/core/dashboard.html`, `static/css/style.css` |
| **UI-02** | **Refonte Graphique du Tableau de Bord & Visualisations** | Remplacer l'affichage JSON brut par des composants visuels modernes (cartes de vulnérabilités interactives avec badge de sévérité, jauges circulaires pour le score de souveraineté). | **P0** | `templates/core/dashboard.html`, `static/css/style.css` |
| **UI-03** | **Assistant ZKP Interactif & Gestionnaire d'Identité** | Remplacer les champs statiques de connexion ZKP par un assistant interactif : génération automatique de phrase mnémonique (BIP-39), jauge de force cryptographique, et bouton de téléchargement de clé privée souveraine protégée. | **P1** | `templates/zkp_auth/login.html` |
| **UI-04** | **Système de Notifications Toast & Statut Temps Réel** | Créer un composant global de messages Toast (succès, avertissement, erreur) affichant les retours utilisateurs lors des actions cryptographiques et de synchronisation. | **P1** | `templates/base.html`, `static/css/style.css` |
| **UI-05** | **Page Métriques Panafricaines Enrichie (Cartographie)** | Intégrer une visualisation interactive des nœuds souverains africains (Abidjan, Dakar, Lagos, Nairobi, Kigali) affichant la latence réseau locale et le statut des datacenters certifiés. | **P2** | `templates/core/metrics.html` |

---

## Axe 5 : Souveraineté Numérique & Conformité Panafricaine (SOUV)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **SOUV-01** | **Audit de Juridiction & Détection de Télémétrie Cloud Act** | Enrichir le moteur `apps/security_scanner/engine.py` pour détecter les SDKs propriétaires soumis au Cloud Act (Azure, AWS, Firebase, Google Analytics) et proposer automatiquement des alternatives open-source hébergées sur le cloud souverain. | **P0** | `apps/security_scanner/engine.py` |
| **SOUV-02** | **Conformité Convention de Malabo & Protection des Données** | Mettre en œuvre une charte stricte de protection des données conforme à la Convention de l'Union Africaine sur la Cybersécurité et la Protection des Données à Caractère Personnel (Malabo 2014) : absence totale de profilage commercial et chiffrement des métadonnées de repos. | **P1** | `templates/core/metrics.html`, `apps/core/models.py` |
| **SOUV-03** | **Mode Déconnecté & Résilience Réseau Local (IXP)** | Optimiser la forge pour fonctionner en autarcie complète au sein des points d'échange Internet locaux (IXP) en cas de coupure des câbles sous-marins transatlantiques (mise en cache des assets statiques, zéro ressource CDN étrangère). | **P1** | `templates/base.html`, `static/css/style.css`, `Dockerfile` |
| **SOUV-04** | **Modèle Gemma 5B Exporté en Format Léger GGUF** | Convertir et packager les poids du modèle Gemma 5B fine-tuné en format GGUF quantifié 4-bit (q4_k_m) pour permettre son inférence sur des serveurs légers africains sans GPU haut de gamme. | **P2** | `finetuning/export_gguf.py`, `finetuning/README.md` |

---

## Axe 6 : Qualité Logicielle, Tests & Intégration Continue (QA/TEST)

| Réf. | Tâche | Description Détaillée | Priorité | Fichiers Cibles |
|---|---|---|---|---|
| **QA-01** | **Tests End-to-End Complets avec Playwright** | Rédiger une suite complète de tests de bout en bout simulant le parcours utilisateur réel : génération de clé ZKP dans le navigateur -> authentification -> soumission de code dans le workbench -> vérification du score de souveraineté. | **P0** | `tests/test_e2e_playwright.py` |
| **QA-02** | **Fuzzing & Tests de Résilience Cryptographique ZKP** | Développer une suite de tests cryptographiques aléatoires (fuzzing) injectant des valeurs non conformes, des clés publiques dégradées, des nonces expirés et des messages altérés pour prouver l'inviolabilité mathématique de l'implémentation. | **P0** | `tests/test_zkp_fuzzing.py` |
| **QA-03** | **Couverture de Code Stricte (Coverage > 95%)** | Configurer `coverage.py` et `pytest-cov` dans le pipeline CI/CD avec blocage automatique si la couverture des modules `apps/zkp_auth`, `apps/security_scanner` ou `apps/ai_assistant` est inférieure à 95%. | **P1** | `pyproject.toml`, `.github/workflows/ci.yml` |
| **QA-04** | **Linter & Formatage Automatisé (Ruff / Bandit)** | Ajouter dans le workflow GitHub Actions les outils de linting ultra-rapides `ruff` et l'analyseur de sécurité statique Python `bandit` pour garantir une propreté de code irréprochable. | **P1** | `.github/workflows/ci.yml` |

---

# 4. ROADMAP D'EXÉCUTION & CRITÈRES D'ACCEPTATION (DOD)

### Jalon 1 : Sécurité Fondamentale & Résilience (Semaines 1-2) — **Priorité P0**
- [ ] Signature HMAC des webhooks Gitea active et testée.
- [ ] Vérification d'appartenance au sous-groupe ZKP implémentée dans `crypto.py`.
- [ ] Traitement asynchrone des analyses via Celery / Redis.
- [ ] Dockerfile durci avec utilisateur non-root et serveur de production Gunicorn/Uvicorn.
- [ ] Suite de tests Playwright E2E opérationnelle.

### Jalon 2 : Expérience Utilisateur & Design Professionnel (Semaines 3-4) — **Priorité P1**
- [ ] Workbench de dashboard refondu avec éditeur interactif et cartes de remédiation claires.
- [ ] Assistant de connexion ZKP avec générateur de phrase mnémonique et export de clé sécurisé.
- [ ] Streaming SSE des analyses de code générées par Gemma 5B.
- [ ] Optimisation des requêtes de base de données et activation du cache Redis.
- [ ] Couverture de tests consolidée à plus de 95%.

### Jalon 3 : Décentralisation Continentale & Industrialisation (Semaines 5-6) — **Priorité P2**
- [ ] Export et packaging de Gemma 5B en format GGUF pour inférence souveraine ultra-légère.
- [ ] Visualisation interactive de la cartographie des IXP et datacenters panafricains.
- [ ] Journal d'audit immuable avec chaînage cryptographique.
- [ ] Documentation d'API Swagger/OpenAPI publiée et accessible aux partenaires du continent.

---
*Document conçu et validé par l'équipe d'architecture souveraine BANTUDEVLAB — Systalink Cloud Africa.*
