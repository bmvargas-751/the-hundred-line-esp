# Plan

## Decisiones

- **Variante:** español neutro (*tú*/*ustedes*, sin regionalismos de ningún país), con frases enteras naturales.
- **Original:** el inglés oficial de Steam, para que los subtítulos coincidan con el doblaje inglés (desde 2026-10-27; la versión basada en el japonés se retiró el 2026-11-03).
- **Otra versión de apoyo:** el japonés, solo para género, sujeto omitido y trato (E-1). Va en `support` de `loc.json` (campo `ja`).
- **Terminología:** glosario propio ([GLOSSARY.md](GLOSSARY.md)); nombres como en el doblaje inglés.
- **Pruebas:** en el juego de Steam, con el instalador (Windows y Linux / Steam Deck).
- **Sin spoilers:** los documentos, los commits y el chat nombran días, rutas o archivos, nunca hechos de la historia.
- **Contenido del repo:** solo nuestra traducción, por ID de línea, y las herramientas; el inglés y el japonés los extrae cada uno de su juego.

## Fases

THL es anterior al kit: lo adoptó la skill `loc-adopt` (2026-11-23). Las fases de antes (por sección del juego) están en DECISIONS.md.

### Fase 0. Decisiones

- [x] Variante, original, versión de apoyo y contenido del repo.
- [x] Base de STYLE.md y GLOSSARY.md.
- [x] Repo en GitHub con las reglas comunes.

### Fase 1. Prueba técnica

- [x] Extraer los archivos del juego: `scripts/extract.sh` (inglés y japonés, en `build/`).
- [x] Adaptador: `scripts/kit_adapter.py export` (formato común) y los hooks sobre los TSV de `translation/`.
- [x] Ida y vuelta idéntica: `build.sh` y el instalador, sin diferencias; los hooks del kit leen y escriben sin cambios.
- [x] Caracteres: tildes, ñ y ¿¡ en las fuentes del menú, con el mismo ancho (`scripts/thlfuente.py`).
- [x] Límites: cajas de 4 renglones y ancho de renglón (`scripts/thlchecks.py`).

### Fase 2. Inventario y costo

- [x] Volumen por sección: 140.590 líneas con texto.

### Fase 3. Glosario y fichas

- [x] Glosario y guía de estilo, con las formas de dirigirse.

### Fase 4. Set de oro

> Todavía no: hace falta solo para corregir con `loc-batch` (skill `loc-start`, punto 5).

### Fase 5. Piloto

- [x] Traducción por bloques con las skills propias de THL (antes del kit).

### Fase 6. Traducción

- [x] Interfaz
- [x] Historia
- [x] Secundarias
- [x] Lectura de calidad completa (siete pasadas, [REVISION.md](REVISION.md)).

### Fase 7. Prueba en el juego

- [ ] Verificar que el juego arranca con el parche y que tildes, ñ y ¿¡ se ven bien.
- [ ] Jugar y completar las pruebas de TESTS.md (local), incluidos los renglones más anchos que el inglés (avisos `ancho` de la interfaz).

### Fase 8. Entrega

- [x] Instalador para Windows y Linux / Steam Deck, con respaldo y desinstalación.
- [x] `project.json` completo.
- [x] CHANGELOG.md y versiones 0.x de prueba (hasta la 0.9.0).
- [ ] Versión 1.0, después de la fase 7.
