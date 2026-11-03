# The Hundred Line -Last Defense Academy- — Traducción al español

Traducción **no oficial** al español neutro del juego *The Hundred Line -Last Defense Academy-*, con un glosario propio. Está hecha desde el **inglés oficial**, para que los subtítulos coincidan con el **doblaje inglés**; el japonés original solo se usa para resolver género, sujeto omitido y trato.

> **En revisión.** La interfaz, la primera partida y los eventos están completos; las rutas se están revisando para que suenen más naturales. Pueden quedar errores: [avísanos](https://github.com/bmvargas-751/the-hundred-line-esp/issues) (sin spoilers). La versión basada en el japonés se retiró el 2026-11-03.
> Es un proyecto de fans, sin relación con los creadores ni los editores del juego. **No incluye el juego ni sus archivos**: necesitas tu propia copia en Steam.

## Avance

<!-- progress: lo actualiza `python3 -I scripts/thl.py progress --readme` en cada commit -->
| Fase | Sección | Traducidas | Total | % |
|---|---|---:|---:|---:|
| 1 | Interfaz | 14.984 | 14.984 | 100,0 % |
| 2 | Primera partida | 18.293 | 18.293 | 100,0 % |
| 3 | Partidas posteriores | 87.918 | 103.496 | 84,9 % |
| 4 | Eventos y charlas | 3.817 | 3.817 | 100,0 % |
| | **Total** | **125.012** | **140.590** | **88,9 %** |
<!-- /progress -->

## Instalar

La traducción reemplaza el idioma **inglés** del juego. Se arma con *tus* archivos del juego, y se puede quitar cuando quieras. También ajusta las fuentes del menú para que las letras con tilde, la ñ y los signos ¿ ¡ tengan el mismo ancho que las demás.
Funciona en **Windows** y en **Linux / Steam Deck**. No hace falta instalar nada más ni clonar el repositorio.

1. Descarga el paquete de tu sistema desde la [última release](https://github.com/bmvargas-751/the-hundred-line-esp/releases/latest):
   - Windows: `THL-ESP-…-windows.zip`
   - Linux y Steam Deck: `THL-ESP-…-linux.tar.gz`
2. Descomprímelo **dentro de la carpeta del juego**, junto a la carpeta `gamedata`. Te queda una carpeta `THL-ESP`.
   Para abrir la carpeta del juego: en Steam, clic derecho en el juego > *Administrar* > *Explorar archivos locales*.
3. Ejecuta el instalador de esa carpeta:
   - Windows: doble clic en **`install.bat`**.
   - Linux: **`install.sh`**. En Steam Deck, en modo escritorio: clic derecho en `install.sh` > *Ejecutar en terminal* (o `./install.sh` desde una terminal).
4. Abre el juego, ve a **Opciones** y cambia el idioma a **English**. El texto aparece en español.

El instalador tarda unos segundos. Guarda antes los archivos originales en `THL-ESP/backup/`.

### Desinstalar

Ejecuta **`uninstall.bat`** (Windows) o **`uninstall.sh`** (Linux). Restaura los archivos originales del juego.
Si algo quedó mal, en Steam: *Propiedades > Archivos instalados > Verificar integridad de los archivos del juego*.
No borres la carpeta `THL-ESP` antes de desinstalar: ahí está el respaldo.

### Si el juego se actualiza

Steam reemplaza los archivos y la traducción se pierde. Vuelve a ejecutar el instalador. Si el juego recibió una actualización nueva, el instalador te avisa; en ese caso conviene bajar la última release.

### Problemas frecuentes

- **"No encuentro el juego"**: la carpeta `THL-ESP` tiene que estar dentro de la carpeta del juego, junto a `gamedata`. Si no, el instalador busca el juego en Steam; si tampoco lo halla, indica la ruta: `install.bat` no la pide, pero `python\python.exe scripts\installer.py install --game "RUTA"` sí (en Linux: `python3 scripts/installer.py install --game "RUTA"`).
- **Se ve en inglés**: comprueba que el idioma del juego sea English y que el instalador terminó con "Listo".
- **Windows muestra un aviso de seguridad** al ejecutar el `.bat`: es normal con archivos descargados; el contenido es de código abierto en este repositorio.
- **Un texto raro, cortado o con un error**: dinos en qué día o pantalla pasó, sin spoilers, en [Issues](https://github.com/bmvargas-751/the-hundred-line-esp/issues).

### Instalar desde el código

Para colaborar o instalar desde una copia del repositorio (WSL o Linux), mira [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentación

- [Guía para colaborar](CONTRIBUTING.md), con la estructura del proyecto y las herramientas
- [Estilo](STYLE.md) y [glosario](GLOSSARY.md); el [glosario del doblaje inglés](GLOSSARY-EN.md) suma lo que cambia en esa versión

## Créditos y aviso

Herramienta de extracción y empaquetado: [MVGLTools](https://github.com/SydMontague/MVGLTools) de SydMontague.
*The Hundred Line -Last Defense Academy-* pertenece a sus autores y editores. Este repositorio solo contiene nuestra traducción y las herramientas para aplicarla. Licencias en [LICENSE.md](LICENSE.md): MIT para los scripts y CC BY-NC-SA 4.0 para la traducción.
