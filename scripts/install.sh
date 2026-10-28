#!/usr/bin/env bash
# Instala dist/*.mvgl en el juego, guardando antes los originales en backup/.
# Uso: scripts/install.sh [jp|en]   (ruta del juego en THL_GAME_DIR). Sin versión, pregunta cuál instalar.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "¿Con qué doblaje vas a jugar?"
  echo "  1) Doblaje japonés (subtítulos basados en el japonés)"
  echo "  2) Doblaje inglés (subtítulos basados en el inglés)"
  read -rp "Elige 1 o 2: " ans
  case "$ans" in 1) VERSION=jp ;; 2) VERSION=en ;; *) echo "Opción no válida" >&2; exit 1 ;; esac
fi
[[ "$VERSION" == "jp" || "$VERSION" == "en" ]] || { echo "Uso: scripts/install.sh [jp|en]" >&2; exit 1; }
DIST="$ROOT/dist/$VERSION"
GAME_DIR="${THL_GAME_DIR:-/mnt/c/Steam/steamapps/common/The Hundred Line -Last Defense Academy-}"
G="$GAME_DIR/gamedata"
BACKUP="$ROOT/backup"
INSTALLED="$BACKUP/installed.sha256"  # hashes de los archivos del parche que instalamos
ARCHIVES=(app_text01 app_steam_text01 patch_text01 patch_steam_text01 app_1)  # app_1: fuentes del menú

[[ -d "$G" ]] || { echo "No encuentro el juego en: $GAME_DIR (define THL_GAME_DIR)" >&2; exit 1; }
for a in "${ARCHIVES[@]}"; do
  [[ -f "$DIST/$a.dx11.mvgl" ]] || "$ROOT/scripts/build.sh" "$VERSION"
done

mkdir -p "$BACKUP"
touch "$INSTALLED"
for a in "${ARCHIVES[@]}"; do
  cur="$(sha256sum "$G/$a.dx11.mvgl" | cut -d' ' -f1)"
  # Si lo que hay en el juego no es un parche nuestro, es el original (o una versión nueva): se respalda
  if ! grep -qx "$cur" "$INSTALLED"; then
    cp "$G/$a.dx11.mvgl" "$BACKUP/"
    echo "backup: $a"
  fi
  cp "$DIST/$a.dx11.mvgl" "$G/"
  sha256sum "$DIST/$a.dx11.mvgl" | cut -d' ' -f1 >> "$INSTALLED"
  echo "instalado: $a"
done
sort -u -o "$INSTALLED" "$INSTALLED"
