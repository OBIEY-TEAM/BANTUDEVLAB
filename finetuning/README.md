# 🧠 Pipeline de Fine-Tuning Gemma 5B — BANTUDEVLAB

Ce dossier contient l'ensemble des outils nécessaires pour entraîner et adapter le modèle de fondation **Gemma 5B** aux spécificités de la forge logicielle souveraine panafricaine.

## 🎯 Objectifs du Fine-Tuning
1. **Sécurité & Zero-Trust** : Maîtrise des protocoles de Zero-Knowledge Proof (Schnorr, Fiat-Shamir) et détection des secrets hardcodés.
2. **Contextes Techniques Africains** : Optimisation pour les architectures bancaires Mobile Money, APIs télécoms USSD, et contraintes d'infrastructure locale.
3. **Souveraineté des Données** : Exécution 100% locale/sur serveur Systalink Cloud sans télémétrie externe ni dépendance étrangère.

---

## 📁 Architecture des Fichiers

| Fichier | Rôle |
|---|---|
| `dataset_preparation.py` | Génère et formate le dataset d'instructions souverain (`sovereign_instruct_dataset.jsonl`). |
| `train_lora.py` | Script d'entraînement avec quantification QLoRA 4-bit (BitsAndBytes + PEFT + TRL). |
| `evaluate.py` | Suite de tests et métriques d'évaluation de la qualité du modèle fine-tuné. |
| `requirements.txt` | Dépendances nécessaires pour les calculs GPU (PyTorch, Transformers, Accelerate). |

---

## 🚀 Guide d'Utilisation

### 1. Préparation de l'environnement GPU
```bash
pip install -r finetuning/requirements.txt
```

### 2. Génération du dataset d'entraînement
```bash
python finetuning/dataset_preparation.py
```

### 3. Lancement du Fine-Tuning (QLoRA 4-bit)
```bash
# Mode simulation / vérification rapide de la configuration :
python finetuning/train_lora.py --dry_run

# Entraînement complet sur GPU Systalink Cloud :
python finetuning/train_lora.py \
  --model_name google/gemma-2-2b-it \
  --num_train_epochs 3 \
  --batch_size 2 \
  --learning_rate 0.0002
```

### 4. Évaluation des résultats
```bash
python finetuning/evaluate.py
```
