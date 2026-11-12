# TASK23.md - Cycle de Developpement Continu 17 / 20
# Pull Requests Brouillon GitHub (Draft Pull Requests & Ready for Review Flow)

> Ce cycle aligne le cycle de vie des Pull Requests en cours de redaction (Draft PRs)
> de Gitea sur le standard GitHub : badge « Draft » Primer neutre, bouton d'action
> « Ready for review » et verrouillage visuel du merge tant que le statut brouillon est actif.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK23

- [x] **T-DRF-2301 : Styles Primer pour les Draft Pull Requests**
  - [x] Ajouter les styles `.gh-draft-badge`, `.gh-ready-for-review-btn`, `.gh-draft-banner` dans `theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [x] **T-DRF-2302 : Rendu Dynamique et Flux « Ready for Review »**
  - [x] Ajouter la detection de PR brouillon et l'injection de la banniere « Ready for review » dans `custom/templates/custom/header.tmpl`.
  - [x] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [x] **T-DRF-2303 : Tests Unitaires et Workflows CI/CD Draft PRs**
  - [x] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [x] Creer les workflows CI/CD `.github/workflows/draft_prs.yml` et `.gitea/workflows/draft_prs.yaml`.
