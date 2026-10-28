"""Herramienta de traducción.

  python3 -I scripts/thl.py export <patrón> [--pendientes] [--jsonl]   JP, EN y ES de cada línea, en el orden del juego
  python3 -I scripts/thl.py apply <ediciones.jsonl>                    guarda traducciones en translation/
  python3 -I scripts/thl.py diff [revisión]                            cambios de la traducción frente a git (por defecto HEAD)
  python3 -I scripts/thl.py check [patrón]                             chequeos automáticos -> build/checks.csv
  python3 -I scripts/thl.py progress [patrón] [--files] [--readme]    líneas traducidas y pendientes
  python3 -I scripts/thl.py table                                      regenera table/: JP, EN y ES de cada línea, por sección

<patrón> se compara con 'message/<nombre>' o 'text/<nombre>' (sin .mbe), con comodines:
  'message/r00_*_d000_*'  prólogo de la primera partida
  'text/*'                toda la interfaz

Con --version en (antes del comando) todo trabaja sobre translation-en/ y table-en/.

Cada línea de ediciones.jsonl: {"key": "...", "es": "texto nuevo", "old": "texto actual (opcional)"}.
Con "old", la edición solo se aplica si el español actual coincide ("" si la línea está pendiente).
"es" igual al inglés: la línea queda como el original. "es": null la vuelve a dejar pendiente.
"""
import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thldatos as td  # noqa: E402


def cmd_export(args):
    rows = [r for r in td.lines(args.pattern) if not args.pendientes or r["estado"] == "pendiente"]
    if args.jsonl:
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return
    for r in rows:
        where = r["group"] + (f", Día {r['day']}" if r["day"] is not None else "")
        print(f"[{r['key']}] {where}" + (f" — {r['speaker']}" if r["speaker"] else ""))
        if r["jp"]:
            print(f"  JP: {r['jp']}")
        print(f"  EN: {r['en']}")
        if r.get("semilla") is not None:
            print(f"  ES(jp): {r['semilla']}")
        if r["estado"] != "pendiente":
            print(f"  ES: {r['es']}" + (" (como el original)" if r["estado"] == "original" else ""))
    print(f"{len(rows)} líneas", file=sys.stderr)


def cmd_hecho(args):
    """Versión 'en': marca como rehechos los archivos del patrón, si todas sus líneas están en los JSONL dados."""
    if td.VERSION == "jp":
        raise SystemExit("hecho es solo para --version en")
    edited = set()
    for path in args.jsonl:
        edited |= {json.loads(l)["key"] for l in open(path, encoding="utf-8") if l.strip()}
    todo = defaultdict(list)
    for r in td.lines(args.pattern):
        if r["en"].strip():
            todo[r["key"].split("#")[0].rsplit("/", 1)[0]].append(r["key"])
    new, missing = [], 0
    for name, keys in sorted(todo.items()):
        faltan = [k for k in keys if k not in edited]
        if faltan:
            missing += len(faltan)
            print(f"{name}: faltan {len(faltan)} líneas (ej. {faltan[0]})")
        else:
            new.append(name)
    path = td.TRANSLATION / "hecho.txt"
    have = set(path.read_text(encoding="utf-8").split("\n")) if path.exists() else set()
    path.write_text("\n".join(sorted((have | set(new)) - {""})) + "\n", encoding="utf-8")
    print(f"marcados como hechos: {len(new)} archivos; sin marcar: {len(todo) - len(new)} ({missing} líneas sin tocar)")


def cmd_apply(args):
    edits = [json.loads(line) for line in open(args.edits, encoding="utf-8") if line.strip()]
    by_file = defaultdict(list)
    for e in edits:
        rel, row_id = td.split_key(e["key"])
        by_file[rel].append((row_id, e))

    applied, skipped = 0, []
    for rel, items in by_file.items():
        col = td.TEXT_COL[rel.parts[0]]
        game = td.original(rel)
        jp = td.japanese(rel)
        ours = td.load_es(rel)
        for row_id, e in items:
            if row_id not in game:
                skipped.append((e["key"], "no existe en el juego"))
                continue
            en = game[row_id][col]
            h, es = ours.get(row_id, (None, None))
            current = "" if h is None else (es or en)
            if "old" in e and e["old"] != current:
                skipped.append((e["key"], "el español actual no coincide con 'old'"))
                continue
            if e["es"] is None:
                ours.pop(row_id, None)
            else:
                # Igual al inglés: se guarda vacío, así el repo no lleva texto del juego
                ours[row_id] = (td.jp_hash(jp[row_id][col] if row_id in jp else ""), "" if e["es"] == en else e["es"])
            applied += 1
        td.save_es(rel, ours)

    print(f"aplicadas: {applied} | omitidas: {len(skipped)}")
    for key, why in skipped:
        print(f"  omitida {key}: {why}")
    if skipped:
        sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", str(td.ROOT), *args], capture_output=True, text=True, check=True).stdout


def cmd_diff(args):
    names = set(git("diff", "--name-only", args.rev, "--", td.TRANSLATION.name).split())
    names |= set(git("ls-files", "--others", "--exclude-standard", "--", td.TRANSLATION.name).split())
    changes = []
    for name in sorted(names):
        path = td.ROOT / name
        rel = td.tsv_rel(path)
        try:
            old = td.parse_tsv(git("show", f"{args.rev}:{name}"))
        except subprocess.CalledProcessError:
            old = {}  # archivo nuevo
        new = td.load_es(rel)
        game = td.original(rel)
        col = td.TEXT_COL[rel.parts[0]]
        for row_id in game:
            en = game[row_id][col]
            before, after = (old.get(row_id, (None, None))[1], new.get(row_id, (None, None))[1])
            if before != after:
                changes.append((td.make_key(rel, row_id), en, before, after))

    def show(es, en):
        return "(pendiente)" if es is None else (es or f"(como el original) {en}")

    for key, en, before, after in changes:
        print(f"[{key}]")
        print(f"  EN: {en}")
        print(f"  - : {show(before, en)}")
        print(f"  + : {show(after, en)}")
    print(f"{len(changes)} líneas cambiadas", file=sys.stderr)


def cmd_check(args):
    import thlchecks
    # Casos revisados que no son errores: check,key,motivo
    ignore_path = td.ROOT / "review" / "ignore.csv"
    ignored = set()
    if ignore_path.exists():
        with open(ignore_path, newline="", encoding="utf-8") as f:
            ignored = {(r["check"], r["key"]) for r in csv.DictReader(f)}
    # Interfaz: el mismo japonés debe tener la misma traducción en todos los archivos (los _bug se deforman a propósito)
    def comparable(r):
        return r["key"].startswith("text/") and "_bug" not in r["key"] and r["estado"] != "pendiente" and r["jp"].strip()

    variants = defaultdict(Counter)
    for r in td.lines("text/*"):
        if comparable(r):
            variants[r["jp"].strip()][r["es"]] += 1
    report = []
    for r in td.lines(args.pattern):
        if r["estado"] == "pendiente":
            continue
        found = thlchecks.check_line(r)
        if r["huella"] != r["huella_jp"]:
            found.append(("japones_cambiado", "el juego cambió el japonés desde que se tradujo"))
        # Solo se marcan nuestras traducciones: si dos líneas quedan como el original, la diferencia es del inglés
        if comparable(r) and r["estado"] == "traducida" and len(variants[r["jp"].strip()]) > 1:
            others = "; ".join(f"'{es}' ({n})" for es, n in variants[r["jp"].strip()].items() if es != r["es"])
            found.append(("inconsistente", f"el mismo japonés está traducido de otra forma: {others}"))
        for name, detail in found:
            if (name, r["key"]) in ignored:
                continue
            report.append([name, r["key"], r["group"], r["day"] if r["day"] is not None else "", r["speaker"],
                           detail, r["en"], r["es"]])
    out = td.ROOT / "build" / "checks.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["check", "key", "group", "day", "speaker", "detail", "en", "es"])
        w.writerows(sorted(report, key=lambda x: (x[0], x[1])))
    counts = defaultdict(set)
    for name, key, *_ in report:
        counts[name].add(key)
    for name, keys in sorted(counts.items(), key=lambda x: -len(x[1])):
        print(f"{name:16} {len(keys):6} líneas")
    print(f"reporte: {out}")


SECTIONS = ["Interfaz", "Primera partida", "Partidas posteriores", "Eventos y charlas"]  # en el orden de las fases del PLAN


def area(r):
    if r["group"] in ("Interfaz", "Primera partida"):
        return r["group"]
    return "Partidas posteriores" if r["group"].startswith("Partidas") else "Eventos y charlas"


def num(n):
    return f"{n:,}".replace(",", ".")


def pct(done, total):
    return f"{100 * done / total:.1f} %".replace(".", ",")


def current_stage():
    """Etapa en curso según PLAN.md: la fase marcada '← en curso' y su primer punto sin hacer."""
    plan = td.ROOT / "PLAN.md"
    if not plan.exists():  # PLAN.md es local: sin él no se muestra la etapa
        return None
    lines = plan.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"### (Fase \d+)\. (.+?)(?: \(`.*`\))? ←", line)
        if not m:
            continue
        for item in lines[i + 1:]:
            if item.startswith("### "):
                break
            if item.startswith("- [ ] "):
                step = re.sub(r"\s*\(`.*", "", item[6:])  # sin la lista de archivos
                return f"{m.group(1)} ({m.group(2)}), {step[0].lower()}{step[1:]}"
        return f"{m.group(1)} ({m.group(2)})"
    return None


def update_readme(total, done):
    """Reescribe la tabla de avance del README, entre los marcadores <!-- progress ... --> y <!-- /progress -->."""
    t, d = sum(total.values()), sum(done.values())
    stage = current_stage()
    rows = [f"**Etapa actual:** {stage}.", ""] if stage else []
    rows += ["| Fase | Sección | Traducidas | Total | % |", "|---|---|---:|---:|---:|"]
    rows += [f"| {i} | {s} | {num(done[s])} | {num(total[s])} | {pct(done[s], total[s])} |"
             for i, s in enumerate(SECTIONS, 1)]
    rows.append(f"| | **Total** | **{num(d)}** | **{num(t)}** | **{pct(d, t)}** |")
    path = td.ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("\n", text.index("<!-- progress")) + 1
    end = text.index("<!-- /progress -->")
    path.write_text(text[:start] + "\n".join(rows) + "\n" + text[end:], encoding="utf-8")
    print(f"README actualizado: {path}")


def cmd_progress(args):
    """Solo cuentan las líneas con texto visible en el original."""
    if args.readme and td.VERSION != "jp":
        raise SystemExit("--readme es solo de la versión jp")
    if args.readme and (args.pattern != "*" or args.files):
        raise SystemExit("--readme cuenta todo el juego: sin patrón ni --files")
    total, done = Counter(), Counter()
    for r in td.lines(args.pattern):
        if not r["en"].strip():
            continue
        name = r["key"].split("#")[0] if args.files else area(r)
        total[name] += 1
        done[name] += r["estado"] != "pendiente"
    order = sorted(total) if args.files else [s for s in SECTIONS if s in total]
    for name in order:
        if args.files and done[name] == total[name]:
            continue
        print(f"{name:40} {done[name]:7} de {total[name]:7}  {pct(done[name], total[name]):>7}"
              f"  faltan {total[name] - done[name]}")
    t, d = sum(total.values()), sum(done.values())
    print(f"{'Total':40} {d:7} de {t:7}  {pct(d, t):>7}")
    if args.readme:
        update_readme(total, done)


# table/: cada línea con el japonés, el inglés y el español, para leer en GitHub. Es la única copia del texto del juego en el repo.
TABLE = td.ROOT / "table"  # con --version en: table-en/ (se fija en main)
SECTION_DIRS = dict(zip(SECTIONS, ["interface", "first-playthrough", "later-playthroughs", "events-and-chats"]))
PAGE_MAX = 150_000  # bytes por página: GitHub deja de mostrar las tablas muy largas
COLOR_CODES = re.compile(r"\{[a-z]+\d*(?:\([^)]*\))?|\}")


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_cell(text):
    """Texto para una celda de Markdown: sin códigos de color, con <br> en los saltos de línea."""
    text = COLOR_CODES.sub("", text.replace("{chr}", "[chr]"))
    text = html.escape(text, quote=False).replace("|", "\\|")
    return "<br>".join(part.strip() for part in text.strip().split("\n"))


def table_page_of(r):
    """Página de una línea: (carpeta, archivo, título, nombre en el índice)."""
    section, d = area(r), r["day"]
    mbe = r["key"].split("/")[1]
    day_file, day_name = (f"day-{d:03d}", f"Día {d}") if d is not None else ("other", "Otros")
    if section == "Interfaz":
        return SECTION_DIRS[section], mbe, f"Interfaz — {mbe}", mbe
    if section == "Primera partida":
        return SECTION_DIRS[section], day_file, f"Primera partida — {day_name}", day_name
    if section == "Partidas posteriores":
        route = r["group"].rsplit(" ", 1)[1]
        return f"{SECTION_DIRS[section]}/{route}", day_file, f"Partidas posteriores — ruta {route}, {day_name}", day_name
    return SECTION_DIRS[section], slug(r["group"]), f"Eventos y charlas — {r['group']}", r["group"]


def table_row(r):
    cells = [r["key"].rsplit("#", 1)[1]]
    if r["key"].startswith("message/"):
        cells.append(md_cell(r["speaker"]))
    cells += [md_cell(r["jp"]) or "—", md_cell(r["en"]), "*Pendiente*" if r["estado"] == "pendiente" else md_cell(r["es"])]
    return "| " + " | ".join(cells) + " |"


def table_pages(rows):
    """Filas -> páginas de hasta PAGE_MAX bytes, con un encabezado y una tabla por archivo del juego."""
    pages, out, size, current = [], [], 0, None
    for r in rows:
        path = r["key"].split("#")[0]
        kind, mbe, sheet = path.split("/")
        line = table_row(r)
        full = out and size + len(line.encode()) > PAGE_MAX
        if full:
            pages.append(out)
            out, size = [], 0
        if path != current or full:
            cols = ["#", "Personaje"] if kind == "message" else ["#"]
            head = ([""] if out else []) + [
                f"## `{mbe if kind == 'message' else sheet}`" + (" (sigue)" if path == current else ""), "",
                "| " + " | ".join(cols + ["Japonés", "Inglés", "Español"]) + " |",
                "|---:|" + "---|" * (len(cols) + 2)]
            out += head
            size += sum(len(h.encode()) + 1 for h in head)
            current = path
        out.append(line)
        size += len(line.encode()) + 1
    return pages + [out]


def write_md(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def table_index(path, title, back, intro, entries):
    """Índice de una carpeta (GitHub lo muestra debajo de la lista de archivos): avance de cada página o subcarpeta."""
    lines = [f"# {title}", ""] + ([back, ""] if back else []) + intro
    lines += ["| | Líneas | Traducidas | % |", "|---|---:|---:|---:|"]
    lines += [f"| [{name}]({link}) | {num(t)} | {num(d)} | {pct(d, t)} |" for name, link, t, d in entries]
    t, d = sum(e[2] for e in entries), sum(e[3] for e in entries)
    lines.append(f"| **Total** | **{num(t)}** | **{num(d)}** | **{pct(d, t)}** |")
    write_md(path, lines)


def cmd_table(args):
    """Regenera table/ desde el juego extraído (build/) y translation/. Solo las líneas con texto visible."""
    pages, info = defaultdict(list), {}
    for r in td.lines():
        if r["en"].strip():
            folder, name, title, label = table_page_of(r)
            pages[(folder, name)].append(r)
            info[(folder, name)] = (title, label, area(r))
    shutil.rmtree(TABLE, ignore_errors=True)
    listing, by_section = defaultdict(list), defaultdict(lambda: [0, 0])
    for (folder, name), rows in pages.items():
        title, label, section = info[(folder, name)]
        parts = table_pages(rows)
        names = [f"{name}.md"] if len(parts) == 1 else [f"{name}-{i}.md" for i in range(1, len(parts) + 1)]
        t, d = len(rows), sum(r["estado"] != "pendiente" for r in rows)
        for i, (fname, body) in enumerate(zip(names, parts)):
            nav = ["[Índice](README.md)"]
            if len(parts) > 1:
                nav.append(f"parte {i + 1} de {len(parts)}")
                nav += [f"[anterior]({names[i - 1]})"] if i else []
                nav += [f"[siguiente]({names[i + 1]})"] if i + 1 < len(parts) else []
            head = [f"# {title}", "", " · ".join(nav), "",
                    f"{num(t)} líneas, {num(d)} traducidas ({pct(d, t)}). *Pendiente*: todavía sin traducir.", ""]
            write_md(TABLE / folder / fname, head + body)
        listing[folder].append((label, names[0], t, d))
        by_section[section][0] += t
        by_section[section][1] += d

    for section, folder in SECTION_DIRS.items():
        back = "[Volver a la tabla](../README.md)"
        if section != "Partidas posteriores":
            table_index(TABLE / folder / "README.md", section, back, [], listing[folder])
            continue
        routes = []
        for sub in sorted(f for f in listing if f.startswith(folder + "/")):
            route = sub.rsplit("/", 1)[1]
            entries = listing[sub]
            table_index(TABLE / sub / "README.md", f"{section} — ruta {route}", "[Volver a las rutas](../README.md)", [], entries)
            routes.append((f"Ruta {route}", f"{route}/README.md", sum(e[2] for e in entries), sum(e[3] for e in entries)))
        table_index(TABLE / folder / "README.md", section, back, [], routes)

    intro = [
        "Cada línea del juego, por sección: el japonés original, el inglés oficial y nuestro español "
        "(*Pendiente*: todavía sin traducir). Sin los códigos de color del juego.", "",
        "> **Spoilers:** tiene el texto completo de la historia. El japonés y el inglés son del juego: "
        "esta carpeta es solo para revisar la traducción.", "",
        "No se edita a mano: la traducción está en `translation/`. La regenera `python3 -I scripts/thl.py table` "
        "en cada bloque, desde la copia del juego que extrae `scripts/extract.sh`.", ""]
    table_index(TABLE / "README.md", "Tabla de textos", "[Volver al README](../README.md)", intro,
                [(s, f"{SECTION_DIRS[s]}/README.md", *by_section[s]) for s in SECTIONS])
    n = sum(1 for _ in TABLE.rglob("*.md"))
    print(f"table/: {n} archivos, {sum(len(v) for v in pages.values())} líneas")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", "-V", choices=sorted(td.VERSIONS), default=None,
                   help="jp (base japonés, por defecto) o en (base inglés); también THL_VERSION")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("pattern")
    e.add_argument("--pendientes", action="store_true", help="solo las líneas sin traducir")
    e.add_argument("--jsonl", action="store_true")
    a = sub.add_parser("apply")
    a.add_argument("edits")
    d = sub.add_parser("diff")
    d.add_argument("rev", nargs="?", default="HEAD")
    c = sub.add_parser("check")
    c.add_argument("pattern", nargs="?", default="*")
    v = sub.add_parser("progress")
    v.add_argument("pattern", nargs="?", default="*")
    v.add_argument("--files", action="store_true", help="por archivo, solo los que tienen pendientes")
    v.add_argument("--readme", action="store_true", help="actualiza la tabla de avance del README")
    h = sub.add_parser("hecho")
    h.add_argument("pattern")
    h.add_argument("jsonl", nargs="+")
    sub.add_parser("table")
    args = p.parse_args()
    global TABLE
    if args.version:
        td.set_version(args.version)
    if td.VERSION != "jp":
        TABLE = td.ROOT / f"table-{td.VERSION}"
    {"export": cmd_export, "apply": cmd_apply, "diff": cmd_diff, "check": cmd_check, "progress": cmd_progress,
     "table": cmd_table, "hecho": cmd_hecho}[args.cmd](args)


if __name__ == "__main__":
    main()
