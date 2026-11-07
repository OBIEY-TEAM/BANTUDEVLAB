"""
Centralized Base URLs Configuration for BANTUDEVLAB Sovereign Platform.

Defines the foundational sovereign domains and services:
- BASE_URL_1: Main Sovereign Web Portal (https://cybersocle.site)
- BASE_URL_2: Forge Git / Code Collaboration (https://git.cybersocle.site)
- BASE_URL_3: Sovereign REST API & Services (https://api.cybersocle.site)
- GITEA_WEB_URL: Gitea Web UI (https://gitea.cybersocle.site)
- FORGE_INTERNAL_URL: Internal Forge Engine (https://forge.cybersocle.site)
- AI_URL: AI / Gemma LLM Gateway (https://ai.cybersocle.site)

All application URLs, clone endpoints, webhook callbacks, attestation links,
and external references should be dynamically constructed from these base URLs
rather than hardcoding localhost or static development addresses.
"""

import os
from urllib.parse import urlparse

# Canonical sovereign production endpoints
DEFAULT_BASE_URL_1 = "https://cybersocle.site"
DEFAULT_BASE_URL_2 = "https://git.cybersocle.site"
DEFAULT_BASE_URL_3 = "https://api.cybersocle.site"

DEFAULT_FORGE_SIGNUP_URL = f"{DEFAULT_BASE_URL_2}/users/sign_up"
DEFAULT_GITEA_WEB_URL = "https://gitea.cybersocle.site"
DEFAULT_FORGE_INTERNAL_URL = "https://forge.cybersocle.site"
DEFAULT_AI_URL = "https://ai.cybersocle.site"

# Environment-configurable base URLs (sanitized without trailing slash)
BASE_URL_1 = os.environ.get("BASE_URL_1", DEFAULT_BASE_URL_1).rstrip("/")
BASE_URL_2 = os.environ.get("BASE_URL_2", DEFAULT_BASE_URL_2).rstrip("/")
BASE_URL_3 = os.environ.get("BASE_URL_3", DEFAULT_BASE_URL_3).rstrip("/")

FORGE_SIGNUP_URL = os.environ.get(
    "FORGE_SIGNUP_URL",
    os.environ.get("GITLAB_SIGNUP_URL", f"{BASE_URL_2}/users/sign_up"),
).rstrip("/")
GITEA_WEB_URL = os.environ.get("GITEA_WEB_URL", os.environ.get("GITEA_EXTERNAL_URL", DEFAULT_GITEA_WEB_URL)).rstrip("/")
FORGE_INTERNAL_URL = os.environ.get("FORGE_INTERNAL_URL", DEFAULT_FORGE_INTERNAL_URL).rstrip("/")
AI_URL = os.environ.get("AI_URL", os.environ.get("GEMMA_API_URL", DEFAULT_AI_URL)).rstrip("/")


def get_base_urls() -> dict[str, str]:
    """Returns the sovereign service URLs as a dictionary."""
    return {
        "BASE_URL_1": BASE_URL_1,
        "BASE_URL_2": BASE_URL_2,
        "BASE_URL_3": BASE_URL_3,
        "FORGE_SIGNUP_URL": FORGE_SIGNUP_URL,
        "GITEA_WEB_URL": GITEA_WEB_URL,
        "FORGE_INTERNAL_URL": FORGE_INTERNAL_URL,
        "AI_URL": AI_URL,
    }


def get_base_domains() -> list[str]:
    """Extracts unique hostnames/domains from all sovereign URLs."""
    urls = (BASE_URL_1, BASE_URL_2, BASE_URL_3, GITEA_WEB_URL, FORGE_INTERNAL_URL, AI_URL)
    domains = []
    for u in urls:
        parsed = urlparse(u)
        netloc = parsed.netloc or parsed.path
        if ":" in netloc:
            netloc = netloc.split(":")[0]
        if netloc and netloc not in domains:
            domains.append(netloc)
    return domains


def build_url(base: str, path: str = "") -> str:
    """
    Constructs a URL from a given base URL and path.
    Guarantees proper slash concatenation.
    """
    base_clean = (base or "").rstrip("/")
    if not path:
        return base_clean
    path_clean = path if path.startswith("/") else f"/{path}"
    return f"{base_clean}{path_clean}"


def build_portal_url(path: str = "") -> str:
    """Constructs a URL relative to BASE_URL_1 (Main Sovereign Web Portal)."""
    return build_url(BASE_URL_1, path)


def build_git_url(path: str = "") -> str:
    """Constructs a URL relative to BASE_URL_2 (Forge Git / GitLab / Gitea)."""
    return build_url(BASE_URL_2, path)


def build_api_url(path: str = "") -> str:
    """Constructs a URL relative to BASE_URL_3 (Sovereign API & Services)."""
    return build_url(BASE_URL_3, path)


def build_gitea_url(path: str = "") -> str:
    """Constructs a URL relative to GITEA_WEB_URL (Gitea Web UI)."""
    return build_url(GITEA_WEB_URL, path)


def build_forge_url(path: str = "") -> str:
    """Constructs a URL relative to FORGE_INTERNAL_URL (Internal Forge Engine)."""
    return build_url(FORGE_INTERNAL_URL, path)


def build_ai_url(path: str = "") -> str:
    """Constructs a URL relative to AI_URL (AI / Gemma LLM Gateway)."""
    return build_url(AI_URL, path)
