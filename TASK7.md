# TASK7.md - Cycle de Developpement Continu 1 / 20
# Assistant Souverain GitHub Copilot et Navigation Interactive Moderne

> Ce cycle integre l'equivalent souverain de **GitHub Copilot** s'appuyant sur le LLM local du projet (`gemma2:2b`),
> ainsi que la palette de commandes globale moderne (`Ctrl+K` / `Cmd+K`) et les flux de verification CI/CD.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK7

- [x] **T-COP-701 : Points d'Acces API Copilot Souverain (Completions, Explications, PR Summary)**
  - [x] Implementer l'endpoint `/api/ai/copilot/explain/` permettant d'expliquer un fichier ou fragment de code selectionne.
  - [x] Implementer l'endpoint `/api/ai/copilot/complete/` pour la suggestion et l'autocompletion de code basee sur `gemma2:2b`.
  - [x] Implementer l'endpoint `/api/ai/copilot/pr-summary/` pour generer automatiquement le resume d'une Pull Request.

- [x] **T-COP-702 : Widget Flottant et Interface Chat Copilot dans Gitea**
  - [x] Ajouter le bouton et la fenetre tiroir Copilot en bas a droite dans `custom/templates/custom/footer.tmpl`.
  - [x] Permettre l'interaction en direct avec l'assistant local (analyse du fichier courant, prompt libre).
  - [x] Synchroniser les templates personnalises avec `gitea_home/custom/templates/`.

- [x] **T-COP-703 : Palette de Commandes Globale Moderne (Equivalent GitHub Ctrl+K / Cmd+K)**
  - [x] Integrer la fenetre modale de commande spotlight declenchee par le raccourci `Ctrl+K` ou `Cmd+K` dans `custom/templates/custom/header.tmpl`.
  - [x] Proposer la recherche rapide, le basculement d'onglet (Code, Issues, PRs), et l'appel direct a Copilot.
  - [x] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-COP-704 : Suite de Tests et Pipeline CI/CD Copilot**
  - [ ] Rediger les tests unitaires et d'integration pour les points d'acces Copilot dans `tests/test_ai_assistant.py`.
  - [ ] Creer le workflow CI/CD `.github/workflows/copilot_verification.yml` et son miroir `.gitea/workflows/copilot_verification.yaml`.
