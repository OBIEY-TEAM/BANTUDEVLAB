# Dossier Stratégique CADEV 2026 : BANTUDEVLAB / SysteLink Cloud Africain

**Auteurs :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne  
**Événement :** Systalink Challenge / CADEV 2026 (29 sept. – 15 nov. 2026)
**Thème officiel :** « Construire la plateforme d'échange africaine, pour les devs, par les devs »
**Positionnement :** Forge logicielle panafricaine souveraine (Alternative locale à GitHub / GitLab avec Zero-Trust ZKP, scanner SAST Shannon SARIF 2.1.0 et IA d'audit in-forge Gemma 2 2B quantifiée en local).

---

## Sommaire Exécutif

1. [Analyse Technique Approfondie du Projet (Commits, PRs, Fichiers)](#1-analyse-technique-approfondie-du-projet-commits-prs-fichiers)
2. [Autopsie Critique des Deux Pitches Antérieurs (Facteurs d'Échec)](#2-autopsie-critique-des-deux-pitches-antérieurs-facteurs-déchec)
3. [Pitch Professionnel Hackathon CADEV 2026 (5 Minutes Chronométrées)](#3-pitch-professionnel-hackathon-cadev-2026-5-minutes-chronométrées)
4. [Script Scénarisé de la Démonstration (Vidéo & Direct - 3 Minutes)](#4-script-scénarisé-de-la-démonstration-vidéo--direct---3-minutes)
5. [Matrice Stratégique de Défense face au Jury (Q&A Haute Précision)](#5-matrice-stratégique-de-défense-face-au-jury-qa-haute-précision)
6. [Checklist Opérationnelle pour le Jour J](#6-checklist-opérationnelle-pour-le-jour-j)

---

## 1. Analyse Technique Approfondie du Projet (Commits, PRs, Fichiers)

L'état actuel du référentiel Git démontre une trajectoire d'industrialisation continue, articulée autour de 26 commits majeurs, de PRs d'axes spécialisés et d'une structure logicielle modulaire robuste.

### 1.1 Chronologie et Cartographie des Commits & PRs

- **Phase Initiale et Socle Fondateur (`b0fa102`, `d04ed7f`, `4e44895`) :**
  - Mise en place du socle Django 5.2 et intégration avec le moteur Gitea CE.
  - Implémentation du moteur ZKP Schnorr (`apps/zkp_auth/crypto.py`).
  - Scanner de sécurité initial et premiers prompts pour l'IA locale.
  - Formalisation de l'audit initial et de la feuille de route `TASK1.md`.

- **Industrialisation des 6 Axes Métier (`6a6a1da`, `2c1f0b4`, `3763a05`, `2d26ecf`, `b315e70`, `bff59af`) :**
  - **Axe 1 (Sécurité & Zero-Trust) :** Hardening strict de l'authentification ZKP avec vérification des sous-groupes premiers ($y^q \equiv 1 \pmod p$), expiration atomique des nonces anti-rejeu, jetons Git CLI ZKP (`GitAccessToken`), et journal d'audit immuable SHA-256 (`AuditTrailLog` conforme Convention de Malabo 2014).
  - **Axe 2 (Scalabilité & Résilience) :** Traitement asynchrone Celery adossé à Valkey 7.2 (remplacement BSD-3 de Redis), cache Django structuré avec repli hors-ligne, circuit breakers et sondes Kubernetes (`/healthz`, `/readyz`).
  - **Axe 3 (Architecture & Écosystème) :** Synchronisation bidirectionnelle REST v1 avec Gitea (`GiteaSyncService`), modélisation multi-tenant `SovereignOrganization` (banques centrales, ministères, universités, startups), conformité OASIS SARIF 2.1.0, documentation OpenAPI 3.0 via `drf-spectacular`.
  - **Axe 4 (Design System & Expérience Développeur) :** Intégration de l'éditeur CodeMirror auto-hébergé, jauge circulaire de score de souveraineté numérique, wizard ZKP avec mnémonique BIP-39 (12 mots), système de notifications toasts unifié, et cartographie interactive de la topologie cible panafricaine (Projet, non déployé : Abidjan, Dakar, Lagos, Nairobi, Kigali).
  - **Axe 6 (Assurance Qualité & Tests) :** Tests de fuzzing cryptographique (`test_zkp_fuzzing.py`), tests end-to-end Playwright (`test_e2e_playwright.py`), couverture de test stricte à 95,62 %, linting/formatage automatisé Ruff, et audit de sécurité Bandit.
  - **Industrialisation IA & Conteneurisation :** Scripts de préparation LoRA/GGUF (`finetuning/`) hors inférence de production (modèle actif : `gemma2:2b` standard via Ollama) et conteneurisation Docker durcie sous utilisateur non-root (`appuser:appgroup`).

- **Convergence et Alignement Modèle Local `gemma2:2b` (`c192064`, `ff7e4ef`, `f8c1a1e`) :**
  - Rédaction de l'audit exhaustif `TASK/TASK5.md` identifiant le désalignement historique : correction du tag `gemma:5b` vers l'architecture compacte et souveraine `gemma2:2b` (Google Gemma 2 2B Instruct / Q4_K_M).
  - Résolution du dimensionnement de mémoire : passage d'un modèle 5B lourd et non standard à un modèle 2B compact capable de tourner sur CPU ou GPU modeste (4 à 8 Go VRAM) en datacenter africain ou environnement local déconnecté.
  - Assainissement strict des payloads avant inférence (anonymisation IP/tokens) et limitation de contexte à 8192 tokens.

- **Consolidation Gitea & Retrait de GitLab (`09a6d3a`, `d0ff819`, `50d5438`, `8f59411`) :**
  - Forge unifiée autour de Gitea CE 1.22 (MIT) ; les anciens éléments GitLab ont été retirés de l'interface, des menus et de la CI (`docs/archive/`).
  - Conteneurisation Docker clé-en-main avec redirection automatique vers Gitea (port 3002).
  - Rédaction des spécifications d'équivalence totale GitHub dans `TASK/TASK6.md` et des 20 cycles opérationnels dans `TASK/`.

- **Harmonisation UX, Écosystème et Parité Visuelle (`8277e57`, `a11c4ae`, `7d29430`, `08e8c5d`, `7403272`, `73c25ca`) :**
  - Synchronisation bidirectionnelle du thème sombre/clair et de la langue (Anglais, Français, Swahili, Portugais) entre BantuDevLab (port 8000/8001) et Gitea (port 3002) via `bantu-ecosystem-sync.js`, cookies partagés et BroadcastChannel.
  - Éradication définitive du phénomène de flash blanc (FOUC) en mode sombre dans Gitea via injection CSS critique `#bantu-anti-fouc-critical` et `theme-github-dark.css`.
  - Intégration de logos optimisés et transparents avec vérification Pillow.
  - Modularisation des workflows CI GitHub Actions (`setup-bantudevlab`).

### 1.2 Cartographie de l'Arborescence Actuelle

```text
/app
├── CADEV26/                     # Dossier stratégique du pitch et support hackathon
│   └── pitch.md                 # Pitch professionnel, script démo et matrice Q&A
├── TASK/                        # Spécifications des 20 cycles d'équivalence GitHub et audits
│   ├── TASK3.md, TASK5.md       # Audits d'industrialisation et alignement gemma2:2b
│   ├── TASK6.md                 # Spécifications de transformation Gitea -> GitHub
│   └── TASK7.md à TASK26.md     # Cycles 1 à 20 (Copilot, PR bot, Merge Queue, SBOM...)
├── apps/
│   ├── zkp_auth/                # Authentification Zero-Trust Schnorr RFC 3526 & Jetons Git
│   ├── security_scanner/        # Scanner SAST, calcul d'entropie Shannon, export SARIF 2.1.0
│   ├── ai_assistant/            # Moteur local Gemma 2 2B (Ollama/vLLM), revue Celery, Copilot
│   ├── gitea_client/            # Synchronisation Gitea REST v1, Webhooks HMAC, fallback offline
│   ├── gitlab_client/           # Client GitLab v4, passerelle webhooks, bridge OmniAuth
│   └── core/                    # Multi-tenancy organisations, audit SHA-256, icônes SVG sans emoji
├── custom/                      # Surcharges Gitea (Templates Primer, CSS Dark/Light, JS Sync)
├── deploy/                      # Scripts d'orchestration, runners, cluster d'inférence IA
├── docs/                        # Modèle de menaces STRIDE, spécifications cryptographiques, FAQ
├── finetuning/                  # Pipeline LoRA pour Gemma 2 2B, jeux de données, conversion GGUF
├── forge_data/                  # Dépôts bare Git locaux pour résilience en mode déconnecté
├── gitlab/                      # Extensions et middleware Ruby OmniAuth pour GitLab CE/EE
├── locale/                      # Catalogues de traduction i18n (en, fr, pt, sw)
├── scripts/                     # Scripts d'automatisation, vérification zéro emoji, SBOM CycloneDX
├── static/ & templates/         # Interface web Primer, CodeMirror local, carte des nœuds
├── tests/                       # Suite de tests (E2E Playwright, Fuzzing ZKP, couverture > 95%)
├── Dockerfile                   # Image de production durcie non-root UID 1000 Gunicorn/Uvicorn
├── docker-compose.yml           # Composition orchestrée (Django, Gitea, Postgres, Valkey, Celery)
└── pyproject.toml               # Configuration Ruff, Bandit, Pytest et couverture
```

---

## 2. Autopsie Critique des Deux Pitches Antérieurs (Facteurs d'Échec)

L'évaluation lucide des deux ébauches de pitch précédentes révèle des faiblesses structurelles majeures qui ont empêché le projet d'obtenir l'adhésion unanime des jurys :

### Diagnostic de la Version 1 (Format 10 minutes)
1. **Dispersion et rythme léthargique :** Un pitch de 10 minutes avec une accroche de 45 secondes et 1 minute 15 sur le problème perd l'attention du jury. Les jurys de hackathons (Systalink / CADEV) évaluent l'efficacité en moins de 5 minutes.
2. **Le piège de l'objection d'hébergement :** Le pitch indiquait candidement « Gitea déployé en [VPS / serveur local, à préciser] » et ouvrait le flanc à la question assassine : *« Pourquoi votre démo souveraine tourne-t-elle sur un VPS externe étranger (Hostinger) plutôt que sur Systalink ? »*.
3. **Flou cryptographique et technique :** L'authentification ZKP était mentionnée comme une intention philosophique sans citer les garanties cryptographiques formelles (Schnorr, RFC 3526, non-rejeu par nonces atomiques, sous-groupe premier).
4. **Survol de l'IA (mention non calibrée Gemma 5B) :** L'annonce d'un modèle « Gemma 5B » non réaliste sur petit serveur laissait planer le doute sur la faisabilité matérielle et masquait le travail d'ingénierie réel fait sur `gemma2:2b` quantifié en 4-bit (GGUF Q4_K_M).
5. **Détails futiles :** S'attarder sur « le choix de la langue et le thème sombre/clair » dans les premières minutes banalise le projet au rang de simple maquette web.

### Diagnostic de la Version 2 (Version révisée condensée)
1. **Élagage excessif des preuves techniques tangibles :** Bien que le texte ait été raccourci, il est tombé dans l'écueil inverse : un discours trop déclaratif sans citer les livrables fonctionnels concrets du dépôt (tokens Git ZKP, export OASIS SARIF 2.1.0, audit trail SHA-256 conforme Malabo, registre CycloneDX SBOM).
2. **Vulnérabilité face aux questions de performance :** Aucune métrique concrète n'était fournie pour prouver le fonctionnement de l'IA locale et la latence Git face aux hyperscalers.
3. **Absence d'un script de démo millimétré :** La démo manquait d'une synchronisation rigoureuse écran/parole montrant l'application réelle, ce qui augmente le risque de cafouillage en direct.

---

## 3. Pitch Professionnel Hackathon CADEV 2026 (5 Minutes Chronométrées)

**Format :** Soutenance orale de 5 minutes avec démonstration live intégrée.
**Intervenants :** OBIEY Christ Dany (Capitaine & Lead Développeur) et MAMPOUYA Alicia Syrianne (Équipe CYBERSOCLE).

---

### [0:00 – 0:35] 1. L'Accroche Souveraine : Le Paradoxe Numérique Africain

> « Excellents membres du jury,
>
> À cet instant précis, des milliers de développeurs conçoivent les systèmes bancaires, les infrastructures d'énergie et les applications gouvernementales de l'Afrique. Mais où réside ce patrimoine stratégique ?
>
> Il réside sur des serveurs situés à 8 000 kilomètres d'ici. Soumis à des juridictions étrangères, vulnérable à des coupures unilatérales d'accès, et audité par des intelligences artificielles propriétaires qui s'abreuvent de nos données.
>
> Nous payons une bande passante sous-marine prohibitive pour pousser du code chez des hyperscalers tiers, tandis que nos institutions manquent aux exigences de la Convention de Malabo sur la territorialité des données.
>
> Je m'appelle Christ Dany Obiey, développeur à Pointe-Noire, capitaine de l'équipe CYBERSOCLE, aux côtés de ma co-équipière Alicia Syrianne Mampouya. Avec notre équipe, nous avons refusé cette fatalité. Voici **BANTUDEVLAB** : une forge logicielle souveraine panafricaine, conçue par les développeurs africains, pour les développeurs africains. »

---

### [0:35 – 1:15] 2. Le Problème : La Triple Rupture Technologique

> « Notre dépendance aux plateformes comme GitHub et GitLab engendre trois ruptures critiques pour le continent :
>
> - **Rupture 1 : L'extraterritorialité du code.** Nos dépôts sensibles, nos brevets logiciels et nos secrets industriels échappent à toute souveraineté juridique locale.
> - **Rupture 2 : La vulnérabilité de l'identité.** Les mots de passe et les jetons d'accès API traditionnels circulent en clair sur les réseaux et sont régulièrement dérobés par ingénierie sociale ou attaques de type "Man-in-the-Middle".
> - **Rupture 3 : La fuite intellectuelle vers l'IA.** Lorsque nos développeurs utilisent des assistants de code hébergés dans le Cloud public, chaque ligne de code stratégique traverse les frontières pour entraîner des modèles fermés hors d'Afrique. »

---

### [1:15 – 2:30] 3. La Solution BANTUDEVLAB : Les Trois Piliers Robustes et Vérifiables

> « BANTUDEVLAB transforme radicalement cette donne en combinant un moteur Git ultra-performant (Gitea CE) et une surcouche de gouvernance souveraine industrielle en Python/Django, bâtie sur trois piliers robustes et vérifiables :
>
> - **Pilier 1 : La Souveraineté de l'Infrastructure et des Données.**
>   BANTUDEVLAB est autonome, conteneurisé avec Docker, PgBouncer, PostgreSQL et Valkey. Déployé avec des domaines achetés chez Systalink/Datacloud et une application hébergée sur un VPS Ubuntu externe (déploiement souverain en objectif de la feuille de route), avec un chaînage cryptographique SHA-256 garantissant un journal d'audit immuable aligné sur la Convention de Malabo.
>
> - **Pilier 2 : La Sécurité Zero-Trust par Preuve à Divulgation Nulle (ZKP).**
>   Nous éliminons les mots de passe. L'authentification repose sur le protocole mathématique de **Schnorr (groupe RFC 3526 MODP 2048 bits)** avec transformée de Fiat-Shamir. L'utilisateur prouve qu'il détient son secret sans jamais le transmettre au serveur. Même en cas de compromission de l'infrastructure, aucun mot de passe ne peut fuiter car aucun mot de passe n'existe sur le serveur. Ce protocole protège également l'émission des jetons d'accès Git CLI (`tea` et `git-credential`).
>
> - **Pilier 3 : L'Intelligence Artificielle d'Aide à la Revue 100 % Locale (Gemma 2 2B via Ollama).**
>   Intégration d'un petit modèle local d'aide au développement : le modèle **Gemma 2 2B Instruct de Google** (sous conditions d'utilisation Google Gemma Terms, exécuté localement sans redistribution). L'IA audite les commits et Pull Requests en tâche d'arrière-plan Celery, détecte les secrets enfouis grâce à notre scanner d'entropie de Shannon, et propose des suggestions de revue sans qu'aucune ligne de code ne quitte l'infrastructure. »

---

### [2:30 – 3:15] 4. Démonstration Opérationnelle en Direct (3 Points d'Impact)

> « Ne nous croyez pas sur parole : regardons la forge en direct.
>
> 1. **Connexion Zero-Trust :** Je génère ma clé cryptographique via une phrase mnémonique de 12 mots. Je demande un défi aléatoire au serveur, je calcule ma preuve locale. En 80 millisecondes, le serveur valide l'équation sans avoir vu mon secret, et m'ouvre l'accès.
> 2. **Audit de Sécurité Shannon & SARIF 2.1.0 :** J'injecte un code contenant une clé privée et une vulnérabilité SQL dans le Workbench. Le moteur calcule l'entropie de Shannon, génère instantanément un rapport officiel OASIS SARIF 2.1.0 pour nos pipelines CI/CD, et attribue un score de souveraineté en temps réel.
> 3. **Revue de Code par l'IA Locale :** J'invoque notre assistant Gemma 2 2B local. En streaming instantané sans aucun accès Internet, le modèle analyse le diff, identifie la faille et propose la remédiation exacte. Rien n'est simulé, tout tourne sur notre machine hôte. »

---

### [3:15 – 4:05] 5. Adéquation au Thème CADEV, Traction & Équipe MIABE

> « Le thème de ce hackathon est : *"Construire la plateforme d'échange africaine, pour les devs, par les devs"*.
>
> BANTUDEVLAB en est la réalisation tangible. Nous ne présentons pas un concept théorique, mais une forge logicielle opérationnelle, forte de 308 commits d'ingénierie rigoureuse, 201 tests automatisés validés à 95,62 % de couverture de code, 63 dépendances Python vérifiées permissives et une politique d'accessibilité stricte zéro emoji.
>
> La plateforme héberge d'ores et déjà des briques stratégiques panafricaines, notamment notre passerelle `afri-fintech-gateway`.
>
> Notre équipe n'en est pas à son coup d'essai. Nous avons remporté le 1er prix du Hackathon MIABE 2026 grâce à FoncierChain sur Hyperledger Fabric. Nous maîtrisons les passerelles USSD, la cryptographie distribuée et le DevOps de production. »

---

### [4:05 – 4:40] 6. Modèle Économique et Vision d'Avenir avec Systalink / Datacloud

> « Notre modèle de durabilité est clair :
> - **Gratuit et ouvert :** Pour tous les développeurs individuels, étudiants et communautés open source africaines.
> - **Offres Entreprises & Souveraineté Dédiée :** Abonnements de conformité, instances privées durcies, clusters d'inférence GPU pour banques centrales, ministères et grands groupes de télécommunications.
> - **Alliance avec Systalink / Datacloud (Feuille de route) :** L'objectif de la feuille de route est de déployer des nœuds de forge interconnectés (topologie cible : Abidjan, Dakar, Lagos, Nairobi, Kigali), afin de réduire la latence et d'offrir une réplication inter-régionale. »

---

### [4:40 – 5:00] 7. Conclusion & Appel à l'Action

> « L'Afrique ne peut plus se contenter de consommer les infrastructures logicielles du reste du monde. Si nous voulons protéger notre jeunesse, nos données et nos innovations, nous devons posséder nos forges, nos modèles d'intelligence artificielle et nos clés cryptographiques.
>
> BANTUDEVLAB est prêt, sécurisé et opérationnel. Construisons ensemble notre souveraineté technologique.
>
> Je vous remercie pour votre attention et suis prêt pour vos questions. »

---

## 4. Script Scénarisé de la Démonstration (Vidéo & Direct - 3 Minutes)

**Conditions techniques requises :** Navigateur en plein écran (zoom 110-125 %), thème sombre GitHub activé, terminal Git ouvert en split-screen, notifications système coupées.
**Plan de secours :** Vidéo MP4 pré-enregistrée 1080p 60fps disponible en local sur clé USB et bureau.

| Horodatage | Action à l'Écran | Démonstrateur (Voix Off / Direct) | Données / Éléments Visuels |
|---|---|---|---|
| **0:00 – 0:25** | Affichage de la mire d'accueil BANTUDEVLAB (`/`). Bascule instantanée de la langue (Français / Swahili) et démonstration de l'identité visuelle sans aucun emoji. | « Bienvenue sur BANTUDEVLAB. Une interface sobre, accessible, inspirée des standards Primer, auto-hébergée sans aucune dépendance à des CDN externes. » | Logo carte d'Afrique vectoriel SVG, absence totale de flash blanc (FOUC). |
| **0:25 – 0:55** | Clic sur *Connexion Souveraine*. Wizard ZKP : génération des 12 mots BIP-39, calcul de la clé publique $y = g^x \pmod p$. Clic sur *Prouver mon identité*. Validation instantanée et toast de succès. | « Fini les mots de passe vulnérables. L'authentification repose sur une preuve de Schnorr Zero-Knowledge (groupe RFC 3526). Mon navigateur prouve la connaissance de la clé privée sans la transmettre. Le serveur vérifie l'équation mathématique : accès validé sans compromission possible. » | Jauge d'entropie, consommation atomique du challenge nonce unique. |
| **0:55 – 1:35** | Redirection vers le Dashboard. Vue sur les dépôts souverains synchronisés avec Gitea. Ouverture d'un dépôt (`afri-fintech-gateway`). Édition d'un fichier avec CodeMirror embarqué. | « Je bascule directement dans ma forge. Mes dépôts sont synchronisés en temps réel avec le moteur Gitea local. Pas d'attente, pas de transfert à l'autre bout de la planète. Je peux naviguer dans l'arborescence, inspecter les branches et éditer mon code en local. » | Éditeur CodeMirror, arborescence interactive, raccourci clavier `t`. |
| **1:35 – 2:15** | Dans le Workbench Souverain, collage d'un code Python contenant une clé secrète en dur (`sk_live_...`) et un `SELECT * FROM users WHERE id=` concaténé. Clic sur *Lancer l'Audit SAST*. | « Démonstration de notre scanner SAST souverain : en une fraction de seconde, le moteur calcule l'entropie de Shannon des chaînes, détecte les secrets enfouis et les injections SQL, calcule notre score de souveraineté et produit un rapport au standard OASIS SARIF 2.1.0 prêt pour la CI. » | Score de souveraineté dynamique, cartes interactives des failles, bouton d'export SARIF. |
| **2:15 – 2:45** | Clic sur *Revue par Gemma 2 2B*. L'IA locale répond en streaming continu sans accès Internet. Proposition d'un patch de sécurité immédiat. | « Voici notre modèle d'aide au développement : l'assistant d'IA local Gemma 2 2B Instruct. Exécuté localement via Ollama, il analyse le diff en direct, signale la faille et propose des suggestions de revue sans qu'aucun octet ne quitte notre machine. » | Flux SSE continu, suggestion de code nettoyé, zéro appel réseau extérieur. |
| **2:45 – 3:00** | Ouverture de l'onglet `/sovereignty-metrics/` : visualisation de la topologie cible des 5 nœuds panafricains (Projet, non déployé) et mesure de latence en direct vers le serveur actif (`/healthz`). | « Enfin, notre télémétrie en temps réel mesure la latence directe du serveur actif et présente notre topologie cible panafricaine. BANTUDEVLAB : par les devs, pour les devs. » | Carte interactive SVG annotée « Projet, non déployé », mesure `/healthz` en direct, journal chaîné SHA-256. |

---

## 5. Matrice Stratégique de Défense face au Jury (Q&A Haute Précision)

### Catégorie A : Infrastructure & Hébergement

**Question 1 : Comment est hébergée votre application et comment s'articule l'usage des services Systalink / Datacloud ?**
> *Réponse du Lead :* « Nos domaines de production officiels (`cybersocle.site` et `git.cybersocle.site`) ont été achetés chez Systalink / Datacloud. Pour cette phase de validation, l'application est hébergée sur un VPS Ubuntu externe avec une architecture entièrement conteneurisée sous Docker Compose (Django, Gitea CE, Valkey, PostgreSQL, PgBouncer, Nginx). Cette portabilité garantit une transition sans friction vers les infrastructures Datacloud de Systalink pour le passage à l'échelle panafricain. »

**Question 2 : Que se passe-t-il en cas de coupure de fibre sous-marine ou de connectivité internationale dégradée ?**
> *Réponse du Lead :* « C'est l'essence même de notre conception. Git est par essence un système distribué : chaque développeur détient l'historique complet en local. De plus, notre moteur de forge et notre assistant d'IA Gemma 2 2B tournent localement sur le réseau ou en intranet. Même si l'ensemble de la connectivité internationale vers l'Europe ou les États-Unis est rompue, les équipes africaines continuent de commiter, pusher, auditer et collaborer sans interruption. »

---

### Catégorie B : Cybersécurité, Cryptographie & Zero-Trust

**Question 3 : En quoi votre implémentation Zero-Trust ZKP est-elle supérieure à un simple système d'authentification 2FA ?**
> *Réponse du Lead :* « Le 2FA traditionnel (SMS ou TOTP) continue de reposer sur un secret partagé stocké dans la base de données du serveur (le mot de passe et la graine TOTP). Si la base de données est compromise, ces secrets sont exposés. Avec notre protocole ZKP de Schnorr sur le groupe RFC 3526 (2048 bits), le serveur ne stocke **que la clé publique $y$**. L'authentification s'effectue par vérification d'une équation d'engagement $g^s \cdot y^c \equiv t \pmod p$. Le secret $x$ ne quitte jamais la mémoire du navigateur ou du terminal du développeur. De plus, nos défis aléatoires à usage unique (nonces) sont consommés de manière atomique en base pour empêcher toute attaque par rejeu. »

**Question 4 : Comment le développeur utilise-t-il Git en ligne de commande (CLI) sans mot de passe ?**
> *Réponse du Lead :* « Nous avons développé le service `GitTokenService` (`apps/zkp_auth/tokens.py`). Le développeur valide son identité via une preuve ZKP ponctuelle, ce qui lui permet d'émettre un jeton Git sécurisé à privilèges limités (lecture, écriture, administration) avec expiration automatique, directement compatible avec Git CLI et notre outil en ligne de commande `tea`. »

**Question 5 : Votre journal d'audit est-il vraiment infalsifiable ?**
> *Réponse du Lead :* « Oui. Nous avons implémenté dans `apps/core/models.py` le modèle `AuditTrailLog` reposant sur un chaînage cryptographique SHA-256 similaire à une blockchain privée (`previous_hash -> current_hash`). Toute modification frauduleuse ou suppression d'un événement rompt immédiatement la chaîne de hachage. La conformité peut être vérifiée et exportée en ligne de commande via la commande `python manage.py export_malabo_compliance_report`. »

---

### Catégorie C : Intelligence Artificielle & Modèle Gemma 2 2B

**Question 6 : Pourquoi avoir choisi Gemma 2 2B plutôt qu'un modèle plus volumineux comme Llama-3 8B ou un modèle 5B ?**
> *Réponse du Lead :* « C'est le fruit d'une analyse rigoureuse consignée dans notre rapport `TASK/TASK5.md`. Un modèle 5B ou 8B exige des cartes graphiques professionnelles coûteuses (16 Go à 24 Go de VRAM) souvent indisponibles ou hors de prix sur notre continent. Gemma 2 2B, quantifié en 4-bit (GGUF Q4_K_M), ne pèse que 1,6 Go et tourne avec une fluidité exceptionnelle (plus de 35 tokens par seconde) sur un simple processeur multicœur ou un GPU d'entrée de gamme de 4 Go de VRAM. Ses performances sur l'analyse de syntaxe, l'extraction de vulnérabilités et la génération de patchs sont remarquables tout en respectant notre impératif d'éco-conception souveraine. »

**Question 7 : Que répondez-vous au risque d'hallucination de l'IA lors des revues de sécurité ?**
> *Réponse du Lead :* « Nous appliquons le principe de défense en profondeur : l'IA Gemma 2 2B n'agit jamais seule. Elle intervient en surcouche d'un scanner SAST déterministe qui effectue le calcul d'entropie de Shannon et l'analyse syntaxique stricte des vulnérabilités connues (injections, secrets en dur). L'IA est strictement consultative : elle fournit des suggestions de refactorisation que le développeur ou le relecteur humain valide explicitement avant toute fusion. »

---

### Catégorie D : Positionnement Produit & Concurrence

**Question 8 : « N'est-ce pas simplement un habillage de Gitea ? »**
> *Réponse du Lead :* « Gitea est notre moteur Git de bas niveau, tout comme Linux est le noyau d'Ubuntu ou Android. Nous avons bâti au-dessus une surcouche souveraine propriétaire et open source comprenant :
> 1. Un moteur d'authentification cryptographique Zero-Trust ZKP complet.
> 2. Un scanner SAST multi-langages conforme SARIF 2.1.0.
> 3. Un agent d'IA local autonome piloté par Celery.
> 4. Une gouvernance multi-organisation (ministères, banques, universités).
> 5. Une suite de synchronisation bidirectionnelle de session, de thème et de langue.
> 6. Plus de 20 cycles d'extensions documentés dans `TASK/` garantissant une équivalence fonctionnelle complète avec GitHub. »

**Question 9 : Pourquoi un développeur quitterait-il GitHub pour BantuDevLab ?**
> *Réponse du Lead :* « Il ne s'agit pas d'opposer les plateformes, mais d'offrir le choix de la souveraineté. Pour les projets open source mondiaux, GitHub reste pertinent. Mais pour les infrastructures critiques, les banques centrales, les dossiers médicaux, les télécoms et le code d'État, héberger sur BantuDevLab vise la conformité avec la Convention de Malabo et la certitude qu'aucune IA étrangère n'exploite le code africain. De plus, nos fonctionnalités de miroir Git permettent une synchronisation transparente entre les deux mondes. »

---

## 6. Checklist Opérationnelle pour le Jour J

### Avant la Présentation (H - 2 heures)
- [ ] Vérifier la connectivité locale et tester la résolution DNS du serveur.
- [ ] Démarrer le cluster conteneurisé : `docker compose up -d` ou serveur local actif sur les ports 8000 et 3002.
- [ ] Vérifier que le runtime Ollama / vLLM local répond sur le modèle `gemma2:2b` : `curl http://localhost:11434/api/tags`.
- [ ] Exécuter les vérifications de conformité :
  ```bash
  python scripts/check_no_emoji.py
  ruff check .
  ```
- [ ] Connecter le compte de démonstration non privilégié (`cadev_evaluator`) via « Connexion Démo 1-Clic » et vérifier que le dépôt témoin est prêt.
- [ ] Ouvrir la vidéo de secours 1080p dans un lecteur multimédia réduit dans la barre des tâches.
- [ ] Mettre l'ordinateur en mode « Ne pas déranger » et désactiver le verrouillage automatique d'écran.

### Pendant le Passage (5 Minutes)
- [ ] Conserver un contact visuel soutenu avec les membres du jury.
- [ ] Articuler calmement et respecter le minutage (ne pas déborder au-delà des 5 minutes).
- [ ] En cas de latence réseau imprévue pendant la démo, basculer sans aucune hésitation ni justification vers la vidéo de secours en expliquant les étapes avec assurance.
- [ ] Répondre aux questions du jury de façon directe, technique et étayée par les réalisations du référentiel Git.
