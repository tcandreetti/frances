#!/usr/bin/env python3
"""Gera os áudios das aulas com edge-tts (voz francesa nativa).

Uso: python3 scripts/gerar_audios.py [--force]

Lê scripts/audios.tsv (aula, arquivo, texto) e grava
aulas/assets/<aula>/audio/<arquivo>.mp3. Também gera um "todos.mp3"
por aula com todas as frases em sequência.
Requer: pip install --user --break-system-packages edge-tts
"""
import subprocess, sys, pathlib, collections

VOZ = "fr-FR-DeniseNeural"
RATE = "-20%"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
force = "--force" in sys.argv

def tts(texto, destino):
    if destino.exists() and destino.stat().st_size > 0 and not force:
        return
    destino.parent.mkdir(parents=True, exist_ok=True)
    for tentativa in range(3):
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", VOZ,
                            f"--rate={RATE}", "--text", texto,
                            "--write-media", str(destino)], capture_output=True, text=True)
        if r.returncode == 0 and destino.stat().st_size > 0:
            print("ok ", destino.relative_to(RAIZ))
            return
    raise SystemExit(f"falhou: {destino}: {r.stderr}")

por_aula = collections.OrderedDict()
for linha in (RAIZ / "scripts/audios.tsv").read_text(encoding="utf-8").splitlines():
    if not linha.strip() or linha.startswith("#"):
        continue
    aula, arq, texto = linha.split("\t")
    por_aula.setdefault(aula, []).append((arq, texto))
    tts(texto, RAIZ / "aulas/assets" / aula / "audio" / f"{arq}.mp3")

# aulas com o link "todos os áudios da aula"
for aula, itens in por_aula.items():
    md = (RAIZ / "aulas" / f"{aula}.md").read_text(encoding="utf-8")
    if f"assets/{aula}/audio/todos.mp3" in md:
        # diálogos, ditados e quizzes de ouvido ficam fora do "todos"
        textos = [t for a, t in itens
                  if not a.startswith(("dialogo", "ditado", "ouvido", "quiz"))]
        texto = " ... ".join(t if t.rstrip()[-1:] in ".!?" else t + "." for t in textos)
        tts(texto, RAIZ / "aulas/assets" / aula / "audio" / "todos.mp3")
