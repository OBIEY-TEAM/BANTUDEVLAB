# Hebergement de Sites Statiques Souverains (Equivalent GitHub Pages) - T-EXT-601

Ce guide decrit la publication de sites web statiques et documentations directement depuis vos depots Git BantuDevLab.

---

## 1. Fonctionnement

Tout comme GitHub Pages, le moteur Pages souverain surveille la branche `gh-pages` ou le sous-dossier `/docs` de votre depot.

A chaque push :
1. Le workflow Gitea Actions / GitHub Actions `.github/workflows/pages_deploy.yml` est declenche.
2. Le site est compile (HTML pur, Hugo, Jekyll, MkDocs, Astro).
3. L'artefact est deploye sur le serveur Nginx souverain.

---

## 2. Configuration DNS et TLS

- **URL de projet standard :** `http://<utilisateur>.pages.bantudevlab.africa/<depot>/`
- **Domaines personnalises (CNAME) :** Placez un fichier `CNAME` a la racine de la branche `gh-pages`.
- **Certificats SSL/TLS :** Generation et renouvellement automatique des certificats via Let's Encrypt / PKI souveraine.
