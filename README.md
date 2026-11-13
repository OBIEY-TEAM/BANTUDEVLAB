# BANTUDEVLAB - Forge Logicielle Souveraine de l'Afrique

> **BANTUDEVLAB** centralise le code des développeurs africains sur une infrastructure souveraine et sécurisée : moteur Git résilient (Gitea CE), authentification Zero-Trust sans mot de passe par preuve à divulgation nulle de connaissance (ZKP), scanner de sécurité et d'entropie de Shannon (SAST / SARIF 2.1.0), et assistant IA local (Gemma 2 2B) optimisé pour l'inférence locale via Ollama.

- **Dépôt officiel (Forge souveraine Gitea) :** [https://git.cybersocle.site/obiey-code/bantudevlab.git](https://git.cybersocle.site/obiey-code/bantudevlab.git)
- **Accès web & Commits (branche `main`) :** [https://git.cybersocle.site/obiey-code/bantudevlab/commits/branch/main](https://git.cybersocle.site/obiey-code/bantudevlab/commits/branch/main)
- **Portail souverain en ligne :** [https://cybersocle.site](https://cybersocle.site)
- **Miroir GitHub :** [https://github.com/OBIEY-TEAM/BANTUDEVLAB](https://github.com/OBIEY-TEAM/BANTUDEVLAB)

---

## Sommaire

1. [Vision et Philosophie Souveraine](#vision-et-philosophie-souveraine)
2. [Architecture Globale](#architecture-globale)
3. [Stack Technique Complète](#stack-technique-complète)
4. [Démarrage Rapide](#démarrage-rapide)
5. [Sécurité et Hardening](#sécurité-et-hardening)
6. [Authentification Zero-Trust ZKP (Schnorr / Fiat-Shamir)](#authentification-zero-trust-zkp-schnorr--fiat-shamir)
7. [Scanner SAST Shannon & Conformité SARIF 2.1.0](#scanner-sast-shannon--conformité-sarif-210)
8. [Assistant IA Local Gemma 2 2B & Copilot Souverain](#assistant-ia-local-gemma-2-2b--copilot-souverain)
9. [Equivalence Fonctionnelle GitHub via Gitea](#equivalence-fonctionnelle-github-via-gitea)
10. [Cycles de Développement Continu (Dossier TASK)](#cycles-de-développement-continu-dossier-task)
11. [API et Documentation Interactive](#api-et-documentation-interactive)
12. [Interface Souveraine et Charte Graphique](#interface-souveraine-et-charte-graphique)
13. [Tests, CI/CD et Qualité](#tests-cicd-et-qualité)
14. [Outils Utilisés](#outils-utilisés)
15. [Index de la Documentation](#index-de-la-documentation)

---

## Vision et Philosophie Souveraine

BANTUDEVLAB répond aux impératifs d'indépendance numérique et technologique du continent africain, alignée sur la **Convention de Malabo (2014)** sur la cybersécurité et la protection des données à caractère personnel ainsi que les directives de l'Union Africaine :

- **Hébergement & Domaines :** Domaines achetés chez Systalink/Datacloud (`cybersocle.site`, `git.cybersocle.site`), application hébergée sur un VPS Ubuntu externe avec architecture conteneurisée.
- **Souveraineté des Données :** Contrôle territorialisé des données (aucun transfert vers des hyperscalers tiers).
- **Zéro Dépendance aux CDN Tiers :** Tous les composants frontaux (styles Primer, polices, scripts CodeMirror, icônes SVG) sont auto-hébergés localement.
- **Zéro Emoji :** Respect d'une interface professionnelle sobre et accessible, excluant tout caractère emoji au profit d'icônes vectorielles SVG souveraines.
- **Résilience et Mode Déconnecté :** Fonctionnement garanti en intranet ou réseau isolé avec modèles d'intelligence artificielle compacts exécutés en local (quantification GGUF 4-bit).

---

## Architecture Globale

L'infrastructure BANTUDEVLAB s'articule autour d'une architecture hybride associant un moteur Git ultra-performant et une surcouche de gouvernance souveraine en Python / Django :

```mermaid
flowchart TD
    subgraph Clients["Clients & Utilisateurs"]
        Dev["Developpeurs (Web / CLI)"]
        TeaCli["CLI tea (Equivalent gh)"]
        GitCli["Git CLI (SSH / HTTPS)"]
    end

    subgraph Edge["Frontal & Ingress"]
        Nginx["Nginx Reverse Proxy & SSL"]
    end

    subgraph CorePlatform["Plateforme Souveraine BantuDevLab"]
        DjangoCore["Django Core & DRF (Port 8000)<br/>Gouvernance, Multi-Tenancy & ZKP"]
        GiteaForge["Gitea CE Engine (Port 3002)<br/>Depots Git, Issues, PRs, LFS, Actions"]
    end

    subgraph StorageData["Persistance & Cache Isole"]
        PgBouncer["PgBouncer Pooler (Port 6432)"]
        PostgresDB[("PostgreSQL 16 Engine")]
        RedisCache[("Redis 7<br/>Broker Celery & Cache")]
        GitStorage[("Volumes Git Bare Repos")]
    end

    subgraph AsynchronousWorkers["Traitement Asynchrone & IA"]
        CeleryWorker["Celery Worker & Beat<br/>Audit, Purge, Webhooks"]
        GemmaEngine["Gemma 2 2B Local Engine<br/>Ollama / vLLM (Inference Locale)"]
    end

    Dev --> Nginx
    TeaCli --> Nginx
    GitCli --> GiteaForge

    Nginx --> DjangoCore
    Nginx --> GiteaForge

    DjangoCore --> PgBouncer --> PostgresDB
    DjangoCore --> RedisCache
    DjangoCore --> GemmaEngine
    DjangoCore -->|"REST API v1 + HMAC"| GiteaForge

    CeleryWorker --> RedisCache
    CeleryWorker --> PgBouncer
    CeleryWorker --> GemmaEngine
```

---

## Stack Technique Complète

| Domaine | Composant | Rôle & Spécificités |
|---|---|---|
| **Backend Core** | Python 3.12, Django 5.2, DRF 3.18 | API REST, multi-tenancy souverain, gouvernance des organisations |
| **Forge Git** | Gitea CE 1.22.6 (MIT) | Dépôts Git, Pull Requests, Code Review, Registres de paquets |
| **Base de Données** | PostgreSQL 16 + PgBouncer | Stockage relationnel haute performance avec pooling de connexions |
| **Cache & Tâches** | Redis 7 + Celery 5.6 | Files d'attente asynchrones, invalidation de cache, sessions |
| **Intelligence Artificielle** | Gemma 2 2B (Google) | Modèle souverain compact (2 milliards de paramètres), QLoRA / GGUF |
| **Cryptographie** | Cryptography 50+, hashlib | Zero-Knowledge Proofs Schnorr/Fiat-Shamir, SHA-256 Chained Audit |
| **Serveur ASGI/WSGI** | Gunicorn + Uvicorn Workers | Serveur d'application durci avec dimensionnement dynamique |
| **Interface Utilisateur** | Primer CSS, SVG natifs, CodeMirror | Équivalence visuelle GitHub, thème sombre/clair, sans CDN |
| **Assurance Qualité** | Pytest, Coverage (95.6% démontrée, 201 tests), Ruff, Bandit | Analyse statique, fuzzing cryptographique, tests end-to-end |

---

## Démarrage Rapide

### 1. Préparation des variables d'environnement

Copiez le modèle d'environnement et générez les secrets cryptographiques requis :

```bash
cp .env.example .env
# Generer des cles securisees
python -c "import secrets; print('DJANGO_SECRET_KEY=' + secrets.token_urlsafe(64))"
python -c "import secrets; print('GITEA_WEBHOOK_SECRET=' + secrets.token_hex(32))"
```

### 2. Déploiement Conteneurisé avec Docker Compose

L'intégralité des services (Django, Gitea, PostgreSQL, Redis, Celery) démarre en une seule commande :

```bash
docker compose up -d --build
```

Consultez le guide détaillé : [docker-deployment.md](docker-deployment.md).

### 3. Exécution Locale en Environnement de Développement

```bash
# Creation et activation de l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate

# Installation des dependances
pip install -r requirements.txt

# Application des migrations de base de donnees
python manage.py migrate

# Demarrage du serveur de developpement
python manage.py runserver 0.0.0.0:8000
```

---

## Sécurité et Hardening

- **Contrôle d'accès par défaut :** Toutes les routes de l'API requièrent une authentification par défaut (`IsAuthenticated`), à l'exception des points de terminaison cryptographiques publics (inscription ZKP, défi de challenge, vérification de preuve, santé).
- **Audit Trail Immuable :** Chaque action critique (connexion ZKP, création de dépôt, scan SAST, approbation de MR) est inscrite dans `AuditTrailLog` avec chaînage cryptographique SHA-256 (`previous_hash -> hash`) pour garantir la non-répudiation (vérifiable via `python manage.py export_malabo_compliance_report`).
- **En-têtes de Sécurité HTTP :** CSP strict sans `'unsafe-inline'` externe, HSTS avec préchargement, protection contre le clickjacking (`DENY`), isolation d'origine croisée (`COOP`/`COEP`).
- **Conteneurs Hardened :** Exécution sous utilisateur non-privilégié (`appuser:appgroup`, UID 1000), `read_only_root_filesystem`, et révocation de toutes les capacités Linux (`cap_drop: ALL`).

---

## Authentification Zero-Trust ZKP (Schnorr / Fiat-Shamir)

Le protocole d'identification de Schnorr non interactif (transformée de Fiat-Shamir) est implémenté sur le groupe RFC 3526 MODP 2048 bits ($p, q, g$).

```mermaid
sequenceDiagram
    autonumber
    actor Developpeur as Developpeur (Client)
    participant Serveur as Serveur BantuDevLab (API)
    participant BDD as Base de Donnees Souveraine

    Note over Developpeur: Secret prive x genere localement<br/>Cle publique y = g^x mod p
    Developpeur->>Serveur: POST /api/zkp/register/ {username, public_key: y}
    Serveur->>Serveur: Validation sous-groupe premier (y^q == 1 mod p)
    Serveur->>BDD: Stockage identite et cle publique y

    Note over Developpeur,Serveur: Phase d'Authentification Zero-Trust
    Developpeur->>Serveur: POST /api/zkp/challenge/ {username}
    Serveur->>BDD: Creation nonce aleatoire (usage unique, 5 min)
    Serveur-->>Developpeur: {challenge_nonce: c}

    Note over Developpeur: Calcul de l'engagement t = g^v mod p<br/>Reponse de Schnorr s = v - c * x mod q
    Developpeur->>Serveur: POST /api/zkp/verify/ {username, challenge_nonce, proof: (t, s)}
    Serveur->>Serveur: Verification verification equation:<br/>g^s * y^c == t mod p
    Serveur->>BDD: Consommation atomique du nonce (Anti-rejeu)
    Serveur-->>Developpeur: Session ouverte & Jetons JWT souverains
```

- `POST /api/zkp/tokens/generate/` : Émission de jetons Git sécurisés (`read`, `write`, `admin`) protégés par preuve ZKP.
- Spécifications cryptographiques complètes : [docs/security/crypto-spec.md](docs/security/crypto-spec.md).

---

## Scanner SAST Shannon & Conformité SARIF 2.1.0

Le module `apps/security_scanner` intègre un moteur d'analyse statique de sécurité (SAST) multi-langages :
- **Calcul d'Entropie de Shannon :** Détection automatique des clés privées, jetons d'accès et secrets enfouis dans le code source ($H \ge 3.8$).
- **Règles Anti-Vulnérabilités :** Injections SQL, fonctions d'exécution arbitraire (`eval`, `exec`), failles XSS, et bibliothèques non souveraines.
- **Formats Standards d'Exportation :** Rapports complets conformes à la norme internationale OASIS SARIF 2.1.0 (`/api/security/sarif/`).

---

## Assistant IA Local Gemma 2 2B & Copilot Souverain

BANTUDEVLAB intègre en local le modèle open-weights **Gemma 2 2B** développé par Google DeepMind, adapté aux contraintes de souveraineté et d'exécution locale :

- **Revue Autonome de Pull Requests :** Tâche d'arrière-plan Celery analysant les diffs Git, commentant les propositions de code et soumettant des suggestions structurées.
- **Spotlight Palette & Raccourcis Clavier :** Palette de commandes accessible via `Ctrl+K` ou `Cmd+K` pour rechercher des fichiers, naviguer ou invoquer l'IA.
- **Exportation de Sessions :** Sauvegarde et extraction des interactions Copilot au format Markdown ou JSON (`/api/ai/copilot/export/`).
- **Pipeline de Fine-Tuning Souverain :** Outils prêts à l'emploi dans `finetuning/` :
  - `dataset_preparation.py` : Génération de jeux de données d'instructions de cybersécurité.
  - `train_lora.py` : Fine-tuning compact par adaptateurs QLoRA.
  - `evaluate.py` : Évaluation automatique de conformité souveraine.
  - `export_gguf.py` : Conversion et quantification 4-bit (`q4_k_m`) pour inférence CPU/GPU ultra-rapide.

---

## Equivalence Fonctionnelle GitHub via Gitea

Le socle Gitea est personnalisé via des surcharges de templates Go (`custom/templates/`) et des styles Primer CSS pour offrir une parité visuelle et fonctionnelle totale avec GitHub :

- **Navigation & Vue Dépôt :** Arborescence interactive, sélecteur rapide de fichiers avec la touche `t`, affichage du `README.md` de profil pour l'utilisateur (`username/username`).
- **Gestion des Pull Requests :** Support complet des Draft Pull Requests (brouillons), Merge Box Primer, widget de suggestion de code multilignes et validation en 1 clic.
- **File de Fusion Souveraine (Merge Queue) :** Sérialisation FIFO et vérification automatisée de compatibilité avant intégration (`scripts/simulate_merge_queue.py`).
- **Graphe de Commits & Blame :** Heatmap interactive d'ancienneté des lignes de code et graphe topologique de branches en SVG multicolore.
- **Gestion de Projet & Équipes :** Jalons (Milestones) avec jauges de burndown, tableaux Markdown Primer avec tri par clic sur en-tête, et matrice à 5 rôles d'organisation (`Read`, `Triage`, `Write`, `Maintain`, `Admin`).
- **Avis de Sécurité (Security Advisories) :** Signalement confidentiel de failles avec calculatrice de sévérité CVSS v3.1.
- **Génération de Release Notes :** Agrégation automatique des PRs et contributeurs par catégorie (`scripts/generate_release_notes.py`).
- **Attestation SLSA & SBOM :** Génération de SBOM au standard CycloneDX v1.5 (`scripts/generate_sovereign_sbom.py`) et provenance cryptographique SHA-256 (`scripts/generate_release_provenance.py`).

---

## Cycles de Développement Continu (Dossier Archivé docs/archive/TASK)

Tous les plans directeurs, audits stratégiques et spécifications des 20 cycles de développement continu ont été classés dans le dossier d'archive [`docs/archive/TASK/`](docs/archive/TASK/) :

| Fichier | Objet et Périmètre Opérationnel |
|---|---|
| [`docs/archive/TASK/task2.md`](docs/archive/TASK/task2.md) | Plan de déploiement en production industrielle et guide d'exploitation |
| [`docs/archive/TASK/TASK3.md`](docs/archive/TASK/TASK3.md) | Transition industrielle et intégration de la fédération GitLab CE/EE |
| [`docs/archive/TASK/TASK5.md`](docs/archive/TASK/TASK5.md) | Audit global de sécurité, catalogue des failles et plan directeur IA Gemma |
| [`docs/archive/TASK/TASK6.md`](docs/archive/TASK/TASK6.md) | Spécifications opérationnelles de transformation Gitea vers l'expérience GitHub |
| [`docs/archive/TASK/TASK7.md`](docs/archive/TASK/TASK7.md) | Cycle 1 : Copilot local Gemma 2 2B et Command Palette Spotlight (`Ctrl+K`) |
| [`docs/archive/TASK/TASK8.md`](docs/archive/TASK/TASK8.md) | Cycle 2 : PR Review Bot autonome (Celery), explorateur d'arborescence (`t`) |
| [`docs/archive/TASK/TASK9.md`](docs/archive/TASK/TASK9.md) | Cycle 3 : Heatmap Blame interactive, générateur de provenance SLSA v1 |
| [`docs/archive/TASK/TASK10.md`](docs/archive/TASK/TASK10.md) | Cycle 4 : Tableaux Markdown Primer avec tri dynamique interactif |
| [`docs/archive/TASK/TASK11.md`](docs/archive/TASK/TASK11.md) | Cycle 5 : Graphe de dépendances et exportateur CycloneDX v1.5 SBOM PURL |
| [`docs/archive/TASK/TASK12.md`](docs/archive/TASK/TASK12.md) | Cycle 6 : Dépôts épinglés Primer et profil README spécial (`user/user`) |
| [`docs/archive/TASK/TASK13.md`](docs/archive/TASK/TASK13.md) | Cycle 7 : Polyfill de réactions GitHub (`:+1:`, `:heart:`, `:rocket:`) sans emoji |
| [`docs/archive/TASK/TASK14.md`](docs/archive/TASK/TASK14.md) | Cycle 8 : Inspecteur d'historique de livraison de webhooks et simulateur de renvoi |
| [`docs/archive/TASK/TASK15.md`](docs/archive/TASK/TASK15.md) | Cycle 9 : Rulesets de branches et badges de signature de commits Verified |
| [`docs/archive/TASK/TASK16.md`](docs/archive/TASK/TASK16.md) | Cycle 10 : Centre de notifications GitHub (Inbox, filtres dynamiques, raccourci `m`) |
| [`docs/archive/TASK/TASK17.md`](docs/archive/TASK/TASK17.md) | Cycle 11 : Générateur automatique de notes de version à partir des PRs |
| [`docs/archive/TASK/TASK18.md`](docs/archive/TASK/TASK18.md) | Cycle 12 : Recherche de code avancée, qualificateurs de recherche (`path:`, `repo:`) |
| [`docs/archive/TASK/TASK19.md`](docs/archive/TASK/TASK19.md) | Cycle 13 : Polyfill de suggestions de modifications de code dans les PRs |
| [`docs/archive/TASK/TASK20.md`](docs/archive/TASK/TASK20.md) | Cycle 14 : Graphe de réseau de commits et visualisation topologique SVG |
| [`docs/archive/TASK/TASK21.md`](docs/archive/TASK/TASK21.md) | Cycle 15 : Jalons d'issues (Milestones) et calcul de burndown d'avancement |
| [`docs/archive/TASK/TASK22.md`](docs/archive/TASK/TASK22.md) | Cycle 16 : Gestion d'équipes d'organisation et matrice de permissions à 5 rôles |
| [`docs/archive/TASK/TASK23.md`](docs/archive/TASK/TASK23.md) | Cycle 17 : Flux complet des Draft PRs (brouillons, badges, conversion en review) |
| [`docs/archive/TASK/TASK24.md`](docs/archive/TASK/TASK24.md) | Cycle 18 : File d'attente de fusion sécurisée (Merge Queue) et simulateur |
| [`docs/archive/TASK/TASK25.md`](docs/archive/TASK/TASK25.md) | Cycle 19 : Avis de sécurité (Security Advisories), signalement privé et CVSS |
| [`docs/archive/TASK/TASK26.md`](docs/archive/TASK/TASK26.md) | Cycle 20 : Export de session Copilot (Markdown/JSON) et audit de clôture |

Consultez la synthèse globale de l'audit des 20 cycles : [docs/SOVEREIGN_GITHUB_FORGE_COMPLETE_REVIEW.md](docs/SOVEREIGN_GITHUB_FORGE_COMPLETE_REVIEW.md).

---

## API et Documentation Interactive

L'API REST est documentée selon la spécification OpenAPI 3.0 via `drf-spectacular` :

- **Swagger UI Interactif :** `/api/docs/`
- **ReDoc :** `/api/redoc/`
- **Schéma OpenAPI JSON/YAML brut :** `/api/schema/`
- **Sondes de Vitalité et Disponibilité :** `/healthz` (liveness) et `/readyz` (readiness de la base de données et du cache Redis).

---

## Interface Souveraine et Charte Graphique

L'interface de BANTUDEVLAB applique rigoureusement les principes de design panafricain souverain :

- **Système d'Icônes SVG Sans Emoji :** Balises de gabarit Django dédiées `{% icon "nom" size=20 %}` et `{% flag "PAYS" %}` basées sur des vecteurs SVG hébergés en local (`apps/core/templatetags/icons.py`).
- **Thème Github Primer :** Styles CSS Primer GitHub Dark et Light natifs sans dépendance à des CDN externes (`custom/public/assets/css/theme-github.css` et `static/css/style.css`).
- **Éditeur de Code Intégré :** CodeMirror local embarqué (`static/vendor/codemirror/`) pour la navigation et l'édition directe de code.
- **Cartographie Panafricaine :** Carte interactive des nœuds souverains africains sur `/metrics/` affichant la télémétrie des centres de calcul.

---

## Tests, CI/CD et Qualité

Le projet applique une politique d'assurance qualité stricte validée automatiquement sur la suite de tests unitaires et d'intégration :

- **Couverture réelle démontrée :** **95,78 %** mesurée sur les modules clés (`apps/zkp_auth`, `apps/security_scanner`, `apps/ai_assistant`) avec 204 tests collectés (201 exécutés avec succès, 3 tests E2E ignorés en environnement sans Chromium binaire).
- **Langues supportées et démontrées :** **4 langues** avec catalogues compilés complets (`.mo` / `.po`) : Français (`fr`), Anglais (`en`), Kiswahili (`sw`), Portugais (`pt`).
- **Garantie Zéro Dépendance Non Permissive :** Validation automatique en CI via `python scripts/check_licenses.py` garantissant 0 dépendance sous GPL/AGPL/LGPL.

```bash
# Verification stricte du formatage et du linting (Ruff)
ruff check .
ruff format --check .

# Analyse de securite statique du code applicatif (Bandit)
bandit -c pyproject.toml -r apps config

# Verification de conformite des licences CADEV 2026 (Art. 6)
python scripts/check_licenses.py

# Verification de l'absence totale d'emojis dans le code et les gabarits
python scripts/check_no_emoji.py

# Execution de la suite Pytest avec seuil de couverture strict >= 95% (reel: 95.78%)
pytest --cov=apps/zkp_auth --cov=apps/security_scanner --cov=apps/ai_assistant --cov-report=term-missing --cov-fail-under=95

# Execution de la suite de tests Django
python manage.py test tests -v 2
```

### Note Opérationnelle sur les Workflows Gitea Actions « En attente »

Sur l'instance Gitea souveraine, 4 workflows peuvent apparaître en statut **« En attente »** (*Waiting*) :
- **Cause racine :** Gitea Actions fonctionne avec des runners auto-hébergés (`act_runner`). Contrairement à GitHub qui fournit des machines virtuelles mutualisées, Gitea place les tâches en attente tant qu'aucun runner n'est connecté avec le label correspondant (`ubuntu-latest`).
- **Correctif opérationnel :**
  1. Générer un jeton d'enregistrement sur Gitea : *Administration du site > Actions > Runners > Nouveau Runner*.
  2. Renseigner la variable `GITEA_RUNNER_REGISTRATION_TOKEN` dans `.env.production`.
  3. Lancer le conteneur act-runner prévu dans `docker-compose.yml` :
     ```bash
     docker compose up -d act_runner
     ```
  4. Dès connexion du conteneur au socket Docker, les tâches en attente sont immédiatement dépilées et exécutées.

---

## Outils Utilisés

Le développement de BantuDevLab s'appuie sur des éditeurs de code assistés par IA (Antigravity IA, Jules IA), un outil d'aide à la rédaction et planification (Claude IA), et GitHub pour le versionnement du code source. Le modèle local Gemma 2 2B est un composant applicatif intégré au produit final et non un outil de développement. Pour le détail exhaustif des interventions et la déclaration réglementaire de l'Article 6, se référer à [`CADEV26/SOUMISSION.md`](CADEV26/SOUMISSION.md).

---

## Index de la Documentation

| Thématique | Fichier de Documentation | Description |
|---|---|---|
| **Architecture** | [`docs/architecture.md`](docs/architecture.md) | Principes d'architecture logicielle et décisions techniques (ADR) |
| **Exploitation** | [`docs/operations.md`](docs/operations.md) | Runbook de production, procédures de sauvegarde et restauration |
| **Menaces** | [`docs/security/threat-model.md`](docs/security/threat-model.md) | Analyse méthodique des vecteurs de menaces selon le modèle STRIDE |
| **Cryptographie** | [`docs/security/crypto-spec.md`](docs/security/crypto-spec.md) | Spécifications mathématiques du protocole ZKP Schnorr / Fiat-Shamir |
| **Guide & FAQ** | [`docs/guide-utilisation-faq.md`](docs/guide-utilisation-faq.md) | Guide pratique des utilisateurs, création de compte et FAQ |
| **Audit des 20 Cycles** | [`docs/SOVEREIGN_GITHUB_FORGE_COMPLETE_REVIEW.md`](docs/SOVEREIGN_GITHUB_FORGE_COMPLETE_REVIEW.md) | Bilan exhaustif de la transition GitHub vers Gitea Souverain |
| **CLI tea** | [`docs/TEA_CLI_GUIDE.md`](docs/TEA_CLI_GUIDE.md) | Manuel d'utilisation du CLI souverain tea (équivalent GitHub CLI `gh`) |
| **Registres Paquets** | [`docs/MULTI_LANGUAGE_PACKAGE_REGISTRIES.md`](docs/MULTI_LANGUAGE_PACKAGE_REGISTRIES.md) | Registres de paquets multi-écosystèmes (PyPI, npm, Maven, Cargo) |
| **Conteneurs OCI** | [`docs/CONTAINER_REGISTRY.md`](docs/CONTAINER_REGISTRY.md) | Configuration et utilisation du registre de conteneurs OCI |
| **Pages Statiques** | [`docs/SOVEREIGN_PAGES_GUIDE.md`](docs/SOVEREIGN_PAGES_GUIDE.md) | Déploiement de sites statiques souverains (équivalent GitHub Pages) |
| **Recherche de Code** | [`docs/SOVEREIGN_CODE_SEARCH.md`](docs/SOVEREIGN_CODE_SEARCH.md) | Recherche plein texte avec le moteur Bleve et qualificateurs |
| **Attestation SLSA** | [`docs/SOVEREIGN_RELEASE_INTEGRITY.md`](docs/SOVEREIGN_RELEASE_INTEGRITY.md) | Intégrité cryptographique et génération d'attestations de provenance |
| **SBOM & Graphe** | [`docs/SOVEREIGN_DEPENDENCY_GRAPH_SBOM.md`](docs/SOVEREIGN_DEPENDENCY_GRAPH_SBOM.md) | Export CycloneDX v1.5 et cartographie des dépendances logicielles |
| **File de Fusion** | [`docs/SOVEREIGN_MERGE_QUEUE.md`](docs/SOVEREIGN_MERGE_QUEUE.md) | Architecture et fonctionnement de la file de fusion automatisée |
| **Rôles Organisation** | [`docs/SOVEREIGN_ORG_ROLES.md`](docs/SOVEREIGN_ORG_ROLES.md) | Spécification de la matrice des 5 rôles d'équipe et privilèges |
| **Avis de Sécurité** | [`docs/SOVEREIGN_SECURITY_ADVISORIES.md`](docs/SOVEREIGN_SECURITY_ADVISORIES.md) | Publication et traitement confidentiel des avis de sécurité |
| **Notes de Version** | [`docs/SOVEREIGN_RELEASE_NOTES.md`](docs/SOVEREIGN_RELEASE_NOTES.md) | Spécification du générateur de notes de version automatique |
| **Fédération SSO** | [`docs/SOVEREIGN_ZKP_SSO_BRIDGE.md`](docs/SOVEREIGN_ZKP_SSO_BRIDGE.md) | Pont d'authentification Zero-Trust ZKP et fédération SSO |
| **Supervision** | [`docs/SOVEREIGN_BACKUPS_AND_METRICS.md`](docs/SOVEREIGN_BACKUPS_AND_METRICS.md) | Sauvegardes automatisées et métriques Prometheus |
| **Codespaces Web** | [`docs/SOVEREIGN_CODESPACES_IDE.md`](docs/SOVEREIGN_CODESPACES_IDE.md) | IDE en ligne souverain conteneurisé (équivalent GitHub Codespaces) |
| **Discussions** | [`docs/SOVEREIGN_DISCUSSIONS.md`](docs/SOVEREIGN_DISCUSSIONS.md) | Espace communautaire de discussions et échanges techniques |
| **Snippets Gist** | [`docs/SOVEREIGN_GIST_SNIPPETS.md`](docs/SOVEREIGN_GIST_SNIPPETS.md) | Partage de bribes de code souverain (équivalent GitHub Gist) |
| **Rulesets Branches** | [`docs/SOVEREIGN_BRANCH_RULESETS.md`](docs/SOVEREIGN_BRANCH_RULESETS.md) | Règles fines de protection de branches et revues obligatoires |
| **Pitch Officiel** | [`docs/pitch-cadev-2026.md`](docs/pitch-cadev-2026.md) | Présentation de référence pour la conférence CADEV 2026 |
| **Déploiement Docker**| [`docker-deployment.md`](docker-deployment.md) | Guide complet de démarrage conteneurisé en 1 commande |
| **Intervention Gitea (Archivée)** | [`docs/archive/intervention.md`](docs/archive/intervention.md) | Guide d'intervention, topologie et accès de la forge Gitea |
| **Audit UX & Design** | [`develop-design.md`](develop-design.md) | Analyse critique de l'expérience utilisateur et du design system |
| **Backlog Améliorations (Archivé)**| [`docs/archive/backlod.md`](docs/archive/backlod.md) | Suivi des améliorations et priorisation technique |
| **Contribution** | [`CONTRIBUTING.md`](CONTRIBUTING.md) | Directives pour les contributeurs au code source |
| **Changelog** | [`CHANGELOG.md`](CHANGELOG.md) | Historique exhaustif des versions et évolutions |
| **Sécurité** | [`SECURITY.md`](SECURITY.md) | Politique de divulgation responsable des vulnérabilités |
