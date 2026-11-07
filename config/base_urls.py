"""
Centralized Base URLs Configuration for BANTUDEVLAB Sovereign Platform.

Defines the three foundational domains/base URLs:
- BASE_URL_1: Main Sovereign Web Portal (https://cybersocle.site)
- BASE_URL_2: Forge Git / Code Collaboration (https://git.cybersocle.site)
- BASE_URL_3: Sovereign REST API & Services (https://api.cybersocle.site)

All application URLs, clone endpoints, webhook callbacks, attestation links,
and external references should be dynamically constructed from these base URLs
rather than hardcoded.
"""

import os
from urllib.parse import urlparse

# Default sovereign production endpoints
DEFAULT_BASE_URL_1 = "https://cybersocle.site"
DEFAULT_BASE_URL_2 = "https://git.cybersocle.site"
DEFAULT_BASE_URL_3 = "https://api.cybersocle.site"

# Environment-configurable base URLs (sanitized without trailing slash)
BASE_URL_1 = os.environ.get("BASE_URL_1", DEFAULT_BASE_URL_1).rstrip("/")
BASE_URL_2 = os.environ.get("BASE_URL_2", DEFAULT_BASE_URL_2).rstrip("/")
BASE_URL_3 = os.environ.get("BASE_URL_3", DEFAULT_BASE_URL_3).rstrip("/")


def get_base_urls() -> dict[str, str]:
    """Returns the three base URLs as a dictionary."""
    return {
        "BASE_URL_1": BASE_URL_1,
        "BASE_URL_2": BASE_URL_2,
        "BASE_URL_3": BASE_URL_3,
    }


def get_base_domains() -> list[str]:
    """Extracts hostnames/domains from the three base URLs."""
    domains = []
    for u in (BASE_URL_1, BASE_URL_2, BASE_URL_3):
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
