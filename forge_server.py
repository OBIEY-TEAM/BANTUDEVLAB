"""
Moteur de Forge Git Souveraine BANTUDEVLAB (Gitea / GitLab CE Engine).
Fournit :
1. Interface Web moderne pour explorer les depots, commits, branches et PRs.
2. API REST v1 compatible Gitea / GitLab CE (/api/v1/*).
3. Protocole Git Smart HTTP pour git clone / git push via git http-backend.
4. Emetteur de Webhooks cryptographiques signes HMAC-SHA256 vers BantuDevLab Core.
"""

import hashlib
import hmac
import json
import os
import re
import subprocess
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from config.base_urls import BASE_URL_1, BASE_URL_2, GITEA_WEB_URL
except ImportError:
    BASE_URL_1 = os.environ.get("BASE_URL_1", "https://cybersocle.site")
    BASE_URL_2 = os.environ.get("BASE_URL_2", "https://git.cybersocle.site")
    GITEA_WEB_URL = os.environ.get("GITEA_WEB_URL", "https://gitea.cybersocle.site")

BASE_DIR = Path(__file__).resolve().parent
REPOS_DIR = BASE_DIR / "forge_data" / "repos"
BANTU_CORE_URL = os.environ.get("BANTU_CORE_URL", BASE_URL_1)
GITEA_LOGIN_URL = os.environ.get("GITEA_LOGIN_URL", f"{BASE_URL_2}/user/login")
WEBHOOK_SECRET = os.environ.get("GITEA_WEBHOOK_SECRET", "bantu_dev_webhook_secret_key_2026")
PORT = int(os.environ.get("FORGE_PORT", 3001))

FORGE_I18N = {
    "fr": {
        "brand_title": "BANTUDEVLAB FORGE GIT",
        "brand_badge": "FORGE SOUVERAINE",
        "switch_gitea": "Basculer vers Gitea",
        "portal_return": "Portail BantuDevLab",
        "dashboard_audit": "Tableau de Bord & Audit",
        "hero_title": "Moteur Git Gitea CE & Dépôts (Production)",
        "hero_desc": "Forge logicielle connectée en temps réel au portail BantuDevLab. Protocoles Git Smart HTTP, Zero-Trust ZKP et Webhooks signés HMAC.",
        "emit_webhook": "Émettre Webhook de Production HMAC vers BantuDevLab",
        "hosted_repos": "Dépôts Hébergés",
        "stars": "Étoiles",
        "forks": "Forks",
        "tier_badge": "Gitea CE",
        "clone_prompt": "Cloner le dépôt sur votre poste",
        "zkp_note": "Pour pousser avec ZKP, utilisez votre token généré depuis l'assistant Zero-Trust.",
        "recent_commits": "Historique Récent des Commits",
        "by_author": "Par",
        "theme_toggle": "Mode d'Affichage",
        "theme_dark": "Sombre",
        "theme_light": "Clair",
        "lang_fr": "Français",
        "lang_en": "English",
        "lang_sw": "Kiswahili",
        "lang_pt": "Português",
    },
    "en": {
        "brand_title": "BANTUDEVLAB GIT FORGE",
        "brand_badge": "SOVEREIGN FORGE",
        "switch_gitea": "Switch to Gitea",
        "switch_gitlab": "GitLab Workspace",
        "portal_return": "BantuDevLab Portal",
        "dashboard_audit": "Dashboard & Audit",
        "hero_title": "Pan-African Git Engine & Sovereign Repositories (Production)",
        "hero_desc": "Distributed software forge connected in real-time to the BantuDevLab portal. Git Smart HTTP protocols, Zero-Trust ZKP and HMAC signed Webhooks.",
        "emit_webhook": "Emit Production HMAC Webhook to BantuDevLab",
        "hosted_repos": "Repositories Hosted on Sovereign Infrastructure",
        "stars": "Stars",
        "forks": "Forks",
        "tier_badge": "Tier-1 Sovereign",
        "clone_prompt": "Clone repository to your workstation",
        "zkp_note": "To push with ZKP, use your sovereign token generated from the Zero-Trust assistant.",
        "recent_commits": "Recent Commits History",
        "by_author": "By",
        "theme_toggle": "Display Mode",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "lang_fr": "Francais",
        "lang_en": "English",
        "lang_sw": "Kiswahili",
        "lang_pt": "Portugues",
    },
    "sw": {
        "brand_title": "BANTUDEVLAB FORGE GIT",
        "brand_badge": "JUKWAA LA UHURU",
        "switch_gitea": "Badilisha kwenda Gitea",
        "switch_gitlab": "Sehemu ya GitLab",
        "portal_return": "Tovuti Kuu ya BantuDevLab",
        "dashboard_audit": "Dashibodi na Ukaguzi",
        "hero_title": "Injini ya Git ya Afrika na Hifadhi za Uhuru (Uzalishaji)",
        "hero_desc": "Jukwaa lililosambazwa lililounganishwa kwa wakati halisi na BantuDevLab. Itifaki za Git Smart HTTP, Zero-Trust ZKP na Webhooks za HMAC.",
        "emit_webhook": "Tuma Webhook ya HMAC kwa BantuDevLab",
        "hosted_repos": "Hifadhi Zilizowekwa kwenye Miundombinu Huru",
        "stars": "Nyota",
        "forks": "Forks",
        "tier_badge": "Kiwango cha 1 Uhuru",
        "clone_prompt": "Pakua msimbo kwenye kompyuta yako",
        "zkp_note": "Kusukuma na ZKP, tumia kitambulisho chako cha siri cha Zero-Trust.",
        "recent_commits": "Historia ya Hivi Karibuni ya Mabadiliko",
        "by_author": "Na",
        "theme_toggle": "Hali ya Skrini",
        "theme_dark": "Giza",
        "theme_light": "Mwanga",
        "lang_fr": "Francais",
        "lang_en": "English",
        "lang_sw": "Kiswahili",
        "lang_pt": "Portugues",
    },
    "pt": {
        "brand_title": "BANTUDEVLAB FORJA GIT",
        "brand_badge": "FORJA SOBERANA",
        "switch_gitea": "Mudar para Gitea",
        "switch_gitlab": "Espaco GitLab",
        "portal_return": "Portal BantuDevLab",
        "dashboard_audit": "Painel & Auditoria",
        "hero_title": "Motor Git Pan-Africano & Repositorios Soberanos (Producao)",
        "hero_desc": "Forja distribuida conectada em tempo real ao portal BantuDevLab. Protocolos Git Smart HTTP, Zero-Trust ZKP e Webhooks HMAC.",
        "emit_webhook": "Emitir Webhook HMAC de Producao para BantuDevLab",
        "hosted_repos": "Repositorios Hospedados na Infraestrutura Soberana",
        "stars": "Estrelas",
        "forks": "Forks",
        "tier_badge": "Tier-1 Soberano",
        "clone_prompt": "Clonar o repositorio em sua maquina",
        "zkp_note": "Para enviar com ZKP, use seu token soberano gerado no assistente Zero-Trust.",
        "recent_commits": "Historico Recente de Commits",
        "by_author": "Por",
        "theme_toggle": "Modo de Exibicao",
        "theme_dark": "Escuro",
        "theme_light": "Claro",
        "lang_fr": "Francais",
        "lang_en": "English",
        "lang_sw": "Kiswahili",
        "lang_pt": "Portugues",
    },
}

REPO_METADATA = {
    "sovereign-org/afri-fintech-gateway": {
        "description": "Passerelle panafricaine de paiement mobile & interoperabilite souveraine",
        "stars": 42,
        "forks": 12,
        "sovereignty_level": "Tier-1 Continental",
    },
    "sovereign-org/agro-sentinel-ai": {
        "description": "Modeles de vision embarquee pour la surveillance des recoltes saheliennes",
        "stars": 89,
        "forks": 27,
        "sovereignty_level": "Tier-1 Continental",
    },
    "bantudevlab/bantu-zkp-identity": {
        "description": "Bibliotheque cryptographique Zero-Knowledge Proof pour l'Afrique de l'Ouest",
        "stars": 154,
        "forks": 34,
        "sovereignty_level": "Tier-1 Continental",
    },
}

PULL_REQUESTS_STORE = [
    {
        "id": 1,
        "number": 1,
        "repo": "sovereign-org/afri-fintech-gateway",
        "title": "Integration du protocole Schnorr NIZKP",
        "state": "open",
        "head": {"label": "feat/schnorr-zkp", "ref": "feat/schnorr-zkp"},
        "base": {"label": "main", "ref": "main"},
        "user": {"username": "kouame-dev"},
        "created_at": "2026-05-10T10:00:00Z",
        "updated_at": "2026-05-10T12:00:00Z",
    }
]


class SovereignForgeHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Gitea-Signature")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath, content_type):
        p = Path(filepath)
        if not p.exists():
            return self._send_json({"error": "File not found"}, status=404)
        data = p.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _get_lang_and_theme(self):
        url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(url.query)
        cookie_str = self.headers.get("Cookie", "")

        theme = "dark"
        if "theme" in qs and qs["theme"][0] in ("light", "github"):
            theme = "light"
        elif "bantu_theme=light" in cookie_str or "theme=github;" in cookie_str or cookie_str.endswith("theme=github"):
            theme = "light"

        lang = "fr"
        if "lang" in qs:
            val = qs["lang"][0].lower()
            if "en" in val:
                lang = "en"
            elif "sw" in val:
                lang = "sw"
            elif "pt" in val:
                lang = "pt"
            elif "fr" in val:
                lang = "fr"
        elif "bantu_lang=en" in cookie_str or "django_language=en" in cookie_str or "lang=en-US" in cookie_str:
            lang = "en"
        elif "bantu_lang=sw" in cookie_str or "django_language=sw" in cookie_str or "lang=sw-KE" in cookie_str:
            lang = "sw"
        elif "bantu_lang=pt" in cookie_str or "django_language=pt" in cookie_str or "lang=pt-PT" in cookie_str:
            lang = "pt"

        return lang, theme

    def _send_html(self, html_content, status=200):
        body = html_content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Gitea-Signature")
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        urllib.parse.parse_qs(url.query)

        # 0. Health probes (unauthenticated JSON)
        if path in ("/health", "/healthz", "/readyz"):
            return self._send_json({"status": "ok", "service": "forge-engine", "health": "healthy"})

        # 0. Static routes for Cyber Logo, Favicon & Sync JS
        if path in ("/static/img/logo.svg", "/assets/img/logo.svg", "/img/logo.svg", "/logo.svg"):
            return self._send_file(BASE_DIR / "static" / "img" / "logo.svg", "image/svg+xml")
        if path in ("/static/img/logo.png", "/assets/img/logo.png", "/img/logo.png", "/logo.png"):
            return self._send_file(BASE_DIR / "static" / "img" / "logo.png", "image/png")
        if path in ("/static/img/favicon.svg", "/assets/img/favicon.svg", "/favicon.svg"):
            return self._send_file(BASE_DIR / "static" / "img" / "favicon.svg", "image/svg+xml")
        if path in ("/static/js/bantu-ecosystem-sync.js", "/assets/js/bantu-ecosystem-sync.js", "/sync.js"):
            return self._send_file(BASE_DIR / "static" / "js" / "bantu-ecosystem-sync.js", "application/javascript")
        if path == "/api/sync/state":
            lang, theme = self._get_lang_and_theme()
            return self._send_json({"lang": lang, "theme": theme, "ts": int(time.time() * 1000)})

        # 1. API: /api/v1/version & /api/v4/version (GitLab CE)
        if path == "/api/v4/version":
            return self._send_json(
                {
                    "version": "16.11.0-gitlab-sovereign",
                    "revision": "7bf3e9a4f21",
                    "status": "ONLINE",
                    "engine": "GitLab CE Panafricain",
                }
            )

        if path == "/api/v4/user":
            return self._send_json(
                {
                    "id": 1,
                    "username": "sovereign_admin",
                    "name": "Administrateur Souverain",
                    "state": "active",
                }
            )

        if path == "/api/v4/projects":
            return self._send_json(self._get_gitlab_projects_list())

        m_gl_proj = re.match(r"^/api/v4/projects/(\d+)$", path)
        if m_gl_proj:
            pid = int(m_gl_proj.group(1))
            for p in self._get_gitlab_projects_list():
                if p["id"] == pid:
                    return self._send_json(p)
            return self._send_json({"message": "404 Project Not Found"}, status=404)

        if path == "/api/v1/version":
            return self._send_json(
                {
                    "version": "1.23.0-sovereign-panafrican",
                    "status": "ONLINE",
                    "engine": "Gitea / GitLab CE Hybrid",
                    "cloud_provider": "Systalink Cloud Sovereign Cluster",
                    "location": "Abidjan Tier-3 Datacenter",
                }
            )

        # 2. API: /api/v1/repos/search
        if path == "/api/v1/repos/search":
            repos = self._get_repos_list()
            return self._send_json({"ok": True, "data": repos})

        # 3. API: /api/v1/repos/{owner}/{repo}/commits
        m_commits = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/commits$", path)
        if m_commits:
            owner, repo = m_commits.groups()
            commits = self._get_repo_commits(owner, repo)
            return self._send_json(commits)

        # 4. API: /api/v1/repos/{owner}/{repo}/branches
        m_branches = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/branches$", path)
        if m_branches:
            owner, repo = m_branches.groups()
            branches = self._get_repo_branches(owner, repo)
            return self._send_json(branches)

        # 5. API: /api/v1/repos/{owner}/{repo}/pulls
        m_pulls = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/pulls$", path)
        if m_pulls:
            owner, repo = m_pulls.groups()
            pulls = [p for p in PULL_REQUESTS_STORE if p["repo"] == f"{owner}/{repo}"]
            return self._send_json(pulls)

        # 6. Smart Git HTTP backend
        if ".git" in path:
            return self._handle_git_http(url)

        # 7. UI: Web Pages
        if path.rstrip("/") in ("/gitea", "/switch-gitea", "/basculer-gitea"):
            self.send_response(302)
            self.send_header("Location", GITEA_LOGIN_URL)
            self.end_headers()
            return

        if path in ("", "/", "/explore", "/gitlab"):
            return self._render_home_ui()

        m_repo_ui = re.match(r"^/([^/]+)/([^/]+)$", path)
        if m_repo_ui:
            owner, repo = m_repo_ui.groups()
            return self._render_repo_ui(owner, repo)

        return self._send_html("<h1>404 - Page Introuvable</h1>", status=404)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b""

        # 1. API: /api/v1/user/repos
        if path == "/api/v1/user/repos":
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                data = {}
            name = data.get("name", "nouveau-depot")
            desc = data.get("description", "")
            private = bool(data.get("private", False))

            repo_full = self._create_repo("sovereign-org", name, desc, private)
            return self._send_json(repo_full, status=201)

        # 2. Trigger webhook towards BantuDevLab Core (Gitea / GitLab)
        if path in ("/trigger-webhook", "/trigger-gitlab-webhook"):
            try:
                data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
            except Exception:
                data = {}
            if "gitlab" in path or data.get("forge") == "gitlab":
                result = self._dispatch_gitlab_webhook(data)
            else:
                result = self._dispatch_webhook(data)
            return self._send_json(result)

        # 3. Smart Git HTTP backend POST
        if ".git" in path:
            return self._handle_git_http_post(url, body_bytes)

        return self._send_json({"error": "Endpoint inconnu"}, status=404)

    def do_PATCH(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/")
        content_len = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_len) if content_len > 0 else b""
        try:
            data = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            data = {}

        m_pr = re.match(r"^/api/v1/repos/([^/]+)/([^/]+)/pulls/(\d+)$", path)
        if m_pr:
            owner, repo, pr_id = m_pr.groups()
            for p in PULL_REQUESTS_STORE:
                if p["repo"] == f"{owner}/{repo}" and str(p["number"]) == pr_id:
                    if "state" in data:
                        p["state"] = data["state"]
                    if "title" in data:
                        p["title"] = data["title"]
                    return self._send_json(p)
            return self._send_json({"error": "PR introuvable"}, status=404)

        return self._send_json({"error": "Endpoint inconnu"}, status=404)

    # ---------------- Git HTTP backend ----------------
    def _handle_git_http(self, url):
        # Service info/refs
        git_dir, service = self._resolve_git_repo(url.path)
        if not git_dir or not git_dir.exists():
            return self._send_html("Dépôt Git introuvable", status=404)

        query = urllib.parse.parse_qs(url.query)
        svc = query.get("service", [None])[0]
        if svc in ("git-upload-pack", "git-receive-pack"):
            cmd = ["git", svc.replace("git-", ""), "--stateless-rpc", "--advertise-refs", str(git_dir)]
            res = subprocess.run(cmd, capture_output=True)
            self.send_response(200)
            self.send_header("Content-Type", f"application/x-{svc}-advertisement")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            # Smart HTTP header packet
            packet = f"# service={svc}\n"
            hex_len = f"{len(packet) + 4:04x}"
            self.wfile.write(f"{hex_len}{packet}0000".encode("utf-8"))
            self.wfile.write(res.stdout)
            return

        self._send_html("Git HTTP info", status=200)

    def _handle_git_http_post(self, url, body_bytes):
        git_dir, service = self._resolve_git_repo(url.path)
        if not git_dir or not git_dir.exists():
            return self._send_html("Dépôt Git introuvable", status=404)

        svc = "upload-pack" if "upload-pack" in url.path else "receive-pack"
        cmd = ["git", svc, "--stateless-rpc", str(git_dir)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = proc.communicate(input=body_bytes)

        self.send_response(200)
        self.send_header("Content-Type", f"application/x-git-{svc}-result")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(out)

    def _resolve_git_repo(self, path):
        m = re.search(r"/([^/]+)/([^/]+)\.git", path)
        if m:
            owner, name = m.groups()
            return REPOS_DIR / owner / f"{name}.git", None
        return None, None

    # ---------------- Helpers Git ----------------
    def _get_repos_list(self):
        items = []
        if REPOS_DIR.exists():
            for owner_dir in REPOS_DIR.iterdir():
                if owner_dir.is_dir():
                    for repo_dir in owner_dir.glob("*.git"):
                        name = repo_dir.stem
                        full = f"{owner_dir.name}/{name}"
                        meta = REPO_METADATA.get(
                            full,
                            {
                                "description": "Dépôt souverain BANTUDEVLAB",
                                "stars": 10,
                                "forks": 2,
                                "sovereignty_level": "Tier-1 Continental",
                            },
                        )
                        items.append(
                            {
                                "id": abs(hash(full)) % 10000,
                                "name": name,
                                "full_name": full,
                                "description": meta["description"],
                                "private": False,
                                "stars_count": meta["stars"],
                                "forks_count": meta["forks"],
                                "open_issues_count": 1,
                                "owner": {"username": owner_dir.name},
                                "clone_url": f"http://localhost:{PORT}/{full}.git",
                                "html_url": f"http://localhost:{PORT}/{full}",
                                "default_branch": "main",
                                "sovereignty_level": meta["sovereignty_level"],
                            }
                        )
        return items

    def _get_gitlab_projects_list(self):
        repos = self._get_repos_list()
        projects = []
        for r in repos:
            owner, name = r["full_name"].split("/", 1)
            projects.append(
                {
                    "id": r["id"],
                    "name": name,
                    "path": name,
                    "path_with_namespace": r["full_name"],
                    "description": r["description"],
                    "star_count": r["stars_count"],
                    "forks_count": r["forks_count"],
                    "web_url": f"http://localhost:{PORT}/{r['full_name']}",
                    "http_url_to_repo": f"http://localhost:{PORT}/{r['full_name']}.git",
                    "default_branch": "main",
                    "visibility": "public",
                    "created_at": "2026-01-01T00:00:00.000Z",
                    "last_activity_at": "2026-11-02T04:00:00.000Z",
                    "namespace": {"id": 1, "name": owner, "path": owner, "kind": "group"},
                }
            )
        return projects

    def _get_repo_commits(self, owner, repo):
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return []
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "log", "-n", "10", "--pretty=format:%H||%an||%ad||%s", "--date=iso"],
            capture_output=True,
            text=True,
        )
        commits = []
        for line in res.stdout.splitlines():
            parts = line.split("||")
            if len(parts) == 4:
                commits.append(
                    {
                        "sha": parts[0],
                        "commit": {
                            "author": {"name": parts[1], "date": parts[2]},
                            "message": parts[3],
                        },
                    }
                )
        return commits

    def _get_repo_branches(self, owner, repo):
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return [{"name": "main", "commit": {"id": "000000"}}]
        res = subprocess.run(
            ["git", "-C", str(repo_dir), "branch", "--format=%(refname:short)"],
            capture_output=True,
            text=True,
        )
        branches = [{"name": b.strip(), "commit": {"id": "HEAD"}} for b in res.stdout.splitlines() if b.strip()]
        return branches or [{"name": "main", "commit": {"id": "HEAD"}}]

    def _create_repo(self, owner, name, desc="", private=False):
        repo_dir = REPOS_DIR / owner / f"{name}.git"
        repo_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "--bare", str(repo_dir)], check=True, capture_output=True)
        REPO_METADATA[f"{owner}/{name}"] = {
            "description": desc or "Dépôt souverain BANTUDEVLAB",
            "stars": 1,
            "forks": 0,
            "sovereignty_level": "Tier-1 Continental",
        }
        return {
            "id": abs(hash(f"{owner}/{name}")) % 10000,
            "name": name,
            "full_name": f"{owner}/{name}",
            "description": desc,
            "private": private,
            "html_url": f"http://localhost:{PORT}/{owner}/{name}",
            "clone_url": f"http://localhost:{PORT}/{owner}/{name}.git",
        }

    def _dispatch_webhook(self, payload):
        import urllib.request

        webhook_url = f"{BANTU_CORE_URL}/api/forge/webhook/"
        body = json.dumps(payload).encode("utf-8")
        sig = hmac.new(WEBHOOK_SECRET.encode("utf-8"), body, hashlib.sha256).hexdigest()
        req = urllib.request.Request(
            webhook_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Gitea-Signature": sig,
                "X-Gitea-Event": "push",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "bantu_response": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _dispatch_gitlab_webhook(self, payload):
        import urllib.request

        webhook_url = f"{BANTU_CORE_URL}/api/gitlab/webhook/"
        body = json.dumps(payload).encode("utf-8")
        token = os.environ.get("GITLAB_WEBHOOK_SECRET", "bantu_gitlab_webhook_secret_2026")
        req = urllib.request.Request(
            webhook_url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "X-Gitlab-Token": token,
                "X-Gitlab-Event": "Push Hook",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"success": True, "gitlab_response": data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ---------------- UI Templates ----------------
    def _render_navbar(self, lang, theme, active_view="gitlab"):
        t = FORGE_I18N.get(lang, FORGE_I18N["fr"])
        brand_title = t["brand_title"]
        brand_badge = t["brand_badge"]
        switch_gitea = t["switch_gitea"]
        portal_return = t["portal_return"]
        dashboard_audit = t["dashboard_audit"]
        theme_toggle = t["theme_toggle"]
        theme_label = t["theme_light"] if theme == "dark" else t["theme_dark"]

        theme_icon = (
            """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>"""
            if theme == "dark"
            else """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0070f3" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>"""
        )

        sel_fr = "selected" if lang == "fr" else ""
        sel_en = "selected" if lang == "en" else ""
        sel_sw = "selected" if lang == "sw" else ""
        sel_pt = "selected" if lang == "pt" else ""

        return f"""
    <nav class="navbar">
        <a href="/" class="brand">
            <img src="/static/img/logo.svg" width="34" height="34" alt="BantuDevLab Logo" class="brand-logo">
            <span>{brand_title}</span>
            <span class="badge">{brand_badge}</span>
        </a>
        <div class="nav-controls">
            <!-- Language selector -->
            <div class="control-box">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                <select id="forgeLangSelect" class="sync-select" onchange="changeForgeLang(this.value)">
                    <option value="fr" {sel_fr}>FR - {t["lang_fr"]}</option>
                    <option value="en" {sel_en}>EN - {t["lang_en"]}</option>
                    <option value="sw" {sel_sw}>SW - {t["lang_sw"]}</option>
                    <option value="pt" {sel_pt}>PT - {t["lang_pt"]}</option>
                </select>
            </div>

            <!-- Theme toggle -->
            <button id="forgeThemeBtn" class="theme-btn" onclick="toggleForgeTheme()" title="{theme_toggle}">
                {theme_icon}
                <span id="forgeThemeLabel">{theme_label}</span>
            </button>

            <!-- Ecosystem navigation links -->
            <a href="{GITEA_LOGIN_URL}" class="btn btn-outline" style="border-color: var(--cyan); color: var(--cyan);">{switch_gitea} &rarr;</a>
            <a href="{BANTU_CORE_URL}/" class="btn btn-outline">&larr; {portal_return}</a>
            <a href="{BANTU_CORE_URL}/dashboard/" class="btn btn-gold">{dashboard_audit}</a>
        </div>
    </nav>"""

    def _render_head(self, title, theme):
        return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="icon" type="image/svg+xml" href="/static/img/favicon.svg">
    <style>
        :root {{
            --gold: #f59e0b;
            --emerald: #10b981;
            --cyan: #00e5ff;
            --blue: #0070f3;
            --bg: #020617;
            --surface: #070e1e;
            --surface-card: #0b1528;
            --border: #1e293b;
            --text: #f8fafc;
            --muted: #94a3b8;
        }}
        [data-theme="light"] {{
            --gold: #d97706;
            --emerald: #059669;
            --cyan: #0284c7;
            --blue: #0051cc;
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-card: #f1f5f9;
            --border: #cbd5e1;
            --text: #0f172a;
            --muted: #64748b;
        }}
        body {{
            margin: 0; font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg); color: var(--text); line-height: 1.6;
            transition: background-color 0.2s ease, color 0.2s ease;
        }}
        .navbar {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 0.85rem 2rem; background: var(--surface); border-bottom: 2px solid var(--gold);
            flex-wrap: wrap; gap: 1rem;
        }}
        .brand {{ display: flex; align-items: center; gap: 0.6rem; font-weight: 800; font-size: 1.15rem; color: var(--text); text-decoration: none; }}
        .brand-logo {{
            border-radius: 8px; box-shadow: 0 0 12px rgba(0, 229, 255, 0.45);
            vertical-align: middle; border: 1px solid rgba(0, 229, 255, 0.3);
        }}
        .badge {{ background: var(--gold); color: #000; font-size: 0.72rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; letter-spacing: 0.5px; }}
        .nav-controls {{ display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap; }}
        .control-box {{
            display: flex; align-items: center; background: var(--surface-card);
            border: 1px solid var(--border); border-radius: 6px; padding: 0.25rem 0.6rem; color: var(--text);
        }}
        .sync-select {{
            background: transparent; border: none; color: var(--text); font-size: 0.82rem;
            outline: none; cursor: pointer; font-family: inherit; font-weight: 600;
        }}
        .sync-select option {{ background: var(--surface); color: var(--text); }}
        .theme-btn {{
            display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.75rem;
            background: var(--surface-card); border: 1px solid var(--border); border-radius: 6px;
            color: var(--text); font-size: 0.82rem; font-weight: 600; cursor: pointer; font-family: inherit;
        }}
        .theme-btn:hover {{ border-color: var(--cyan); }}
        .container {{ max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
        .btn {{
            display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.85rem; border-radius: 6px;
            font-weight: 600; font-size: 0.84rem; text-decoration: none; cursor: pointer; border: none;
        }}
        .btn-gold {{ background: var(--gold); color: #000; }}
        .btn-gold:hover {{ opacity: 0.9; }}
        .btn-emerald {{ background: var(--emerald); color: #000; }}
        .btn-outline {{ background: transparent; border: 1px solid var(--border); color: var(--text); }}
        .btn-outline:hover {{ border-color: var(--gold); color: var(--gold); }}
        .hero {{
            background: radial-gradient(circle at 50% 10%, rgba(245, 158, 11, 0.12), transparent 70%);
            padding: 2.25rem; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 2rem; text-align: center;
        }}
        .repo-card {{
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .repo-card:hover {{ border-color: var(--cyan); transform: translateY(-2px); }}
        .repo-header {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }}
        .repo-title {{ font-size: 1.15rem; font-weight: 700; color: var(--gold); text-decoration: none; word-break: break-word; }}
        .repo-desc {{ color: var(--muted); margin: 0.5rem 0; font-size: 0.95rem; }}
        .repo-footer {{ display: flex; gap: 1.5rem; align-items: center; font-size: 0.85rem; color: var(--muted); flex-wrap: wrap; }}
        .clone-snippet {{ background: var(--surface-card); padding: 0.25rem 0.6rem; border-radius: 4px; color: var(--emerald); font-family: monospace; border: 1px solid var(--border); max-width: 100%; overflow-x: auto; word-break: break-all; }}
        *, *::before, *::after {{ box-sizing: border-box; }}
        html, body {{ max-width: 100vw; overflow-x: hidden; }}
        @media (min-width: 1600px) {{
            .container {{ max-width: 1440px; }}
        }}
        @media (max-width: 768px) {{
            .navbar {{ padding: 0.75rem 1rem; }}
            .nav-controls {{ width: 100%; justify-content: flex-start; gap: 0.5rem; }}
            .hero {{ padding: 1.5rem 1rem; }}
            .hero h1 {{ font-size: 1.5rem; }}
            .repo-card {{ padding: 1rem; }}
            .repo-footer {{ gap: 0.75rem; }}
        }}
        @media (max-width: 480px) {{
            .brand .badge {{ display: none; }}
            .nav-controls .btn {{ width: 100%; justify-content: center; text-align: center; }}
        }}
    </style>
</head>"""

    def _render_scripts(self):
        return """
    <script src="/static/js/bantu-ecosystem-sync.js"></script>
    <script>
    function changeForgeLang(newLang) {
        if (window.syncEcosystemChange) {
            window.syncEcosystemChange(null, newLang);
        } else {
            document.cookie = 'bantu_lang=' + newLang + ';path=/;max-age=31536000';
            document.cookie = 'django_language=' + newLang + ';path=/;max-age=31536000';
            window.location.search = '?lang=' + newLang;
        }
    }

    function toggleForgeTheme() {
        const cur = document.documentElement.getAttribute('data-theme') || 'dark';
        const next = (cur === 'dark') ? 'light' : 'dark';
        if (window.syncEcosystemChange) {
            window.syncEcosystemChange(next, null);
        } else {
            document.documentElement.setAttribute('data-theme', next);
            document.cookie = 'bantu_theme=' + next + ';path=/;max-age=31536000';
            document.cookie = 'theme=' + (next === 'light' ? 'github' : 'github-dark') + ';path=/;max-age=31536000';
            const label = document.getElementById('forgeThemeLabel');
            if (label) label.textContent = (next === 'dark') ? 'Clair' : 'Sombre';
        }
    }

    function triggerTestWebhook() {
        const out = document.getElementById('webhookResult');
        if (!out) return;
        out.textContent = "Envoi du webhook HMAC en cours...";
        fetch('/trigger-webhook', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                repository: { name: 'afri-fintech-gateway' },
                pusher: { username: 'kouame_dev' },
                ref: 'refs/heads/main'
            })
        })
        .then(r => r.json())
        .then(data => {
            out.textContent = "Webhook acquitte par BantuDevLab Core : " + JSON.stringify(data.bantu_response || data);
        })
        .catch(err => {
            out.textContent = "Erreur webhook : " + err.message;
        });
    }
    </script>"""

    def _render_home_ui(self):
        lang, theme = self._get_lang_and_theme()
        t = FORGE_I18N.get(lang, FORGE_I18N["fr"])
        repos = self._get_repos_list()
        repos_html = "".join(
            f"""
        <div class="repo-card">
            <div class="repo-header">
                <a href="/{r["full_name"]}" class="repo-title">{r["full_name"]}</a>
                <span class="badge">{t["tier_badge"]}</span>
            </div>
            <p class="repo-desc">{r["description"]}</p>
            <div class="repo-footer">
                <span>{t["stars"]}: {r["stars_count"]}</span>
                <span>{t["forks"]}: {r["forks_count"]}</span>
                <code class="clone-snippet">git clone {r["clone_url"]}</code>
            </div>
        </div>
        """
            for r in repos
        )

        repos_section = f"<h2>{t['hosted_repos']}</h2>\n        {repos_html}" if repos else ""
        html = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="{theme}">
{self._render_head(f"BANTUDEVLAB - {t['brand_title']}", theme)}
<body>
    {self._render_navbar(lang, theme, active_view="gitlab")}

    <div class="container">
        <div class="hero">
            <h1 style="margin-top: 0;">{t["hero_title"]}</h1>
            <p style="color: var(--muted); max-width: 700px; margin: 0 auto 1.5rem;">
                {t["hero_desc"]}
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <button class="btn btn-gold" onclick="triggerTestWebhook()">{t["emit_webhook"]}</button>
            </div>
            <div id="webhookResult" style="margin-top: 1rem; font-family: monospace; font-size: 0.85rem; color: var(--emerald);"></div>
        </div>

        {repos_section}
    </div>

    {self._render_scripts()}
</body>
</html>"""
        return self._send_html(html)

    def _render_gitea_ui(self):
        lang, theme = self._get_lang_and_theme()
        t = FORGE_I18N.get(lang, FORGE_I18N["fr"])
        repos = self._get_repos_list()
        repos_html = "".join(
            f"""
        <div class="repo-card" style="border-left: 3px solid var(--emerald);">
            <div class="repo-header">
                <a href="/{r["full_name"]}" class="repo-title" style="color: var(--emerald);">{r["full_name"]}</a>
                <span class="badge" style="background: var(--emerald); color: #000;">Gitea CE Souverain</span>
            </div>
            <p class="repo-desc">{r["description"]}</p>
            <div class="repo-footer">
                <span>{t["stars"]}: {r["stars_count"]}</span>
                <span>{t["forks"]}: {r["forks_count"]}</span>
                <code class="clone-snippet">git clone {r["clone_url"]}</code>
            </div>
        </div>
        """
            for r in repos
        )

        repos_section = f"<h2>{t['hosted_repos']}</h2>\n        {repos_html}" if repos else ""
        html = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="{theme}">
{self._render_head("Gitea Souverain - BANTUDEVLAB", theme)}
<body>
    {self._render_navbar(lang, theme, active_view="gitea")}

    <div class="container">
        <div class="hero" style="background: radial-gradient(circle at 50% 10%, rgba(16, 185, 129, 0.12), transparent 70%);">
            <h1 style="margin-top: 0; color: var(--emerald);">Forge Logicielle Gitea Souveraine</h1>
            <p style="color: var(--muted); max-width: 700px; margin: 0 auto 1.5rem;">
                {t["hero_desc"]}
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <a href="/api/v1/version" target="_blank" class="btn btn-outline">Consulter Version API v1</a>
                <a href="/" class="btn btn-emerald">{t["portal_return"]}</a>
            </div>
        </div>

        {repos_section}
    </div>

    {self._render_scripts()}
</body>
</html>"""
        return self._send_html(html)

    def _render_repo_ui(self, owner, repo):
        lang, theme = self._get_lang_and_theme()
        t = FORGE_I18N.get(lang, FORGE_I18N["fr"])
        repo_dir = REPOS_DIR / owner / f"{repo}.git"
        if not repo_dir.exists():
            return self._send_html("Depot introuvable", status=404)

        commits = self._get_repo_commits(owner, repo)
        self._get_repo_branches(owner, repo)
        commits_html = "".join(
            f"""
        <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border); font-size: 0.9rem;">
            <strong>{c["commit"]["message"]}</strong>
            <div style="color: var(--muted); font-size: 0.8rem;">
                {t["by_author"]} {c["commit"]["author"]["name"]} - SHA: <code>{c["sha"][:8]}</code> - {c["commit"]["author"]["date"]}
            </div>
        </li>
        """
            for c in commits
        )

        repos_section = f"<h2>{t['hosted_repos']}</h2>\n        {repos_html}" if repos else ""
        html = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="{theme}">
{self._render_head(f"{owner}/{repo} - BantuDevLab Forge", theme)}
<body>
    {self._render_navbar(lang, theme, active_view="repo")}
    <div class="container">
        <h1>{owner}/{repo}</h1>
        <div class="repo-card">
            <h3>{t["clone_prompt"]}</h3>
            <div style="background: var(--surface-card); padding: 0.75rem; border-radius: 6px; font-family: monospace; color: var(--emerald); display: flex; justify-content: space-between; border: 1px solid var(--border);">
                <span>git clone http://localhost:{PORT}/{owner}/{repo}.git</span>
            </div>
            <p style="font-size: 0.85rem; color: var(--muted); margin-top: 0.5rem;">
                {t["zkp_note"]}
            </p>
        </div>
        <div class="repo-card">
            <h3>{t["recent_commits"]} ({len(commits)})</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {commits_html}
            </ul>
        </div>
    </div>

    {self._render_scripts()}
</body>
</html>"""
        return self._send_html(html)


def run_server():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), SovereignForgeHandler)
    server.daemon_threads = True
    print(f"BantuDevLab Sovereign Git Forge Engine démarré sur http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
