from pathlib import Path

# Fix home.html
home_path = Path("templates/core/home.html")
home_content = home_path.read_text(encoding="utf-8")
home_content = home_content.replace(
    "l'intelligence artificielle locale Gemma 5B",
    "l'intelligence artificielle locale Gemma 2 2B",
)
home_content = home_content.replace(
    "{% trans \"IA Locale Gemma 5B Fine-tunée\" %}",
    "{% trans \"IA Locale Gemma 2 2B Souveraine\" %}",
)
home_content = home_content.replace(
    '<span class="stat-number">5 {% trans "Milliards" %}</span>',
    '<span class="stat-number">2 {% trans "Milliards" %}</span>',
)
home_path.write_text(home_content, encoding="utf-8")

# Fix dashboard.html
dash_path = Path("templates/core/dashboard.html")
dash_content = dash_path.read_text(encoding="utf-8")
dash_content = dash_content.replace(
    "{% trans \"Audits IA Gemma 5B\" %}",
    "{% trans \"Audits IA Gemma 2 2B\" %}",
)
dash_path.write_text(dash_content, encoding="utf-8")

# Fix README.md
readme_path = Path("README.md")
readme_content = readme_path.read_text(encoding="utf-8")
readme_content = readme_content.replace(
    "| **Assurance Qualité** | Pytest, Coverage (> 95%), Ruff, Bandit |",
    "| **Assurance Qualité** | Pytest, Coverage (95.6% démontrée, 201 tests), Ruff, Bandit |",
)
readme_path.write_text(readme_content, encoding="utf-8")

print("SUCCESS: Fixed claims in home.html, dashboard.html, and README.md")
