#!/usr/bin/env bash
# Arma los .mvgl traducidos: inglés original (build/vanilla/) + nuestra traducción (translation/).
# Lo que falta traducir queda en inglés.
# También arma app_1 con las fuentes del menú arregladas (scripts/thlfuente.py).
# Uso: scripts/build.sh [jp|en]   -> genera dist/<versión>/*.dx11.mvgl (jp: doblaje japonés, por defecto; en: doblaje inglés)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI_DIR="$ROOT/tools/MVGLTools-v2.2.0-Linux"
CLI="$CLI_DIR/MVGLToolsCLI"
VERSION="${1:-jp}"
[[ "$VERSION" == "jp" || "$VERSION" == "en" ]] || { echo "Uso: scripts/build.sh [jp|en]" >&2; exit 1; }
SRC="$ROOT/build/es-$VERSION"
WORK="$ROOT/build/repacked-$VERSION"
DIST="$ROOT/dist/$VERSION"
ARCHIVES=(app_text01 app_steam_text01 patch_text01 patch_steam_text01)

[[ -x "$CLI" ]] || "$ROOT/scripts/get-tools.sh"
[[ -d "$ROOT/build/vanilla" && -d "$ROOT/build/unpacked/app_1" ]] || "$ROOT/scripts/extract.sh"

python3 -I "$ROOT/scripts/generar.py" "$SRC" "$VERSION"
rm -rf "$WORK"
mkdir -p "$DIST"
for a in "${ARCHIVES[@]}"; do
  echo "== $a"
  for d in "$SRC/$a"/*/; do
    sub="$(basename "$d")"
    (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=pack-mbe-dir \
        -i "$d" -o "$WORK/$a/$sub" >/dev/null)
  done
  (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=pack-mvgl \
      -i "$WORK/$a" -o "$DIST/$a.dx11.mvgl" >/dev/null)
done

echo "== app_1 (fuentes)"
cp -r "$ROOT/build/unpacked/app_1" "$WORK/app_1"
for f in commonfont.bin commonfont2.bin; do
  python3 -I "$ROOT/scripts/thlfuente.py" "$WORK/app_1/$f"
done
(cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=pack-mvgl \
    -i "$WORK/app_1" -o "$DIST/app_1.dx11.mvgl" >/dev/null)

ls -la "$DIST"
