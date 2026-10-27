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

La traducción reemplaza el idioma **inglés** del juego. El parche se arma a partir de *tus* archivos del juego, y se puede quitar cuando quieras.

### Requisitos

- El juego instalado desde Steam.
- Windows con [WSL](https://learn.microsoft.com/windows/wsl/install) (Ubuntu), o Linux.
- `python3`, `curl` y `git` dentro de WSL/Linux (`sudo apt install python3 curl git`).
- Unos 200 MB libres.

### Pasos

1. Descarga el repositorio, en una terminal de WSL/Linux:
   ```
   git clone https://github.com/bmvargas-751/the-hundred-line-esp.git
   cd the-hundred-line-esp
   ```
2. Si el juego **no** está en `C:\Steam\steamapps\common\The Hundred Line -Last Defense Academy-`, indica dónde está (ruta de WSL, por ejemplo en el disco D:):
   ```
   export THL_GAME_DIR="/mnt/d/SteamLibrary/steamapps/common/The Hundred Line -Last Defense Academy-"
   ```
3. Extrae los textos de tu juego y arma el parche (la primera vez descarga [MVGLTools](https://github.com/SydMontague/MVGLTools), unos segundos):
   ```
   scripts/extract.sh
   scripts/build.sh
   ```
4. Instálalo. Antes guarda los archivos originales en `backup/`:
   ```
   scripts/install.sh
   ```
5. Abre el juego, ve a **Opciones** y cambia el idioma a **English**. El texto aparece en español.

### Desinstalar

```
scripts/uninstall.sh
```

Restaura los archivos originales desde `backup/`. Si algo quedó mal, en Steam: *Propiedades > Archivos instalados > Verificar integridad de los archivos del juego*.

### Si el juego se actualiza

Steam reemplaza los archivos y el parche se pierde. Actualiza este repositorio (`git pull`) y repite los pasos 3 y 4.

### Problemas frecuentes

- **"No encuentro el juego"**: revisa `THL_GAME_DIR` (paso 2). La ruta lleva comillas por los espacios.
- **Se ve en inglés**: comprueba que el idioma del juego sea English y que `scripts/install.sh` terminó sin errores.
- **Un texto raro, cortado o con un error**: dinos en qué día o pantalla pasó, sin spoilers, en [Issues](https://github.com/bmvargas-751/the-hundred-line-esp/issues).

## Documentación

- [Guía para colaborar](CONTRIBUTING.md), con la estructura del proyecto y las herramientas
- [Estilo](STYLE.md) y [glosario](GLOSSARY.md)

## Créditos y aviso

Herramienta de extracción y empaquetado: [MVGLTools](https://github.com/SydMontague/MVGLTools) de SydMontague.
*The Hundred Line -Last Defense Academy-* pertenece a sus autores y editores. Este repositorio solo contiene nuestra traducción y las herramientas para aplicarla. Licencias en [LICENSE.md](LICENSE.md): MIT para los scripts y CC BY-NC-SA 4.0 para la traducción.
