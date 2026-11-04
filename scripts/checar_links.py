#!/usr/bin/env python3
"""Confere todos os links e arquivos locais do site servido por HTTP.

Uso: python3 -m http.server -d docs 8000 &  e depois  python3 scripts/checar_links.py [http://localhost:8000/]
"""
import sys, re, urllib.request, urllib.parse
from html.parser import HTMLParser

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/"

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src"):
            if a.get(k): self.links.append(a[k])

vistos, fila, erros, ids, ancoras = set(), [BASE], [], {}, []
while fila:
    url = fila.pop()
    if url in vistos: continue
    vistos.add(url)
    try:
        r = urllib.request.urlopen(url)
        corpo = r.read()
    except Exception as e:
        erros.append(f"{url}: {e}"); continue
    if not url.endswith(".html") and not url.endswith("/"): continue
    p = P(); p.feed(corpo.decode("utf-8")); ids[url] = p.ids
    for l in p.links:
        if re.match(r"^(https?:|mailto:)", l) and not l.startswith(BASE): continue
        alvo = urllib.parse.urljoin(url, l)
        alvo, _, frag = alvo.partition("#")
        if frag: ancoras.append((url, alvo, frag))
        if alvo.startswith(BASE): fila.append(alvo)
for origem, alvo, frag in ancoras:
    chave = alvo if alvo in ids else (alvo + "index.html" if alvo + "index.html" in ids else alvo)
    if chave in ids and frag not in ids[chave]:
        erros.append(f"{origem}: âncora #{frag} não existe em {alvo}")
print(f"{len(vistos)} URLs conferidas, {len(erros)} erro(s)")
for e in erros: print("  ✗", e)
sys.exit(1 if erros else 0)
