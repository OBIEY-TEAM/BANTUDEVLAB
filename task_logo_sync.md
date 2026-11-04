# Plan d'Execution : Nouveau Logo, Charte Graphique & Synchronisation Langue / Mode d'Affichage (BantuDevLab + Gitea)

## Objectifs Principaux
1. Remplacer l'integralite du logo actuel par la nouvelle image officielle : Carte d'Afrique neon cyber avec symbole de code `</>` luminescent et orbite doree panafricaine.
2. Deriver et appliquer la charte graphique officielle inspiree du logo (Bleu neon `#0070f3`, Cyan `#00e5ff`, Orbite Or `#f59e0b`, Noir spatial `#030712`, Blanc glacier `#f8fafc`).
3. Rendre la synchronisation de la langue 100% coherente : tout le contenu et tous les onglets de BantuDevLab traduits (FR, EN, SW, PT) et synchronises avec Gitea.
4. Rendre la synchronisation du mode d'affichage (Sombre / Clair) 100% coherente et persistee entre BantuDevLab et Gitea.
5. Effectuer un commit pour chaque tache et sous-tache, puis pousser vers origin.

---

## Taches et Sous-taches

### Tache 1 : Nouveau Logo et Charte Graphique Cyber-Panafricaine
- [ ] 1.1 Traitement de l'image source, generation des formats optimises (PNG, JPG, SVG vectoriel hybride, favicons) pour BantuDevLab et Gitea.
- [ ] 1.2 Integration du nouveau logo dans les templates de BantuDevLab (base, africa_logo, navbar, vitrine, dashboard, zkp, souverainete) et de Gitea (header, login, public assets).
- [ ] 1.3 Charte graphique et tokens CSS derives du logo pour le Mode Sombre Cyber et le Mode Clair Savane sur BantuDevLab et Gitea.

### Tache 2 : Synchronisation Complete de la Langue
- [ ] 2.1 Traduction integrale (i18n) de tous les onglets et contenus de BantuDevLab (FR, EN, SW, PT) sans aucun texte fige.
- [ ] 2.2 Passerelle de synchronisation de langue bidirectionnelle entre BantuDevLab et Gitea (cookies django_language, cookie Gitea lang, API REST Gitea /api/v1/user).
- [ ] 2.3 Propagation automatique de la langue lors de la navigation et des redirections vers Gitea.

### Tache 3 : Synchronisation Complete du Mode d'Affichage (Sombre / Clair)
- [ ] 3.1 Gestionnaire de theme unifie BantuDevLab avec persistance cookie/localStorage.
- [ ] 3.2 Synchronisation du theme avec le cookie et les styles Gitea.
- [ ] 3.3 Elimination totale des defauts de transparence sur les modales et fenetres reduites.

### Tache 4 : Tests, Cloture et Push
- [ ] 4.1 Tests automatises de la synchronisation de langue, de theme et verification zero-emoji.
- [ ] 4.2 Push sur origin et validation de sante des 3 services locaux (8001, 3001, 3002).
