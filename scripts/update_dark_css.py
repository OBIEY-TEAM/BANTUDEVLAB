import os

# 1. Update theme-github-dark.css
css_vars = """
  /* Gitea 1.22+ Standard Variables for Dark Mode */
  --color-body: #020617;
  --color-box-header: #050b18;
  --color-box-body: #070e1e;
  --color-box-body-highlight: #0b1528;
  --color-text: #f8fafc;
  --color-text-dark: #f8fafc;
  --color-text-light: #94a3b8;
  --color-text-light-1: #94a3b8;
  --color-text-light-2: #64748b;
  --color-text-light-3: #475569;
  --color-footer: #050b18;
  --color-navbar: #050b18;
  --color-nav-bg: #050b18;
  --color-nav-hover-bg: #0b1528;
  --color-menu: #070e1e;
  --color-card: #070e1e;
  --color-secondary-bg: #070e1e;
  --color-secondary-nav-bg: #050b18;
  --color-input-background: #0b1528;
  --color-input-text: #f8fafc;
  --color-input-border: #1e293b;
  --color-input-border-hover: #00e5ff;
  --color-markup-code-block: #0b1528;
  --color-markup-code-inline: #1e293b;
  --color-console-bg: #020617;
  --color-console-fg: #f8fafc;
  --color-border: #1e293b;
  --color-border-subtle: #0f172a;
  --color-active: rgba(0, 229, 255, 0.15);
  --color-hover: rgba(255, 255, 255, 0.05);
"""

for path in [
    "custom/public/assets/css/theme-github-dark.css",
    "gitea_home/custom/public/assets/css/theme-github-dark.css"
]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "--color-input-background:" not in content:
        content = content.replace(":root {", ":root {" + css_vars)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)

print("Updated theme-github-dark.css")
