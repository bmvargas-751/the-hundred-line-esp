#!/usr/bin/env bash
# Instala dist/*.mvgl en el juego, guardando antes los originales en backup/.
# Uso: scripts/install.sh   (ruta del juego en THL_GAME_DIR).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist/mvgl"
GAME_DIR="${THL_GAME_DIR:-/mnt/c/Steam/steamapps/common/The Hundred Line -Last Defense Academy-}"
G="$GAME_DIR/gamedata"
BACKUP="$ROOT/backup"
INSTALLED="$BACKUP/installed.sha256"  # hashes de los archivos del parche que instalamos
ARCHIVES=(app_text01 app_steam_text01 patch_text01 patch_steam_text01 app_1)  # app_1: fuentes del menú

[[ -d "$G" ]] || { echo "No encuentro el juego en: $GAME_DIR (define THL_GAME_DIR)" >&2; exit 1; }
for a in "${ARCHIVES[@]}"; do
  [[ -f "$DIST/$a.dx11.mvgl" ]] || "$ROOT/scripts/build.sh"
done

mkdir -p "$BACKUP"
touch "$INSTALLED"
# Huellas de los originales que traducimos (las mismas del instalador de la release)
declare -A ORIG
while read -r name hash; do ORIG[$name]=$hash; done < <(python3 -I - "$ROOT/scripts/installer.py" <<'PY'
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
for name, h in re.findall(r'"(\w+)":\s*"([0-9a-f]{64})"', src[src.index("SUPPORTED"):src.index("ALL =")]):
    print(name, h)
PY
)
# Primero se revisa todo: si algo no es ni el original ni nuestro parche, no se toca nada
for a in "${ARCHIVES[@]}"; do
  cur="$(sha256sum "$G/$a.dx11.mvgl" | cut -d' ' -f1)"
  if ! grep -qx "$cur" "$INSTALLED" && [[ "$cur" != "${ORIG[$a]:-}" ]] && [[ "${THL_FORCE:-0}" != "1" ]]; then
    echo "AVISO: $a no es el original que traducimos ni un parche nuestro (¿actualización del juego o una traducción instalada desde otra carpeta?)." >&2
    echo "       No se instaló nada. En Steam: Propiedades > Archivos instalados > Verificar integridad, y reintenta (o THL_FORCE=1 para forzar)." >&2
    exit 1
  fi
done
for a in "${ARCHIVES[@]}"; do
  cur="$(sha256sum "$G/$a.dx11.mvgl" | cut -d' ' -f1)"
  # Solo se respalda el original de Steam: un respaldo bueno nunca se pisa con otra cosa
  if ! grep -qx "$cur" "$INSTALLED"; then
    if [[ "$cur" == "${ORIG[$a]:-}" ]]; then
      cp "$G/$a.dx11.mvgl" "$BACKUP/"
      echo "backup: $a"
    elif [[ ! -f "$BACKUP/$a.dx11.mvgl" ]]; then
      cp "$G/$a.dx11.mvgl" "$BACKUP/"
      echo "backup (OJO: no es el original conocido): $a"
    fi
  fi
  cp "$DIST/$a.dx11.mvgl" "$G/"
  sha256sum "$DIST/$a.dx11.mvgl" | cut -d' ' -f1 >> "$INSTALLED"
  echo "instalado: $a"
done
sort -u -o "$INSTALLED" "$INSTALLED"
