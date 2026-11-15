# Dossier Stratégique CADEV 2026 : BANTUDEVLAB / SysteLink Cloud Africain

**Auteurs :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany  
- **Membre de l'équipe (Présentatrice) :** GAMBOUE Ursie  
- **Membre de l'équipe (Présentatrice) :** MAMPOUYA Alicia Syrianne  
**Événement :** Systalink Challenge / CADEV 2026 (29 sept. – 15 nov. 2026)
**Thème officiel :** « Construire la plateforme d'échange africaine, pour les devs, par les devs. »
**Positionnement :** Forge logicielle panafricaine souveraine (Alternative locale à GitHub / GitLab avec Zero-Trust ZKP, scanner SAST Shannon SARIF 2.1.0 et IA d'audit in-forge Gemma 2 2B quantifiée en local).

---

## Sommaire Exécutif

1. [Analyse Technique Approfondie du Projet (Commits, PRs, Fichiers)](#1-analyse-technique-approfondie-du-projet-commits-prs-fichiers)
2. [Autopsie Critique des Pitches Antérieurs (Facteurs d'Échec)](#2-autopsie-critique-des-pitches-antérieurs-facteurs-déchec)
3. [Discours Final CADEV 2026 (5 Minutes Chronométrées)](#3-discours-final-cadev-2026-5-minutes-chronométrées)
4. [Aide-Mémoire (à tenir en main)](#4-aide-mémoire-à-tenir-en-main)
5. [Réponses Éclair aux Questions Pièges & Matrice Technique](#5-réponses-éclair-aux-questions-pièges--matrice-technique)
6. [Checklist Avant de Passer (Jour J)](#6-checklist-avant-de-passer-jour-j)

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
  - **Axe 6 (Assurance Qualité & Tests) :** Tests de fuzzing cryptographique (`test_zkp_fuzzing.py`), tests end-to-end Playwright (`test_e2e_playwright.py`), couverture de test mesurée à 95,65 % sur les modules cœur, linting/formatage automatisé Ruff, et audit de sécurité Bandit.
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

## 3. Discours Final CADEV 2026 (5 Minutes Chronométrées)

**Thème officiel :** « Construire la plateforme d’échange africaine, pour les devs, par les devs. »  
**Livrables demandés :** dépôt Git + démo en ligne (projet utilisable et hébergé en ligne).  
**Présentation :** GAMBOUE Ursie, MAMPOUYA Alicia Syrianne, avec OBIEY Christ Dany (capitaine).

---

### [0:00 – 0:30] Accroche

> « Mesdames et messieurs les membres du jury, bonjour.
> Le thème de ce challenge est : construire la plateforme d’échange africaine, pour les devs, par les devs. Posons-nous une question simple : où échangent aujourd’hui les développeurs africains ? Sur des plateformes situées à des milliers de kilomètres, soumises à des lois qui ne sont pas les nôtres, et dont le code peut alimenter des modèles d’IA hébergés hors du continent.
> Nous sommes l’équipe CYBERSOCLE, de Pointe-Noire. Je suis Ursie GAMBOUE, Alicia Mampouya, et avec notre capitaine Christ Dany Obiey, nous avons construit BantuDevLab. »

---

### [0:30 – 1:05] Le problème

> « Trois risques concrets.
> Un : notre code échappe à notre cadre juridique. Deux : nos accès reposent sur des mots de passe, l’une des principales causes de compromission. Trois : chaque ligne envoyée à une IA dans le cloud peut servir à entraîner des modèles fermés, hors d’Afrique.
> Pour une banque, un ministère ou une startup, c’est un risque stratégique. »

---

### [1:05 – 2:10] La solution

> « BantuDevLab est une plateforme d’échange de code : dépôts, branches, revues et tickets. Elle est hébergée en ligne et utilisable dès aujourd’hui. Elle s’appuie sur le moteur Git Gitea, et nous avons développé par-dessus trois briques.
> Première brique : l’identité sans mot de passe. Notre authentification utilise une preuve à divulgation nulle de connaissance, le protocole de Schnorr. Vous prouvez que vous possédez votre clé sans jamais l’envoyer. Notre serveur ne stocke que la clé publique : s’il est piraté, il n’y a aucun mot de passe à voler.
> Deuxième brique : l’audit de sécurité intégré. Notre scanner repère les secrets oubliés dans le code grâce à l’entropie de Shannon, détecte les injections SQL, et exporte ses rapports au standard SARIF 2.1.0, utilisable directement en CI/CD.
> Troisième brique : une IA qui reste chez nous. Nous utilisons Gemma 2 2B, un modèle compact qui tourne en local, sans connexion externe. L’IA suggère, le scanner vérifie, et c’est toujours l’humain qui décide. »

---

### [2:10 – 3:35] Démonstration en direct

> « Ne nous croyez pas sur parole, regardez.
> *(Ouvrir cybersocle.site)* Voici la plateforme en ligne. Je clique sur la connexion démo : mon navigateur calcule une preuve cryptographique, le serveur la vérifie, et j’entre sans aucun mot de passe.
> *(Dashboard)* Je crée un dépôt, et il est immédiatement synchronisé avec notre forge Git.
> *(Échange)* Sur ce dépôt, j’ouvre un ticket, et un second compte peut y répondre : c’est cela, l’échange entre développeurs.
> *(Workbench)* Je colle un code contenant une clé secrète et une requête SQL vulnérable. Je lance l’audit : en environ une seconde, les failles sont détectées et un rapport SARIF est prêt.
> *(Revue IA)* Je demande la revue à Gemma. La réponse arrive en continu et propose la correction, sans qu’une seule ligne de code ne quitte l’infrastructure. »

*Note : répétez l’étape « Échange » (ticket + second compte) avant le jour J. Si elle n’est pas prête, supprimez cette phrase plutôt que de l’improviser.*

---

### [3:35 – 4:20] Preuves et transparence

> « Ce projet est réel. Notre premier commit date du 31 octobre : en deux semaines, nous avons produit 325 commits et 202 tests automatisés, avec 95,65 % de couverture sur nos modules cœur. Notre build de soumission ne contient aucun composant GPL, AGPL ou LGPL, vérifié automatiquement. Le modèle Gemma reste sous les conditions d’utilisation de Google, exécuté en local et non redistribué.
> Nous tenons aussi à être transparents. Nos domaines sont achetés chez Systalink Datacloud, et l’application tourne aujourd’hui sur un serveur VPS externe. L’étape suivante est de la migrer sur l’infrastructure Systalink. Nous avons aussi déclaré tous les outils d’assistance utilisés, et nous assumons chaque ligne livrée. »

---

### [4:20 – 4:40] Vision

> « Notre feuille de route : des nœuds interconnectés à Abidjan, Dakar, Lagos, Nairobi et Kigali, pour rapprocher le code des développeurs. Gratuit pour les développeurs, étudiants et communautés open source ; des offres dédiées pour les institutions. »

---

### [4:40 – 5:00] Conclusion

> « L’Afrique ne doit pas seulement consommer les plateformes des autres. Elle doit avoir les siennes, par les devs, pour les devs. BantuDevLab est en ligne, il est utilisable, et nous vous invitons à le tester dès maintenant. Merci. »

---

## 4. Aide-Mémoire (à tenir en main)

| Minute | À dire / à faire |
| :--- | :--- |
| **0:00** | Accroche : thème officiel + « où échangent les devs africains ? » |
| **0:30** | 3 risques : droit, mots de passe, IA dans le cloud |
| **1:05** | 3 briques : ZKP sans mot de passe, audit SAST + SARIF, Gemma 2 2B en local |
| **2:10** | Démo : connexion démo → dépôt → ticket (échange) → audit → revue IA |
| **3:35** | Preuves : 325 commits, 202 tests, 95,65 % (modules cœur), pas de GPL/AGPL/LGPL |
| **3:35** | Transparence : domaines Datacloud, application sur VPS externe, migration prévue |
| **4:20** | Vision : 5 nœuds cibles (projet, non déployé), modèle gratuit + institutions |
| **4:40** | Conclusion : « par les devs, pour les devs » + invitation à tester |

---

## 5. Réponses Éclair aux Questions Pièges & Matrice Technique

### Réponses éclair (à dégainer en soutenance)

- **« Pourquoi pas hébergé chez Systalink ? »**  
  Domaines achetés chez Datacloud, application en conteneurs Docker portable : la migration est l’étape suivante de la feuille de route.
- **« N’est-ce pas juste Gitea ? »**  
  Gitea est le moteur Git, utilisé tel quel. Nous avons développé l’authentification ZKP, le scanner SAST, l’assistant IA local, l’audit chaîné SHA-256 et la gestion multi-organisations.
- **« L’IA peut halluciner. »**  
  Elle est consultative : le scanner déterministe vérifie, et l’humain valide avant toute fusion.
- **« Pourquoi un modèle 2B ? »**  
  Il tourne sur un processeur ou un GPU modeste, sans Internet, ce qui convient aux infrastructures disponibles sur le continent.
- **« Où est l’échange ? »**  
  Dépôts partagés, tickets et pull requests entre comptes, sur une forge hébergée en ligne.

### Matrice Technique Complémentaire (Détails pour Questions Approfondies)

### Catégorie A : Infrastructure & Hébergement

**Question 1 : Comment est hébergée votre application et comment s'articule l'usage des services Systalink / Datacloud ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Nos domaines de production officiels (`cybersocle.site` et `git.cybersocle.site`) ont été achetés chez Systalink / Datacloud. Pour cette phase de validation, l'application est hébergée sur un VPS Ubuntu externe avec une architecture entièrement conteneurisée sous Docker Compose (Django, Gitea CE, Valkey, PostgreSQL, PgBouncer, Nginx). Cette portabilité garantit une transition sans friction vers les infrastructures Datacloud de Systalink pour le passage à l'échelle panafricain. »

**Question 2 : Que se passe-t-il en cas de coupure de fibre sous-marine ou de connectivité internationale dégradée ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « C'est l'essence même de notre conception. Git est par essence un système distribué : chaque développeur détient l'historique complet en local. De plus, notre moteur de forge et notre assistant d'IA Gemma 2 2B tournent localement sur le réseau ou en intranet. Même si l'ensemble de la connectivité internationale vers l'Europe ou les États-Unis est rompue, les équipes africaines continuent de commiter, pusher, auditer et collaborer sans interruption. »

---

### Catégorie B : Cybersécurité, Cryptographie & Zero-Trust

**Question 3 : En quoi votre implémentation Zero-Trust ZKP est-elle supérieure à un simple système d'authentification 2FA ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Le 2FA traditionnel (SMS ou TOTP) continue de reposer sur un secret partagé stocké dans la base de données du serveur (le mot de passe et la graine TOTP). Si la base de données est compromise, ces secrets sont exposés. Avec notre protocole ZKP de Schnorr sur le groupe RFC 3526 (2048 bits), le serveur ne stocke **que la clé publique $y$**. L'authentification s'effectue par vérification d'une équation d'engagement $g^s \cdot y^c \equiv t \pmod p$. Le secret $x$ ne quitte jamais la mémoire du navigateur ou du terminal du développeur. De plus, nos défis aléatoires à usage unique (nonces) sont consommés de manière atomique en base pour empêcher toute attaque par rejeu. »

**Question 4 : Comment le développeur utilise-t-il Git en ligne de commande (CLI) sans mot de passe ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Nous avons développé le service `GitTokenService` (`apps/zkp_auth/tokens.py`). Le développeur valide son identité via une preuve ZKP ponctuelle, ce qui lui permet d'émettre un jeton Git sécurisé à privilèges limités (lecture, écriture, administration) avec expiration automatique, directement compatible avec Git CLI et notre outil en ligne de commande `tea`. »

**Question 5 : Votre journal d'audit est-il vraiment infalsifiable ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Oui. Nous avons implémenté dans `apps/core/models.py` le modèle `AuditTrailLog` reposant sur un chaînage cryptographique SHA-256 similaire à une blockchain privée (`previous_hash -> current_hash`). Toute modification frauduleuse ou suppression d'un événement rompt immédiatement la chaîne de hachage. La conformité peut être vérifiée et exportée en ligne de commande via la commande `python manage.py export_malabo_compliance_report`. »

---

### Catégorie C : Intelligence Artificielle & Modèle Gemma 2 2B

**Question 6 : Pourquoi avoir choisi Gemma 2 2B plutôt qu'un modèle plus volumineux comme Llama-3 8B ou un modèle 5B ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « C'est le fruit d'une analyse rigoureuse consignée dans notre rapport `TASK/TASK5.md`. Un modèle 5B ou 8B exige des cartes graphiques professionnelles coûteuses (16 Go à 24 Go de VRAM) souvent indisponibles ou hors de prix sur notre continent. Gemma 2 2B, quantifié en 4-bit (GGUF Q4_K_M), ne pèse que 1,6 Go et tourne avec une fluidité exceptionnelle (plus de 35 tokens par seconde) sur un simple processeur multicœur ou un GPU d'entrée de gamme de 4 Go de VRAM. Ses performances sur l'analyse de syntaxe, l'extraction de vulnérabilités et la génération de patchs sont remarquables tout en respectant notre impératif d'éco-conception souveraine. »

**Question 7 : Que répondez-vous au risque d'hallucination de l'IA lors des revues de sécurité ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Nous appliquons le principe de défense en profondeur : l'IA Gemma 2 2B n'agit jamais seule. Elle intervient en surcouche d'un scanner SAST déterministe qui effectue le calcul d'entropie de Shannon et l'analyse syntaxique stricte des vulnérabilités connues (injections, secrets en dur). L'IA est strictement consultative : elle fournit des suggestions de refactorisation que le développeur ou le relecteur humain valide explicitement avant toute fusion. »

---

### Catégorie D : Positionnement Produit & Concurrence

**Question 8 : « N'est-ce pas simplement un habillage de Gitea ? »**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Gitea est notre moteur Git de bas niveau, tout comme Linux est le noyau d'Ubuntu ou Android. Nous avons bâti au-dessus une surcouche souveraine open source (licence MIT) comprenant :
> 1. Un moteur d'authentification cryptographique Zero-Trust ZKP complet.
> 2. Un scanner SAST multi-langages conforme SARIF 2.1.0.
> 3. Un agent d'IA local autonome piloté par Celery.
> 4. Une gouvernance multi-organisation (ministères, banques, universités).
> 5. Une suite de synchronisation bidirectionnelle de session, de thème et de langue.
> 6. Plus de 20 cycles d'extensions documentés dans `TASK/` garantissant une équivalence fonctionnelle complète avec GitHub. »

**Question 9 : Pourquoi un développeur quitterait-il GitHub pour BantuDevLab ?**
> *Réponse de l'équipe (Alicia / Christ Dany) :* « Il ne s'agit pas d'opposer les plateformes, mais d'offrir le choix de la souveraineté. Pour les projets open source mondiaux, GitHub reste pertinent. Mais pour les infrastructures critiques, les banques centrales, les dossiers médicaux, les télécoms et le code d'État, héberger sur BantuDevLab vise la conformité avec la Convention de Malabo et la certitude qu'aucune IA étrangère n'exploite le code africain. De plus, nos fonctionnalités de miroir Git permettent une synchronisation transparente entre les deux mondes. »

---

## 6. Avant de Passer (Checklist Jour J)

### Avant de passer (à cocher juste avant la soutenance)
- [ ] Vidéo de secours prête dans un lecteur réduit.
- [ ] Dépôt `bantudevlab` public sur `git.cybersocle.site/explore/repos`.
- [ ] Étape ticket + second compte répétée.
- [ ] Notifications coupées, écran en mode « Ne pas déranger ».
- [ ] Ne pas dépasser 5 minutes : couper la « Vision » en premier si besoin.

### Vérifications Techniques Préalables (H - 2 heures)
- [ ] Vérifier la connectivité locale et tester la résolution DNS du serveur (`cybersocle.site`, `git.cybersocle.site`).
- [ ] Vérifier que le runtime Ollama local répond sur le modèle `gemma2:2b` : `curl http://localhost:11434/api/tags`.
- [ ] Exécuter les vérifications de conformité :
  ```bash
  python scripts/check_no_emoji.py
  python scripts/check_licenses.py
  ruff check .
  ```
- [ ] Connecter le compte de démonstration non privilégié (`cadev_evaluator`) via « Connexion Démo » et vérifier que le dépôt témoin est prêt.

### Pendant le Passage (5 Minutes)
- [ ] Conserver un contact visuel soutenu avec les membres du jury.
- [ ] Articuler calmement et respecter le minutage (ne pas dépasser 5 minutes ; couper la « Vision » en premier si besoin).
- [ ] En cas de latence réseau imprévue pendant la démo, basculer sans aucune hésitation ni justification vers la vidéo de secours.
- [ ] Répondre aux questions du jury de façon directe, technique et étayée par les réalisations du référentiel Git.
