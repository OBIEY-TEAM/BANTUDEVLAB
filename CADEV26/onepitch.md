# BANTUDEVLAB — Le Pitch en Une Phrase & Stack Technique (CADEV 2026)

**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany (Lead Architect / Fullstack)  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne (QA & Sécurité)  
**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Concours :** CADEV 2026 (Systalink / Datacloud) — Date limite : 15 novembre 2026, 17 h 00 GMT  
**Accès en ligne :** https://cybersocle.site | https://git.cybersocle.site  
**Code source public :** https://git.cybersocle.site/obiey-code/bantudevlab.git (branche `main` : https://git.cybersocle.site/obiey-code/bantudevlab/commits/branch/main)  
**Infrastructure :** Domaines achetés chez Systalink/Datacloud, application hébergée sur un VPS Ubuntu externe.

---

## 1. Le Pitch Officiel en Une Phrase (One-Sentence Pitch)

> **« BANTUDEVLAB est une forge logicielle souveraine panafricaine qui héberge, protège par cryptographie Zero-Trust sans mot de passe et audite par IA locale le patrimoine numérique de l'Afrique, avec des domaines achetés chez Systalink/Datacloud et une application hébergée sur un VPS Ubuntu externe. »**

---

## 2. Déclinaisons Stratégiques en Une Phrase

### A. Formulation Décideurs & Jury CADEV 2026 (Impact & Souveraineté)
> *« BANTUDEVLAB offre aux gouvernements, banques et développeurs africains une alternative souveraine aux hyperscalers étrangers en leur proposant une plateforme de code durcie, avec des domaines achetés chez Systalink/Datacloud, une application hébergée sur un VPS Ubuntu externe, et alignée sur la Convention de Malabo. »*

### B. Formulation Technique & Cyber (Rigueur Ingénierie)
> *« BANTUDEVLAB unifie une forge Git distribuée sous Gitea CE, une authentification Schnorr NIZKP 2048 bits sans mot de passe, un scanner SAST d'entropie de Shannon aux normes SARIF 2.1.0 et un modèle d'aide à la revue IA Gemma 2 2B exécuté localement sans fuite de télémétrie. »*

### C. Formulation Développeurs (Adoption & Communauté)
> *« La forge logicielle conçue par des développeurs africains pour les développeurs africains, accessible sans mot de passe en 1 clic, synchronisée en 4 langues et protégée contre les coupures d'accès extraterritoriales. »*

---

## 3. Le Hook Éclair Oral (10 Secondes en Début de Soutenance)

> « Membres du jury : aujourd'hui, le code de l'Afrique réside majoritairement hors de ses frontières ; avec **BANTUDEVLAB**, nous favorisons l'autonomie technologique sur le sol africain, sécurisée par des protocoles cryptographiques Zero-Knowledge vérifiés et assistée par un modèle IA local. »

---

## 4. Stack Technique du Projet (Architecture Souveraine & Licences Permissives)

| Couche | Technologies & Outils | Rôle & Usage | Licence |
| :--- | :--- | :--- | :--- |
| **Noyau Applicatif & API** | Python 3.12 / Django 5.2 & DRF | Architecture backend, modèles de données, API REST et vues d'authentification | BSD-3-Clause |
| **Moteur Forge Git** | Gitea CE 1.22 (Go) | Moteur Git distribué, gestion des dépôts, branches, commits, PR et webhooks (utilisé tel quel) | MIT |
| **Cryptographie Zero-Trust** | Protocole Schnorr NIZKP (RFC 3526) | Preuves non-interactives Fiat-Shamir sur groupe 2048-bit, génération BIP-39 (12 mots), tokens Git signés, aucun mot de passe | code original de l'équipe, licence MIT |
| **Scanner de Sécurité SAST** | Python AST & Entropie Shannon | Détection de fuites de secrets ($H \ge 3.8$), détection de failles, calcul du score de souveraineté ADSS-v1, exports OASIS SARIF 2.1.0 et GitLab SAST | code original de l'équipe, licence MIT |
| **Assistant IA Local** | Google Gemma 2 2B & Ollama | Petit modèle local d'aide au développement et à la revue de code, inférence on-premise sans fuite de données | Ollama (MIT) / Gemma Terms Google (modèle local non redistribué) |
| **Base de Données** | SQLite (build standard) & PostgreSQL 16 (optionnel) | Base SQLite standard pour l'évaluation ; PostgreSQL et PgBouncer configurables pour la production | Domaine Public (SQLite) / PostgreSQL License |
| **Cache & Broker Async** | Valkey 7.2-alpine & Celery 5.6 | Cache distribué en mémoire (remplacement BSD-3 de Redis) et exécution des tâches périodiques/asynchrones | BSD-3-Clause |
| **Serveur Web & Reverse Proxy** | Nginx 1.27-alpine | Terminaison TLS 1.3, CSP stricte sans CDN externe (`default-src 'self'`), isolation et routage des services | 2-Clause BSD |
| **Frontend & UI / UX** | Vanilla JavaScript ES6+ & CodeMirror 5 | Éditeur de code intégré, terminal de commande pro sans saisie libre, composants SVG Primer (zéro emoji, zéro CDN) | MIT |
| **Internationalisation (i18n)** | GNU gettext (`.po` / `.mo`) | Traduction complète et synchronisation instantanée en 4 langues (Français, Anglais, Kiswahili, Portugais) | Permissif |
| **Intégrité & Audit Trail** | Chaînage cryptographique SHA-256 | Journal d'audit immuable (`previous_hash -> hash`) aligné sur la Convention de Malabo 2014 | code original de l'équipe, licence MIT |
| **Hébergement & Domaines** | VPS Ubuntu & Systalink / Datacloud | Domaines achetés chez Systalink/Datacloud (`cybersocle.site`, `git.cybersocle.site`), application hébergée sur un VPS Ubuntu externe | Infrastructure externe & Domaines Datacloud |
| **Qualité, Tests & CI/CD** | Pytest, Playwright, Ruff & Bandit | Suite de tests automatisés, tests E2E navigateur Chromium, linter PEP 8 et analyse SAST CI | MIT / Apache-2.0 |
