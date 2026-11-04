#!/usr/bin/env python3
"""Gera o site estático em docs/ a partir dos arquivos .md.

Uso: python3 scripts/build_site.py
Requer: pip install markdown

O resultado (docs/) vai para o repositório já pronto, então o GitHub Pages
publica direto da pasta /docs da branch main, sem nenhum passo de build.
"""
import html, pathlib, re, shutil
import markdown

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
SITE = RAIZ / "scripts" / "site"

PAGINAS = [  # (origem, destino, rótulo no menu)
    ("README.md", "index.html", "🏠 Início"),
    ("roadmap.md", "roadmap.html", "🗺️ Roadmap"),
    ("plano-de-estudo.md", "plano-de-estudo.html", "📋 Plano de estudo"),
    ("progresso.md", "progresso.html", "📒 Progresso"),
    ("gamificacao.md", "gamificacao.html", "🎮 Gamificação"),
]
AULAS = sorted((RAIZ / "aulas").glob("aula-*.md"))


def gh_slug(valor, sep="-"):
    """Âncoras iguais às do GitHub (ex.: '📅 Rotina semanal' -> '-rotina-semanal')."""
    v = valor.strip().lower()
    v = re.sub(r"[^\w\- ]", "", v)
    return v.replace(" ", "-")


def titulo(md):
    m = re.search(r"^# (.+)$", md, re.M)
    return m.group(1).strip() if m else "Francês da Thaís"


def link_md_para_html(m):
    attr, url = m.group(1), m.group(2)
    if re.match(r"^[a-z]+:", url) or url.startswith("#"):
        return m.group(0)
    if url == "docs/index.html":
        url = "index.html"
    url = re.sub(r"README\.md(?=$|#)", "index.html", url)
    url = re.sub(r"\.md(?=$|#)", ".html", url)
    if url.endswith("aulas/"):
        url += "aula-01.html"
    return f'{attr}="{url}"'


def indentar_listas(md_texto):
    """O GitHub aceita sublistas com 2 espaços; o Python-Markdown pede 4."""
    saida, em_codigo = [], False
    for linha in md_texto.split("\n"):
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
        m = re.match(r"^((?:  )+)(\d+\.|[-*]) ", linha)
        if m and not em_codigo:
            linha = m.group(1) * 2 + linha[len(m.group(1)):]
        saida.append(linha)
    return "\n".join(saida)


def render(md_texto, prefixo):
    md_texto = indentar_listas(md_texto)
    md_texto = md_texto.replace("<details>", '<details markdown="1">')
    conv = markdown.Markdown(
        extensions=["tables", "fenced_code", "md_in_html", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": gh_slug}},
    )
    corpo = conv.convert(md_texto)
    # mermaid
    corpo = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: f'<pre class="mermaid">{m.group(1)}</pre>', corpo, flags=re.S)
    # listas de tarefas
    corpo = re.sub(r"<li>\[ \]\s*", '<li class="task"><input type="checkbox"> ', corpo)
    corpo = re.sub(r"<li>\[x\]\s*", '<li class="task"><input type="checkbox" checked> ', corpo)
    corpo = re.sub(r"<li>\s*<p>\[ \]\s*", '<li class="task"><p><input type="checkbox"> ', corpo)
    # links .md -> .html
    corpo = re.sub(r'(href)="([^"]+)"', link_md_para_html, corpo)
    # tabelas roláveis no celular
    corpo = corpo.replace("<table>", '<div class="tabela"><table>').replace("</table>", "</table></div>")
    return corpo


def menu(prefixo, atual):
    itens = []
    for _, dest, rot in PAGINAS:
        cls = ' class="ativo"' if dest == atual else ""
        itens.append(f'<li><a{cls} href="{prefixo}{dest}">{rot}</a></li>')
    itens.append('<li class="sec">📚 Aulas</li>')
    for a in AULAS:
        dest = f"aulas/{a.stem}.html"
        t = titulo(a.read_text(encoding="utf-8"))
        t = re.sub(r"^🇫🇷\s*", "", t)
        cls = ' class="ativo"' if dest == atual else ""
        itens.append(f'<li><a{cls} href="{prefixo}{dest}">{html.escape(t)}</a></li>')
    return "\n".join(itens)


def pagina(md_path, dest):
    md = md_path.read_text(encoding="utf-8")
    prefixo = "../" * dest.count("/")
    corpo = render(md, prefixo)
    tpl = (SITE / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{titulo}}", html.escape(re.sub(r"[*`]", "", titulo(md))))
              .replace("{{prefixo}}", prefixo)
              .replace("{{menu}}", menu(prefixo, dest))
              .replace("{{conteudo}}", corpo)
              .replace("{{pagina}}", dest))
    alvo = DOCS / dest
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text(out, encoding="utf-8")
    print("ok ", alvo.relative_to(RAIZ))


def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    (DOCS / ".nojekyll").write_text("")
    shutil.copy(SITE / "style.css", DOCS / "style.css")
    shutil.copy(SITE / "app.js", DOCS / "app.js")
    shutil.copytree(RAIZ / "aulas" / "assets", DOCS / "aulas" / "assets")
    for src, dest, _ in PAGINAS:
        pagina(RAIZ / src, dest)
    for a in AULAS:
        pagina(a, f"aulas/{a.stem}.html")


if __name__ == "__main__":
    main()
