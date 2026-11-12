# -*- coding: utf-8 -*-
"""
Script maître : master_sync_translations.py
1. Scanne templates/ pour extraire tous les {% trans %}
2. Génère / met à jour les catalogues PO pour EN, SW, PT, FR avec les msgids exacts
3. Compile les fichiers MO correspondants
"""

import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
from compile_po import compile_po_to_mo  # noqa: E402

# Dictionnaire de correspondances / dictionnaires pour la traduction automatique
# Clé normalisée (sans accents, minuscules, espaces condensés) -> {en, sw, pt, fr}
NORM_DICT = {
    # FAQ & Général
    "guide & faq": {"en": "Documentation & FAQ", "sw": "Mwongozo na Maswali", "pt": "Guia & FAQ", "fr": "Guide & FAQ"},
    "tableau de bord souverain bantudevlab": {
        "en": "BANTUDEVLAB Sovereign Dashboard",
        "sw": "Dashibodi Huru ya BANTUDEVLAB",
        "pt": "Painel de Controle Soberano BANTUDEVLAB",
        "fr": "Tableau de Bord Souverain BANTUDEVLAB",
    },
    "« connexion avec bantu zkp »": {
        "en": '"Login with Bantu ZKP"',
        "sw": '"Ingia na Bantu ZKP"',
        "pt": "« Iniciar sessão com Bantu ZKP »",
        "fr": "« Connexion avec Bantu ZKP »",
    },
    "acces direct gitea :": {
        "en": "Direct Gitea access:",
        "sw": "Ufikiaji wa moja kwa moja wa Gitea:",
        "pt": "Acesso direto Gitea :",
        "fr": "Accès direct Gitea :",
    },
    "chemin de connexion direct aux depots git :": {
        "en": "Direct login path to Git repositories:",
        "sw": "Njia ya moja kwa moja ya kuingia kwenye hazina za Git:",
        "pt": "Caminho de ligação direta aos repositórios Git :",
        "fr": "Chemin de connexion direct aux dépôts Git :",
    },
    "guide d'utilisation & faq souveraine - bantudevlab": {
        "en": "User Guide & Sovereign FAQ - BANTUDEVLAB",
        "sw": "Mwongozo wa Mtumiaji & Maswali ya Enzi - BANTUDEVLAB",
        "pt": "Guia de Utilização & FAQ Soberana - BANTUDEVLAB",
        "fr": "Guide d'Utilisation & FAQ Souveraine - BANTUDEVLAB",
    },
    "guide d'utilisation & foire aux questions": {
        "en": "User Guide & Frequently Asked Questions",
        "sw": "Mwongozo wa Mtumiaji & Maswali Yanayoulizwa Mara kwa Mara",
        "pt": "Guia de Utilização & Perguntas Frequentes",
        "fr": "Guide d'Utilisation & Foire Aux Questions",
    },
    "accueil": {"en": "Home", "sw": "Nyumbani", "pt": "Início", "fr": "Accueil"},
    "tableau de bord": {"en": "Dashboard", "sw": "Dashibodi", "pt": "Painel", "fr": "Tableau de Bord"},
    "acceder au tableau de bord": {
        "en": "Go to Dashboard",
        "sw": "Nenda Dashibodi",
        "pt": "Ir ao Painel",
        "fr": "Accéder au Tableau de Bord",
    },
    "retrouvez l'ensemble des reponses techniques pour exploiter la forge souveraine bantudevlab et son integration gitlab ce/ee : creation de compte, connexion zero-trust, consultation du code source et collaboration securisee.": {
        "en": "Find all technical answers for using the BANTUDEVLAB sovereign forge and its GitLab CE/EE integration: account creation, Zero-Trust login, source code browsing and secure collaboration.",
        "sw": "Pata majibu yote ya kiufundi ya kutumia jukwaa huru la BANTUDEVLAB na muunganiko wake wa GitLab CE/EE: uundaji wa akaunti, kuingia Zero-Trust, kuvinjari msimbo chanzo na ushirikiano salama.",
        "pt": "Encontre todas as respostas técnicas para usar a forge soberana BANTUDEVLAB e a sua integração GitLab CE/EE: criação de conta, login Zero-Trust, consulta de código fonte e colaboração segura.",
        "fr": "Retrouvez l'ensemble des réponses techniques pour exploiter la forge souveraine BANTUDEVLAB et son intégration GitLab CE/EE : création de compte, connexion Zero-Trust, consultation du code source et collaboration sécurisée.",
    },
    "rechercher une question, mot-cle (ex: git, zkp, token, clone, merge request)...": {
        "en": "Search a question or keyword (e.g.: Git, ZKP, token, clone, merge request)...",
        "sw": "Tafuta swali au neno muhimu (mf: Git, ZKP, token, clone, merge request)...",
        "pt": "Pesquisar questão ou palavra-chave (ex: Git, ZKP, token, clone, merge request)...",
        "fr": "Rechercher une question, mot-clé (ex: Git, ZKP, token, clone, merge request)...",
    },
    "rechercher dans la faq": {
        "en": "Search the FAQ",
        "sw": "Tafuta katika Maswali",
        "pt": "Pesquisar na FAQ",
        "fr": "Rechercher dans la FAQ",
    },
    "mode d'utilisation fondamental : gitlab & bantudevlab": {
        "en": "Fundamental Usage Mode: GitLab & BantuDevLab",
        "sw": "Hali ya Matumizi ya Msingi: GitLab & BantuDevLab",
        "pt": "Modo de Utilização Fundamental: GitLab & BantuDevLab",
        "fr": "Mode d'Utilisation Fondamental : GitLab & BantuDevLab",
    },
    "les trois etapes indispensables pour initialiser votre environnement de travail souverain.": {
        "en": "The three essential steps to initialize your sovereign work environment.",
        "sw": "Hatua tatu muhimu za kuanzisha mazingira yako ya kazi huru.",
        "pt": "Os três passos essenciais para inicializar o seu ambiente de trabalho soberano.",
        "fr": "Les trois étapes indispensables pour initialiser votre environnement de travail souverain.",
    },
    "comment creer un compte gitlab sur la plateforme souveraine ?": {
        "en": "How to create a GitLab account on the sovereign platform?",
        "sw": "Jinsi ya kuunda akaunti ya GitLab kwenye jukwaa huru?",
        "pt": "Como criar uma conta GitLab na plataforma soberana?",
        "fr": "Comment créer un compte GitLab sur la plateforme souveraine ?",
    },
    "sur la plateforme souveraine bantudevlab, l'acces a gitlab ce est unifie avec votre identite cryptographique zero-trust. vous avez deux methodes pour creer votre compte :": {
        "en": "On the BANTUDEVLAB sovereign platform, access to GitLab CE is unified with your Zero-Trust cryptographic identity. You have two methods to create your account:",
        "sw": "Kwenye jukwaa huru la BANTUDEVLAB, ufikiaji wa GitLab CE umeunganishwa na utambulisho wako wa kriptografia wa Zero-Trust. Una njia mbili za kuunda akaunti yako:",
        "pt": "Na plataforma soberana BANTUDEVLAB, o acesso ao GitLab CE é unificado com a sua identidade criptográfica Zero-Trust. Tem dois métodos para criar a sua conta:",
        "fr": "Sur la plateforme souveraine BANTUDEVLAB, l'accès à GitLab CE est unifié avec votre identité cryptographique Zero-Trust. Vous avez deux méthodes pour créer votre compte :",
    },
    "methode 1 : inscription cryptographique via bantudevlab (recommandee)": {
        "en": "Method 1: Cryptographic registration via BantuDevLab (Recommended)",
        "sw": "Njia 1: Usajili wa kriptografia kupitia BantuDevLab (Inashauriwa)",
        "pt": "Método 1: Registo criptográfico via BantuDevLab (Recomendado)",
        "fr": "Méthode 1 : Inscription cryptographique via BantuDevLab (Recommandée)",
    },
    "rendez-vous sur l'onglet": {
        "en": "Go to the tab",
        "sw": "Nenda kwenye kichupo cha",
        "pt": "Vá ao separador",
        "fr": "Rendez-vous sur l'onglet",
    },
    "connexion zero-trust": {
        "en": "Zero-Trust Login",
        "sw": "Kuingia Zero-Trust",
        "pt": "Login Zero-Trust",
        "fr": "Connexion Zero-Trust",
    },
    "basculez sur l'onglet « inscription souveraine » de l'assistant interactif.": {
        "en": "Switch to the 'Sovereign Registration' tab of the interactive assistant.",
        "sw": "Badilisha kwenye kichupo cha 'Usajili Huru' cha msaidizi wa maingiliano.",
        "pt": "Mude para o separador 'Registo Soberano' do assistente interativo.",
        "fr": "Basculez sur l'onglet « Inscription Souveraine » de l'assistant interactif.",
    },
    "choisissez votre identifiant developpeur et selectionnez votre pays souverain d'attachement (ex: cote d'ivoire, senegal, kenya, nigeria).": {
        "en": "Choose your developer username and select your sovereign country of affiliation (e.g.: Ivory Coast, Senegal, Kenya, Nigeria).",
        "sw": "Chagua jina lako la mtumiaji la msanidi na uchague nchi yako huru (mf: Ivory Coast, Senegal, Kenya, Nigeria).",
        "pt": "Escolha o seu nome de utilizador e selecione o seu país soberano de afiliação (ex: Costa do Marfim, Senegal, Quénia, Nigéria).",
        "fr": "Choisissez votre identifiant développeur et sélectionnez votre pays souverain d'attachement (ex: Côte d'Ivoire, Sénégal, Kenya, Nigeria).",
    },
    "generez votre trousseau de cles mathematiques (phrase mnemonique bip-39 et cle publique schnorr). conservez precieusement votre phrase secrete : elle ne quitte jamais votre terminal.": {
        "en": "Generate your mathematical key pair (BIP-39 mnemonic phrase and Schnorr public key). Keep your secret phrase safe: it never leaves your terminal.",
        "sw": "Tengeneza jozi ya funguo za kihisabati (neno la siri la BIP-39 na ufunguo wa umma wa Schnorr). Hifadhi neno lako la siri vizuri: haliwahi kutoka kwenye kifaa chako.",
        "pt": "Gere o seu par de chaves matemáticas (frase mnemónica BIP-39 e chave pública Schnorr). Guarde bem a sua frase secreta: nunca sai do seu terminal.",
        "fr": "Générez votre trousseau de clés mathématiques (phrase mnémonique BIP-39 et clé publique Schnorr). Conservez précieusement votre phrase secrète : elle ne quitte jamais votre terminal.",
    },
    "validez : votre identite souveraine est instantanement enregistree. votre compte gitlab ce associe est automatiquement provisionne sans aucun mot de passe requis.": {
        "en": "Validate: your sovereign identity is instantly registered. Your associated GitLab CE account is automatically provisioned without any password required.",
        "sw": "Thibitisha: utambulisho wako huru unasajiliwa papo hapo. Akaunti yako inayohusiana ya GitLab CE inatolewa kiotomatiki bila nenosiri lolote linalohitajika.",
        "pt": "Valide: a sua identidade soberana é registada instantaneamente. A sua conta GitLab CE associada é provisionada automaticamente sem qualquer senha necessária.",
        "fr": "Validez : votre identité souveraine est instantanément enregistrée. Votre compte GitLab CE associé est automatiquement provisionné sans aucun mot de passe requis.",
    },
    "methode 2 : inscription directe sur l'instance gitlab auto-hebergee": {
        "en": "Method 2: Direct registration on the self-hosted GitLab instance",
        "sw": "Njia 2: Usajili wa moja kwa moja kwenye GitLab ya kujilisha",
        "pt": "Método 2: Registo direto na instância GitLab auto-hospedada",
        "fr": "Méthode 2 : Inscription directe sur l'instance GitLab auto-hébergée",
    },
    "si votre organisation dispose d'une passerelle gitlab dediee, ouvrez l'interface gitlab (via le bouton « acces forge git »), cliquez sur « s'inscrire » (register), completez votre profil institutionnel, puis associez votre cle zkp bantudevlab via le bouton « connecter avec bantu zkp ».": {
        "en": "If your organization has a dedicated GitLab gateway, open the GitLab interface (via the 'Git Forge Access' button), click 'Register', complete your institutional profile, then link your BantuDevLab ZKP key via the 'Connect with Bantu ZKP' button.",
        "sw": "Ikiwa shirika lako lina lango maalum la GitLab, fungua kiolesura cha GitLab (kupitia kitufe cha 'Ufikiaji wa Git Forge'), bonyeza 'Sajili', kamilisha wasifu wako, kisha unganisha ufunguo wako wa ZKP kupitia kitufe cha 'Unganisha na Bantu ZKP'.",
        "pt": "Se a sua organização tem um gateway GitLab dedicado, abra a interface GitLab (via o botão 'Acesso Git Forge'), clique em 'Registar', complete o seu perfil institucional e ligue a sua chave ZKP via o botão 'Ligar com Bantu ZKP'.",
        "fr": "Si votre organisation dispose d'une passerelle GitLab dédiée, ouvrez l'interface GitLab (via le bouton « Accès Forge Git »), cliquez sur « S'inscrire » (Register), complétez votre profil institutionnel, puis associez votre clé ZKP BantuDevLab via le bouton « Connecter avec Bantu ZKP ».",
    },
    "regle de securite :": {
        "en": "Security rule:",
        "sw": "Kanuni ya usalama:",
        "pt": "Regra de segurança:",
        "fr": "Règle de sécurité :",
    },
    "aucun mot de passe en clair n'est stocke en base de donnees. l'authentification repose exclusivement sur des preuves mathematiques a divulgation nulle de connaissance.": {
        "en": "No plaintext password is stored in the database. Authentication relies exclusively on zero-knowledge mathematical proofs.",
        "sw": "Hakuna nenosiri la wazi linalohifadhiwa kwenye hifadhidata. Uthibitishaji unategemea pekee uthibitisho wa kihisabati wa maarifa sifuri.",
        "pt": "Nenhuma senha em texto simples é armazenada na base de dados. A autenticação baseia-se exclusivamente em provas matemáticas de conhecimento zero.",
        "fr": "Aucun mot de passe en clair n'est stocké en base de données. L'authentification repose exclusivement sur des preuves mathématiques à divulgation nulle de connaissance.",
    },
    "comment se connecter a son compte ?": {
        "en": "How to log in to your account?",
        "sw": "Jinsi ya kuingia kwenye akaunti yako?",
        "pt": "Como iniciar sessão na sua conta?",
        "fr": "Comment se connecter à son compte ?",
    },
    "la connexion s'opere en mode zero-trust sans mot de passe, garantissant l'immunite contre le hameconnage, le vol d'identifiants et les attaques par force brute :": {
        "en": "Connection operates in Zero-Trust mode without passwords, ensuring immunity against phishing, credential theft, and brute force attacks:",
        "sw": "Kuingia kunafanyika katika hali ya Zero-Trust bila nenosiri, kuhakikisha kinga dhidi ya hadaa, wizi wa vitambulisho na mashambulizi ya brute force:",
        "pt": "A ligação opera em modo Zero-Trust sem senhas, garantindo imunidade contra phishing, roubo de credenciais e ataques de força bruta:",
        "fr": "La connexion s'opère en mode Zero-Trust sans mot de passe, garantissant l'immunité contre le hameçonnage, le vol d'identifiants et les attaques par force brute :",
    },
    "connexion a bantudevlab :": {
        "en": "Login to BantuDevLab:",
        "sw": "Kuingia BantuDevLab:",
        "pt": "Ligação ao BantuDevLab:",
        "fr": "Connexion à BantuDevLab :",
    },
    "allez sur la page de connexion zkp. renseignez votre identifiant developpeur. l'application emet un defi cryptographique (nonce a usage unique valable 5 minutes). saisissez votre phrase mnemonique ou cle secrete locale pour calculer la preuve de schnorr": {
        "en": "Go to the ZKP login page. Enter your developer username. The app issues a cryptographic challenge (one-time nonce valid 5 min). Enter your mnemonic phrase or local secret key to calculate the Schnorr proof.",
        "sw": "Nenda kwenye ukurasa wa kuingia wa ZKP. Weka jina la msanidi. Programu inatoa changamoto ya kriptografia (nonce ya dakika 5). Weka neno lako la siri ili kuhesabu uthibitisho wa Schnorr.",
        "pt": "Vá para a página de login ZKP. Introduza o seu nome de utilizador. A aplicação emite um desafio criptográfico (nonce válido 5 min). Introduza a frase mnemónica para calcular a prova de Schnorr.",
        "fr": "Allez sur la page de connexion ZKP. Renseignez votre identifiant développeur. L'application émet un défi cryptographique (nonce à usage unique valable 5 minutes). Saisissez votre phrase mnémonique ou clé secrète locale pour calculer la preuve de Schnorr",
    },
    "une fois la preuve verifiee par le serveur, votre session est ouverte.": {
        "en": "Once the proof is verified by the server, your session is opened.",
        "sw": "Mara uthibitisho unapothibitishwa na seva, kikao chako kinafunguliwa.",
        "pt": "Assim que a prova for verificada pelo servidor, a sua sessão é aberta.",
        "fr": "Une fois la preuve vérifiée par le serveur, votre session est ouverte.",
    },
    "connexion a gitlab ce via single sign-on (sso omniauth zkp) :": {
        "en": "Login to GitLab CE via Single Sign-On (SSO OmniAuth ZKP):",
        "sw": "Kuingia GitLab CE kupitia Single Sign-On (SSO OmniAuth ZKP):",
        "pt": "Ligação ao GitLab CE via Single Sign-On (SSO OmniAuth ZKP):",
        "fr": "Connexion à GitLab CE via Single Sign-On (SSO OmniAuth ZKP) :",
    },
    "sur la mire de connexion gitlab, cliquez sur le bouton souverain": {
        "en": "On the GitLab login page, click the sovereign button",
        "sw": "Kwenye ukurasa wa kuingia wa GitLab, bonyeza kitufe huru",
        "pt": "No ecrã de login do GitLab, clique no botão soberano",
        "fr": "Sur la mire de connexion GitLab, cliquez sur le bouton souverain",
    },
    "si vous etes deja authentifie sur bantudevlab, la session gitlab est ouverte instantanement. sinon, vous serez invite a signer le defi cryptographique sans jamais saisir de mot de passe.": {
        "en": "If you are already authenticated on BantuDevLab, the GitLab session opens instantly. Otherwise, you will be prompted to sign the cryptographic challenge without ever entering a password.",
        "sw": "Ikiwa tayari umethibitishwa kwenye BantuDevLab, kikao cha GitLab kinafunguliwa mara moja. Vinginevyo, utaalikwa kusaini changamoto ya kriptografia bila kuingiza nenosiri.",
        "pt": "Se já estiver autenticado no BantuDevLab, a sessão GitLab abre instantaneamente. Caso contrário, será convidado a assinar o desafio criptográfico sem nunca digitar uma senha.",
        "fr": "Si vous êtes déjà authentifié sur BantuDevLab, la session GitLab est ouverte instantanément. Sinon, vous serez invité à signer le défi cryptographique sans jamais saisir de mot de passe.",
    },
    "protection anti-rejeu :": {
        "en": "Anti-replay protection:",
        "sw": "Ulinzi dhidi ya kurudia:",
        "pt": "Proteção anti-repetição:",
        "fr": "Protection anti-rejeu :",
    },
    "chaque defi de connexion est unique et consomme atomiquement. une preuve interceptee sur le reseau ne peut jamais etre reutilisee.": {
        "en": "Each connection challenge is unique and atomically consumed. An intercepted proof can never be reused.",
        "sw": "Kila changamoto ya muunganisho ni ya kipekee na inatumiwa mara moja tu. Uthibitisho ulionaswa mtandaoni hauwezi kamwe kutumiwa tena.",
        "pt": "Cada desafio de ligação é único e consumido atomicamente. Uma prova intercetada na rede nunca pode ser reutilizada.",
        "fr": "Chaque défi de connexion est unique et consommé atomiquement. Une preuve interceptée sur le réseau ne peut jamais être réutilisée.",
    },
    "comment consulter et cloner le code source des depots souverains ?": {
        "en": "How to view and clone source code from sovereign repositories?",
        "sw": "Jinsi ya kuona na kunakili msimbo chanzo kutoka hazina huru?",
        "pt": "Como consultar e clonar código fonte dos repositórios soberanos?",
        "fr": "Comment consulter et cloner le code source des dépôts souverains ?",
    },
    "le code source heberge sur bantudevlab et gitlab est consultable et clonable selon plusieurs modalites :": {
        "en": "Source code hosted on BantuDevLab and GitLab can be viewed and cloned via several methods:",
        "sw": "Msimbo chanzo uliopo BantuDevLab na GitLab unaweza kutazamwa na kunakiliwa kwa njia kadhaa:",
        "pt": "O código fonte hospedado no BantuDevLab e GitLab pode ser consultado e clonado por várias modalidades:",
        "fr": "Le code source hébergé sur BANTUDEVLAB et GitLab est consultable et clonable selon plusieurs modalités :",
    },
    "consultation web immediate": {
        "en": "Immediate Web Browsing",
        "sw": "Kuvinjari Wavuti Papo Hapo",
        "pt": "Consulta Web Imediata",
        "fr": "Consultation Web Immédiate",
    },
    "depuis le": {"en": "From the", "sw": "Kutoka", "pt": "A partir do", "fr": "Depuis le"},
    "consultez la liste des depots, l'arborescence des fichiers, l'historique des commits et editez du code en ligne avec colorisation syntaxique.": {
        "en": "browse repository lists, file trees, commit histories, and edit code online with syntax highlighting.",
        "sw": "angalia orodha ya hazina, muundo wa faili, historia ya commits na hariri msimbo mtandaoni kwa rangi za sintaksia.",
        "pt": "consulte a lista de repositórios, a árvore de ficheiros, o histórico de commits e edite código online com realce de sintaxe.",
        "fr": "consultez la liste des dépôts, l'arborescence des fichiers, l'historique des commits et éditez du code en ligne avec colorisation syntaxique.",
    },
    "clone https avec jeton git zkp": {
        "en": "HTTPS Clone with ZKP Git Token",
        "sw": "Kunakili kwa HTTPS kwa Kutumia Tokeni ya Git ZKP",
        "pt": "Clone HTTPS com Token Git ZKP",
        "fr": "Clone HTTPS avec Jeton Git ZKP",
    },
    "generez un token d'acces git": {
        "en": "Generate a Git access token",
        "sw": "Tengeneza tokeni ya ufikiaji ya Git",
        "pt": "Gere um token de acesso Git",
        "fr": "Générez un token d'accès Git",
    },
    "valide par preuve zkp depuis l'api": {
        "en": "validated by ZKP proof from the API",
        "sw": "iliyothibitishwa na ZKP kutoka kwa API",
        "pt": "validado por prova ZKP a partir da API",
        "fr": "validé par preuve ZKP depuis l'API",
    },
    "clonez ensuite via :": {
        "en": "Then clone via:",
        "sw": "Kisha nakili kupitia:",
        "pt": "Depois clone através de:",
        "fr": "Clonez ensuite via :",
    },
    "clone securise ssh": {
        "en": "Secure SSH Clone",
        "sw": "Kunakili Salama kwa SSH",
        "pt": "Clone Seguro SSH",
        "fr": "Clone Sécurisé SSH",
    },
    "ajoutez votre cle publique ssh (ed25519 ou rsa 4096 bits) dans vos parametres gitlab pour cloner directement :": {
        "en": "Add your SSH public key (Ed25519 or RSA 4096-bit) in your GitLab settings to clone directly:",
        "sw": "Ongeza ufunguo wako wa umma wa SSH (Ed25519 au RSA 4096 bits) kwenye mipangilio yako ya GitLab ili kunakili moja kwa moja:",
        "pt": "Adicione a sua chave pública SSH (Ed25519 ou RSA 4096 bits) nas suas configurações GitLab para clonar diretamente:",
        "fr": "Ajoutez votre clé publique SSH (Ed25519 ou RSA 4096 bits) dans vos paramètres GitLab pour cloner directement :",
    },
    "questions frequentes techniques & securite": {
        "en": "Technical & Security Frequently Asked Questions",
        "sw": "Maswali ya Kiufundi & Usalama",
        "pt": "Perguntas Frequentes Técnicas & Segurança",
        "fr": "Questions Fréquentes Techniques & Sécurité",
    },
    "approfondissement sur les fonctionnalites avancees : zkp, ia gemma 5b, sast, multi-tenancy et souverainete continentale.": {
        "en": "Deep dive into advanced features: ZKP, Gemma 5B AI, SAST, Multi-Tenancy, and continental sovereignty.",
        "sw": "Uchambuzi wa kina wa vipengele vya juu: ZKP, AI ya Gemma 5B, SAST, Multi-Tenancy na mamlaka ya bara.",
        "pt": "Aprofundamento nas funcionalidades avançadas: ZKP, IA Gemma 5B, SAST, Multi-Tenancy e soberania continental.",
        "fr": "Approfondissement sur les fonctionnalités avancées : ZKP, IA Gemma 5B, SAST, Multi-Tenancy et souveraineté continentale.",
    },
    "qu'est-ce que l'authentification zero-trust zkp et pourquoi surpasse-t-elle les mots de passe classiques ?": {
        "en": "What is Zero-Trust ZKP authentication and why is it superior to traditional passwords?",
        "sw": "Uthibitishaji wa Zero-Trust ZKP ni nini na kwa nini unazidi manenosiri ya kawaida?",
        "pt": "O que é a autenticação Zero-Trust ZKP e porque supera as senhas tradicionais?",
        "fr": "Qu'est-ce que l'authentification Zero-Trust ZKP et pourquoi surpasse-t-elle les mots de passe classiques ?",
    },
    "zkp (zero-knowledge proof, ou preuve a divulgation nulle de connaissance) est un protocole cryptographique mathematique fonde sur le probleme du logarithme discret (rfc 3526 modp 2048 bits). grace au protocole de schnorr rendu non-interactif via la transformation de fiat-shamir, vous prouvez au serveur que vous detenez votre secret mathematique sans jamais lui reveler ce secret, ni meme le faire transiter sur le reseau.": {
        "en": "ZKP (Zero-Knowledge Proof) is a mathematical cryptographic protocol based on the discrete logarithm problem (RFC 3526 MODP 2048 bits). Thanks to Schnorr's protocol made non-interactive via Fiat-Shamir transformation, you prove to the server that you hold the secret without EVER revealing it or transmitting it across the network.",
        "sw": "ZKP (Uthibitisho wa Maarifa Sifuri) ni itifaki ya kihisabati ya kriptografia inayotegemea tatizo la discrete logarithm (RFC 3526 MODP 2048 bits). Kupitia itifaki ya Schnorr na Fiat-Shamir, unathibitisha una siri yako bila KUWEKA WAZI kamwe au kuituma mtandaoni.",
        "pt": "ZKP (Prova de Conhecimento Zero) é um protocolo criptográfico baseado no problema do logaritmo discreto (RFC 3526 MODP 2048 bits). Pelo protocolo de Schnorr e transformação Fiat-Shamir, prova deter o segredo sem NUNCA o revelar ou transmitir pela rede.",
        "fr": "ZKP (Zero-Knowledge Proof, ou preuve à divulgation nulle de connaissance) est un protocole cryptographique mathématique fondé sur le problème du logarithme discret (RFC 3526 MODP 2048 bits). Grâce au protocole de Schnorr rendu non-interactif via la transformation de Fiat-Shamir, vous prouvez au serveur que vous détenez votre secret mathématique sans JAMAIS lui révéler ce secret, ni même le faire transiter sur le réseau.",
    },
    "avantages majeurs :": {
        "en": "Major advantages:",
        "sw": "Faida kuu:",
        "pt": "Vantagens principais:",
        "fr": "Avantages majeurs :",
    },
    "confidentialite mathematique": {
        "en": "Mathematical Confidentiality",
        "sw": "Usiri wa Kihisabati",
        "pt": "Confidencialidade Matemática",
        "fr": "Confidentialité Mathématique",
    },
    "meme en cas de compromission totale de la base de donnees du serveur, aucun mot de passe ni cle privee ne peut fuiter, car seules les cles publiques sont enregistrees.": {
        "en": "Even in the event of total server database compromise, no password or private key can leak, as only public keys are stored.",
        "sw": "Hata kama hifadhidata ya seva itadukuliwa kabisa, hakuna nenosiri wala ufunguo wa siri utakaovuja, kwa sababu funguo za umma pekee ndizo zilizohifadhiwa.",
        "pt": "Mesmo em caso de comprometimento total da base de dados do servidor, nenhuma senha ou chave privada vaza, pois apenas as chaves públicas são guardadas.",
        "fr": "Même en cas de compromission totale de la base de données du serveur, aucun mot de passe ni clé privée ne peut fuiter, car seules les clés publiques sont enregistrées.",
    },
    "immunite integrale contre les ecoutes reseau et le rejeu de requetes grace aux nonces ephemeres consommes atomiquement.": {
        "en": "Full immunity against network eavesdropping and replay attacks thanks to atomically consumed ephemeral nonces.",
        "sw": "Kinga kamili dhidi ya udukuzi wa mtandao na mashambulizi ya kurudia kutokana na nonces zinazotumiwa mara moja tu.",
        "pt": "Imunidade integral contra escutas de rede e ataques de repetição graças a nonces efémeros consumidos atomicamente.",
        "fr": "Immunité intégrale contre les écoutes réseau et le rejeu de requêtes grâce aux nonces éphémères consommés atomiquement.",
    },
    "validation mathematique stricte de non-appartenance aux petits sous-groupes pour eliminer toute tentative de falsification de cle.": {
        "en": "Strict mathematical validation of non-membership in small subgroups to eliminate any key forgery attempt.",
        "sw": "Uthibitishaji mkali wa kihisabati wa kutokuwa sehemu ya vikundi vidogo ili kuzuia majaribio yote ya kughushi funguo.",
        "pt": "Validação matemática estrita de não pertença a pequenos subgrupos para eliminar qualquer tentativa de falsificação de chave.",
        "fr": "Validation mathématique stricte de non-appartenance aux petits sous-groupes pour éliminer toute tentative de falsification de clé.",
    },
    "comment fonctionne la double approbation zkp sur les merge requests (mr) ?": {
        "en": "How does ZKP dual approval work on Merge Requests (MR)?",
        "sw": "Jinsi idhini mbili ya ZKP inavyofanya kazi kwenye Merge Requests (MR)?",
        "pt": "Como funciona a dupla aprovação ZKP em Merge Requests (MR)?",
        "fr": "Comment fonctionne la double approbation ZKP sur les Merge Requests (MR) ?",
    },
    "pour les projets critiques des ministeres, banques centrales et agences publiques, bantudevlab integre un quorum d'approbation cryptographique :": {
        "en": "For critical projects of ministries, central banks, and public agencies, BANTUDEVLAB integrates a cryptographic approval quorum:",
        "sw": "Kwa miradi nyeti ya wizara, benki kuu na mashirika ya umma, BANTUDEVLAB inajumuisha akidi ya idhini ya kriptografia:",
        "pt": "Para projetos críticos de ministérios, bancos centrais e agências públicas, o BANTUDEVLAB integra um quórum de aprovação criptográfica:",
        "fr": "Pour les projets critiques des ministères, banques centrales et agences publiques, BANTUDEVLAB intègre un quorum d'approbation cryptographique :",
    },
    "la fusion (merge) d'une branche de fonctionnalites vers la branche principale exige la signature mathematique d'au moins deux relecteurs habilites.": {
        "en": "Merging a feature branch into the main branch requires the mathematical signature of at least two authorized reviewers.",
        "sw": "Kuunganisha tawi la vipengele kwenye tawi kuu kunahitaji saini ya kihisabati ya angalau wakaguzi wawili walioidhinishwa.",
        "pt": "A fusão de um branch de funcionalidades para o branch principal exige a assinatura matemática de pelo menos dois revisores autorizados.",
        "fr": "La fusion (merge) d'une branche de fonctionnalités vers la branche principale exige la signature mathématique d'au moins deux relecteurs habilités.",
    },
    "chaque approbation est scellee par une preuve zkp enregistree sous le modele sovereignmergerequestapproval.": {
        "en": "Each approval is sealed by a ZKP proof recorded under the SovereignMergeRequestApproval model.",
        "sw": "Kila idhini inafungwa na uthibitisho wa ZKP uliorekodiwa chini ya muundo wa SovereignMergeRequestApproval.",
        "pt": "Cada aprovação é selada por uma prova ZKP registada sob o modelo SovereignMergeRequestApproval.",
        "fr": "Chaque approbation est scellée par une preuve ZKP enregistrée sous le modèle SovereignMergeRequestApproval.",
    },
    "le pipeline gitlab ci/cd et la passerelle de fusion bloquent automatiquement l'operation si le quorum cryptographique n'est pas reuni.": {
        "en": "The GitLab CI/CD pipeline and merge gateway automatically block the operation if the cryptographic quorum is not reached.",
        "sw": "Bomba la GitLab CI/CD na lango la kuunganisha huzuia kiotomatiki operesheni ikiwa akidi ya kriptografia haijafikiwa.",
        "pt": "O pipeline GitLab CI/CD e o gateway de fusão bloqueiam automaticamente a operação se o quórum criptográfico não for atingido.",
        "fr": "Le pipeline GitLab CI/CD et la passerelle de fusion bloquent automatiquement l'opération si le quorum cryptographique n'est pas réuni.",
    },
    "comment l'assistant ia local gemma 5b audite-t-il le code sans aucune fuite vers l'etranger ?": {
        "en": "How does the local Gemma 5B AI assistant audit code without any leaks abroad?",
        "sw": "Jinsi gani msaidizi wa ndani wa AI Gemma 5B anavyokagua msimbo bila uvujaji wowote nje ya nchi?",
        "pt": "Como é que o assistente de IA local Gemma 5B audita o código sem fugas para o estrangeiro?",
        "fr": "Comment l'assistant IA local Gemma 5B audite-t-il le code sans aucune fuite vers l'étranger ?",
    },
    "contrairement aux assistants cloud proprietaires heberges sous juridiction etrangere (cloud act, fisa), le modele gemma 5b de bantudevlab :": {
        "en": "Unlike proprietary cloud assistants hosted under foreign jurisdiction (Cloud Act, FISA), BANTUDEVLAB's Gemma 5B model:",
        "sw": "Tofauti na wasaidizi wa wingu wa kigeni wanaotawaliwa na sheria za kigeni (Cloud Act, FISA), mfumo wa Gemma 5B wa BANTUDEVLAB:",
        "pt": "Ao contrário dos assistentes em nuvem proprietários sujeitos a jurisdição estrangeira (Cloud Act, FISA), o modelo Gemma 5B do BANTUDEVLAB:",
        "fr": "Contrairement aux assistants cloud propriétaires hébergés sous juridiction étrangère (Cloud Act, FISA), le modèle Gemma 5B de BANTUDEVLAB :",
    },
    "est deploye exclusivement sur des serveurs physiques situes sur le sol africain (systalink cloud, datacenters tier-3 abidjan, dakar, nairobi, kigali).": {
        "en": "Is deployed exclusively on physical servers located on African soil (Systalink Cloud, Tier-3 datacenters in Abidjan, Dakar, Nairobi, Kigali).",
        "sw": "Imewekwa pekee kwenye seva halisi zilizopo barani Afrika (Systalink Cloud, vituo vya data vya Tier-3 Abidjan, Dakar, Nairobi, Kigali).",
        "pt": "É implementado exclusivamente em servidores físicos em solo africano (Systalink Cloud, datacenters Tier-3 em Abidjan, Dakar, Nairobi, Kigali).",
        "fr": "Est déployé exclusivement sur des serveurs physiques situés sur le sol africain (Systalink Cloud, datacenters Tier-3 Abidjan, Dakar, Nairobi, Kigali).",
    },
    "s'execute en local via vllm / ollama sans aucune transmission de telemetrie ou de code source a des tiers.": {
        "en": "Runs locally via vLLM / Ollama with zero telemetry or source code transmission to third parties.",
        "sw": "Inaendeshwa ndani ya nchi kupitia vLLM / Ollama bila kutuma data yoyote au msimbo kwa wahusika wengine.",
        "pt": "Executa localmente via vLLM / Ollama sem qualquer transmissão de telemetria ou código fonte a terceiros.",
        "fr": "S'exécute en local via vLLM / Ollama sans aucune transmission de télémétrie ou de code source à des tiers.",
    },
    "masque et anonymise automatiquement les secrets eventuels avant toute journalisation (aiinteractionlog).": {
        "en": "Automatically masks and anonymizes any secrets prior to any logging (AIInteractionLog).",
        "sw": "Inaficha na kubadilisha siri zote kuwa zisizojulikana kabla ya kuweka kumbukumbu (AIInteractionLog).",
        "pt": "Mascara e anonimiza automaticamente quaisquer segredos antes de qualquer registo (AIInteractionLog).",
        "fr": "Masque et anonymise automatiquement les secrets éventuels avant toute journalisation (AIInteractionLog).",
    },
    "est fine-tune avec lora/qlora (4-bit gguf) sur les cadres legaux panafricains et les meilleures pratiques de souverainete logicielle.": {
        "en": "Is fine-tuned with LoRA/QLoRA (4-bit GGUF) on pan-African legal frameworks and software sovereignty best practices.",
        "sw": "Imefunzwa kwa kina na LoRA/QLoRA (GGUF ya biti 4) kuhusu mifumo ya kisheria ya Afrika nzima na viwango vya juu vya mamlaka ya programu.",
        "pt": "É ajustado com LoRA/QLoRA (GGUF 4-bit) sobre os quadros jurídicos pan-africanos e as melhores práticas de soberania de software.",
        "fr": "Est fine-tuné avec LoRA/QLoRA (4-bit GGUF) sur les cadres légaux panafricains et les meilleures pratiques de souveraineté logicielle.",
    },
    "comment fonctionne le scanner de securite sast et comment est calcule le score de souverainete ?": {
        "en": "How does the SAST security scanner work and how is the sovereignty score calculated?",
        "sw": "Jinsi gani skana ya usalama ya SAST inavyofanya kazi na jinsi alama ya mamlaka inavyopigwa mahesabu?",
        "pt": "Como funciona o scanner de segurança SAST e como é calculada a pontuação de soberania?",
        "fr": "Comment fonctionne le scanner de sécurité SAST et comment est calculé le score de souveraineté ?",
    },
    "le scanner d'analyse statique sast de bantudevlab analyse automatiquement chaque commit et fichier soumis :": {
        "en": "BANTUDEVLAB's SAST static analysis scanner automatically analyzes each submitted commit and file:",
        "sw": "Skana ya uchambuzi tuli ya SAST ya BANTUDEVLAB inachunguza kiotomatiki kila commit na faili iliyowasilishwa:",
        "pt": "O scanner de análise estática SAST do BANTUDEVLAB analisa automaticamente cada commit e ficheiro submetido:",
        "fr": "Le scanner d'analyse statique SAST de BANTUDEVLAB analyse automatiquement chaque commit et fichier soumis :",
    },
    "detection des secrets codes en dur (cles privees, tokens api, identifiants).": {
        "en": "Detection of hardcoded secrets (private keys, API tokens, credentials).",
        "sw": "Ugunduzi wa siri zilizowekwa moja kwa moja kwenye msimbo (funguo za siri, tokeni za API, vitambulisho).",
        "pt": "Deteção de segredos em código (chaves privadas, tokens de API, credenciais).",
        "fr": "Détection des secrets codés en dur (clés privées, tokens API, identifiants).",
    },
    "detection des injections sql, executions de commandes non securisees (eval, exec, pickle).": {
        "en": "Detection of SQL injections, insecure command execution (eval, exec, pickle).",
        "sw": "Ugunduzi wa mashambulizi ya SQL injection na utekelezaji usio salama wa amri (eval, exec, pickle).",
        "pt": "Deteção de injeções SQL e execuções de comandos inseguras (eval, exec, pickle).",
        "fr": "Détection des injections SQL, exécutions de commandes non sécurisées (eval, exec, pickle).",
    },
    "detection des dependances externes non souveraines ou non auditees.": {
        "en": "Detection of non-sovereign or unaudited external dependencies.",
        "sw": "Ugunduzi wa utegemezi wa nje usio huru au usiofanyiwa ukaguzi.",
        "pt": "Deteção de dependências externas não soberanas ou não auditadas.",
        "fr": "Détection des dépendances externes non souveraines ou non auditées.",
    },
    "attribution d'un score de 0 a 100 : un score inferieur a 70 peut declencher un blocage automatique preventif dans les hooks de pre-receive.": {
        "en": "Assignment of a score from 0 to 100: a score below 70 can trigger automatic preventive blocking in pre-receive hooks.",
        "sw": "Utoaji wa alama kutoka 0 hadi 100: alama chini ya 70 inaweza kuzuia kiotomatiki kusukuma msimbo kupitia pre-receive hooks.",
        "pt": "Atribuição de uma pontuação de 0 a 100: pontuação abaixo de 70 pode acionar bloqueio preventivo automático nos pre-receive hooks.",
        "fr": "Attribution d'un score de 0 à 100 : un score inférieur à 70 peut déclencher un blocage automatique préventif dans les hooks de pre-receive.",
    },
    "exportation des rapports aux formats standard oasis sarif 2.1.0 et gitlab sast (gl-sast-report.json).": {
        "en": "Export of reports in OASIS SARIF 2.1.0 and GitLab SAST (gl-sast-report.json) standard formats.",
        "sw": "Usafirishaji wa ripoti katika miundo rasmi ya OASIS SARIF 2.1.0 na GitLab SAST (gl-sast-report.json).",
        "pt": "Exportação de relatórios nos formatos padrão OASIS SARIF 2.1.0 e GitLab SAST (gl-sast-report.json).",
        "fr": "Exportation des rapports aux formats standard OASIS SARIF 2.1.0 et GitLab SAST (gl-sast-report.json).",
    },
    "comment est assuree l'etancheite entre organisations (banques, ministeres, universites, startups) ?": {
        "en": "How is segregation ensured between organizations (Banks, Ministries, Universities, Startups)?",
        "sw": "Jinsi gani utengano unahakikishwa kati ya mashirika (Benki, Wizara, Vyuo Vikuu, Startups)?",
        "pt": "Como é assegurada a separação entre organizações (Bancos, Ministérios, Universidades, Startups)?",
        "fr": "Comment est assurée l'étanchéité entre organisations (Banques, Ministères, Universités, Startups) ?",
    },
    "le modele sovereignorganization assure une compartimentation multi-tenancy stricte :": {
        "en": "The SovereignOrganization model guarantees strict multi-tenancy compartmentalization:",
        "sw": "Muundo wa SovereignOrganization unahakikisha utengano mkali wa wateja wengi (multi-tenancy):",
        "pt": "O modelo SovereignOrganization assegura compartimentação multi-inquilino rigorosa:",
        "fr": "Le modèle SovereignOrganization assure une compartimentation multi-tenancy stricte :",
    },
    "chaque organisation dispose d'espaces de noms (namespaces) dedies synchronises avec les groupes gitlab.": {
        "en": "Each organization has dedicated namespaces synchronized with GitLab groups.",
        "sw": "Kila shirika lina nafasi maalum za majina (namespaces) zilizosawazishwa na vikundi vya GitLab.",
        "pt": "Cada organização tem espaços de nomes (namespaces) dedicados sincronizados com os grupos GitLab.",
        "fr": "Chaque organisation dispose d'espaces de noms (namespaces) dédiés synchronisés avec les groupes GitLab.",
    },
    "la creation d'organisations est soumise a validation administrative (controle isadminuser).": {
        "en": "Organization creation is subject to administrative validation (IsAdminUser check).",
        "sw": "Uundaji wa mashirika unahitaji uthibitisho wa kiutawala (udhibiti wa IsAdminUser).",
        "pt": "A criação de organizações está sujeita a validação administrativa (controlo IsAdminUser).",
        "fr": "La création d'organisations est soumise à validation administrative (contrôle IsAdminUser).",
    },
    "des niveaux de souverainete graduels (tier-1 continental, tier-2 regional, tier-3 startup) definissent les regles de chiffrement et d'hebergement.": {
        "en": "Graduated sovereignty tiers (Tier-1 Continental, Tier-2 Regional, Tier-3 Startup) govern encryption and hosting rules.",
        "sw": "Ngazi za mamlaka za taratibu (Tier-1 Bara, Tier-2 Kanda, Tier-3 Startup) zinaamuru sheria za usimbaji fiche na uhifadhi.",
        "pt": "Níveis de soberania graduais (Tier-1 Continental, Tier-2 Regional, Tier-3 Startup) definem regras de encriptação e alojamento.",
        "fr": "Des niveaux de souveraineté graduels (Tier-1 Continental, Tier-2 Régional, Tier-3 Startup) définissent les règles de chiffrement et d'hébergement.",
    },
    "en quoi bantudevlab est-il conforme a la convention de malabo et aux reglementations africaines de cybersecurite ?": {
        "en": "How does BANTUDEVLAB comply with the Malabo Convention and African cybersecurity regulations?",
        "sw": "BANTUDEVLAB inafanana vipi na Mkataba wa Malabo na kanuni za usalama wa mtandao za Afrika?",
        "pt": "De que forma o BANTUDEVLAB cumpre a Convenção de Malabo e os regulamentos africanos de cibersegurança?",
        "fr": "En quoi BANTUDEVLAB est-il conforme à la Convention de Malabo et aux réglementations africaines de cybersécurité ?",
    },
    "la convention de l'union africaine sur la cybersecurite et la protection des donnees a caractere personnel (malabo 2014) impose des garanties strictes d'integrite, de tracabilite et de non-ingerence :": {
        "en": "The African Union Convention on Cyber Security and Personal Data Protection (Malabo 2014) mandates strict guarantees of integrity, auditability, and non-interference:",
        "sw": "Mkataba wa Umoja wa Afrika kuhusu Usalama wa Mtandao na Ulinzi wa Data ya Kibinafsi (Malabo 2014) unahitaji dhamana kali za uadilifu, ufuatiliaji na kutoingiliwa:",
        "pt": "A Convenção da União Africana sobre Cibersegurança e Proteção de Dados Pessoais (Malabo 2014) exige garantias estritas de integridade, rastreabilidade e não ingerência:",
        "fr": "La Convention de l'Union Africaine sur la Cybersécurité et la Protection des Données à Caractère Personnel (Malabo 2014) impose des garanties strictes d'intégrité, de traçabilité et de non-ingérence :",
    },
    "journal d'audit immuable (audittraillog) chaine cryptographiquement par hachage sha-256 (blockchain interne verifiable).": {
        "en": "Immutable audit log (AuditTrailLog) cryptographically chained via SHA-256 hashing (verifiable internal blockchain).",
        "sw": "Kumbukumbu ya ukaguzi isiyobadilika (AuditTrailLog) iliyounganishwa kwa kriptografia kupitia heshi ya SHA-256 (blockchain ya ndani inayoweza kukaguliwa).",
        "pt": "Registo de auditoria imutável (AuditTrailLog) encadeado criptograficamente por hash SHA-256 (blockchain interna verificável).",
        "fr": "Journal d'audit immuable (AuditTrailLog) chaîné cryptographiquement par hachage SHA-256 (blockchain interne vérifiable).",
    },
    "verification automatisee de l'integrite via la commande de gestion :": {
        "en": "Automated integrity verification via management command:",
        "sw": "Uthibitishaji wa kiotomatiki wa uadilifu kupitia amri ya usimamizi:",
        "pt": "Verificação automatizada de integridade através de comando de gestão:",
        "fr": "Vérification automatisée de l'intégrité via la commande de gestion :",
    },
    "souverainete des donnees garantie : aucun hebergement soumis a des legislations extraterritoriales.": {
        "en": "Guaranteed data sovereignty: zero hosting subject to extraterritorial jurisdiction.",
        "sw": "Mamlaka ya data yamehakikishwa: hakuna uhifadhi unaotawaliwa na sheria za kigeni.",
        "pt": "Soberania de dados garantida: nenhum alojamento sujeito a legislações extraterritoriais.",
        "fr": "Souveraineté des données garantie : aucun hébergement soumis à des législations extraterritoriales.",
    },
    "pourquoi la plateforme n'utilise-t-elle aucun emoji ?": {
        "en": "Why does the platform not use any emojis?",
        "sw": "Kwa nini jukwaa halitumii emoji yoyote?",
        "pt": "Porque é que a plataforma não utiliza nenhum emoji?",
        "fr": "Pourquoi la plateforme n'utilise-t-elle aucun emoji ?",
    },
    "bantudevlab applique une politique stricte zero-emoji (controlee en continu par le script scripts/check_no_emoji.py) pour trois raisons majeures :": {
        "en": "BANTUDEVLAB enforces a strict Zero-Emoji policy (continuously monitored by scripts/check_no_emoji.py) for three core reasons:",
        "sw": "BANTUDEVLAB inatekeleza sera kali ya Zero-Emoji (inayofuatiliwa kila mara na scripts/check_no_emoji.py) kwa sababu tatu kuu:",
        "pt": "O BANTUDEVLAB aplica uma política rigorosa Zero-Emoji (monitorizada continuamente por scripts/check_no_emoji.py) por três razões principais:",
        "fr": "BANTUDEVLAB applique une politique stricte Zéro-Emoji (contrôlée en continu par le script scripts/check_no_emoji.py) pour trois raisons majeures :",
    },
    "accessibilite universelle (wcag 2.2 aa) : les lecteurs d'ecran pour personnes malvoyantes prononcent souvent de facon erratique les pictogrammes unicode.": {
        "en": "Universal accessibility (WCAG 2.2 AA): screen readers for visually impaired users often misread Unicode pictograms.",
        "sw": "Upatikanaji kwa wote (WCAG 2.2 AA): visoma-skrini vya wasioona mara nyingi husoma vibaya picha za Unicode.",
        "pt": "Acessibilidade universal (WCAG 2.2 AA): leitores de ecrã para utilizadores com deficiência visual frequentemente pronunciam pictogramas Unicode de forma errática.",
        "fr": "Accessibilité universelle (WCAG 2.2 AA) : les lecteurs d'écran pour personnes malvoyantes prononcent souvent de façon erratique les pictogrammes Unicode.",
    },
    "souverainete visuelle & neutralite : l'ensemble des icones et drapeaux sont des fichiers vectoriels svg auto-heberges sans aucun recours a des polices ou cdn tiers.": {
        "en": "Visual sovereignty & neutrality: all icons and flags are self-hosted SVG vector files without any external font or CDN dependencies.",
        "sw": "Mamlaka ya kuona & kutopendelea: aikoni na bendera zote ni faili za vektori za SVG za ndani bila kutegemea fonti au CDN za nje.",
        "pt": "Soberania visual & neutralidade: todos os ícones e bandeiras são ficheiros vetoriais SVG auto-hospedados sem recorrer a fontes ou CDNs de terceiros.",
        "fr": "Souveraineté visuelle & neutralité : l'ensemble des icônes et drapeaux sont des fichiers vectoriels SVG auto-hébergés sans aucun recours à des polices ou CDN tiers.",
    },
    "coherence d'affichage : affichage strictement identique quel que soit le systeme d'exploitation client (linux, bsd, windows, macos, terminaux mobiles).": {
        "en": "Rendering consistency: strictly identical display across any client operating system (Linux, BSD, Windows, macOS, mobile terminals).",
        "sw": "Uthabiti wa muonekano: muonekano unaofanana kabisa kwenye mfumo wowote wa uendeshaji (Linux, BSD, Windows, macOS, vifaa vya mkononi).",
        "pt": "Consistência de exibição: visualização estritamente idêntica qualquer que seja o sistema operativo cliente (Linux, BSD, Windows, macOS, dispositivos móveis).",
        "fr": "Cohérence d'affichage : affichage strictement identique quel que soit le système d'exploitation client (Linux, BSD, Windows, macOS, terminaux mobiles).",
    },
    "comment configurer et executer des pipelines ci/cd sur les runners souverains ?": {
        "en": "How to configure and run CI/CD pipelines on sovereign runners?",
        "sw": "Jinsi ya kusanidi na kuendesha mabomba ya CI/CD kwenye waendeshaji huru?",
        "pt": "Como configurar e executar pipelines de CI/CD nos runners soberanos?",
        "fr": "Comment configurer et exécuter des pipelines CI/CD sur les runners souverains ?",
    },
    "vos fichiers .gitlab-ci.yml peuvent cibler directement les noeuds d'execution certifies panafricains grace aux tags de runners :": {
        "en": "Your .gitlab-ci.yml files can directly target certified pan-African execution nodes using runner tags:",
        "sw": "Faili zako za .gitlab-ci.yml zinaweza kulenga moja kwa moja nodi zilizoidhinishwa za Afrika kupitia vitambulisho vya runner:",
        "pt": "Os seus ficheiros .gitlab-ci.yml podem apontar diretamente para nós de execução certificados pan-africanos através de tags de runners:",
        "fr": "Vos fichiers .gitlab-ci.yml peuvent cibler directement les nœuds d'exécution certifiés panafricains grâce aux tags de runners :",
    },
    "ces runners sont isoles dans des conteneurs securises rootless heberges dans nos datacenters partenaires.": {
        "en": "These runners are isolated inside secure rootless containers hosted in our partner datacenters.",
        "sw": "Waendeshaji hawa wametengwa katika kontena salama zisizo na mizizi (rootless) zilizopo kwenye vituo vyetu vya data vya washirika.",
        "pt": "Estes runners estão isolados em contentores seguros sem privilégios de root alojados nos nossos datacenters parceiros.",
        "fr": "Ces runners sont isolés dans des conteneurs sécurisés rootless hébergés dans nos datacenters partenaires.",
    },
    "une autre question technique ?": {
        "en": "Another technical question?",
        "sw": "Swali lingine la kiufundi?",
        "pt": "Outra questão técnica?",
        "fr": "Une autre question technique ?",
    },
    "consultez la documentation technique approfondie du projet ou adressez-vous directement aux ingenieurs souverains de bantudevlab.": {
        "en": "Consult the in-depth technical documentation or reach out directly to BANTUDEVLAB sovereign engineers.",
        "sw": "Angalia nyaraka za kiufundi za kina au wasiliana moja kwa moja na wahandisi huru wa BANTUDEVLAB.",
        "pt": "Consulte a documentação técnica aprofundada do projeto ou contacte diretamente os engenheiros soberanos do BANTUDEVLAB.",
        "fr": "Consultez la documentation technique approfondie du projet ou adressez-vous directement aux ingénieurs souverains de BANTUDEVLAB.",
    },
    # Dashboard & SAST
    "workbench souverain & audit sast": {
        "en": "Sovereign Workbench & SAST Audit",
        "sw": "Jukwaa Huru la Kazi na Ukaguzi wa SAST",
        "pt": "Workbench Soberano & Auditoria SAST",
        "fr": "Workbench Souverain & Audit SAST",
    },
    "lancer l'audit de securite": {
        "en": "Run Security Audit",
        "sw": "Anzisha Ukaguzi wa Usalama",
        "pt": "Executar Auditoria de Seguranca",
        "fr": "Lancer l'Audit de Sécurité",
    },
    "demander l'avis de gemma 5b": {
        "en": "Ask Gemma 5B Review",
        "sw": "Omba Maoni ya AI ya Gemma 5B",
        "pt": "Pedir Opiniao do Gemma 5B",
        "fr": "Demander l'Avis de Gemma 5B",
    },
    "audits ia gemma 5b": {
        "en": "Gemma 5B AI Audits",
        "sw": "Ukaguzi wa AI Gemma 5B",
        "pt": "Auditorias IA Gemma 5B",
        "fr": "Audits IA Gemma 5B",
    },
    "rapport d'audit gemma 5b (local / on-premise)": {
        "en": "Gemma 5B Audit Report (Local / On-Premise)",
        "sw": "Ripoti ya Ukaguzi wa Gemma 5B (Ndani / On-Premise)",
        "pt": "Relatório de Auditoria Gemma 5B (Local / On-Premise)",
        "fr": "Rapport d'Audit Gemma 5B (Local / On-Premise)",
    },
    "connexion securisee au moteur ia on-premise gemma 5b...": {
        "en": "Secure connection to On-Premise Gemma 5B AI engine...",
        "sw": "Muunganisho salama kwa injini ya ndani ya AI Gemma 5B...",
        "pt": "Ligação segura ao motor de IA On-Premise Gemma 5B...",
        "fr": "Connexion sécurisée au moteur IA On-Premise Gemma 5B...",
    },
    "connexion au flux sse de gemma 5b...": {
        "en": "Connecting to Gemma 5B SSE stream...",
        "sw": "Inaunganisha kwenye mkondo wa SSE wa Gemma 5B...",
        "pt": "A ligar ao fluxo SSE do Gemma 5B...",
        "fr": "Connexion au flux SSE de Gemma 5B...",
    },
    "revue de code par gemma 5b completee.": {
        "en": "Code review by Gemma 5B completed.",
        "sw": "Ukaguzi wa msimbo na Gemma 5B umekamilika.",
        "pt": "Revisão de código por Gemma 5B concluída.",
        "fr": "Revue de code par Gemma 5B complétée.",
    },
    "veuillez saisir du code a analyser.": {
        "en": "Please enter code to analyze.",
        "sw": "Tafadhali ingiza msimbo wa kuchambua.",
        "pt": "Por favor, insira o código a analisar.",
        "fr": "Veuillez saisir du code à analyser.",
    },
    "veuillez saisir du code pour l'audit ia.": {
        "en": "Please enter code for AI audit.",
        "sw": "Tafadhali ingiza msimbo kwa ukaguzi wa AI.",
        "pt": "Por favor, insira o código para a auditoria de IA.",
        "fr": "Veuillez saisir du code pour l'audit IA.",
    },
    "scan en cours...": {
        "en": "Scan in progress...",
        "sw": "Uchambuzi unaendelea...",
        "pt": "Análise em curso...",
        "fr": "Scan en cours...",
    },
    "analyse par le moteur de securite souverain...": {
        "en": "Analysis by sovereign security engine...",
        "sw": "Uchambuzi unafanywa na injini huru ya usalama...",
        "pt": "Análise pelo motor de segurança soberano...",
        "fr": "Analyse par le moteur de sécurité souverain...",
    },
    "scan termine ! score de souverainete :": {
        "en": "Scan completed! Sovereignty score:",
        "sw": "Uchambuzi umekamilika! Alama ya mamlaka:",
        "pt": "Análise concluída! Pontuação de soberania:",
        "fr": "Scan terminé ! Score de souveraineté :",
    },
    "termine": {"en": "Completed", "sw": "Imekamilika", "pt": "Concluído", "fr": "Terminé"},
    "erreur": {"en": "Error", "sw": "Hitilafu", "pt": "Erro", "fr": "Erreur"},
    "erreur du scanner :": {
        "en": "Scanner error:",
        "sw": "Hitilafu ya skana:",
        "pt": "Erro do scanner:",
        "fr": "Erreur du scanner :",
    },
    "erreur de connexion ia :": {
        "en": "AI connection error:",
        "sw": "Hitilafu ya muunganisho wa AI:",
        "pt": "Erro de ligação de IA:",
        "fr": "Erreur de connexion IA :",
    },
    # Metrics & Datacenters
    "hote principal du moteur git souverain gitea, cluster postgresql replique et api bantudevlab.": {
        "en": "Primary host of sovereign Git engine Gitea, replicated PostgreSQL cluster and BantuDevLab API.",
        "sw": "Mwenyeji mkuu wa injini huru ya Git Gitea, nguzo ya PostgreSQL iliyorudiwa na API ya BantuDevLab.",
        "pt": "Hospedeiro principal do motor Git soberano Gitea, cluster PostgreSQL replicado e API BantuDevLab.",
        "fr": "Hôte principal du moteur Git souverain Gitea, cluster PostgreSQL répliqué et API BantuDevLab.",
    },
    "certifie tier-3 souverain": {
        "en": "CERTIFIED TIER-3 SOVEREIGN",
        "sw": "IMETHIBITISHWA TIER-3 HURU",
        "pt": "CERTIFICADO TIER-3 SOBERANO",
        "fr": "CERTIFIÉ TIER-3 SOUVERAIN",
    },
    "latence locale": {
        "en": "Local Latency",
        "sw": "Muda wa Kuchelewa wa Ndani",
        "pt": "Latência Local",
        "fr": "Latence Locale",
    },
    "bande passante ixp": {
        "en": "IXP Bandwidth",
        "sw": "Upana wa Bendi ya IXP",
        "pt": "Largura de Banda IXP",
        "fr": "Bande Passante IXP",
    },
    "protection legale": {
        "en": "Legal Protection",
        "sw": "Ulinzi wa Kisheria",
        "pt": "Proteção Legal",
        "fr": "Protection Légale",
    },
    "disponibilite sla": {
        "en": "SLA Availability",
        "sw": "Upatikanaji wa SLA",
        "pt": "Disponibilidade SLA",
        "fr": "Disponibilité SLA",
    },
    "localisation des donnees & hebergement": {
        "en": "Data Location & Hosting",
        "sw": "Mahali pa Data & Uhifadhi",
        "pt": "Localização de Dados & Hospedagem",
        "fr": "Localisation des Données & Hébergement",
    },
    "les serveurs git, bases de donnees relationnelles postgresql et sauvegardes sont heberges sur l'infrastructure systalink cloud en cote d'ivoire et au senegal.": {
        "en": "Git servers, PostgreSQL relational databases and backups are hosted on Systalink Cloud infrastructure in Ivory Coast and Senegal.",
        "sw": "Seva za Git, hifadhidata za PostgreSQL na nakala rudufu zinahifadhiwa kwenye miundombinu ya Systalink Cloud nchini Ivory Coast na Senegal.",
        "pt": "Os servidores Git, bases de dados relacionais PostgreSQL e cópias de segurança são hospedados na infraestrutura Systalink Cloud na Costa do Marfim e no Senegal.",
        "fr": "Les serveurs Git, bases de données relationnelles PostgreSQL et sauvegardes sont hébergés sur l'infrastructure Systalink Cloud en Côte d'Ivoire et au Sénégal.",
    },
    "statut : 100% souverain": {
        "en": "Status: 100% Sovereign",
        "sw": "Hali: 100% Huru",
        "pt": "Estado: 100% Soberano",
        "fr": "Statut : 100% Souverain",
    },
    "immunite totale face au cloud act et aux juridictions extraterritoriales.": {
        "en": "Total immunity against the CLOUD Act and extraterritorial jurisdictions.",
        "sw": "Kinga kamili dhidi ya Sheria ya CLOUD na mamlaka za kigeni.",
        "pt": "Imunidade total perante o CLOUD Act e jurisdições extraterritoriais.",
        "fr": "Immunité totale face au CLOUD Act et aux juridictions extraterritoriales.",
    },
    "cryptographie zero-knowledge (zkp)": {
        "en": "Zero-Knowledge Cryptography (ZKP)",
        "sw": "Kriptografia ya Maarifa Sifuri (ZKP)",
        "pt": "Criptografia de Conhecimento Zero (ZKP)",
        "fr": "Cryptographie Zero-Knowledge (ZKP)",
    },
    "preuves de schnorr non-interactives basees sur fiat-shamir garantissant une authentification a divulgation nulle de connaissance. meme en cas de compromission serveur, aucun mot de passe n'existe.": {
        "en": "Non-interactive Schnorr proofs based on Fiat-Shamir ensuring zero-knowledge authentication. Even in the event of server compromise, no password exists.",
        "sw": "Uthibitisho wa Schnorr kupitia Fiat-Shamir unaohakikisha uingiaji wa maarifa sifuri. Hata seva ikivamiwa, hakuna nenosiri linalopatikana.",
        "pt": "Provas de Schnorr não interativas baseadas em Fiat-Shamir garantindo autenticação de conhecimento zero. Mesmo em caso de invasão do servidor, não existe senha.",
        "fr": "Preuves de Schnorr non-interactives basées sur Fiat-Shamir garantissant une authentification à divulgation nulle de connaissance. Même en cas de compromission serveur, aucun mot de passe n'existe.",
    },
    "statut : cryptographiquement inviolable": {
        "en": "Status: Cryptographically Unbreakable",
        "sw": "Hali: Haiwezi Kuvunjwa Kikriptografia",
        "pt": "Estado: Criptograficamente Inviolável",
        "fr": "Statut : Cryptographiquement inviolable",
    },
    "aucune empreinte secrete conservee.": {
        "en": "No secret imprint retained.",
        "sw": "Hakuna alama ya siri inayohifadhiwa.",
        "pt": "Nenhuma marca secreta guardada.",
        "fr": "Aucune empreinte secrète conservée.",
    },
    "intelligence artificielle locale (gemma 5b)": {
        "en": "Local Artificial Intelligence (Gemma 5B)",
        "sw": "Akili Bandia ya Ndani (Gemma 5B)",
        "pt": "Inteligência Artificial Local (Gemma 5B)",
        "fr": "Intelligence Artificielle Locale (Gemma 5B)",
    },
    "modele de fondation gemma 5b fine-tune sur les depots de code et besoins d'infrastructures telecoms/fintech africaines. execution 100% on-premise / local.": {
        "en": "Gemma 5B foundation model fine-tuned on code repositories and African telecoms/fintech infrastructure needs. 100% On-Premise / Local execution.",
        "sw": "Mfano wa msingi wa Gemma 5B uliofunzwa kwa hazina za msimbo na miundombinu ya simu/fintech ya Kiafrika. Utekelezaji wa 100% wa ndani.",
        "pt": "Modelo de fundação Gemma 5B ajustado para repositórios de código e infraestruturas africanas de telecomunicações/fintech. Execução 100% local / on-premise.",
        "fr": "Modèle de fondation Gemma 5B fine-tuné sur les dépôts de code et besoins d'infrastructures télécoms/fintech africaines. Exécution 100% On-Premise / Local.",
    },
    "statut : zero fuite de telemetrie": {
        "en": "Status: Zero Telemetry Leak",
        "sw": "Hali: Hakuna Uvujaji wa Takwimu",
        "pt": "Estado: Zero Fuga de Telemetria",
        "fr": "Statut : Zéro fuite de télémétrie",
    },
    "vos algorithmes critiques restent strictement confidentiels.": {
        "en": "Your critical algorithms remain strictly confidential.",
        "sw": "Mifumo yako nyeti inabaki kuwa siri kabisa.",
        "pt": "Os seus algoritmos críticos permanecem estritamente confidenciais.",
        "fr": "Vos algorithmes critiques restent strictement confidentiels.",
    },
    # Login / ZKP Wizard
    "assistant d'identite & connexion zero-trust": {
        "en": "Identity Assistant & Zero-Trust Login",
        "sw": "Msaidizi wa Utambulisho & Kuingia Zero-Trust",
        "pt": "Assistente de Identidade & Login Zero-Trust",
        "fr": "Assistant d'Identité & Connexion Zero-Trust",
    },
    "protocole schnorr nizkp / fiat-shamir": {
        "en": "SCHNORR NIZKP / FIAT-SHAMIR PROTOCOL",
        "sw": "ITIFAKI YA SCHNORR NIZKP / FIAT-SHAMIR",
        "pt": "PROTOCOLO SCHNORR NIZKP / FIAT-SHAMIR",
        "fr": "PROTOCOLE SCHNORR NIZKP / FIAT-SHAMIR",
    },
    "generez votre cle souveraine protegee par mnemonique bip-39 et prouvez mathematiquement votre identite sans jamais exposer de mot de passe.": {
        "en": "Generate your sovereign key protected by BIP-39 mnemonic and mathematically prove your identity without ever exposing passwords.",
        "sw": "Tengeneza ufunguo wako huru unaolindwa na maneno ya BIP-39 na uthibitishe utambulisho wako bila kuweka wazi nenosiri.",
        "pt": "Gere a sua chave soberana protegida por mnemónica BIP-39 e prove matematicamente a sua identidade sem nunca expor senhas.",
        "fr": "Générez votre clé souveraine protégée par mnémonique BIP-39 et prouvez mathématiquement votre identité sans jamais exposer de mot de passe.",
    },
    "identite": {"en": "Identity", "sw": "Utambulisho", "pt": "Identidade", "fr": "Identité"},
    "mnemonique": {"en": "Mnemonic", "sw": "Mnemonic", "pt": "Mnemónica", "fr": "Mnémonique"},
    "zero-trust auth": {
        "en": "Zero-Trust Auth",
        "sw": "Uthibitishaji Zero-Trust",
        "pt": "Autenticação Zero-Trust",
        "fr": "Zero-Trust Auth",
    },
    "nom de developpeur souverain (username) :": {
        "en": "Sovereign Developer Username:",
        "sw": "Jina la Msanidi Huru (Username):",
        "pt": "Nome de Utilizador Desenvolvedor Soberano:",
        "fr": "Nom de Développeur Souverain (Username) :",
    },
    "juridiction continentale (noeud souverain) :": {
        "en": "Continental Jurisdiction (Sovereign Node):",
        "sw": "Mamlaka ya Bara (Nodi Huru):",
        "pt": "Jurisdição Continental (Nó Soberano):",
        "fr": "Juridiction Continentale (Nœud Souverain) :",
    },
    "suivant : generer la cle souveraine": {
        "en": "Next: Generate Sovereign Key",
        "sw": "Ifuatayo: Tengeneza Ufunguo Huru",
        "pt": "Seguinte: Gerar Chave Soberana",
        "fr": "Suivant : Générer la Clé Souveraine",
    },
    "force cryptographique :": {
        "en": "Cryptographic Strength:",
        "sw": "Nguvu ya Kriptografia:",
        "pt": "Força Criptográfica:",
        "fr": "Force Cryptographique :",
    },
    "inviolable (256 bits)": {
        "en": "Unbreakable (256 bits)",
        "sw": "Haiwezi Kuvunjwa (biti 256)",
        "pt": "Inviolável (256 bits)",
        "fr": "Inviolable (256 bits)",
    },
    "authentification decentralisee prete": {
        "en": "Decentralized Authentication Ready",
        "sw": "Uthibitishaji wa Ugatuzi Uko Tayari",
        "pt": "Autenticação Descentralizada Pronta",
        "fr": "Authentification Décentralisée Prête",
    },
    "calcul de la preuve fiat-shamir et interrogation du serveur...": {
        "en": "Computing Fiat-Shamir proof and querying server...",
        "sw": "Inahesabu uthibitisho wa Fiat-Shamir na kuita seva...",
        "pt": "A calcular a prova Fiat-Shamir e a consultar o servidor...",
        "fr": "Calcul de la preuve Fiat-Shamir et interrogation du serveur...",
    },
    "prouver & se connecter avec zkp": {
        "en": "Prove & Log In with ZKP",
        "sw": "Thibitisha & Ingia na ZKP",
        "pt": "Provar & Iniciar Sessão com ZKP",
        "fr": "Prouver & Se Connecter avec ZKP",
    },
    # Notifications, Toasts & Messages Dynamiques (JS)
    "fermer": {"en": "Close", "sw": "Funga", "pt": "Fechar", "fr": "Fermer"},
    "theme clair active": {
        "en": "Light theme activated",
        "sw": "Mandhari meupe yamewashwa",
        "pt": "Tema claro ativado",
        "fr": "Thème clair activé",
    },
    "theme sombre active": {
        "en": "Dark theme activated",
        "sw": "Mandhari meusi yamewashwa",
        "pt": "Tema escuro ativado",
        "fr": "Thème sombre activé",
    },
    "code de demonstration recharge.": {
        "en": "Demo code reloaded.",
        "sw": "Msimbo wa mfano umepakiwa tena.",
        "pt": "Código de demonstração recarregado.",
        "fr": "Code de démonstration rechargé.",
    },
    "aucune vulnerabilite detectee !": {
        "en": "No vulnerability detected!",
        "sw": "Hakuna udhaifu uliogunduliwa!",
        "pt": "Nenhuma vulnerabilidade detetada!",
        "fr": "Aucune vulnérabilité détectée !",
    },
    "le code respecte strictement les criteres de souverainete panafricaine.": {
        "en": "The code strictly complies with Pan-African sovereignty criteria.",
        "sw": "Msimbo unazingatia kikamilifu vigezo vya uhuru wa Afrika.",
        "pt": "O código cumpre estritamente os critérios de soberania pan-africana.",
        "fr": "Le code respecte strictement les critères de souveraineté panafricaine.",
    },
    "vulnerabilite": {"en": "Vulnerability", "sw": "Udhaifu", "pt": "Vulnerabilidade", "fr": "Vulnérabilité"},
    "ligne": {"en": "Line", "sw": "Mstari", "pt": "Linha", "fr": "Ligne"},
    "recommandation souveraine :": {
        "en": "Sovereign Recommendation:",
        "sw": "Mapendekezo Huru:",
        "pt": "Recomendação Soberana:",
        "fr": "Recommandation Souveraine :",
    },
    "erreur lors du scan": {
        "en": "Error during scan",
        "sw": "Hitilafu wakati wa ukaguzi",
        "pt": "Erro durante a verificação",
        "fr": "Erreur lors du scan",
    },
    "probleme(s) identifie(s)": {
        "en": "issue(s) identified",
        "sw": "matatizo yaliyotambuliwa",
        "pt": "problema(s) identificado(s)",
        "fr": "problème(s) identifié(s)",
    },
    "veuillez saisir du code pour l audit ia.": {
        "en": "Please enter code for AI audit.",
        "sw": "Tafadhali weka msimbo kwa ukaguzi wa AI.",
        "pt": "Por favor, insira o código para a auditoria IA.",
        "fr": "Veuillez saisir du code pour l'audit IA.",
    },
    "erreur de connexion ia: http": {
        "en": "AI connection error: HTTP",
        "sw": "Hitilafu ya muunganisho wa AI: HTTP",
        "pt": "Erro de ligação IA: HTTP",
        "fr": "Erreur de connexion IA: HTTP",
    },
    "erreur lors du streaming sse:": {
        "en": "Error during SSE streaming:",
        "sw": "Hitilafu wakati wa utiririshaji wa SSE:",
        "pt": "Erro durante a transmissão SSE:",
        "fr": "Erreur lors du streaming SSE:",
    },
    "erreur sse:": {"en": "SSE Error:", "sw": "Hitilafu ya SSE:", "pt": "Erro SSE:", "fr": "Erreur SSE:"},
    "noeud selectionne :": {
        "en": "Selected node:",
        "sw": "Nodi iliyochaguliwa:",
        "pt": "Nó selecionado:",
        "fr": "Nœud sélectionné :",
    },
    "mesure de la latence reseau en temps reel (ping rtt)...": {
        "en": "Measuring real-time network latency (Ping RTT)...",
        "sw": "Inapima muda wa mtandao kwa wakati halisi (Ping RTT)...",
        "pt": "A medir a latência da rede em tempo real (Ping RTT)...",
        "fr": "Mesure de la latence réseau en temps réel (Ping RTT)...",
    },
    "latence mesuree en temps reel : rtt local": {
        "en": "Real-time latency measured: local RTT",
        "sw": "Muda wa mtandao umepimwa: RTT ya ndani",
        "pt": "Latência medida em tempo real: RTT local",
        "fr": "Latence mesurée en temps réel : RTT local",
    },
    "latence directe rtt :": {
        "en": "Direct RTT latency:",
        "sw": "Muda wa moja kwa moja wa RTT:",
        "pt": "Latência direta RTT:",
        "fr": "Latência directe RTT :",
    },
    "actualisation des metriques souveraines...": {
        "en": "Refreshing sovereign metrics...",
        "sw": "Inasasisha vipimo huru...",
        "pt": "A atualizar métricas soberanas...",
        "fr": "Actualisation des métriques souveraines...",
    },
    "metriques et latences actualisees en direct.": {
        "en": "Metrics and latencies updated live.",
        "sw": "Vipimo na muda wa mawasiliano vimesasishwa moja kwa moja.",
        "pt": "Métricas e latências atualizadas em direto.",
        "fr": "Métriques et latences actualisées en direct.",
    },
    "copie !": {"en": "Copied!", "sw": "Imenakiliwa!", "pt": "Copiado!", "fr": "Copié !"},
    "phrase de 12 mots copiee !": {
        "en": "12-word phrase copied!",
        "sw": "Maneno 12 yamenakiliwa!",
        "pt": "Frase de 12 palavras copiada!",
        "fr": "Phrase de 12 mots copiée !",
    },
    "copier la phrase": {"en": "Copy phrase", "sw": "Nakili maneno", "pt": "Copiar frase", "fr": "Copier la phrase"},
    "mot": {"en": "Word", "sw": "Neno", "pt": "Palavra", "fr": "Mot"},
    "identifiant obligatoire (3-32 caracteres : lettres, chiffres, point, tiret).": {
        "en": "Username required (3-32 chars: letters, digits, dot, hyphen).",
        "sw": "Jina la mtumiaji linahitajika (herufi 3-32: herufi, nambari, nukta).",
        "pt": "Identificador obrigatório (3-32 caracteres: letras, números, ponto, hífen).",
        "fr": "Identifiant obligatoire (3-32 caractères : lettres, chiffres, point, tiret).",
    },
    "identifiant invalide : les espaces sont interdits.": {
        "en": "Invalid username: spaces are not allowed.",
        "sw": "Jina la mtumiaji si sahihi: nafasi haziruhusiwi.",
        "pt": "Identificador inválido: espaços não são permitidos.",
        "fr": "Identifiant invalide : les espaces sont interdits.",
    },
    "identifiant invalide : doit comporter 3 a 32 caracteres autorises.": {
        "en": "Invalid username: must contain 3 to 32 allowed characters.",
        "sw": "Jina la mtumiaji si sahihi: lazima liwe na herufi 3 hadi 32 zinazoruhusiwa.",
        "pt": "Identificador inválido: deve conter de 3 a 32 caracteres permitidos.",
        "fr": "Identifiant invalide : doit comporter 3 à 32 caractères autorisés.",
    },
    "nouvelle phrase mnemonique generee (12 mots).": {
        "en": "New mnemonic phrase generated (12 words).",
        "sw": "Maneno mapya ya siri yametengenezwa (maneno 12).",
        "pt": "Nova frase mnemónica gerada (12 palavras).",
        "fr": "Nouvelle phrase mnémonique générée (12 mots).",
    },
    "vide": {"en": "Empty", "sw": "Tupu", "pt": "Vazio", "fr": "Vide"},
    "inviolable souverain": {
        "en": "Sovereign Unbreakable",
        "sw": "Huru Isiyovunjika",
        "pt": "Soberano Inviolável",
        "fr": "Inviolable Souverain",
    },
    "fort": {"en": "Strong", "sw": "Imara", "pt": "Forte", "fr": "Fort"},
    "moyen": {"en": "Medium", "sw": "Wastani", "pt": "Médio", "fr": "Moyen"},
    "faible": {"en": "Weak", "sw": "Dhaifu", "pt": "Fraco", "fr": "Faible"},
    "veuillez renseigner votre identifiant et votre secret.": {
        "en": "Please enter your username and your secret.",
        "sw": "Tafadhali weka jina lako la mtumiaji na siri yako.",
        "pt": "Por favor, preencha o seu identificador e o seu segredo.",
        "fr": "Veuillez renseigner votre identifiant et votre secret.",
    },
    "identite souveraine telechargee :": {
        "en": "Sovereign identity downloaded:",
        "sw": "Utambulisho huru umepakuliwa:",
        "pt": "Identidade soberana transferida:",
        "fr": "Identité souveraine téléchargée :",
    },
    "fichier d identite souveraine exporte pour": {
        "en": "Sovereign identity file exported for",
        "sw": "Faili ya utambulisho huru imehamishwa kwa",
        "pt": "Ficheiro de identidade soberana exportado para",
        "fr": "Fichier d'identité souveraine exporté pour",
    },
    "derivation de la cle publique souveraine pour": {
        "en": "Deriving sovereign public key for",
        "sw": "Inatengeneza ufunguo wa umma huru kwa",
        "pt": "Derivação da chave pública soberana para",
        "fr": "Dérivation de la clé publique souveraine pour",
    },
    "cle publique (y = g^x mod p) generee localement.": {
        "en": "Public key (y = g^x mod p) generated locally.",
        "sw": "Ufunguo wa umma (y = g^x mod p) umetengenezwa ndani ya kifaa.",
        "pt": "Chave pública (y = g^x mod p) gerada localmente.",
        "fr": "Clé publique (y = g^x mod p) générée localement.",
    },
    "enregistrement zkp reussi ! aucune information secrete n a quitte votre machine.": {
        "en": "ZKP registration successful! No secret information left your machine.",
        "sw": "Usajili wa ZKP umefanikiwa! Hakuna taarifa ya siri iliyotoka kwenye kifaa chako.",
        "pt": "Registo ZKP bem-sucedido! Nenhuma informação secreta saiu da sua máquina.",
        "fr": "Enregistrement ZKP réussi ! Aucune information secrète n'a quitté votre machine.",
    },
    "identite zkp enregistree avec succes !": {
        "en": "ZKP identity registered successfully!",
        "sw": "Utambulisho wa ZKP umesajiliwa kwa mafanikio!",
        "pt": "Identidade ZKP registada com sucesso!",
        "fr": "Identité ZKP enregistrée avec succès !",
    },
    "erreur d enregistrement": {
        "en": "Registration error",
        "sw": "Hitilafu ya usajili",
        "pt": "Erro de registo",
        "fr": "Erreur d'enregistrement",
    },
    "erreur :": {"en": "Error:", "sw": "Hitilafu:", "pt": "Erro:", "fr": "Erreur :"},
    "echec de l enregistrement": {
        "en": "Registration failed",
        "sw": "Usajili umeshindwa",
        "pt": "Falha no registo",
        "fr": "Échec de l'enregistrement",
    },
    "demande d un defi (challenge nonce) au serveur pour": {
        "en": "Requesting challenge nonce from server for",
        "sw": "Inaomba changamoto (nonce) kutoka kwa seva kwa",
        "pt": "A solicitar desafio (Challenge nonce) ao servidor para",
        "fr": "Demande d'un défi (Challenge nonce) au serveur pour",
    },
    "erreur defi:": {
        "en": "Challenge error:",
        "sw": "Hitilafu ya changamoto:",
        "pt": "Erro de desafio:",
        "fr": "Erreur défi:",
    },
    "challenge recu :": {
        "en": "Challenge received:",
        "sw": "Changamoto imepokelewa:",
        "pt": "Desafio recebido:",
        "fr": "Challenge reçu :",
    },
    "preuve (t, s) calculee. envoi de la preuve au serveur pour verification...": {
        "en": "Proof (t, s) computed. Sending proof to server for verification...",
        "sw": "Uthibitisho (t, s) umehesabiwa. Inatuma uthibitisho kwa seva kuhakikiwa...",
        "pt": "Prova (t, s) calculada. A enviar prova ao servidor para verificação...",
        "fr": "Preuve (t, s) calculée. Envoi de la preuve au serveur pour vérification...",
    },
    "verification zero-knowledge reussie !": {
        "en": "Zero-Knowledge Verification Successful!",
        "sw": "Uthibitishaji wa Zero-Knowledge Umefanikiwa!",
        "pt": "Verificação Zero-Knowledge Bem-sucedida!",
        "fr": "Vérification Zero-Knowledge Réussie !",
    },
    "acces autorise sans mot de passe.": {
        "en": "Passwordless access granted.",
        "sw": "Ufikiaji umeruhusiwa bila nenosiri.",
        "pt": "Acesso autorizado sem senha.",
        "fr": "Accès autorisé sans mot de passe.",
    },
    "connexion zero-trust reussie pour": {
        "en": "Zero-Trust login successful for",
        "sw": "Kuingia kwa Zero-Trust kumefanikiwa kwa",
        "pt": "Login Zero-Trust bem-sucedido para",
        "fr": "Connexion Zero-Trust réussie pour",
    },
    "echec de la verification :": {
        "en": "Verification failed:",
        "sw": "Uthibitishaji umeshindwa:",
        "pt": "Falha na verificação:",
        "fr": "Échec de la vérification :",
    },
    "echec verification zkp :": {
        "en": "ZKP verification failed:",
        "sw": "Uthibitishaji wa ZKP umeshindwa:",
        "pt": "Falha na verificação ZKP:",
        "fr": "Échec vérification ZKP :",
    },
    "prouver mon identite (connexion zero-trust)": {
        "en": "Prove My Identity (Zero-Trust Login)",
        "sw": "Thibitisha Utambulisho Wangu (Kuingia Zero-Trust)",
        "pt": "Provar a Minha Identidade (Login Zero-Trust)",
        "fr": "Prouver mon Identité (Connexion Zero-Trust)",
    },
    "regenerer (12 mots)": {
        "en": "Regenerate (12 Words)",
        "sw": "Tengeneza Upya (Maneno 12)",
        "pt": "Regenerar (12 Palavras)",
        "fr": "Regénérer (12 Mots)",
    },
    "phrase mnemonique souveraine (standard bip-39) :": {
        "en": "Sovereign Mnemonic Phrase (BIP-39 Standard):",
        "sw": "Maneno ya Siri Huru (Kiwango cha BIP-39):",
        "pt": "Frase Mnemónica Soberana (Padrão BIP-39):",
        "fr": "Phrase Mnémonique Souveraine (Standard BIP-39) :",
    },
    "ces 12 mots permettent de regenerer mathematiquement votre cle privee de signature zkp dans n'importe quel terminal securise.": {
        "en": "These 12 words mathematically regenerate your ZKP private signing key in any secure terminal.",
        "sw": "Maneno haya 12 yanakuwezesha kutengeneza upya ufunguo wako wa siri wa ZKP kwenye kifaa chochote salama.",
        "pt": "Estas 12 palavras permitem regenerar matematicamente a sua chave privada de assinatura ZKP em qualquer terminal seguro.",
        "fr": "Ces 12 mots permettent de régénérer mathématiquement votre clé privée de signature ZKP dans n'importe quel terminal sécurisé.",
    },
    "secret prive derive (ne quitte jamais votre navigateur) :": {
        "en": "Derived Private Secret (NEVER leaves your browser):",
        "sw": "Siri Binafsi Iliyotokana (HAIWAHI kutoka kwenye kivinjari chako):",
        "pt": "Segredo Privado Derivado (NUNCA sai do seu navegador):",
        "fr": "Secret Privé Dérivé (Ne quitte JAMAIS votre navigateur) :",
    },
    "telecharger fichier cle souveraine (.json)": {
        "en": "Download Sovereign Key File (.json)",
        "sw": "Pakua Faili ya Ufunguo Huru (.json)",
        "pt": "Transferir Ficheiro Chave Soberana (.json)",
        "fr": "Télécharger Fichier Clé Souveraine (.json)",
    },
    "enregistrer identite sur bantudevlab": {
        "en": "Register Identity on BantuDevLab",
        "sw": "Sajili Utambulisho kwenye BantuDevLab",
        "pt": "Registar Identidade no BantuDevLab",
        "fr": "Enregistrer Identité sur BantuDevLab",
    },
    "precedent": {"en": "Previous", "sw": "Iliyotangulia", "pt": "Anterior", "fr": "Précédent"},
    "passer a la connexion": {
        "en": "Proceed to Login",
        "sw": "Endelea Kuingia",
        "pt": "Avançar para o Login",
        "fr": "Passer à la Connexion",
    },
    "lors du clic, votre navigateur resout un defi cryptographique avec votre cle privee locale pour prouver la possession de la cle sans jamais la devoiler au serveur.": {
        "en": "When clicked, your browser solves a cryptographic challenge with your local private key to prove key possession without ever revealing it to the server.",
        "sw": "Unapobonyeza, kivinjari chako kinatatua changamoto ya kriptografia kwa ufunguo wako wa siri ili kuthibitisha umiliki bila kuufichua kwa seva.",
        "pt": "Ao clicar, o seu navegador resolve um desafio criptográfico com a sua chave privada local para provar a posse da chave sem nunca a revelar ao servidor.",
        "fr": "Lors du clic, votre navigateur résout un défi cryptographique avec votre clé privée locale pour prouver la possession de la clé sans jamais la dévoiler au serveur.",
    },
    "revenir au mnemonique": {
        "en": "Back to Mnemonic",
        "sw": "Rudi kwenye Maneno ya Siri",
        "pt": "Voltar à Mnemónica",
        "fr": "Revenir au Mnémonique",
    },
    "votre identite souveraine": {
        "en": "Your sovereign identity",
        "sw": "Utambulisho wako huru",
        "pt": "A sua identidade soberana",
        "fr": "Votre identité souveraine",
    },
    "est authentifiee sans mot de passe. finalisez ou liez votre compte sur la forge gitea souveraine.": {
        "en": "is authenticated without password. Complete or link your account on the sovereign Gitea forge.",
        "sw": "imethibitishwa bila nenosiri. Kamilisha au unganisha akaunti yako kwenye Gitea huru.",
        "pt": "está autenticada sem senha. Finalize ou associe a sua conta na forja Gitea soberana.",
        "fr": "est authentifiée sans mot de passe. Finalisez ou liez votre compte sur la forge Gitea souveraine.",
    },
    "redirection automatique vers l'inscription gitea dans": {
        "en": "Automatic redirection to Gitea registration in",
        "sw": "Inaelekeza kiotomatiki kwenye usajili wa Gitea ndani ya",
        "pt": "Redirecionamento automático para o registo Gitea em",
        "fr": "Redirection automatique vers l'inscription Gitea dans",
    },
    "secondes...": {"en": "seconds...", "sw": "sekunde...", "pt": "segundos...", "fr": "secondes..."},
}


def normalize_key(s):
    # Enlève les accents, met en minuscule, normalise les espaces
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def extract_template_strings():
    templates_dir = BASE / "templates"
    extracted = []
    # Scanne tous les fichiers HTML
    for p in templates_dir.rglob("*.html"):
        content = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'\{%\s*trans\s+[\'"](.*?)[\'"]\s*%\}', content, re.DOTALL):
            s = m.group(1).strip()
            if s:
                extracted.append(s)
        for m in re.finditer(r"\{%\s*blocktrans(?:\s+.*?)?%\}(.*?)\{%\s*endblocktrans\s*%\}", content, re.DOTALL):
            s = m.group(1).strip()
            if s and not s.startswith("#"):
                extracted.append(" ".join(s.split()))
    return list(dict.fromkeys(extracted))


def read_po_file(po_path):
    catalog = {}
    if not po_path.exists():
        return catalog
    content = po_path.read_text(encoding="utf-8", errors="replace")
    # Parse entries
    pattern = r'msgid "((?:[^"\\]|\\.)*)"\nmsgstr "((?:[^"\\]|\\.)*)"'
    for m in re.finditer(pattern, content):
        mid = m.group(1).replace('\\"', '"').replace("\\\\", "\\")
        mstr = m.group(2).replace('\\"', '"').replace("\\\\", "\\")
        catalog[mid] = mstr
    return catalog


def translate_string(raw_str, lang, existing_catalog):
    # 1. Chercher d'abord dans NORM_DICT (pour appliquer les traductions exactes et corrigées)
    norm = normalize_key(raw_str)
    if norm in NORM_DICT:
        return NORM_DICT[norm].get(lang, raw_str)

    # 2. Si déjà dans le catalogue existant et non vide
    if raw_str in existing_catalog and existing_catalog[raw_str].strip():
        if lang == "fr":
            return raw_str
        return existing_catalog[raw_str]

    # 3. Chercher fuzzy dans NORM_DICT
    for k, trans in NORM_DICT.items():
        if k in norm or norm in k:
            if len(norm) > 10 and len(k) > 10:
                return trans.get(lang, raw_str)

    # 4. Fallback si FR
    if lang == "fr":
        return raw_str

    # 5. Fallback par défaut : conserver raw_str
    return raw_str


def write_po_file(po_path, lang, catalog):
    po_path.parent.mkdir(parents=True, exist_ok=True)
    header = f"""msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: {lang}\\n"
"MIME-Version: 1.0\\n"
"Content-Transfer-Encoding: 8bit\\n"

"""
    entries = []
    # Ordre alphabétique pour la reproductibilité
    for mid in sorted(catalog.keys()):
        if mid == "":
            continue
        mstr = catalog[mid]
        # Escape quotes and backslashes
        mid_esc = mid.replace("\\", "\\\\").replace('"', '\\"')
        mstr_esc = mstr.replace("\\", "\\\\").replace('"', '\\"')
        entries.append(f'msgid "{mid_esc}"\nmsgstr "{mstr_esc}"\n')

    full_text = header + "\n".join(entries) + "\n"
    po_path.write_text(full_text, encoding="utf-8")
    print(f"[{lang.upper()}] Écrit {len(catalog)} entrées dans {po_path.name}")


def main():
    print("=== SYNCHRONISATION MAÎTRE DE TOUTES LES TRADUCTIONS ===")
    template_strings = extract_template_strings()
    print(f"Total des chaînes trans uniques extraites des templates : {len(template_strings)}")

    languages = ["en", "sw", "pt", "fr"]

    for lang in languages:
        po_path = BASE / "locale" / lang / "LC_MESSAGES" / "django.po"
        mo_path = BASE / "locale" / lang / "LC_MESSAGES" / "django.mo"

        existing = read_po_file(po_path)

        # Créer le nouveau catalogue complet
        new_catalog = {}
        for s in template_strings:
            translated = translate_string(s, lang, existing)
            new_catalog[s] = translated

        # Conserver également toute chaîne existante dans le PO qui n'a pas été trouvée directement
        for k, v in existing.items():
            if k not in new_catalog and k != "":
                new_catalog[k] = v

        write_po_file(po_path, lang, new_catalog)

        # Compilation en MO
        try:
            compile_po_to_mo(str(po_path), str(mo_path))
            print(f"[{lang.upper()}] MO compilé avec succès !")
        except Exception as e:
            print(f"[{lang.upper()}] Erreur compilation MO : {e}")

    print("\n=== SYNCHRONISATION TERMINÉE AVEC SUCCÈS ===")


if __name__ == "__main__":
    main()
