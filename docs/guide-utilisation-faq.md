# Guide d'Utilisation & Foire Aux Questions (FAQ) Souveraine

Ce document détaille l'utilisation complète de la plateforme souveraine panafricaine **BANTUDEVLAB** et de son moteur intégré **GitLab CE/EE**.

---

## Sommaire

1. [Mode d'utilisation fondamental](#1-mode-dutilisation-fondamental)
   - [Créer un compte GitLab / BantuDevLab](#comment-créer-un-compte)
   - [Se connecter en mode Zero-Trust](#comment-se-connecter)
   - [Consulter et cloner le code source](#comment-consulter-et-cloner-le-code-source)
2. [Questions fréquentes techniques & sécurité](#2-questions-fréquentes-techniques--sécurité)
   - [Authentification Zero-Trust ZKP vs mots de passe traditionnels](#quest-ce-que-lauthentification-zero-trust-zkp)
   - [Double approbation ZKP sur les Merge Requests](#comment-fonctionne-la-double-approbation-zkp-sur-les-merge-requests)
   - [Revue de code IA locale Gemma 5B sans fuite de données](#comment-lassistant-ia-local-gemma-5b-protège-t-il-le-code)
   - [Scanner SAST et calcul du score de souveraineté](#comment-fonctionne-le-scanner-de-sécurité-sast)
   - [Gestion Multi-Tenancy des organisations africaines](#comment-est-assurée-létanchéité-multi-tenancy)
   - [Conformité à la Convention de Malabo](#en-quoi-bantudevlab-respecte-t-il-la-convention-de-malabo)
   - [Politique Zéro-Emoji et accessibilité](#pourquoi-la-plateforme-nutilise-t-elle-aucun-emoji)
   - [Pipelines CI/CD sur runners souverains](#comment-exécuter-les-pipelines-cicd-sur-des-runners-panafricains)

---

## 1. Mode d'Utilisation Fondamental

### Comment créer un compte ?

L'accès à GitLab CE et à BANTUDEVLAB est unifié autour de l'identité cryptographique Zero-Trust.

#### Méthode 1 : Inscription cryptographique souveraine (Recommandée)
1. Ouvrez l'interface web de BANTUDEVLAB et accédez à **Connexion Zero-Trust** (`/zkp/login/`).
2. Sélectionnez l'onglet **Inscription Souveraine**.
3. Renseignez votre identifiant développeur (`username`) et votre pays de rattachement (ex: Côte d'Ivoire, Sénégal, Kenya, Nigeria...).
4. L'assistant génère automatiquement une phrase mnémonique BIP-39 (12 mots) et votre clé publique Schnorr $y = g^x \pmod p$.
5. Conservez votre phrase secrète en lieu sûr (elle ne transite jamais sur le réseau).
6. Cliquez sur **Créer mon Identité Souveraine** : le compte est créé et provisionné automatiquement dans l'instance GitLab CE associée via le fournisseur OmniAuth Bantu ZKP.

#### Méthode 2 : Inscription directe sur l'instance GitLab
1. Accédez à l'URL externe GitLab (bouton « Accès Forge Git »).
2. Cliquez sur « S'inscrire » (Register) ou utilisez le Single Sign-On (SSO) « Connexion avec Bantu ZKP ».
3. L'authentification mutuelle associe instantanément votre profil développeur à votre organisation d'appartenance.

---

### Comment se connecter ?

La connexion s'opère **sans aucun mot de passe stocké** grâce aux preuves à divulgation nulle de connaissance (ZKP) :

1. **Sur BantuDevLab :**
   - Accédez à la page de connexion.
   - Entrez votre nom d'utilisateur : le serveur émet un défi cryptographique (`challenge_nonce`) valable 5 minutes.
   - L'interface locale calcule la preuve Schnorr `(t, s)` avec votre secret $x$ et le nonce $c$ (Fiat-Shamir).
   - Le serveur valide mathématiquement que $g^s \equiv t \cdot y^c \pmod p$ sans jamais connaître $x$.
   - La session est ouverte.

2. **Sur GitLab CE (Single Sign-On OmniAuth) :**
   - Cliquez sur « Connexion avec Bantu ZKP ».
   - Si votre session BantuDevLab est déjà ouverte, l'accès est instantané.
   - Sinon, signez le défi mathématique émis pour ouvrir votre session GitLab en une étape.

---

### Comment consulter et cloner le code source ?

Plusieurs modalités sécurisées s'offrent aux développeurs :

1. **Consultation Web interactive :**
   - Directement depuis le **Tableau de Bord** (`/dashboard/`) de BANTUDEVLAB : visualisez l'arborescence, les branches, les commits et le code source avec l'éditeur intégré CodeMirror.
   - Directement sur l'instance GitLab CE : visualisez les Merge Requests, le graphe de commits, les wikis et les issues.

2. **Clonage Git via HTTPS avec Jeton ZKP :**
   - Générez un jeton d'accès Git (`bnt_...`) via l'endpoint `/api/zkp/tokens/generate/` ou depuis l'espace utilisateur.
   - Clonez le projet :
     ```bash
     git clone https://bnt_token@git.bantudevlab.africa/organisation/projet.git
     ```

3. **Clonage Git via SSH :**
   - Enregistrez votre clé publique SSH (Ed25519 ou RSA 4096 bits) dans votre profil GitLab.
   - Clonez le dépôt :
     ```bash
     git clone git@git.bantudevlab.africa:organisation/projet.git
     ```

---

## 2. Questions Fréquentes Techniques & Sécurité

### Qu'est-ce que l'authentification Zero-Trust ZKP ?
Le protocole Schnorr NIZKP (Non-Interactive Zero-Knowledge Proof) avec transformation de Fiat-Shamir repose sur le problème du logarithme discret (groupe MODP 2048 bits de la RFC 3526). Le serveur n'enregistre que la clé publique $y = g^x \pmod p$.
Le secret $x$ ne quitte jamais la mémoire du poste client. En cas de vol de la base de données serveur, aucun mot de passe ne peut être dérobé car aucun mot de passe n'existe.

### Comment fonctionne la double approbation ZKP sur les Merge Requests ?
Pour garantir l'intégrité du code critique gouvernemental, financier ou académique, une Merge Request ne peut pas être fusionnée sur un simple clic. Elle requiert la double signature mathématique ZKP (`SovereignMergeRequestApproval`) d'au moins deux relecteurs autorisés. Le webhook de validation bloque la fusion tant que le quorum cryptographique n'est pas atteint.

### Comment l'assistant IA local Gemma 5B protège-t-il le code ?
Contrairement aux solutions cloud étrangères assujetties au Cloud Act, l'inférence de l'assistant Gemma 5B est exécutée localement sur les serveurs Systalink Cloud (nœuds Abidjan, Dakar, Nairobi, Kigali). Le code analysé ne franchit aucune frontière continentale, et tous les secrets ou informations sensibles sont anonymisés (`AIInteractionLog`) avant toute persistance.

### Comment fonctionne le scanner de sécurité SAST ?
Le moteur SAST analyse syntaxiquement le code pour identifier les secrets codés en dur, les injections SQL, les appels dangereux (`eval`, `exec`, `os.system`) et les dépendances vulnérables. Il calcule un score de souveraineté sur 100. Les rapports sont générés au format OASIS SARIF 2.1.0 et GitLab SAST (`gl-sast-report.json`).

### Comment est assurée l'étanchéité Multi-Tenancy ?
Le modèle `SovereignOrganization` segmente les entités (banques centrales, ministères, universités, startups). Chaque entité dispose d'un espace isolé (`Tier-1 Continental`, `Tier-2 Regional`, `Tier-3 Startup`) synchronisé avec les groupes GitLab, avec cloisonnement strict des accès.

### En quoi BANTUDEVLAB respecte-t-il la Convention de Malabo ?
La Convention de l'Union Africaine sur la Cybersécurité et la Protection des Données Personnelles (2014) exige traçabilité et intégrité. BANTUDEVLAB implémente un journal d'audit immuable (`AuditTrailLog`) avec chaînage SHA-256 (`previous_hash`), vérifiable à tout instant via la commande :
```bash
python manage.py export_malabo_compliance_report
```

### Pourquoi la plateforme n'utilise-t-elle aucun emoji ?
La politique Zéro-Emoji est vérifiée en continu par `scripts/check_no_emoji.py`. Les icônes et drapeaux sont 100% SVG natifs et auto-hébergés. Cela assure une accessibilité irréprochable (WCAG 2.2 AA pour lecteurs d'écran) et une indépendance visuelle sans dépendre de polices tierces.

### Comment exécuter les pipelines CI/CD sur des runners panafricains ?
Les fichiers `.gitlab-ci.yml` peuvent cibler les tags de runners souverains :
```yaml
test-sovereign:
  stage: test
  tags:
    - sovereign-abidjan
    - tier1-runner
  script:
    - python -m pytest
    - python scripts/check_no_emoji.py
```
Les conteneurs de build s'exécutent en mode non-root avec isolation renforcée sur le continent africain.
