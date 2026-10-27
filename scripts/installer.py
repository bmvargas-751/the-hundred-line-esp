"""Instalador de la traducción al español. Funciona igual en Windows y en Linux (Steam Deck incluida).

  python3 installer.py install     arma la traducción desde tu copia del juego y la instala
  python3 installer.py uninstall   quita la traducción y restaura los archivos originales
  python3 installer.py status      muestra qué hay instalado

Opciones: --game RUTA  carpeta del juego (si no se indica, se busca sola)
          --force      sigue aunque la versión del juego no sea la traducida
          --pause      espera un Enter al terminar (para cuando se abre con doble clic)

Solo usa la biblioteca estándar de Python. Necesita MVGLTools (carpeta tools/); si falta, lo descarga.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar  # noqa: E402
import thldatos as td  # noqa: E402

ROOT = td.ROOT
GAME_NAME = "The Hundred Line -Last Defense Academy-"
BACKUP = ROOT / "backup"
INSTALLED = BACKUP / "installed.sha256"  # hashes de los archivos del parche que instalamos
MVGL_VERSION = "v2.2.0"
# sha256 de los archivos originales de la versión del juego que traducimos (actualización de Steam del 2026-09-17)
SUPPORTED = {
    "app_text01": "34713a3f12515075c253c1dd78b8a14b1c5b74dc1c5e9b5c07ad5746cdaab658",
    "patch_text01": "74c8167c7eb2f8be663babad35c50cf6f30d04369073a50fbf10e6da80182d1c",
}


class Fail(Exception):
    pass


def say(msg=""):
    print(msg, flush=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def archive_file(game, name):
    return game / "gamedata" / f"{name}.dx11.mvgl"


# ---------- dónde está el juego ----------

def steam_roots():
    """Carpetas de Steam conocidas, según el sistema."""
    home = Path.home()
    roots = []
    if sys.platform == "win32":
        try:
            import winreg
            for hive, key in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                              (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")):
                try:
                    with winreg.OpenKey(hive, key) as k:
                        roots.append(Path(winreg.QueryValueEx(k, "SteamPath" if hive == winreg.HKEY_CURRENT_USER else "InstallPath")[0]))
                except OSError:
                    pass
        except ImportError:
            pass
        for env in ("ProgramFiles(x86)", "ProgramFiles"):
            if os.environ.get(env):
                roots.append(Path(os.environ[env]) / "Steam")
    else:
        roots += [home / ".local/share/Steam", home / ".steam/steam", home / ".steam/root",
                  home / ".var/app/com.valvesoftware.Steam/.local/share/Steam"]
        for drive in ("c", "d"):  # WSL
            roots += [Path(f"/mnt/{drive}/Steam"), Path(f"/mnt/{drive}/Program Files (x86)/Steam")]
    return roots


def libraries(root):
    """La propia carpeta de Steam más las bibliotecas extra que lista libraryfolders.vdf."""
    libs = [root]
    for vdf in (root / "steamapps/libraryfolders.vdf", root / "config/libraryfolders.vdf"):
        if vdf.exists():
            text = vdf.read_text(encoding="utf-8", errors="replace")
            libs += [Path(p.replace("\\\\", "\\")) for p in re.findall(r'"path"\s+"([^"]+)"', text)]
    return libs


def is_game(path):
    return archive_file(Path(path), "app_text01").exists()


def find_game(arg):
    here = ROOT
    tried = []
    candidates = []
    if arg:
        candidates.append(Path(arg))
    if os.environ.get("THL_GAME_DIR"):
        candidates.append(Path(os.environ["THL_GAME_DIR"]))
    # descomprimido dentro de la carpeta del juego (o en una subcarpeta suya)
    candidates += [here, here.parent, here.parent.parent]
    for root in steam_roots():
        for lib in libraries(root):
            candidates.append(lib / "steamapps" / "common" / GAME_NAME)
    for c in candidates:
        tried.append(c)
        if is_game(c):
            return c
    raise Fail("No encuentro el juego. Descomprime esta carpeta dentro de la carpeta del juego, "
               "o indica la ruta con:  --game \"RUTA\"\n(En Steam: clic derecho en el juego > Administrar > Explorar archivos locales.)")


# ---------- MVGLTools ----------

def find_tool():
    exe = "MVGLToolsCLI.exe" if sys.platform == "win32" else "MVGLToolsCLI"
    for p in sorted((ROOT / "tools").glob(f"**/{exe}")):
        return p
    kind = "win64" if sys.platform == "win32" else "Linux"
    zip_name = f"MVGLTools-{MVGL_VERSION}-{kind}.zip"
    url = f"https://github.com/SydMontague/MVGLTools/releases/download/{MVGL_VERSION}/{zip_name}"
    say(f"Descargando MVGLTools ({kind})...")
    dest = ROOT / "tools"
    dest.mkdir(exist_ok=True)
    zpath = dest / zip_name
    try:
        urllib.request.urlretrieve(url, zpath)
    except OSError as e:
        raise Fail(f"No pude descargar MVGLTools ({e}). Descárgalo de {url} y descomprímelo en la carpeta tools/.")
    with zipfile.ZipFile(zpath) as z:
        z.extractall(dest)
    zpath.unlink()
    for p in sorted(dest.glob(f"**/{exe}")):
        if sys.platform != "win32":
            p.chmod(0o755)
        return p
    raise Fail("MVGLTools no trae el ejecutable esperado.")


def run_tool(tool, *args):
    # MVGLToolsCLI busca structures/ relativo a su carpeta
    r = subprocess.run([str(tool), "--game=thl", *map(str, args)], cwd=tool.parent,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        raise Fail(f"MVGLTools falló ({' '.join(map(str, args[:2]))}): {r.stderr.strip()[:300]}")


# ---------- armado ----------

def extract(tool, mvgl, name, out_dir, work):
    unpacked = work / "unpacked" / name
    run_tool(tool, "--mode=unpack-mvgl", "-i", mvgl, "-o", unpacked)
    for d in sorted(p for p in unpacked.iterdir() if p.is_dir()):
        run_tool(tool, "--mode=unpack-mbe-dir", "-i", d, "-o", out_dir / name / d.name)


def pack(tool, src, name, work):
    repacked = work / "repacked" / name
    for d in sorted(p for p in (src / name).iterdir() if p.is_dir()):
        run_tool(tool, "--mode=pack-mbe-dir", "-i", d, "-o", repacked / d.name)
    out = work / "dist" / f"{name}.dx11.mvgl"
    out.parent.mkdir(parents=True, exist_ok=True)
    run_tool(tool, "--mode=pack-mvgl", "-i", repacked, "-o", out)
    return out


def read_installed():
    return set(INSTALLED.read_text().split()) if INSTALLED.exists() else set()


def cmd_install(args):
    game = find_game(args.game)
    say(f"Juego: {game}")
    installed = read_installed()
    sources = {}
    for name in td.ARCHIVES:
        cur = archive_file(game, name)
        if sha256(cur) in installed:  # ya está la traducción: el inglés sale del original respaldado
            orig = BACKUP / cur.name
            if not orig.exists():
                raise Fail(f"Falta el respaldo {orig}. En Steam: Propiedades > Archivos instalados > Verificar integridad, y reintenta.")
            sources[name] = orig
        else:
            sources[name] = cur
        if sha256(sources[name]) != SUPPORTED[name]:
            say(f"AVISO: {name} no es la versión del juego que traducimos (actualización de Steam del 2026-09-17).")
            say("       Algunas líneas pueden verse en inglés o desfasadas.")
            if not args.force:
                if not sys.stdin.isatty() or input("¿Continuar de todos modos? [s/N] ").strip().lower() not in ("s", "si", "sí", "y"):
                    raise Fail("Cancelado. Con --force sigue sin preguntar.")
    tool = find_tool()
    work = Path(tempfile.mkdtemp(prefix="thl-"))
    try:
        say("1/3 Extrayendo los textos de tu juego...")
        vanilla = work / "vanilla"
        for name in td.ARCHIVES:
            extract(tool, sources[name], name, vanilla, work)
        say("2/3 Aplicando la traducción...")
        td.VANILLA = vanilla
        generar.build(work / "es")
        say("3/3 Empaquetando e instalando...")
        BACKUP.mkdir(exist_ok=True)
        built = {name: pack(tool, work / "es", name, work) for name in td.ARCHIVES}
        for name in td.ARCHIVES:
            cur = archive_file(game, name)
            if sha256(cur) not in installed:  # lo que hay es el original: se respalda antes de pisarlo
                shutil.copyfile(cur, BACKUP / cur.name)
            shutil.copyfile(built[name], cur)
            installed.add(sha256(built[name]))
            say(f"  instalado: {name}")
        INSTALLED.write_text("\n".join(sorted(installed)) + "\n")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    say("\nListo. Abre el juego, pon el idioma en English y verás el texto en español.")
    say("Para quitarla: ejecuta el desinstalador.")


def cmd_uninstall(args):
    game = find_game(args.game)
    installed = read_installed()
    for name in td.ARCHIVES:
        cur = archive_file(game, name)
        orig = BACKUP / cur.name
        if sha256(cur) in installed and orig.exists():
            shutil.copyfile(orig, cur)
            say(f"restaurado: {name}")
        else:
            say(f"sin cambios: {name} no tiene la traducción instalada")
    say("\nSi algo quedó mal, en Steam: Propiedades > Archivos instalados > Verificar integridad.")


def cmd_status(args):
    game = find_game(args.game)
    say(f"Juego: {game}")
    installed = read_installed()
    for name in td.ARCHIVES:
        h = sha256(archive_file(game, name))
        if h in installed:
            state = "traducción instalada"
        elif h == SUPPORTED[name]:
            state = "original (sin traducción)"
        else:
            state = "versión distinta de la traducida"
        say(f"  {name}: {state}")


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["install", "uninstall", "status"])
    ap.add_argument("--game")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--pause", action="store_true")
    args = ap.parse_args()
    code = 0
    try:
        {"install": cmd_install, "uninstall": cmd_uninstall, "status": cmd_status}[args.cmd](args)
    except Fail as e:
        say(f"\nError: {e}")
        code = 1
    if args.pause:
        try:
            input("\nPulsa Enter para cerrar...")
        except EOFError:
            pass
    sys.exit(code)


if __name__ == "__main__":
    main()
