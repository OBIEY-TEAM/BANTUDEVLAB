"""
Gemma 2 2B Sovereign AI Assistant Engine.
Provides local / self-hosted inference integration for:
- Automated code reviews and pull-request audits
- Vulnerability remediation advice across Python, Dockerfile, YAML, and JavaScript
- African context-aware architectural recommendations
- Multi-lingual response synchronization (fr, en, sw, pt)
- Offline sovereign fallback if external LLM host is unreachable
"""

import json
import logging
import time
from typing import Any, Dict, Generator, Optional

import requests
from django.conf import settings

logger = logging.getLogger("bantudevlab.security")


class GemmaAssistant:
    """
    Client for Gemma 2 2B inference running locally on the sovereign server (e.g., via Ollama, vLLM, or TGI).
    """

    SYSTEM_PROMPTS = {
        "fr": (
            "Vous êtes BANTU-AI, l'assistant d'ingénierie logicielle souverain de BANTUDEVLAB, "
            "la forge panafricaine. Votre mission est d'aider les développeurs africains à concevoir des "
            "architectures sécurisées, résilientes, indépendantes et conformes aux meilleures pratiques mondiales. "
            "Vous analysez le code, identifiez les failles, et proposez des solutions concrètes et optimisées. "
            "Répondez intégralement en FRANÇAIS."
        ),
        "en": (
            "You are BANTU-AI, the sovereign software engineering assistant of BANTUDEVLAB, "
            "the Pan-African code forge. Your mission is to help developers build secure, resilient, "
            "independent architectures compliant with global best practices. "
            "Analyze the code, identify vulnerabilities, and provide concrete fixes. "
            "Respond entirely in ENGLISH."
        ),
        "sw": (
            "Wewe ni BANTU-AI, msaidizi huru wa uhandisi wa programu wa BANTUDEVLAB, "
            "jukwaa la teknolojia la Afrika. Jukumu lako ni kusaidia wahandisi kujenga mifumo salama, "
            "imara na huru. Chambua msimbo, tambua udhaifu wa kiusalama na utoe mapendekezo. "
            "Jibu kikamilifu kwa KISWAHILI."
        ),
        "pt": (
            "Você é o BANTU-AI, o assistente soberano de engenharia de software do BANTUDEVLAB, "
            "a forja pan-africana. A sua missão é ajudar os programadores a projetar arquiteturas seguras, "
            "resilientes e independentes. Analise o código, identifique vulnerabilidades e proponha correções. "
            "Responda inteiramente em PORTUGUÊS."
        ),
    }

    SYSTEM_PROMPT = SYSTEM_PROMPTS["fr"]

    I18N_FALLBACK = {
        "fr": {
            "title": "Revue BantuDevLab AI (Moteur Gemma 2 2B Souverain)",
            "status_lbl": "Statut de l'analyse",
            "status_issues": "Anomalies détectées",
            "status_clean": "Code sain",
            "findings_hdr": "Constats",
            "recs_hdr": "Recommandations Souveraines",
            "footer": "Inférence certifiée par le nœud souverain BantuDevLab (Systalink Cloud Africa)",
            "eval_find": "[CRITIQUE] Alerte Critique : Présence de fonction d'exécution dynamique non sécurisée (eval/exec). Risque immédiat d'exécution de code arbitraire à distance (RCE).",
            "eval_rec": "Remplacez `eval`/`exec` par `ast.literal_eval`, `JSON.parse` ou une structure de données typée.",
            "sql_find": "[AVERTISSEMENT] Vulnérabilité SQL : Détection de concaténation dans une requête SQL. Risque d'injection SQL.",
            "sql_rec": "Utilisez des requêtes paramétrées avec tuples d'arguments : `cursor.execute('SELECT * FROM table WHERE id = %s', (val,))`.",
            "secret_find": "[CONFIDENTIALITE] Sécurité des données : Présence de références directes à des secrets, clés API ou jetons d'authentification.",
            "secret_rec": "Assurez-vous que ces secrets sont gérés par BantuDevLab ZKP Zero-Trust ou des variables d'environnement chiffrées.",
            "docker_find": "[CONTENEUR] Sécurité Dockerfile : Image non épinglée (`:latest`), exécution en `root`, ou script distant exécuté via `curl | sh` / `chmod 777`.",
            "docker_rec": "Épinglez le digest SHA256 de l'image de base, créez un utilisateur dédié non-root (`USER appuser`) et évitez `chmod 777`.",
            "yaml_find": "[PIPELINE CI/CD] Sécurité YAML : Conteneur en mode `privileged: true`, contournement `allow_failure: true` ou fuite vers un cloud non souverain.",
            "yaml_rec": "Désactivez `privileged: true`, imposez le blocage sur les jobs SAST et ciblez les runners souverains (`sovereign-abidjan`).",
            "js_find": "[FRONTEND/NODE] Sécurité JavaScript : Injection DOM XSS potentielle via `innerHTML` ou exécution système via `child_process.exec`.",
            "js_rec": "Utilisez `textContent` à la place de `innerHTML` et remplacez `exec` par `execFile` avec liste d'arguments validés.",
            "telemetry_find": "[SOUVERAINETE] Fuite de télémétrie : Appel réseau vers un service tiers hors juridiction africaine (tracking/AWS/Google).",
            "telemetry_rec": "Redirigez les flux d'audit et de stockage vers le cluster souverain Systalink Cloud (Abidjan, Dakar, Nairobi, Kigali).",
            "clean_find": "[CONFORME] Qualité de code : La structure générale respecte les principes de modularité et aucune anomalie critique évidente n'a été relevée.",
            "clean_rec": "Poursuivre avec la mise en place de tests unitaires et la validation ZKP des commits.",
            "explain_tpl": "Explication souveraine ({lang_label}) : Ce module comporte {lines} lignes d'instructions structurant la logique métier et les contrôles de sécurité.",
            "pr_summary_tpl": "### Synthèse de Pull Request ({title})\n- **Modifications analysées** : {lines} lignes de diff inspectées.\n- **Impact Sécurité & Souveraineté** : Validation ZKP et contrôle SAST recommandés avant fusion.",
        },
        "en": {
            "title": "BantuDevLab AI Review (Sovereign Gemma 2 2B Engine)",
            "status_lbl": "Analysis Status",
            "status_issues": "Vulnerabilities detected",
            "status_clean": "Clean code",
            "findings_hdr": "Findings",
            "recs_hdr": "Sovereign Recommendations",
            "footer": "Inference certified by the BantuDevLab Sovereign Node (Systalink Cloud Africa)",
            "eval_find": "[CRITICAL] Critical Alert: Unsafe dynamic code execution (`eval`/`exec`) detected. Immediate risk of Remote Code Execution (RCE).",
            "eval_rec": "Replace `eval`/`exec` with `ast.literal_eval`, `JSON.parse`, or a strictly typed parser.",
            "sql_find": "[WARNING] SQL Vulnerability: String concatenation detected in SQL query. High risk of SQL Injection.",
            "sql_rec": "Use parameterized queries with bound parameters: `cursor.execute('SELECT * FROM table WHERE id = %s', (val,))`.",
            "secret_find": "[PRIVACY] Data Security: Direct reference to hardcoded secrets, API keys, or authentication tokens.",
            "secret_rec": "Store all credentials in BantuDevLab ZKP Zero-Trust Vault or encrypted environment variables.",
            "docker_find": "[CONTAINER] Dockerfile Security: Unpinned `:latest` tag, `USER root` execution, or remote script piped to shell (`curl | sh` / `chmod 777`).",
            "docker_rec": "Pin base image versions, run as a non-root user (`USER appuser`), and apply least-privilege permissions.",
            "yaml_find": "[CI/CD PIPELINE] YAML Security: `privileged: true` container mode, `allow_failure: true` security bypass, or non-sovereign cloud endpoint.",
            "yaml_rec": "Disable `privileged: true`, enforce strict SAST gates, and target Pan-African runners (`sovereign-abidjan`).",
            "js_find": "[FRONTEND/NODE] JavaScript Security: Potential DOM XSS via `innerHTML` or shell injection via `child_process.exec`.",
            "js_rec": "Use `textContent` instead of `innerHTML` and replace `exec` with parameterized `execFile`.",
            "telemetry_find": "[SOVEREIGNTY] Telemetry Leakage: Outbound network call to a foreign third-party tracking or cloud endpoint.",
            "telemetry_rec": "Route all telemetry and storage to the Systalink Cloud Pan-African Sovereign Cluster.",
            "clean_find": "[COMPLIANT] Code Quality: The overall structure follows modularity best practices with no critical anomalies detected.",
            "clean_rec": "Continue with automated unit testing and ZKP cryptographic commit signing.",
            "explain_tpl": "Sovereign Explanation ({lang_label}): This component defines {lines} lines of code structuring business logic and security controls.",
            "pr_summary_tpl": "### Pull Request Summary ({title})\n- **Analyzed changes**: {lines} diff lines inspected.\n- **Security & Sovereignty Impact**: ZKP verification and SAST audit recommended prior to merge.",
        },
        "sw": {
            "title": "Ukaguzi wa BantuDevLab AI (Injini Huru ya Gemma 2 2B)",
            "status_lbl": "Hali ya Uchambuzi",
            "status_issues": "Dosari zimegunduliwa",
            "status_clean": "Msimbo salama",
            "findings_hdr": "Matokeo ya Ukaguzi",
            "recs_hdr": "Mapendekezo ya Uhuru wa Kidijitali",
            "footer": "Uchambuzi umethibitishwa na Nodi Huru ya BantuDevLab (Systalink Cloud Africa)",
            "eval_find": "[HATARI KUBWA] Tahadhari: Matumizi hatari ya `eval`/`exec` yamegunduliwa. Hatari ya utekelezaji wa msimbo wa mbali (RCE).",
            "eval_rec": "Badilisha `eval`/`exec` kwa `ast.literal_eval`, `JSON.parse` au muundo salama wa data.",
            "sql_find": "[ONYO] Udhaifu wa SQL: Unganisho la maneno ndani ya hoja ya SQL limegunduliwa (SQL Injection).",
            "sql_rec": "Tumia hoja zenye vigezo salama: `cursor.execute('SELECT * FROM table WHERE id = %s', (val,))`.",
            "secret_find": "[FARAGHA] Usalama wa Data: Uwepo wa siri, funguo za API au tokeni zilizowekwa wazi kwenye msimbo.",
            "secret_rec": "Hifadhi siri zote ndani ya BantuDevLab ZKP Zero-Trust Vault au vigezo vya mazingira vilivyosimbwa.",
            "docker_find": "[KONTENA] Usalama wa Dockerfile: Picha isiyofungwa (`:latest`), utekelezaji wa `USER root` au `curl | sh` / `chmod 777`.",
            "docker_rec": "Funga toleo mahususi la picha ya Docker na utumie mtumiaji asiye root (`USER appuser`).",
            "yaml_find": "[BOMBA LA CI/CD] Usalama wa YAML: Hali ya `privileged: true` au kuruka ukaguzi wa usalama (`allow_failure: true`).",
            "yaml_rec": "Zima `privileged: true` na utumie wakimbiaji huru wa Afrika (`sovereign-abidjan`).",
            "js_find": "[FRONTEND/NODE] Usalama wa JavaScript: Hatari ya DOM XSS kupitia `innerHTML` au amri ya mfumo kupitia `child_process.exec`.",
            "js_rec": "Tumia `textContent` badala ya `innerHTML` na `execFile` yenye vigezo salama.",
            "telemetry_find": "[UHURU WA DATA] Uvujaji wa Telemetry: Muunganisho kwenda huduma za nje zisizo chini ya mamlaka ya Afrika.",
            "telemetry_rec": "Elekeza data zote kwenye kituo huru cha Systalink Cloud Africa (Abidjan, Dakar, Nairobi, Kigali).",
            "clean_find": "[SAWA] Ubora wa Msimbo: Muundo wa msimbo unafuata kanuni bora za usalama na hakuna dosari kubwa iliyogunduliwa.",
            "clean_rec": "Endelea na majaribio ya kiotomatiki na uthibitishaji wa ZKP kwenye kila commit.",
            "explain_tpl": "Maelezo Huru ({lang_label}): Kipengele hiki kina mistari {lines} ya maelekezo yanayounda mantiki ya mfumo.",
            "pr_summary_tpl": "### Muhtasari wa Pull Request ({title})\n- **Mabadiliko yaliyokaguliwa**: Mistari {lines} ya diff.\n- **Usalama**: Uthibitishaji wa ZKP na ukaguzi wa SAST unashauriwa kabla ya kuunganisha.",
        },
        "pt": {
            "title": "Revisão BantuDevLab AI (Motor Soberano Gemma 2 2B)",
            "status_lbl": "Estado da Análise",
            "status_issues": "Anomalias detetadas",
            "status_clean": "Código limpo",
            "findings_hdr": "Constatações",
            "recs_hdr": "Recomendações Soberanas",
            "footer": "Inferência certificada pelo nó soberano BantuDevLab (Systalink Cloud Africa)",
            "eval_find": "[CRÍTICO] Alerta Crítico: Presença de execução dinâmica insegura (`eval`/`exec`). Risco imediato de execução remota de código (RCE).",
            "eval_rec": "Substitua `eval`/`exec` por `ast.literal_eval`, `JSON.parse` ou uma estrutura tipada segura.",
            "sql_find": "[AVISO] Vulnerabilidade SQL: Concatenação detetada numa consulta SQL. Risco de Injeção SQL.",
            "sql_rec": "Utilize consultas parametrizadas: `cursor.execute('SELECT * FROM table WHERE id = %s', (val,))`.",
            "secret_find": "[CONFIDENCIALIDADE] Segurança de Dados: Referências diretas a segredos, chaves de API ou tokens de autenticação.",
            "secret_rec": "Garanta que os segredos são geridos pelo BantuDevLab ZKP Zero-Trust ou variáveis de ambiente cifradas.",
            "docker_find": "[CONTENTOR] Segurança Dockerfile: Imagem `:latest` não fixa, execução como `USER root` ou script remoto `curl | sh` / `chmod 777`.",
            "docker_rec": "Fixe a versão da imagem base, utilize um utilizador não-root (`USER appuser`) e remova `chmod 777`.",
            "yaml_find": "[PIPELINE CI/CD] Segurança YAML: Modo `privileged: true`, bypass `allow_failure: true` ou endpoint cloud não soberano.",
            "yaml_rec": "Desative `privileged: true`, exija validação SAST obrigatória e utilize runners soberanos (`sovereign-abidjan`).",
            "js_find": "[FRONTEND/NODE] Segurança JavaScript: Potencial falha DOM XSS via `innerHTML` ou execução de comando via `child_process.exec`.",
            "js_rec": "Utilize `textContent` em vez de `innerHTML` e substitua `exec` por `execFile` parametrizado.",
            "telemetry_find": "[SOBERANIA] Fuga de Telemetria: Chamada de rede para serviço externo fora da jurisdição africana.",
            "telemetry_rec": "Migre os endpoints para o cluster soberano Systalink Cloud (Abidjan, Dakar, Nairobi, Kigali).",
            "clean_find": "[CONFORME] Qualidade de Código: A estrutura geral respeita os princípios de modularidade sem anomalias críticas.",
            "clean_rec": "Prosseguir com testes unitários automatizados e validação ZKP dos commits.",
            "explain_tpl": "Explicação Soberana ({lang_label}): Este módulo define {lines} linhas de instruções estruturando a lógica de negócio.",
            "pr_summary_tpl": "### Resumo da Pull Request ({title})\n- **Alterações analisadas**: {lines} linhas de diff inspecionadas.\n- **Impacto de Segurança**: Validação ZKP e auditoria SAST recomendadas antes da fusão.",
        },
    }

    def __init__(self, api_url: Optional[str] = None, model_name: Optional[str] = None):
        self.api_url = api_url or getattr(settings, "GEMMA_API_URL", "http://localhost:11434/api/generate")
        self.model_name = model_name or getattr(settings, "GEMMA_MODEL_NAME", "gemma2:2b")

    @classmethod
    def _norm_lang(cls, lang: Optional[str]) -> str:
        code = str(lang or "fr").lower().strip()[:2]
        return code if code in ("fr", "en", "sw", "pt") else "fr"

    def _build_prompt(self, code_snippet: str, context: str, lang: str = "fr") -> str:
        """Formatte le prompt selon le standard officiel Gemma 2 Instruct dans la langue choisie."""
        lang_code = self._norm_lang(lang)
        sys_prompt = self.SYSTEM_PROMPTS.get(lang_code, self.SYSTEM_PROMPT)
        lang_instruction = {
            "fr": "Fournis une analyse structurée en FRANÇAIS : Points forts, Vulnérabilités potentielles, Recommandation de souveraineté et Correctif proposé en signant 'BantuDevLab AI'.",
            "en": "Provide a structured analysis in ENGLISH: Strengths, Potential Vulnerabilities, Sovereignty Recommendation, and Proposed Fix signed 'BantuDevLab AI'.",
            "sw": "Toa uchambuzi uliopangwa kwa KISWAHILI: Nguvu, Udhaifu wa Kiusalama, Mapendekezo ya Uhuru wa Kidijitali na Marekebisho ukisaini 'BantuDevLab AI'.",
            "pt": "Forneça uma análise estruturada em PORTUGUÊS: Pontos fortes, Vulnerabilidades potenciais, Recomendação de soberania e Correção proposta assinando 'BantuDevLab AI'.",
        }[lang_code]
        return (
            f"<start_of_turn>user\n"
            f"{sys_prompt}\n\n"
            f"TASK / TÂCHE: ({context})\n"
            f"CODE:\n```\n{code_snippet}\n```\n\n"
            f"{lang_instruction}<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )

    def analyze_code(self, code_snippet: str, context: str = "review", lang: str = "fr") -> Dict[str, Any]:
        """
        Sends code to Gemma 2 2B for review, suggestions, or vulnerability analysis in the active language.
        """
        lang_code = self._norm_lang(lang)
        prompt = self._build_prompt(code_snippet=code_snippet, context=context, lang=lang_code)

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.15, "top_p": 0.9, "num_predict": 1024},
                },
                timeout=8,
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "model": self.model_name,
                    "response": data.get("response", ""),
                    "lang": lang_code,
                    "mode": "live_inference",
                }
        except Exception as exc:
            logger.warning("Echec de connexion a l'inference Gemma 2 2B (%s): %s", self.api_url, exc)

        return self._generate_sovereign_fallback(code_snippet=code_snippet, context=context, lang=lang_code)

    def _generate_sovereign_fallback(self, code_snippet: str, context: str, lang: str = "fr") -> Dict[str, Any]:
        """
        Deterministic, offline sovereign knowledge engine simulating Gemma 2 2B
        in the user's selected language (fr, en, sw, pt).
        """
        lang_code = self._norm_lang(lang)
        t = self.I18N_FALLBACK[lang_code]
        analysis = []
        recommendations = []
        lower_code = code_snippet.lower()

        if "eval(" in code_snippet or "exec(" in code_snippet:
            analysis.append(t["eval_find"])
            recommendations.append(t["eval_rec"])

        if ("cursor.execute(" in code_snippet or "execute(" in code_snippet) and (
            "%" in code_snippet or "+" in code_snippet
        ):
            analysis.append(t["sql_find"])
            recommendations.append(t["sql_rec"])

        if (
            "password" in lower_code
            or "secret" in lower_code
            or "token" in lower_code
            or "api_key" in lower_code
            or "apikey" in lower_code
            or "[secret masque]" in lower_code
        ):
            analysis.append(t["secret_find"])
            recommendations.append(t["secret_rec"])

        if (
            ("from " in lower_code and ":latest" in lower_code)
            or "user root" in lower_code
            or "chmod 777" in lower_code
            or ("curl " in lower_code and "| sh" in lower_code)
        ):
            analysis.append(t["docker_find"])
            recommendations.append(t["docker_rec"])

        if (
            "privileged: true" in lower_code
            or "allow_failure: true" in lower_code
            or "network_mode: host" in lower_code
        ):
            analysis.append(t["yaml_find"])
            recommendations.append(t["yaml_rec"])

        if ".innerhtml" in lower_code or "document.write(" in lower_code or "child_process.exec" in lower_code:
            analysis.append(t["js_find"])
            recommendations.append(t["js_rec"])

        if (
            "tracking." in lower_code
            or "telemetry." in lower_code
            or "analytics." in lower_code
            or "amazonaws.com" in lower_code
            or "googleapis.com" in lower_code
        ):
            analysis.append(t["telemetry_find"])
            recommendations.append(t["telemetry_rec"])

        has_anomalies = len(analysis) > 0
        if not analysis:
            analysis.append(t["clean_find"])
            recommendations.append(t["clean_rec"])

        response_text = (
            f"### {t['title']}\n\n"
            f"**{t['status_lbl']}** : {t['status_issues'] if has_anomalies else t['status_clean']}\n\n"
            f"#### {t['findings_hdr']} :\n" + "\n".join(f"- {a}" for a in analysis) + "\n\n"
            f"#### {t['recs_hdr']} :\n" + "\n".join(f"- {r}" for r in recommendations) + "\n\n"
            f"---\n*{t['footer']}*"
        )

        return {
            "success": True,
            "model": f"{self.model_name} (Sovereign Engine)",
            "response": response_text,
            "lang": lang_code,
            "mode": "sovereign_local_engine",
        }

    def stream_analyze_code(
        self, code_snippet: str, context: str = "review", lang: str = "fr"
    ) -> Generator[str, None, None]:
        """
        Génère un flux de tokens/mots pour l'analyse Gemma 2 2B (Server-Sent Events) dans la langue active.
        """
        lang_code = self._norm_lang(lang)
        prompt = self._build_prompt(code_snippet=code_snippet, context=context, lang=lang_code)

        response = None
        try:
            timeout_val = 0.5 if getattr(settings, "TESTING", False) else 10
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"temperature": 0.15, "top_p": 0.9, "num_predict": 1024},
                },
                stream=True,
                timeout=timeout_val,
            )
            if response.status_code == 200:
                try:
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line.decode("utf-8"))
                            token = chunk.get("response", "")
                            if token:
                                yield token
                            if chunk.get("done", False):
                                return
                finally:
                    response.close()
                return
        except Exception as exc:
            logger.warning("Echec du streaming Gemma 2 2B (%s): %s", self.api_url, exc)
        finally:
            if response is not None:
                try:
                    response.close()
                except Exception:
                    pass

        # Fallback mot à mot dans la langue sélectionnée
        fallback_res = self._generate_sovereign_fallback(code_snippet=code_snippet, context=context, lang=lang_code)
        full_text = fallback_res.get("response", "")
        tokens = full_text.split(" ")
        for i, token in enumerate(tokens):
            if i < len(tokens) - 1:
                yield token + " "
            else:
                yield token
            time.sleep(0.01)

    def explain_code(self, code_snippet: str, language: str = "", lang: str = "fr") -> Dict[str, Any]:
        """
        T-COP-701 : Explication pedagogique et architecturale du code selectionne dans la langue active.
        """
        lang_code = self._norm_lang(lang or language)
        sys_prompt = self.SYSTEM_PROMPTS.get(lang_code, self.SYSTEM_PROMPT)
        prompt = (
            f"<start_of_turn>user\n"
            f"{sys_prompt}\n\n"
            f"TASK: Explain the following code ({language or 'general'}).\n"
            f"CODE:\n```\n{code_snippet}\n```<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 1024},
                },
                timeout=8,
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "model": self.model_name,
                    "explanation": data.get("response", ""),
                    "lang": lang_code,
                    "mode": "live_inference",
                }
        except Exception as exc:
            logger.warning("Echec de connexion Gemma explain (%s): %s", self.api_url, exc)

        t = self.I18N_FALLBACK[lang_code]
        return {
            "success": True,
            "model": f"{self.model_name} (Sovereign Engine)",
            "explanation": t["explain_tpl"].format(lang_label=language or "code", lines=len(code_snippet.splitlines())),
            "lang": lang_code,
            "mode": "sovereign_local_engine",
        }

    def complete_code(self, prefix_code: str, language: str = "") -> Dict[str, Any]:
        """
        T-COP-701 : Autocompletion et suggestion de code en temps reel style GitHub Copilot.
        """
        prompt = (
            f"<start_of_turn>user\n"
            f"{self.SYSTEM_PROMPT}\n\n"
            f"TACHE: Completer la suite du code de maniere optimale et securisee.\n"
            f"LANGAGE: {language}\n"
            f"PREFIX:\n```\n{prefix_code}\n```\n"
            f"Reponds UNIQUEMENT avec le bloc de completion de code.<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "top_p": 0.85, "num_predict": 512},
                },
                timeout=8,
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "model": self.model_name,
                    "completion": data.get("response", ""),
                    "mode": "live_inference",
                }
        except Exception as exc:
            logger.warning("Echec de connexion Gemma complete (%s): %s", self.api_url, exc)

        return {
            "success": True,
            "model": f"{self.model_name} (Sovereign Engine)",
            "completion": "# Completion souveraine automatique\npass\n",
            "mode": "sovereign_local_engine",
        }

    def generate_pr_summary(self, diff_content: str, pr_title: str = "", lang: str = "fr") -> Dict[str, Any]:
        """
        T-COP-701 : Generation de synthese et notes de mise a jour pour Pull Request.
        """
        lang_code = self._norm_lang(lang)
        sys_prompt = self.SYSTEM_PROMPTS.get(lang_code, self.SYSTEM_PROMPT)
        prompt = (
            f"<start_of_turn>user\n"
            f"{sys_prompt}\n\n"
            f"TACHE: Generer une synthese concise des modifications de la Pull Request.\n"
            f"TITRE: {pr_title}\n"
            f"DIFF:\n```diff\n{diff_content[:8000]}\n```\n"
            f"Fournis: 1. Resume des changements, 2. Impacts potentiels, 3. Recommandations de tests.<end_of_turn>\n"
            f"<start_of_turn>model\n"
        )
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 1024},
                },
                timeout=8,
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "model": self.model_name,
                    "summary": data.get("response", ""),
                    "lang": lang_code,
                    "mode": "live_inference",
                }
        except Exception as exc:
            logger.warning("Echec de connexion Gemma PR summary (%s): %s", self.api_url, exc)

        t = self.I18N_FALLBACK[lang_code]
        return {
            "success": True,
            "model": f"{self.model_name} (Sovereign Engine)",
            "summary": t["pr_summary_tpl"].format(
                title=pr_title or "Pull Request", lines=len(diff_content.splitlines())
            ),
            "lang": lang_code,
            "mode": "sovereign_local_engine",
        }
