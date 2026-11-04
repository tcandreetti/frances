#!/usr/bin/env python3
"""Gera o deck Anki do curso: docs/anki/frances-thais.apkg

Uso: python3 scripts/gerar_anki.py
Requer: pip install --user --break-system-packages genanki edge-tts

Lê scripts/anki_vocab.tsv (aula, francês, português, áudio).
- Coluna "áudio" vazia: usa o mp3 de scripts/audios.tsv com o mesmo texto
  (da mesma aula, se houver); se não existir, gera com edge-tts
  (fr-FR-DeniseNeural, -20%) e guarda em scripts/anki_audio/.
- Cada linha vira 1 nota com 2 cartões: FR → PT e PT → FR.
- IDs de modelo e de deck são fixos, e o GUID de cada nota vem do texto
  em francês. Assim, importar uma versão nova ATUALIZA as notas que já
  existem (sem duplicar e sem perder o progresso) e só acrescenta as novas.
  ⚠️ Corrigir o texto em francês de uma linha cria uma nota nova.
- Para uma aula nova: acrescente linhas no TSV e rode de novo.
"""
import hashlib, pathlib, re, subprocess, sys, unicodedata
import genanki

RAIZ = pathlib.Path(__file__).resolve().parent.parent
VOCAB = RAIZ / "scripts" / "anki_vocab.tsv"
AUDIOS_TSV = RAIZ / "scripts" / "audios.tsv"
CACHE = RAIZ / "scripts" / "anki_audio"
SAIDA = RAIZ / "docs" / "anki" / "frances-thais.apkg"
VOZ, RATE = "fr-FR-DeniseNeural", "-20%"

NOME_DECK = "Francês da Thaís"
MODEL_ID = 1730461001          # fixo: nunca mude
DECK_ID_BASE = 1730462000      # deck principal; subdeck da aula N = base + N

CSS = """
.card { font-family: system-ui, sans-serif; font-size: 26px; text-align: center;
        color: #222; background: #fffdf7; padding: 12px; }
.fr { font-size: 32px; font-weight: 600; color: #1c3d8f; }
.pt { font-size: 26px; color: #333; }
.aula { font-size: 13px; color: #999; margin-top: 18px; }
"""
MODELO = genanki.Model(
    MODEL_ID, "Francês da Thaís (FR ↔ PT)",
    fields=[{"name": "Frances"}, {"name": "Portugues"}, {"name": "Audio"}, {"name": "Aula"}],
    templates=[
        {"name": "FR → PT",
         "qfmt": '<div class="fr">{{Frances}}</div>{{Audio}}',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="pt">{{Portugues}}</div>'
                 '<div class="aula">{{Aula}}</div>'},
        {"name": "PT → FR",
         "qfmt": '<div class="pt">{{Portugues}}</div>',
         "afmt": '{{FrontSide}}<hr id="answer"><div class="fr">{{Frances}}</div>{{Audio}}'
                 '<div class="aula">{{Aula}}</div>'},
    ],
    css=CSS, sort_field_index=0)


def norm(txt):
    t = unicodedata.normalize("NFC", txt).replace("\u00a0", " ").strip().lower()
    return re.sub(r"[\s.!?,…]+$", "", t)


def titulo_aula(aula):
    md = RAIZ / "aulas" / f"{aula}.md"
    num = aula.split("-")[1]
    if md.exists():
        m = re.search(r"^# (.+)$", md.read_text(encoding="utf-8"), re.M)
        if m:
            t = re.sub(r"^🇫🇷\s*", "", m.group(1)).strip()
            t = re.sub(r"^Aula \d+\s*·\s*", "", t)
            return f"Aula {num} · {t}"
    return f"Aula {num}"


def gerar_tts(texto, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(3):
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", VOZ, f"--rate={RATE}",
                            "--text", texto, "--write-media", str(destino)],
                           capture_output=True, text=True)
        if r.returncode == 0 and destino.exists() and destino.stat().st_size > 0:
            print("tts", destino.relative_to(RAIZ))
            return
    raise SystemExit(f"falhou o áudio de: {texto}\n{r.stderr}")


# mp3 já existentes das aulas
existentes = {}
for linha in AUDIOS_TSV.read_text(encoding="utf-8").splitlines():
    if not linha.strip() or linha.startswith("#"):
        continue
    aula, arq, texto = linha.split("\t")
    caminho = RAIZ / "aulas" / "assets" / aula / "audio" / f"{arq}.mp3"
    if caminho.exists():
        existentes.setdefault(norm(texto), {})[aula] = caminho

decks, midias, vistos = {}, {}, set()
pai = genanki.Deck(DECK_ID_BASE, NOME_DECK)
contagem = {}
for n, linha in enumerate(VOCAB.read_text(encoding="utf-8").splitlines(), 1):
    if not linha.strip() or linha.startswith("#"):
        continue
    partes = linha.split("\t") + [""]
    aula, fr, pt, audio = (p.strip() for p in partes[:4])
    chave = norm(fr)
    if chave in vistos:
        print(f"aviso: linha {n} repetida ({fr}); ficou só a primeira")
        continue
    vistos.add(chave)

    # áudio: explícito > mesmo texto em audios.tsv > edge-tts
    if audio:
        origem = RAIZ / audio
    elif chave in existentes:
        opcoes = existentes[chave]
        origem = opcoes.get(aula) or next(iter(opcoes.values()))
    else:
        origem = CACHE / f"{hashlib.sha1(chave.encode()).hexdigest()[:12]}.mp3"
        if not origem.exists():
            gerar_tts(fr, origem)
    if not origem.exists():
        raise SystemExit(f"áudio não encontrado: {origem}")
    # nome único e estável dentro do pacote
    rel = origem.relative_to(RAIZ).as_posix()
    nome_midia = "frth_" + re.sub(r"[^a-zA-Z0-9]+", "_", rel.replace(".mp3", "")).strip("_") + ".mp3"
    midias[nome_midia] = origem

    num = int(aula.split("-")[1])
    if aula not in decks:
        decks[aula] = genanki.Deck(DECK_ID_BASE + num, f"{NOME_DECK}::{titulo_aula(aula)}")
    nota = genanki.Note(model=MODELO,
                        fields=[fr, pt, f"[sound:{nome_midia}]", titulo_aula(aula)],
                        guid=genanki.guid_for("frances-thais", chave),
                        tags=[aula])
    decks[aula].add_note(nota)
    contagem[aula] = contagem.get(aula, 0) + 1

# copia as mídias com o nome único para uma pasta temporária
tmp = RAIZ / "scripts" / ".anki_tmp"
tmp.mkdir(exist_ok=True)
for f in tmp.glob("*"):
    f.unlink()
arquivos = []
for nome, origem in midias.items():
    alvo = tmp / nome
    alvo.write_bytes(origem.read_bytes())
    arquivos.append(str(alvo))

SAIDA.parent.mkdir(parents=True, exist_ok=True)
pacote = genanki.Package([pai] + [decks[a] for a in sorted(decks)])
pacote.media_files = arquivos
pacote.write_to_file(str(SAIDA))
for f in tmp.glob("*"):
    f.unlink()
tmp.rmdir()

total = sum(contagem.values())
for a in sorted(contagem):
    print(f"{titulo_aula(a)}: {contagem[a]} notas = {2 * contagem[a]} cartões")
print(f"TOTAL: {total} notas = {2 * total} cartões · {len(midias)} áudios → {SAIDA.relative_to(RAIZ)}")
