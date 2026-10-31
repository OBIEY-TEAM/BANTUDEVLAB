"""
Dataset preparation pipeline for fine-tuning Gemma 5B on African Sovereign Software Engineering tasks.
Generates instruction-tuning datasets covering:
1. Zero-Knowledge Proof protocol implementations.
2. Hardcoded secret remediation and secure coding for African FinTechs (USSD, Mobile Money, Interswitch).
3. Decentralized Git workflows and sovereign cloud architectures.
"""

import json
import os
from typing import Dict, List

RAW_DATASET_EXAMPLES: List[Dict[str, str]] = [
    {
        "instruction": "Écris une fonction Python pour vérifier une preuve Zero-Knowledge Schnorr sans exposer le secret.",
        "input": "Paramètres publics p, g, clé publique y, engagement t, réponse s, message m",
        "output": (
            "import hashlib\n\n"
            "def verify_schnorr(p: int, g: int, y: int, t: int, s: int, message: str) -> bool:\n"
            "    # Calcul du défi Fiat-Shamir c = H(g || y || t || m)\n"
            "    data = f'{g}:{y}:{t}:{message}'.encode('utf-8')\n"
            "    c = int(hashlib.sha256(data).hexdigest(), 16)\n"
            "    # Vérification: (g^s * y^c) mod p == t\n"
            "    return (pow(g, s, p) * pow(y, c, p)) % p == t\n"
        ),
    },
    {
        "instruction": "Audite cette fonction de paiement Mobile Money et élimine le risque d'injection SQL.",
        "input": "cursor.execute('SELECT balance FROM accounts WHERE user_id = ' + request.POST['user_id'])",
        "output": (
            "### Analyse de sécurité BantuDevLab\n"
            "La concaténation de variables utilisateurs dans une requête SQL permet une injection SQL critique pouvant exposer l'ensemble des soldes financiers.\n\n"
            "### Correction sécurisée :\n"
            "cursor.execute('SELECT balance FROM accounts WHERE user_id = %s', (request.POST['user_id'],))\n"
        ),
    },
    {
        "instruction": "Comment configurer un webhook Gitea sécurisé pour déclencher l'analyse de souveraineté numérique ?",
        "input": "Configuration endpoint /api/forge/webhook/ avec secret partagé HMAC SHA-256",
        "output": (
            "Pour garantir l'intégrité des webhooks Gitea sur BantuDevLab :\n"
            "1. Définissez un secret HMAC fort dans les paramètres du webhook Gitea.\n"
            "2. Dans la vue Django, interceptez l'en-tête 'X-Gitea-Signature'.\n"
            "3. Calculez hmac.new(SECRET, request.body, hashlib.sha256).hexdigest() et comparez avec hmac.compare_digest().\n"
            "4. En cas de succès, déclenchez l'analyseur SecurityScannerEngine."
        ),
    },
    {
        "instruction": "Fournis une politique de souveraineté des données pour une fintech panafricaine conforme à l'Union Africaine.",
        "input": "Politique de stockage des clés de chiffrement et métadonnées",
        "output": (
            "1. Hébergement strict : Toutes les bases de données financières doivent résider dans des datacenters certifiés Tier-3 en Afrique (ex: Côte d'Ivoire, Sénégal, Kenya, Rwanda).\n"
            "2. Zero-Trust ZKP : Les identités des développeurs et administrateurs sont validées via ZKP sans transmission de hash réversible.\n"
            "3. Chiffrement post-quantique et HSM souverain pour toutes les clés privées."
        ),
    },
]


def generate_training_data(output_path: str = "finetuning/sovereign_instruct_dataset.jsonl") -> int:
    """Generates JSONL formatted training dataset for Gemma 5B fine-tuning."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in RAW_DATASET_EXAMPLES:
            formatted_item = {
                "text": (
                    f"<bos><start_of_turn>user\n"
                    f"{ex['instruction']}\n"
                    f"Contexte / Entrée : {ex['input']}<end_of_turn>\n"
                    f"<start_of_turn>model\n"
                    f"{ex['output']}<end_of_turn><eos>"
                )
            }
            f.write(json.dumps(formatted_item, ensure_ascii=False) + "\n")
            count += 1
    return count


if __name__ == "__main__":
    count = generate_training_data()
    print(f"Jeu de données de fine-tuning généré avec succès : {count} exemples.")
