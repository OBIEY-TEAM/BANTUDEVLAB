# TASK5.md — Audit Global, Incohérences, Failles et Plan Directeur BANTUDEVLAB (LLM Cible : gemma2:2b)

Ce document constitue le rapport d'analyse exhaustif, technique et opérationnel de la plateforme de forge logicielle souveraine panafricaine **BANTUDEVLAB**, intégrant l'alignement stratégique sur le modèle de langage local optimisé **gemma2:2b** (Google Gemma 2 2B Instruct / GGUF Q4_K_M).

---

## 1. Synthèse Exécutive et Diagnostic du Projet

BANTUDEVLAB combine un écosystème hybride composé de :
1. Un frontal et backend Django souverain (Zero-Knowledge Proofs Schnorr, Scanner SAST, Audit Trail Malabo).
2. Un moteur Git collaboratif s'appuyant sur Gitea CE et GitLab CE/EE.
3. Un module d'assistance logicielle et de revue de code par intelligence artificielle locale.

### Contexte du Modèle LLM : Migration et Alignement vers `gemma2:2b`
L'analyse du référentiel révèle une incohérence majeure de ciblage de modèle de langage :
- Le fichier `config/settings.py`, les modèles de données `apps/ai_assistant/models.py` et le moteur `apps/ai_assistant/gemma.py` référencent par défaut le tag obsolète ou lourd `gemma:5b`.
- À l'inverse, l'outillage de fine-tuning (`finetuning/train_lora.py` et `finetuning/README.md`) cible déjà explicitement `google/gemma-2-2b-it` et l'architecture `gemma2` (`finetuning/export_gguf.py`).
- **Décision d'architecture :** La version **gemma2:2b** offre un ratio performance/consommation mémoire idéal pour un déploiement souverain sur des serveurs panafricains à ressources maîtrisées (CPU standard ou GPU 4 Go à 8 Go VRAM avec quantification 4-bit GGUF). Toutes les spécifications doivent converger vers l'identifiant et l'architecture unifiée `gemma2:2b`.

---

## 2. Inventaire Exhaustif des Failles de Sécurité, Incohérences et Bugs Détectés

### 2.1 Failles de Sécurité (SEC)

| Identifiant | Sévérité | Composant | Description de la Faille | Risque et Impact |
|---|---|---|---|---|
| **BUG-SEC-01** | **Haute** | `templates/core/dashboard.html` & `config/settings.py` | Inclusion de ressources JavaScript et CSS externes via le CDN public `cdnjs.cloudflare.com` (CodeMirror 5.65.16), couplée à une directive CSP permissive (`script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com`). | Contredit directement le principe de souveraineté numérique et d'autonomie continentale. En cas de blocage d'accès internet international ou de compromission du CDN étranger, l'intégrité de la forge et la confidentialité du code sont compromises. |
| **BUG-SEC-02** | **Moyenne** | `apps/security_scanner/engine.py` | L'analyseur SAST utilise des expressions régulières (Regex) statiques plutôt qu'un analyseur syntaxique abstrait (AST). De plus, les motifs de secrets n'intègrent pas de vérification d'entropie (Shannon entropy). | Faux-positifs fréquents et faux-négatifs critiques (évasion facile par obfusquation, découpage de chaînes ou encodage Base64). |
| **BUG-SEC-03** | **Moyenne** | `apps/zkp_auth/views.py` | Absence de purge automatique en tâche de fond des challenges ZKP expirés (`ZKPChallenge`). Seule la validation à l'authentification marque les nonces utilisés. | Risque d'attaque par déni de service (DoS) par accumulation massive de challenges orphelins dans la table PostgreSQL/SQLite. |
| **BUG-SEC-04** | **Faible** | `apps/core/audit.py` | La méthode `verify_chain_integrity()` charge la totalité de la table `AuditTrailLog` en mémoire vive sans découpage par curseur de lot (`iterator(chunk_size=...)`). | Saturation mémoire (OOM Crash) dès que le journal d'audit dépasse plusieurs dizaines de milliers d'événements. |
| **BUG-SEC-05** | **Faible** | `apps/zkp_auth/crypto.py` | Les opérations d'exponentiation modulaire `pow(G, x, P)` utilisent l'arithmétique standard Python sans garantie de temps d'exécution strictement constant face aux attaques par canaux auxiliaires (timing attacks). | Risque théorique de fuite d'informations partielles sur le secret x sous surveillance réseau ou sur hôte mutualisé. |

### 2.2 Incohérences d'Architecture et d'Implémentation (ARCH & AI)

| Identifiant | Sévérité | Composant | Description de l'Incohérence | Impact Opérationnel |
|---|---|---|---|---|
| **BUG-ARCH-01** | **Haute** | `apps/ai_assistant/` vs `finetuning/` | Divergence de nommage et de calibrage du modèle LLM : `GEMMA_MODEL_NAME = "gemma:5b"` dans Django vs `google/gemma-2-2b-it` dans `train_lora.py` et `export_gguf.py`. | Si l'opérateur déploie Ollama avec le modèle finetuné `gemma2:2b`, l'assistant Django tente d'appeler `gemma:5b` et bascule silencieusement sur le moteur de secours (fallback). |
| **BUG-ARCH-02** | **Haute** | `apps/core/views.py` | Les vues `home_view` et `dashboard_view` effectuent des appels directs et synchrones vers `GitLabClient` et `GiteaClient` lors du rendu de la page HTML. | Si l'instance GitLab ou Gitea ralentit ou subit une coupure, le thread Django se bloque et la page d'accueil ne répond plus aux utilisateurs. |
| **BUG-ARCH-03** | **Moyenne** | `apps/ai_assistant/views.py` & `gemma.py` | Absence de validation de la taille maximale du code soumis à l'API IA (taille de payload non bornée avant injection dans le prompt LLM). | Risque de dépassement de la fenêtre de contexte du modèle `gemma2:2b` (8192 tokens) ou crash du service d'inférence local par saturation GPU/RAM. |
| **BUG-ARCH-04** | **Moyenne** | `gitlab/lib/gitlab/auth/bantu_zkp.rb` & `apps/gitlab_client/client.py` | Les exceptions réseau sont interceptées par de simples blocs `try...except Exception: pass` sans journalisation structurée ni notification d'alerte dans Prometheus/Sentry. | Débogage difficile en production industrielle lors d'échecs de synchronisation ou de webhooks rejetés. |
| **BUG-ARCH-05** | **Faible** | `config/settings.py` | `SESSION_COOKIE_SAMESITE = "Lax"` et `CSRF_COOKIE_SAMESITE = "Lax"` sont configurés par défaut au lieu de la politique stricte recommandée pour une forge Zero-Trust. | Protection CSRF relâchée sur les requêtes cross-site en environnement d'entreprise. |

### 2.3 Problèmes de Design UI/UX et Front-end (UI/UX)

| Identifiant | Sévérité | Composant | Description du Problème Front-end | Impact Utilisateur |
|---|---|---|---|---|
| **BUG-UI-01** | **Moyenne** | `templates/core/dashboard.html` | Dépendance externe directe vers les feuilles de style et scripts de CodeMirror sur Cloudflare CDN. | En cas de déconnexion WAN (réseau souverain déconnecté d'Internet), l'éditeur de code intégré au tableau de bord ne se charge pas et affiche une zone de texte brute non stylisée. |
| **BUG-UI-02** | **Faible** | `templates/zkp_auth/login.html` | Le visualiseur d'entropie et de dérivation de clé Schnorr ne fournit pas de feedback visuel explicite de latence lorsque l'inférence ou la vérification dure plus de 500 ms. | Confusion possible de l'utilisateur qui clique plusieurs fois sur le bouton de connexion ZKP. |
| **BUG-UI-03** | **Faible** | `templates/core/metrics.html` | La carte de télémétrie des nœuds souverains (Abidjan, Dakar, Nairobi, Kigali) contient des données statiques codées en dur sans possibilité de rafraîchissement dynamique WebSocket/SSE. | Manque de visibilité en temps réel sur la disponibilité des nœuds d'infrastructure. |

---

## 3. Matrice Opérationnelle des Tâches de Correction et d'Évolution

### Axe 1 : Développement Backend & Architecture Souveraine (DEV)

- [ ] **T-DEV-501 : Bascule Complète du Socle IA vers le Modèle `gemma2:2b`**
  - Modifier `config/settings.py` : définir `GEMMA_MODEL_NAME = os.environ.get("GEMMA_MODEL_NAME", "gemma2:2b")`.
  - Mettre à jour `apps/ai_assistant/models.py` : définir la valeur par défaut du champ `model_used` sur `"gemma2:2b"`.
  - Mettre à jour `apps/ai_assistant/gemma.py` et les tâches Celery associées (`tasks.py`) pour exploiter l'identifiant `"gemma2:2b"`.
  - Adapter le prompt système pour respecter le format de prompt de Gemma 2 (`<start_of_turn>user\n...<end_of_turn>\n<start_of_turn>model\n`).
- [ ] **T-DEV-502 : Découplage Asynchrone et Mise en Cache des Appels GitLab/Gitea**
  - Supprimer tout appel direct bloquant aux API GitLab/Gitea dans les vues HTML de `apps/core/views.py`.
  - Mettre en place une tâche Celery périodique (`sync_forge_repositories_cache`) rafraîchissant les dépôts dans Redis toutes les 30 secondes.
  - Servir les vues `home_view` et `dashboard_view` exclusivement via le cache Redis avec stratégie de repli instantané sans latence.
- [ ] **T-DEV-503 : Curseur et Pagination par Lots pour la Vérification d'Audit Malabo**
  - Modifier `apps/core/audit.py` : refactoriser `verify_chain_integrity()` pour utiliser `.iterator(chunk_size=1000)`.
  - Créer une tâche Celery dédiée planifiée chaque nuit pour certifier la chaîne de hachage SHA-256 sans impacter la mémoire du serveur.
- [ ] **T-DEV-504 : Purge Automatique Périodique des Challenges ZKP Expirés**
  - Ajouter une méthode de classe `ZKPChallenge.purge_expired_challenges()` supprimant les nonces expirés depuis plus de 10 minutes.
  - Planifier l'exécution de la purge toutes les 15 minutes via Celery Beat.
- [ ] **T-DEV-505 : Limitation Stricte du Payload et Anonymisation PII pour l'Assistant IA**
  - Dans `apps/ai_assistant/views.py`, ajouter une vérification de la taille du code soumis (limite maximale : 256 Ko ou 15 000 caractères).
  - Nettoyer les adresses IP, emails et clés API évidents du code avant soumission au modèle `gemma2:2b`.

---

### Axe 2 : Sécurité Industrielle, Cryptographie & Zero-Trust (SEC)

- [ ] **T-SEC-501 : Éradication Totale des CDN Externes et CSP Stricte**
  - Télécharger et auto-héberger les scripts et feuilles de style CodeMirror 5.65.16 dans le répertoire statique local `static/vendor/codemirror/`.
  - Mettre à jour `templates/core/dashboard.html` pour charger les assets via le tag Django `{% static 'vendor/codemirror/...' %}`.
  - Verrouiller la directive CSP dans `config/settings.py` : supprimer toute référence à `https://cdnjs.cloudflare.com`.
- [ ] **T-SEC-502 : Durcissement du Scanner SAST avec Détection d'Entropie**
  - Étendre `apps/security_scanner/engine.py` en ajoutant le calcul de l'entropie de Shannon sur les chaînes de plus de 20 caractères pour détecter les tokens chiffrés ou aléatoires.
  - Intégrer l'analyseur syntaxique standard Python `ast` pour repérer formellement les appels à `eval`, `exec` et `os.system` même en cas de renommage d'alias.
- [ ] **T-SEC-503 : Journalisation Structurée des Exceptions GitLab/Gitea**
  - Remplacer les clauses silencieuses `except Exception: pass` dans `apps/gitlab_client/client.py` et `apps/ai_assistant/gemma.py` par des logs structurés via `logging.getLogger("bantudevlab.security")`.
  - Enregistrer les tentatives d'accès échouées dans l'audit trail souverain.
- [ ] **T-SEC-504 : Durcissement des Cookies de Session et Protection CSRF**
  - Définir `SESSION_COOKIE_SAMESITE = "Strict"` et `CSRF_COOKIE_SAMESITE = "Strict"` en production.
  - Garantir l'invalidation systématique de session lors du renouvellement des clés ZKP.

---

### Axe 3 : Modèle LLM, Inférence et Fine-Tuning `gemma2:2b` (AI/LLM)

- [ ] **T-AI-501 : Standardisation du Format de Dialogue Instruct Gemma 2**
  - Adapter le constructeur de prompt dans `apps/ai_assistant/gemma.py` pour respecter la syntaxe officielle de Gemma 2 :
    ```text
    <start_of_turn>user
    Système : Vous êtes BANTU-AI...
    Code à analyser :
    ...
    <end_of_turn>
    <start_of_turn>model
    ```
- [ ] **T-AI-502 : Alignement du Script de Fine-Tuning LoRA et Export GGUF**
  - Vérifier que `finetuning/train_lora.py` utilise par défaut `--model_name google/gemma-2-2b-it`.
  - Mettre à jour `finetuning/export_gguf.py` pour générer un fichier nommé `gemma2-2b-sovereign-q4_k_m.gguf`.
  - Mettre à jour la documentation `finetuning/README.md` et les scripts d'importation Ollama (`Modelfile`) avec la mention de `gemma2:2b`.
- [ ] **T-AI-503 : Optimisation du Streaming SSE pour Gemma 2 2B**
  - Ajuster les paramètres d'inférence pour `gemma2:2b` : `temperature: 0.15`, `top_p: 0.9`, `num_predict: 1024`.
  - Traiter les cas de déconnexion client SSE pendant la génération pour stopper prématurément la requête vers Ollama/vLLM.

---

### Axe 4 : Design UI/UX Panafricain & Front-End Souverain (UI/UX)

- [ ] **T-UX-501 : Intégration Locale Complète de l'Éditeur CodeMirror**
  - Déployer les fichiers de CodeMirror en local : CSS du thème, JS principal, mode Python, addon de fermeture automatique de crochets.
  - S'assurer que le thème sombre/clair s'adapte automatiquement aux variables CSS existantes (`--bg-primary`, `--accent-color`).
- [ ] **T-UX-502 : Feedback d'État Interactif pour le Wizard ZKP (BIP-39)**
  - Ajouter un indicateur de chargement SVG natif (sans emoji) lors du calcul des preuves Fiat-Shamir et de l'interrogation du serveur.
  - Améliorer l'accessibilité au clavier (touches Tab, Entrée) du sélecteur de mots de la phrase mnémonique souveraine.
- [ ] **T-UX-503 : Rafraîchissement Visuel des Métriques de Souveraineté**
  - Ajouter un bouton d'actualisation asynchrone (Fetch API) dans `templates/core/metrics.html` pour recharger les indicateurs de nœuds sans recharger la page complète.
  - Garantir le respect absolu des contrastes de couleur WCAG 2.2 AA sur l'ensemble des badges et graphiques SVG.
- [ ] **T-UX-504 : Maintien Strict de la Politique Zéro-Emoji**
  - Veiller à ce qu'aucun emoji Unicode ne soit introduit dans les gabarits, fichiers CSS/JS ou fichiers de documentation.
  - Utiliser exclusivement les balises `{% icon 'nom_icone' %}` et `{% flag 'code_pays' %}`.

---

### Axe 5 : Assurance Qualité, Tests & Fuzzing (QA/TEST)

- [ ] **T-QA-501 : Tests Unitaires et d'Intégration du Moteur `gemma2:2b`**
  - Mettre à jour `tests/test_ai_assistant.py` et `tests/test_qa_coverage.py` pour valider les réponses et fallbacks avec le modèle `gemma2:2b`.
  - Tester les formats de prompts spécifiques Gemma 2 et la gestion des flux SSE partiels.
- [ ] **T-QA-502 : Extension des Tests de Fuzzing Cryptographique ZKP**
  - Dans `tests/test_zkp_fuzzing.py`, tester des nonces dépassant la taille de 512 octets et des clés publiques en dehors du groupe premier pour vérifier le rejet strict.
  - Valider l'idempotence et la résistance aux attaques par rejeu de challenge sous accès concurrent.
- [ ] **T-QA-503 : Tests E2E Playwright de l'Expérience Hors-Ligne (Zero CDN)**
  - Enrichir `tests/test_e2e_playwright.py` pour vérifier que le tableau de bord et l'éditeur CodeMirror se chargent parfaitement sans aucune requête réseau sortant vers l'extérieur du serveur local.
- [ ] **T-QA-504 : Maintien d'une Couverture de Code Supérieure ou Égale à 95%**
  - S'assurer que `apps/zkp_auth`, `apps/security_scanner` et `apps/ai_assistant` conservent une couverture de test stricte `pytest --cov`.

---

### Axe 6 : Intégration Continue, Docker & Déploiement Industriel (OPS/CI)

- [ ] **T-OPS-501 : Configuration du Service Inférence Ollama dans Docker Compose**
  - Ajouter un service `ollama` configuré avec le volume de stockage local des poids `gemma2:2b` dans `docker-compose.yml` et `docker-compose.production.yml`.
  - Configurer un script d'initialisation téléchargeant ou chargeant le modèle `gemma2:2b` au démarrage du conteneur.
- [ ] **T-OPS-502 : Automatisation des Contrôles de Sécurité dans GitLab CI**
  - Compléter `.gitlab-ci.yml` avec l'exécution systématique de :
    - `ruff check .` et `ruff format --check .`
    - `bandit -r apps config -lll`
    - `python scripts/check_no_emoji.py`
    - `pytest --cov=apps/zkp_auth --cov=apps/security_scanner --cov=apps/ai_assistant --cov-fail-under=95`
- [ ] **T-OPS-503 : Durcissement des Images Docker et Isolation Réseau**
  - Valider l'exécution rootless de l'ensemble des conteneurs (`appuser:1000`).
  - Isoler le conteneur d'inférence LLM pour qu'il ne soit accessible que par le réseau privé interne `backend_net`.

---

## 4. Critères de Validation et Définition du Terminé (Definition of Done)

Toute tâche de ce plan directeur sera considérée comme terminée uniquement lorsque les conditions suivantes seront intégralement vérifiées :
1. **Modèle de Langage Aligné :** Le nom de modèle `gemma2:2b` est utilisé de façon uniforme dans la configuration Django, les logs de base de données et l'outillage de fine-tuning.
2. **Zéro CDN Externe :** L'intégralité des scripts, styles et polices est hébergée en local sur le serveur souverain.
3. **Zéro Emoji :** Le script de contrôle `python scripts/check_no_emoji.py` retourne `OK : aucun emoji.` avec le code de sortie 0.
4. **Qualité et Sécurité Validées :** Les commandes `ruff check .`, `ruff format --check .`, `bandit` et `pytest` s'exécutent avec succès sans aucun avertissement bloquant.
5. **Traçabilité Malabo :** Toute modification critique est inscrite dans la chaîne d'audit immuable SHA-256.
