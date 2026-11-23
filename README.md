# The Hundred Line -Last Defense Academy- en español

Traducción fan al español neutro de *The Hundred Line -Last Defense Academy-*, basada en la versión oficial en inglés, para Steam (Windows, Linux y Steam Deck), para que los subtítulos coincidan con el doblaje inglés. El japonés solo se usa para resolver género, sujeto omitido y trato.

> Proyecto de fans, sin relación con Too Kyo Games ni con Aniplex. **No incluye el juego**: el instalador arma la traducción a partir de tu propia copia.

## Instalar

<!-- loc:install -->
Necesitas tu propia copia del juego en Steam. No hace falta instalar nada más ni clonar el repositorio.

**Windows:**

1. Descarga **THL-ESP-…-windows.zip** de la [última versión](https://github.com/nox-traducciones/the-hundred-line/releases/latest).
2. Descomprímelo dentro de la carpeta del juego, junto a la carpeta `gamedata`. Para abrirla: en Steam, clic derecho en el juego > **Administrar** > **Explorar archivos locales**.
3. En la carpeta **THL-ESP**, haz doble clic en **install.bat**.
4. Abre el juego, ve a **Opciones** y cambia el idioma a **English**: el texto aparece en español.

<details>
<summary>Linux y Steam Deck</summary>

1. Descarga **THL-ESP-…-linux.tar.gz** de la [última versión](https://github.com/nox-traducciones/the-hundred-line/releases/latest) y descomprímelo dentro de la carpeta del juego, junto a `gamedata`.
2. En la carpeta **THL-ESP**, ejecuta **install.sh**. En Steam Deck, en modo escritorio: clic derecho en install.sh > **Ejecutar en terminal**.
3. Abre el juego, ve a **Opciones** y cambia el idioma a **English**: el texto aparece en español.

</details>

<details>
<summary>Desinstalar, o si el juego se actualiza</summary>

1. El instalador guarda los archivos originales en `THL-ESP/backup/`: no borres esa carpeta antes de desinstalar.
2. Para desinstalar, ejecuta **uninstall.bat** (Windows) o **uninstall.sh** (Linux). Si algo quedó mal, en Steam: **Propiedades** > **Archivos instalados** > **Verificar integridad de los archivos del juego**.
3. Si Steam actualiza el juego, la traducción se pierde: vuelve a ejecutar el instalador. Si el juego recibió una actualización nueva, el instalador te avisa; en ese caso conviene bajar la última versión.

</details>
<!-- /loc:install -->

## Avance

<!-- loc:progress -->
| Sección | Líneas | Traducidas | Avance |
|---|---:|---:|---:|
| Interfaz | 14.984 | 14.984 | 100,0 % |
| Historia | 121.789 | 121.789 | 100,0 % |
| Secundarias | 3.817 | 3.817 | 100,0 % |
| **Total** | **140.590** | **140.590** | **100,0 %** |
<!-- /loc:progress -->

## Documentación

<!-- loc:docs -->
Localización: [Glosario](GLOSSARY.md) · [Estilo](STYLE.md) · [Decisiones](DECISIONS.md)\
Desarrollo: [Plan](PLAN.md)
<!-- /loc:docs -->

Para colaborar o instalar desde el código (WSL o Linux): [CONTRIBUTING.md](CONTRIBUTING.md), con la estructura del proyecto y los scripts.

## Corrección de calidad

La traducción estaba completa, pero al jugarla tenía español poco natural. Se corrigió, sección por sección, con el método de siete pasadas de [REVISION.md](REVISION.md) (fidelidad, naturalidad, localización, gramática, género, consistencia y lectura final). Es aparte del avance:

<!-- correccion -->
| Sección | Líneas | Lectura completa |
|---|---:|---:|
| Primera partida | 18.294 | 100 % |
| Rutas `s00` a `s03` | 17.061 | 100 % |
| Rutas `s04` a `s11` | 30.571 | 100 % |
| Rutas `s12` a `s14` | 40.287 | 100 % |
| Ruta `s15` | 15.579 | 100 % |
| Eventos y charlas | 3.848 | 100 % |
| Cajas de texto (4 renglones) | 125.640 | 100 % |
| **Total** | **125.640** | **100 %** |
<!-- /correccion -->

"Lectura completa" son las líneas leídas una por una; el resto pasó por barridos de errores repetidos. Detalle, decisiones de trato y lo que falta: [REVISION.md](REVISION.md).

## Problemas frecuentes

- **"No encuentro el juego"**: la carpeta `THL-ESP` tiene que estar dentro de la carpeta del juego, junto a `gamedata`. Si no, el instalador busca el juego en Steam; si tampoco lo halla, indica la ruta: `install.bat` no la pide, pero `python\python.exe scripts\installer.py install --game "RUTA"` sí (en Linux: `python3 scripts/installer.py install --game "RUTA"`).
- **Se ve en inglés**: comprueba que el idioma del juego sea English y que el instalador terminó con "Listo".
- **Windows muestra un aviso de seguridad** al ejecutar el `.bat`: es normal con archivos descargados; el contenido es de código abierto en este repositorio.
- **Un texto raro, cortado o con un error**: dinos en qué día o pantalla pasó, sin spoilers, en [Issues](https://github.com/nox-traducciones/the-hundred-line/issues).

## Créditos y aviso

Herramienta de extracción y empaquetado: [MVGLTools](https://github.com/SydMontague/MVGLTools) de SydMontague.
*The Hundred Line -Last Defense Academy-* pertenece a sus autores y editores. Este repositorio solo contiene nuestra traducción y las herramientas para aplicarla. Licencias en [LICENSE.md](LICENSE.md): MIT para los scripts y CC BY-NC-SA 4.0 para la traducción.
