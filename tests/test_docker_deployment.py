"""Tests de validation et de cohérence pour les déploiements Docker de BANTUDEVLAB."""

import os
import shutil
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
        self.assertIn(
            "--no-control-socket",
            content,
            "Gunicorn doit désactiver le socket de contrôle pour fonctionner sur système de fichiers en lecture seule.",
        )
        self.assertIn(
            "XDG_RUNTIME_DIR=/tmp",
            content,
            "XDG_RUNTIME_DIR doit pointer vers /tmp pour les environnements durcis rootless.",
        )

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

    def test_gitlab_configuration_syntax_and_erb_safety(self):
        """Vérifie la syntaxe Ruby de gitlab.rb et l'absence de balises ERB causant des plantages Omnibus."""
        gitlab_rb = self.root_dir / "gitlab" / "config" / "gitlab.rb"
        self.assertTrue(gitlab_rb.exists(), "Le fichier gitlab/config/gitlab.rb doit exister.")

        content = gitlab_rb.read_text(encoding="utf-8")
        self.assertNotIn(
            "<%=",
            content,
            "gitlab.rb est évalué directement par Chef Ruby et ne doit pas contenir de balises ERB '<%= ... %>'.",
        )
        self.assertIn("ENV['DJANGO_SECRET_KEY']", content)
        self.assertIn("ENV['GITLAB_WEBHOOK_SECRET']", content)

        compose_prod = self.root_dir / "docker-compose.production.yml"
        compose_content = compose_prod.read_text(encoding="utf-8")
        self.assertIn("DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}", compose_content)
        self.assertIn("GITLAB_WEBHOOK_SECRET: ${GITLAB_WEBHOOK_SECRET}", compose_content)

        # Si ruby est installé dans l'environnement, simuler la génération et l'évaluation ERB de gitlab.yml
        if shutil.which("ruby") is not None:
            ruby_script = """
require "erb"
require "json"

def external_url(url); end
gitlab_rails = {}
gitlab_ci = {}
puma = {}
sidekiq = {}
prometheus_monitoring = {}
nginx = {}

eval(File.read(ARGV[0]))

gitlab_yml_template = <<~YAML
  production: &base
    gitlab:
      host: localhost
    omniauth:
      enabled: <%= gitlab_rails["omniauth_enabled"] %>
      providers: <%= gitlab_rails["omniauth_providers"].to_json %>
    webhook_secret_token: <%= gitlab_rails["webhook_secret_token"].to_json %>
YAML

rendered = ERB.new(gitlab_yml_template).result(binding)
ERB.new(rendered).result
puts "OK"
"""
            res = subprocess.run(
                ["ruby", "-e", ruby_script, str(gitlab_rb)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Erreur de syntaxe/évaluation ERB dans gitlab.rb: {res.stderr}")
            self.assertIn("OK", res.stdout)

    def test_gitlab_container_resilience_parameters(self):
        """Vérifie que le conteneur GitLab Omnibus est durci contre les boucles de crash (shm_size, healthcheck, et montages de stratégie OmniAuth)."""
        compose_prod = self.root_dir / "docker-compose.production.yml"
        content = compose_prod.read_text(encoding="utf-8")

        self.assertIn("shm_size:", content, "GitLab Omnibus doit avoir shm_size configuré.")
        self.assertIn(
            "/opt/gitlab/bin/gitlab-healthcheck", content, "GitLab doit utiliser le gitlab-healthcheck officiel."
        )
        self.assertIn("start_period: 300s", content, "Le start_period de GitLab doit être d'au moins 300s.")
        self.assertIn(
            "bantu_zkp.rb", content, "La stratégie OmniAuth Bantu ZKP doit être montée dans le conteneur GitLab."
        )
        self.assertIn(
            "config/initializers/bantu_zkp.rb",
            content,
            "L'initialiseur Rails OmniAuth Bantu ZKP doit être monté dans le conteneur GitLab.",
        )

        gitlab_rb = self.root_dir / "gitlab" / "config" / "gitlab.rb"
        gitlab_rb_content = gitlab_rb.read_text(encoding="utf-8")
        self.assertIn(
            "strategy_class", gitlab_rb_content, "gitlab.rb doit déclarer strategy_class pour éviter StrategyNotFound."
        )

    def test_bantu_zkp_omniauth_strategy_registration(self):
        """Vérifie que bantu_zkp.rb s'enregistre dans OmniAuth::Strategies::BantuZkp pour éviter Devise StrategyNotFound."""
        bantu_zkp_rb = self.root_dir / "gitlab" / "lib" / "gitlab" / "auth" / "bantu_zkp.rb"
        self.assertTrue(bantu_zkp_rb.exists(), "Le fichier de stratégie bantu_zkp.rb doit exister.")

        content = bantu_zkp_rb.read_text(encoding="utf-8")
        self.assertIn("class BantuZkp < OmniAuth::Strategies::OAuth2", content)
        self.assertIn("OmniAuth::Strategies", content)
        self.assertIn("BantuZkp = ::Gitlab::Auth::BantuZkp", content)

        if shutil.which("ruby") is not None:
            ruby_script = """
module OmniAuth
  module Strategies
    class OAuth2
      def self.option(*args); end
      def self.uid(&b); end
      def self.info(&b); end
      def self.extra(&b); end
    end
  end
end
$LOADED_FEATURES << 'omniauth-oauth2.rb'

require ARGV[0]

unless defined?(OmniAuth::Strategies::BantuZkp) && OmniAuth::Strategies::BantuZkp == Gitlab::Auth::BantuZkp
  abort("OmniAuth::Strategies::BantuZkp is not properly defined as Gitlab::Auth::BantuZkp")
end

puts "STRATEGY_OK"
"""
            res = subprocess.run(
                ["ruby", "-e", ruby_script, str(bantu_zkp_rb)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Erreur de chargement de la stratégie OmniAuth BantuZkp: {res.stderr}")
            self.assertIn("STRATEGY_OK", res.stdout)

    def test_gitlab_rb_loads_strategy_class_into_provider_and_args(self):
        """Vérifie que gitlab.rb résout et configure la stratégie OmniAuth à la fois au niveau provider et dans args."""
        gitlab_rb = self.root_dir / "gitlab" / "config" / "gitlab.rb"

        if shutil.which("ruby") is not None:
            ruby_script = """
def external_url(*); end
gitlab_rails = {}
gitlab_ci = {}
puma = {}
sidekiq = {}
prometheus_monitoring = {}
nginx = {}

module OmniAuth
  module Strategies
    class OAuth2
      def self.option(*args); end
      def self.uid(&b); end
      def self.info(&b); end
      def self.extra(&b); end
    end
  end
end
$LOADED_FEATURES << 'omniauth-oauth2.rb'

eval(File.read(ARGV[0]))

provider = gitlab_rails['omniauth_providers']&.first
abort("No provider configured") unless provider

abort("Provider name is not bantu_zkp") unless provider[:name] == 'bantu_zkp'
abort("Strategy class missing in provider") unless provider[:strategy_class].to_s == 'Gitlab::Auth::BantuZkp'
abort("Strategy class missing in provider args") unless provider[:args][:strategy_class].to_s == 'Gitlab::Auth::BantuZkp'

puts "PROVIDER_OK"
"""
            res = subprocess.run(
                ["ruby", "-e", ruby_script, str(gitlab_rb)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Erreur de configuration provider dans gitlab.rb: {res.stderr}")
            self.assertIn("PROVIDER_OK", res.stdout)

    def test_docker_compose_cli_validation(self):
        """Valide la syntaxe des compositions via docker compose config si docker est disponible."""
        if shutil.which("docker") is not None:
            res_dev = subprocess.run(
                ["docker", "compose", "--env-file", ".env.example", "config", "--quiet"],
                cwd=self.root_dir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res_dev.returncode, 0, f"Erreur docker compose config dev: {res_dev.stderr}")

            env_file = ".env.production" if (self.root_dir / ".env.production").exists() else ".env.production.example"
            prod_cmd = [
                "docker",
                "compose",
                "-f",
                "docker-compose.production.yml",
                "--env-file",
                env_file,
                "config",
                "--quiet",
            ]
            env_override = os.environ.copy()
            env_override["ENV_FILE"] = env_file
            res_prod = subprocess.run(
                prod_cmd,
                cwd=self.root_dir,
                capture_output=True,
                text=True,
                env=env_override,
            )
            self.assertEqual(res_prod.returncode, 0, f"Erreur docker compose config prod: {res_prod.stderr}")
