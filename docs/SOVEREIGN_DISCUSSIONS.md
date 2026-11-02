# Espace de Discussions Communautaires Souveraines (Equivalent GitHub Discussions) - T-EXT-604

Ce document detaille l'architecture et la mise en oeuvre de l'equivalent souverain a **GitHub Discussions** pour BantuDevLab et Gitea.

---

## 1. Approche Native integree a Gitea

Gitea ne possede pas d'onglet "Discussions" separe par defaut, mais permet une experience equivalente et fluide grace a :

1. **Formulaire d'Issue Form YAML Dedie** :
   - Fichiers `.gitea/ISSUE_TEMPLATE/discussion.yaml` et `.github/ISSUE_TEMPLATE/discussion.yaml`.
   - Etiquetage automatique sous le label `type/discussion` et `status/community`.
   - Classification par categories : Idees & Propositions, Questions & Entraide, Architecture RFC, Annonces.

2. **Filtres et Vues Personnalisees** :
   - Les discussions sont consultables directement dans la liste des tickets avec le filtre `label:type/discussion`.
   - Elles ne polluent pas les anomalies (`kind/bug`) et les evolutions (`kind/feature`).

---

## 2. Solution Etendue : Instance Discourse Auto-Hebergee

Pour les organisations souhaitant une experience de forum riche identique ou superieure a GitHub Discussions :

### Interconnexion OAuth2 / OIDC avec Gitea

Gitea agit comme fournisseur d'identite OAuth2 :

```yaml
# Configuration Discourse OAuth2 (discourse-oauth2-basic)
DISCOURSE_OAUTH2_ENABLED: true
DISCOURSE_OAUTH2_CLIENT_ID: <GITEA_CLIENT_ID>
DISCOURSE_OAUTH2_CLIENT_SECRET: <GITEA_CLIENT_SECRET>
DISCOURSE_OAUTH2_AUTHORIZE_URL: "http://localhost:3002/login/oauth/authorize"
DISCOURSE_OAUTH2_TOKEN_URL: "http://localhost:3002/login/oauth/access_token"
DISCOURSE_OAUTH2_USER_JSON_URL: "http://localhost:3002/api/v1/user"
```

---

## 3. Categories de Discussions

| Categorie | Usage |
|---|---|
| Idees & Propositions | Nouvelles fonctionnalites et ameliorations de la forge |
| Questions & Entraide | Support technique et assistance a l'usage de la plateforme |
| Architecture & Securite | RFCs d'architecture zero-trust, cryptographie post-quantique |
| Annonces | Nouveautes, versions de releases et retours d'experience |
