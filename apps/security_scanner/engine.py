"""
Sovereign Security Engine for BANTUDEVLAB.
Performs:
1. Hardcoded Secret & Key Detection (AWS, GitHub tokens, Private keys, JWTs, Dockerfile ENV secrets).
2. Code Vulnerability Analysis (SQL Injection, Command Injection, Insecure Deserialization, eval/exec, DOM XSS, Dockerfile root/latest, YAML privileged).
3. Digital Sovereignty Compliance (Flags foreign data leakage, untrusted third-party telemetry, unencrypted cloud calls).
4. Shannon Entropy analysis for random / encrypted credentials (> 20 chars).
5. Formal Python AST parsing to detect dangerous dynamic execution (eval, exec, os.system) even with aliasing.
6. Multi-lingual output synchronization (fr, en, sw, pt) & Continental Sovereignty Score (0 - 100).
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
    I18N_MESSAGES = {
        "fr": {
            "secret_rec": "Utiliser le gestionnaire de secrets sécurisé BantuDevLab Vault.",
            "entropy_desc": "Token à haute entropie détecté (entropie: {entropy:.2f} bits)",
            "entropy_rec": "Extraire le token chiffré/aléatoire dans les variables d'environnement.",
            "vuln_rec": "Remplacer par des requêtes paramétrées ou une alternative sécurisée.",
            "ast_desc": "Appel dangereux à {func_name}() détecté via analyse syntaxique AST (T-SEC-502)",
            "ast_rec": "Remplacer par ast.literal_eval, une structure typée ou subprocess sans shell=True.",
            "sov_rec": "Migrer les endpoints vers une infrastructure auto-hébergée ou souveraine.",
            "jurisdiction": "African Digital Sovereignty Standards (ADSS-v1)",
        },
        "en": {
            "secret_rec": "Use the secure BantuDevLab Vault secret manager or encrypted environment variables.",
            "entropy_desc": "High-entropy secret token detected (entropy: {entropy:.2f} bits)",
            "entropy_rec": "Extract the encrypted/random token into sovereign environment variables.",
            "vuln_rec": "Replace with parameterized queries, rootless container rules, or a safe API.",
            "ast_desc": "Dangerous call to {func_name}() detected via AST static analysis (T-SEC-502)",
            "ast_rec": "Replace with ast.literal_eval, typed structures, or subprocess without shell=True.",
            "sov_rec": "Migrate endpoints to a self-hosted or sovereign infrastructure.",
            "jurisdiction": "African Digital Sovereignty Standards (ADSS-v1)",
        },
        "sw": {
            "secret_rec": "Tumia mfumo salama wa kuhifadhi siri wa BantuDevLab Vault.",
            "entropy_desc": "Tokeni ya siri yenye entropia ya juu imegunduliwa (entropia: {entropy:.2f} bits)",
            "entropy_rec": "Hamisha tokeni ya siri kwenye vigezo vya mazingira vilivyosimbwa.",
            "vuln_rec": "Badilisha kwa hoja salama za SQL, kontena isiyo ya root au mbadala salama.",
            "ast_desc": "Wito hatari kwa {func_name}() umegunduliwa kupitia uchambuzi wa AST (T-SEC-502)",
            "ast_rec": "Badilisha kwa ast.literal_eval au subprocess bila shell=True.",
            "sov_rec": "Hamisha miunganisho kwenda Systalink Cloud au miundombinu huru ya Afrika.",
            "jurisdiction": "Viwango vya Uhuru wa Kidijitali Afrika (ADSS-v1)",
        },
        "pt": {
            "secret_rec": "Utilize o gestor seguro de segredos BantuDevLab Vault.",
            "entropy_desc": "Token secreto de alta entropia detetado (entropia: {entropy:.2f} bits)",
            "entropy_rec": "Extraia o token aleatório/cifrado para variáveis de ambiente seguras.",
            "vuln_rec": "Substitua por consultas parametrizadas, contentores sem root ou alternativa segura.",
            "ast_desc": "Chamada perigosa a {func_name}() detetada via análise AST (T-SEC-502)",
            "ast_rec": "Substitua por ast.literal_eval ou subprocess sem shell=True.",
            "sov_rec": "Migre os endpoints para a Systalink Cloud ou infraestrutura soberana pan-africana.",
            "jurisdiction": "Normas Africanas de Soberania Digital (ADSS-v1)",
        },
    }

    RULE_TRANSLATIONS = {
        "Secret/API Key hardcodée": {
            "en": "Hardcoded Secret / API Key exposed",
            "sw": "Siri / Ufunguo wa API uliowekwa wazi kwenye msimbo",
            "pt": "Segredo / Chave de API codificada diretamente",
        },
        "Gitea/GitHub Personal Access Token exposé": {
            "en": "Exposed Gitea/GitHub Personal Access Token",
            "sw": "Tokeni ya ufikiaji binafsi ya Gitea/GitHub imewekwa wazi",
            "pt": "Token de acesso pessoal Gitea/GitHub exposto",
        },
        "Clé privée RSA/SSH exposée en clair": {
            "en": "Plaintext RSA/SSH private key exposed",
            "sw": "Ufunguo wa siri wa RSA/SSH umewekwa wazi",
            "pt": "Chave privada RSA/SSH exposta em texto simples",
        },
        "Identifiant AWS IAM exposé": {
            "en": "Exposed AWS IAM Access Key ID",
            "sw": "Kitambulisho cha AWS IAM kimewekwa wazi",
            "pt": "Credencial AWS IAM exposta",
        },
        "Token JWT en dur": {
            "en": "Hardcoded JWT token",
            "sw": "Tokeni ya JWT iliyowekwa moja kwa moja",
            "pt": "Token JWT codificado diretamente",
        },
        "Secret exposé dans une directive ENV Dockerfile": {
            "en": "Secret exposed in Dockerfile ENV instruction",
            "sw": "Siri imewekwa wazi ndani ya ENV ya Dockerfile",
            "pt": "Segredo exposto numa instrução ENV do Dockerfile",
        },
        "Injection SQL potentielle (concaténation de requête)": {
            "en": "Potential SQL Injection (query string concatenation)",
            "sw": "Hatari ya SQL Injection (unganisho la hoja)",
            "pt": "Potencial Injeção SQL (concatenação de consulta)",
        },
        "Injection de commande OS potentielle": {
            "en": "Potential OS Command Injection",
            "sw": "Hatari ya uingizaji wa amri ya mfumo (OS Command Injection)",
            "pt": "Potencial Injeção de Comando de Sistema Operativo",
        },
        "Utilisation dangereuse de eval()": {
            "en": "Dangerous use of eval() dynamic execution",
            "sw": "Matumizi hatari ya eval()",
            "pt": "Utilização perigosa de eval()",
        },
        "Utilisation dangereuse de exec()": {
            "en": "Dangerous use of exec() dynamic execution",
            "sw": "Matumizi hatari ya exec()",
            "pt": "Utilização perigosa de exec()",
        },
        "Désérialisation non sécurisée avec pickle": {
            "en": "Insecure deserialization with pickle",
            "sw": "Uchakataji usio salama wa data kwa pickle",
            "pt": "Desserialização insegura com pickle",
        },
        "Faille XSS DOM potentielle via innerHTML / document.write (JavaScript)": {
            "en": "Potential DOM XSS vulnerability via innerHTML / document.write (JavaScript)",
            "sw": "Hatari ya DOM XSS kupitia innerHTML / document.write (JavaScript)",
            "pt": "Potencial vulnerabilidade DOM XSS via innerHTML / document.write (JavaScript)",
        },
        "Exécution de commande système risquée via child_process.exec (JavaScript)": {
            "en": "Risky shell command execution via child_process.exec (JavaScript)",
            "sw": "Utekelezaji hatari wa amri kupitia child_process.exec (JavaScript)",
            "pt": "Execução arriscada de comando via child_process.exec (JavaScript)",
        },
        "Image Docker non épinglée (:latest) ou exécution en root (Dockerfile)": {
            "en": "Unpinned Docker image (:latest) or root execution (Dockerfile)",
            "sw": "Picha ya Docker isiyofungwa (:latest) au utekelezaji kama root (Dockerfile)",
            "pt": "Imagem Docker sem versão fixa (:latest) ou execução como root (Dockerfile)",
        },
        "Exécution distante curl/wget pipée vers shell ou permissions 777 (Dockerfile)": {
            "en": "Remote script piped to shell (curl | sh) or insecure chmod 777 (Dockerfile)",
            "sw": "Hati ya mbali iliyounganishwa kwa shell (curl | sh) au chmod 777 (Dockerfile)",
            "pt": "Script remoto redirecionado para shell (curl | sh) ou chmod 777 inseguro (Dockerfile)",
        },
        "Conteneur privilégié ou désactivation des contrôles de sécurité (YAML/CI)": {
            "en": "Privileged container mode or security check bypass (YAML/CI)",
            "sw": "Kontena yenye mamlaka kamili (privileged) au kuruka ukaguzi wa usalama (YAML/CI)",
            "pt": "Contentor privilegiado ou desativação de controlo de segurança (YAML/CI)",
        },
        "Fuite de métadonnées vers des services de télémétrie tiers étrangers": {
            "en": "Metadata leakage to foreign third-party telemetry services",
            "sw": "Uvujaji wa metadata kwenda huduma za nje za ufuatiliaji (telemetry)",
            "pt": "Fuga de metadados para serviços externos de telemetria",
        },
        "Dépendance non souveraine détectée (AWS US/EU)": {
            "en": "Non-sovereign cloud dependency detected (AWS US/EU)",
            "sw": "Utegemezi wa wingu usio huru umegunduliwa (AWS US/EU)",
            "pt": "Dependência cloud não soberana detetada (AWS US/EU)",
        },
        "Dépendance externe étrangère détectée (Google API)": {
            "en": "Foreign external API dependency detected (Google API)",
            "sw": "Utegemezi wa API ya nje umegunduliwa (Google API)",
            "pt": "Dependência externa estrangeira detetada (Google API)",
        },
    }

    SECRET_PATTERNS = [
        (
            re.compile(
                r'(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?key|auth[_-]?token)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{12,})["\']'
            ),
            "Secret/API Key hardcodée",
        ),
        (re.compile(r"ghp_[a-zA-Z0-9_]{20,}"), "Gitea/GitHub Personal Access Token exposé"),
        (re.compile(r"-----BEGIN\s+(RSA|OPENSSH|EC|DSA)?\s*PRIVATE KEY-----"), "Clé privée RSA/SSH exposée en clair"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "Identifiant AWS IAM exposé"),
        (re.compile(r"eyJ[a-zA-Z0-9-_]+\.eyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"), "Token JWT en dur"),
        (
            re.compile(r'(?i)^\s*ENV\s+\w*(SECRET|PASSWORD|TOKEN|KEY)\w*\s*[:=]?\s*["\']?[^\s"\']{8,}'),
            "Secret exposé dans une directive ENV Dockerfile",
        ),
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
        (
            re.compile(r"(?i)(\.innerHTML\s*=|document\.write\s*\()"),
            "Faille XSS DOM potentielle via innerHTML / document.write (JavaScript)",
        ),
        (
            re.compile(r"(?i)(child_process\.exec|execSync)\s*\("),
            "Exécution de commande système risquée via child_process.exec (JavaScript)",
        ),
        (
            re.compile(r"(?i)^\s*(FROM\s+\S+:latest|USER\s+root)\b"),
            "Image Docker non épinglée (:latest) ou exécution en root (Dockerfile)",
        ),
        (
            re.compile(r"(?i)(curl\s+[^|\n]+\|\s*(ba)?sh|chmod\s+(-R\s+)?777\b)"),
            "Exécution distante curl/wget pipée vers shell ou permissions 777 (Dockerfile)",
        ),
        (
            re.compile(r'(?i)^\s*(privileged\s*:\s*true|allow_failure\s*:\s*true|network_mode\s*:\s*["\']?host)'),
            "Conteneur privilégié ou désactivation des contrôles de sécurité (YAML/CI)",
        ),
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
    def _translate_rule(cls, fr_desc: str, lang: str) -> str:
        if lang == "fr" or lang not in ("en", "sw", "pt"):
            return fr_desc
        return cls.RULE_TRANSLATIONS.get(fr_desc, {}).get(lang, fr_desc)

    @classmethod
    def scan_code(cls, filename: str, content: str, lang: str = "fr") -> Dict[str, Any]:
        lang_code = (lang or "fr").lower()[:2]
        if lang_code not in cls.I18N_MESSAGES:
            lang_code = "fr"
        msg = cls.I18N_MESSAGES[lang_code]

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
                            "description": cls._translate_rule(desc, lang_code),
                            "snippet": line.strip()[:100],
                            "recommendation": msg["secret_rec"],
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
                            "description": msg["entropy_desc"].format(entropy=entropy),
                            "snippet": line.strip()[:100],
                            "recommendation": msg["entropy_rec"],
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
                            "description": cls._translate_rule(desc, lang_code),
                            "snippet": line.strip()[:100],
                            "recommendation": msg["vuln_rec"],
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
                    if lang_code != "fr":
                        fn = ast_issue.get("snippet", "").split(":")[-1].strip() or "eval/exec"
                        ast_issue["description"] = msg["ast_desc"].format(func_name=fn)
                        ast_issue["recommendation"] = msg["ast_rec"]
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
                            "description": cls._translate_rule(desc, lang_code),
                            "snippet": line.strip()[:100],
                            "recommendation": msg["sov_rec"],
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
            "lang": lang_code,
            "jurisdiction": msg["jurisdiction"],
        }


# Alias de compatibilité souveraine
SovereignSecurityScanner = SecurityScannerEngine
