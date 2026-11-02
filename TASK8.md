# TASK8.md - Cycle de Developpement Continu 2 / 20
# Automatisation des Revues de Pull Requests et Boite de Fusion GitHub Moderne

> Ce cycle apporte a Gitea le comportement visuel et fonctionnel de la boite de fusion moderne de GitHub
> (Merge Box & Status Checks), le bot autonome de revue de PR base sur le LLM local `gemma2:2b`,
> ainsi que l'arborescence de fichiers interactive (File Tree) et les tests CI/CD associes.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK8

- [ ] **T-PR-801 : Bot Autonome de Revue de Code sur Pull Requests (Local Gemma 2 2B)**
  - [ ] Implementer le service `SovereignPRReviewBot` dans `apps/ai_assistant/tasks.py` et `apps/ai_assistant/views.py` analysant les diffs d'une PR et soumettant la revue via l'API Gitea.
  - [ ] Exposer l'endpoint `/api/ai/copilot/pr-review-bot/` permettant de declencher la revue automatique lors d'un webhook `pull_request`.

- [ ] **T-PR-802 : Boite de Fusion GitHub Moderne et Statuts CI/CD (Merge Box & Checks)**
  - [ ] Enrichir les styles Primer dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css` avec les classes de boite de fusion (`.gh-merge-box`, `.gh-status-check-item`).
  - [ ] Integrer la previsualisation interactive des regles de protection (revues requises, checks verts, options de merge squash/rebase).
  - [ ] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-PR-803 : Arborescence de Fichiers Interactive (GitHub File Tree Sidebar)**
  - [ ] Ajouter le panneau lateral pliable d'arborescence de fichiers dans `custom/templates/repo/view_file.tmpl` avec raccourci clavier `t` (Go to file).
  - [ ] Synchroniser avec `gitea_home/custom/templates/repo/view_file.tmpl`.

- [ ] **T-PR-804 : Suite de Tests et Pipeline CI/CD pour la Revue Automatique de PR**
  - [ ] Ajouter les tests unitaires et de simulation de webhooks dans `tests/test_ai_assistant.py` et `tests/test_gitea_client.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/pr_review_bot.yml` et `.gitea/workflows/pr_review_bot.yaml`.
