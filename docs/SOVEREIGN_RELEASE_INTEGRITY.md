# Integrite Cryptographique et Attestation SLSA des Releases (T-REL-902)

Ce document decrit la procedure de verification et d'attestation d'integrite des livrables de releases selon les standards SLSA (Supply-chain Levels for Software Artifacts) v1.

---

## 1. Objectifs de Securite de la Chaine d'Approvisionnement

Afin de garantir que les binaires, archives et conteneurs n'ont subi aucune alteration malveillante :
- Chaque artefact est hache avec l'algorithme SHA256 des sa generation dans le runner souverain.
- Un fichier `SHA256SUMS` est automatiquement attache aux actifs de la release.
- Un document de provenance cryptographique au format in-toto / SLSA v1 (`provenance.slsa.json`) certifie le commit Git source, l'horodatage et l'identite du build runner.

---

## 2. Generation Automatique dans le Pipeline CI/CD

Dans les pipelines Gitea Actions / GitHub Actions, l'etape de signature et d'attestation s'execute via :

```bash
python scripts/generate_release_provenance.py dist/ --out dist/
```

---

## 3. Verification par les Utilisateurs et Developpeurs

Pour verifier l'integrite d'une archive telechargee :

```bash
# Verification standard
sha256sum -c SHA256SUMS

# Verification sous PowerShell
Get-FileHash -Algorithm SHA256 <archive_name>
```
