# Pitch CADEV 2026 - BANTUDEVLAB (10 minutes)

**Message unique** : « Le code de l'Afrique, hébergé, sécurisé et assisté en Afrique. »
**Objectif** : obtenir 3 pilotes institutionnels, des partenaires d'hébergement et un financement d'amorçage.
**Durée cible** : 9 min 30 (30 s de marge). **Format** : 12 diapositives maximum, démo en direct de 3 min 15 avec vidéo de secours.

> Les chiffres entre crochets `[...]` sont à **mesurer et sourcer avant le jour J** (voir la check-list). Ne présentez aucun chiffre non vérifié.

## Minutage

| Temps | Section | Orateur | Support |
|---|---|---|---|
| 0:00-0:45 | Accroche | Porteur du projet | Diapo 1-2 |
| 0:45-1:45 | Problème | Porteur | Diapo 3 |
| 1:45-2:45 | Solution | Porteur | Diapo 4-5 |
| 2:45-6:00 | Démo en direct | Technique | Application + vidéo de secours |
| 6:00-7:00 | Technologie et sécurité | Technique | Diapo 6-7 |
| 7:00-8:00 | Marché et impact | Porteur | Diapo 8 |
| 8:00-8:45 | Modèle économique et feuille de route | Porteur | Diapo 9-10 |
| 8:45-9:30 | Équipe et traction | Porteur | Diapo 11 |
| 9:30-10:00 | Appel à l'action | Porteur | Diapo 12 |

## Script détaillé

### 0:00-0:45 - Accroche (diapo 1-2)
« Imaginez un développeur d'Abidjan, de Dakar ou de Kigali. Chaque ligne de code qu'il écrit, chaque secret, chaque idée de produit est stocké sur des serveurs situés sous une autre juridiction, derrière un compte et un mot de passe qui peuvent être suspendus, piratés ou surveillés. Aujourd'hui, la plus grande partie du code africain vit hors d'Afrique. Nous changeons cela. Je vous présente BANTUDEVLAB. »

### 0:45-1:45 - Le problème (diapo 3)
Quatre risques, une icône par risque (aucun emoji) :
1. **Dépendance** : un fournisseur étranger peut couper l'accès.
2. **Juridique** : données soumises à des lois extraterritoriales.
3. **Sécurité** : mots de passe réutilisés et volés, secrets commités par erreur.
4. **Coût et latence** : paiement en devises, aller-retour intercontinental `[latence mesurée Abidjan vers un hébergeur européen / local]`.

### 1:45-2:45 - La solution (diapo 4-5)
« BANTUDEVLAB est une forge logicielle souveraine : un moteur Git éprouvé, Gitea, hébergé sur une infrastructure panafricaine, avec trois ajouts qui font la différence. » Schéma d'architecture ([docs/architecture.md](architecture.md)) :
1. **Identité sans mot de passe** (preuve à divulgation nulle de connaissance).
2. **Audit de sécurité et de souveraineté** automatique du code.
3. **Assistant IA local** (Gemma 5B) : le code ne quitte jamais la juridiction.

### 2:45-6:00 - Démo en direct (3 min 15)
Préparer : jeu de données de démonstration, navigateur plein écran, zoom 125 %, notifications désactivées.

| Min | Action | Message à dire |
|---|---|---|
| 0:00-0:50 | Page de connexion : générer la phrase de 12 mots, enregistrer l'identité | « Aucun mot de passe n'est envoyé : le serveur ne connaît que la clé publique. » |
| 0:50-1:20 | Se connecter : « Prouver mon identité » | « Une preuve mathématique à usage unique remplace le mot de passe : impossible à rejouer. » |
| 1:20-2:00 | Tableau de bord : coller un fichier avec un secret en dur, lancer l'audit | « Secrets, injections, dépendances non souveraines : score de souveraineté immédiat, export SARIF pour la CI. » |
| 2:00-2:45 | Demander l'avis de Gemma (flux en direct) | « L'IA tourne chez nous, hors ligne si nécessaire. » |
| 2:45-3:15 | Page souveraineté : carte des nœuds | « Cinq nœuds panafricains, une seule juridiction africaine. » |

**Plan B** (si réseau ou application en panne) : lancer la vidéo de 3 min pré-enregistrée sans commentaire d'excuse ; enchaîner.

### 6:00-7:00 - Technologie et sécurité (diapo 6-7)
- Preuve de Schnorr (RFC 3526, 2048 bits), défis à usage unique consommés de façon atomique.
- API fermée par défaut, journal d'audit chaîné par hachage, secrets masqués avant journalisation de l'IA.
- Conteneurs durcis, base de données non exposée, HTTPS strict et HSTS en production.
- Qualité : `[nombre]` tests automatisés, couverture `[mesurée]` %, analyse `bandit`/`ruff`/dépendances en intégration continue.
- Transparence : modèle de menaces et limites publiés ([threat-model](security/threat-model.md)). Audit externe prévu.

### 7:00-8:00 - Marché et impact (diapo 8)
Cibles : banques centrales et banques, ministères, universités, startups, éditeurs de logiciels. Un cas d'usage par pays de la démo (Côte d'Ivoire, Sénégal, Nigeria, Kenya, Rwanda). Chiffres de marché : `[source citée obligatoire]`.

### 8:00-8:45 - Modèle économique et feuille de route (diapo 9-10)
- **Revenus** : hébergement géré par organisation, support et conformité, formation, instances dédiées.
- **Feuille de route** : T4 2026 audit cryptographique et CSP stricte ; 2027 multi-régions, application mobile, SSO institutionnel.

### 8:45-9:30 - Équipe et traction (diapo 11)
Équipe OBIEY-TEAM, partenaire d'hébergement Systalink Cloud, jalons livrés (8 PR, forge, ZKP, scanner, IA, tableau de bord). Ne citer que des partenariats confirmés.

### 9:30-10:00 - Appel à l'action (diapo 12)
« Nous cherchons trois institutions pilotes, deux partenaires d'hébergement et un financement d'amorçage de `[montant]`. Scannez ce code pour tester la démo et lire le code. Hébergeons le code de l'Afrique en Afrique. Merci. »

## Plan des 12 diapositives

1. Titre et accroche
2. Chiffre ou image d'accroche (dépendance du code africain)
3. Le problème (4 risques)
4. La solution en une phrase
5. Architecture (schéma Mermaid exporté)
6. Sécurité : identité sans mot de passe
7. Sécurité : audit, journal chaîné, IA locale
8. Marché et cas d'usage par pays
9. Modèle économique
10. Feuille de route
11. Équipe et traction
12. Appel à l'action et QR code

**Règles de design** : fond sombre, 1 idée par diapo, 24 pt minimum, icônes SVG du projet, pas d'emoji, contraste AA.

## Questions probables (réponses courtes)

| Question | Réponse |
|---|---|
| Pourquoi pas GitHub ou GitLab ? | Juridiction, souveraineté des données et de l'IA, coût en devises, identité sans mot de passe. Nous nous appuyons sur Gitea, sans le réinventer. |
| Le ZKP est-il sûr ? Qui l'a audité ? | Schnorr est un protocole standard (RFC 3526, hachage SHA-256) ; défis à usage unique, clés validées contre les petits sous-groupes. Pas encore d'audit externe : il est planifié et la spécification est publique. |
| Que se passe-t-il si je perds ma clé ? | Aucune récupération par mot de passe ; la phrase de 12 mots permet de la régénérer. Une récupération institutionnelle (clés multiples, révocation) est en feuille de route. |
| Quel modèle économique ? | Hébergement géré, support, conformité et formation par organisation ; instances dédiées pour les institutions. |
| Et la licence ? | Gitea est sous licence MIT ; le code de la surcouche sera publié sous une licence à confirmer avant le pitch. |
| Où sont hébergées les données ? | Sur Systalink Cloud, nœuds africains ; réseau interne pour la base de données. `[confirmer les sites réellement actifs]` |
| Comment passer à l'échelle ? | Workers Celery, cache Redis, circuit breaker, Gunicorn/Uvicorn ; tests de charge `[résultats]` avant la CADEV. |
| Conformité (Malabo, lois nationales) ? | Cartographie des données et des juridictions en cours ; journal d'audit et export SARIF facilitent la conformité. |
| Et si l'IA hallucine ? | Elle est consultative, ses sorties ne sont jamais exécutées ; l'audit déterministe reste la référence. |
| Qui gouverne le projet ? | `[à préciser : gouvernance, comité de pilotage]` |

## Check-list avant le jour J

- [ ] Mesurer et sourcer tous les chiffres entre crochets.
- [ ] Trois répétitions chronométrées dont une devant un public externe ; ramener à 9 min 30.
- [ ] Vidéo de secours de 3 min exportée localement (MP4) et testée.
- [ ] Environnement de démo hors ligne, jeu de données chargé, comptes de démonstration créés.
- [ ] Deux copies du diaporama (PDF et PPTX) sur clé USB et en ligne.
- [ ] Adaptateurs HDMI/USB-C, chargeur, télécommande de présentation.
- [ ] One-pager PDF avec QR code ; kit visuel (logo, captures).
- [ ] Salle, horaire et créneau de test technique confirmés auprès des organisateurs.
- [ ] Notifications système désactivées, mode « ne pas déranger ».
