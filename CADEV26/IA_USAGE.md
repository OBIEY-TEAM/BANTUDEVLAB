# RAPPORT DE TRAÇABILITÉ DE L'USAGE DE L'IA — CADEV 2026

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany (Lead Architecture & Développement Fullstack)  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne (Présentation vidéo démo & parcours utilisateur)  
- **Membre de l'équipe :** GAMBOUE Ursie Semence (Présentatrice — Présentation vidéo démo & parcours utilisateur)  
**Cadre réglementaire :** Article 6 du concours CADEV 2026 (Transparence et déclaration des outils d'assistance)  
**Date du relevé :** 15 novembre 2026  

---

## 1. Objectif du Document

Conformément à l'Article 6 du règlement du concours CADEV 2026, l'usage de l'intelligence artificielle est libre mais doit être déclaré de manière transparente et vérifiable.

Ce document fournit une description factuelle du flux de travail de l'équipe, identifie les outils mobilisés, et dresse l'inventaire objectif des commits et des fichiers qui portent la trace d'un outillage d'assistance au sein du dépôt Git. Conformément aux directives d'évaluation, ce relevé s'en tient aux faits observables sans extrapoler ni conclure sur une part quantitative de code générée.

---

## 2. Description Factuelle du Flux de Travail

Le flux de travail collaboratif mis en place par l'équipe CYBERSOCLE associe pilotage humain, assistance outillée et contrôle qualité rigoureux :

### 2.1 Rôles et Répartition des Outils
- **OBIEY Christ Dany (Capitaine d'équipe & Lead Developer) :**
  - **Conception & Pilotage :** Définit l'architecture générale, le schéma de données Django, les protocoles cryptographiques Zero-Knowledge Proof (Schnorr / Fiat-Shamir), et les algorithmes de détection SAST (entropie de Shannon).
  - **Jules IA :** Utilisé comme éditeur de code assisté par IA pour la préparation de correctifs sur des branches isolées, le débogage de routes HTTP, l'alignement d'assets et les propositions de feuilles de route (fichiers de tâches).
  - **Antigravity IA :** Utilisé comme éditeur de code assisté par IA pour l'audit de licences, le refactoring sans dépendance LGPL (remplacement de `python-gitlab` par `requests`), la création des scripts de contrôle qualité CI (`scripts/check_licenses.py`, `scripts/check_no_emoji.py`), et l'enrichissement des tests unitaires de couverture.
  - **Claude IA :** Mobilisé pour la compréhension et l'analyse de documents de référence, l'élaboration de plans d'action de mise en conformité, la rédaction de synthèses méthodologiques et l'argumentation relative à la souveraineté numérique.
- **MAMPOUYA Alicia Syrianne (Membre d'équipe) :**
  - Intervient sur la validation du parcours utilisateur non technique (parcours d'évaluation), la relecture des interfaces, et la préparation du support audiovisuel de démonstration (vidéo de présentation).
- **GAMBOUE Ursie Semence (Membre d'équipe — Présentatrice) :**
  - Intervient en co-présentation du pitch, de la démonstration vidéo et de la validation du parcours utilisateur.
- **GitHub :**
  - Utilisé comme outil de gestion de version et d'hébergement distant pour le suivi des branches, des revues de Pull Requests et le miroir de sauvegarde (`https://github.com/OBIEY-TEAM/BANTUDEVLAB`). GitHub n'est pas un outil d'intelligence artificielle.
- **Gemma 2 2B (via Ollama) :**
  - Modèle d'inférence exécuté localement au sein de l'architecture BantuDevLab pour la fonction applicative d'analyse et de revue de code. Il s'agit d'un composant de la solution livrée et non d'un outil d'aide au développement.

### 2.2 Mécanismes de Relecture et de Validation Humaine
1. **Relecture Systématique :** Chaque proposition de code, script ou documentation issue d'un éditeur ou assistant est intégralement relue et analysée par l'ingénieur humain avant toute intégration.
2. **Exécution des Tests Automatisés :** Aucune modification n'est conservée sans validation par la suite de tests Pytest (202 tests unitaires et d'intégration validés, avec une couverture mesurée de 95,65%).
3. **Contrôles Statiques Automatisés :** Exécution systématique des outils de contrôle qualité :
   - `scripts/check_no_emoji.py` : interdiction stricte de tout emoji.
   - `scripts/check_licenses.py` : interdiction stricte de tout composant sous GPL, AGPL, LGPL ou licences assimilées dans le build standard.
   - `ruff` et `bandit` : vérification syntaxique et détection de failles de sécurité statiques.
4. **Intégration Contrôlée :** Les modifications sont commitées de manière atomique sur des branches thématiques dédiées avant fusion dans la branche principale `main`.

---

## 3. Traces Observables dans l'Historique Git

L'analyse de l'historique Git du dépôt révèle plusieurs traces explicites d'outils et de flux d'assistance :

### 3.1 Commits et Branches Portant la Trace d'un Outil (Jules IA)
Plusieurs commits de fusion attestent de l'intégration de branches préparées avec l'assistance de Jules IA :
- `14b9222` : *Merge pull request #41 from OBIEY-TEAM/develop-jules-sovereign-fixes-12293149301539559159* (Alignement des URLs souveraines, flux ZKP UI, logo Gitea, CSRF i18n et anti-FOUC sombre).
- `ddbc311` : *Merge pull request #36 from OBIEY-TEAM/jules-14760533911454615293-e35bf1ba* (Correction 404 sur `/health`, mise à jour des logos officiels et collectstatic).
- `0a20429` : *Merge pull request #24 from OBIEY-TEAM/jules-14936153306870637178-30c6f4a6* (Dossier stratégique et pitch CADEV 2026 pour BantuDevLab).
- `bf0b212` : *Merge pull request #15 from OBIEY-TEAM/jules-17682843790772572118-a62bd70d* (Audit et feuille de route `TASK5.md` pour BANTUDEVLAB avec gemma2:2b).
- `91dc118` : *Merge pull request #11 from OBIEY-TEAM/jules-630987579237867581-93513853* (Exécution des tâches de production et intégration GitLab, `TASK3.md`).
- `c49444f` : *Merge pull request #10 from OBIEY-TEAM/jules-18005639709413914516-d9bee9a5* (Plan de transition en production et collaboration GitLab, `TASK3.md`).

### 3.2 Fichiers Portant la Trace de Plans et de Tâches
Plusieurs documents du dépôt témoignent d'une structuration assistée par étapes et tâches de travail :
- **Dossier `docs/archive/TASK/` :** Fichiers de planification séquentielle (`TASK2.md`, `TASK3.md`, `TASK5.md` jusqu'à `TASK27.md`) documentant les jalons successifs du développement.
- **Fichier `develop-design.md` :** Document d'alignement UX et architecture front-end portant en en-tête la mention d'assistance de conception Antigravity.
- **Dossier `docs/archive/scratch/` :** Scripts Python d'automatisation ponctuelle et de refactorisation (`patch_base_html.py`, `patch_style_css.py`, `patch_templates_design.py`, `fix_claims.py`, etc.).
- **Dossier `docs/archive/` :** Fichiers d'intervention et de suivi (`backlod.md`, `intervension.md`, `intervention.md`).
- **Scripts de validation CI :** `scripts/check_licenses.py` et `scripts/check_no_emoji.py` conçus pour garantir le respect automatique des contraintes du concours.

---

## 4. Synthèse et Positionnement de l'Équipe

L'équipe CYBERSOCLE assume pleinement l'ensemble des développements livrés dans le dépôt BANTUDEVLAB. Les assistants d'intelligence artificielle et éditeurs de code ont été utilisés comme des leviers d'efficacité technique, d'accélération d'outillage et d'aide à la conception, sous le contrôle exclusif et la responsabilité des auteurs du projet.
