import requests
import re

r = requests.get('http://localhost:3002/assets/css/index.css?v=1.22.6')
css = r.text

variables = set(re.findall(r'--color-[a-zA-Z0-9_-]+', css))
print("Total --color-* variables in index.css:", len(variables))
print("Sample color variables:", sorted(list(variables))[:30])

# Check what color rules apply to body, page-content, ui segment, text
for sel in ['body', '.page-content', '.ui.segment', '.ui.form', '.flex-item']:
    matches = re.findall(rf'({re.escape(sel)}\s*\{{[^}}]*\}})', css)
    if matches:
        print(f"Selector {sel}:", matches[0][:200])
