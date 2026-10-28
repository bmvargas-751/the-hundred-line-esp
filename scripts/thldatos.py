"""Acceso a los textos: originales del juego (build/), nuestra traducción (translation/) y vista unificada."""
import csv
import hashlib
import os
import re
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Dos versiones de la traducción: "jp" (base japonés, para jugar con el doblaje japonés) y
# "en" (base inglés, para el doblaje inglés). Cada una tiene su carpeta.
VERSIONS = {"jp": "translation", "en": "translation-en"}
VERSION_NAMES = {"jp": "Doblaje japonés", "en": "Doblaje inglés"}
VERSION = "jp"
TRANSLATION = ROOT / VERSIONS["jp"]
VANILLA = ROOT / "build" / "vanilla"  # inglés original (scripts/extract.sh)
JAPANESE = ROOT / "build" / "jp"  # japonés original (scripts/extract.sh)
# En orden de prioridad creciente: patch pisa a app. Los _steam traen los textos propios de la versión de PC
# (opciones gráficas, "Salir del juego"...), con nombres de archivo distintos a los del resto.
ARCHIVES = ("app_text01", "app_steam_text01", "patch_text01", "patch_steam_text01")
JP_ARCHIVES = ("app_text00", "app_steam_text00", "patch_text00", "patch_steam_text00")
TEXT_COL = {"message": 2, "text": 1}  # columna con el texto visible (la misma en inglés, japonés y español)
TSV_HEADER = ["id", "huella_jp", "es"]

def set_version(version):
    """Elige con qué traducción se trabaja: 'jp' o 'en'."""
    global VERSION, TRANSLATION
    if version not in VERSIONS:
        raise SystemExit(f"Versión desconocida: {version} (usa jp o en)")
    VERSION = version
    TRANSLATION = ROOT / VERSIONS[version]


set_version(os.environ.get("THL_VERSION", "jp"))

# Grupos de archivos de diálogo, por prefijo (descripciones sin spoilers)
GROUPS = [
    (r"r00_", "Primera partida"),
    (r"s(\d\d)_", "Partidas posteriores, ruta s{0}"),
    (r"a_chr", "Reacciones a regalos"),
    (r"g_chr", "Eventos de tiempo libre"),
    (r"k_chr", "Conversaciones con personajes"),
    (r"npc_chr", "Charlas en exploración"),
    (r"gim_", "Objetos y biblioteca"),
]


def load(path):
    """CSV de MVGLToolsCLI -> (encabezado, {id: fila}), en el orden del archivo."""
    if not path.exists():
        return None, {}
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], {r[0]: r for r in rows[1:] if r}


def save(path, header, rows):
    """Escribe en el formato de MVGLToolsCLI: columnas int sin comillas, string entre comillas."""
    numeric = [h.startswith(("int", "float")) for h in header]

    def cell(value, is_num):
        return value if is_num else '"' + value.replace('"', '""') + '"'

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            f.write(",".join(cell(v, n) for v, n in zip(row, numeric)) + "\n")


def day(name):
    m = re.search(r"_d(\d{3})_", name)
    return int(m.group(1)) if m else None


def group(name):
    for rx, label in GROUPS:
        m = re.match(rx, name)
        if m:
            return label.format(*m.groups())
    return "Otros"


def split_key(key):
    """'message/<mbe>/<hoja>#<id>' -> (ruta relativa al archivo .mvgl, id)."""
    path, row_id = key.rsplit("#", 1)
    kind, mbe, sheet = path.split("/")
    return Path(kind) / f"{mbe}.mbe" / f"{sheet}.csv", row_id


def make_key(rel, row_id):
    return f"{rel.parts[0]}/{rel.parts[1][:-4]}/{rel.stem}#{row_id}"


def jp_hash(text):
    """Huella del japonés con el que se tradujo una línea: si el juego lo cambia, check lo avisa."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


# Traducción: translation/<kind>/<mbe>/<hoja>.tsv, una línea por fila del juego: id, huella_jp, es.
# "es" vacío = la línea queda como el original (nombres, siglas, símbolos). Saltos de línea como \n.
ESCAPES = {"\\": "\\\\", "\t": "\\t", "\n": "\\n", "\r": "\\r"}
UNESCAPES = {v[1]: k for k, v in ESCAPES.items()}


def escape(s):
    return "".join(ESCAPES.get(c, c) for c in s)


def unescape(s):
    return re.sub(r"\\(.)", lambda m: UNESCAPES[m.group(1)], s)


def tsv_path(rel):
    return TRANSLATION / rel.parts[0] / rel.parts[1][:-4] / f"{rel.stem}.tsv"


def tsv_rel(path):
    """translation/<kind>/<mbe>/<hoja>.tsv -> kind/<mbe>.mbe/<hoja>.csv"""
    kind, mbe, sheet = Path(path).relative_to(TRANSLATION).parts
    return Path(kind) / f"{mbe}.mbe" / f"{Path(sheet).stem}.csv"


def parse_tsv(text):
    """Contenido de un .tsv -> {id: (huella_jp, es)}"""
    out = {}
    for line in text.split("\n")[1:]:  # no splitlines: cortaría en separadores Unicode del texto
        if not line:
            continue
        row_id, h, es = line.split("\t")
        out[row_id] = (h, unescape(es))
    return out


def load_es(rel):
    path = tsv_path(rel)
    return parse_tsv(path.read_text(encoding="utf-8")) if path.exists() else {}


def save_es(rel, entries):
    """Guarda en el orden de las filas del juego; sin entradas, borra el archivo."""
    path = tsv_path(rel)
    if not entries:
        path.unlink(missing_ok=True)
        return
    order = {k: i for i, k in enumerate(original(rel))}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(TSV_HEADER) + "\n")
        for row_id in sorted(entries, key=lambda k: order.get(k, len(order))):
            h, es = entries[row_id]
            f.write(f"{row_id}\t{h}\t{escape(es)}\n")


def files(pattern="*"):
    """Archivos del juego (kind/x.mbe/hoja.csv) cuyo 'kind/nombre' coincide con el patrón, con el archivo que usa el juego."""
    if not VANILLA.exists():
        raise SystemExit("Falta el original del juego en build/vanilla: correr scripts/extract.sh")
    found = {}
    for arch in ARCHIVES:
        for p in (VANILLA / arch).rglob("*.csv"):
            rel = p.relative_to(VANILLA / arch)
            if fnmatch(f"{rel.parts[0]}/{rel.parts[1][:-4]}", pattern):
                found[rel] = arch
    return dict(sorted(found.items()))


def original(rel):
    """Filas del inglés original que usa el juego para un archivo (el de patch si existe)."""
    for arch in reversed(ARCHIVES):
        header, rows = load(VANILLA / arch / rel)
        if header:
            return rows
    return {}


def hecho():
    """Versión 'en': archivos ('kind/nombre') ya rehechos desde el inglés. En 'jp' no se usa."""
    path = TRANSLATION / "hecho.txt"
    if VERSION == "jp" or not path.exists():
        return None if VERSION == "jp" else set()
    return {l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}


def japanese(rel):
    """Filas del japonés original para un archivo (patch sobre app)."""
    rows = {}
    for arch in JP_ARCHIVES:
        rows.update(load(JAPANESE / arch / rel)[1])
    return rows


def char_names():
    rel = Path("text/char_name.mbe/000_char_name.csv")
    names = {k: r[1] for k, r in original(rel).items()}
    names.update({k: es for k, (_, es) in load_es(rel).items() if es})
    return names


def lines(pattern="*"):
    """Vista unificada: una entrada por línea del juego, tomada del archivo que el juego usa.

    estado: "traducida", "original" (se decidió dejarla como el inglés) o "pendiente".
    es: lo que mostraría el juego en español ("" si está pendiente).
    """
    if not JAPANESE.exists():
        raise SystemExit("Falta el japonés en build/jp: correr scripts/extract.sh")
    names = char_names()
    done_files = hecho()
    out = []
    for rel, arch in files(pattern).items():
        kind = rel.parts[0]
        mbe = rel.parts[1][:-4]
        col = TEXT_COL[kind]
        rows = load(VANILLA / arch / rel)[1]
        jp = japanese(rel)
        ours = load_es(rel)
        for row_id, r in rows.items():
            en = r[col]
            jp_text = jp[row_id][col] if row_id in jp else ""
            h, es = ours.get(row_id, (None, None))
            state = "pendiente" if h is None else ("original" if es == "" else "traducida")
            seed = None
            if done_files is not None and f"{kind}/{mbe}" not in done_files and state != "pendiente":
                # versión 'en': el texto de la versión japonesa sirve de punto de partida, pero falta rehacerlo
                seed = es or en
                state = "pendiente"
            out.append({
                "key": make_key(rel, row_id), "archive": arch,
                "group": group(mbe) if kind == "message" else "Interfaz", "day": day(mbe),
                "speaker": names.get(r[1], r[1]) if kind == "message" else "",
                "jp": jp_text, "en": en,
                "es": {"pendiente": "", "original": en, "traducida": es}[state],
                "estado": state, "huella": h, "huella_jp": jp_hash(jp_text), "semilla": seed,
            })
    return out
