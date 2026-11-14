# Relevé Factuel de l'Historique Git & Originalité du Code — BANTUDEVLAB

> **Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
> **Équipe candidate :** CYBERSOCLE  
> - **Capitaine d'équipe :** OBIEY Christ Dany  
> - **Membre de l'équipe :** MAMPOUYA Alicia Syrianne  
> **Date du relevé :** 14 novembre 2026  
> **Source des données :** Historique Git du dépôt (`git log`) et arborescence du projet.  
> **Règle méthodologique appliquée :** Aucune conclusion subjective ; relevé strict et exhaustif des faits vérifiables.

---

## 1. Chronologie et Dates Clés du Dépôt Git

- **Date et heure du premier commit :**  
  `2026-10-31 11:14:31 +0100` (SHA: `23945e2` / `62062f2`)
- **Date et heure du dernier commit analysé :**  
  `2026-11-14 12:32:42 +0100` (SHA: `502f2b1`)
- **Nombre total de commits enregistrés :**  
  `325` commits
- **Code antérieur au 29 septembre 2026 (Article 6 du règlement CADEV 2026) :**  
  `0` commit.  
  Aucun fichier, commit ou branche n'est antérieur au 29 septembre 2026. L'intégralité du travail consigné dans l'historique Git a débuté le 31 octobre 2026.

---

## 2. Répartition des Commits par Auteur

Les commits de l'historique se répartissent comme suit entre les identités de validation utilisées par l'équipe :

| Auteur déclaré dans Git | Email Git | Nombre de commits | Pourcentage |
| :--- | :--- | :---: | :---: |
| **obiey** | `obieychristdany@gmail.com` | 229 | 70,5 % |
| **obieydany-code** | `286418433+obieydany-code@users.noreply.github.com` & `obieydany@gmail.com` | 79 | 24,3 % |
| **obiey christ dany** | `admin_noisim@srv1825963.hstgr.cloud` | 11 | 3,4 % |
| **OBIEY Christ Dany** | `obieychristdany@gmail.com` & `obieydany@gmail.com` | 6 | 1,8 % |
| **Total** | — | **325** | **100,0 %** |

---

## 3. Répartition des Commits par Semaine

| Semaine ISO | Intervalle Calendrier | Nombre de commits | Principaux chantiers réalisés |
| :--- | :--- | :---: | :--- |
| **2026-W44** | 26 octobre 2026 – 01 novembre 2026 | 15 | Création du dépôt, squelette Django, intégration initiale Gitea et premier module ZKP |
| **2026-W45** | 02 novembre 2026 – 08 novembre 2026 | 238 | Industrialisation des 6 axes, durcissement Zero-Trust, scanner SAST, assistant IA local Gemma 2 2B, intégration Docker et composition de production |
| **2026-W46** | 09 novembre 2026 – 15 novembre 2026 | 72 | Audit et remédiation des licences (CADEV 2026 Art. 6), assainissement des identifiants, exactitude et parcours évaluateur, barre de navigation verticale à droite, i18n inter-domaines et correctifs forge Gitea |

---

## 4. Part du Code Issue de Composants Existants vs Code Original de l'Équipe

### 4.1 Composants Tiers Utilisés Tels Quels (Sans Modification du Code Source)
- **Moteur Git Gitea Community Edition (Gitea CE) :**  
  - Version : `1.22` (binaire officiel compilé en Go, image Docker `gitea/gitea:1.22`).  
  - Modification du code source Go : **0 %** (utilisé tel quel, orchestré via son API REST et des webhooks).
- **Moteur de Cache et Broker Valkey :**  
  - Version : `7.2-alpine` (image officielle Linux Foundation).  
  - Modification : **0 %** (utilisé tel quel en remplacement BSD-3 de Redis).
- **Serveur Web Nginx :**  
  - Version : `1.27-alpine`.  
  - Modification : **0 %** (seuls des fichiers de configuration de virtual host ont été rédigés).
- **Base de Données PostgreSQL :**  
  - Version : `16-alpine`.  
  - Modification : **0 %** (SGBD standard).
- **Moteur d'Inférence IA Ollama & Modèle Google Gemma 2 2B :**  
  - Version : `ollama:latest` et modèle `gemma2:2b`.  
  - Modification : **0 %** (logiciel standard d'inférence locale).

### 4.2 Code Original Conçu et Développé par l'Équipe CYBERSOCLE
- **Couche Applicative et Logique Métier Django (`apps/`) :**  
  - `apps/zkp_auth/` : Cryptographie Schnorr ZKP sur groupe RFC 3526 MODP 2048-bit, génération mnémonique BIP-39, émission de tokens Git CLI signés.
  - `apps/security_scanner/` : Moteur SAST d'analyse d'AST Python, calcul d'entropie de Shannon ($H \ge 3.8$), détection de failles OWASP/CWE, sérialiseurs SARIF 2.1.0.
  - `apps/ai_assistant/` : Client d'inférence locale Gemma 2 2B, pipeline de revue de code asynchrone Celery, assainissement des secrets et PII.
  - `apps/gitea_client/` : Client HTTP REST souverain vers la forge Gitea CE, circuit breaker et gestion de cache distribué (`apps/gitlab_client/` conservé uniquement pour compatibilité des tests existants, non exposé en production).
  - `apps/core/` : Middleware de sécurité, audit trail immuable à chaînage SHA-256 aligné sur la Convention de Malabo, sélecteur multilingue i18n (Français, Anglais, Kiswahili, Portugais).
  - Volume : `4 632` lignes de code Python (mesuré hors tests et migrations).
- **Templates, Assets et Personnalisation UI (`templates/`, `custom/`) :**  
  - Templates HTML du portail central et du Workbench souverain.
  - Feuilles de style CSS pour le support complet des modes sombre et clair (`static/css/style.css`).
  - Terminal de commande interactif (`static/js/bantu-command-terminal.js` et `custom/public/assets/js/bantu-command-terminal.js`).
  - Tracés d'icônes SVG intégrés (`apps/core/templatetags/icons.py`).
- **Scripts et Automatisation CI/CD (`scripts/`, `.github/workflows/`, `.gitea/workflows/`) :**  
  - Script de contrôle des licences `scripts/check_licenses.py`.
  - Script de vérification de la politique zéro emoji `scripts/check_no_emoji.py`.
  - Pipelines GitHub Actions et Gitea Actions compatibles.
