# Rapport d'Exactitude, Cohérence et Conformité — CADEV 2026 (`CADEV26/RAPPORT_EXACTITUDE.md`)

**Projet :** BANTUDEVLAB (Équipe CYBERSOCLE : OBIEY Christ Dany, capitaine ; MAMPOUYA Alicia Syrianne, présentation vidéo et parcours utilisateur ; GAMBOUE Ursie, présentatrice et parcours utilisateur)  
**Branche de travail :** `main` / `docker-cadev26` (commit `b1b1ebb`, tag `v1-cadev-submission`)  
**Date :** 15 novembre 2026

---

## 1. Synthèse des modifications effectuées (Tâches 1 à 12)

1. **Tâche 1 — Parcours évaluateur & frictions (`CADEV26/TEST_PARCOURS.md`)** :
   - Remplacement du message figé `Initialisation de la synchronisation avec Gitea...` sur `templates/core/home.html` par un état vide explicite avec liens vers `/dashboard/#new-repo` et `https://git.cybersocle.site/explore/repos`.
   - Invalidation des caches `bantudevlab_forge_repos_cache` et `gitea_repos_list` lors de la création d'un dépôt (`apps/gitea_client/views.py`) et fusion des dépôts `SovereignRepository` dans `get_cached_repositories()` (`apps/core/views.py`) afin que `demo-cadev-2026` apparaisse immédiatement dans `/dashboard/`.
   - Ajout d'un délai maximal côté serveur (35 s dans `apps/ai_assistant/gemma.py`) et d'un `AbortController` côté client (45 s dans `templates/core/dashboard.html`) affichant un message clair si Ollama ne répond pas.
   - Envoi de `X-CSRFToken` lors des appels `/api/zkp/challenge/` et `/api/zkp/verify/` dans `templates/zkp_auth/login.html`.

2. **Tâche 2 — Compte de démonstration (`cadev_evaluator`)** :
   - Vérification dans `apps/core/management/commands/init_sovereign_admin.py` : `is_staff=False`, `is_superuser=False`, `set_unusable_password()`, identité ZKP dérivée de `DEFAULT_DEMO_MNEMONIC`.
   - **Fonctionnement du bouton « Connexion Démo 1-Clic »** : Le bouton pré-remplit `cadev_evaluator` et le mnémonique de démonstration dans le navigateur, puis exécute **réellement** le protocole cryptographique Schnorr NIZKP (RFC 3526 MODP 2048 bits) : demande de nonce à `/api/zkp/challenge/`, calcul côté client de `(t, s)`, vérification serveur sur `/api/zkp/verify/`. Cela ne contredit pas l'authentification ZKP des autres comptes : aucune porte dérobée ni contournement de mot de passe n'existe ; seul un compte de démonstration strictement non privilégié et limité en quotas utilise une graine publique de test.
   - **Quotas & nettoyage automatique** : Pour `cadev_evaluator`, limitation à 20 dépôts actifs maximum, description limitée à 1024 octets (`apps/gitea_client/views.py`), purge automatique des dépôts > 24 h à la création et tâche périodique Celery Beat `cleanup-demo-repositories-hourly` (`apps/core/tasks.py`, `config/settings.py`).

3. **Tâche 3 — Dépôts visibles & intégrité des secrets** :
   - Ajout du dépôt `bantudevlab/bantudevlab` (public, avec `README.md`, licence `MIT`, lien de démo `https://cybersocle.site`) dans `scripts/init_forge_repos.py`.
   - Vérification de `git ls-files` et de l'historique complet (`git log --all --name-only`) : aucun fichier `.env`, clé privée ou secret exposé (seuls `.env.example`, `.env.production.example` et `CADEV26/ROTATION_SECRETS.md` sont présents).

4. **Tâche 4 — Une seule entrée claire** :
   - Redirection HTTP 301 de `forge.cybersocle.site` vers `https://git.cybersocle.site$request_uri` dans `deploy/nginx/bantudevlab.conf`.
   - Masquage de l'en-tête « Dépôts Hébergés » sur `forge_server.py` lorsqu'aucun dépôt réel n'est listé.

5. **Tâche 5 — Retrait de GitLab** :
   - Suppression des mentions GitLab (bouton « Espace GitLab », SSO OmniAuth, comptes GitLab, Merge Requests, `sovereign-abidjan`, `.gitlab-ci.yml`, `GitLab CE/EE`) dans `templates/base.html`, `templates/core/home.html`, `templates/core/dashboard.html`, `templates/core/faq.html`, `README.md`, `apps/core/tasks.py`, `apps/core/views.py`, `apps/gitea_client/views.py`, `apps/ai_assistant/gemma.py`, `forge_server.py`.
   - Archivage de `.gitlab-ci.yml` et `scripts/register_gitlab_runner.sh` vers `docs/archive/`.
   - *Note de transparence* : `gitlab/` et `apps/gitlab_client/` sont conservés dans l'arborescence uniquement pour ne pas casser les tests existants (`tests/test_docker_deployment.py` et `tests/test_gitlab_client.py`), et l'assertion `test_core_faq_view` dans `tests/test_api_and_views.py` a été alignée sur « Comment créer un compte ».

6. **Tâche 6 — Hébergement & carte des datacenters** :
   - Remplacement des affirmations Systalink Cloud, datacenters Tier-3/Tier-4, SLA, bande passante, « nœud central Abidjan », hébergement en Côte d'Ivoire/Sénégal par la mention exacte sur l'accueil, `/sovereignty-metrics/`, la FAQ et le pied de page : *« Application hébergée sur un VPS Ubuntu externe ; domaines acquis chez Datacloud. Déploiement souverain : objectif de la feuille de route. »*
   - Conservation de la carte (Dakar, Abidjan, Lagos, Kigali, Nairobi) sur `/sovereignty-metrics/` sous le titre explicite **« Topologie cible (projet) »**, avec mention **« Projet, non déployé »** sur chaque nœud, suppression des statuts actifs, latences en dur et certifications, et mesure en direct vers `/healthz` uniquement pour le serveur actuel.

7. **Tâche 7 — IA (Gemma 2 2B)** :
   - Remplacement de « Gemma 5B » par « Gemma 2 2B » dans la FAQ, `/sovereignty-metrics/`, `/dashboard/`, `static/js/bantu-command-terminal.js`, `apps/ai_assistant/views.py`, `apps/gitea_client/views.py`.
   - Retrait des mentions non vérifiables de fine-tuning LoRA/QLoRA en production.

8. **Tâche 8 — Absolus invérifiables** :
   - Retrait ou remplacement de « immunité totale face au CLOUD Act », « cryptographiquement inviolable », « 100 % », « garantie », « jamais » par des formulations factuelles et mesurables dans les templates et `README.md`.

9. **Tâche 9 — Liens, marque et accents** :
   - Remplacement de `git.bantudevlab.africa` par `git.cybersocle.site` (`templates/core/faq.html`, `apps/zkp_auth/tokens.py`).
   - Dans Gitea (`custom/conf/app.ini`, `custom/templates/custom/header.tmpl`, `custom/templates/custom/footer.tmpl`) : titre `BantuDevLab - Forge souveraine`, lien « Documentation » pointant vers `https://cybersocle.site/faq/`, suppression du lien cassé `http://localhost:6157/`, correction des accents (`Dépôts`, `Hébergés`, `Français`).

10. **Tâche 10 — Accueil (`templates/core/home.html`)** :
    - Ajout avant le jargon de la phrase : *« Hébergez votre code, connectez-vous sans mot de passe, faites analyser votre code par une IA locale. »*
    - Ajout de la section « Échange » pointant vers les dépôts/discussions (Issues/PR) et registres de paquets Gitea actifs (`https://git.cybersocle.site/explore/repos`). Les snippets (OpenGist) ne sont pas liés car non exposés publiquement.

11. **Tâche 11 — Sécurité de production** :
    - Vérification `config/settings.py` & `docker-compose.production.yml` : `DEBUG=False`, `SECURE_SSL_REDIRECT=True`, HSTS (1 an, subdomains, preload), `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `HttpOnly`, `SameSite=Strict`, `X_FRAME_OPTIONS="DENY"`, `SECURE_CONTENT_TYPE_NOSNIFF=True`, CSP active, CSRF actif.
    - Limitation de rythme ajoutée : `zkp_register` (`10/hour`) et `repo_create` (`60/hour` sur `POST /api/forge/repositories/`).
    - **Gitea 1.22.6 — Vulnérabilités connues & proposition de mise à jour (non appliquée)** :
      - La branche Gitea 1.22.6 corrige des failles antérieures (ex. CVE-2024-6886), mais des avis de sécurité plus récents concernent les versions non mises à jour (notamment épuisement de ressources `go-git < v5.13` dans certaines distributions 1.22, et des CVE critiques publiées sur les branches Gitea suivantes telles que CVE-2026-59774 lecture arbitraire de fichiers et CVE-2026-60004 RCE via hooks Git).
      - **Recommandation** : Planifier une mise à jour de l'image `gitea/gitea:1.22` vers la dernière version stable maintenue après sauvegarde complète (`scripts/backup_gitea.py`) et validation en pré-production.

12. **Tâche 12 — Responsivité multi-appareils & conformité finale** :
    - Masquage des boutons Pro injectés dans la barre supérieure sur `<= 768px` (Django) / `<= 1024px` (Gitea) et déplacement dans le menu tiroir mobile (`#navDrawer`) dans `static/js/bantu-command-terminal.js` et `custom/public/assets/js/bantu-command-terminal.js`.
    - Adaptation complète de la navbar dans `static/css/style.css` (`white-space: nowrap`, breakpoints `1460px`, `1240px`, `768px`) pour éviter tout débordement ou retour à la ligne de `320px` au grand bureau, et durcissement anti-débordement horizontal (`html, body { overflow-x: hidden; max-width: 100%; }`).
    - Marge inférieure mobile ajoutée au pied de page Gitea (`custom/templates/custom/footer.tmpl`) pour éviter le chevauchement avec le bouton flottant Copilot IA.
    - Ajout de la section Q12 dans `templates/core/faq.html` détaillant la conformité CADEV 2026 (Art. 6 et Annexe 1) et fusion des dépôts fallback dans `GET /api/forge/repositories/` (`apps/gitea_client/views.py`).
    - Validation locale complète : `scripts/check_licenses.py` (`63/63` paquets conformes), `scripts/check_no_emoji.py` (`OK`), `pytest -q` (`202 passed, 3 skipped, 43 subtests passed`, couverture `95,65 %`).

---

## 2. Résultats du parcours en production

Voir le détail complet dans [TEST_PARCOURS.md](TEST_PARCOURS.md) :
- **Étape 1 (Connexion 1-Clic `cadev_evaluator`)** : Succès (3,8 s chargement + 0,42 s preuve ZKP).
- **Étape 2 (FAQ & Métriques)** : Succès HTTP 200 (3,32 s et 2,18 s) ; débordement horizontal mobile (720 px sur 375 px) corrigé dans le code.
- **Étape 3 (Création `demo-cadev-2026`)** : Succès API HTTP 201 (1,08 s) ; anomalie d'affichage liste vide sur `/dashboard/` corrigée par invalidation de cache et fusion locale.
- **Étape 4 (Security Audit & Ask Gemma Review)** : Succès (1,21 s pour l'audit SAST, 16,4 s pour Gemma SSE).

---

## 3. Points « à vérifier » (côté déploiement VPS en production)

Les éléments suivants dépendent de l'état du serveur VPS externe et doivent être vérifiés / appliqués lors du redéploiement :
1. **Redéploiement des conteneurs et de Nginx sur le VPS** : appliquer les modifications de la branche `main` (incluant la redirection 301 `forge.cybersocle.site` -> `git.cybersocle.site`, `static/css/style.css`, `static/js/bantu-command-terminal.js`, et les templates `custom/` de Gitea) puis re-tester le parcours sans cache sur mobile (`375x812`).
2. **Visibilité publique du dépôt `bantudevlab` sur `https://git.cybersocle.site/explore/repos`** : lors du test en production, l'explorateur Gitea affichait `No matching results found.` pour un visiteur non connecté. **À vérifier** sur l'instance Gitea de production : rendre le dépôt `bantudevlab` public (ou exécuter `scripts/init_forge_repos.py` / créer le dépôt public via l'administration Gitea avec `README.md`, licence MIT et lien `https://cybersocle.site`). Accès jury garanti en parallèle via `cadev_evaluator` sur `https://cybersocle.site`.
3. **Modèle Ollama chargé en production** : **à vérifier** par `ollama list` sur le VPS que `gemma2:2b` est bien le modèle actif (aucun modèle fine-tuné personnalisé n'est revendiqué).
4. **Services Snippets (OpenGist)** : non exposés publiquement (`localhost:6157` uniquement) ; **à vérifier** si un déploiement public est souhaité ultérieurement.
