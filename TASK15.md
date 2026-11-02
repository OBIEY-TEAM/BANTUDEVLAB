# TASK15.md - Cycle de Developpement Continu 9 / 20
# Rulesets de Protection de Branches et Badges de Signature de Commits

> Ce cycle apporte a Gitea l'experience visuelle et la configuration avancee des Rulesets GitHub :
> obligation de signature cryptographique GPG/SSH, badge « Verified » Primer, et blocage des push forces.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK15

- [x] **T-BRN-1501 : Badges Primer de Signature de Commits (« Verified » & « Unverified »)**
  - [x] Styliser les badges `.gh-commit-badge.verified` et `.gh-commit-badge.unverified` dans `custom/public/assets/css/theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [x] **T-BRN-1502 : Guide et Specification des Rulesets GitHub pour Gitea**
  - [x] Documenter les regles de protection equivalentes aux Rulesets modernes dans `docs/SOVEREIGN_BRANCH_RULESETS.md`.
  - [x] Configurer les directives de conformite cryptographique et revues requises.

- [ ] **T-BRN-1503 : Tests Unitaires et Pipeline CI/CD pour les Rulesets**
  - [ ] Rediger les tests de verification de signatures dans `tests/test_sec_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/branch_rulesets.yml` et `.gitea/workflows/branch_rulesets.yaml`.
