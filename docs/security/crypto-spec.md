# Spécification cryptographique du protocole ZKP

Implémentation : `apps/zkp_auth/crypto.py`.

## Paramètres publics

- Groupe MODP 2048 bits de la RFC 3526 (groupe 14) : `p` premier sûr, `g = 2`, `q = (p - 1) / 2`.
- Hachage : SHA-256, réduit modulo `q`.

## Clés

- Secret : `x` dans `[1, q - 2]` (aléatoire via `secrets`, ou dérivé d'une phrase).
- Public : `y = g^x mod p`.
- Validation d'une clé publique : `1 < y < p - 1` et `y^q mod p = 1` (appartenance au sous-groupe d'ordre premier `q`, anti petit sous-groupe).

## Preuve (Schnorr non interactive, Fiat-Shamir)

Prouveur, pour un message `m` (le nonce du défi) :

1. `v` aléatoire dans `[1, q - 2]`, `t = g^v mod p`.
2. `c = H(g || y || t || m) mod q`.
3. `s = (v - c * x) mod q`.
4. Preuve : `(t, s, m)`.

Vérificateur :

1. Vérifie `1 <= t < p`, `0 <= s < q`, `y` valide.
2. Recalcule `c`.
3. Accepte si `g^s * y^c mod p = t`.

## Défis et anti-rejeu

- Le nonce (256 bits aléatoires) est lié à un utilisateur, valable 5 minutes, à usage unique.
- Consommation atomique en base (`UPDATE ... WHERE is_used = false`) : une seule requête concurrente réussit.
- La vérification et l'émission de tokens Git exigent un nonce émis, valide et non utilisé.

## Tokens Git

- Format `bnt_git_` + 160 bits aléatoires ; seul le hachage SHA-256 est stocké (le token est entropique, un hachage rapide est adapté).
- Permissions : `read`, `write`, `admin`. Durée : 1 à 365 jours. Révocation par désactivation.

## Limites connues

- L'encodage du haché est une concaténation de représentations décimales/texte : un encodage à longueur préfixée est prévu (backlog T-034).
- La dérivation d'un secret depuis une phrase utilise SHA-256 : une fonction à coût mémoire (scrypt/Argon2id, T-033) est prévue.
- Pas de revue cryptographique externe à ce jour (T-036). Ne pas considérer ce module comme audité.
