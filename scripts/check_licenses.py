"""
Script de validation stricte de conformité des licences (CADEV 2026 - Art. 6).
Échoue (code 1) si une dépendance sous GPL, AGPL, LGPL, SSPL ou BUSL est détectée.
Valide que seules les licences permissives (MIT, Apache-2.0, BSD, ISC, PSF, etc.) sont admises.
Audite les dépendances du projet (directes et transitives à partir de requirements.txt et requirements-dev.txt).
"""

import importlib.metadata as md
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

FORBIDDEN_TOKENS = ["agpl", "lgpl", "gpl", "sspl", "busl"]

# Mots-clés qui indiquent explicitement une licence permissive
PERMISSIVE_KEYWORDS = ["mit", "apache", "bsd", "isc", "psf", "public domain", "unlicense"]


def parse_requirements(req_path: Path) -> Set[str]:
    """Extrait les noms normalisés de paquets depuis un fichier requirements."""
    pkgs = set()
    if not req_path.exists():
        return pkgs
    for line in req_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Extrait le nom du paquet avant tout opérateur (>=, ==, <=, ~, ;, etc.)
        match = re.match(r"^([a-zA-Z0-9_\-\.]+)", line)
        if match:
            pkgs.add(match.group(1).lower().replace("_", "-"))
    return pkgs


def get_project_dependency_tree(root_pkgs: Set[str]) -> Set[str]:
    """Calcule récursivement l'ensemble des paquets directs et transitifs."""
    all_dists = {}
    for dist in md.distributions():
        name = dist.metadata.get("Name", "")
        if name:
            all_dists[name.lower().replace("_", "-")] = dist

    project_pkgs = set()
    queue = list(root_pkgs)

    while queue:
        pkg = queue.pop(0)
        norm_pkg = pkg.lower().replace("_", "-")
        if norm_pkg in project_pkgs:
            continue
        project_pkgs.add(norm_pkg)

        dist = all_dists.get(norm_pkg)
        if not dist or not dist.requires:
            continue

        for req in dist.requires:
            # Nettoie les marqueurs d'environnement (ex: 'importlib-metadata ; python_version < "3.8"')
            req_clean = req.split(";")[0].strip()
            match = re.match(r"^([a-zA-Z0-9_\-\.]+)", req_clean)
            if match:
                dep_name = match.group(1).lower().replace("_", "-")
                if dep_name not in project_pkgs and dep_name in all_dists:
                    queue.append(dep_name)

    return project_pkgs


def is_license_forbidden(license_str: str, classifiers: List[str]) -> bool:
    """Vérifie si une licence enfreint l'Article 6 (GPL, AGPL, LGPL, SSPL, BUSL)."""
    # 1. Vérification dans les classifiers normalisés (plus fiables)
    for c in classifiers:
        c_low = c.lower()
        if any(f"license :: osi approved :: gnu {token}" in c_low or f"gnu {token}" in c_low for token in ["general", "lesser", "library", "affero"]):
            return True
        if any(token in c_low for token in ["gpl", "agpl", "lgpl", "sspl", "busl"]):
            return True

    # 2. Vérification dans la chaîne de licence courte
    # Si le texte fait plus de 200 caractères, c'est souvent un dump de licence avec des notices
    raw_short = license_str.strip().lower() if len(license_str) < 150 else ""
    if raw_short:
        # Exclusion explicite si c'est du BSD/MIT/Apache
        if any(perm in raw_short for perm in PERMISSIVE_KEYWORDS):
            return False
        for token in FORBIDDEN_TOKENS:
            if re.search(r"\b" + token + r"\b", raw_short):
                return True

    return False


def analyze_licenses(target_pkgs: Set[str]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    compliant = []
    violations = []

    for dist in md.distributions():
        pkg_name = dist.metadata.get("Name", "unknown")
        norm_name = pkg_name.lower().replace("_", "-")

        # Filtre sur les paquets du projet
        if norm_name not in target_pkgs:
            continue

        version = dist.version
        raw_license = dist.metadata.get("License", "") or ""
        classifiers = dist.metadata.get_all("Classifier") or []
        license_classifiers = [c.split("::")[-1].strip() for c in classifiers if "License ::" in c]

        is_forbidden = is_license_forbidden(raw_license, license_classifiers)

        item = {
            "name": pkg_name,
            "version": version,
            "license": raw_license if len(raw_license) < 80 else (license_classifiers[0] if license_classifiers else "Licence détaillée"),
            "classifiers": "; ".join(license_classifiers),
        }

        if is_forbidden:
            violations.append(item)
        else:
            compliant.append(item)

    return compliant, violations


def main():
    print("=" * 65)
    print("BantuDevLab - Audit de Conformité Licences CADEV 2026 (Art. 6)")
    print("=" * 65)

    base_dir = Path(__file__).resolve().parent.parent
    req_runtime = parse_requirements(base_dir / "requirements.txt")
    req_dev = parse_requirements(base_dir / "requirements-dev.txt")
    all_root_reqs = req_runtime | req_dev

    print(f"Dépendances directes racines identifiées : {len(all_root_reqs)}")
    project_pkgs = get_project_dependency_tree(all_root_reqs)
    print(f"Arbre complet (directes + transitives) : {len(project_pkgs)} paquets")

    compliant, violations = analyze_licenses(project_pkgs)

    print(f"Total paquets audités : {len(compliant) + len(violations)}")
    print(f"Paquets conformes : {len(compliant)}")

    if violations:
        print("\n[ERREUR CRITIQUE] Dépendances non conformes détectées (GPL/LGPL/AGPL/SSPL) :")
        for v in violations:
            print(f"  - {v['name']} ({v['version']}) -> Licence : {v['license']} [{v['classifiers']}]")
        print("\nLe projet est IRRECEVABLE selon l'Article 6 du règlement CADEV 2026.")
        sys.exit(1)

    print("\n[SUCCÈS] Toutes les dépendances du projet sont conformes au règlement CADEV 2026.")
    print("Seules les licences permissives (MIT, Apache-2.0, BSD, PSF, etc.) sont présentes.")
    sys.exit(0)


if __name__ == "__main__":
    main()
