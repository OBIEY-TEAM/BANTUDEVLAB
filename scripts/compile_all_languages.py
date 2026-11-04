import struct
from pathlib import Path

# Complete Translation Catalogs for BantuDevLab
TRANSLATIONS = {
    "en": {
        "Accueil": "Home",
        "Tableau de Bord": "Dashboard",
        "Souveraineté Numérique": "Digital Sovereignty",
        "Guide & FAQ": "Guide & FAQ",
        "Connexion Zero-Trust": "Zero-Trust Login",
        "Basculer vers Gitea": "Switch to Gitea",
        "Espace GitLab": "GitLab Workspace",
        "FORGE SOUVERAINE": "SOVEREIGN FORGE",
        "La Forge Logicielle Souveraine de l'Afrique": "The Pan-African Sovereign Software Forge",
        "BANTUDEVLAB réunit la robustesse d'un moteur Git distribué, la sécurité mathématique des preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs), et l'intelligence artificielle locale Gemma 5B pour garantir l'indépendance technologique du continent.": "BANTUDEVLAB combines the robustness of a distributed Git engine, the mathematical security of Zero-Knowledge Proofs, and local Gemma 5B AI to guarantee the continent's technological independence.",
        "Explorer le Tableau de Bord": "Explore Dashboard",
        "Authentification Zero-Trust (ZKP)": "Zero-Trust Authentication (ZKP)",
        "Mode d'Emploi & FAQ": "User Guide & FAQ",
        "Moteur Git Souverain (Systalink Cloud)": "Sovereign Git Engine (Systalink Cloud)",
        "Forge distribuée basée sur Gitea/GitLab CE déployée sur nos serveurs en Afrique. Zéro dépendance vis-à-vis des juridictions extérieures (Cloud Act exempt).": "Distributed forge based on Gitea/GitLab CE deployed on our African servers. Zero reliance on foreign jurisdictions (Cloud Act exempt).",
        "Connexion Gitea : http://localhost:3002/user/login": "Gitea Login : http://localhost:3002/user/login",
        "Contrôle Panafricain": "Pan-African Control",
        "Authentification Zero-Trust ZKP": "Zero-Trust ZKP Authentication",
        "Protocole cryptographique de Schnorr / Sigma non-interactif via Fiat-Shamir. Prouvez votre identité sans JAMAIS transmettre votre mot de passe au réseau.": "Cryptographic Schnorr / Sigma non-interactive protocol via Fiat-Shamir. Prove your identity without EVER transmitting your password over the network.",
        "Confidentialité Mathématique": "Mathematical Privacy",
        "IA Locale Gemma 5B Fine-tunée": "Fine-Tuned Local Gemma 5B AI",
        "Assistant d'ingénierie logicielle exécuté localement pour auditer le code, détecter les secrets et assister les développeurs sans fuite de code vers l'extérieur.": "Software engineering assistant running locally to audit code, detect secrets and assist developers with no external code leakage.",
        "5 Milliards": "5 Billion",
        "Milliards": "Billion",
        "Paramètres Optimisés": "Optimized Parameters",
        "Nouveau sur BANTUDEVLAB & GitLab ?": "New to BANTUDEVLAB & GitLab?",
        "Consultez notre guide complet : création de compte, connexion sans mot de passe Zero-Trust, consultation du code source, clone avec token Git et foire aux questions.": "Read our comprehensive guide: account creation, passwordless Zero-Trust login, source code browsing, cloning with Git token and FAQ.",
        "Consulter la FAQ & Guide": "Browse FAQ & Guide",
        "Dépôts Souverains Récents": "Recent Sovereign Repositories",
        "Initialisation de la synchronisation avec Gitea...": "Initializing synchronization with Gitea...",
        "Fil d Ariane": "Breadcrumbs",
        "Tableau de Bord Souverain BANTUDEVLAB": "BANTUDEVLAB Sovereign Dashboard",
        "Surveillance de la forge logicielle, sécurité Zero-Trust et assistance IA locale": "Software forge monitoring, Zero-Trust security and local AI assistance",
        "NŒUD SOUVERAIN ACTIF": "ACTIVE SOVEREIGN NODE",
        "Dépôts Actifs": "Active Repositories",
        "Identités ZKP": "ZKP Identities",
        "Score de Souveraineté": "Sovereignty Score",
        "Audits IA Gemma 5B": "Gemma 5B AI Audits",
        "Bascule d'Environnement Forge Souveraine": "Sovereign Forge Environment Switch",
        "Accédez directement à vos espaces de dépôts Gitea ou GitLab CE.": "Access directly your Gitea or GitLab CE repository workspaces.",
        "Connexion directe Gitea": "Direct Gitea Login",
        "Dépôts Hébergés sur Gitea Souverain": "Repositories Hosted on Sovereign Gitea",
        "Données Réelles Gitea API": "Real Gitea API Data",
        "Dépôt": "Repository",
        "Visibilité": "Visibility",
        "Branche": "Branch",
        "Action": "Action",
        "Gitea": "Gitea",
        "Aucun dépôt détecté sur le cluster Gitea local.": "No repository detected on local Gitea cluster.",
        "Lancer l'Audit de Sécurité": "Run Security Audit",
        "Indicateurs & Topologie Souveraine Panafricaine": "Pan-African Sovereign Indicators & Topology",
        "Supervision en temps réel des nœuds certifiés et conformité UA 2020-2030.": "Real-time supervision of certified nodes and AU 2020-2030 compliance.",
        "Tester la Latence": "Test Latency",
        "Actualiser les Métriques": "Refresh Metrics",
        "Topologie des Datacenters Certifiés": "Certified Datacenters Topology",
        "Cliquez sur un nœud ou une carte pour inspecter les métriques locales": "Click on a node or card to inspect local metrics",
        "Mesures de Latence Réelle Intra-Afrique (Temps Réel)": "Real Intra-Africa Latency Measurements (Real-Time)",
        "Nœud": "Node",
        "Ville": "City",
        "Pays": "Country",
        "Latence Réelle": "Real Latency",
        "Statut": "Status",
        "Changer de langue": "Change language",
        "Basculer thème clair / sombre": "Toggle light / dark theme",
        "Session authentifiée via Zero-Trust ZKP": "Session authenticated via Zero-Trust ZKP",
        "Menu de navigation": "Navigation menu"
    },
    "sw": {
        "Accueil": "Mwanzo",
        "Tableau de Bord": "Dashibodi",
        "Souveraineté Numérique": "Uhuru wa Kidijitali",
        "Guide & FAQ": "Mwongozo na Maswali",
        "Connexion Zero-Trust": "Kuingia kwa Zero-Trust",
        "Basculer vers Gitea": "Badilisha kwenda Gitea",
        "Espace GitLab": "Sehemu ya GitLab",
        "FORGE SOUVERAINE": "JUKWAA LA UHURU",
        "La Forge Logicielle Souveraine de l'Afrique": "Jukwaa la Maendeleo la Programu Huru la Afrika",
        "BANTUDEVLAB réunit la robustesse d'un moteur Git distribué, la sécurité mathématique des preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs), et l'intelligence artificielle locale Gemma 5B pour garantir l'indépendance technologique du continent.": "BANTUDEVLAB inachanganya uimara wa injini ya Git iliyosambazwa, usalama wa hisabati wa Uthibitisho Usio na Maarifa (ZKP), na akili bandia ya kienyeji ya Gemma 5B kulinda uhuru wa kiteknolojia wa bara.",
        "Explorer le Tableau de Bord": "Chunguza Dashibodi",
        "Authentification Zero-Trust (ZKP)": "Uthibitishaji wa Zero-Trust (ZKP)",
        "Mode d'Emploi & FAQ": "Mwongozo na Maswali",
        "Moteur Git Souverain (Systalink Cloud)": "Injini Huru ya Git (Systalink Cloud)",
        "Forge distribuée basée sur Gitea/GitLab CE déployée sur nos serveurs en Afrique. Zéro dépendance vis-à-vis des juridictions extérieures (Cloud Act exempt).": "Jukwaa lililosambazwa kulingana na Gitea/GitLab CE lililowekwa kwenye seva zetu za Afrika. Bila utegemezi wa nje.",
        "Connexion Gitea : http://localhost:3002/user/login": "Kuingia Gitea : http://localhost:3002/user/login",
        "Contrôle Panafricain": "Udhibiti wa Kiafrika",
        "Authentification Zero-Trust ZKP": "Uthibitishaji wa Zero-Trust ZKP",
        "Protocole cryptographique de Schnorr / Sigma non-interactif via Fiat-Shamir. Prouvez votre identité sans JAMAIS transmettre votre mot de passe au réseau.": "Itifaki ya siri ya Schnorr / Sigma bila kuingiliana kupitia Fiat-Shamir. Thibitisha utambulisho wako bila kuweka nenosiri.",
        "Confidentialité Mathématique": "Faragha ya Kihisabati",
        "IA Locale Gemma 5B Fine-tunée": "Akili Bandia ya Kienyeji ya Gemma 5B",
        "Assistant d'ingénierie logicielle exécuté localement pour auditer le code, détecter les secrets et assister les développeurs sans fuite de code vers l'extérieur.": "Msaidizi wa programu anayeendesha ndani kukagua msimbo na kusaidia watengenezaji bila kutoa data nje.",
        "5 Milliards": "Bilioni 5",
        "Milliards": "Bilioni",
        "Paramètres Optimisés": "Vigezo Vilivyoboreshwa",
        "Nouveau sur BANTUDEVLAB & GitLab ?": "Mgeni kwenye BANTUDEVLAB & GitLab?",
        "Consultez notre guide complet : création de compte, connexion sans mot de passe Zero-Trust, consultation du code source, clone avec token Git et foire aux questions.": "Soma mwongozo wetu: ufunguzi wa akaunti, kuingia bila nenosiri, kuvinjari msimbo na maswali.",
        "Consulter la FAQ & Guide": "Tazama Mwongozo & Maswali",
        "Dépôts Souverains Récents": "Hifadhi za Hivi Karibuni za Uhuru",
        "Initialisation de la synchronisation avec Gitea...": "Inaanzisha usawazishaji na Gitea...",
        "Fil d Ariane": "Njia ya Ukurasa",
        "Tableau de Bord Souverain BANTUDEVLAB": "Dashibodi Huru ya BANTUDEVLAB",
        "Surveillance de la forge logicielle, sécurité Zero-Trust et assistance IA locale": "Uangalizi wa jukwaa, usalama wa Zero-Trust na msaada wa AI",
        "NŒUD SOUVERAIN ACTIF": "KIPANDE CHA UHURU KILICHO HAI",
        "Dépôts Actifs": "Hifadhi Zinazofanya Kazi",
        "Identités ZKP": "Vitambulisho vya ZKP",
        "Score de Souveraineté": "Alama ya Uhuru",
        "Audits IA Gemma 5B": "Ukaguzi wa AI Gemma 5B",
        "Bascule d'Environnement Forge Souveraine": "Badilisha Mazingira ya Hifadhi",
        "Accédez directement à vos espaces de dépôts Gitea ou GitLab CE.": "Pata nafasi zako za hifadhi za Gitea au GitLab CE.",
        "Connexion directe Gitea": "Kuingia moja kwa moja Gitea",
        "Dépôts Hébergés sur Gitea Souverain": "Hifadhi Zilizowekwa kwenye Gitea Huru",
        "Données Réelles Gitea API": "Data Halisi ya API ya Gitea",
        "Dépôt": "Hifadhi",
        "Visibilité": "Mwonekano",
        "Branche": "Tawi",
        "Action": "Hatua",
        "Gitea": "Gitea",
        "Aucun dépôt détecté sur le cluster Gitea local.": "Hakuna hifadhi iliyopatikana kwenye mfumo wa ndani wa Gitea.",
        "Lancer l'Audit de Sécurité": "Anzisha Ukaguzi wa Usalama",
        "Indicateurs & Topologie Souveraine Panafricaine": "Viashiria na Muundo wa Uhuru wa Afrika",
        "Supervision en temps réel des nœuds certifiés et conformité UA 2020-2030.": "Uangalizi wa wakati halisi wa vituo vilivyothibitishwa.",
        "Tester la Latence": "Pima Muda wa Mawasiliano",
        "Actualiser les Métriques": "Sasisha Takwimu",
        "Topologie des Datacenters Certifiés": "Muundo wa Vituo vya Data Vilivyothibitishwa",
        "Cliquez sur un nœud ou une carte pour inspecter les métriques locales": "Bonyeza kituo kuona takwimu za mtaa",
        "Mesures de Latence Réelle Intra-Afrique (Temps Réel)": "Vipimo Halisi vya Muda wa Mawasiliano Barani Afrika",
        "Nœud": "Kituo",
        "Ville": "Mji",
        "Pays": "Nchi",
        "Latence Réelle": "Muda Halisi",
        "Statut": "Hali",
        "Changer de langue": "Badilisha lugha",
        "Basculer thème clair / sombre": "Badilisha mandhari meusi / meupe",
        "Session authentifiée via Zero-Trust ZKP": "Kipindi kimethibitishwa kupitia Zero-Trust ZKP",
        "Menu de navigation": "Menyu ya urambazaji"
    },
    "pt": {
        "Accueil": "Inicio",
        "Tableau de Bord": "Painel de Controle",
        "Souveraineté Numérique": "Soberania Digital",
        "Guide & FAQ": "Guia & FAQ",
        "Connexion Zero-Trust": "Login Zero-Trust",
        "Basculer vers Gitea": "Mudar para Gitea",
        "Espace GitLab": "Espaco GitLab",
        "FORGE SOUVERAINE": "FORJA SOBERANA",
        "La Forge Logicielle Souveraine de l'Afrique": "A Forja Soberana de Software da Africa",
        "BANTUDEVLAB réunit la robustesse d'un moteur Git distribué, la sécurité mathématique des preuves à divulgation nulle de connaissance (Zero-Knowledge Proofs), et l'intelligence artificielle locale Gemma 5B pour garantir l'indépendance technologique du continent.": "BANTUDEVLAB une a robustez de um motor Git distribuido, a seguranca matematica das Provas de Conhecimento Zero (ZKP), e a IA local Gemma 5B para garantir a independencia tecnologica do continente.",
        "Explorer le Tableau de Bord": "Explorar o Painel",
        "Authentification Zero-Trust (ZKP)": "Autenticacao Zero-Trust (ZKP)",
        "Mode d'Emploi & FAQ": "Guia de Uso & FAQ",
        "Moteur Git Souverain (Systalink Cloud)": "Motor Git Soberano (Systalink Cloud)",
        "Forge distribuée basée sur Gitea/GitLab CE déployée sur nos serveurs en Afrique. Zéro dépendance vis-à-vis des juridictions extérieures (Cloud Act exempt).": "Forja distribuida baseada em Gitea/GitLab CE implantada em servidores na Africa. Zero dependencia de jurisdicoes externas.",
        "Connexion Gitea : http://localhost:3002/user/login": "Login Gitea : http://localhost:3002/user/login",
        "Contrôle Panafricain": "Controle Pan-Africano",
        "Authentification Zero-Trust ZKP": "Autenticacao Zero-Trust ZKP",
        "Protocole cryptographique de Schnorr / Sigma non-interactif via Fiat-Shamir. Prouvez votre identité sans JAMAIS transmettre votre mot de passe au réseau.": "Protocolo criptografico de Schnorr / Sigma nao-interativo via Fiat-Shamir. Prove sua identidade sem NUNCA transmitir sua senha pela rede.",
        "Confidentialité Mathématique": "Privacidade Matematica",
        "IA Locale Gemma 5B Fine-tunée": "IA Local Gemma 5B Otimizada",
        "Assistant d'ingénierie logicielle exécuté localement pour auditer le code, détecter les secrets et assister les développeurs sans fuite de code vers l'extérieur.": "Assistente de engenharia de software executado localmente para auditar codigo sem vazamento de dados.",
        "5 Milliards": "5 Bilhoes",
        "Milliards": "Bilhoes",
        "Paramètres Optimisés": "Parametros Otimizados",
        "Nouveau sur BANTUDEVLAB & GitLab ?": "Novo no BANTUDEVLAB & GitLab?",
        "Consultez notre guide complet : création de compte, connexion sans mot de passe Zero-Trust, consultation du code source, clone avec token Git et foire aux questions.": "Consulte nosso guia completo: criacao de conta, login Zero-Trust sem senha, exploracao de codigo e FAQ.",
        "Consulter la FAQ & Guide": "Consultar Guia & FAQ",
        "Dépôts Souverains Récents": "Repositorios Soberanos Recentes",
        "Initialisation de la synchronisation avec Gitea...": "Inicializando sincronizacao com Gitea...",
        "Fil d Ariane": "Navegacao Estrutural",
        "Tableau de Bord Souverain BANTUDEVLAB": "Painel de Controle Soberano BANTUDEVLAB",
        "Surveillance de la forge logicielle, sécurité Zero-Trust et assistance IA locale": "Monitoramento da forja de software, seguranca Zero-Trust e assistencia IA",
        "NŒUD SOUVERAIN ACTIF": "NO SOBERANO ATIVO",
        "Dépôts Actifs": "Repositorios Ativos",
        "Identités ZKP": "Identidades ZKP",
        "Score de Souveraineté": "Pontuacao de Soberania",
        "Audits IA Gemma 5B": "Auditorias IA Gemma 5B",
        "Bascule d'Environnement Forge Souveraine": "Alternar Ambiente da Forja Soberana",
        "Accédez directement à vos espaces de dépôts Gitea ou GitLab CE.": "Acesse diretamente os espacos de repositorios Gitea ou GitLab CE.",
        "Connexion directe Gitea": "Login Direto Gitea",
        "Dépôts Hébergés sur Gitea Souverain": "Repositorios Hospedados no Gitea Soberano",
        "Données Réelles Gitea API": "Dados Reais da API Gitea",
        "Dépôt": "Repositorio",
        "Visibilité": "Visibilidade",
        "Branche": "Ramo",
        "Action": "Acao",
        "Gitea": "Gitea",
        "Aucun dépôt détecté sur le cluster Gitea local.": "Nenhum repositorio encontrado no cluster Gitea local.",
        "Lancer l'Audit de Sécurité": "Executar Auditoria de Seguranca",
        "Indicateurs & Topologie Souveraine Panafricaine": "Indicadores e Topologia Soberana Pan-Africana",
        "Supervision en temps réel des nœuds certifiés et conformité UA 2020-2030.": "Supervisao em tempo real dos nos certificados e conformidade UA.",
        "Tester la Latence": "Testar Latencia",
        "Actualiser les Métriques": "Atualizar Metricas",
        "Topologie des Datacenters Certifiés": "Topologia de Datacenters Certificados",
        "Cliquez sur un nœud ou une carte pour inspecter les métriques locales": "Clique em um no para inspecionar metricas locais",
        "Mesures de Latence Réelle Intra-Afrique (Temps Réel)": "Medicoes de Latencia Real Intra-Africa (Tempo Real)",
        "Nœud": "No",
        "Ville": "Cidade",
        "Pays": "Pais",
        "Latence Réelle": "Latencia Real",
        "Statut": "Status",
        "Changer de langue": "Alterar idioma",
        "Basculer thème clair / sombre": "Alternar tema claro / escuro",
        "Session authentifiée via Zero-Trust ZKP": "Sessao autenticada via Zero-Trust ZKP",
        "Menu de navigation": "Menu de navegacao"
    }
}

def generate_mo(entries):
    # Sort entries by msgid
    entries = sorted(entries.items(), key=lambda x: x[0])
    
    header = b"Content-Type: text/plain; charset=UTF-8\n"
    # Prepend empty string header
    all_keys = [b""] + [k.encode("utf-8") for k, _ in entries]
    all_vals = [header] + [v.encode("utf-8") for _, v in entries]

    N = len(all_keys)
    # Magic number for GNU gettext .mo (little endian)
    magic = 0x950412de
    version = 0
    O_strings = 28
    T_strings = O_strings + (N * 8)
    
    # Calculate tables
    orig_table = []
    trans_table = []
    
    data_start = T_strings + (N * 8)
    curr_offset = data_start
    
    encoded_data = b""
    for k in all_keys:
        orig_table.append((len(k), curr_offset))
        encoded_data += k + b"\x00"
        curr_offset += len(k) + 1
        
    for v in all_vals:
        trans_table.append((len(v), curr_offset))
        encoded_data += v + b"\x00"
        curr_offset += len(v) + 1
        
    header_bytes = struct.pack("<Iiiiiii", magic, version, N, O_strings, T_strings, 0, 0)
    
    orig_bytes = b"".join(struct.pack("<ii", l, o) for l, o in orig_table)
    trans_bytes = b"".join(struct.pack("<ii", l, o) for l, o in trans_table)
    
    return header_bytes + orig_bytes + trans_bytes + encoded_data

def build():
    for lang, catalog in TRANSLATIONS.items():
        lang_dir = Path("locale") / lang / "LC_MESSAGES"
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Write .po file
        po_lines = [
            'msgid ""',
            'msgstr ""',
            '"Content-Type: text/plain; charset=UTF-8\\n"',
            f'"Language: {lang}\\n"',
            ""
        ]
        for msgid, msgstr in catalog.items():
            po_lines.append(f'msgid "{msgid}"')
            po_lines.append(f'msgstr "{msgstr}"')
            po_lines.append("")
            
        po_path = lang_dir / "django.po"
        po_path.write_text("\n".join(po_lines), encoding="utf-8")
        
        # Write .mo file
        mo_data = generate_mo(catalog)
        mo_path = lang_dir / "django.mo"
        mo_path.write_bytes(mo_data)
        
        print(f"Generated {po_path} and {mo_path} ({len(catalog)} entries)")

if __name__ == "__main__":
    build()
