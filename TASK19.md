# TASK19.md - Cycle de Developpement Continu 13 / 20
# Modifications Suggerees dans les Pull Requests GitHub (Suggested Changes Primer & Apply)

> Ce cycle apporte a Gitea le composant d'excellence de revue de code de GitHub moderne :
> le bloc de proposition de modification de code (« Suggested change »), le diff inline avec coloration
> syntaxique et le bouton d'application directe de suggestion (« Apply suggestion »).

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK19

- [ ] **T-SUG-1901 : Styles Primer pour les Blocs de Modification Suggeree**
  - [ ] Ajouter les styles `.gh-suggestion-box`, `.gh-suggestion-header`, `.gh-suggestion-btn` dans `theme-github.css` et `theme-github-dark.css`.
  - [ ] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-SUG-1902 : Moteur de Rendu Polyfill des Blocs ```suggestion**
  - [ ] Implementer le transformateur Markdown cote client dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-SUG-1903 : Tests Unitaires et Workflows CI/CD Suggested Changes**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/suggested_changes.yml` et `.gitea/workflows/suggested_changes.yaml`.
