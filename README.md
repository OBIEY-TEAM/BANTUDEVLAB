# 🌍 BANTUDEVLAB — Forge Logicielle Souveraine de l'Afrique

> **BANTUDEVLAB** est la forge logicielle souveraine de l'Afrique : un système complet et sécurisé de gestion de versions conçu pour centraliser le code et propulser la collaboration des développeurs du continent en toute indépendance technologique et réglementaire.

---

## 🏛️ Stratégie Hybride et Architecture

BANTUDEVLAB combine la robustesse d'un moteur open-source éprouvé avec une surcouche souveraine en Python/Django :

```
                               ┌──────────────────────────────────────────────────┐
                               │                 DÉVELOPPEURS                     │
                               └────────────────────────┬─────────────────────────┘
                                                        │
                      ┌─────────────────────────────────┴─────────────────────────────────┐
                      │                                                                   │
                      ▼                                                                   ▼
       ┌──────────────────────────────┐                                   ┌──────────────────────────────┐
       │   Gitea / GitLab CE Engine   │◄──────── API REST / Webhooks ────►│    Surcouche BANTUDEVLAB     │
       │     (Systalink Cloud)        │                                   │       (Python / Django)      │
       ├──────────────────────────────┤                                   ├──────────────────────────────┤
       │ • Dépôts Git souverains      │                                   │ • Dashboard Panafricain      │
       │ • Pull Requests & Issues     │                                   │ • Zero-Trust ZKP Auth        │
       │ • CI/CD Runner intégré       │                                   │ • Scanner de Sécurité        │
       │ • Contrôle d'accès Git       │                                   │ • Assistant IA Gemma 5B      │
       └──────────────┬───────────────┘                                   └──────────────┬───────────────┘
                      │                                                                  │
                      └───────────────────────────────┬──────────────────────────────────┘
                                                      ▼
                                   ┌──────────────────────────────────────┐
                                   │       PostgreSQL 16 Multi-Tenant     │
                                   │   (Hébergement Cloud Panafricain)    │
                                   └──────────────────────────────────────┘
```

1. **Le moteur de gestion de versions (Déploiement)** :
   - Basé sur **Gitea / GitLab CE** déployé directement sur l'infrastructure cloud souveraine **Systalink**.
   - Fournit instantanément l'infrastructure de base de type GitHub (dépôts Git, pull requests, revues, interface standard).
2. **La surcouche souveraine (Code Python & Django)** :
   - Tableau de bord d'analyse de souveraineté et de sécurité.
   - Système d'authentification **Zero-Trust** basé sur les **Zero-Knowledge Proofs (ZKP)**.
   - Intégration de l'IA locale **Gemma 5B** pour auditer et assister les développeurs sans fuite de code vers l'extérieur.

---

## 🧰 Stack Technique

- **Moteur Git** : Gitea 1.23+ / GitLab CE
- **Backend & Surcouche** : Python 3.12, Django 5.x, Django REST Framework
- **Cryptographie & Sécurité** : Zero-Knowledge Proofs (Schnorr / Sigma NIZKP via Fiat-Shamir), Cryptography
- **Base de données** : PostgreSQL 16
- **Conteneurisation & OS** : Docker, Docker Compose, Linux
- **Intelligence Artificielle** : Gemma 5B (Local / QLoRA 4-bit)

---

## 🚀 Démarrage Rapide

### 1. Cloner le projet et configurer l'environnement
```bash
cp .env.example .env
```

### 2. Démarrer avec Docker Compose (Environnement Complet)
```bash
docker compose up -d
```
Les services seront accessibles sur :
- **Surcouche Souveraine BantuDevLab** : `http://localhost:8000`
- **Forge Git Gitea** : `http://localhost:3000`
- **Base PostgreSQL** : `localhost:5432`

### 3. Exécution locale (Mode Développement)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🔐 Authentification Zero-Trust (Zero-Knowledge Proofs - ZKP)

BANTUDEVLAB intègre un protocole cryptographique de **preuves à divulgation nulle de connaissance** (Schnorr / Sigma NIZKP via l'heuristique de Fiat-Shamir) :
- **Clé Privée ($x$)** : Reste strictement sur la machine du développeur.
- **Clé Publique ($y = g^x \pmod p$)** : Enregistrée sur la plateforme.
- **Engagement ($t = g^v \pmod p$)** et **Réponse ($s = v - c \cdot x \pmod q$)** : Permettent de vérifier mathématiquement l'identité sans qu'aucun mot de passe ni hash réversible ne transite sur le réseau.
- **Protection Anti-Replay** : Chaque session d'authentification requiert un *challenge nonce* à usage unique.

---

## 🛡️ Scanner de Sécurité et Score de Souveraineté

Le moteur `apps/security_scanner` analyse le code source à chaque commit et pull request :
- Détection des secrets et tokens hardcodés (GitHub/Gitea tokens, clés privées SSH/RSA, identifiants IAM, JWTs).
- Détection des failles courantes (Injections SQL, exécutions de commandes OS, eval/exec).
- Analyse de souveraineté : Détection des fuites de télémétrie et dépendances cloud étrangères non souveraines.
- Attribution d'un **Score de Souveraineté Numérique** (0-100%).

---

## 🧠 Dossier de Fine-Tuning Gemma 5B (`finetuning/`)

Le dossier `finetuning/` contient un pipeline d'entraînement complet pour adapter Gemma 5B aux cas d'usage africains :
- `dataset_preparation.py` : Génération de jeux de données d'instructions pour les systèmes bancaires (Mobile Money, USSD), la sécurité ZKP et les architectures souveraines.
- `train_lora.py` : Script d'entraînement avec quantification **QLoRA 4-bit (NF4)** optimisé pour GPU.
- `evaluate.py` : Évaluation des métriques de précision et de conformité sécuritaire.
- `README.md` : Guide complet d'entraînement et d'inférence.

Pour lancer un test du pipeline de fine-tuning :
```bash
python finetuning/dataset_preparation.py
python finetuning/train_lora.py --dry_run
python finetuning/evaluate.py
```

---

## 🧪 Tests Automatisés & Intégration Continue (CI/CD)

Le projet dispose d'une suite de tests complète couvrant 100% des modules :
```bash
python manage.py test tests -v 2
```

Le pipeline CI/CD GitHub Actions (`.github/workflows/ci.yml`) automatise :
1. Les vérifications de conformité système Django (`manage.py check`).
2. L'exécution de tous les tests unitaires et d'intégration (ZKP, Gitea client, Scanner, Assistant Gemma, Endpoints API).
3. La validation syntaxique et fonctionnelle du pipeline de fine-tuning.
4. La validation de la configuration Docker Compose et le build des conteneurs.

---

## 🌍 Vision Stratégique & Souveraineté Panafricaine

BANTUDEVLAB libère l'écosystème tech africain des dépendances extérieures :
- **Immunité Juridique** : Données protégées contre le Cloud Act américain et les sanctions extraterritoriales.
- **Résilience Réseau** : Capacité d'opération locale et décentralisée au sein des points d'échange Internet africains (IXP).
- **Fierté & Indépendance** : Une infrastructure pensée par et pour les développeurs africains.
