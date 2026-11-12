# TASK 27 : ARCHITECTURE SOUVERAINE EN PRODUCTION, GITEA REEL, ZKP FLUIDE, LOGO AFRIQUE & CHARTE PRO

## Objectif
Eliminer toutes les donnees fictives du tableau de bord, connecter BantuDevLab aux donnees reelles de Gitea, rendre fonctionnel le test de latence en temps reel pour la Souverainete Numerique, fluidifier l'authentification Zero-Trust ZKP avec redirection vers l'inscription Gitea, activer la selection des langues (FR, EN, SW, PT), passer le moteur Git en production, concevoir le logo souverain Carte d'Afrique pour Gitea et BantuDevLab, concevoir la charte graphique pro clair/sombre, eliminer le bug d'arriere-plan transparent dans Gitea avec bascule dark/light, tester les endpoints de http://localhost:3002/api/swagger et mettre en place les tests CI/CD GitHub.

---

## Plan de Subdivision des Taches

### Sous-Tache T27.1 : Connexion Reelle du Tableau de Bord BantuDevLab a Gitea
- Provisionner les depots souverains reels dans Gitea via l'API REST.
- Nettoyer apps/core/views.py et apps/gitea_client/client.py pour interroger directement Gitea.
- Afficher les depots et metriques reels dans templates/core/dashboard.html.

### Sous-Tache T27.2 : Test de Latence Reseau en Temps Reel
- Implementer l'endpoint de mesure de latence reel /api/core/network-latency/.
- Remplacer les simulations aleatoires de templates/core/metrics.html par des pings asynchrones en temps reel.

### Sous-Tache T27.3 : Authentification Zero-Trust et Redirection Inscription Gitea
- Corriger la validation du nom d'utilisateur et fiabiliser la verification Schnorr NIZKP.
- Afficher une carte de redirection immediate vers http://localhost:3002/user/sign_up avec nom pre-rempli.

### Sous-Tache T27.4 : Fonctionnalite du Choix des Langues (i18n)
- Generer les catalogues de traduction locale/ pour FR, EN, SW, PT.
- Assurer le basculement dynamique et la persistance du cookie django_language.

### Sous-Tache T27.5 : Productionisation du Moteur Git Panafricain
- Supprimer toute reference a la simulation dans forge_server.py.
- Brancher les operations sur les depots Git reels et webhooks securises HMAC-SHA256.

### Sous-Tache T27.6 : Logo Carte d'Afrique Souveraine pour Gitea et BantuDevLab
- Generer le logo vectoriel SVG de la carte d'Afrique souveraine.
- L'integrer dans static/img/logo.svg et custom/public/img/logo.svg.

### Sous-Tache T27.7 : Charte Graphique Pro Sombre/Clair & Correction Transparence Gitea
- Harmoniser le Design System (sombre et clair) sur BantuDevLab et Gitea.
- Eliminer le probleme d'arriere-plan transparent / blanc sur les fenetres reduites et modales Gitea.
- Ajouter le commutateur Dark/Light directement dans la barre superieure de Gitea.

### Sous-Tache T27.8 : Audit Swagger Gitea & Tests CI/CD GitHub
- Tester les endpoints Swagger http://localhost:3002/api/swagger via pytest.
- Mettre en place le workflow GitHub CI/CD .github/workflows/gitea_swagger_ci.yml.

### Sous-Tache T27.9 : Verification Zero-Emoji, Push et Relance des Services
- Audit strict zero emoji.
- Git push vers origin/develop-jule.
- Redemarrage propre des daemons (Django 8001, Forge 3001, Gitea 3002).
