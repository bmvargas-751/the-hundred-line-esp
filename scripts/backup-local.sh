#!/usr/bin/env bash
# Respalda lo que vive solo en local (no está en el repo) en un .tar.gz fechado.
# Uso: scripts/backup-local.sh [carpeta-destino]   (por defecto, la carpeta que contiene al repo)
# table/, build/, dist/ y tools/ no se respaldan: se regeneran (thl.py table, extract.sh, build.sh, get-tools.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${1:-$(dirname "$ROOT")}"
OUT="$DEST/thl-local-$(date +%F).tar.gz"
FILES=()
for f in .claude PLAN.md TESTS.md PENDING-REVIEW.md backup build/work; do
  [[ -e "$ROOT/$f" ]] && FILES+=("$f")
done
tar -czf "$OUT" -C "$ROOT" "${FILES[@]}"
echo "respaldo: $OUT"
