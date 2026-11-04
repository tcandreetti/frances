#!/usr/bin/env bash
# Copia o material de preposições de /workspace/frances para aulas/assets/aula-06/.
# Rode de novo se o material de origem for atualizado.
set -euo pipefail
ORIG="${1:-/workspace/frances}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/aulas/assets/aula-06"
mkdir -p "$DEST/img" "$DEST/fonte"
cp -v "$ORIG/infografico_preposicoes_frances.png" "$DEST/img/"
cp -v "$ORIG/info.html" "$DEST/fonte/info.html"
for f in infografico_preposicoes_A4.png infografico_preposicoes_A4_p1.png infografico_preposicoes_A4_p2.png; do
  [ -f "$ORIG/$f" ] && cp -v "$ORIG/$f" "$DEST/img/" || echo "TODO: falta $f"
done
for f in infografico_preposicoes_A4.pdf exercicios_preposicoes_A4.pdf gabarito_preposicoes_A4.pdf frances_preposicoes_completo_A4.pdf; do
  [ -f "$ORIG/$f" ] && cp -v "$ORIG/$f" "$DEST/" || echo "TODO: falta $f"
done
for f in infografico_preposicoes_A4.html exercicios_preposicoes_A4.html gabarito_preposicoes_A4.html; do
  [ -f "$ORIG/$f" ] && cp -v "$ORIG/$f" "$DEST/fonte/" || echo "TODO: falta $f"
done
