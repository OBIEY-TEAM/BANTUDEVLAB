# TASK9.md - Cycle de Developpement Continu 3 / 20
# Visualisation Blame Moderne, Integrite des Releases et Barres de Progression

> Ce cycle apporte a Gitea l'experience visuelle de Git Blame interactive a gradient thermique de GitHub,
> les badges d'integrite cryptographique des assets de release (SHA256 & SLSA),
> ainsi que les barres de progression interactives des listes de taches Markdown.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK9

- [x] **T-BLM-901 : Vue Blame Interactive a Gradient Thermique et Cartes de Commit**
  - [x] Integrer la barre thermique d'anciennete de commit (`.gh-blame-heat-marker`) dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Permettre la previsualisation contextuelle de l'auteur et du message de commit.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [x] **T-REL-902 : Integrite Cryptographique et Sommes de Controle des Releases (SHA256 & SLSA)**
  - [x] Creer le script utilitaire `scripts/generate_release_provenance.py` calculant et attestant les sommes de controle SHA256 de chaque livrable de release.
  - [x] Exposer les informations d'integrite dans `docs/SOVEREIGN_RELEASE_INTEGRITY.md`.

- [x] **T-TSK-903 : Barres de Progression des Listes de Taches Markdown (Issue & PR Tasklists)**
  - [x] Ajouter le script client de calcul dynamique de progression (`x of y tasks`) dans `custom/templates/custom/header.tmpl`.
  - [x] Afficher la jauge de completion Primer (`.gh-task-progress-bar`) au-dessus du corps des tickets et des PRs.
  - [x] Synchroniser avec `gitea_home/custom/templates/custom/header.tmpl`.

- [ ] **T-TSK-904 : Suite de Tests et Pipeline CI/CD d'Integrite des Releases**
  - [ ] Ajouter les tests unitaires dans `tests/test_qa_coverage.py` et `tests/test_sec_axes.py`.
  - [ ] Creer le workflow CI/CD `.github/workflows/provenance_integrity.yml` et `.gitea/workflows/provenance_integrity.yaml`.
