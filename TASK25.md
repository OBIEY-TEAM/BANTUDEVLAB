# TASK25.md - Cycle de Developpement Continu 19 / 20
# Avis de Securite GitHub et Signalement Confidentiel de Vulnerabilites (Security Advisories & CVE Flow)

> Ce cycle aligne l'onglet Security et la gestion des avis de securite de Gitea sur le standard
> GitHub Security Advisories : divulgation confidentielle privee, badges de severite Primer
> (Critical, High, Medium, Low), notation CVSS v3.1 et workflow d'alerte CVE.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK25

- [x] **T-SEC-2501 : Styles Primer pour les Avis de Securite et Badges de Severite**
  - [x] Ajouter les classes `.gh-advisory-card`, `.gh-severity-badge`, `.gh-confidential-banner` dans `theme-github.css` et `theme-github-dark.css`.
  - [x] Synchroniser avec `gitea_home/custom/public/assets/css/`.

- [ ] **T-SEC-2502 : Modele de Signalement Confidentiel et Specification des Advisories**
  - [ ] Creer `.gitea/SECURITY_ADVISORY_TEMPLATE.md` et `.github/SECURITY_ADVISORY_TEMPLATE.md`.
  - [ ] Documenter le processus de divulgation responsable dans `docs/SOVEREIGN_SECURITY_ADVISORIES.md`.

- [ ] **T-SEC-2503 : Tests Unitaires et Workflows CI/CD Security Advisories**
  - [ ] Rediger les tests unitaires dans `tests/test_sec_axes.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/security_advisories.yml` et `.gitea/workflows/security_advisories.yaml`.
