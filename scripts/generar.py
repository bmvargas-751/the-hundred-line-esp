"""Arma los CSV del juego en español: cada archivo del inglés original con nuestra traducción encima.

Uso: python3 -I scripts/generar.py <destino>   (lo usa scripts/build.sh, con destino build/es)
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thldatos as td  # noqa: E402


def build(dest):
    dest = Path(dest)
    shutil.rmtree(dest, ignore_errors=True)
    translated = 0
    for arch in td.ARCHIVES:
        for src in sorted((td.VANILLA / arch).rglob("*.csv")):
            rel = src.relative_to(td.VANILLA / arch)
            out = dest / arch / rel
            ours = {k: es for k, (_, es) in td.load_es(rel).items() if es}  # vacío = queda el original
            if not ours:
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, out)
                continue
            # La misma traducción va en app y en patch: el juego usa el de patch si el archivo está en los dos
            header, rows = td.load(src)
            col = td.TEXT_COL[rel.parts[0]]
            for row_id, row in rows.items():
                if row_id in ours:
                    row[col] = ours[row_id]
                    translated += 1
            td.save(out, header, rows.values())
    print(f"filas traducidas (app y patch): {translated}")
    return translated


if __name__ == "__main__":
    build(sys.argv[1])
