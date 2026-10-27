# The Hundred Line -Last Defense Academy- — Traducción al español

Traducción **no oficial** al español neutro del juego *The Hundred Line -Last Defense Academy-*, hecha desde el japonés original, con el inglés oficial como apoyo y un glosario propio.

> **Versión 0.1, en revisión.** Todo el texto está traducido, pero falta la revisión final y probarlo entero en el juego. Pueden quedar errores: [avísanos](https://github.com/bmvargas-751/the-hundred-line-esp/issues).
> Es un proyecto de fans, sin relación con los creadores ni los editores del juego. **No incluye el juego ni sus archivos**: necesitas tu propia copia en Steam.

## Avance

<!-- progress: lo actualiza `python3 -I scripts/thl.py progress --readme` en cada commit -->
**Etapa actual:** Fase 5 (Prueba y entrega), verificar que el juego arranca con el parche y que tildes, ñ y ¿¡ se ven bien (se puede probar en cualquier momento).

| Fase | Sección | Traducidas | Total | % |
|---|---|---:|---:|---:|
| 1 | Interfaz | 14.917 | 14.917 | 100,0 % |
| 2 | Primera partida | 18.293 | 18.293 | 100,0 % |
| 3 | Partidas posteriores | 103.496 | 103.496 | 100,0 % |
| 4 | Eventos y charlas | 3.817 | 3.817 | 100,0 % |
| | **Total** | **140.523** | **140.523** | **100,0 %** |
<!-- /progress -->

## Instalar

La traducción reemplaza el idioma **inglés** del juego. Se arma con *tus* archivos del juego, y se puede quitar cuando quieras.
Funciona en **Windows** y en **Linux / Steam Deck**. No hace falta instalar nada más ni clonar el repositorio.

1. Descarga el paquete de tu sistema desde la [última release](https://github.com/bmvargas-751/the-hundred-line-esp/releases/latest):
   - Windows: `THL-ESP-…-windows.zip`
   - Linux y Steam Deck: `THL-ESP-…-linux.tar.gz`
2. Descomprímelo **dentro de la carpeta del juego**, junto a la carpeta `gamedata`. Te queda una carpeta `THL-ESP`.
   Para abrir la carpeta del juego: en Steam, clic derecho en el juego > *Administrar* > *Explorar archivos locales*.
3. Ejecuta el instalador de esa carpeta:
   - Windows: doble clic en **`INSTALAR.bat`**.
   - Linux: **`instalar.sh`**. En Steam Deck, en modo escritorio: clic derecho en `instalar.sh` > *Ejecutar en terminal* (o `./instalar.sh` desde una terminal).
4. Abre el juego, ve a **Opciones** y cambia el idioma a **English**. El texto aparece en español.

El instalador tarda unos segundos. Guarda antes los archivos originales en `THL-ESP/backup/`.

### Desinstalar

Ejecuta **`DESINSTALAR.bat`** (Windows) o **`desinstalar.sh`** (Linux). Restaura los archivos originales del juego.
Si algo quedó mal, en Steam: *Propiedades > Archivos instalados > Verificar integridad de los archivos del juego*.
No borres la carpeta `THL-ESP` antes de desinstalar: ahí está el respaldo.

### Si el juego se actualiza

Steam reemplaza los archivos y la traducción se pierde. Vuelve a ejecutar el instalador. Si el juego recibió una actualización nueva, el instalador te avisa; en ese caso conviene bajar la última release.

### Problemas frecuentes

- **"No encuentro el juego"**: la carpeta `THL-ESP` tiene que estar dentro de la carpeta del juego, junto a `gamedata`. Si no, el instalador busca el juego en Steam; si tampoco lo halla, indica la ruta: `INSTALAR.bat` no la pide, pero `python\python.exe scripts\installer.py install --game "RUTA"` sí (en Linux: `python3 scripts/installer.py install --game "RUTA"`).
- **Se ve en inglés**: comprueba que el idioma del juego sea English y que el instalador terminó con "Listo".
- **Windows muestra un aviso de seguridad** al ejecutar el `.bat`: es normal con archivos descargados; el contenido es de código abierto en este repositorio.
- **Un texto raro, cortado o con un error**: dinos en qué día o pantalla pasó, sin spoilers, en [Issues](https://github.com/bmvargas-751/the-hundred-line-esp/issues).

### Instalar desde el código

Para colaborar o instalar desde una copia del repositorio (WSL o Linux), mira [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentación

- [Guía para colaborar](CONTRIBUTING.md), con la estructura del proyecto y las herramientas
- [Estilo](STYLE.md) y [glosario](GLOSSARY.md)

## Créditos y aviso

Herramienta de extracción y empaquetado: [MVGLTools](https://github.com/SydMontague/MVGLTools) de SydMontague.
*The Hundred Line -Last Defense Academy-* pertenece a sus autores y editores. Este repositorio solo contiene nuestra traducción y las herramientas para aplicarla. Licencias en [LICENSE.md](LICENSE.md): MIT para los scripts y CC BY-NC-SA 4.0 para la traducción.
