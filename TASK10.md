# TASK10.md - Cycle de Developpement Continu 4 / 20
# Tableaux Markdown Interactifs Modernes Style GitHub

> Ce cycle apporte a Gitea les capacites de tri dynamique par colonne, de filtrage textuel
> et de mise en forme avancee des tableaux Markdown (.md), conformement aux standards modernes de GitHub.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK10

- [x] **T-TAB-1001 : Mise en Forme Primer des Tableaux Markdown**
  - [x] Styliser les tableaux Markdown (`table`, `th`, `td`) avec les bordures et espacements GitHub Primer dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [x] **T-TAB-1002 : Tri Interactif et Filtrage Dynamique des Colonnes**
  - [x] Implementer le tri ascendant/descendant au clic sur les en-tetes `th` dans `custom/templates/custom/header.tmpl`.
  - [x] Ajouter l'indicateur visuel de tri discret (fleche SVG).
  - [x] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-TAB-1003 : Tests Unitaires et Pipeline CI/CD pour le Moteur de Rendu Markdown**
  - [ ] Ajouter les tests de conformite du rendu Markdown dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/markdown_tables.yml` et `.gitea/workflows/markdown_tables.yaml`.
