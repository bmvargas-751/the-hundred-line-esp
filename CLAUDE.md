# Reglas del repo

Traducción de *The Hundred Line -Last Defense Academy-* al español con el kit de traducción de juegos (`~/.claude/loc-kit`: METHOD.md y REPO.md).

- Empezar o retomar el proyecto: skill `loc-start`. Traducir un lote: skill `loc-batch`.
- `main` está protegido: todo cambio va en una rama y un pull request, sin firma de Claude. El usuario fusiona; Claude nunca fusiona.
- Al cerrar un lote o una fase: casillas del PLAN, `loc.py progress --readme`, commit, push y pull request, sin pedir permiso.
- Sin spoilers en los documentos, los commits, los pull requests y el chat: se nombran zonas o archivos, nunca hechos de la historia.
- En el repo nunca van archivos del juego: lo extraído vive fuera, en `../local/NOMBRE/`.
- No se inventan reglas: solo valen STYLE.md, TECH.md, GLOSSARY.md, las fichas de `characters/` y DECISIONS.md. Lo que no cubren va a PENDING.md.
- Antes de lanzar agentes, estimar el costo y pedir el visto bueno; nunca más de unos 3 a la vez.

## Lo propio de este repo

- THL es anterior al kit: lo adoptó la skill `loc-adopt` (2026-11-23).
  - La traducción vive en los TSV de `translation/` (`id`, `huella_jp`, `es`); el kit la lee y la escribe con `scripts/hooks.py`, con las mismas reglas que `scripts/thl.py apply`.
  - El original del kit se exporta con `python3 -I scripts/kit_adapter.py export`, a `../local/the-hundred-line/source.jsonl` (con el japonés como apoyo). Hace falta antes `scripts/extract.sh`.
  - Lo extraído del juego sigue en `build/` (ignorado), porque lo usan `build.sh`, `generar.py` y el instalador.
- El README lo escribe el kit (`loc.py progress --readme`): «Instalar» sale de `project.json`. `thl.py progress --readme` ya no se usa; `thl.py progress` sigue sirviendo para ver el avance por archivo.
- Las skills de `.claude/skills/` son las de THL de antes del kit (locales). Las correcciones nuevas van con `loc-batch`, que pide antes el set de oro (fase 4).
- Los paquetes se arman con `scripts/make-release.py`; cómo se trabaja, en CONTRIBUTING.md.
