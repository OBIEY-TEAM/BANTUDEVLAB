import pathlib

root = pathlib.Path(r"c:/Users/User/Desktop/AGENT/BANTUDEVLAB")

# 1. Update templates/core/home.html
home_path = root / "templates/core/home.html"
home_text = home_path.read_bytes().decode("utf-8").replace("\r\n", "\n")
if "{% load i18n %}" not in home_text:
    home_text = home_text.replace("{% extends 'base.html' %}", "{% extends 'base.html' %}\n{% load i18n %}")
    home_path.write_bytes(home_text.replace("\n", "\r\n").encode("utf-8"))
    print("home.html patched")

# 2. Update templates/core/dashboard.html
dash_path = root / "templates/core/dashboard.html"
dash_text = dash_path.read_bytes().decode("utf-8").replace("\r\n", "\n")
if "{% load i18n %}" not in dash_text:
    dash_text = dash_text.replace("{% extends 'base.html' %}", "{% extends 'base.html' %}\n{% load i18n %}")

# Add breadcrumb in dashboard
breadcrumb_dash = """{% block content %}
<nav class="breadcrumbs" aria-label="{% trans 'Fil d Ariane' %}">
    <a href="{% url 'home' %}">{% icon "landmark" size=14 %} {% trans "Accueil" %}</a>
    <span class="breadcrumbs-separator">/</span>
    <span class="breadcrumbs-current" aria-current="page">{% trans "Tableau de Bord" %}</span>
</nav>
"""
if 'class="breadcrumbs"' not in dash_text:
    dash_text = dash_text.replace("{% block content %}", breadcrumb_dash, 1)

# Add Language Selector in code editor toolbar
old_file_tag = """                    <div class="file-tag">
                        <span>{% icon "code" size=16 %}</span>
                        <span>workbench_security_audit.py</span>
                    </div>"""
new_file_tag = """                    <div class="file-tag">
                        <span>{% icon "code" size=16 %}</span>
                        <span>workbench_security_audit.py</span>
                        <select class="editor-lang-select" id="editorLangSelect" aria-label="{% trans 'Langage' %}" onchange="if(window.changeEditorMode) changeEditorMode(this.value)">
                            <option value="python">Python</option>
                            <option value="javascript">JavaScript</option>
                            <option value="yaml">YAML</option>
                            <option value="dockerfile">Dockerfile</option>
                        </select>
                    </div>"""
if old_file_tag in dash_text:
    dash_text = dash_text.replace(old_file_tag, new_file_tag, 1)

if "window.changeEditorMode" not in dash_text:
    editor_mode_js = """
window.changeEditorMode = function(lang) {
    if (window.showToast) {
        window.showToast(`{% trans "Langage sélectionné :" %} ${lang.toUpperCase()}`, 'info', 2000);
    }
};
"""
    dash_text = dash_text.replace("function initCodeEditor() {", editor_mode_js + "\nfunction initCodeEditor() {", 1)

dash_path.write_bytes(dash_text.replace("\n", "\r\n").encode("utf-8"))
print("dashboard.html patched")

# 3. Update templates/core/metrics.html
metrics_path = root / "templates/core/metrics.html"
metrics_text = metrics_path.read_bytes().decode("utf-8").replace("\r\n", "\n")
if "{% load i18n %}" not in metrics_text:
    metrics_text = metrics_text.replace("{% extends 'base.html' %}", "{% extends 'base.html' %}\n{% load i18n %}")

breadcrumb_metrics = """{% block content %}
<div style="max-width: 1000px; margin: 0 auto;">
    <nav class="breadcrumbs" aria-label="{% trans 'Fil d Ariane' %}">
        <a href="{% url 'home' %}">{% icon "landmark" size=14 %} {% trans "Accueil" %}</a>
        <span class="breadcrumbs-separator">/</span>
        <span class="breadcrumbs-current" aria-current="page">{% trans "Souveraineté Numérique" %}</span>
    </nav>
"""
if 'class="breadcrumbs"' not in metrics_text:
    metrics_text = metrics_text.replace(
        '{% block content %}\n<div style="max-width: 1000px; margin: 0 auto;">', breadcrumb_metrics, 1
    )

# Add keyboard accessibility to node cards & SVG points
metrics_text = metrics_text.replace(
    '<g class="map-node-point" onclick="selectNode(\'',
    '<g class="map-node-point" tabindex="0" role="button" onkeydown="if(event.key===\'Enter\'||event.key===\' \') selectNode(\'',
)
metrics_text = metrics_text.replace(
    'class="node-card" onclick="selectNode(\'',
    'class="node-card" tabindex="0" role="button" onkeydown="if(event.key===\'Enter\'||event.key===\' \') selectNode(\'',
)
metrics_text = metrics_text.replace(
    'class="node-card selected" onclick="selectNode(\'',
    'class="node-card selected" tabindex="0" role="button" onkeydown="if(event.key===\'Enter\'||event.key===\' \') selectNode(\'',
)

metrics_path.write_bytes(metrics_text.replace("\n", "\r\n").encode("utf-8"))
print("metrics.html patched")

# 4. Update templates/zkp_auth/login.html
login_path = root / "templates/zkp_auth/login.html"
login_text = login_path.read_bytes().decode("utf-8").replace("\r\n", "\n")
if "{% load i18n %}" not in login_text:
    login_text = login_text.replace("{% extends 'base.html' %}", "{% extends 'base.html' %}\n{% load i18n %}")

breadcrumb_login = """{% block content %}
<nav class="breadcrumbs" aria-label="{% trans 'Fil d Ariane' %}">
    <a href="{% url 'home' %}">{% icon "landmark" size=14 %} {% trans "Accueil" %}</a>
    <span class="breadcrumbs-separator">/</span>
    <span class="breadcrumbs-current" aria-current="page">{% trans "Authentification Zero-Trust" %}</span>
</nav>
<div class="zkp-wizard-card">
"""
if 'class="breadcrumbs"' not in login_text:
    login_text = login_text.replace('{% block content %}\n<div class="zkp-wizard-card">', breadcrumb_login, 1)

# Add Copy Mnemonic button next to regenerate
old_regen = """            <button class="btn btn-secondary" style="padding: 0.3rem 0.7rem; font-size: 0.8rem;" onclick="generateNewMnemonic()">
                {% icon "refresh-cw" size=18 %} Regénérer (12 Mots)
            </button>"""
new_regen = """            <div style="display: flex; gap: 0.5rem; align-items: center;">
                <button type="button" class="copy-btn" id="copyMnemonicBtn" onclick="copyMnemonicPhrase()">
                    {% icon "copy" size=14 %} <span id="copyMnemonicLabel">{% trans "Copier la phrase" %}</span>
                </button>
                <button class="btn btn-secondary" style="padding: 0.3rem 0.7rem; font-size: 0.8rem;" onclick="generateNewMnemonic()">
                    {% icon "refresh-cw" size=18 %} Regénérer (12 Mots)
                </button>
            </div>"""
if old_regen in login_text:
    login_text = login_text.replace(old_regen, new_regen, 1)

# Add copyMnemonicPhrase JS function
copy_fn = """
function copyMnemonicPhrase() {
    const text = (typeof currentMnemonic !== 'undefined' && currentMnemonic.length) ? currentMnemonic.join(' ') : document.getElementById('zkpSecret').value;
    if (navigator.clipboard && text) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.getElementById('copyMnemonicBtn');
            const label = document.getElementById('copyMnemonicLabel');
            if (btn) btn.classList.add('copied');
            if (label) label.textContent = 'Copié !';
            if (window.showToast) window.showToast('Phrase de 12 mots copiée !', 'success', 2000);
            setTimeout(() => {
                if (btn) btn.classList.remove('copied');
                if (label) label.textContent = 'Copier la phrase';
            }, 2000);
        });
    }
}
"""
if "function copyMnemonicPhrase" not in login_text:
    login_text = login_text.replace(
        "function generateNewMnemonic() {", copy_fn + "\nfunction generateNewMnemonic() {", 1
    )

login_path.write_bytes(login_text.replace("\n", "\r\n").encode("utf-8"))
print("login.html patched")
