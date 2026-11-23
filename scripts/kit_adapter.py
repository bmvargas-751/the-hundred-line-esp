"""Adaptador de The Hundred Line para el kit de traducción (~/.claude/loc-kit).

    python3 -I scripts/kit_adapter.py export

Escribe el original en el formato común del kit, en ../local/the-hundred-line/source.jsonl
(el «source» de loc.json): una línea por texto del juego, en su orden, con
{key, en, ja, speaker, note}. Lo lee de build/vanilla y build/jp con thldatos
(hace falta scripts/extract.sh). La traducción no se mueve: la leen y la
escriben los hooks (scripts/hooks.py) sobre los TSV de translation/.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thldatos as td  # noqa: E402

LOCAL = td.ROOT.parent / "local" / "the-hundred-line"


def export():
    LOCAL.mkdir(parents=True, exist_ok=True)
    out = LOCAL / "source.jsonl"
    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for r in td.lines():
            note = r["group"] + (f", Día {r['day']}" if r["day"] is not None else "")
            d = {"key": r["key"], "en": r["en"], "ja": r["jp"], "note": note}
            if r["speaker"]:
                d["speaker"] = r["speaker"]
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
            n += 1
    print(f"{n} líneas en {out}")


if __name__ == "__main__":
    if sys.argv[1:] != ["export"]:
        raise SystemExit(__doc__)
    export()
