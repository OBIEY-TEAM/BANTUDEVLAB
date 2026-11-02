"""
Sovereign Security Engine for BANTUDEVLAB.
Performs:
1. Hardcoded Secret & Key Detection (AWS, GitHub tokens, Private keys, JWTs).
2. Code Vulnerability Analysis (SQL Injection, Command Injection, Insecure Deserialization, eval/exec).
3. Digital Sovereignty Compliance (Flags foreign data leakage, untrusted third-party telemetry, unencrypted cloud calls).
4. Shannon Entropy analysis for random / encrypted credentials (> 20 chars).
5. Formal Python AST parsing to detect dangerous dynamic execution (eval, exec, os.system) even with aliasing.
6. Calculation of Continental Sovereignty Score (0 - 100).
"""

import ast
import math
import re
from collections import Counter
from typing import Any, Dict, List


def calculate_shannon_entropy(data: str) -> float:
    """
    T-SEC-502 : Calcule l'entropie de Shannon en bits par caractère.
    Une chaîne aléatoire ou chiffrée (token, secret, clé privée) présente une haute entropie (> 4.2).
    """
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


class PythonASTSecurityVisitor(ast.NodeVisitor):
    """
    T-SEC-502 : Analyseur syntaxique abstrait (AST) pour détecter les appels à eval(),
    exec() et os.system() même en cas de renommage d'alias ou d'assignation indirecte.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[Dict[str, Any]] = []
        self.aliases: Dict[str, str] = {}

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == "os" and alias.asname:
                self.aliases[alias.asname] = "os"
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module == "os":
            for alias in node.names:
                if alias.name == "system":
                    target_name = alias.asname or alias.name
                    self.aliases[target_name] = "os.system"
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Name):
            source_id = node.value.id
            resolved = self.aliases.get(source_id, source_id)
            if resolved in ("eval", "exec", "os.system"):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.aliases[target.id] = resolved
        elif isinstance(node.value, ast.Attribute):
            if isinstance(node.value.value, ast.Name):
                base = node.value.value.id
                resolved_base = self.aliases.get(base, base)
                if resolved_base == "os" and node.value.attr == "system":
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.aliases[target.id] = "os.system"
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = None
        if isinstance(node.func, ast.Name):
            resolved = self.aliases.get(node.func.id, node.func.id)
            if resolved in ("eval", "exec", "os.system"):
                func_name = resolved
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                base = self.aliases.get(node.func.value.id, node.func.value.id)
                if base == "os" and node.func.attr == "system":
                    func_name = "os.system"

        if func_name:
            desc = f"Appel dangereux à {func_name}() détecté via analyse syntaxique AST (T-SEC-502)"
            self.issues.append(
                {
                    "file": self.filename,
                    "line": getattr(node, "lineno", 1),
                    "type": "VULNERABILITY",
                    "severity": "HIGH",
                    "description": desc,
                    "snippet": f"Appel de fonction critique : {func_name}",
                    "recommendation": "Remplacer par ast.literal_eval, une structure typée ou subprocess sans shell=True.",
                }
            )
        self.generic_visit(node)


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

    QUOTED_TOKEN_RE = re.compile(r'["\']([A-Za-z0-9+/=_\-]{21,})["\']')

    @classmethod
    def scan_code(cls, filename: str, content: str) -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        lines = content.splitlines()

        # 1. Detect hardcoded secrets via Regex
        secret_lines = set()
        for line_no, line in enumerate(lines, start=1):
            for pattern, desc in cls.SECRET_PATTERNS:
                if pattern.search(line):
                    secret_lines.add(line_no)
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

        # 2. T-SEC-502 : Shannon Entropy calculation on strings > 20 chars
        for line_no, line in enumerate(lines, start=1):
            if line_no in secret_lines:
                continue
            for match in cls.QUOTED_TOKEN_RE.finditer(line):
                token = match.group(1)
                # Ignore common long URLs or plain text words
                if token.startswith("http://") or token.startswith("https://"):
                    continue
                entropy = calculate_shannon_entropy(token)
                if entropy >= 4.3:
                    secret_lines.add(line_no)
                    issues.append(
                        {
                            "file": filename,
                            "line": line_no,
                            "type": "SECRET_LEAK",
                            "severity": "CRITICAL",
                            "description": f"Token à haute entropie détecté (entropie: {entropy:.2f} bits)",
                            "snippet": line.strip()[:100],
                            "recommendation": "Extraire le token chiffré/aléatoire dans les variables d'environnement.",
                        }
                    )
                    break

        # 3. Detect code vulnerabilities via Regex
        vuln_lines = set()
        for line_no, line in enumerate(lines, start=1):
            for pattern, desc in cls.VULNERABILITY_PATTERNS:
                if pattern.search(line):
                    vuln_lines.add(line_no)
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

        # 4. T-SEC-502 : AST visitor for formal python parsing (aliases and calls)
        try:
            tree = ast.parse(content, filename=filename)
            visitor = PythonASTSecurityVisitor(filename=filename)
            visitor.visit(tree)
            for ast_issue in visitor.issues:
                # Add if not already reported by regex on the same line
                if ast_issue["line"] not in vuln_lines:
                    issues.append(ast_issue)
                    vuln_lines.add(ast_issue["line"])
        except Exception:
            # Fallback silencieux si le fichier n'est pas du code Python valide
            pass

        # 5. Detect sovereignty risks
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
