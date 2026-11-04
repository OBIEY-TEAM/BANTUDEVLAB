# Plan d'Execution : Nouveau Logo, Charte Graphique & Synchronisation Universelle Tri-Ecosysteme (BantuDevLab + GitLab + Gitea)

## Objectifs Principaux
1. Remplacer l'integralite du logo actuel par la nouvelle image officielle : Carte d'Afrique neon cyber avec symbole de code `</>` luminescent et orbite doree panafricaine sur TOUS les 3 ecosystemes : BantuDevLab (8001), GitLab CE Forge (3001) et Gitea (3002).
2. Appliquer la charte graphique officielle derivee du logo (Bleu neon `#0070f3`, Cyan `#00e5ff`, Orbite Or `#f59e0b`, Noir spatial `#020617`, Blanc glacier `#f8fafc`) sur les 3 plateformes en mode sombre et clair.
3. Synchronisation Universelle Bidirectionnelle de la Langue (FR, EN, SW, PT) "VIS ET VERSA" : un changement de langue sur BantuDevLab, GitLab ou Gitea met a jour et synchronise automatiquement tous les autres.
4. Synchronisation Universelle Bidirectionnelle du Mode d'Affichage (Sombre / Clair) "VIS ET VERSA" : un changement de mode sur BantuDevLab, GitLab ou Gitea applique immediatement le theme a tous les autres sans defaut de transparence.
5. Effectuer un commit pour chaque tache et sous-tache, tester, relancer les services en local et faire le push sur origin.

---

## Taches et Sous-taches

### Tache 1 : Mise a jour de la feuille de route et du plan de synchronisation Tri-Ecosysteme
- [x] 1.1 Subdivision detaillee de la synchronisation bidirectionnelle BantuDevLab + GitLab + Gitea dans `task_logo_sync.md`.

### Tache 2 : Nouveau Logo et Charte Graphique Cyber-Panafricaine (BantuDevLab + Gitea)
- [x] 2.1 Traitement de l'image source, generation des formats optimises (PNG, JPG, SVG vectoriel hybride, favicons) pour BantuDevLab et Gitea.
- [x] 2.2 Integration du nouveau logo dans les templates de BantuDevLab et de Gitea.
- [x] 2.3 Charte graphique et tokens CSS derives du logo pour le Mode Sombre Cyber et le Mode Clair Savane sur BantuDevLab et Gitea.

### Tache 3 : Integration du Logo et de la Charte Graphique sur GitLab Forge (Port 3001)
- [x] 3.1 Integrer le logo cyber carte d'Afrique officiel (SVG/PNG/Favicon), les routes statiques (/static/img/logo.svg, /favicon.svg, /static/js/bantu-ecosystem-sync.js) et la charte graphique bicolore (Obsidian / Savane) dans `forge_server.py`.

### Tache 4 : Synchronisation Universelle de la Langue sur GitLab Forge (Port 3001)
- [x] 4.1 Ajouter le dictionnaire complet de traduction quadri-lingue (FR, EN, SW, PT) pour toutes les vues de GitLab Forge (`_render_home_ui`, `_render_gitea_ui`, `_render_repo_ui`).
- [x] 4.2 Ajouter le selecteur de langues interactif dans la barre de navigation de GitLab Forge, gerer les cookies (`bantu_lang`, `django_language`, `lang`) et l'API de synchronisation.

### Tache 5 : Synchronisation Universelle du Mode d'Affichage sur GitLab Forge (Port 3001)
- [x] 5.1 Ajouter le bouton de bascule de theme Sombre / Clair dans la barre de navigation de GitLab Forge avec bascule dynamique `[data-theme]` et cookies.

### Tache 6 : Branchement et Liaison Bidirectionnelle "Vis et Versa" sur BantuDevLab (Port 8001) et Gitea (Port 3002)
- [x] 6.1 Brancher `bantu-ecosystem-sync.js` dans `templates/base.html` de BantuDevLab pour ecouter les changements locaux et propager aux autres ports.
- [x] 6.2 Brancher `bantu-ecosystem-sync.js` dans `custom/templates/custom/header.tmpl` de Gitea (et copie dans `gitea_home/`) pour ecouter et propager les changements locaux.

### Tache 7 : Tests Automatises Tri-Ecosysteme et Validation Zero-Emoji
- [x] 7.1 Mettre a jour et executer les tests automatises de conformite du logo, de la synchronisation de langue et du mode d'affichage sur les 3 ecosystemes.
- [x] 7.2 Validation stricte de la regle zero-emoji.

### Tache 8 : Cloture, Relance des Processus et Push Git
- [ ] 8.1 Arreter et relancer les 3 processus locaux (Django sur 8001, GitLab Forge sur 3001, Gitea sur 3002).
- [ ] 8.2 Valider la reponse HTTP 200 sur les 3 plateformes.
- [ ] 8.3 Git push vers origin sur develop-jule et design-figma.
