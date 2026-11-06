#!/usr/bin/env python3
"""
BantuDevLab - Generateur d'Attestation et d'Integrite des Releases (T-REL-902)
Calcule les sommes de controle SHA256 des artefacts et produit un fichier
d'attestation conforme au standard SLSA Provenance v1.
"""

import argparse
import datetime
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Dict, List


def calculate_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_git_commit() -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "UNKNOWN_COMMIT"


def generate_provenance(files: List[Path], output_dir: Path) -> Dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    checksums = []
    subjects = []

    for file_path in files:
        if not file_path.is_file():
            continue
        digest = calculate_sha256(file_path)
        rel_name = file_path.name
        checksums.append(f"{digest}  {rel_name}")
        subjects.append({"name": rel_name, "digest": {"sha256": digest}})

    # Fichier SHA256SUMS standard
    checksums_path = output_dir / "SHA256SUMS"
    with open(checksums_path, "w", encoding="utf-8") as f:
        f.write("\n".join(checksums) + "\n")

    # Attestation SLSA v1
    slsa_provenance = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": subjects,
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://cybersocle.site/attestation/v1",
                "externalParameters": {
                    "sourceRepository": "https://github.com/OBIEY-TEAM/BANTUDEVLAB",
                    "commit": get_git_commit(),
                },
                "internalParameters": {
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "builder": "BantuDevLab Sovereign CI Runner",
                },
            },
            "runDetails": {
                "builder": {"id": "https://cybersocle.site/runners/sovereign"},
                "metadata": {
                    "invocationId": f"run-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                },
            },
        },
    }

    slsa_path = output_dir / "provenance.slsa.json"
    with open(slsa_path, "w", encoding="utf-8") as f:
        json.dump(slsa_provenance, f, indent=2)

    return {
        "checksums": str(checksums_path),
        "slsa": str(slsa_path),
        "total_files": len(subjects),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Attestation d'integrite des livrables de release")
    parser.add_argument("paths", nargs="+", help="Fichiers ou dossiers a attester")
    parser.add_argument("--out", default="dist", help="Dossier de sortie des attestations")
    args = parser.parse_args()

    target_files = []
    for p in args.paths:
        path_obj = Path(p)
        if path_obj.is_file():
            target_files.append(path_obj)
        elif path_obj.is_dir():
            target_files.extend([f for f in path_obj.rglob("*") if f.is_file()])

    res = generate_provenance(target_files, Path(args.out))
    print(f"[SUCCESS] {res['total_files']} artefacts attestes. Fichiers: {res['checksums']}, {res['slsa']}")
