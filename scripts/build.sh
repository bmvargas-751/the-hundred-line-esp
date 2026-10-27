#!/usr/bin/env bash
# Arma los .mvgl traducidos: inglés original (build/vanilla/) + nuestra traducción (translation/).
# Lo que falta traducir queda en inglés.
# Uso: scripts/build.sh   -> genera dist/*.dx11.mvgl
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI_DIR="$ROOT/tools/MVGLTools-v2.2.0-Linux"
CLI="$CLI_DIR/MVGLToolsCLI"
SRC="$ROOT/build/es"
WORK="$ROOT/build/repacked"
ARCHIVES=(app_text01 patch_text01)

[[ -x "$CLI" ]] || "$ROOT/scripts/get-tools.sh"
[[ -d "$ROOT/build/vanilla" ]] || "$ROOT/scripts/extract.sh"

python3 -I "$ROOT/scripts/generar.py" "$SRC"
rm -rf "$WORK"
mkdir -p "$ROOT/dist"
for a in "${ARCHIVES[@]}"; do
  echo "== $a"
  for d in "$SRC/$a"/*/; do
    sub="$(basename "$d")"
    (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=pack-mbe-dir \
        -i "$d" -o "$WORK/$a/$sub" >/dev/null)
  done
  (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=pack-mvgl \
      -i "$WORK/$a" -o "$ROOT/dist/$a.dx11.mvgl" >/dev/null)
done

ls -la "$ROOT/dist"
