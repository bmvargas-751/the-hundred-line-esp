# Guía para colaborar

Cómo está armado el proyecto y cómo se trabaja en él. Si solo quieres instalar la traducción, ve al [README](README.md).

Todo cambio entra por pull request y lo aprueba la persona que mantiene el repositorio. Antes de traducir: [STYLE.md](STYLE.md) y [GLOSSARY.md](GLOSSARY.md).

La traducción está en `translation/`, por ID de línea, y guarda **solo nuestro texto**: el japonés y el inglés salen de la copia del juego de cada persona (`scripts/extract.sh`).
`table/` (japonés, inglés y español de cada línea, para revisar) se genera en local con `python3 -I scripts/thl.py table` y **no se sube**: tiene el texto del juego.

## Estructura

```
translation/<message|text>/<archivo>/<hoja>.tsv   nuestra traducción
review/ignore.csv      avisos de los chequeos revisados que no son errores
scripts/thl.py          trabajo: ver líneas, aplicar traducciones, ver cambios, chequeos, progreso
scripts/thldatos.py     lectura del original y de la traducción (lo usa thl.py)
scripts/thlchecks.py    chequeos automáticos
scripts/extract.sh      textos originales del juego -> build/vanilla y build/jp
scripts/generar.py      original + traducción -> build/es (lo usa build.sh)
scripts/build.sh        build/es -> dist/*.mvgl
scripts/install.sh      instala dist/ en el juego (respalda los originales en backup/)
scripts/uninstall.sh    quita la traducción restaurando los originales
scripts/get-tools.sh    descarga MVGLToolsCLI v2.2.0 (Linux) en tools/
```

Cada `.tsv` tiene una línea por fila traducida del juego, con tres columnas separadas por tabulador:

- `id`: el ID de la fila en el archivo del juego.
- `huella_jp`: huella (sha1, 8 caracteres) del japonés con el que se tradujo. Si una actualización del juego lo cambia, `thl.py check` lo avisa.
- `es`: el texto en español, con los saltos de línea como `\n`. Vacío = la línea queda como el original (nombres, siglas, símbolos).

Archivos de texto del juego: `app_text01.dx11.mvgl` y `patch_text01.dx11.mvgl` (inglés), `app_text00` y `patch_text00` (japonés).
`patch` pisa a `app`: si un archivo está en los dos, el juego usa el de `patch`. `build.sh` pone la traducción en los dos.
Texto visible: en `message/`, columna `string 2`; en `text/`, `string 1`.

## Trabajar con `scripts/thl.py`

```
python3 -I scripts/thl.py export 'message/r00_*_d000_*'               # prólogo: JP, EN y ES
python3 -I scripts/thl.py export 'text/*' --pendientes                # interfaz sin traducir
python3 -I scripts/thl.py apply build/work/bloque.jsonl               # guarda traducciones en translation/
python3 -I scripts/thl.py diff                                        # cambios sin commitear, con el inglés
python3 -I scripts/thl.py check                                       # chequeos -> build/checks.csv
python3 -I scripts/thl.py progress --readme                             # avance por sección; actualiza la tabla de arriba
```

- `export` muestra cada línea como la ve el juego, en orden. Con `--jsonl` sale en formato para procesar.
- `apply` lee una traducción por línea: `{"key": "...", "es": "texto nuevo", "old": "texto actual"}`.
  Si el español actual no coincide con `old` (`""` si la línea está pendiente), no la aplica: así no se pisan cambios hechos en el medio.
  Si `es` es igual al inglés, la línea queda como el original; con `"es": null` vuelve a quedar pendiente.
- `progress --files` lista los archivos que tienen líneas pendientes.

Los archivos de trabajo (bloques exportados, JSONL) van en `build/work/`, que no se sube.

### Mapa de archivos de diálogo

| Prefijo | Contenido |
|---|---|
| `r00_` | Primera partida (Día 0 = prólogo, hasta el Día 100) |
| `s00_`…`s15_` | Partidas posteriores (rutas) |
| `a_chr` | Reacciones a regalos |
| `g_chr` | Eventos de tiempo libre con cada personaje |
| `k_chr` | Conversaciones con personajes (tipo por confirmar) |
| `npc_chr` | Charlas durante la exploración |
| `gim_` | Objetos y biblioteca |

En los nombres, `_dNNN_` es el día del juego. Los códigos de ruta del nombre del archivo no se usan para describir nada (pueden ser spoilers).

### Cuando el juego se actualiza

```
scripts/extract.sh                       # vuelve a extraer el original nuevo
python3 -I scripts/thl.py check          # japones_cambiado: líneas a revisar
scripts/build.sh && scripts/install.sh
```

Base actual: actualización del juego del 2026-09-17 (Steam).

## Herramientas

- [MVGLTools](https://github.com/SydMontague/MVGLTools) de SydMontague (`--game=thl`).
