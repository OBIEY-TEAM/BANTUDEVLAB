"""
Sovereign Security Engine for BANTUDEVLAB.
Performs:
1. Hardcoded Secret & Key Detection (AWS, GitHub tokens, Private keys, JWTs).
2. Code Vulnerability Analysis (SQL Injection, Command Injection, Insecure Deserialization, eval/exec).
3. Digital Sovereignty Compliance (Flags foreign data leakage, untrusted third-party telemetry, unencrypted cloud calls).
4. Calculation of Continental Sovereignty Score (0 - 100).
"""

import re
from typing import Any, Dict, List


class SecurityScannerEngine:
    SECRET_PATTERNS = [
        (
            re.compile(
                r'(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?key)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{16,})["\']'
            ),
            "Secret/API Key hardcodée",
        ),
        (re.compile(r"ghp_[a-zA-Z0-9]{36}"), "Gitea/GitHub Personal Access Token exposé"),
        (re.compile(r"-----BEGIN\s+(RSA|OPENSSH|EC|DSA)?\s*PRIVATE KEY-----"), "Clé privée RSA/SSH exposée en clair"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "Identifiant AWS IAM exposé"),
        (re.compile(r"eyJ[a-zA-Z0-9-_]+\.eyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"), "Token JWT en dur"),
    ]

    VULNERABILITY_PATTERNS = [
        (
            re.compile(r'(?i)(execute|cursor\.execute)\s*\(\s*["\'].*?%s.*?\+'),
            "Injection SQL potentielle (concaténation de requête)",
        ),
        (
            re.compile(r'(?i)(os\.system|subprocess\.Popen|subprocess\.call)\s*\(\s*f?["\'].*?\{.*?\}'),
            "Injection de commande OS potentielle",
        ),
        (re.compile(r"(?i)\beval\s*\("), "Utilisation dangereuse de eval()"),
        (re.compile(r"(?i)\bexec\s*\("), "Utilisation dangereuse de exec()"),
        (re.compile(r"(?i)\bpickle\.loads?\s*\("), "Désérialisation non sécurisée avec pickle"),
    ]

    SOVEREIGNTY_RISK_PATTERNS = [
        (
            re.compile(r"(?i)https?://[a-zA-Z0-9.-]*\.(telemetry|analytics|tracking)\.[a-z]+"),
            "Fuite de métadonnées vers des services de télémétrie tiers étrangers",
        ),
        (re.compile(r"(?i)https?://[a-zA-Z0-9.-]*amazonaws\.com"), "Dépendance non souveraine détectée (AWS US/EU)"),
        (
            re.compile(r"(?i)https?://[a-zA-Z0-9.-]*googleapis\.com"),
            "Dépendance externe étrangère détectée (Google API)",
        ),
    ]

    @classmethod
    def scan_code(cls, filename: str, content: str) -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        lines = content.splitlines()

        # 1. Detect hardcoded secrets
        for line_no, line in enumerate(lines, start=1):
            for pattern, desc in cls.SECRET_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        {
                            "file": filename,
                            "line": line_no,
                            "type": "SECRET_LEAK",
                            "severity": "CRITICAL",
                            "description": desc,
                            "snippet": line.strip()[:100],
                            "recommendation": "Utiliser le gestionnaire de secrets sécurisé BantuDevLab Vault.",
                        }
                    )

        # 2. Detect code vulnerabilities
        for line_no, line in enumerate(lines, start=1):
            for pattern, desc in cls.VULNERABILITY_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        {
                            "file": filename,
                            "line": line_no,
                            "type": "VULNERABILITY",
                            "severity": "HIGH",
                            "description": desc,
                            "snippet": line.strip()[:100],
                            "recommendation": "Remplacer par des requêtes paramétrées ou une alternative sécurisée.",
                        }
                    )

        # 3. Detect sovereignty risks
        for line_no, line in enumerate(lines, start=1):
            for pattern, desc in cls.SOVEREIGNTY_RISK_PATTERNS:
                if pattern.search(line):
                    issues.append(
                        {
                            "file": filename,
                            "line": line_no,
                            "type": "SOVEREIGNTY_RISK",
                            "severity": "MEDIUM",
                            "description": desc,
                            "snippet": line.strip()[:100],
                            "recommendation": "Migrer les endpoints vers Systalink Cloud ou l'infrastructure souveraine panafricaine.",
                        }
                    )

        # Calculate Sovereignty and Security Score
        critical_count = sum(1 for i in issues if i["severity"] == "CRITICAL")
        high_count = sum(1 for i in issues if i["severity"] == "HIGH")
        medium_count = sum(1 for i in issues if i["severity"] == "MEDIUM")

        deductions = (critical_count * 25) + (high_count * 15) + (medium_count * 5)
        score = max(0, 100 - deductions)

        status_rating = "EXCELLENT"
        if score < 50:
            status_rating = "CRITICAL_RISK"
        elif score < 75:
            status_rating = "WARNING"
        elif score < 90:
            status_rating = "GOOD"

        return {
            "file": filename,
            "total_issues": len(issues),
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "sovereignty_score": score,
            "status_rating": status_rating,
            "issues": issues,
            "jurisdiction": "African Digital Sovereignty Standards (ADSS-v1)",
        }


# Alias de compatibilité souveraine
SovereignSecurityScanner = SecurityScannerEngine
