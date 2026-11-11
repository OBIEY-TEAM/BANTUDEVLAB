# FICHE OFFICIELLE DE SOUMISSION — CONCOURS CADEV 2026 (SYSTALINK)

**Projet :** BANTUDEVLAB — Forge Logicielle Souveraine Panafricaine  
**Équipe candidate :** Équipe CYBERSOCLE (Christ Dany Obiey et membres de l'équipe CYBERSOCLE)  
**Événement :** Concours CADEV 2026 — Systalink Cloud  
**Date limite de soumission :** 15 novembre 2026, 23h59 GMT (heure de Dakar)  
**URL de production :** https://cybersocle.site (Portail Central & API) / https://git.cybersocle.site (Forge Gitea CE)  
**Dépôt source :** https://github.com/OBIEY-TEAM/BANTUDEVLAB  

---

## a) Présentation du Projet et du Sujet Traité

### Contexte & Problématique
L'Afrique subit une dépendance numérique critique vis-à-vis des plateformes étrangères de développement et d'hébergement de code source (GitHub, GitLab.com). Cette dépendance expose les données stratégiques des États, des banques centrales, des universités et des startups africaines aux lois extraterritoriales (ex. US Cloud Act, FISA), aux risques de coupures unilatérales et aux fuites de secrets vers des modèles d'IA tiers hébergés hors du continent.

### Solution Apportée : BANTUDEVLAB
BANTUDEVLAB est une forge logicielle panafricaine souveraine d'échange de code, conçue « par les développeurs, pour les développeurs », alliant :
1. **Un moteur Git distribué et léger** s'appuyant sur Gitea CE et une passerelle multi-forges.
2. **Une authentification Zero-Trust sans mot de passe** fondée sur les preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs - protocole de Schnorr non-interactif via Fiat-Shamir sur groupe RFC 3526 MODP 2048 bits).
3. **Un scanner d'analyse statique SAST intégré** calculant en continu un score de souveraineté numérique (0 à 100%) avec calcul d'entropie de Shannon ($H \ge 3.8$) et export aux normes standard OASIS SARIF 2.1.0 et GitLab SAST (`gl-sast-report.json`).
4. **Un assistant d'ingénierie logicielle IA local (Gemma 2 2B)** exécuté sur conteneur d'inférence Ollama au sein de l'infrastructure sans transfert de données vers l'extérieur.
5. **Une expérience utilisateur moderne multi-écrans** intégrant un terminal de commande pro sans saisie libre, un éditeur CodeMirror et la synchronisation en 4 langues (Français, Anglais, Kiswahili, Portugais).

---

## b) Déclaration de Titularité des Droits

Les soussignés, membres de l'équipe candidate **CYBERSOCLE**, déclarent sur l'honneur que le projet BantuDevLab a été entièrement conçu, développé et réalisé à titre personnel et indépendant, **hors de toute mission, contrat de travail, mandat ou commande émanant d'un employeur, client ou établissement d'enseignement**. L'ensemble des droits de propriété intellectuelle afférents au projet appartient exclusivement aux membres de l'équipe CYBERSOCLE sous licence permissive MIT.

### Tableau d'engagement et de confirmation par les membres de l'équipe CYBERSOCLE :

| Nom et Prénom | Rôle dans le projet | Statut d'indépendance | Signature / Confirmation | Date |
| :--- | :--- | :--- | :--- | :--- |
| **Christ Dany Obiey** | Porteur de projet & Lead Dev | [À compléter et confirmer par le membre] | [Signature / Mention « Lu et approuvé »] | [Date] |
| **[Membre 2 - Nom Prénom]** | [Rôle : Cryptographie / Backend] | [À compléter et confirmer par chaque membre] | [Signature / Mention « Lu et approuvé »] | [Date] |
| **[Membre 3 - Nom Prénom]** | [Rôle : Infrastructure / DevOps] | [À compléter et confirmer par chaque membre] | [Signature / Mention « Lu et approuvé »] | [Date] |
| **[Membre 4 - Nom Prénom]** | [Rôle : Frontend / QA / Sécurité] | [À compléter et confirmer par chaque membre] | [Signature / Mention « Lu et approuvé »] | [Date] |

---

## c) Composants Tiers et Licences Associées

Conformément au règlement de la CADEV 2026, l'inventaire exhaustif des composants tiers utilisés dans le projet, de leurs versions et de leurs licences est reproduit ci-après :

### 1. Composants d'Infrastructure et Frontend

| Composant | Version | Licence Détectée | Rôle / Usage | Statut CADEV 2026 | Notes & Plan de Remplacement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Valkey (remplacement de Redis)** | `7.2.7-alpine` | BSD-3-Clause | Infrastructure / Cache & Broker | **OK (Permissif)** | Drop-in replacement 100% compatible Redis fork Linux Foundation sous licence BSD-3-Clause. Remplace Redis >= 7.4 qui n'est plus BSD. |
| **Redis (version antérieure)** | `7-alpine (>= 7.4)` | RSALv2 / SSPLv1 (Non BSD depuis 7.4) | Infrastructure / Cache & Broker | **À remplacer (Bloquant CADEV)** | Depuis Redis 7.4, Redis n'est plus distribué sous licence BSD libre. Remplacé sans risque par Valkey 7.2 (BSD-3-Clause). |
| **Gitea CE** | `1.22` | MIT License | Forge Git Principale | **OK (Permissif)** | Forge Git distribuée légère sous licence permissive MIT. |
| **GitLab CE (Omnibus)** | `16.11.0-ce.0` | MIT License (GitLab CE) | Forge Git Secondaire / Fédérée | **OK (Permissif)** | L'édition Community Edition (CE / FOSS) est sous licence MIT. |
| **PostgreSQL** | `16-alpine` | PostgreSQL License | Base de données | **OK (Permissif)** | Licence permissive approuvée OSI (équivalente BSD / MIT). |
| **PgBouncer** | `latest (edoburu/pgbouncer)` | BSD-2-Clause | Pooler de connexions PostgreSQL | **OK (Permissif)** | Licence permissive BSD 2-Clause. |
| **Nginx** | `1.27-alpine` | 2-Clause BSD License | Reverse Proxy & TLS 1.3 Gateway | **OK (Permissif)** | Licence permissive 2-Clause BSD. |
| **Ollama (moteur d'inférence)** | `latest` | MIT License | Serveur d'inférence IA locale | **OK (Permissif)** | Le logiciel Ollama est distribué sous licence MIT permissive. |
| **Gemma 2 2B (modèle IA Google)** | `2B-IT (quantifié Q4_K_M)` | Gemma Terms of Use (Google) | Modèle de poids d'IA | **À vérifier / Conforme aux CGU (Non redistribué)** | Exécuté localement sans redistribution. Non qualifié de permissif (conditions d'utilisation spécifiques Google). Non bloquant car exécuté localement comme un modèle tiers. |
| **CodeMirror 5** | `5.65.16` | MIT License | Composant Frontend / Éditeur de code | **OK (Permissif)** | Auto-hébergé dans `static/vendor/codemirror/` sous licence MIT (Marijn Haverbeke). |

### 2. Dépendances Python (Directes et Transitives)

| Paquet Python | Version | Licence Déclarée | Statut CADEV 2026 | Site Officiel / Référentiel | Remarques |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **amqp** | `5.4.1` | BSD License | **OK (Permissif)** | [amqp](http://github.com/celery/py-amqp) | Licence libre permissive conforme au règlement CADEV 2026. |
| **asgiref** | `3.13.0` | BSD-3-Clause | **OK (Permissif)** | [asgiref](https://github.com/django/asgiref/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **attrs** | `26.1.0` | MIT | **OK (Permissif)** | [attrs](https://www.attrs.org/en/stable/changelog.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **bandit** | `1.9.4` | Apache-2.0 | **OK (Permissif)** | [bandit](https://bandit.readthedocs.io/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **billiard** | `4.3.1` | BSD License | **OK (Permissif)** | [billiard](https://github.com/celery/billiard) | Licence libre permissive conforme au règlement CADEV 2026. |
| **celery** | `5.6.3` | BSD-3-Clause | **OK (Permissif)** | [celery](https://docs.celeryq.dev/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **certifi** | `2026.10.23` | Mozilla Public License 2.0 (MPL 2.0) | **À vérifier (Weak Copyleft)** | [certifi](https://github.com/certifi/python-certifi) | Mozilla Public License 2.0. Autorise l'intégration sans contamination si utilisé sous forme de bibliothèque dynamique sans modification. |
| **cffi** | `2.1.1` | MIT-0 | **OK (Permissif)** | [cffi](https://cffi.readthedocs.io/en/latest/whatsnew.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **charset-normalizer** | `3.5.2` | MIT | **OK (Permissif)** | [charset-normalizer](https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click** | `8.5.0` | BSD-3-Clause | **OK (Permissif)** | [click](https://github.com/pallets/click/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-didyoumean** | `0.3.1` | MIT License | **OK (Permissif)** | [click-didyoumean](https://github.com/click-contrib/click-didyoumean) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-plugins** | `1.1.1.2` | BSD License | **OK (Permissif)** | [click-plugins](https://github.com/click-contrib/click-plugins) | Licence libre permissive conforme au règlement CADEV 2026. |
| **click-repl** | `0.4.1` | MIT | **OK (Permissif)** | [click-repl](https://github.com/click-contrib/click-repl) | Licence libre permissive conforme au règlement CADEV 2026. |
| **colorama** | `0.4.6` | BSD License | **OK (Permissif)** | [colorama](https://github.com/tartley/colorama) | Licence libre permissive conforme au règlement CADEV 2026. |
| **coverage** | `7.17.0` | Apache-2.0 | **OK (Permissif)** | [coverage](https://github.com/coveragepy/coveragepy) | Licence libre permissive conforme au règlement CADEV 2026. |
| **cryptography** | `50.0.2` | Apache-2.0 OR BSD-3-Clause | **OK (Permissif)** | [cryptography](https://github.com/pyca/cryptography) | Licence libre permissive conforme au règlement CADEV 2026. |
| **Django** | `5.2.18` | BSD-3-Clause | **OK (Permissif)** | [Django](https://www.djangoproject.com/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **djangorestframework** | `3.18.3` | BSD-3-Clause | **OK (Permissif)** | [djangorestframework](https://www.django-rest-framework.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **drf-spectacular** | `0.30.0` | BSD-3-Clause | **OK (Permissif)** | [drf-spectacular](https://github.com/tfranzel/drf-spectacular) | Licence libre permissive conforme au règlement CADEV 2026. |
| **greenlet** | `3.5.6` | MIT AND PSF-2.0 | **OK (Permissif)** | [greenlet](https://greenlet.readthedocs.io) | Licence libre permissive conforme au règlement CADEV 2026. |
| **gunicorn** | `26.2.0` | MIT | **OK (Permissif)** | [gunicorn](https://gunicorn.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **h11** | `0.16.0` | MIT License | **OK (Permissif)** | [h11](https://github.com/python-hyper/h11) | Licence libre permissive conforme au règlement CADEV 2026. |
| **idna** | `3.20` | BSD-3-Clause | **OK (Permissif)** | [idna](https://github.com/kjd/idna) | Licence libre permissive conforme au règlement CADEV 2026. |
| **inflection** | `0.5.1` | MIT License | **OK (Permissif)** | [inflection](https://github.com/jpvanhal/inflection) | Licence libre permissive conforme au règlement CADEV 2026. |
| **iniconfig** | `2.3.1` | MIT | **OK (Permissif)** | [iniconfig](https://github.com/pytest-dev/iniconfig) | Licence libre permissive conforme au règlement CADEV 2026. |
| **jsonschema** | `4.26.0` | MIT | **OK (Permissif)** | [jsonschema](https://github.com/python-jsonschema/jsonschema) | Licence libre permissive conforme au règlement CADEV 2026. |
| **jsonschema-specifications** | `2025.9.1` | MIT | **OK (Permissif)** | [jsonschema-specifications](https://github.com/python-jsonschema/jsonschema-specifications) | Licence libre permissive conforme au règlement CADEV 2026. |
| **kombu** | `5.6.2` | BSD-3-Clause | **OK (Permissif)** | [kombu](https://kombu.readthedocs.io) | Licence libre permissive conforme au règlement CADEV 2026. |
| **markdown-it-py** | `4.2.0` | MIT License | **OK (Permissif)** | [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | Licence libre permissive conforme au règlement CADEV 2026. |
| **mdurl** | `0.1.2` | MIT License | **OK (Permissif)** | [mdurl](https://github.com/executablebooks/mdurl) | Licence libre permissive conforme au règlement CADEV 2026. |
| **packaging** | `26.3` | Apache-2.0 OR BSD-2-Clause | **OK (Permissif)** | [packaging](https://github.com/pypa/packaging) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pillow** | `13.0.0` | MIT-CMU | **OK (Permissif)** | [pillow](https://python-pillow.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pip** | `25.2` | MIT | **OK (Permissif)** | [pip](https://pip.pypa.io) | Outil de gestion des paquets Python sous licence libre MIT. |
| **pip-licenses** | `5.5.5` | MIT | **OK (Permissif)** | [pip-licenses](https://github.com/raimon49/pip-licenses) | Outil d'audit des licences logicielles sous licence libre MIT. |
| **playwright** | `1.64.1` | Apache-2.0 | **OK (Permissif)** | [playwright](https://github.com/Microsoft/playwright-python) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pluggy** | `1.7.0` | MIT License | **OK (Permissif)** | [pluggy](https://github.com/pytest-dev/pluggy) | Licence libre permissive conforme au règlement CADEV 2026. |
| **prettytable** | `3.18.0` | BSD-3-Clause | **OK (Permissif)** | [prettytable](https://github.com/jazzband/prettytable) | Affichage tabulaire sous licence libre BSD-3-Clause. |
| **prompt_toolkit** | `3.0.53` | BSD License | **OK (Permissif)** | [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) | Licence libre permissive conforme au règlement CADEV 2026. |
| **psycopg2-binary** | `2.9.13` | LGPL-3.0-or-later with exceptions | **À remplacer (Bloquant CADEV)** | [psycopg2-binary](https://psycopg.org/) | Pilote PostgreSQL officiel sous licence LGPLv3. Django dépend de psycopg2/psycopg3 (tous deux LGPL). Remplacement permissif proposé : pg8000 (BSD-3-Clause) ou SQLite (Public Domain). |
| **pycparser** | `3.12` | BSD-3-Clause | **OK (Permissif)** | [pycparser](https://github.com/eliben/pycparser) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pyee** | `14.0.0` | MIT License | **OK (Permissif)** | [pyee](https://github.com/jfhbrook/pyee) | Licence libre permissive conforme au règlement CADEV 2026. |
| **Pygments** | `2.21.0` | BSD-2-Clause | **OK (Permissif)** | [Pygments](https://pygments.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest** | `9.2.0` | MIT | **OK (Permissif)** | [pytest](https://docs.pytest.org/en/latest/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest-cov** | `7.1.0` | MIT | **OK (Permissif)** | [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/changelog.html) | Licence libre permissive conforme au règlement CADEV 2026. |
| **pytest-django** | `4.14.0` | BSD License | **OK (Permissif)** | [pytest-django](https://github.com/pytest-dev/pytest-django) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-dateutil** | `4.0.0` | BSD-3-Clause | **OK (Permissif)** | [python-dateutil](https://github.com/dateutil/dateutil) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-dotenv** | `1.2.4` | BSD-3-Clause | **OK (Permissif)** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Licence libre permissive conforme au règlement CADEV 2026. |
| **python-gitlab** | `8.6.0` | LGPL-3.0-or-later | **À remplacer (Bloquant CADEV)** | [python-gitlab](https://github.com/python-gitlab/python-gitlab) | SDK d'intégration GitLab API v4 sous licence LGPLv3. Remplacement permissif sans risque proposé : appels HTTP directs via 'requests' (Apache 2.0). |
| **PyYAML** | `6.0.3` | MIT License | **OK (Permissif)** | [PyYAML](https://pyyaml.org/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **redis** | `8.1.0` | MIT | **OK (Permissif)** | [redis](https://github.com/redis/redis-py) | Bibliothèque cliente Python sous licence MIT. Le serveur Redis >= 7.4 (non-BSD) a été remplacé par Valkey 7.2 (BSD-3). |
| **referencing** | `0.37.0` | MIT | **OK (Permissif)** | [referencing](https://github.com/python-jsonschema/referencing) | Licence libre permissive conforme au règlement CADEV 2026. |
| **requests** | `2.34.2` | Apache Software License | **OK (Permissif)** | [requests](https://github.com/psf/requests) | Licence libre permissive conforme au règlement CADEV 2026. |
| **requests-toolbelt** | `1.0.0` | Apache Software License | **OK (Permissif)** | [requests-toolbelt](https://toolbelt.readthedocs.io/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **rich** | `15.0.0` | MIT License | **OK (Permissif)** | [rich](https://github.com/Textualize/rich) | Licence libre permissive conforme au règlement CADEV 2026. |
| **rpds-py** | `2026.9.1` | MIT | **OK (Permissif)** | [rpds-py](https://github.com/crate-py/rpds) | Licence libre permissive conforme au règlement CADEV 2026. |
| **ruff** | `0.17.3` | MIT | **OK (Permissif)** | [ruff](https://docs.astral.sh/ruff) | Licence libre permissive conforme au règlement CADEV 2026. |
| **sqlparse** | `0.6.1` | BSD License | **OK (Permissif)** | [sqlparse](https://github.com/andialbrecht/sqlparse) | Licence libre permissive conforme au règlement CADEV 2026. |
| **stevedore** | `5.9.1` | Apache-2.0 | **OK (Permissif)** | [stevedore](https://docs.openstack.org/stevedore) | Licence libre permissive conforme au règlement CADEV 2026. |
| **typing_extensions** | `4.16.0` | PSF-2.0 | **OK (Permissif)** | [typing_extensions](https://github.com/python/typing_extensions) | Licence libre permissive conforme au règlement CADEV 2026. |
| **tzdata** | `2026.6` | Apache-2.0 | **OK (Permissif)** | [tzdata](https://github.com/python/tzdata) | Licence libre permissive conforme au règlement CADEV 2026. |
| **tzlocal** | `5.4.5` | MIT | **OK (Permissif)** | [tzlocal](https://github.com/regebro/tzlocal/blob/master/CHANGES.txt) | Licence libre permissive conforme au règlement CADEV 2026. |
| **uritemplate** | `4.2.0` | BSD 3-Clause OR Apache-2.0 | **OK (Permissif)** | [uritemplate](https://uritemplate.readthedocs.org) | Licence libre permissive conforme au règlement CADEV 2026. |
| **urllib3** | `2.8.0` | MIT | **OK (Permissif)** | [urllib3](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) | Licence libre permissive conforme au règlement CADEV 2026. |
| **uvicorn** | `0.54.0` | BSD-3-Clause | **OK (Permissif)** | [uvicorn](https://uvicorn.dev/) | Licence libre permissive conforme au règlement CADEV 2026. |
| **vine** | `5.1.0` | BSD License | **OK (Permissif)** | [vine](https://github.com/celery/vine) | Licence libre permissive conforme au règlement CADEV 2026. |
| **wcwidth** | `0.9.4` | MIT | **OK (Permissif)** | [wcwidth](https://github.com/jquast/wcwidth) | Calcul de largeur de caractères sous licence libre MIT. |

---

## d) Déclaration sur l'Usage de l'Intelligence Artificielle

### 1. Modèle d'Inférence Embarqué dans le Produit (Gemma 2 2B)
- **Modèle :** Google Gemma 2 2B Instruct (`gemma2:2b`), quantifié en 4-bit (GGUF Q4_K_M).
- **Moteur d'exécution :** Ollama (logiciel sous licence MIT).
- **Statut de licence :** Le modèle Gemma est régi par les **Gemma Terms of Use de Google** (conditions d'utilisation et politique d'usage responsable). **Il n'est pas qualifié de licence permissive.**
- **Modalité d'exécution :** Le modèle est exécuté **strictement en local** sur le serveur d'hébergement. Aucune donnée utilisateur, aucun extrait de code source ni métadonnée n'est transmis à Google ni à aucun tiers externe. Les poids du modèle ne sont pas redistribués dans le dépôt Git de BantuDevLab.
- **Rôle applicatif :** Revue automatique de sécurité de code (analyse SAST souveraine, explications pédagogiques de failles, résumé de Pull Requests).

### 2. Outils d'Aide au Développement Utilisés par l'Équipe
- **Outils utilisés :** Assistants IA de complétion de code et d'aide à la conception (Claude Code, Antigravity AI, GitHub Copilot).
- **Parties du projet concernées :** Génération des stubs de tests unitaires, factorisation des structures CSS responsives, documentation technique et matrices de conformité.
- **Maîtrise du code :** L'équipe CYBERSOCLE certifie avoir relu, testé, débogué et validé l'intégralité du code livré. L'équipe maîtrise 100% de la logique métier, de l'implémentation cryptographique ZKP Schnorr, des algorithmes de calcul d'entropie Shannon et des contrôles d'accès multi-tenants.

---

## e) Architecture de Déploiement et Services Systalink / Datacloud

### 1. Architecture Réseau et Hébergement
- **Noms de domaine de production :** `cybersocle.site` et `git.cybersocle.site`.
- **Achat du domaine :** Domaine acheté via l'infrastructure partenaire Systalink / Datacloud.
- **Serveur d'hébergement :** Serveur Privé Virtuel (VPS Hostinger sous Ubuntu 24.04 LTS), assurant l'exécution des conteneurs durcis Docker (Django, Gitea CE, Valkey, PostgreSQL, Ollama, Nginx TLS 1.3).

### 2. Traçabilité des Commandes Datacloud (À compléter par l'équipe CYBERSOCLE) :
- **Identifiant / Compte client Datacloud :** `[À compléter : identifiant client Datacloud]`
- **Numéro de référence de commande du domaine / service :** `[À compléter : Référence de commande Datacloud / Systalink]`
- **Date de souscription :** `[À compléter : Date exacte d'achat]`
- **Usage effectif du service Datacloud :** Résolution DNS souveraine, enregistrements de zone A/CNAME pointant vers le cluster de la forge, et passerelle de messagerie.

---

## f) Historique de Développement : Ce qui a été créé par l'Équipe CYBERSOCLE vs Composants Existants

### 1. Chronologie Réelle issue de l'Historique Git
- **Date du premier commit :** 31 octobre 2026 (`b0fa102ec01065d0b9a788363b3d4c03b2f99535`).
- **Période active de développement :** 31 octobre 2026 au 12 novembre 2026.
- **Volume d'historique :** 257 commits structurés et audités documentant chaque étape d'implémentation.

### 2. Ce qui provient de Composants Tiers Éprouvés (Open-Source)
- **Framework Web :** Django 5.2 & Django REST Framework (licence BSD-3-Clause).
- **Forge Git Engine :** Gitea CE 1.22 (licence MIT) avec intégration via API REST v1 et webhooks.
- **Serveur HTTP / Reverse Proxy :** Nginx 1.27-alpine (licence 2-Clause BSD) avec terminaison TLS 1.3.
- **Cache & Broker :** Valkey 7.2-alpine (licence BSD-3-Clause, fork Linux Foundation sous gouvernance ouverte).
- **Base de Données :** PostgreSQL 16-alpine (licence PostgreSQL).
- **Moteur d'Inférence :** Ollama (licence MIT).
- **Éditeur de Code Web :** CodeMirror 5 (licence MIT).

### 3. Ce qui a été Entièrement Créé et Développé par l'Équipe CYBERSOCLE
- **Moteur Cryptographique Zero-Trust ZKP (`apps/zkp_auth/crypto.py`) :** Implémentation complète de Schnorr NIZKP (RFC 3526 MODP 2048-bit, challenge Fiat-Shamir, validation stricte du sous-groupe premier $y^q \equiv 1 \pmod p$, génération BIP-39 12 mots, nonces atomiques avec protection anti-rejeu et génération de jetons CLI Git signés).
- **Scanner SAST & Moteur de Souveraineté (`apps/security_scanner/engine.py`) :** Détection de secrets par calcul d'entropie de Shannon ($H \ge 3.8$), détection de patterns de vulnérabilités multi-langages (Python, Dockerfile, YAML, JavaScript), calcul du score de souveraineté numérique africaine (ADSS-v1) et sérialisation conforme OASIS SARIF 2.1.0 et `gl-sast-report.json`.
- **Terminal de Commande Prompt Pro (`static/js/bantu-command-terminal.js`) :** Interface interactive sans zone de texte libre, avec navigation structurée par sélecteurs (+, Dépôt, Branche, Fichier, Exécuter) et panneau de restitution Top-Up.
- **Surcouche d'Intégration et Synchronisation d'Écosystème (`static/js/bantu-ecosystem-sync.js`) :** Synchronisation bidirectionnelle instantanée de thèmes et de langues (FR, EN, SW, PT) entre le portail Django et la forge Gitea.
- **Modèle de Données et Audit Trail Conforme Convention de Malabo 2014 (`apps/core/audit.py`) :** Journal d'audit immuable avec chaînage cryptographique SHA-256 (`previous_hash -> hash`).
- **Ensemble des Templates, Thèmes et Composants Graphiques :** Intégration sur-mesure Primer, suppression totale des emojis au profit de pictogrammes SVG accessibles, et jauge vectorielle circulaire de souveraineté.
