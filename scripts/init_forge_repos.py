import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPOS_DIR = BASE_DIR / "forge_data" / "repos"

REPOS = [
    (
        "bantudevlab",
        "bantudevlab",
        "Forge logicielle souveraine BANTUDEVLAB - Zero-Trust ZKP (Schnorr) et audit IA local Gemma 2 2B",
    ),
    (
        "sovereign-org",
        "afri-fintech-gateway",
        "Passerelle panafricaine de paiement mobile & interoperabilite souveraine",
    ),
    ("sovereign-org", "agro-sentinel-ai", "Modeles de vision embarquee pour la surveillance des recoltes saheliennes"),
    (
        "bantudevlab",
        "bantu-zkp-identity",
        "Bibliotheque cryptographique Zero-Knowledge Proof pour l'Afrique de l'Ouest",
    ),
]

MIT_LICENSE_TEXT = """MIT License

Copyright (c) 2026 BANTUDEVLAB / CYBERSOCLE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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
            readme_path.write_text(
                f"# {name}\n\n> {desc}\n\n"
                "Portail de demonstration : https://cybersocle.site\n"
                "Forge Gitea : https://git.cybersocle.site\n"
                "Licence : MIT\n",
                encoding="utf-8",
            )
            license_path = temp_dir / "LICENSE"
            license_path.write_text(MIT_LICENSE_TEXT, encoding="utf-8")
            subprocess.run(["git", "-C", str(temp_dir), "add", "README.md", "LICENSE"], check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(temp_dir), "commit", "-m", "Initial sovereign commit"],
                check=True,
                capture_output=True,
            )
            subprocess.run(["git", "-C", str(temp_dir), "branch", "-M", "main"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(temp_dir), "push", "origin", "main"], check=True, capture_output=True)
            subprocess.run(
                ["git", "-C", str(repo_dir), "symbolic-ref", "HEAD", "refs/heads/main"], check=True, capture_output=True
            )

            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Repository initialized: {owner}/{name}")


if __name__ == "__main__":
    init_sample_repos()
