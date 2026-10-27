#!/usr/bin/env bash
# Descarga MVGLToolsCLI v2.2.0 (Linux) en tools/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VER=v2.2.0
ZIP="$ROOT/tools/MVGLTools-$VER-Linux.zip"

mkdir -p "$ROOT/tools"
curl -fL -o "$ZIP" "https://github.com/SydMontague/MVGLTools/releases/download/$VER/MVGLTools-$VER-Linux.zip"
python3 -I -m zipfile -e "$ZIP" "$ROOT/tools"
chmod +x "$ROOT/tools/MVGLTools-$VER-Linux/MVGLToolsCLI"
rm -f "$ZIP"
