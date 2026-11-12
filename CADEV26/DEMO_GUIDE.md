# GUIDE DU PARCOURS DE DÉMONSTRATION & ÉVALUATION — CADEV 2026

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne (Présentation vidéo démo & parcours utilisateur)  
**Public cible :** Membres du Jury et Évaluateurs CADEV 2026 (profil technique ou non technique)  
**Environnement de test :**  
- Portail Souverain & API : https://cybersocle.site  
- Forge Gitea CE : https://git.cybersocle.site  

---

## 1. Vue d'Ensemble du Parcours d'Évaluation

Ce guide a été conçu pour permettre à tout évaluateur de tester l'ensemble des fonctionnalités clés de BantuDevLab en **moins de 5 minutes**, sans configuration préalable, sans ligne de commande complexe et sans aucun risque de blocage.

Le parcours s'articule autour de 4 étapes fluides :
1. **Accueil & Présentation :** Prise en main et indicateurs de souveraineté.
2. **Connexion Zero-Trust 1-Clic :** Démonstration de l'authentification ZKP sans mot de passe avec le compte préconfiguré `cadev_evaluator`.
3. **Consultation de la FAQ :** Compréhension des enjeux de souveraineté et d'architecture.
4. **Création d'un Dépôt & Revue de Code IA (Gemma 2 2B) :** Test direct de l'assistant d'ingénierie sur 3 exemples ciblés.

---

## 2. Étape 1 : Découverte de l'Accueil

1. Rendez-vous sur l'URL officielle du portail : **https://cybersocle.site/**
2. Vous arrivez sur la page d'accueil de la forge souveraine :
   - Présentation de la mission panafricaine (indépendance numérique, conformité Convention de Malabo 2014).
   - Jauge circulaire du score de souveraineté globale (ADSS-v1).
   - Sélecteur de langue bilingue et panafricain en haut à droite : Français (`FR`), Anglais (`EN`), Kiswahili (`SW`), Portugais (`PT`).
   - Bascule de thème Sombre / Clair via le bouton d'accessibilité.

---

## 3. Étape 2 : Connexion Zero-Trust en 1-Clic (ZKP)

BantuDevLab intègre une authentification sans mot de passe reposant sur les preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs - protocole de Schnorr non interactif avec challenge Fiat-Shamir).

### Procédure rapide pour l'évaluateur :
1. Accédez directement à la page d'authentification : **https://cybersocle.site/api/zkp/login-ui/?demo=cadev**  
   *(Ou cliquez sur « Connexion Zero-Trust » dans la barre de navigation, puis sur le bandeau vert « Connexion Démo 1-Clic »)*.
2. **Ce qui se produit automatiquement :**
   - Le champ nom d'utilisateur est pré-rempli avec l'identifiant démo : `cadev_evaluator`.
   - La clé secrète mnémonique BIP-39 (12 mots) est injectée localement dans le navigateur.
   - Le navigateur génère un engagement cryptographique aléatoire $r$, calcule le challenge Fiat-Shamir $c = \text{SHA-256}(g, y, t)$, puis la réponse $s = r + c \cdot x \pmod q$.
   - La preuve est transmise au serveur. Le serveur vérifie l'équation $g^s \equiv t \cdot y^c \pmod p$ sans jamais connaître ni stocker le secret.
3. **Résultat :** Un message de succès vert s'affiche instantanément :  
   `[SUCCÈS] Vérification Zero-Knowledge réussie ! Accès autorisé sans mot de passe.`
4. Vous êtes redirigé vers le tableau de bord souverain avec votre jeton de session actif.

---

## 4. Étape 3 : Consultation de la FAQ Souveraine

1. Cliquez sur l'onglet **« FAQ »** dans le menu de navigation ou accédez à : **https://cybersocle.site/faq/**
2. Cette section répond aux questions fondamentales sur le projet :
   - Qu'est-ce que le score de souveraineté ADSS-v1 ?
   - Comment fonctionne le protocole Schnorr Zero-Knowledge Proof ?
   - Pourquoi le projet n'utilise-t-il aucun service externe ou CDN non souverain ?
   - En quoi l'infrastructure est-elle alignée sur la Convention de Malabo de l'Union Africaine ?
   - Quel est le rôle exact du modèle local Gemma 2 2B par rapport aux outils développeur ?

---

## 5. Étape 4 : Création d'un Dépôt de Démonstration

L'évaluateur peut créer ou inspecter un dépôt Git souverain en quelques clics :

### Option A : Consultation d'un dépôt public existant
1. Rendez-vous sur le tableau de bord : **https://cybersocle.site/dashboard/**
2. Les dépôts officiels sont listés dans le sélecteur.
3. Cliquez sur le bouton externe **Gitea** pour ouvrir directement la vue du dépôt sur la forge :  
   `https://git.cybersocle.site/obiey-code/bantudevlab.git`

### Option B : Création d'un nouveau dépôt de test sur Gitea
1. Ouvrez l'interface de la forge : **https://git.cybersocle.site/**
2. Cliquez sur le bouton **« + »** en haut à droite puis sur **« Nouveau dépôt »**.
3. Renseignez un nom de dépôt (ex: `demo-audit-2026`) et cochez « Initialiser le dépôt (ajoute un .gitignore, une licence et un README) ».
4. Validez en cliquant sur **« Créer un dépôt »**. Le dépôt est immédiatement disponible pour les analyses SAST et les revues de code IA.

---

## 6. Étape 5 : Revue de Code IA avec Gemma 2 2B (3 Exemples Adaptés)

Le moteur d'intelligence artificielle locale de BantuDevLab s'appuie sur le modèle **Gemma 2 2B Instruct** (quantifié en 4 bits) hébergé localement sur conteneur Ollama.

> **Note sur le modèle 2B :** Un modèle compact de 2 milliards de paramètres est optimisé pour des tâches précises d'analyse de code, de détection de patterns de vulnérabilité et de documentation ciblée. Il ne s'agit pas d'un modèle généraliste lourd, mais d'une sentinelle de code souveraine exécutée on-premise sans fuite de données.

Voici **3 exemples concrets et prêts à tester** dans le Workbench du Dashboard (`/dashboard/`) ou via l'API de revue `/api/ai/code-review/` :

---

### Exemple 1 : Détection d'un Secret Codé en Dur (Fuite de Clé API)
*Objectif : Vérifier que le scanner et Gemma 2 2B détectent les secrets en clair avec forte entropie de Shannon.*

#### Code à coller dans l'analyseur :
```python
import requests

def push_audit_report(report_data):
    # Clé API sensible codée en dur dans le code source
    API_KEY = "sk-live-african-fintech-998822334455aabbcc"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post("https://api.fintech.sovereign/v1/audit", json=report_data, headers=headers)
    return response.json()
```

#### Résultat attendu :
- **Constat SAST / Gemma :** Alerte de niveau `CONFIDENTIALITÉ / CRITIQUE`. Détection d'un secret codé en clair avec entropie de Shannon $H \ge 3.8$.
- **Recommandation fournie :** Isoler immédiatement la clé secrète dans une variable d'environnement chiffrée ou dans le coffre-fort Zero-Trust de BantuDevLab, et ne jamais commiter de secret dans le dépôt.

---

### Exemple 2 : Faille d'Injection SQL par Concaténation de Chaînes
*Objectif : Vérifier que l'assistant identifie une requête SQL non paramétrée et propose la syntaxe sécurisée.*

#### Code à coller dans l'analyseur :
```python
def get_user_by_username(db_cursor, username_input):
    # Vulnérabilité : concaténation directe d'une variable non nettoyée
    query = f"SELECT id, username, email FROM auth_user WHERE username = '{username_input}'"
    db_cursor.execute(query)
    return db_cursor.fetchone()
```

#### Résultat attendu :
- **Constat SAST / Gemma :** Alerte `AVERTISSEMENT / INJECTION SQL`. Détection d'une f-string intégrant une variable d'entrée utilisateur directement dans la clause SQL.
- **Correction proposée :** Remplacement par une requête paramétrée avec tuple d'arguments :
  ```python
  query = "SELECT id, username, email FROM auth_user WHERE username = %s"
  db_cursor.execute(query, (username_input,))
  ```

---

### Exemple 3 : Fonction Utilitaires à Documenter et Sécuriser (Validation & Typage)
*Objectif : Évaluer la capacité du modèle compact à enrichir une fonction brute avec typage statique, docstring structurée et gestion d'erreurs (division par zéro).*

#### Code à coller dans l'analyseur :
```python
def compute_sovereignty_ratio(local_nodes, total_nodes):
    return (local_nodes / total_nodes) * 100
```

#### Résultat attendu :
- **Constat SAST / Gemma :** Risque de levée d'exception non interceptée `ZeroDivisionError` si `total_nodes == 0`. Absence d'annotations de types et de documentation.
- **Correction et optimisation proposées :**
  ```python
  def compute_sovereignty_ratio(local_nodes: int, total_nodes: int) -> float:
      """
      Calcule le pourcentage de nœuds d'infrastructure souverains.
      
      Args:
          local_nodes (int): Nombre de nœuds hébergés sur le continent.
          total_nodes (int): Nombre total de nœuds du cluster.
          
      Returns:
          float: Ratio de souveraineté compris entre 0.0 et 100.0%.
      """
      if total_nodes <= 0:
          return 0.0
      return round((local_nodes / total_nodes) * 100, 2)
  ```

---

## 7. Tableau Récapitulatif du Parcours d'Évaluation

| Étape | Page / URL | Action Évaluateur | Temps estimé | Résultat visible |
| :--- | :--- | :--- | :--- | :--- |
| **1. Accueil** | `/` | Découvrir l'interface, tester le switch de langue (FR/EN/SW/PT) | 30 s | Affichage multilingue instantané, score de souveraineté |
| **2. Connexion ZKP** | `/api/zkp/login-ui/?demo=cadev` | Cliquer sur « Connexion Démo 1-Clic » | 15 s | Preuve cryptographique Schnorr résolue sans mot de passe |
| **3. FAQ** | `/faq/` | Parcourir les explications d'architecture et de souveraineté | 45 s | Réponses détaillées sur ZKP, Malabo et l'IA locale |
| **4. Forge Git** | `https://git.cybersocle.site` | Consulter les dépôts ou créer un dépôt test | 1 min | Interface Gitea CE native 100% opérationnelle |
| **5. Revue IA** | `/dashboard/` | Tester l'un des 3 snippets de code avec Gemma 2 2B | 1 min 30 s | Constats SAST, recommandations de sécurité et correction |
