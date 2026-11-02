# TASK17.md - Cycle de Developpement Continu 11 / 20
# Generateur Automatique de Notes de Version GitHub (Release Notes from Merged PRs)

> Ce cycle integre a BantuDevLab et Gitea la fonctionnalite moderne GitHub « Generate release notes » :
> categorisation automatique des PRs fusionnees (Features, Bug Fixes, Docs, Maintenance),
> attribution des auteurs et synthese de changelog au standard Primer.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK17

- [x] **T-REL-1701 : Moteur de Generation de Notes de Version**
  - [x] Implementer `scripts/generate_release_notes.py` capable de classifier les PRs fusionnees et commits selon les conventions semantiques (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
  - [x] Generer le format Markdown standard GitHub (« What's Changed », liste des contributeurs, lien vers le diff complet).

- [x] **T-REL-1702 : Configuration Declaration et Documentation des Releases**
  - [x] Rediger `docs/SOVEREIGN_RELEASE_NOTES.md` specifiant la configuration `.github/release.yml` et `.gitea/release.yml`.
  - [x] Fournir les exemples de modeles de categories et exclusions (dependabot, bot).

- [ ] **T-REL-1703 : Tests Unitaires et Workflows CI/CD Release Notes**
  - [ ] Rediger les tests unitaires de validation du parseur dans `tests/test_sec_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/release_notes.yml` et `.gitea/workflows/release_notes.yaml`.
