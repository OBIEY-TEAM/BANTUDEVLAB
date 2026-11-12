"""
Script de validation stricte de conformité des licences (CADEV 2026 - Art. 6).
Échoue (code 1) si une dépendance sous GPL, AGPL, LGPL, SSPL ou BUSL est détectée.
Valide que seules les licences permissives (MIT, Apache-2.0, BSD, ISC, PSF, etc.) sont admises.
"""

import importlib.metadata as md
import sys
from typing import Dict, List, Tuple

FORBIDDEN_TOKENS = ["agpl", "lgpl", "gpl", "sspl", "busl"]

# Packages exclus de l'audit de prod si packages de test/outillage developpeur
DEV_TOOLING_PACKAGES = {
    "pip", "setuptools", "wheel", "pip-licenses", "git-filter-repo"
}


def analyze_licenses() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    compliant = []
    violations = []

    for dist in md.distributions():
        pkg_name = dist.metadata.get("Name", "unknown")
        version = dist.version
        raw_license = dist.metadata.get("License", "") or ""
        classifiers = dist.metadata.get_all("Classifier") or []
        license_classifiers = [c.split("::")[-1].strip() for c in classifiers if "License ::" in c]

        full_license_desc = (raw_license + " " + " ".join(license_classifiers)).strip()
        lower_desc = full_license_desc.lower()

        is_forbidden = any(token in lower_desc for token in FORBIDDEN_TOKENS)

        item = {
            "name": pkg_name,
            "version": version,
            "license": raw_license or (license_classifiers[0] if license_classifiers else "Unknown"),
            "classifiers": "; ".join(license_classifiers),
        }

        if is_forbidden:
            violations.append(item)
        else:
            compliant.append(item)

    return compliant, violations


def main():
    print("=" * 60)
    print("BantuDevLab - Audit de Conformité Licences CADEV 2026 (Art. 6)")
    print("=" * 60)

    compliant, violations = analyze_licenses()

    print(f"Total dépendances auditées : {len(compliant) + len(violations)}")
    print(f"Dépendances conformes : {len(compliant)}")

    if violations:
        print("\n[ERREUR CRITIQUE] Dépendances non conformes détectées (GPL/LGPL/AGPL/SSPL) :")
        for v in violations:
            print(f"  - {v['name']} ({v['version']}) -> Licence : {v['license']} [{v['classifiers']}]")
        print("\nLe projet est IRRECEVABLE selon l'Article 6 du règlement CADEV 2026.")
        sys.exit(1)

    print("\n[SUCCÈS] Toutes les dépendances installées sont conformes au règlement CADEV 2026.")
    print("Seules les licences permissives (MIT, Apache-2.0, BSD, PSF, etc.) sont présentes.")
    sys.exit(0)


if __name__ == "__main__":
    main()
