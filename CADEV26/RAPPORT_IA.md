# RAPPORT DE CONFORMITÉ SUR L'USAGE DE L'IA — CADEV 2026

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE  
- **Capitaine d'équipe :** OBIEY Christ Dany (Lead Architecture & Développement Fullstack)  
- **Membre de l'équipe :** MAMPOUYA Alicia Syrianne (Présentation vidéo démo & parcours utilisateur)  
**Branche de travail :** `main` / `docker-cadev26`  
**Date du rapport :** 13 novembre 2026  

---

## 1. Synthèse des Actions Réalisées (Tâches 1 à 4)

L'intégralité de la chaîne de déclaration d'usage de l'intelligence artificielle et de l'outillage de développement a été formalisée conformément à l'Article 6 du règlement du concours CADEV 2026 :

### 1.1 Tâche 1 — Section de déclaration dans `CADEV26/SOUMISSION.md`
- Mise à jour de la section **d)** avec un tableau complet catégorisant chaque outil mobilisé :
  - **Jules IA :** Éditeur de code assisté par IA, utilisé pour la résolution de bugs sur branches dédiées, l'alignement d'assets et les propositions de feuilles de route (PR #10, #11, #15, #24, #36, #41 déduites de l'historique Git).
  - **Antigravity IA :** Éditeur de code assisté par IA, utilisé pour l'audit de licences, le refactoring sans dépendance LGPL (`requests`), les scripts de conformité CI (`check_licenses.py`, `check_no_emoji.py`), et les suites de tests.
  - **Claude IA :** Assistant de compréhension, planification, rédaction de synthèses méthodologiques et d'analyses de conformité.
  - **GitHub :** Précisé expressément à part comme outil de versionnement et miroir de continuité Git, et **non comme un outil d'IA**.
  - **Gemma 2 2B (via Ollama) :** Clarifié comme **composant technique intégré à la solution livrée** (modèle local pour la revue de code sur la forge) et non comme outillage de développement.
- **Rôles de l'équipe formalisés :**
  - OBIEY Christ Dany : Capitaine d'équipe, Lead Architecture & Développement Fullstack.
  - MAMPOUYA Alicia Syrianne : Membre de l'équipe, Présentation vidéo démo & parcours utilisateur.
- **Engagement d'appropriation :** Déclaration solennelle certifiant que l'équipe comprend, relit, teste et assume l'intégralité du code et de l'architecture livrés.
- **Champs de signature :** Emplacements réservés avec signatures laissées vides pour chaque membre.

### 1.2 Tâche 2 — Ajout d'une section concise dans `README.md`
- Intégration d'une section factuelle et mesurée « Outils Utilisés » (exactement 5 lignes), renvoyant directement vers `CADEV26/SOUMISSION.md` sans superlatif.
- Indexation dans le sommaire principal du README.

### 1.3 Tâche 3 — Traçabilité et flux de travail dans `CADEV26/IA_USAGE.md`
- Rédaction d'un rapport de traçabilité complet décrivant la méthodologie de relecture humaine systématique et la validation par les tests automatisés (201 tests, couverture réelle de 95,62%).
- Inventaire exhaustif des traces observables dans l'historique Git (branches et PRs Jules, fichiers de planification `TASK/`, scripts d'outillage ponctuels `scratch/`).
- Respect strict de la consigne d'objectivité : aucune extrapolation sur un pourcentage de code généré n'a été formulée.

### 1.4 Tâche 4 — Audit de cohérence globale
- Analyse croisée de `pitch.md`, `onepitch.md`, `README.md` et `SOUMISSION.md`.
- **Résultat :** Aucune assertion contradictoire (telle que « codé entièrement à la main sans outil ») n'est présente dans les documents. Les mentions de « code original produit par l'équipe » font référence à la titularité et à l'absence de code tiers antérieur au 29 septembre 2026, ce qui est pleinement cohérent avec l'assistance d'éditeurs intelligents sous supervision humaine.

---

## 2. Liste Exhaustive des Champs « À Confirmer par l'Équipe »

Les points suivants relèvent de la validation humaine des membres de l'équipe CYBERSOCLE et doivent être confirmés avant la remise finale :

### 2.1 Périmètre de Déclaration des Outils IA (`CADEV26/SOUMISSION.md` - Section d.2)
- **Jules IA :** Confirmer si d'autres parties du code ou de l'architecture ont fait l'objet d'une assistance au-delà des PRs #10, #11, #15, #24, #36 et #41 identifiées dans l'historique Git.
- **Antigravity IA :** Confirmer si d'autres modules ont été assistés au-delà des scripts d'audit de licences, du refactoring client `requests`, de l'outillage CI et de la fiabilisation des tests unitaires.
- **Claude IA :** Confirmer si d'autres usages de rédaction ou de planification ont été mobilisés au-delà des documents de synthèse, de l'analyse juridique et de la méthodologie de conformité.

### 2.2 Signatures et Approbations Manuscrites (`CADEV26/SOUMISSION.md` - Sections b et d.3)
- **OBIEY Christ Dany :**
  - Renseigner la date et apposer la signature / mention « Lu et approuvé » pour la titularité des droits (section b).
  - Apposer la signature pour l'engagement de maîtrise et de responsabilité technique de la solution livrée (section d.3).
- **MAMPOUYA Alicia Syrianne :**
  - Renseigner la date et apposer la signature / mention « Lu et approuvé » pour la titularité des droits (section b).
  - Apposer la signature pour l'engagement de validation du parcours démo et de la solution livrée (section d.3).

### 2.3 Justificatifs Datacloud (`CADEV26/SOUMISSION.md` - Sections e.2 et f)
- **Identifiant client Datacloud :** Renseigner votre identifiant client Systalink / Datacloud.
- **Référence de commande / facture :** Renseigner le numéro de commande du domaine `cybersocle.site`.
- **Preuve d'achat :** Insérer la copie textuelle ou la référence de facture confirmant le règlement du service auprès de Datacloud.
