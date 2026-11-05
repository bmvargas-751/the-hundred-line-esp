# Corrección de calidad — doblaje inglés

Esta página sigue la **corrección** de la traducción, aparte del [avance de la traducción](README.md#avance). La traducción está completa, pero al jugarla las partidas posteriores quedaron con español poco natural. Aquí se lleva cuenta de qué se ha revisado y qué falta.

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

Se cambia solo con un motivo real; lo que ya está bien se deja. El método completo está en `.claude/skills/traducir-bloque/METODO-REVISION.md` y las decisiones de trato en [GLOSSARY.md](GLOSSARY.md).

### Decisiones de trato

- **Ima** habla de *usted* (señor/señorita) con todos, salvo con su hermana Kako, a quien trata de *tú*.
- **Kako** habla casual (*tú*, por el nombre) con todos.
- **Kyoshika**: *usted* y *don/doña*. **Ginzaki**: *usted*. **Kurara**: altiva, con insultos. **Darumi** dice *la Ama Hiruko*.
- El resto de los estudiantes se tutean.

## Estado por sección

La **lectura completa** cuenta las líneas leídas una por una con las siete pasadas. El resto pasó por **barridos de patrones** (errores que se repiten) y **muestras**, que atrapan los errores frecuentes pero no los de una sola línea.

| Sección | Líneas | Lectura completa | Cobertura del resto |
|---|---:|---:|---|
| Primera partida (`r00`) | 18.294 | 100% | — |
| Ruta `s00` | 14.835 | 100% | — |
| Rutas `s01` a `s03` | 2.226 | 100% | — |
| Rutas `s04` a `s11` | 30.571 | 100% | — |
| Rutas `s12` a `s14` | 40.287 | 100% | — |
| Ruta `s15` | 15.579 | 100% (retraducida desde el inglés y corregida) | — |
| Eventos y charlas | 3.848 | ~77% (2.966 líneas del volcado) | patrones |
| **Total** | **125.640** | **~99%** | |


### Barridos globales ya hechos

- *y* → *e* ante Ima, Hiruko y palabras con /i/ (59 líneas).
- Insultos con *tonto* donde el inglés dice *idiot*, *moron* o *dullard*.
- Puntuación mal abierta o cerrada (`¡¿…?`, `¡Pero ¿…?`).
- Calcos frecuentes: *realmente*, *hace sentido*, *Mi nombre es*, *Lo siento por todo*.
- Porcentajes con espacio (*50 %* → *50%*).
- **Cajas de texto**: la caja admite 3 renglones de ~62 caracteres (el inglés más largo mide 178 caracteres visibles). 20 líneas pasaban de 3 renglones y la última palabra quedaba fuera de la caja; se acortaron. El chequeo `caja` de `thl.py check` avisa de cualquier otra.
- «eh...?» sin «¿» (11 líneas).
- Trato de Ima, Kako y Kyoshika según lo anterior.
- Glosario y léxico regional en todo el juego (`s00` a `s15`): TL, *okey*, *recién*, *qué onda*, *nomás*, anuncios de SIREI con el día en ordinal y *Sr. Sumino* en boca de Ima.
- Lugares y términos comunes del juego en minúscula a media frase (*sala de guerra*, *cafetería*, *llamas eternas*, *muerte del mundo*…, unas 2.800 líneas) y *su excelencia SIREI* / *honorable SIREI* a media frase.
- *Sin embargo* al final de frase (calco de *though*) por *eso sí* (55 líneas); *esa hora* (*That time again*) por *ya se hizo tarde* / *ya es hora de dormir*; *un acto* por *una actuación*; *mandadero* por *chico de los mandados*.

## Lo que falta

1. **Lectura completa** de lo que falta de *Eventos y charlas* (unas 880 líneas). `r00` y `s00` a `s15` ya están leídas completas.
3. Resolver las dudas que dejaron los barridos:
   - Ima con *tú* hacia personajes que no son Kako, donde aún no se confirmó el destinatario (unas 15 líneas en `s08`, `s09` y `s11`).
   - Ginzaki con *tú* en `s09_a` (el glosario dice *usted*).
   - *Sr.* / *señor* y *Srta.* / *señorita*: se usan ambos; falta unificar.
   - *Por el amor al asesinato* frente a *Por el amor de la muerte* (muletilla de Yugamu).
   - *Kyohoho* y *Kyohohoho* conviven (risa de Darumi).
4b. **Tarea aparte (pendiente):** barrido de puntuación. Unas 300 líneas usan signos anidados del tipo `¡Nozomi, ¿estás bien?!`; `STYLE.md` pide `¡¿...?!` cuando el inglés usa `?!`. Mecánico, pero toca muchas líneas: hacerlo en un PR propio.
5. Reinstalar el build nuevo y jugar para confirmar (nada se instala en el juego sin pedirlo).

## Cómo reportar un error

Abre un [issue](https://github.com/bmvargas-751/the-hundred-line-esp/issues) con la captura y el Día o la ruta, **sin spoilers**. Cada captura sirve para corregir la línea y buscar el mismo calco en todo el juego.
