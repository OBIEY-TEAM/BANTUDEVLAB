# TASK12.md - Cycle de Developpement Continu 6 / 20
# Epinglage de Depots et Profil README Moderne Style GitHub

> Ce cycle apporte a Gitea l'equivalent moderne du **GitHub Profile README** (`username/username`)
> et le systeme de cartes de depots epingles (Pinned Repositories) avec pastilles de langage colorees.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK12

- [x] **T-PRF-1201 : Cartes de Depots Epingles Primer et Pastilles de Langages**
  - [x] Integrer les classes `.gh-pinned-repo-card` et `.repo-language-color` dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-PRF-1202 : Rendu Automatique du Profil README (`username/username`)**
  - [ ] Configurer la detection du depot special de profil et l'injection dynamique du README souverain dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-PRF-1203 : Tests Unitaires et Pipeline CI/CD pour la Presentation de Profil**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/profile_presentation.yml` et `.gitea/workflows/profile_presentation.yaml`.
