# RAPPORT FINAL DE CONFORMITÉ & PLAN D'ACTION — CADEV 2026

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne  
**Organisateur & Événement :** Systalink Cloud — Concours CADEV 2026  
**Date limite impérative :** Dimanche 15 novembre 2026, 23h59 GMT (heure de Dakar)  
**URL de Production :** https://cybersocle.site / https://git.cybersocle.site  
**Dépôt Officiel :** https://github.com/OBIEY-TEAM/BANTUDEVLAB  

---

## 1. Synthèse Globale des Réalisations (Ce qui a été fait)

L'intégralité du dépôt BantuDevLab a été audité, durci et aligné avec le règlement officiel du concours CADEV 2026 sans altération de la logique métier applicative :

### TÂCHE 1 — Audit exhaustif des licences logicielles (`CADEV26/LICENSES_AUDIT.md`)
- **Inventaire complet :** 66 dépendances directes et transitives Python analysées par introspection `importlib.metadata` et `pip-licenses`, ainsi que l'ensemble des briques d'infrastructure (Gitea, PostgreSQL, Nginx, PgBouncer, Ollama) et de frontend (CodeMirror 5 auto-hébergé, scripts internes CYBERSOCLE).
- **Zéro dépendance aux CDN tiers :** Tous les styles Primer, icônes vectorielles SVG et scripts CodeMirror sont embarqués localement.
- **Remplacement immédiat et sans risque de Redis :** Depuis sa version 7.4, Redis n'est plus distribué sous licence open-source BSD libre (passage sous double licence RSALv2 / SSPLv1 incompatible CADEV). Le service a été immédiatement basculé dans `docker-compose.yml` et `docker-compose.production.yml` vers **Valkey 7.2-alpine** (fork sous gouvernance de la Linux Foundation, distribué sous licence permissive **BSD-3-Clause** stricte). Valkey est un remplaçant direct 100% compatible protocolairement avec Celery et Django-Redis.
- **Identification des composants bloquants :** `psycopg2-binary` (LGPLv3) et `python-gitlab` (LGPLv3) ont été cartographiés avec leurs alternatives permissives prêtes à l'emploi (`pg8000` BSD-3 / SQLite pour la base de données, requêtes REST HTTP `requests` Apache-2.0 pour GitLab).
- **Modèle IA Gemma 2 2B :** Statut clarifié selon les conditions d'utilisation Google (non qualifié de permissif, exécuté localement sous conteneur Ollama MIT sans redistribution des poids dans le code source).

### TÂCHE 2 — Fichier LICENSE à la racine
- Fichier `LICENSE` sous licence permissive **MIT** standard ajouté à la racine du dépôt.
- Titularité attribuée à l'**Équipe CYBERSOCLE** : **OBIEY Christ Dany (Capitaine)** et **MAMPOUYA Alicia Syrianne**.

### TÂCHE 3 — Fiche officielle de soumission (`CADEV26/SOUMISSION.md`)
- Document structuré respectant scrupuleusement les points **a)** à **f)** exigés par le règlement de Systalink :
  - **a) Présentation :** Enjeux de cyber-souveraineté africaine, convention de Malabo, architecture Django + Gitea CE + ZKP Schnorr + SAST Shannon + IA locale Gemma 2 2B.
  - **b) Déclaration de titularité :** Conception indépendante hors mission d'employeur, client ou école, avec tableau d'engagement pour les deux membres de l'équipe CYBERSOCLE (OBIEY Christ Dany [Capitaine] et MAMPOUYA Alicia Syrianne).
  - **c) Composants & licences :** Tableau exhaustif reproduisant l'audit de licences.
  - **d) Déclaration IA :** Précision sur l'inférence locale Gemma 2 2B, utilisation des outils d'aide au développement (Claude Code, Antigravity AI, GitHub Copilot) et maîtrise intégrale du code source par l'équipe.
  - **e) Déploiement :** Domaines `cybersocle.site` / `git.cybersocle.site` (Systalink / Datacloud) et cluster conteneurisé sur VPS Hostinger.
  - **f) Historique Git :** 257 commits documentés depuis le premier commit du 31 octobre 2026 (`b0fa102ec01065d0b9a788363b3d4c03b2f99535`).

### TÂCHE 4 — Vérification rigoureuse des affirmations et métriques
- **Correction du modèle IA :** Élimination de l'affirmation inexacte "Gemma 5B" dans la page d'accueil (`templates/core/home.html`) et le tableau de bord (`templates/core/dashboard.html`), remplacée par la spécification réelle et démontrable : **Gemma 2 2B (2 milliards de paramètres)**.
- **Vérification de la couverture de tests :** Suite Pytest exécutée (201 tests automatisés). Ajout de tests ciblés sur les branches d'erreurs ZKP et IA Copilot dans `tests/test_qa_coverage.py` assurant une couverture réelle mesurée de **95.6%** sur les modules applicatifs cibles (`apps/zkp_auth`, `apps/security_scanner`, `apps/ai_assistant`). Seuil minimal CI configuré à 94% dans `pyproject.toml` pour éliminer tout faux-positif lié aux arrondis.
- **Multilinguisme certifié :** Vérification de l'implémentation effective des 4 langues déclarées : Français (`fr`), Anglais (`en`), Kiswahili (`sw`), Portugais (`pt`), toutes pourvues de leurs catalogues compilés `.mo` dans `locale/`.

### TÂCHE 5 — Parcours de démonstration pour évaluateur non technique
- **Compte démo préconfiguré :** Création du compte utilisateur `cadev_evaluator` (email: `evaluator@cadev2026.africa`, mot de passe: `CadevEvaluator2026!`, juridiction: `SEN` / Sénégal, clé publique ZKP enregistrée et validée).
- **Connexion ZKP en 1 clic :** Ajout d'une bannière interactive sur `/api/zkp/login-ui/` avec bouton « Connexion Démo 1-Clic » exécutant automatiquement le protocole Schnorr NIZKP (Fiat-Shamir) avec affichage instantané des étapes cryptographiques et feedback vert de validation. Prise en charge du paramètre d'URL `?demo=cadev` depuis la page d'accueil.
- **Guide dédié dans la FAQ :** Accordéon ouvert par défaut en tête de la FAQ (`/faq/`) guidant l'évaluateur en 4 étapes claires.
- **Création autonome de dépôt de démo :** Ajout sur le tableau de bord (`/dashboard/`) d'un bouton et d'une fenêtre modale intuitive « Créer un Dépôt de Démonstration ». Un évaluateur non technique peut en 2 clics renseigner un nom (ex: `demo-cadev-sovereign`) et initialiser le dépôt sur la forge Gitea. L'action est reliée à l'API `/api/forge/repositories/` (testée avec succès, retour HTTP 201 Created) et le nouveau dépôt apparaît immédiatement dans le tableau de bord sans intervention technique.

---

## 2. Ce qui reste Bloquant au Regard du Règlement CADEV 2026

Le règlement stipule qu'aucun composant sous licence GPL, AGPL ou LGPL ne doit être présent. Deux bibliothèques Python spécifiques restent sous licence LGPL dans l'environnement :

1. **`psycopg2-binary` (LGPL-3.0-or-later with exceptions) :**
   - **Rôle :** Pilote officiel de connexion PostgreSQL pour le framework Django.
   - **Statut :** Composant standard indispensable à l'ORM Django en production. Remplacer ce pilote par `pg8000` (BSD-3) ou basculer vers SQLite à quelques jours de la date limite fait courir un risque majeur de régression sur les transactions concurrentes et les migrations.
   - **Recommandation :** Documenter cette dépendance technique comme une exception standard de l'écosystème Django et solliciter la tolérance du jury CADEV via `cadev@systalink.com`.

2. **`python-gitlab` (LGPL-3.0-or-later) :**
   - **Rôle :** SDK client utilisé dans `apps/gitlab_client/client.py` pour la fédération optionnelle avec GitLab CE.
   - **Statut :** Le code dispose déjà d'un mode de secours natif s'appuyant directement sur la bibliothèque `requests` (Apache-2.0).
   - **Recommandation :** Si le jury refuse formellement toute exception LGPL, finaliser le basculement complet de `apps/gitlab_client/client.py` vers `requests` et supprimer `python-gitlab` de `requirements.txt`.

3. **Conditions d'utilisation du modèle Google Gemma 2 2B :**
   - **Statut :** Régie par les *Gemma Terms of Use* (Google). Non permissif au sens strict OSI, mais exécuté de façon 100% autonome et locale via Ollama (licence MIT), sans redistribution des poids dans le dépôt de BantuDevLab.

---

## 3. Ce que l'Équipe CYBERSOCLE Doit Faire Elle-Même (Actions Indispensables)

Avant le **dimanche 15 novembre 2026 à 23h59 GMT (heure de Dakar)**, les membres de l'équipe CYBERSOCLE doivent accomplir les démarches suivantes qui relèvent de leur responsabilité humaine, contractuelle et financière :

### Action 1 : Justificatif et Achat Systalink / Datacloud
1. Se connecter à l'espace client **Systalink / Datacloud**.
2. Récupérer le numéro de commande officiel et la facture d'achat du nom de domaine `cybersocle.site` (et/ou du pack cloud Systalink).
3. Ouvrir le fichier [`CADEV26/SOUMISSION.md`](file:///c:/Users/User/Desktop/AGENT/BANTUDEVLAB/CADEV26/SOUMISSION.md) à la section **e.2** et renseigner les champs :
   - `Numéro de référence de commande du domaine / service : [Indiquer le numéro Datacloud]`
   - `Date de souscription : [Indiquer la date d'achat]`
   - `Identifiant client Datacloud : [Indiquer votre ID client]`

### Action 2 : Déclarations de Titularité et Signatures de l'Équipe
1. Ouvrir le fichier [`CADEV26/SOUMISSION.md`](file:///c:/Users/User/Desktop/AGENT/BANTUDEVLAB/CADEV26/SOUMISSION.md) à la section **b)**.
2. Le tableau comporte déjà l'identité officielle des membres de l'équipe CYBERSOCLE :
   - **OBIEY Christ Dany** (Capitaine d'équipe, Porteur de projet & Lead Architect / Fullstack)
   - **MAMPOUYA Alicia Syrianne** (Membre d'équipe, Ingénierie logicielle / QA & Sécurité)
3. Faire apposer par chaque membre sa signature finale (mention manuscrite ou électronique « Lu et approuvé »).
4. Le fichier [`LICENSE`](file:///c:/Users/User/Desktop/AGENT/BANTUDEVLAB/LICENSE) à la racine du dépôt a été actualisé au nom de l'Équipe CYBERSOCLE (OBIEY Christ Dany [Capitaine], MAMPOUYA Alicia Syrianne).

### Action 3 : Envoi du Dossier Officiel par Email à Systalink
Transmettre la candidature officielle avant l'heure limite par courrier électronique :
- **Destinataire :** `cadev@systalink.com`
- **Copie (CC) :** Tous les membres de l'équipe CYBERSOCLE
- **Objet :** `[CADEV 2026] Soumission Dossier de Candidature — BantuDevLab — Équipe CYBERSOCLE`
- **Corps de message recommandé :**
  ```text
  Madame, Monsieur les membres du Jury CADEV 2026,

  L'équipe CYBERSOCLE a l'honneur de vous soumettre la candidature officielle du projet BANTUDEVLAB (Forge Logicielle Souveraine Panafricaine) au concours CADEV 2026 organisé par Systalink Cloud.

  1. Liens d'accès à la solution en ligne :
     - Portail Souverain BantuDevLab : https://cybersocle.site
     - Forge Git Gitea CE : https://git.cybersocle.site
     - Dépôt de code source public : https://github.com/OBIEY-TEAM/BANTUDEVLAB

  2. Parcours d'évaluation sans friction (Compte Démo CADEV 2026) :
     - Connexion 1-clic : https://cybersocle.site/api/zkp/login-ui/?demo=cadev
     - Identifiant démo : cadev_evaluator (Authentification mathématique Schnorr NIZKP)
     - Tableau de bord & Création de dépôt : https://cybersocle.site/dashboard/
     - Guide d'utilisation & FAQ : https://cybersocle.site/faq/

  3. Justificatif d'usage Systalink / Datacloud :
     - Nom de domaine de production acheté et géré via Systalink / Datacloud : cybersocle.site
     - Référence de commande Datacloud : [Votre numéro de commande]

  Vous trouverez ci-joint les documents réglementaires :
  - CADEV26/SOUMISSION.md (Fiche officielle dument complétée et signée)
  - CADEV26/LICENSES_AUDIT.md (Audit exhaustif des 66 dépendances et briques d'infrastructure)
  - CADEV26/RAPPORT.md (Rapport technique final et état de conformité)

  Restant à votre entière disposition pour toute démonstration complémentaire.

  Très cordialement,
  L'Équipe CYBERSOCLE :
  - OBIEY Christ Dany (Capitaine d'équipe & Lead Architect / Fullstack - obieychristdany@gmail.com)
  - MAMPOUYA Alicia Syrianne (Membre d'équipe - Ingénierie logicielle / QA & Sécurité)
  ```
- **Pièces jointes obligatoires à attacher au courriel :**
  1. `CADEV26/SOUMISSION.md` (converti en PDF ou au format Markdown dument signé)
  2. `CADEV26/LICENSES_AUDIT.md`
  3. `CADEV26/RAPPORT.md`
  4. La facture ou capture d'écran du reçu de commande Datacloud / Systalink.

---

## 4. Éléments Non Vérifiables par l'Assistant (Transparence Absolue)

Conformément à la règle d'intégrité (« *ne devine pas, signale ce que tu ne peux pas vérifier* ») :
1. **Facturation Datacloud :** L'assistant n'a pas accès au compte bancaire ni au portail privé client Systalink de l'équipe pour extraire le numéro de facture ou le bon de commande.
2. **Identité légale des membres :** Les membres de l'équipe CYBERSOCLE sont désormais formellement enregistrés : OBIEY Christ Dany (Capitaine) et MAMPOUYA Alicia Syrianne.
3. **Position discrétionnaire du jury sur `psycopg2` :** Seul le comité d'organisation CADEV 2026 (`cadev@systalink.com`) est habilité à valider l'exception pour le pilote de base de données PostgreSQL de Django.
