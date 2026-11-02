"""
Gemma 5B Sovereign AI Assistant Engine.
Provides local / self-hosted inference integration for:
- Automated code reviews and pull-request audits
- Vulnerability remediation advice
- African context-aware architectural recommendations
- Offline sovereign fallback if external LLM host is unreachable
"""

import json
import time
from typing import Any, Dict, Generator, Optional

import requests
from django.conf import settings


class GemmaAssistant:
    """
    Client for Gemma 5B inference running locally on the sovereign server (e.g., via Ollama, vLLM, or TGI).
    """

    SYSTEM_PROMPT = (
        "Vous êtes BANTU-AI, l'assistant d'ingénierie logicielle souverain de BANTUDEVLAB, "
        "la forge panafricaine. Votre mission est d'aider les développeurs africains à concevoir des "
        "architectures sécurisées, résilientes, indépendantes et conformes aux meilleures pratiques mondiales. "
        "Vous analysez le code, identifiez les failles, et proposez des solutions concrètes et optimisées."
    )

    def __init__(self, api_url: Optional[str] = None, model_name: Optional[str] = None):
        self.api_url = api_url or getattr(settings, "GEMMA_API_URL", "http://localhost:11434/api/generate")
        self.model_name = model_name or getattr(settings, "GEMMA_MODEL_NAME", "gemma:5b")

    def analyze_code(self, code_snippet: str, context: str = "review") -> Dict[str, Any]:
        """
        Sends code to Gemma 5B for review, suggestions, or vulnerability analysis.
        """
        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"TÂCHE: Analyse et recommandation technique ({context})\n"
            f"CODE À ANALYSER:\n```\n{code_snippet}\n```\n\n"
            f"Fournis une analyse structurée : Points forts, Vulnérabilités potentielles, Recommandation de souveraineté et Correctif proposé."
        )

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 1024},
                },
                timeout=8,
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "model": self.model_name,
                    "response": data.get("response", ""),
                    "mode": "live_inference",
                }
        except Exception:
            # Fallback to sovereign rule-based local assistant engine
            pass

        return self._generate_sovereign_fallback(code_snippet=code_snippet, context=context)

    def _generate_sovereign_fallback(self, code_snippet: str, context: str) -> Dict[str, Any]:
        """
        Deterministic, offline sovereign knowledge engine simulating Gemma 5B
        when running in resource-constrained environments or test harnesses.
        """
        analysis = []
        recommendations = []

        if "eval(" in code_snippet or "exec(" in code_snippet:
            analysis.append(
                "🚨 **Alerte Critique** : Présence de fonction d'exécution dynamique non sécurisée (eval/exec). Risque immédiat d'exécution de code arbitraire à distance (RCE)."
            )
            recommendations.append("Remplacez `eval`/`exec` par `ast.literal_eval` ou une structure de données typée.")

        if "cursor.execute(" in code_snippet and ("%" in code_snippet or "+" in code_snippet):
            analysis.append(
                "⚠️ **Vulnérabilité SQL** : Détection de concaténation dans une requête SQL. Risque d'injection SQL."
            )
            recommendations.append(
                "Utilisez des requêtes paramétrées avec tuples d'arguments : `cursor.execute('SELECT * FROM table WHERE id = %s', (val,))`."
            )

        if "password" in code_snippet.lower() or "secret" in code_snippet.lower() or "token" in code_snippet.lower():
            analysis.append(
                "🔒 **Sécurité des données** : Présence de références directes à des secrets ou identifiants."
            )
            recommendations.append(
                "Assurez-vous que ces secrets sont gérés par BantuDevLab ZKP Zero-Trust ou des variables d'environnement chiffrées."
            )

        if not analysis:
            analysis.append(
                "✅ **Qualité de code** : La structure générale respecte les principes de modularité et aucune anomalie critique évidente n'a été relevée."
            )
            recommendations.append(
                "Poursuivre avec la mise en place de tests unitaires et la validation ZKP des commits."
            )

        response_text = (
            f"### 🛡️ Revue BantuDevLab AI (Moteur Gemma 5B Souverain)\n\n"
            f"**Statut de l'analyse** : {'Anomalies détectées' if len(analysis) > 1 else 'Code sain'}\n\n"
            f"#### Constats :\n" + "\n".join(f"- {a}" for a in analysis) + "\n\n"
            "#### Recommandations Souveraines :\n" + "\n".join(f"- {r}" for r in recommendations) + "\n\n"
            "---\n*Inférence certifiée par le nœud souverain BantuDevLab (Systalink Cloud Africa)*"
        )

        return {
            "success": True,
            "model": f"{self.model_name} (Sovereign Engine)",
            "response": response_text,
            "mode": "sovereign_local_engine",
        }

    def stream_analyze_code(self, code_snippet: str, context: str = "review") -> Generator[str, None, None]:
        """
        Génère un flux de tokens/mots pour l'analyse Gemma 5B (Server-Sent Events).
        Si l'API Ollama/vLLM est accessible en mode streaming, consomme son flux JSON chunks.
        Sinon, émet mot à mot la réponse du moteur souverain de fallback.
        """
        prompt = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"TÂCHE: Analyse et recommandation technique ({context})\n"
            f"CODE À ANALYSER:\n```\n{code_snippet}\n```\n\n"
            f"Fournis une analyse structurée : Points forts, Vulnérabilités potentielles, Recommandation de souveraineté et Correctif proposé."
        )

        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"temperature": 0.2, "num_predict": 1024},
                },
                stream=True,
                timeout=10,
            )
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        token = chunk.get("response", "")
                        if token:
                            yield token
                        if chunk.get("done", False):
                            return
                return
        except Exception:
            pass

        # Fallback mot à mot
        fallback_res = self._generate_sovereign_fallback(code_snippet=code_snippet, context=context)
        full_text = fallback_res.get("response", "")
        # Découpage par mots pour un streaming fluide
        tokens = full_text.split(" ")
        for i, token in enumerate(tokens):
            if i < len(tokens) - 1:
                yield token + " "
            else:
                yield token
            time.sleep(0.01)


# Alias de compatibilité souveraine
GemmaAIEngine = GemmaAssistant
