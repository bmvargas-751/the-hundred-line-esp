# Corrección de calidad — doblaje inglés

Esta página sigue la **corrección** de la traducción, aparte del [avance de la traducción](README.md#avance). La traducción está completa (salvo la ruta `s15`), pero al jugarla las partidas posteriores quedaron con español poco natural. Aquí se lleva cuenta de qué se ha revisado y qué falta.

> Sin spoilers: solo se nombran secciones y rutas por su código, nunca el contenido.

## Qué se corrige

Cada línea se compara con el inglés oficial (el japonés solo ayuda con género, sujeto omitido y trato) y se revisa en siete pasadas:

1. **Fidelidad**: omisiones, añadidos, malas interpretaciones.
2. **Naturalidad**: calcos del inglés, construcciones artificiales, pronombres colgantes.
3. **Localización**: modismos, bromas, insultos (*idiot* → *idiota*, no *tonto*).
4. **Gramática**: ortografía, puntuación, *y* → *e* ante /i/ (*e Ima*, *e Hiruko*), *o* → *u* ante /o/.
5. **Género y concordancia**, como pasada independiente.
6. **Consistencia**: glosario, nombres, habilidades, tratamientos.
7. **Lectura final**: que suene a juego escrito en español.

Se cambia solo con un motivo real; lo que ya está bien se deja. El método completo está en `.claude/skills/traducir-bloque/REVISION-EN.md` y las decisiones de trato en [GLOSSARY-EN.md](GLOSSARY-EN.md).

### Decisiones de trato

- **Ima** habla de *usted* (señor/señorita) con todos, salvo con su hermana Kako, a quien trata de *tú*.
- **Kako** habla casual (*tú*, por el nombre) con todos.
- **Kyoshika**: *usted* y *don/doña*. **Ginzaki**: *usted*. **Kurara**: altiva, con insultos. **Darumi** dice *la Ama Hiruko*.
- El resto de los estudiantes se tutean.

## Estado por sección

La **lectura completa** cuenta las líneas leídas una por una con las siete pasadas. El resto pasó por **barridos de patrones** (errores que se repiten) y **muestras**, que atrapan los errores frecuentes pero no los de una sola línea.

| Sección | Líneas | Lectura completa | Cobertura del resto | Líneas corregidas |
|---|---:|---:|---|---:|
| Primera partida (`r00`) | 18.294 | 0% | patrones y muestras | 23 |
| Ruta `s00` | 14.835 | 0% | patrones y muestras | 9 |
| Rutas `s01` a `s03` | 2.226 | 100% | — | 47 |
| Rutas `s04` a `s11` | 30.571 | ~2% | patrones y muestras | 188 |
| Rutas `s12` a `s14` | 40.287 | ~0% | patrones y muestras (trato de Ima y Kyoshika) | 97 |
| Ruta `s15` | 15.579 | — | en pausa, sin revisar | 0 |
| Eventos y charlas | 3.848 | ~47% | patrones | 18 |
| **Total** | **125.640** | **~5%** | | **382** |

<!-- Cifras a 2026-11-03. "Líneas corregidas" = filas cambiadas frente a main. -->

### Barridos globales ya hechos

- *y* → *e* ante Ima, Hiruko y palabras con /i/ (59 líneas).
- Insultos con *tonto* donde el inglés dice *idiot*, *moron* o *dullard*.
- Puntuación mal abierta o cerrada (`¡¿…?`, `¡Pero ¿…?`).
- Calcos frecuentes: *realmente*, *hace sentido*, *Mi nombre es*, *Lo siento por todo*.
- Porcentajes con espacio (*50 %* → *50%*).
- Trato de Ima, Kako y Kyoshika según lo anterior.

## Lo que falta

1. **Lectura completa** de `r00` y `s00` (unas 33.000 líneas), por tandas de días.
2. Lectura completa de `s13` y `s14`, las más largas.
3. Resolver las dudas que dejaron los barridos:
   - Ima con *tú* hacia personajes que no son Kako, donde aún no se confirmó el destinatario (unas 15 líneas en `s08`, `s09` y `s11`).
   - Ginzaki con *tú* en `s09_a` (el glosario dice *usted*).
   - *Sr.* / *señor* y *Srta.* / *señorita*: se usan ambos; falta unificar.
   - *Por el amor al asesinato* frente a *Por el amor de la muerte* (muletilla de Yugamu).
   - *Kyohoho* y *Kyohohoho* conviven (risa de Darumi).
4. Retomar `s15` cuando se reanude.
5. Reinstalar el build nuevo y jugar para confirmar (nada se instala en el juego sin pedirlo).

## Cómo reportar un error

Abre un [issue](https://github.com/bmvargas-751/the-hundred-line-esp/issues) con la captura y el Día o la ruta, **sin spoilers**. Cada captura sirve para corregir la línea y buscar el mismo calco en todo el juego.
