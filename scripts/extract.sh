#!/usr/bin/env bash
# Extrae los textos originales del juego a CSV: inglés en build/vanilla/ y japonés en build/jp/.
# También desempaqueta app_1 (las fuentes del menú) en build/unpacked/, para que build.sh las arregle.
# Uso: scripts/extract.sh   (ruta del juego en THL_GAME_DIR)
# Si la traducción está instalada, el inglés se toma de los originales respaldados (backup/ de install.sh o THL-ESP/backup/ de un paquete).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GAME_DIR="${THL_GAME_DIR:-/mnt/c/Steam/steamapps/common/The Hundred Line -Last Defense Academy-}"
G="$GAME_DIR/gamedata"
CLI_DIR="$ROOT/tools/MVGLTools-v2.2.0-Linux"
CLI="$CLI_DIR/MVGLToolsCLI"
WORK="$ROOT/build/unpacked"

[[ -d "$G" ]] || { echo "No encuentro el juego en: $GAME_DIR (define THL_GAME_DIR)" >&2; exit 1; }
[[ -x "$CLI" ]] || "$ROOT/scripts/get-tools.sh"

extract() {  # <archivo .mvgl> <destino>
  local a
  a="$(basename "$1" .dx11.mvgl)"
  echo "== $a -> ${2#"$ROOT"/}"
  rm -rf "${WORK:?}/$a" "${2:?}/$a"
  # MVGLToolsCLI necesita ejecutarse desde su carpeta (busca structures/ relativo al cwd)
  (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=unpack-mvgl -i "$1" -o "$WORK/$a" >/dev/null)
  # unpack-mbe-dir no es recursivo: se corre por subcarpeta
  for d in "$WORK/$a"/*/; do
    (cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=unpack-mbe-dir \
        -i "$d" -o "$2/$a/$(basename "$d")" >/dev/null)
  done
}

original() {  # <archivo> -> ruta del original (si la traducción está instalada, el respaldo que guardó el instalador)
  local src="$G/$1.dx11.mvgl" h dir
  h="$(sha256sum "$src" | cut -d' ' -f1)"
  for dir in "$ROOT/backup" "$GAME_DIR/THL-ESP/backup"; do  # install.sh o el paquete de una release
    if [[ -f "$dir/installed.sha256" ]] && grep -qx "$h" "$dir/installed.sha256"; then
      src="$dir/$1.dx11.mvgl"
      break
    fi
  done
  echo "$src"
}

for a in app_text01 app_steam_text01 patch_text01 patch_steam_text01; do
  extract "$(original "$a")" "$ROOT/build/vanilla"
done
for a in app_text00 app_steam_text00 patch_text00 patch_steam_text00; do
  extract "$G/$a.dx11.mvgl" "$ROOT/build/jp"
done
echo "== app_1 -> build/unpacked (fuentes)"
rm -rf "${WORK:?}/app_1"
(cd "$CLI_DIR" && ./MVGLToolsCLI --game=thl --mode=unpack-mvgl -i "$(original app_1)" -o "$WORK/app_1" >/dev/null)

echo "CSV: inglés $(find "$ROOT/build/vanilla" -name '*.csv' | wc -l), japonés $(find "$ROOT/build/jp" -name '*.csv' | wc -l)"
