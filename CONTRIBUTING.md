# Guía para colaborar

Cómo está armado el proyecto y cómo se trabaja en él. Si solo quieres instalar la traducción, ve al [README](README.md).

Todo cambio entra por pull request y lo aprueba la persona que mantiene el repositorio. Antes de traducir: [STYLE.md](STYLE.md) y [GLOSSARY.md](GLOSSARY.md).

La traducción está en `translation/`, por ID de línea, y guarda **solo nuestro texto**: el japonés y el inglés salen de la copia del juego de cada persona (`scripts/extract.sh`).
`table/` (japonés, inglés y español de cada línea, para revisar) se genera en local con `python3 -I scripts/thl.py table` y **no se sube**: tiene el texto del juego.

## Instalador

`scripts/installer.py` (`install`, `uninstall`, `status`) hace en Python y sin dependencias lo mismo que `extract.sh` + `build.sh` + `install.sh`, y funciona en Windows y en Linux. Es lo que usan los paquetes de las releases. Los `.sh` siguen para trabajar con las traducciones (también extraen el japonés).
Los dos comparten `backup/installed.sha256`, así que se pueden mezclar.

## Publicar una release

```
python3 -I scripts/make-release.py v0.1.1      # -> dist/release/THL-ESP-v0.1.1-windows.zip y -linux.tar.gz
```

Cada paquete se descomprime dentro de la carpeta del juego y trae el instalador, la traducción, MVGLTools (con su licencia) y los lanzadores
`INSTALAR` / `DESINSTALAR` (Windows trae también Python embebido). No incluye el juego ni los `.mvgl` traducidos: el instalador los arma con la copia de cada persona.
Las descargas (MVGLTools, Python) se verifican contra los hashes fijados en el script. Se suben con `gh release create` / `gh release upload`.
Antes de publicar, probar `INSTALAR` y `DESINSTALAR` en Windows y en Steam Deck.

## Dos versiones

`python3 -I scripts/thl.py --version en <comando>` (o `THL_VERSION=en`) trabaja sobre `translation-en/` y `table-en/`; sin la opción, sobre `translation/` (jp).
En `en`, un archivo cuenta como pendiente hasta que se marca rehecho con `thl.py --version en hecho <patrón> <ediciones.jsonl>…`
(solo lo marca si todas sus líneas están en los JSONL). El export muestra `ES(jp)` como punto de partida.

## Estructura

```
translation/<message|text>/<archivo>/<hoja>.tsv   traducción del doblaje japonés (base japonés)
translation-en/…       traducción del doblaje inglés (base inglés); hecho.txt lista los archivos ya rehechos desde el inglés
review/ignore.csv      avisos de los chequeos revisados que no son errores
scripts/thl.py          trabajo: ver líneas, aplicar traducciones, ver cambios, chequeos, progreso
scripts/thldatos.py     lectura del original y de la traducción (lo usa thl.py)
scripts/thlchecks.py    chequeos automáticos
scripts/extract.sh      textos originales del juego -> build/vanilla y build/jp
scripts/generar.py      original + traducción -> build/es (lo usa build.sh)
scripts/build.sh [jp|en]  build/es-<versión> -> dist/<versión>/*.mvgl, y app_1 con las fuentes del menú arregladas
scripts/thlfuente.py    rehace á é í ó ú ñ ü ¿ ¡ de las fuentes del menú con el ancho de las demás letras
scripts/install.sh [jp|en]  instala dist/<versión>/ en el juego (sin versión, pregunta) (respalda los originales en backup/)
scripts/uninstall.sh    quita la traducción restaurando los originales
scripts/get-tools.sh    descarga MVGLToolsCLI v2.2.0 (Linux) en tools/
scripts/installer.py    instalador multiplataforma (install, uninstall, status)
scripts/make-release.py arma los paquetes de Windows y Linux de una release
```

Cada `.tsv` tiene una línea por fila traducida del juego, con tres columnas separadas por tabulador:

- `id`: el ID de la fila en el archivo del juego.
- `huella_jp`: huella (sha1, 8 caracteres) del japonés con el que se tradujo. Si una actualización del juego lo cambia, `thl.py check` lo avisa.
- `es`: el texto en español, con los saltos de línea como `\n`. Vacío = la línea queda como el original (nombres, siglas, símbolos).

Archivos de texto del juego: `app_text01.dx11.mvgl` y `patch_text01.dx11.mvgl` (inglés), `app_text00` y `patch_text00` (japonés).
La versión de Steam suma `app_steam_text01` y `patch_steam_text01` (y `_text00` en japonés) con los textos propios de PC: opciones gráficas, *Salir del juego*, avisos del sistema.
Fuentes del menú: `commonfont.bin` y `commonfont2.bin`, dentro de `app_1.dx11.mvgl`. Son japonesas y sus letras con tilde son más anchas que las demás; `thlfuente.py` las rehace en la copia de cada persona al instalar. Las fuentes no se suben al repositorio.
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
