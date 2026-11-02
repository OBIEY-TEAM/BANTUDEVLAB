import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOS_DIR = BASE_DIR / "forge_data" / "repos"

REPOS = [
    ("sovereign-org", "afri-fintech-gateway", "Passerelle panafricaine de paiement mobile & interoperabilite souveraine"),
    ("sovereign-org", "agro-sentinel-ai", "Modeles de vision embarquee pour la surveillance des recoltes saheliennes"),
    ("bantudevlab", "bantu-zkp-identity", "Bibliotheque cryptographique Zero-Knowledge Proof pour l'Afrique de l'Ouest"),
]


def init_sample_repos():
    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    for owner, name, desc in REPOS:
        repo_dir = REPOS_DIR / owner / f"{name}.git"
        if not repo_dir.exists():
            repo_dir.mkdir(parents=True, exist_ok=True)
            # Initialize bare repository
            subprocess.run(["git", "init", "--bare", str(repo_dir)], check=True, capture_output=True)

            # Create an initial commit by cloning into temp and committing a README
            temp_dir = BASE_DIR / "forge_data" / "temp" / name
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            temp_dir.parent.mkdir(parents=True, exist_ok=True)

            subprocess.run(["git", "clone", str(repo_dir), str(temp_dir)], check=True, capture_output=True)
            readme_path = temp_dir / "README.md"
            readme_path.write_text(f"# {name}\n\n> {desc}\n\nHeberge sur la forge souveraine BANTUDEVLAB (Systalink Cloud).\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(temp_dir), "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(temp_dir), "commit", "-m", "Initial sovereign commit"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(temp_dir), "branch", "-M", "main"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(temp_dir), "push", "origin", "main"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo_dir), "symbolic-ref", "HEAD", "refs/heads/main"], check=True, capture_output=True)

            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Repository initialized: {owner}/{name}")


if __name__ == "__main__":
    init_sample_repos()
