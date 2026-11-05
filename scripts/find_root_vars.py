import re

import requests

r = requests.get("http://localhost:3002/assets/css/index.css?v=1.22.6")
css = r.text

root_block = re.search(r":root\s*\{([^}]+)\}", css)
if root_block:
    print("Found :root block in index.css! First 500 chars:")
    print(root_block.group(1)[:500])
else:
    print("No direct :root block in index.css, searching for theme variables...")
    # Find any block with --color-body
    var_blocks = re.findall(r"([^{]+)\{\s*([^}]*--color-body[^}]*)\}", css)
    for sel, b in var_blocks[:5]:
        print(f"Selector {sel.strip()}: {b[:200]}")
