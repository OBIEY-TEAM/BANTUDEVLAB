# Pipeline de Fine-Tuning Gemma 2 2B -- BANTUDEVLAB

Ce dossier contient l'ensemble des outils necessaires pour entrainer et adapter le modele de fondation **Gemma 2 2B** aux specificites de la forge logicielle souveraine panafricaine.

## Objectifs du Fine-Tuning
1. **Securite & Zero-Trust** : Maitrise des protocoles de Zero-Knowledge Proof (Schnorr, Fiat-Shamir) et detection des secrets hardcodes.
2. **Contextes Techniques Africains** : Optimisation pour les architectures bancaires Mobile Money, APIs telecoms USSD, et contraintes d'infrastructure locale.
3. **Souverainete des Donnees** : Execution 100% locale/sur serveur Systalink Cloud sans telemetrie externe ni dependance etrangere.

---

## Architecture des Fichiers

| Fichier | Role |
|---|---|
| `dataset_preparation.py` | Genere et formate le dataset d'instructions souverain (`sovereign_instruct_dataset.jsonl`). |
| `train_lora.py` | Script d'entrainement avec quantification QLoRA 4-bit (BitsAndBytes + PEFT + TRL). |
| `evaluate.py` | Suite de tests et metriques d'evaluation de la qualite du modele fine-tune. |
| `export_gguf.py` | Outil d'export et empaquetage au format quantifie GGUF (q4_k_m) pour inference ultra-legere (SOUV-04). |
| `requirements.txt` | Dependances necessaires pour les calculs GPU (PyTorch, Transformers, Accelerate). |

---

## Guide d'Utilisation

### 1. Preparation de l'environnement GPU
```bash
pip install -r finetuning/requirements.txt
```

### 2. Generation du dataset d'entrainement
```bash
python finetuning/dataset_preparation.py
```

### 3. Lancement du Fine-Tuning (QLoRA 4-bit)
```bash
# Mode simulation / verification rapide de la configuration :
python finetuning/train_lora.py --dry_run

# Entrainement complet sur GPU Systalink Cloud :
python finetuning/train_lora.py \
  --model_name google/gemma-2-2b-it \
  --num_train_epochs 3 \
  --batch_size 2 \
  --learning_rate 0.0002
```

### 4. Evaluation des resultats
```bash
python finetuning/evaluate.py
```

### 5. Export & Packaging GGUF (Inference Souveraine Ultra-Legere - SOUV-04)
```bash
# Exportation simulee (Dry-Run)
python finetuning/export_gguf.py --dry_run

# Exportation complete et quantification 4-bit
python finetuning/export_gguf.py \
  --weights_dir finetuning/lora_gemma_weights \
  --output_path finetuning/gemma2-2b-sovereign-q4_k_m.gguf \
  --quantization q4_k_m
```

### 6. Importation et Deploiement dans Ollama
```bash
ollama create gemma2:2b -f finetuning/Modelfile
ollama run gemma2:2b
```
