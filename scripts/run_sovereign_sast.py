"""
BANTUDEVLAB - CLI d'Analyse SAST et Secret Scanning Souverain (T-SEC-601).
Scanne les fichiers source du projet, calcule l'entropie de Shannon pour les secrets,
et genere un rapport SARIF 2.1.0 standard compatible GitHub / Gitea Actions.
"""

import json
import os
import sys
from pathlib import Path

# Ajouter la racine du projet au sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
try:
    import django

    django.setup()
    from apps.security_scanner.engine import SecurityScannerEngine
    from apps.security_scanner.serializers import SarifReportSerializer
except Exception as e:
    print(f"[ERREUR] Initialisation du scanner : {e}", file=sys.stderr)
    sys.exit(1)


def scan_project(root_dir: str = ".") -> int:
    extensions = {".py", ".html", ".js", ".css", ".yml", ".yaml", ".sh"}
    ignored_dirs = {".venv", ".git", "node_modules", "gitea_home", "forge_data", "__pycache__", ".pytest_cache"}
    total_issues = 0
    raw_findings = []

    for root, dirs, files in os.walk(root_dir):
        # Elagage immediat des repertoires ignores
        dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]
        for file_name in files:
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in extensions:
                continue

            full_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(full_path, root_dir).replace("\\", "/")

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                res = SecurityScannerEngine.scan_code(filename=rel_path, content=content)
                if res.get("issues"):
                    raw_findings.extend(res["issues"])
                    total_issues += len(res["issues"])
            except Exception:
                continue

    # Generation du rapport SARIF
    sarif_output = {
        "$schema": SarifReportSerializer.SARIF_SCHEMA,
        "version": SarifReportSerializer.SARIF_VERSION,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "BantuDevLab Sovereign SAST & Secret Scanner",
                        "version": "1.0.0",
                        "informationUri": "https://cybersocle.site",
                    }
                },
                "results": [
                    {
                        "ruleId": f.get("type", "SOVEREIGN_VULN"),
                        "level": "error" if f.get("severity") in ("CRITICAL", "HIGH") else "warning",
                        "message": {"text": f.get("description", "Alerte de securite")},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {"uri": f.get("file", "unknown")},
                                    "region": {"startLine": f.get("line", 1)},
                                }
                            }
                        ],
                    }
                    for f in raw_findings
                ],
            }
        ],
    }

    sarif_path = "results.sarif"
    with open(sarif_path, "w", encoding="utf-8") as f:
        json.dump(sarif_output, f, indent=2)

    print(f"[OK] Scan termine : {total_issues} anomalie(s) detectee(s). Rapport genere : {sarif_path}")
    return 0


if __name__ == "__main__":
    sys.exit(scan_project())
