# TASK21.md - Cycle de Developpement Continu 15 / 20
# Jalons de Suivi de Projet GitHub (Issue Milestones & Burndown Progress Tracking)

> Ce cycle aligne la gestion des Jalons (Milestones) de Gitea sur GitHub moderne :
> carte de jalon Primer, barre de progression proportionnelle (issues ouvertes / fermees),
> echeances temporelles calculees et metadonnees d'avancement.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK21

- [x] **T-MLS-2101 : Styles Primer pour les Jalons et Barres de Progression**
  - [x] Ajouter les styles `.gh-milestone-card`, `.gh-milestone-progress-bar`, `.gh-milestone-meta` dans `theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-MLS-2102 : Calculateur Dynamique de Progression et Statuts**
  - [ ] Ajouter le script d'enrichissement des barres de jalons dans `custom/templates/custom/header.tmpl`.
  - [ ] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-MLS-2103 : Tests Unitaires et Workflows CI/CD Milestones**
  - [ ] Rediger les tests unitaires dans `tests/test_ui_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/milestones_progress.yml` et `.gitea/workflows/milestones_progress.yaml`.
