"""
SARIF 2.1.0 Serializer for BantuDevLab Security Scanner (DEV-05).
Transforms raw audit findings into the OASIS Static Analysis Results Interchange Format (SARIF) v2.1.0 standard,
enabling native Gitea and CI/CD code scanning diff annotations.
"""

from typing import Any, Dict

from .models import SecurityAuditReport


class SarifReportSerializer:
    """Serializes security findings and audit reports to SARIF 2.1.0 standard."""

    SARIF_SCHEMA = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    SARIF_VERSION = "2.1.0"

    LEVEL_MAP = {
        "CRITICAL": "error",
        "HIGH": "error",
        "MEDIUM": "warning",
        "LOW": "note",
    }

    @classmethod
    def serialize(cls, report: SecurityAuditReport) -> Dict[str, Any]:
        """Converts a SecurityAuditReport instance into a standard SARIF JSON document."""
        rules = []
        rule_indices = {}
        results = []

        findings = report.raw_findings or []

        for finding in findings:
            rule_id = finding.get("type", "SOVEREIGN_SECURITY_RULE")
            desc = finding.get("description", "Alerte de sécurité souveraine")
            severity = finding.get("severity", "MEDIUM")
            level = cls.LEVEL_MAP.get(severity, "warning")
            filename = finding.get("file", report.file_scanned or "unknown.py")
            line = finding.get("line", 1)
            snippet = finding.get("snippet", "")
            recommendation = finding.get("recommendation", "")

            if rule_id not in rule_indices:
                rule_indices[rule_id] = len(rules)
                rules.append(
                    {
                        "id": rule_id,
                        "name": rule_id.replace("_", " ").title(),
                        "shortDescription": {"text": desc},
                        "fullDescription": {"text": f"{desc}. {recommendation}".strip()},
                        "defaultConfiguration": {"level": level},
                        "properties": {"tags": ["security", "sovereignty", "african-standards"], "precision": "high"},
                    }
                )

            rule_index = rule_indices[rule_id]

            result_entry = {
                "ruleId": rule_id,
                "ruleIndex": rule_index,
                "level": level,
                "message": {"text": f"{desc} : {snippet}" if snippet else desc},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": filename, "uriBaseId": "%SRCROOT%"},
                            "region": {"startLine": int(line), "startColumn": 1, "snippet": {"text": snippet}},
                        }
                    }
                ],
            }
            results.append(result_entry)

        sarif_payload = {
            "$schema": cls.SARIF_SCHEMA,
            "version": cls.SARIF_VERSION,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "BantuDevLab Sovereign Security Scanner",
                            "organization": "BantuDevLab African Sovereign Forge",
                            "semanticVersion": "1.0.0",
                            "rules": rules,
                        }
                    },
                    "results": results,
                    "properties": {
                        "repository": report.repository_name,
                        "sovereigntyScore": report.sovereignty_score,
                        "statusRating": report.status_rating,
                        "totalIssues": report.total_issues,
                        "criticalCount": report.critical_count,
                        "highCount": report.high_count,
                        "mediumCount": report.medium_count,
                        "scannedAt": report.scanned_at.isoformat() if report.scanned_at else None,
                    },
                }
            ],
        }

        return sarif_payload

    @classmethod
    def serialize_gitlab_sast(cls, report: SecurityAuditReport) -> Dict[str, Any]:
        """
        T-GIT-304: Exporte l'artefact au format gl-sast-report.json officiel
        pour ingestion directe dans le GitLab Security Dashboard.
        """
        vulnerabilities = []
        findings = report.raw_findings or []

        for idx, finding in enumerate(findings):
            rule_id = finding.get("type", "SOVEREIGN_VULN")
            desc = finding.get("description", "Alerte de sécurité souveraine")
            sev = finding.get("severity", "Medium").capitalize()
            filename = finding.get("file", report.file_scanned or "app.py")
            line = finding.get("line", 1)

            vulnerabilities.append(
                {
                    "id": f"bantu-sast-{report.id or 1}-{idx}",
                    "category": "sast",
                    "name": rule_id,
                    "message": desc,
                    "description": desc,
                    "severity": sev,
                    "confidence": "High",
                    "scanner": {"id": "bantudevlab_sast", "name": "BantuDevLab Sovereign SAST Scanner"},
                    "location": {
                        "file": filename,
                        "start_line": int(line),
                    },
                    "identifiers": [
                        {
                            "type": "bantudevlab_rule_type",
                            "name": rule_id,
                            "value": rule_id,
                        }
                    ],
                }
            )

        return {
            "version": "15.0.0",
            "vulnerabilities": vulnerabilities,
            "scan": {
                "scanner": {
                    "id": "bantudevlab_sast",
                    "name": "BantuDevLab Sovereign SAST Scanner",
                    "version": "1.0.0",
                    "vendor": {"name": "BantuDevLab Panafrican Forge"},
                },
                "type": "sast",
                "status": "success",
                "start_time": report.scanned_at.isoformat() if report.scanned_at else "2026-11-02T00:00:00Z",
                "end_time": report.scanned_at.isoformat() if report.scanned_at else "2026-11-02T00:00:01Z",
            },
        }
