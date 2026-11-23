"""Hooks del kit para The Hundred Line (ver loc.json y lockit/corpus.py del kit).

La traducción vive en los TSV de translation/ (id, huella_jp, es), como siempre:
el kit la lee y la escribe por aquí, con las mismas reglas que `thl.py apply`.
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thldatos as td  # noqa: E402


def read_translation():
    """{clave: lo que muestra el juego} de las líneas que no están pendientes (como `thl.py progress`)."""
    return {r["key"]: r["es"] for r in td.lines() if r["estado"] != "pendiente"}


def write_translation(changes):
    """Guarda {clave: texto}; igual al inglés se guarda vacío (la línea queda como el original)."""
    by_file = defaultdict(dict)
    for key, es in changes.items():
        rel, row_id = td.split_key(key)
        by_file[rel][row_id] = es
    for rel, items in by_file.items():
        col = td.TEXT_COL[rel.parts[0]]
        game = td.original(rel)
        jp = td.japanese(rel)
        ours = td.load_es(rel)
        for row_id, es in items.items():
            if row_id not in game:
                raise SystemExit(f"{td.make_key(rel, row_id)}: no existe en el juego")
            if es is None:
                ours.pop(row_id, None)
                continue
            en = game[row_id][col]
            old = ours.get(row_id)
            if old and (old[1] or en) == es:
                continue  # sin cambios: no se toca la huella
            ours[row_id] = (td.jp_hash(jp[row_id][col] if row_id in jp else ""), "" if es == en else es)
        td.save_es(rel, ours)


def excluded(key, item):
    """Como `thl.py progress`: solo cuentan las líneas con texto visible en el original."""
    return item is not None and not item.get("en", "").strip()
