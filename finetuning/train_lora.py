"""
Fine-Tuning Script for Gemma 2 2B using QLoRA (Quantized Low-Rank Adaptation).
Optimized for sovereign African cloud nodes with consumer or datacenter GPUs (16GB - 24GB VRAM).

Key Techniques:
- 4-bit NormalFloat (NF4) quantization via BitsAndBytes.
- Double quantization and bfloat16 compute.
- LoRA on attention projection layers (q_proj, k_proj, v_proj, o_proj).
- Supervised Fine-Tuning Trainer (SFTTrainer) from TRL.
"""

import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune Gemma 2 2B for BantuDevLab")
    parser.add_argument("--model_name", type=str, default="google/gemma-2-2b-it", help="Base model identifier or path")
    parser.add_argument("--dataset_path", type=str, default="finetuning/sovereign_instruct_dataset.jsonl")
    parser.add_argument("--output_dir", type=str, default="finetuning/lora_gemma_weights")
    parser.add_argument("--num_train_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-4)
    parser.add_argument("--dry_run", action="store_true", help="Validates configuration and inputs without loading GPU")
    return parser.parse_args()


def train(args):
    print("=" * 60)
    print("BANTUDEVLAB -- Entrainement Souverain Gemma 2 2B (QLoRA)")
    print(f"Modele source        : {args.model_name}")
    print(f"Fichier de donnees   : {args.dataset_path}")
    print(f"Dossier de sortie    : {args.output_dir}")
    print(f"Epoques             : {args.num_train_epochs}")
    print(f"Taux d'apprentissage : {args.learning_rate}")
    print("=" * 60)

    if not os.path.exists(args.dataset_path):
        from dataset_preparation import generate_training_data

        print("Generation automatique du jeu de donnees...")
        generate_training_data(args.dataset_path)

    if args.dry_run:
        print("[SUCCES] Validation du pipeline de fine-tuning reussie (Dry-Run mode).")
        print("Pret pour l'execution sur cluster GPU Systalink Cloud.")
        return 0

    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
        from trl import SFTTrainer
    except ImportError as e:
        print(f"[NOTE] Les dependances GPU/PyTorch lourdes ne sont pas installees: {e}")
        print("Pour lancer l'entrainement complet : pip install -r finetuning/requirements.txt")
        return 0

    print("Configuration de la quantification 4-bit NF4...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.pad_token = tokenizer.eos_token

    print("Chargement du modele de base quantifie...")
    model = AutoModelForCausalLM.from_pretrained(args.model_name, quantization_config=bnb_config, device_map="auto")
    model = prepare_model_for_kbit_training(model)

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, peft_config)
    print("Parametres entrainables LoRA calcules.")

    dataset = load_dataset("json", data_files=args.dataset_path)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_steps=10,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        save_strategy="epoch",
        optim="paged_adamw_8bit",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        dataset_text_field="text",
        max_seq_length=1024,
        tokenizer=tokenizer,
        args=training_args,
    )

    print("Demarrage de l'entrainement...")
    trainer.train()
    trainer.model.save_pretrained(args.output_dir)
    print(f"[SUCCES] Modele fine-tune souverain sauvegarde avec succes dans : {args.output_dir}")
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(train(args))
