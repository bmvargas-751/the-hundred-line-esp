"""Arma los paquetes de una release: uno para Windows y otro para Linux (Steam Deck incluida).

  python3 -I scripts/make-release.py v0.1.1     -> dist/release/THL-ESP-v0.1.1-windows.zip y -linux.tar.gz

Cada paquete se descomprime dentro de la carpeta del juego y trae todo lo necesario: el instalador,
la traducción, MVGLTools (con su licencia) y los lanzadores de instalar y desinstalar.
Windows trae además Python embebido, para no pedirle nada instalado a quien juega.
No incluye el juego ni sus archivos: el instalador arma el parche con la copia de cada persona.
Las descargas se guardan en build/work/dl y se comprueban contra los hashes fijados abajo.
"""
import hashlib
import io
import re
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DL = ROOT / "build" / "work" / "dl"
OUT = ROOT / "dist" / "release"
TOP = "THL-ESP"

DOWNLOADS = {
    "MVGLTools-v2.2.0-win64.zip": (
        "https://github.com/SydMontague/MVGLTools/releases/download/v2.2.0/MVGLTools-v2.2.0-win64.zip",
        "9e234ede2bbbb38a08bc66ba052ef542a1dd43f45912e256e63479401a8720b9"),
    "MVGLTools-v2.2.0-Linux.zip": (
        "https://github.com/SydMontague/MVGLTools/releases/download/v2.2.0/MVGLTools-v2.2.0-Linux.zip",
        "7cea2736e6c42046729622770a9a568f66dd214b3d9f261be08c402a667aef70"),
    "python-3.12.8-embed-amd64.zip": (
        "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip",
        "8d3f33be9eb810f23c102f08475af2854e50484b8e4e06275e937be61ce3d2fb"),
}
SCRIPTS = ["installer.py", "generar.py", "thldatos.py"]
DOCS = ["LICENSE.md"]


def fetch(name):
    url, want = DOWNLOADS[name]
    path = DL / name
    DL.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        print(f"descargando {name}")
        urllib.request.urlretrieve(url, path)
    got = hashlib.sha256(path.read_bytes()).hexdigest()
    if got != want:
        path.unlink()
        raise SystemExit(f"{name}: el hash no coincide con el fijado ({got}); descarga borrada.")
    return path


def readme(version, windows):
    launch = ("INSTALAR.bat" if windows else "instalar.sh")
    remove = ("DESINSTALAR.bat" if windows else "desinstalar.sh")
    extra = "" if windows else (
        "\nEn Steam Deck: en modo escritorio, abre esta carpeta, clic derecho en instalar.sh > Ejecutar en terminal\n"
        "(o desde una terminal: ./instalar.sh).\n")
    return f"""THE HUNDRED LINE -LAST DEFENSE ACADEMY- — TRADUCCIÓN AL ESPAÑOL {version}
Traducción no oficial, hecha por fans. No incluye el juego: se arma con TU copia de Steam.

INSTALAR
  1. Esta carpeta ({TOP}) tiene que quedar DENTRO de la carpeta del juego, junto a "gamedata".
     En Steam: clic derecho en el juego > Administrar > Explorar archivos locales.
  2. Ejecuta {launch}.{extra}
  3. Abre el juego, ve a Opciones y pon el idioma en English: el texto aparece en español.

DESINSTALAR
  Ejecuta {remove}. Restaura los archivos originales del juego.
  Si algo quedó mal: en Steam, Propiedades > Archivos instalados > Verificar integridad.

Si el juego se actualiza, Steam pisa el parche: vuelve a ejecutar {launch}.
Errores y comentarios (sin spoilers): https://github.com/bmvargas-751/the-hundred-line-esp/issues
Licencias: ver LICENSE.md y translation/LICENSE. MVGLTools trae la suya en tools/.
"""


BAT = """@echo off
chcp 65001 >nul
cd /d "%~dp0"
"%~dp0python\\python.exe" "%~dp0scripts\\installer.py" {cmd} --pause
"""
SH = """#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
python3 scripts/installer.py {cmd} --pause
"""


def common_files(version, windows):
    """(ruta dentro del paquete, bytes, ejecutable) de lo que comparten los dos paquetes."""
    files = []
    for s in SCRIPTS:
        files.append((f"scripts/{s}", (ROOT / "scripts" / s).read_bytes(), False))
    for p in sorted((ROOT / "translation").rglob("*")):
        if p.is_file():
            files.append((p.relative_to(ROOT).as_posix(), p.read_bytes(), False))
    for d in DOCS:
        files.append((d, (ROOT / d).read_bytes(), False))
    files.append(("LEEME.txt", readme(version, windows).replace("\n", "\r\n" if windows else "\n").encode("utf-8"), False))
    return files


def zip_members(path, prefix_out):
    """Contenido de un zip descargado, con otra raíz."""
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            yield prefix_out + info.filename, z.read(info), bool(info.external_attr >> 16 & 0o111)


def build_windows(version):
    out = OUT / f"THL-ESP-{version}-windows.zip"
    files = common_files(version, True)
    files.append(("INSTALAR.bat", BAT.format(cmd="install").replace("\n", "\r\n").encode(), False))
    files.append(("DESINSTALAR.bat", BAT.format(cmd="uninstall").replace("\n", "\r\n").encode(), False))
    files += [(n, b, x) for n, b, x in zip_members(fetch("python-3.12.8-embed-amd64.zip"), "python/")]
    files += [(n.replace("MVGLTools-v2.2.0-win64/", "tools/MVGLTools-v2.2.0-win64/", 1), b, x)
              for n, b, x in zip_members(fetch("MVGLTools-v2.2.0-win64.zip"), "")]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data, _ in files:
            z.writestr(f"{TOP}/{name}", data)
    return out, len(files)


def build_linux(version):
    out = OUT / f"THL-ESP-{version}-linux.tar.gz"
    files = common_files(version, False)
    files.append(("instalar.sh", SH.format(cmd="install").encode(), True))
    files.append(("desinstalar.sh", SH.format(cmd="uninstall").encode(), True))
    files += [(n.replace("MVGLTools-v2.2.0-Linux/", "tools/MVGLTools-v2.2.0-Linux/", 1), b, x or n.endswith("MVGLToolsCLI"))
              for n, b, x in zip_members(fetch("MVGLTools-v2.2.0-Linux.zip"), "")]
    with tarfile.open(out, "w:gz", compresslevel=9) as t:
        for name, data, exe in files:
            info = tarfile.TarInfo(f"{TOP}/{name}")
            info.size, info.mode, info.mtime = len(data), 0o755 if exe else 0o644, 0
            t.addfile(info, io.BytesIO(data))
    return out, len(files)


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"v\d+\.\d+\.\d+", sys.argv[1]):
        raise SystemExit("Uso: python3 -I scripts/make-release.py vX.Y.Z")
    version = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True)
    for build in (build_windows, build_linux):
        path, n = build(version)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"{path.name}: {n} archivos, {path.stat().st_size / 1e6:.1f} MB\n  sha256 {digest}")


if __name__ == "__main__":
    main()
