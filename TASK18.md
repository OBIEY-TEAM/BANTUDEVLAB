# TASK18.md - Cycle de Developpement Continu 12 / 20
# Recherche de Code Avancee GitHub (Filtres de Chemin, Extensions, Regex Bleve)

> Ce cycle dote la forge Gitea de l'experience de recherche de code moderne GitHub :
> aide a la saisie des qualificateurs de recherche (`path:`, `lang:`, `symbol:`, `repo:`),
> integration avec le moteur Bleve et styles Primer d'auto-completion.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK18

- [x] **T-SRC-1801 : Styles et Palette de Qualificateurs de Recherche Primer**
  - [x] Ajouter les styles `.gh-search-qualifiers-popover`, `.gh-qualifier-badge`, `.gh-qualifier-item` dans `theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-SRC-1802 : Aide a la Recherche Interactive et Documentation Bleve**
  - [ ] Ajouter le volet interactif d'aide aux qualificateurs dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.
  - [ ] Documenter les requetes et l'indexation Bleve dans `docs/SOVEREIGN_CODE_SEARCH.md`.

- [ ] **T-SRC-1803 : Tests de Conformite et Pipeline CI/CD Code Search**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/code_search.yml` et `.gitea/workflows/code_search.yaml`.
