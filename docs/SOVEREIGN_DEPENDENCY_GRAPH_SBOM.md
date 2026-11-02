# Graphe de Dependances et Export SBOM CycloneDX (T-SBM-1101)

Ce document decrit la generation et la gouvernance du graphe de dependances souverain, equivalent a **GitHub Dependency Graph & SBOM Export**, base sur la specification internationale **CycloneDX v1.5**.

---

## 1. Role du SBOM (Software Bill of Materials)

Le SBOM fournit un inventaire numerique complet et verifie de tous les paquets, bibliotheques et dependances transitives de BantuDevLab :
- Identification univoque via Package URL (`purl`, ex: `pkg:pypi/django@5.2.18`).
- Tracabilite des composants pour la prevention des attaques par empoisonnement de la chaine logistique (Software Supply Chain Security).
- Conformite avec les exigences des agences gouvernementales de cybersecurite et standards ISO/IEC 5962 (SPDX) et OWASP CycloneDX.

---

## 2. Generation du Fichier SBOM

Pour generer l'inventaire :

```bash
python scripts/generate_sovereign_sbom.py --project-dir . --out bom.cyclonedx.json
```

Le fichier `bom.cyclonedx.json` produit est directement exportable et visualisable dans les interfaces d'audit de dependances.
