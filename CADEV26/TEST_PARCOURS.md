# Rapport de Test du Parcours Évaluateur CADEV 2026 (`CADEV26/TEST_PARCOURS.md`)

Date du test : 13 novembre 2026  
Environnement testé : Production (`https://cybersocle.site`, `https://git.cybersocle.site`, `https://forge.cybersocle.site`)  
Conditions : Navigateur sans cache, affichage Desktop (`1440x900`) et Mobile (`375x812`).

---

## Résultats des 4 étapes sur la production

### Étape 1 : Connexion Zero-Trust immédiate (« Connexion Démo 1-Clic »)
- **Statut** : Succès (fonctionnel)
- **Durée** : 3,8 s (chargement initial `/api/zkp/login-ui/?demo=cadev&lang=fr&theme=light`) + 0,42 s (génération et validation de la preuve ZKP pour `cadev_evaluator`).
- **Messages observés** :
  - `Vérification Zero-Knowledge Réussie`
  - `Identité : cadev_evaluator | Algorithme : Schnorr Sigma Protocol`
- **Frictions observées** :
  - Sur l'accueil (`https://cybersocle.site/?lang=fr&theme=light`), la section « Dépôts Souverains Récents » restait figée sur `Initialisation de la synchronisation avec Gitea...` lorsque la liste de dépôts était vide.
  - Appels `POST /api/zkp/challenge/` retournant `403 Forbidden` lorsque l'en-tête `X-CSRFToken` n'était pas joint avec une session existante.

### Étape 2 : Consultation de la FAQ et conformité (`/faq/` et `/sovereignty-metrics/`)
- **Statut** : Succès
- **Durée** : 3,32 s (`/faq/`), 2,18 s (`/sovereignty-metrics/`), HTTP 200 OK.
- **Frictions observées (Mobile `375x812`)** :
  - Débordement horizontal de la barre de navigation sur mobile (largeur mesurée 720 px sur un écran de 375 px) dû aux boutons « Run Security Audit » et « Ask Gemma Review » injectés dans le header.

### Étape 3 : Création d'un dépôt de démonstration (`demo-cadev-2026`)
- **Statut** : Succès API (`POST /api/forge/repositories/` -> HTTP 201 Created), friction d'affichage sur `/dashboard/`.
- **Durée** : 1,08 s.
- **Frictions observées** :
  - Après fermeture de la modale et rechargement, `/dashboard/` affichait toujours `Aucun dépôt détecté sur le cluster Gitea local.` (compteur à `0`) car le cache `bantudevlab_forge_repos_cache` n'était pas invalidé et les dépôts privés créés dans `SovereignRepository` n'étaient pas fusionnés avec la recherche publique Gitea.

### Étape 4 : « Run Security Audit » et « Ask Gemma Review »
- **Statut** : Succès
- **Durée** :
  - « Run Security Audit » (entropie de Shannon / SAST) : 1,21 s (6 vulnérabilités détectées sur `workbench_security_audit.py`).
  - « Ask Gemma Review » (streaming SSE `/api/ai/review/`) : 16,4 s (HTTP 200 OK).
- **Frictions observées** :
  - Aucun délai maximal (`AbortController`) côté navigateur si Ollama ne répond pas.

---

## Observations sur les domaines associés

- **`https://git.cybersocle.site`** : Redirection vers `/explore/repos`. Titre d'onglet observé : `Explorateur - Gitea: Git with a cup of tea`. Dépôt `bantudevlab` non visible pour un visiteur non connecté (`No matching results found.`). Lien « Gists » pointant vers `http://localhost:6157/`. Accent manquant sur `Depots` dans le pied de page.
- **`https://forge.cybersocle.site`** : Page autonome chargée en 3,64 s (HTTP 200 OK) sans redirection vers `git.cybersocle.site`. Nombreux accents français manquants (`Depots`, `distribuee`, `connectee`, `temps reel`, `signes`, `Emettre`, `Heberges`, `Francais`, `Portugues`).

---

## Correctifs appliqués dans le code (Tâche 1)

1. **`templates/core/home.html`** : Remplacement du message bloqué `Initialisation de la synchronisation avec Gitea...` par un état vide explicite avec liens vers `/dashboard/#new-repo` et `https://git.cybersocle.site/explore/repos`.
2. **`apps/gitea_client/views.py` & `apps/core/views.py`** : Invalidation du cache `bantudevlab_forge_repos_cache` et `gitea_repos_list` lors de la création d'un dépôt, et fusion des dépôts locaux `SovereignRepository` dans `get_cached_repositories()` afin que `demo-cadev-2026` apparaisse immédiatement dans `/dashboard/`.
3. **`apps/ai_assistant/gemma.py` & `templates/core/dashboard.html`** : Ajout d'un délai maximal côté serveur (35 s en streaming) et d'un `AbortController` côté client (45 s) affichant un message clair si Ollama ne répond pas.
4. **`templates/zkp_auth/login.html`** : Envoi systématique de `X-CSRFToken` (si disponible) lors des appels `POST /api/zkp/challenge/` et `POST /api/zkp/verify/`.
