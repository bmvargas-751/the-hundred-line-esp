# Decisiones

Lo que se decidió y cuándo. Las de antes del kit salen del PLAN de entonces (fases por sección del juego).

- **Antes del 2026-10-27** Español neutro, con frases enteras naturales. Solo nuestra traducción en el repo, por ID de línea; el japonés y el inglés no se guardan (cada uno los extrae de su juego). Lo que falta traducir se ve en inglés.
- **Antes del 2026-10-27** `patch_text01` pisa a `app_text01`: si un archivo está en los dos, el juego usa el de `patch`. `build.sh` pone la traducción en los dos.
- **Antes del 2026-10-27** Fases por sección: interfaz (`text/`), primera partida (`r00_`, por días), partidas posteriores (`s00_` a `s15_`, por ruta) y eventos y charlas (`a_chr`, `g_chr`, `k_chr`, `npc_chr`, `gim_` y el resto de `message/`).
- **2026-10-27** Líneas delicadas de eventos y charlas (juegos de palabras, muletillas, referencias, minijuegos de palabras) rehechas desde el inglés para que coincidan con el doblaje.
- **2026-10-27** Versión basada en el inglés oficial, para que el subtítulo coincida con la voz inglesa; el japonés queda solo para género, sujeto omitido y trato. Las habilidades con nombre en inglés o katakana se traducen al español. Nombres como en el doblaje (GLOSSARY.md).
- **2026-10-27** El inglés difiere del japonés en bastante más que nombres (opciones de decisión, frases enteras): las ~140.000 líneas se revisan contra el inglés.
- **2026-11-03** Se retira la versión basada en el japonés: queda una sola traducción, la del inglés.
- **Hasta 2026-11-05** Corrección de calidad con el método de siete pasadas de REVISION.md, con lectura completa de todo el juego.
- **2026-11-23** Adopción del kit (`loc-adopt`): la traducción sigue en los TSV de `translation/`, y el kit la lee y la escribe con `scripts/hooks.py`. Secciones comunes: Interfaz (`text/`), Historia (primera partida y partidas posteriores) y Secundarias (eventos y charlas). PLAN.md pasa al repo; TESTS.md sigue local. Lo extraído del juego sigue en `build/` (lo usan los scripts que arman el parche); solo el original en formato del kit va a `../local/the-hundred-line/`.
- **2026-11-23** El repo pasa a la organización `nox-traducciones/the-hundred-line` (antes `bmvargas-751/the-hundred-line-esp`).
