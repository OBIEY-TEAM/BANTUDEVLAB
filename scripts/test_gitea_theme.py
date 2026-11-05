import re

import requests

for cookie in ["", "theme=github-dark", "theme=gitea-dark", "theme=github", "bantu_theme=dark"]:
    headers = {"Cookie": cookie} if cookie else {}
    r = requests.get("http://localhost:3002/explore/repos", headers=headers)
    themes = re.findall(r'theme-[^"\'\s]+\.css', r.text)
    print(f"Cookie: {cookie!r:25} -> Themes found: {themes}")
