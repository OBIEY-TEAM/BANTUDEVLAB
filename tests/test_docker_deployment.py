"""Tests de validation et de cohérence pour les déploiements Docker de BANTUDEVLAB."""

import subprocess
import unittest
from pathlib import Path


class DockerDeploymentConsistencyTestCase(unittest.TestCase):
    """Vérifie la rigueur et l'alignement des configurations Docker et Docker Compose."""

    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent

    def test_dockerfile_existence_and_structure(self):
        """Vérifie les directives de sécurité du Dockerfile principal."""
        dockerfile_path = self.root_dir / "Dockerfile"
        self.assertTrue(dockerfile_path.exists(), "Le Dockerfile racine doit exister.")

        content = dockerfile_path.read_text(encoding="utf-8")
        self.assertIn("USER appuser", content, "Le conteneur doit basculer vers un utilisateur non-root.")
        self.assertIn("EXPOSE 8000 3001", content, "Les ports applicatifs 8000 et 3001 doivent être exposés.")
        self.assertIn("uvicorn.workers.UvicornWorker", content, "Gunicorn doit utiliser les workers Uvicorn.")

    def test_docker_compose_files_exist(self):
        """Vérifie la présence des compositions standard et production."""
        compose_dev = self.root_dir / "docker-compose.yml"
        compose_prod = self.root_dir / "docker-compose.production.yml"
        self.assertTrue(compose_dev.exists(), "docker-compose.yml doit exister.")
        self.assertTrue(compose_prod.exists(), "docker-compose.production.yml doit exister.")

    def test_nginx_configuration_coherence(self):
        """Vérifie la cohérence du fichier Nginx de production avec les conteneurs."""
        nginx_conf = self.root_dir / "deploy" / "nginx" / "bantudevlab.conf"
        self.assertTrue(nginx_conf.exists(), "Le fichier de configuration Nginx doit exister.")

        content = nginx_conf.read_text(encoding="utf-8")
        self.assertIn("alias /var/www/static/;", content, "Le chemin static doit correspondre au montage volume Nginx.")
        self.assertIn("proxy_pass http://django_app:8000;", content, "Nginx doit router vers django_app:8000.")
        self.assertIn("proxy_pass http://gitlab:80;", content, "Nginx doit router vers gitlab:80.")
        self.assertIn(
            "cybersocle.site", content, "Le domaine cybersocle.site doit être configuré dans les server_name."
        )
        self.assertIn("auth.bantudevlab.africa", content, "Le domaine auth doit être configuré dans les server_name.")

    def test_pgbouncer_configuration_coherence(self):
        """Vérifie que PgBouncer inclut les bases appropriées."""
        pgb_ini = self.root_dir / "deploy" / "pgbouncer" / "pgbouncer.ini"
        self.assertTrue(pgb_ini.exists(), "Le fichier pgbouncer.ini doit exister.")

        content = pgb_ini.read_text(encoding="utf-8")
        self.assertIn("bantudevlab = host=db", content)
        self.assertIn("bantudevlab_prod = host=db", content)

    def test_env_files_port_alignment(self):
        """Vérifie l'alignement des URLs et des ports dans les fichiers .env."""
        env_example = self.root_dir / ".env.example"
        self.assertTrue(env_example.exists())
        content_example = env_example.read_text(encoding="utf-8")
        self.assertIn("GITEA_EXTERNAL_URL=http://localhost:3002", content_example)

        env_prod = self.root_dir / ".env.production.example"
        self.assertTrue(env_prod.exists())
        content_prod = env_prod.read_text(encoding="utf-8")
        self.assertIn("GEMMA_API_URL=http://ollama:11434/api/generate", content_prod)

    def test_docker_compose_cli_validation(self):
        """Valide la syntaxe des compositions via docker compose config si docker est disponible."""
        if subprocess.run(["which", "docker"], capture_output=True).returncode == 0:
            res_dev = subprocess.run(
                ["docker", "compose", "--env-file", ".env.example", "config", "--quiet"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_dev.returncode, 0, f"Erreur docker compose config dev: {res_dev.stderr}")

            res_prod = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    "docker-compose.production.yml",
                    "--env-file",
                    ".env.production.example",
                    "config",
                    "--quiet",
                ],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_prod.returncode, 0, f"Erreur docker compose config prod: {res_prod.stderr}")
