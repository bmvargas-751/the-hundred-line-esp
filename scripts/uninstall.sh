#!/usr/bin/env bash
# Quita la traducción: restaura en el juego los originales guardados por install.sh.
# Uso: scripts/uninstall.sh   (ruta del juego en THL_GAME_DIR)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GAME_DIR="${THL_GAME_DIR:-/mnt/c/Steam/steamapps/common/The Hundred Line -Last Defense Academy-}"
G="$GAME_DIR/gamedata"
BACKUP="$ROOT/backup"
INSTALLED="$BACKUP/installed.sha256"
ARCHIVES=(app_text01 patch_text01)

[[ -d "$G" ]] || { echo "No encuentro el juego en: $GAME_DIR (define THL_GAME_DIR)" >&2; exit 1; }

for a in "${ARCHIVES[@]}"; do
  cur="$(sha256sum "$G/$a.dx11.mvgl" | cut -d' ' -f1)"
  if [[ -f "$INSTALLED" ]] && grep -qx "$cur" "$INSTALLED"; then
    cp "$BACKUP/$a.dx11.mvgl" "$G/"
    echo "restaurado: $a"
  else
    # No es nuestro parche (ya desinstalado o el juego se actualizó): no se pisa
    echo "sin cambios: $a no tiene el parche instalado"
  fi
done
echo "Si algo quedó mal, en Steam: Propiedades > Archivos instalados > Verificar integridad."
