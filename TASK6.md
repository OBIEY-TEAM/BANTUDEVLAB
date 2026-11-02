# TASK6.md — Feuille de Route & Spécifications Opérationnelles : Transformation de Gitea vers l'Expérience GitHub Actuel

Ce document définit l'ensemble des tâches, sous-tâches techniques et configurations nécessaires pour aligner l'instance Gitea de **BANTUDEVLAB** sur l'apparence, l'ergonomie et les fonctionnalités du **GitHub moderne**, tout en préservant l'architecture souveraine (Zero-Trust ZKP, sécurité SAST, conformité panafricaine).

---

## Sommaire

1. [Matrice des Tâches et Sous-Tâches d'Implémentation](#matrice-des-tâches-et-sous-tâches-dimplémentation)
   - [Axe 1 : Design UI/UX et Thème Visuel GitHub Moderne](#axe-1--design-uiux-et-thème-visuel-github-moderne)
   - [Axe 2 : Moteur de CI/CD et Gitea Actions (Compatible GitHub Actions)](#axe-2--moteur-de-cicd-et-gitea-actions-compatible-github-actions)
   - [Axe 3 : Collaboration, Pull Requests et Gestion de Projet](#axe-3--collaboration-pull-requests-et-gestion-de-projet)
   - [Axe 4 : Sécurité du Code, Analyse et Dépendances](#axe-4--sécurité-du-code-analyse-et-dépendances)
   - [Axe 5 : Registres de Paquets et Artefacts](#axe-5--registres-de-paquets-et-artefacts)
   - [Axe 6 : Intégrations Tiers Écosystème GitHub (Pages, Codespaces, Gist, Discussions)](#axe-6--intégrations-tiers-écosystème-github-pages-codespaces-gist-discussions)
   - [Axe 7 : Administration, Synchronisation et SSO Souverain](#axe-7--administration-synchronisation-et-sso-souverain)
2. [Document de Référence : Équivalence Complète GitHub → Gitea](#document-de-référence--équivalence-complète-github--gitea)
   - [1. Gestion du code source](#1-gestion-du-code-source)
   - [2. Collaboration](#2-collaboration)
   - [3. Qualité et sécurité du code](#3-qualité-et-sécurité-du-code)
   - [4. CI/CD et automatisation](#4-cicd-et-automatisation)
   - [5. Paquets et artefacts](#5-paquets-et-artefacts)
   - [6. Hébergement et environnement de développement](#6-hébergement-et-environnement-de-développement)
   - [7. Authentification et administration](#7-authentification-et-administration)
   - [8. Apparence : se rapprocher du GitHub actuel](#8-apparence--se-rapprocher-du-github-actuel)
   - [9. Mise en route rapide](#9-mise-en-route-rapide)
   - [10. Checklist de migration GitHub → Gitea](#10-checklist-de-migration-github--gitea)
   - [11. Résumé](#11-résumé)

---

## Matrice des Tâches et Sous-Tâches d'Implémentation

### Axe 1 : Design UI/UX et Thème Visuel GitHub Moderne

- [x] **T-UI-601 : Déploiement du Thème GitHub (Light & Dark Dimmed / Dark High Contrast)**
  - [x] Déployer la feuille de style communautaire `theme-github.css` et `theme-github-dark.css` dans `custom/public/assets/css/`.
  - [x] Définir les variables CSS conformes aux tokens de conception GitHub Primer (`--color-canvas-default`, `--color-btn-primary-bg`, `--color-accent-fg`, `--color-border-default`).
  - [x] Configurer `custom/conf/app.ini` avec `THEMES = gitea-auto,gitea-light,gitea-dark,github,github-dark` et `DEFAULT_THEME = github`.
  - [x] Supporter la détection automatique du mode sombre du système d'exploitation (`prefers-color-scheme`).

- [x] **T-UI-602 : Surcharges de Gabarits (Templates Custom) pour Reproduire la Navigation GitHub**
  - [x] Créer `custom/templates/custom/header.tmpl` reproduisant la barre supérieure de navigation GitHub (logo octocat/bantu, barre de recherche globale avec raccourci `/`, menu déroulant contextuel, cloche de notifications).
  - [x] Personnaliser `custom/templates/repo/header.tmpl` pour reproduire l'en-tête de dépôt avec les onglets officiels (Code, Issues, Pull requests, Actions, Projects, Wiki, Security, Insights, Settings).
  - [x] Adapter la vue de lecture de code (`custom/templates/repo/view_file.tmpl`) avec la barre d'outils GitHub (boutons Raw, Blame, Historique, Copie rapide et bouton d'édition avec raccourci clavier `e`).
  - [x] Personnaliser le pied de page (`custom/templates/custom/footer.tmpl`) aux couleurs et typographies discrètes de GitHub.

- [x] **T-UI-603 : Typographie, Badges et Éléments Vectoriels**
  - [x] Configurer la pile de polices système GitHub (`-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif`).
  - [x] Remplacer les boutons et compteurs (Stars, Forks, Watch) par les styles arrondis avec bordures fines caractéristiques de GitHub.
  - [x] Adapter le visualiseur Markdown pour supporter les blocs d'alerte GitHub Flavored Markdown (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`).

---

### Axe 2 : Moteur de CI/CD et Gitea Actions (Compatible GitHub Actions)

- [x] **T-ACT-601 : Activation et Configuration Serveur de Gitea Actions**
  - [x] Activer le sous-système Actions dans `custom/conf/app.ini` :
    ```ini
    [actions]
    ENABLED = true
    DEFAULT_ACTIONS_URL = github
    ARTIFACT_RETENTION_DAYS = 90
    ```
  - [x] Configurer le stockage local ou S3/MinIO pour les artefacts de build et le cache des étapes de workflow.
  - [x] Assurer la rétro-compatibilité de lecture pour les deux dossiers `.gitea/workflows/` et `.github/workflows/`.

- [x] **T-ACT-602 : Déploiement et Enregistrement du Démon `act_runner`**
  - [x] Créer le service Docker Compose pour déployer `gitea/act_runner:latest`.
  - [x] Enregistrer le runner au niveau de l'instance ou de l'organisation via un jeton d'enregistrement (`GITEA_RUNNER_REGISTRATION_TOKEN`).
  - [x] Définir les étiquettes (labels) d'images système compatibles :
    - `ubuntu-latest:docker://node:20-bookworm` ou `catthehacker/ubuntu:act-latest`
    - `ubuntu-22.04:docker://catthehacker/ubuntu:act-22.04`
    - `ubuntu-20.04:docker://catthehacker/ubuntu:act-20.04`
  - [x] Durcir l'exécution du runner pour isoler le socket Docker en environnement multi-locataire.

- [x] **T-ACT-603 : Compatibilité des Workflows et Actions du Marketplace**
  - [x] Tester les actions les plus courantes de la communauté GitHub (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`, `actions/upload-artifact@v3`).
  - [x] Configurer un proxy de mise en cache local pour éviter les limitations de débit de l'API publique GitHub.
  - [x] Mettre en place la gestion unifiée des secrets et variables au niveau dépôt, organisation et instance globale.

---

### Axe 3 : Collaboration, Pull Requests et Gestion de Projet

- [x] **T-COL-601 : Pull Requests et Mécanismes de Revue Approfondie**
  - [x] Configurer les règles de protection de branche par dépôt (revues obligatoires, commits signés, statuts CI exigés avant fusion).
  - [x] Activer le support du fichier `CODEOWNERS` dans la racine ou le dossier `.gitea/`.
  - [x] Prendre en charge les formulaires de pull request via `.gitea/PULL_REQUEST_TEMPLATE.md` et `.gitea/PULL_REQUEST_TEMPLATE/`.
  - [x] Activer les différentes stratégies de fusion (Merge commit, Rebase, Squash, Rebase + fast-forward).

- [x] **T-COL-602 : Gestion Avancée des Issues et Formulaires Structurés (Issue Forms)**
  - [x] Déployer les templates de tickets basés sur des schémas YAML (`.gitea/ISSUE_TEMPLATE/*.yaml`) avec champs typés, listes déroulantes et cases à cocher.
  - [x] Organiser les jalons (Milestones), labels hiérarchisés et affectations multiples.
  - [x] Configurer le tableau de bord Kanban (Projets Gitea) pour émuler la vue Board de GitHub Projects.

- [x] **T-COL-603 : Recherche Globale et Indexation de Code**
  - [x] Configurer le moteur d'indexation de code interne (Bleve ou Elasticsearch/Meilisearch) dans `app.ini` :
    ```ini
    [indexer]
    ISSUE_INDEXER_TYPE = bleve
    REPO_INDEXER_ENABLED = true
    REPO_INDEXER_TYPE = bleve
    MAX_FILE_SIZE = 1048576
    ```
  - [x] Assurer la recherche instantanée de symboles, fonctions et mots-clés dans l'ensemble des dépôts indexés.

---

### Axe 4 : Sécurité du Code, Analyse et Dépendances

- [x] **T-SEC-601 : Pipeline d'Analyse SAST et Secrets (Équivalent CodeQL / Secret Scanning)**
  - [x] Intégrer un workflow Gitea Actions automatisé exécutant **Semgrep** et le scanner souverain BantuDevLab sur chaque commit et pull request.
  - [x] Intégrer **Gitleaks** ou **TruffleHog** dans les étapes de validation pre-receive ou CI pour bloquer la fuite de secrets et tokens.
  - [x] Générer et ingérer les rapports de vulnérabilité au format SARIF standardisé.

- [x] **T-SEC-602 : Analyse des Dépendances et Mises à Jour Automatisées (Équivalent Dependabot)**
  - [x] Déployer un conteneur dédié **Renovate** configuré pour sonder périodiquement l'instance Gitea.
  - [x] Automatiser l'ouverture de pull requests de mise à jour des dépendances vulnérables ou obsolètes (Python, Node.js, Go, Docker).
  - [x] Intégrer **Trivy** et **OSV-Scanner** pour la vérification du graphe des dépendances.

- [ ] **T-SEC-603 : Sécurité des Accès et Authentification Forte**
  - [ ] Activer l'authentification à deux facteurs (2FA) via TOTP et clés de sécurité matérielles WebAuthn/FIDO2.
  - [ ] Vérifier la signature cryptographique des commits via clés GPG et SSH avec affichage du badge « Verified ».

---

### Axe 5 : Registres de Paquets et Artefacts

- [ ] **T-PKG-601 : Registre de Conteneurs OCI / Docker (Équivalent ghcr.io)**
  - [ ] Activer le registre de conteneurs dans `app.ini` :
    ```ini
    [packages]
    ENABLED = true
    ```
  - [ ] Permettre le push et pull d'images Docker via `docker login <domaine>` et l'authentification par jeton d'accès.

- [ ] **T-PKG-602 : Registres de Dépendances Multi-Langages**
  - [ ] Valider le support des registres natifs : PyPI, npm, Maven/Gradle, NuGet, Cargo, Composer, Go, Helm, Debian, RPM.
  - [ ] Configurer les quotas de stockage et les politiques de rétention des versions d'artefacts.

---

### Axe 6 : Intégrations Tiers Écosystème GitHub (Pages, Codespaces, Gist, Discussions)

- [ ] **T-EXT-601 : Publication de Sites Statiques (Équivalent GitHub Pages)**
  - [ ] Mettre en place un pipeline Gitea Actions déployant les sites statiques générés (HTML/Hugo/Jekyll) vers un conteneur Nginx dédié ou intégrer le serveur Pages de Codeberg (`codeberg-pages`).
  - [ ] Configurer la gestion automatique des certificats TLS pour les sous-domaines de projets.

- [ ] **T-EXT-602 : Environnements de Développement Web (Équivalent GitHub Codespaces)**
  - [ ] Déployer une instance auto-hébergée de **Coder**, **DevPod** ou **code-server** connectée à Gitea via OAuth2.
  - [ ] Ajouter un bouton personnalisé « Ouvrir dans l'IDE Web » dans l'en-tête de dépôt via `custom/templates/repo/header.tmpl`.

- [ ] **T-EXT-603 : Partage de Snippets de Code (Équivalent GitHub Gist)**
  - [ ] Déployer **Opengist** en conteneur Docker interconnecté avec le SSO Gitea.
  - [ ] Fournir un lien direct dans la navigation principale vers le service de snippets.

- [ ] **T-EXT-604 : Espace d'Échange Communautaire (Équivalent GitHub Discussions)**
  - [ ] Utiliser des labels d'issues dédiés (`type/discussion`) couplés à des templates, ou intégrer une instance **Discourse** auto-hébergée avec authentification OAuth2 déléguée à Gitea.

---

### Axe 7 : Administration, Synchronisation et SSO Souverain

- [ ] **T-ADM-701 : Intégration CLI Officielle `tea` (Équivalent `gh`)**
  - [ ] Documenter et configurer l'outil CLI officiel `tea` pour la gestion des dépôts, issues, pull requests et releases depuis le terminal des développeurs.

- [ ] **T-ADM-702 : Pont d'Authentification Zero-Trust ZKP et OAuth2/OIDC**
  - [ ] Connecter Gitea à l'API BantuDevLab ZKP en tant que fournisseur d'identité OAuth2/OIDC.
  - [ ] Permettre la synchronisation automatique des équipes et permissions d'organisations.

- [ ] **T-ADM-703 : Sauvegardes Automatisées et Supervision Industrielle**
  - [ ] Automatiser la tâche quotidienne `gitea dump` avec chiffrement GPG des archives de configuration, base de données et dépôts Git.
  - [ ] Exposer les métriques Prometheus de Gitea (`/metrics`) vers la pile d'observabilité Grafana.

---

# Équivalence complète GitHub → Gitea

> Document de référence : pour chaque fonctionnalité de GitHub, son équivalent dans Gitea, son statut et la marche à suivre.
> Les fonctionnalités évoluent vite : vérifiez toujours la documentation de **votre version** de Gitea (https://docs.gitea.com).

**Légende des statuts**

| Statut | Signification |
|---|---|
| ✅ Natif | Disponible dans Gitea sans outil supplémentaire |
| 🟡 Partiel | Disponible, mais avec des différences ou des limites |
| 🔧 Tiers | Pas de fonction native, à compléter avec un outil externe |
| ❌ Absent | Aucun équivalent direct |

---

## 1. Gestion du code source

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| Dépôts publics / privés | Dépôts publics / privés | ✅ Natif | Visibilité réglable par dépôt et par organisation |
| Fork | Fork | ✅ Natif | |
| Stars / Watch | Stars / Watch | ✅ Natif | |
| Dépôts modèles (template repository) | Dépôts modèles | ✅ Natif | Case « Modèle » dans les paramètres du dépôt |
| Git LFS | Git LFS | ✅ Natif | À activer côté serveur (`[server] LFS_START_SERVER = true`) |
| Miroirs de dépôts | Miroirs push / pull | ✅ Natif | Utile pour synchroniser avec GitHub |
| Migration depuis une autre forge | Migration (GitHub, GitLab, Gogs, Gitea, etc.) | ✅ Natif | Peut importer tickets, PR, labels, jalons, releases, wiki |
| Releases et tags | Releases et tags | ✅ Natif | Pièces jointes supportées |
| Signature de commits (GPG / SSH) | GPG / SSH | ✅ Natif | Badge « Vérifié » affiché |
| Deploy keys | Clés de déploiement | ✅ Natif | |
| Recherche de code | Indexeur de code | ✅ Natif | Bleve (défaut) ou Elasticsearch / Meilisearch selon version |
| Dépôts archivés | Archivage | ✅ Natif | |

## 2. Collaboration

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| Pull Requests | Pull Requests | ✅ Natif | Revues, commentaires en ligne, suggestions |
| Pull Requests en brouillon (Draft) | Préfixe `WIP:` / `Draft:` dans le titre | 🟡 Partiel | Pas de vrai statut « brouillon » identique à GitHub |
| Modes de fusion (merge, squash, rebase) | Merge, rebase, rebase + merge, squash, fast-forward only | ✅ Natif | |
| Auto-merge | Fusion automatique quand les contrôles réussissent | ✅ Natif | |
| Merge queue | — | ❌ Absent | À contourner par des règles de protection de branche strictes |
| Issues | Tickets (issues) | ✅ Natif | Labels, jalons, assignations, dépendances, suivi du temps |
| Formulaires de tickets (issue forms YAML) | Issue forms YAML | ✅ Natif | Dossier `.gitea/ISSUE_TEMPLATE/` (ou `.github/`) |
| Templates de PR | `PULL_REQUEST_TEMPLATE.md` | ✅ Natif | Dossier `.gitea/` ou `.github/` |
| GitHub Projects | Projets (tableaux Kanban) | 🟡 Partiel | Moins riche (pas de vues Table / Roadmap, pas de champs personnalisés) |
| Milestones | Jalons | ✅ Natif | |
| Labels | Labels | ✅ Natif | Labels d'organisation supportés |
| Wiki | Wiki | ✅ Natif | Dépôt Git séparé |
| GitHub Discussions | — | ❌ Absent | Alternatives : tickets avec label, wiki, ou Discourse |
| Réactions, mentions, Markdown | Réactions, mentions, Markdown | ✅ Natif | Mermaid, LaTeX et listes de tâches supportés |
| Notifications | Notifications | ✅ Natif | Web et e-mail |
| Organisations et équipes | Organisations et équipes | ✅ Natif | Permissions par équipe et par unité (code, tickets, PR, etc.) |
| GitHub Sponsors | — | ❌ Absent | |

## 3. Qualité et sécurité du code

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| Protection de branches | Protection de branches | ✅ Natif | Revues obligatoires, statuts requis, liste blanche de push, commits signés |
| Rulesets | — | ❌ Absent | Gitea utilise des règles de protection par motif de branche |
| CODEOWNERS | CODEOWNERS | ✅ Natif | Selon version récente |
| Protection des tags | Protection des tags | ✅ Natif | |
| Dependabot (mises à jour) | — | 🔧 Tiers | **Renovate** (compatible Gitea) |
| Dependabot alerts / Dependency graph | — | 🔧 Tiers | Trivy, OSV-Scanner, Renovate |
| Code scanning (CodeQL) | — | 🔧 Tiers | Semgrep, SonarQube, Trivy dans les pipelines |
| Secret scanning | — | 🔧 Tiers | Gitleaks, TruffleHog dans les pipelines ou en pre-commit |
| Security advisories | — | ❌ Absent | Utiliser des tickets confidentiels / un processus interne |
| Authentification à deux facteurs | TOTP et WebAuthn | ✅ Natif | Peut être rendue obligatoire |

## 4. CI/CD et automatisation

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| GitHub Actions | Gitea Actions | 🟡 Partiel | Syntaxe YAML très proche ; certaines actions et contextes diffèrent |
| Runners hébergés par GitHub | — | ❌ Absent | Vous hébergez vos propres runners |
| Runners auto-hébergés | `act_runner` | ✅ Natif | Docker, hôte ou LXC ; enregistrement par jeton |
| Workflows dans `.github/workflows/` | `.gitea/workflows/` ou `.github/workflows/` | ✅ Natif | Les deux dossiers sont lus |
| Secrets et variables | Secrets et variables | ✅ Natif | Niveaux utilisateur, organisation et dépôt |
| Actions du Marketplace | Actions depuis GitHub ou une instance configurée | 🟡 Partiel | Paramètre `DEFAULT_ACTIONS_URL` ; pas de Marketplace propre |
| Artefacts | Artefacts | 🟡 Partiel | Selon version, `upload-artifact` / `download-artifact` v4 peuvent ne pas être supportés : tester la v3 |
| Cache d'actions | Cache | ✅ Natif | |
| Workflows réutilisables / actions composites | Supportés selon version | 🟡 Partiel | À tester sur votre version |
| Environments et protections de déploiement | — | 🟡 Partiel | Fonctionnalité limitée par rapport à GitHub |
| Webhooks | Webhooks | ✅ Natif | Slack, Discord, Matrix, Telegram, Teams, etc. |

## 5. Paquets et artefacts

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| GitHub Packages | Package Registry | ✅ Natif | Activé par défaut |
| Docker / OCI (ghcr.io) | Registre de conteneurs | ✅ Natif | `docker login <votre-domaine>` |
| npm | npm | ✅ Natif | |
| PyPI | PyPI | ✅ Natif | |
| Maven / Gradle | Maven | ✅ Natif | |
| NuGet | NuGet | ✅ Natif | |
| RubyGems | RubyGems | ✅ Natif | |
| Cargo, Composer, Go, Helm, Debian, RPM, Alpine, Generic, etc. | Supportés | ✅ Natif | Liste exacte selon version |

## 6. Hébergement et environnement de développement

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| GitHub Pages | — | 🔧 Tiers | Serveur Pages tiers (ex. celui de Codeberg) ou déploiement via Actions vers Nginx |
| Codespaces | — | 🔧 Tiers | Coder, DevPod, code-server auto-hébergés |
| GitHub Copilot | — | 🔧 Tiers | Assistants IA auto-hébergés (ex. Tabby, Continue) |
| Gist | — | 🔧 Tiers | Opengist (auto-hébergé) |
| GitHub CLI (`gh`) | `tea` | 🟡 Partiel | CLI officielle de Gitea |
| API REST | API REST (Swagger intégré) | ✅ Natif | `/api/swagger` |
| API GraphQL | — | ❌ Absent | |
| GitHub Apps / OAuth Apps | Applications OAuth2 | 🟡 Partiel | Pas de modèle « GitHub App » complet |

## 7. Authentification et administration

| GitHub | Gitea | Statut | Notes |
|---|---|---|---|
| SSO (SAML / OIDC) | OAuth2, OpenID Connect, LDAP | ✅ Natif | SAML selon version |
| Connexion via GitHub, Google, etc. | Fournisseurs OAuth2 externes | ✅ Natif | |
| Gestion des utilisateurs et quotas | Panneau d'administration | ✅ Natif | |
| Audit log | Journaux système | 🟡 Partiel | Moins détaillé que l'audit log GitHub Enterprise |
| Insights (graphiques) | Activité, contributeurs, fréquence de code | 🟡 Partiel | Moins complet |
| Sauvegarde | `gitea dump` | ✅ Natif | |

## 8. Apparence : se rapprocher du GitHub actuel

| Objectif | Méthode |
|---|---|
| Palette claire / sombre de GitHub | Thème CSS communautaire (ex. `gitea-github-theme`) |
| Thème automatique selon le système | Thème `gitea-auto` natif |
| Navigation, icônes, pied de page, tableau de bord | Surcharge de templates dans `custom/templates/` |
| Logo, favicon | `custom/public/assets/img/` |
| Ne jamais modifier les fichiers système | Tout passe par `custom/` pour survivre aux mises à jour |

### Activer un thème dans `app.ini`

```ini
[ui]
THEMES = gitea-auto,gitea-light,gitea-dark,github
DEFAULT_THEME = github
```

Le fichier CSS se place dans `custom/public/assets/css/` et son nom doit suivre la convention `theme-<nom>.css` pour votre version.

## 9. Mise en route rapide

### Activer Gitea Actions

```ini
[actions]
ENABLED = true
```

### Lancer un `act_runner` avec Docker Compose

```yaml
services:
  runner:
    image: gitea/act_runner:latest
    restart: always
    environment:
      GITEA_INSTANCE_URL: https://git.votre-domaine.com
      GITEA_RUNNER_REGISTRATION_TOKEN: <jeton>
      GITEA_RUNNER_NAME: runner-1
    volumes:
      - ./data:/data
      - /var/run/docker.sock:/var/run/docker.sock
```

> Montez le socket Docker avec prudence : il donne un accès élevé à l'hôte. Pour des dépôts non fiables, préférez un runner isolé.

### Exemple de workflow

```yaml
# .gitea/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Tests ici"
```

## 10. Checklist de migration GitHub → Gitea

- [ ] Installer Gitea et configurer `app.ini` (domaine, base de données, SMTP)
- [ ] Activer HTTPS (reverse proxy Nginx ou Caddy)
- [ ] Configurer l'authentification (OIDC / LDAP) et la 2FA
- [ ] Migrer les dépôts (tickets, PR, releases, wiki inclus)
- [ ] Installer le thème et les templates personnalisés
- [ ] Activer Actions et enregistrer un `act_runner`
- [ ] Adapter les workflows (`.gitea/workflows/`) et tester les actions utilisées
- [ ] Configurer la protection des branches et `CODEOWNERS`
- [ ] Activer le Package Registry et migrer les images / paquets
- [ ] Ajouter Renovate, Trivy / Semgrep et Gitleaks
- [ ] Prévoir une solution pour Pages, Codespaces et Gist si nécessaire
- [ ] Planifier les sauvegardes (`gitea dump`) et la supervision

## 11. Résumé

| Domaine | Couverture par rapport à GitHub |
|---|---|
| Code, PR, tickets, wiki, releases | Très proche |
| Actions et paquets | Proche, avec adaptations |
| Sécurité avancée (CodeQL, Dependabot, secret scanning) | À compléter avec des outils tiers |
| Pages, Codespaces, Copilot, Gist, Discussions, Sponsors | Pas d'équivalent natif |
| Apparence | Très proche grâce aux thèmes et à `custom/` |
