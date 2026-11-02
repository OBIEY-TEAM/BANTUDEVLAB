# TASK11.md - Cycle de Developpement Continu 5 / 20
# Visualisation du Graphe de Dependances et Export SBOM CycloneDX

> Ce cycle integre l'equivalent moderne de **GitHub Dependency Graph & SBOM Export** (Software Bill of Materials)
> selon la norme internationale CycloneDX v1.5 et SPDX, interconnecte avec l'onglet Insights du depot.

---

## Directives d'Execution et Regles d'Or

1. **Engagement atomique** : chaque tache ou sous-tache doit faire l'objet d'un commit Git distinct avant de passer a la suivante.
2. **Zero Emoji** : respect absolu de la regle zero-emoji dans l'ensemble des fichiers, scripts, documentations et messages de commit.
3. **Maintien de la couverture de tests** : couverture de tests superieure ou egale a 95% sur les applications metier.
4. **Non-regression** : conservation stricte des fonctionnalites existantes et compatibilite ascendante.

---

## Taches du Cycle TASK11

- [x] **T-SBM-1101 : Generateur Souverain de SBOM CycloneDX et SPDX**
  - [x] Implementer le script `scripts/generate_sovereign_sbom.py` analysant les manifests (`requirements.txt`, `pyproject.toml`, `package.json`) et generant `bom.cyclonedx.json`.
  - [x] Documenter le format et les normes de gouvernance dans `docs/SOVEREIGN_DEPENDENCY_GRAPH_SBOM.md`.

- [x] **T-SBM-1102 : Interconnexion de l'Onglet Insights et Graphe de Dependances**
  - [x] Mettre a jour `custom/templates/repo/header.tmpl` pour activer le lien contextuel de l'onglet Insights vers la vue de dependances.
  - [x] Synchroniser avec `gitea_home/custom/templates/repo/header.tmpl`.

- [ ] **T-SBM-1103 : Tests Unitaires et Pipeline CI/CD d'Attestation SBOM**
  - [ ] Rediger les tests unitaires dans `tests/test_security_hardening.py`.
  - [ ] Creer les workflows CI/CD `.github/workflows/sbom_cyclonedx.yml` et `.gitea/workflows/sbom_cyclonedx.yaml`.
