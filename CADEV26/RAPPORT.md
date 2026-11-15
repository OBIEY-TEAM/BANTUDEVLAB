# RAPPORT FINAL DE CONFORMITÉ & PLAN D'ACTION — CADEV 2026

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne (Présentation vidéo démo & parcours utilisateur)  
- **Membre de l'équipe :** GAMBOUE Ursie Semence (Présentatrice — Présentation vidéo démo & parcours utilisateur)  
**Organisateur & Événement :** SYSTALINK SENEGAL — Concours CADEV 2026  
**Date limite impérative :** Dimanche 15 novembre 2026 à 17 h 00 GMT  
**URL de Production :** https://cybersocle.site (Portail) / https://git.cybersocle.site (Forge Gitea CE)  
**Dépôt Source Officiel (Forge Souveraine Gitea) :** https://git.cybersocle.site/obiey-code/bantudevlab.git  
**Accès Public aux Commits (branche `main`) :** https://git.cybersocle.site/obiey-code/bantudevlab/commits/branch/main  
**Miroir GitHub de Continuité :** https://github.com/OBIEY-TEAM/BANTUDEVLAB  

---

## 1. Synthèse Globale des Réalisations (Tâches 1 à 8)

L'intégralité du dépôt BantuDevLab a été audité, durci et rendu rigoureusement conforme aux Articles 6 et 10 du règlement du concours CADEV 2026 :

### TÂCHE 1 — Audit exhaustif et remédiation des licences (Art. 6)
- **Élimination de toute licence copyleft contaminant :**
  - La bibliothèque `python-gitlab` (LGPL-3.0) a été totalement supprimée du projet et remplacée dans `apps/gitlab_client/client.py` par des appels directs à l'API REST via la bibliothèque `requests` (Apache-2.0).
  - Le pilote `psycopg2-binary` (LGPL-3.0) a été retiré de `requirements.txt`. Le projet s'exécute par défaut de manière 100% autonome sur le moteur SQLite standard (Domaine Public). Le support PostgreSQL de production reste documenté de façon optionnelle et isolée dans `requirements-postgres.txt`.
  - Redis >= 7.4 (sous double licence non libre RSALv2 / SSPLv1) a été remplacé par **Valkey 7.2** (BSD-3-Clause, projet Linux Foundation).
- **Séparation des dépendances :** Scission nette entre `requirements.txt` (exécution de production, 12 paquets directes + transitives 100% permissives) et `requirements-dev.txt` (tests et outillage).
- **Garde-fou CI automatisé :** Création de `scripts/check_licenses.py` intégré dans les workflows CI GitHub et Gitea, bloquant tout ajout futur d'un paquet sous GPL, AGPL, LGPL, SSPL ou BUSL.
- **Dossiers spécifiques inspectés :** Vérification de `gitlab/`, `forge_data/`, `finetuning/`, `custom/`, `figma_export/` : aucun poids de modèle n'est embarqué dans Git et tout le code d'ingénierie est du code original sous licence MIT. Documenté dans `CADEV26/LICENSES_AUDIT.md`.

### TÂCHE 2 — Assainissement des secrets et durcissement sécurité
- **Scan de l'historique :** Audit de l'historique Git à la recherche de secrets et de tokens.
- **Plan de rotation documenté :** Rédaction de `CADEV26/ROTATION_SECRETS.md` avec inventaire des variables sensibles et plan d'exécution `git filter-repo` conservant l'intégrité des dates d'origine (sans exécution non confirmée).
- **Suppression des identifiants en dur :** Retrait de tous les mots de passe administrateurs en dur dans les commandes de gestion et les fichiers compose. Provisionnement délégué aux variables d'environnement (`BANTU_ADMIN_USER`, `BANTU_ADMIN_PASSWORD`).
- **Compte démo sécurisé :** Création d'un compte non-privilégié `cadev_evaluator` (`is_staff=False`, `is_superuser=False`, mot de passe inutilisable, accès ZKP sans mot de passe).
- **Paramètres de production vérifiés :** DEBUG désactivé par défaut, ALLOWED_HOSTS restreint, HSTS sur 1 an, cookies Secure/HttpOnly/Strict, CSRF et CSP stricte sans appel CDN externe.

### TÂCHE 3 — Fichiers de licence officiels
- **LICENSE :** Texte MIT officiel intact à la racine, attribuant la titularité aux deux membres de l'Équipe CYBERSOCLE : OBIEY Christ Dany (Capitaine) et MAMPOUYA Alicia Syrianne.
- **THIRD_PARTY_LICENSES.md :** Tableau exhaustif à la racine répertoriant tous les composants tiers et leurs licences permissives.
- **NOTICE :** Précision formelle à la racine indiquant que Gitea CE 1.22 (MIT) est utilisé tel quel sans modification de code source, Valkey 7.2 (BSD-3-Clause), CodeMirror 5 (MIT), et les conditions d'utilisation de Gemma 2 2B.

### TÂCHE 4 — Documents, pitch et archivage
- **Fusion et nettoyage :** Répertoire unifié `CADEV26/`. Déplacement de tous les documents de travail et brouillons (`backlod.md`, `intervension.md`, `intervention.md`, `scratch/`, `TASK/`, `CADEV2026/`) vers `docs/archive/`.
- **Alignement factuel :** Correction de la date limite officielle (15 novembre 2026 à 17 h 00 GMT). Précision de l'hébergement : « domaines achetés chez Systalink/Datacloud, application hébergée sur un VPS Ubuntu externe ». Suppression de « 100% permissive » (Gemma sous Google Gemma Terms). Remplacement de « Propriétaire CYBERSOCLE » par « code original de l'équipe, licence MIT ». Remplacement des qualificatifs excessifs par des formulations techniques vérifiables, et mention de conformité « alignée sur la Convention de Malabo 2014 ».

### TÂCHE 5 — Historique factuel et originalité du code
- **Relevé objectif dans `CADEV26/HISTORIQUE.md` :**
  - Date du premier commit : 31 octobre 2026 à 11:14:31 GMT.
  - Commits antérieurs au 29 septembre 2026 : **ZÉRO (0 commit)**.
  - Nombre total de commits : 326 commits documentés (dont 325 commits techniques jusqu'à `502f2b1` et 1 commit documentaire `b1b1ebb`).
  - Décomposition claire : composants tiers éprouvés non modifiés (Gitea 0%, Valkey 0%, Nginx 0%, Ollama 0%) vs code original développé par l'équipe (~4 632 lignes Python, ~6 000 lignes templates/UI, scripts et tests).

### TÂCHE 6 — Mesure réelle des tests et correction des métriques
- **Couverture réelle démontrée :** **95,65 %** sur les modules applicatifs cibles (`apps/zkp_auth`, `apps/security_scanner`, `apps/ai_assistant`), au-dessus du seuil requis de 94%.
- **Suite de tests :** 202 tests passés avec succès (3 ignorés, 43 sous-tests validés).
- **Correction des assets :** Élimination des balises orphelines dans `templates/core/dashboard.html` pour garantir 100% de succès sur `test_static_assets.py`.
- **Langues effectives :** 4 langues fonctionnelles compilées (`fr`, `en`, `sw`, `pt`).
- **Workflows Gitea Actions :** Documentation détaillée du statut « en attente » causé par l'absence d'instance `act_runner` connectée, avec guide de configuration pas à pas.

### TÂCHE 7 — Fiche officielle de soumission (`CADEV26/SOUMISSION.md`)
- Rdaction complète et rigoureuse respectant les critères a) à g) : présentation, engagement de titularité avec champs vides pour OBIEY Christ Dany et MAMPOUYA Alicia Syrianne, tableau de licences conforme Art. 6, déclaration IA (modèle local Gemma 2 2B sous Google Gemma Terms, aide à la revue sans remplacer le développeur, maîtrise du code), architecture de déploiement, preuve d'achat Datacloud réservée, et déclaration de code antérieur conforme à la Tâche 5.

### TÂCHE 8 — Parcours de démo sans friction (`CADEV26/DEMO_GUIDE.md`)
- Guide complet pour juré non technique : accueil, connexion ZKP 1-clic avec `cadev_evaluator`, consultation de la FAQ, création autonome de dépôt.
- **3 exemples concrets de revue de code pour Gemma 2 2B :** Détection de fuite de clé API ($H \ge 3.8$), détection de faille d'injection SQL par concaténation, et fonction utilitaire à sécuriser avec typage et gestion de division par zéro.

---

## 2. Ce qui reste Bloquant ou à Surveiller

1. **Absence de toute licence interdite dans le build standard :**
   Le build de soumission standard (exécutable avec `requirements.txt` et SQLite) ne contient **aucune licence GPL, AGPL ou LGPL**. La conformité stricte avec l'Article 6 est totale.
2. **Pilote PostgreSQL optionnel (`requirements-postgres.txt`) :**
   Bien que SQLite soit le moteur par défaut soumis, les déploiements de très grande envergure utilisent PostgreSQL. Or, tous les pilotes Python/Django pour PostgreSQL (`psycopg2`, `psycopg3`) sont sous licence LGPL. Ce composant est maintenu hors du build d'évaluation dans un fichier optionnel documenté.
3. **Statut des Conditions d'Utilisation du Modèle Gemma 2 2B :**
   Gemma 2 2B est régi par les *Google Gemma Terms of Use*. Il est exécuté exclusivement en local via Ollama sans redistribution des poids dans Git. Il ne s'agit pas d'une licence permissive OSI standard, mais d'un usage d'inférence locale on-premise conforme aux CGU de Google.

---

## 3. Actions Indispensables à la Charge de l'Équipe CYBERSOCLE (Actions Humaines)

Avant l'heure limite du **dimanche 15 novembre 2026 à 17 h 00 GMT**, les membres de l'équipe CYBERSOCLE doivent impérativement accomplir les démarches suivantes :

### Action 1 : Rotation effective des secrets en production
- Sur le serveur VPS Ubuntu externe de production, générer un nouveau secret Django `SECRET_KEY` cryptographiquement sûr (`python -c "import secrets; print(secrets.token_urlsafe(50))"`).
- Renouveler les mots de passe de base de données PostgreSQL et les tokens de connexion Gitea dans le fichier `/srv/bantudevlab/.env.production`.
- Redémarrer la pile de conteneurs : `docker compose -f docker-compose.production.yml up -d --force-recreate`.
- *Rappel : Ne jamais commiter de secret réel dans le dépôt Git.*

### Action 2 : Signatures et confirmation des déclarations
- Ouvrir [`CADEV26/SOUMISSION.md`](file:///c:/Users/User/Desktop/AGENT/BANTUDEVLAB/CADEV26/SOUMISSION.md) à la section **b)**.
- Renseigner la date et faire apposer la signature ou mention « Lu et approuvé » par chaque membre :
  - **OBIEY Christ Dany** (Capitaine d'équipe)
  - **MAMPOUYA Alicia Syrianne** (Membre d'équipe)
  - **GAMBOUE Ursie Semence** (Membre d'équipe)
- Renseigner les outils d'assistance au développement utilisés par l'équipe à la section **d.2**.

### Action 3 : Justificatif et référence de commande Datacloud
- Se connecter à l'espace client **Systalink / Datacloud**.
- Récupérer le numéro de référence de commande et la facture d'achat du nom de domaine `cybersocle.site`.
- Compléter les sections **e.2** et **f)** de `CADEV26/SOUMISSION.md` avec ces références et insérer la copie du justificatif.

### Action 4 : Envoi du dossier de soumission avant 17 h 00 GMT
Transmettre le dossier officiel par email avant le **15 novembre 2026 à 17 h 00 GMT** :
- **Destinataire :** `cadev@systalink.com`
- **Copie (CC) :** Les membres de l'équipe CYBERSOCLE
- **Objet :** `[CADEV 2026] Soumission Officielle — BantuDevLab — Équipe CYBERSOCLE`
- **Contenu du mail :**
  - Liens vers le dépôt officiel Gitea : `https://git.cybersocle.site/obiey-code/bantudevlab.git`
  - Lien vers le miroir GitHub : `https://github.com/OBIEY-TEAM/BANTUDEVLAB`
  - URL de démonstration en ligne : `https://cybersocle.site`
  - Mention expresse du tag de soumission officiel : `v1-cadev-submission`
  - Fiche de soumission `CADEV26/SOUMISSION.md` signée en pièce jointe ou corps de message.

### Action 5 : Participation obligatoire au vote des pairs
- Chaque membre inscrit de l'équipe (**OBIEY Christ Dany**, **MAMPOUYA Alicia Syrianne** et **GAMBOUE Ursie Semence**) doit impérativement participer à la session de vote des pairs organisée par Systalink conformément au règlement du concours.

### Action 6 : Questions formelles à poser à Systalink (`cadev@systalink.com`)
Pour sécuriser le dossier sur le plan juridique, poser par écrit les 3 questions de confirmation suivantes :
1. *Pilote de base de données :* « L'Article 6 proscrit la LGPL. Le build standard soumis utilise SQLite natif (Domaine Public). Nous avons documenté de façon optionnelle `psycopg2-binary` (LGPL) pour PostgreSQL de grande envergure. Pouvez-vous confirmer que cette isolation hors build standard est pleinement conforme ? »
2. *Modèle IA local :* « Nous utilisons Gemma 2 2B en inférence locale on-premise sans redistribution de poids sous les Google Gemma Terms. Pouvez-vous confirmer que cet usage applicatif local est bien accepté comme technologie tierce ? »
3. *Propriété intellectuelle :* « Le code original de BantuDevLab est sous licence permissive MIT. Pouvez-vous confirmer que l'équipe CYBERSOCLE conserve l'entière propriété intellectuelle de ses développements en cas de sélection parmi les lauréats ? »
