# FICHE OFFICIELLE DE SOUMISSION — CONCOURS CADEV 2026 (SYSTALINK)

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne  
**Événement :** Concours CADEV 2026 — Systalink Cloud  
**Date limite de soumission :** 15 novembre 2026 à 17 h 00 GMT  
**URL de production :** https://cybersocle.site (Portail Central & API) / https://git.cybersocle.site (Forge Gitea CE)  
**Dépôt source public (Forge souveraine Gitea) :** https://git.cybersocle.site/obiey-code/bantudevlab.git  
**Accès Web aux commits (branche `main`) :** https://git.cybersocle.site/obiey-code/bantudevlab/commits/branch/main  
**Miroir de réplication GitHub :** https://github.com/OBIEY-TEAM/BANTUDEVLAB  

---

## a) Présentation du Projet et du Sujet Traité

### Contexte & Problématique
Le continent africain fait face à une dépendance critique vis-à-vis des plateformes étrangères d'hébergement de code source et d'outillage logiciel (telles que GitHub ou GitLab.com). Cette dépendance expose les données stratégiques des administrations publiques, des institutions financières, des universités et des startups du continent aux réglementations extraterritoriales (ex. Cloud Act, FISA), aux risques de restrictions unilatérales d'accès et au transfert non maîtrisé de code propriétaire vers des modèles d'intelligence artificielle hébergés hors du continent.

### Solution Apportée : BANTUDEVLAB
BANTUDEVLAB est une forge logicielle panafricaine souveraine d'échange et de revue de code, conçue selon le principe « par les développeurs, pour les développeurs ». Elle associe :
1. **Un moteur Git distribué et léger :** Intégration de Gitea CE 1.22 (licence MIT) avec passerelle multi-forges et synchronisation d'écosystème.
2. **Une authentification Zero-Trust sans mot de passe (ZKP) :** Système cryptographique fondé sur le protocole de Schnorr non interactif (Fiat-Shamir sur groupe RFC 3526 MODP 2048 bits), évitant la transmission ou le stockage de mots de passe sur le serveur.
3. **Un scanner d'analyse statique SAST intégré :** Détection de secrets par calcul d'entropie de Shannon ($H \ge 3.8$), détection de vulnérabilités multi-langages, calcul d'un score de souveraineté numérique (0 à 100%) et exports normalisés OASIS SARIF 2.1.0 et GitLab SAST (`gl-sast-report.json`).
4. **Un assistant de revue de code IA local (Gemma 2 2B) :** Inférence locale via Ollama au sein du conteneur d'infrastructure, sans fuite de télémétrie ni de code vers des tiers.
5. **Une expérience utilisateur multi-écrans bilingue et panafricaine :** Terminal de commande guidé sans saisie libre, éditeur CodeMirror 5, et 4 langues supportées (Français, Anglais, Kiswahili, Portugais).

---

## b) Déclaration de Titularité des Droits

Les soussignés, membres de l'équipe candidate **CYBERSOCLE** :
1. **OBIEY Christ Dany** (Capitaine d'équipe)
2. **MAMPOUYA Alicia Syrianne** (Membre de l'équipe)

déclarent sur l'honneur que le projet BANTUDEVLAB a été conçu, développé et réalisé à titre personnel et indépendant, **hors de toute mission, contrat de travail, mandat ou commande émanant d'un employeur, client ou établissement d'enseignement**. L'ensemble des droits d'auteur et de propriété intellectuelle afférents au code original développé appartient exclusivement aux membres de l'équipe CYBERSOCLE et est mis à disposition sous licence permissive MIT.

### Tableau d'engagement et de confirmation des membres :

| Nom et Prénom | Rôle dans le projet | Statut d'indépendance | Signature / Mention | Date de signature |
| :--- | :--- | :--- | :--- | :--- |
| **OBIEY Christ Dany** | **Capitaine d'équipe**, Architecture & Développement Fullstack | Travaux réalisés à titre personnel et indépendant hors contrat employeur/client | [À signer par OBIEY Christ Dany : Mention « Lu et approuvé »] | [Date à compléter : JJ/MM/2026] |
| **MAMPOUYA Alicia Syrianne** | **Membre de l'équipe**, Ingénierie logicielle, QA & Sécurité | Travaux réalisés à titre personnel et indépendant hors contrat employeur/client | [À signer par MAMPOUYA Alicia Syrianne : Mention « Lu et approuvé »] | [Date à compléter : JJ/MM/2026] |

---

## c) Inventaire Complet des Composants Tiers et Licences

Conformément à l'Article 6 du règlement du concours CADEV 2026, l'ensemble des dépendances a été audité. Les licences copyleft (GPL, AGPL, LGPL) ont été proscrites du build standard de soumission. Seules les licences permissives (MIT, Apache-2.0, BSD, PSF, Domaine Public) sont admises.

### 1. Composants d'Infrastructure et Frontend

| Composant | Version | Licence | Rôle / Usage | Statut CADEV 2026 | Conformité |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gitea CE** | `1.22` | MIT | Forge logicielle Git principale | **OK (Permissif)** | Utilisé tel quel, sans modification de code source. |
| **Valkey** | `7.2-alpine` | BSD-3-Clause | Cache applicatif & Broker Celery | **OK (Permissif)** | Fork Linux Foundation sous licence BSD-3-Clause (remplace Redis >= 7.4). |
| **Nginx** | `1.27-alpine` | BSD-2-Clause | Reverse Proxy & Terminaison TLS | **OK (Permissif)** | Licence permissive BSD. |
| **PostgreSQL** | `16-alpine` | PostgreSQL License | SGBD relationnel (optionnel en prod) | **OK (Permissif)** | Licence permissive approuvée OSI. |
| **SQLite 3** | Système (Python) | Public Domain | SGBD standard de référence soumis | **OK (Permissif)** | Inclus en standard, 100% autonome et permissif. |
| **Ollama** | `latest` | MIT | Serveur d'inférence IA locale | **OK (Permissif)** | Moteur d'inférence open-source. |
| **Gemma 2 2B** | `2b-it (Q4_K_M)` | Google Gemma Terms | Poids du modèle IA de fondation | **Usage local non redistribué** | Modèle exécuté localement, non redistribué, régi par les conditions d'utilisation Google Gemma (non qualifié de permissif). |
| **CodeMirror 5** | `5.65.16` | MIT | Éditeur de code intégré (Workbench) | **OK (Permissif)** | Auto-hébergé dans `static/vendor/codemirror/`, zéro CDN. |
| **Icônes SVG Bantu** | `1.0.0` | MIT | Pictogrammes de navigation UI | **OK (Permissif)** | Tracés SVG outline natifs sans emoji ni police d'icônes externe. |

### 2. Dépendances Python Runtime (`requirements.txt`)

L'inventaire complet des paquets d'exécution comprend 12 dépendances directes et leurs dépendances transitives, toutes sous licences permissives :

| Paquet Python | Version | Licence Déclarée | Statut CADEV 2026 |
| :--- | :--- | :--- | :--- |
| **Django** | `5.2.18` | BSD-3-Clause | **OK (Permissif)** |
| **djangorestframework** | `3.18.3` | BSD-3-Clause | **OK (Permissif)** |
| **drf-spectacular** | `0.30.0` | BSD-3-Clause | **OK (Permissif)** |
| **cryptography** | `50.0.2` | Apache-2.0 OR BSD-3-Clause | **OK (Permissif)** |
| **requests** | `2.34.2` | Apache-2.0 | **OK (Permissif)** |
| **celery** | `5.6.3` | BSD-3-Clause | **OK (Permissif)** |
| **redis** | `8.1.0` | MIT | **OK (Permissif)** |
| **python-dotenv** | `1.2.4` | BSD-3-Clause | **OK (Permissif)** |
| **gunicorn** | `26.2.0` | MIT | **OK (Permissif)** |
| **uvicorn** | `0.54.0` | BSD-3-Clause | **OK (Permissif)** |
| **pillow** | `13.0.0` | MIT-CMU | **OK (Permissif)** |
| **PyYAML** | `6.0.3` | MIT | **OK (Permissif)** |
| *Dépendances transitives (asgiref, certifi MPL, cffi, charset-normalizer, click, idna, kombu, packaging, sqlparse, typing_extensions, urllib3, etc.)* | *Dernières versions stables* | BSD / MIT / Apache-2.0 / MPL-2.0 | **OK (Permissif / Non contaminant)** |

### 3. Statut des Bloquants Résolus (Art. 6)
- **`python-gitlab` (LGPL-3.0) :** Retiré du projet et désinstallé. Remplacé intégralement par des appels HTTP REST via la bibliothèque `requests` (Apache-2.0) dans `apps/gitlab_client/client.py`.
- **`psycopg2-binary` (LGPL-3.0) :** Retiré du fichier principal `requirements.txt`. Le projet s'exécute par défaut sur le moteur standard SQLite (Domaine Public). Le support PostgreSQL reste documenté de manière optionnelle dans `requirements-postgres.txt` sans polluer l'environnement soumis.
- **`Redis >= 7.4` (SSPL/RSALv2) :** Remplacé dans l'infrastructure Docker par **Valkey 7.2** (BSD-3-Clause).

---

## d) Déclaration sur l'Usage de l'Intelligence Artificielle

### 1. Modèle d'Inférence Embarqué dans le Produit (Gemma 2 2B)
- **Modèle sélectionné :** Google Gemma 2 2B Instruct (`gemma2:2b`), quantifié en 4-bit (GGUF Q4_K_M).
- **Moteur d'exécution :** Ollama (logiciel open-source sous licence MIT).
- **Statut légal et licence :** Le modèle Gemma est régi par les **Google Gemma Terms of Use** (conditions d'utilisation et politique d'usage responsable de Google). **Ce modèle n'est pas qualifié de licence permissive au sens de l'Article 6 du concours.**
- **Modalité d'exécution stricte :** Le modèle est exécuté **exclusivement en local on-premise** sur le serveur d'hébergement. Aucune donnée utilisateur, aucun extrait de code source ni télémétrie n'est envoyé à Google ou à un tiers externe. Les poids binaires du modèle ne sont pas redistribués dans le dépôt Git de BantuDevLab.
- **Rôle applicatif exact :** Outil d'assistance au développement et à la revue de code (analyse de patterns de sécurité, explication de vulnérabilités, proposition d'optimisations). **Ce modèle 2B constitue une aide au développeur et ne remplace pas l'ingénieur humain ni la validation manuelle.**

### 2. Outils d'Aide au Développement Utilisés par l'Équipe
- **Outils utilisés lors de la phase de conception :**  
  `[À compléter par l'équipe : ex. Claude Code, ChatGPT, GitHub Copilot, Antigravity AI, etc.]`
- **Périmètre d'usage des assistants IA :**  
  `[À compléter par l'équipe : ex. Aide à la structuration des stubs de tests, relecture de documentation, prototypage de styles CSS]`
- **Maîtrise du code livré :**  
  L'équipe CYBERSOCLE atteste et certifie avoir conçu, structuré, relu, testé et validé l'intégralité du code livré dans le dépôt. L'équipe maîtrise 100% de la logique métier, du protocole cryptographique Schnorr NIZKP, des algorithmes d'analyse SAST et de calcul d'entropie Shannon, ainsi que de l'architecture générale.

---

## e) Architecture de Déploiement et Services Systalink / Datacloud

### 1. Architecture Réseau et Hébergement
- **Noms de domaine de production :** `cybersocle.site` (Portail Central & API) et `git.cybersocle.site` (Forge Gitea CE).
- **Achat du domaine :** Domaines achetés auprès de l'infrastructure d'enregistrement Systalink / Datacloud.
- **Serveur d'hébergement effectif :** L'application est hébergée sur un Serveur Privé Virtuel (VPS externe sous Ubuntu 24.04 LTS), exécutant la pile de conteneurs Docker durcis (Django, Gitea CE, Valkey, PostgreSQL, Ollama, Nginx TLS 1.3). Elle n'est pas hébergée sur une instance d'exécution Systalink Cloud.
- **Résolution DNS :** Les enregistrements de zone A et CNAME des domaines achetés chez Datacloud routent le trafic sécurisé HTTPS vers le VPS d'hébergement.

### 2. Références du Service Datacloud (À compléter par l'équipe CYBERSOCLE) :
- **Identifiant / Compte client Datacloud :** `[À compléter : identifiant client Datacloud]`
- **Numéro de référence de commande du domaine / service :** `[À compléter : Numéro de commande ou de facture Datacloud]`
- **Date de souscription :** `[À compléter : Date exacte d'achat du domaine]`
- **Usage effectif du service Datacloud :** Gestion et délégation de la zone DNS souveraine pour les domaines `cybersocle.site` et `git.cybersocle.site`.

---

## f) Preuve d'Achat Datacloud

Section réservée à la justification de l'achat du service Datacloud conformément aux exigences du concours CADEV 2026.

```text
[EMPLACEMENT RÉSERVÉ — PREUVE D'ACHAT DATACLOUD]

Veuillez insérer ici le reçu, la facture, le bon de commande ou la confirmation
de paiement émise par Systalink / Datacloud attestant de l'achat des domaines
cybersocle.site et git.cybersocle.site.

- Numéro de transaction / reçu : [À compléter]
- Montant réglé : [À compléter]
- Date de paiement : [À compléter]
- Copie textuelle ou référence du justificatif : [À compléter]
```

---

## g) Code Antérieur au Concours

Conformément à l'Article 6 du règlement du concours (déclaration obligatoire de tout code antérieur au 29 septembre 2026), l'historique Git du projet a été intégralement relevé dans le document de référence `CADEV26/HISTORIQUE.md`.

### Déclaration Factuelle :
- **Date du tout premier commit Git :** **31 octobre 2026 à 11:14:31 GMT** (`b0fa102ec01065d0b9a788363b3d4c03b2f99535`).
- **Commits réalisés avant le 29 septembre 2026 :** **ZÉRO (0 commit)**. Aucun code préexistant antérieur au 29 septembre 2026 n'a été réutilisé ou importé dans le projet.
- **Nombre total de commits enregistrés :** 280 commits traçables, documentant le développement continu entre le 31 octobre 2026 et le 12 novembre 2026.
- **Auteurs des contributions :**  
  - OBIEY Christ Dany : 280 commits (identifiants `obiey`, `obieydany-code`, `obiey christ dany`, `OBIEY Christ Dany`).
- **Composants tiers non modifiés :** Gitea CE 1.22 (0% de code modifié), Valkey 7.2 (0% de code modifié), Nginx 1.27 (0% de code modifié), Ollama (0% de code modifié).
- **Code original produit par l'équipe :** 100% du code applicatif situé dans `apps/` (~4 632 lignes Python), les templates HTML/CSS (~6 000 lignes), les scripts de contrôle qualité et la documentation ont été écrits intégralement durant la période officielle du concours.
