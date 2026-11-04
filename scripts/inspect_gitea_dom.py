import requests
from bs4 import BeautifulSoup

for path in ['/', '/user/login', '/user/sign_up', '/explore/repos']:
    r = requests.get('http://localhost:3002' + path)
    soup = BeautifulSoup(r.text, 'html.parser')
    body_classes = soup.body.get('class', [])
    div_classes = set()
    for el in soup.find_all(['div', 'form', 'table', 'section', 'main']):
        for c in el.get('class', []):
            div_classes.add(c)
    print(f"Path: {path} -> Body class: {body_classes}")
    # Check for semantic ui classes
    print("Semantic classes found:", [c for c in sorted(div_classes) if any(k in c for k in ['ui', 'segment', 'page', 'content', 'container', 'header', 'form', 'menu', 'item'])][:20])
