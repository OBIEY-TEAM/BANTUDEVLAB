# TASK22.md - Cycle de Developpement Continu 16 / 20
# Equipes d'Organisation et Matrice de Roles GitHub (Maintainer, Triage, Admin)

> Ce cycle aligne le modele de gouvernance et de gestion d'equipes organisationnelles de Gitea
> sur la matrice de roles moderne de GitHub Enterprise : roles fins (Read, Triage, Write, Maintain, Admin),
> badges d'acces Primer et controle d'acces granulaire.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK22

- [ ] **T-ORG-2201 : Styles Primer pour les Equipes et Badges de Roles**
  - [ ] Ajouter les classes `.gh-team-card`, `.gh-role-badge`, `.gh-role-triage`, `.gh-role-maintain` dans `theme-github.css` et `theme-github-dark.css`.
  - [ ] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-ORG-2202 : Specification et Guide de la Matrice de Roles Souveraine**
  - [ ] Documenter le mapping des unites de permissions Gitea vers les 5 roles GitHub dans `docs/SOVEREIGN_ORG_ROLES.md`.
  - [ ] Fournir les exemples d'automatisation d'equipes via l'API REST.

- [ ] **T-ORG-2203 : Tests Unitaires et Workflows CI/CD Organization Teams**
  - [ ] Rediger les tests unitaires dans `tests/test_sec_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/org_teams.yml` et `.gitea/workflows/org_teams.yaml`.
