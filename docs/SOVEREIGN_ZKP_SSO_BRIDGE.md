# Pont d'Authentification Zero-Trust ZKP et Federation SSO (T-ADM-702)

Ce document detaille l'interconnexion entre le moteur d'identite souveraine BantuDevLab (base sur Zero-Knowledge Proof / preuve a divulgation nulle de connaissance Schnorr) et la forge Git Gitea via les protocoles standards OpenID Connect (OIDC) et OAuth2.

---

## 1. Architecture Zero-Knowledge Proof (ZKP)

Contrairement aux mecanismes conventionnels transmettant des mots de passe en clair ou hashes a travers le reseau, BantuDevLab s'appuie sur une preuve d'identite cryptographique Schnorr sur courbe ou groupe multiplicatif premier ($p, g, y = g^x \pmod p$) :

1. Le client demande un defi a usage unique (`challenge_nonce`).
2. Le client calcule un engagement $t = g^v \pmod p$, puis repond au defi avec $s = v - c \cdot x \pmod q$.
3. Le serveur verifie que $g^s \cdot y^c \equiv t \pmod p$ sans jamais connaitre la cle privee $x$.
4. Un jeton d'acces de session et OIDC est emis pour acceder a Gitea et aux services souverains.

---

## 2. Decouverte OpenID Connect (OIDC Discovery)

BantuDevLab expose le point de terminaison de decouverte standard :
`GET http://localhost:8001/.well-known/openid-configuration`

Les informations d'authentification et de profil utilisateur sont fournies par :
- Point de terminaison d'autorisation : `http://localhost:8001/api/zkp/login-ui/`
- Point de terminaison de validation / jeton : `http://localhost:8001/api/zkp/verify/`
- Point de terminaison UserInfo : `http://localhost:8001/api/zkp/userinfo/`

---

## 3. Synchronisation Automatique des Groupes et Equipes

L'attribut `groups` est transmis dans les reclamations UserInfo :
- `Sovereign African Developers`
- `Bantu Forge Members`

Dans `custom/conf/app.ini`, Gitea est configure pour reconnaitre ces scopes :
```ini
[oauth2_client]
REGISTER_EMAIL_CONFIRM = false
OPENID_CONNECT_SCOPES = openid profile email groups

[openid]
ENABLE_OPENID_SIGNIN = true
ENABLE_OPENID_SIGNUP = true
WHITELISTED_URIS = http://localhost:8001/,http://127.0.0.1:8001/
```
Gitea effectue automatiquement la correspondance entre ces groupes OIDC et les equipes d'organisation au moment de la premiere connexion ou lors des rafraichissements de jetons.
