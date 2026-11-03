# Guía de estilo

Reglas para toda traducción. Los términos fijos están en [GLOSSARY.md](GLOSSARY.md).

## Principio general

La base es el **inglés oficial**: cada línea se traduce frase por frase, con el mismo sentido y un largo parecido al de la voz, para que el subtítulo coincida con el doblaje inglés. El japonés original (`thl.py export` lo muestra como `JP:`) solo ayuda a resolver género, sujeto omitido y trato (tú/usted).
Se localiza al español: nada de honoríficos japoneses (-san, -kun, -sama, -sensei...) ni giros calcados del inglés.
Los nombres siguen al inglés (ver [GLOSSARY.md](GLOSSARY.md)). Lo que el juego ya escribe en inglés se deja tal cual (*SAFETY*, *Nice DEATH*).
Se traduce **frase por frase**: si se cambia una palabra, se revisa que el resto de la oración siga concordando y suene natural.

## Español neutro

Español natural, como lo diría una persona en una conversación equivalente, y comprensible en toda América: sin iberismos ni regionalismos marcados de ningún país.

### Ustedes

El plural es siempre *ustedes*, nunca *vosotros*: verbos en 3.ª persona del plural, pronombres *los/las*, *les* y *se* (*se lo dije*), posesivo *su* o *de ustedes* si *su* queda ambiguo.
Imperativo con el subjuntivo (*descansen*, *vayan*, *esperen*). Si la frase queda ambigua con *ellos*, reformularla.

### Vocabulario

Elegir según el contexto y el registro del personaje.

| Evitar (España) | Usar |
|---|---|
| vale | está bien, de acuerdo, bueno, okey (según el tono) |
| echar de menos | extrañar |
| menudo (*menudo punto ciego*) | qué, vaya |
| venga (ánimo) | vamos, anda |
| tío/tía (= amigo) | amigo, viejo (casual) u omitir; *tío* (pariente) se mantiene |
| guay, mola | genial, increíble, me encanta |
| coger | tomar, agarrar, atrapar |
| pillar | atrapar, entender, sorprender |
| ordenador | computadora |
| móvil | teléfono |
| pasta (dinero) | dinero |
| majo/maja | simpático, agradable |
| gilipollas | idiota, imbécil |
| joder | maldición, mierda, rayos (según la intensidad del original) |
| enfadarse | enojarse |
| pulsar (un botón) | presionar |
| mando (de consola) | control |
| ratón (de la computadora) | mouse |
| vídeo | video |
| castellano (nombre del idioma) | español |
| bombona | cartucho, tanque, garrafa (según el objeto) |
| destripe (spoiler) | spoiler |
| gafas | lentes, anteojos |
| bañador | traje de baño |
| nevera | refrigerador |
| mono/mona (= bonito) | lindo, tierno |
| fardar | presumir |
| motero | motociclista |
| tragaperras | tragamonedas |
| cristal (el material) | vidrio |
| aparcamiento, aparcar | estacionamiento, estacionar |
| jersey | suéter |
| auriculares | audífonos |
| seta | hongo |
| coche | auto |
| cubo de basura | bote de basura |
| pendientes (joya) | aretes |
| marcapáginas | separador |
| ambientador | aromatizante |
| taquilla (armario) | casillero |
| diana (de dardos) | tablero de dardos |
| pista (de tenis) | cancha |
| chaval | chico |
| judía (legumbre) | frijol |
| megafonía | altavoz |

Evitar también regionalismos latinoamericanos marcados (*chido*, *bacán*, *boludo*, *wey*, *pana*).

## Tratamiento

- **Nombres:** como el inglés (nombre de pila casi siempre; ver [GLOSSARY.md](GLOSSARY.md)). Los honoríficos se localizan según la tabla de [GLOSSARY.md](GLOSSARY.md#cómo-se-llaman-los-personajes).
- **Tú** por defecto entre estudiantes.
- **Usted** solo si el personaje habla formalmente en japonés. Hoy lo usan sobre todo Ima (っす, con *Sr./Srta.*; solo a su hermana Kako le dice *tú*), Kyoshika (でござる, con *Sir/Lady*) y Ginzaki (です/ます con todos); NIGOU y Eva, a veces (verificar contra el japonés caso por caso). Kako habla casual con todos.
  Mantener el mismo tratamiento entre dos personajes durante todo el juego.
- **Ustedes** para el plural, siempre.
- **Cursos:** 高校 = *preparatoria* (*último año de preparatoria*, 高校３年), 中学 = *secundaria* (*tercero de secundaria*).
- **Tablero de exploración:** Takumi narra en primera persona, como el japonés (*Encontré una colmena*); los avisos del sistema van como en el resto de la interfaz (*Obtuviste: X.*) y las opciones, en infinitivo y en un solo renglón (*Estirar la mano.*).

## Tono y voz de los personajes

Mantener los tics de cada personaje según el inglés (cortes, tartamudeos *"N-No"*, jerga, muletillas, groserías).
No suavizar ni intensificar las groserías: igualar la intensidad del original.
**Frases delicadas** (juegos de palabras, muletillas, referencias, acertijos y minijuegos de palabras): se traducen desde el inglés, para que el subtítulo no desentone con el doblaje inglés; el japonés queda como apoyo. No se agregan datos que el inglés no tiene, y los nombres siguen el glosario.
Risas fijas, como el inglés: SIREI *Juafafafaj* (ちゅふふ), NIGOU *Juofofofoj* (la misma ちゅふふ; el inglés le dio otra), Darumi *Kyohohoho* (きょっきょっきょ), Kurara *Kijijijí* (キシシシ), Yugamu *Ufufu* (うふふ). Darumi habla de sí misma en primera persona, como el inglés.

## Formato

- Signos de apertura obligatorios: `¿` y `¡`. Si la línea continúa una frase de la línea anterior (empieza en minúscula), el signo de apertura va en la anterior.
- Combinados: `¡¿...?!` cuando el inglés usa `?!`. Varios signos de cierre llevan la misma cantidad de apertura: `¡¡FUERA!!`.
- Comillas: siempre rectas `"..."` (no `«»` ni `“”`). Donde el inglés o el japonés (「」, 『』) las usan para una cita; las que agrega solo uno de los dos, solo si aclaran que alguien cita o dice algo.
  El punto final va **fuera** de las comillas (`"...lo que yo diga".`); `?`, `!` y `...` van dentro si son de lo citado.
- Puntos suspensivos: tres puntos `...` (como el original), sin espacio antes.
- Tartamudeo: `P-Por favor`, con mayúscula repetida si la palabra la lleva.
- Gritos en MAYÚSCULAS como en el inglés.
- **Códigos de control intactos**: `{fc(57e4f1)...}`, `{ft1}`, `%s`, etc. Ni traducir ni mover lo que está dentro de las llaves salvo el texto visible.
- Saltos de línea: en los mensajes de historia no se agregan (el motor parte el texto); en la interfaz, respetar los del original. La caja admite 3 renglones de ~62 caracteres (≈175 visibles): si el español es más largo, se acorta (lo avisan los chequeos `caja`, `largo` y `ancho`).

### Estudiantes de la Penúltima Academia

- **NIGOU:** habla casual como SIREI (*tú*, *Takumi*); le dice *Su Excelencia SIREI* a SIREI. Regla general (decisión del usuario, 2026-11-03): tú o usted **según con quién habla**; si trata de usted a alguien es porque le tiene más respeto.
- **Kyoshika:** *usted* con todos y *Sir/Lady* + nombre (*Lady Kurara*, *Sir Takumi*; hombres *Sir*, mujeres *Lady*); a veces habla de sí misma por el nombre. Mezcla referencias de manga y ninjas con su habla de época. Sin la muletilla なんともにんとも ni el にんにん, como el inglés, salvo el grito *¡Nin, nin, niiin!* del Día 28, que el inglés mantiene.
- **Kurara:** *tú*, insultos constantes (*plebeyo*, *pobretón*, *Inclina la cabeza, idiota*).
- **Yugamu:** *tú*, *Takumi*; cambia *hacer* por *matar* en sus frases (殺る). Sus muletillas siguen al inglés de cada línea: 殺れ殺れ suele ser *Por amor al asesinato...* (*For the love of murder*); 殺ぁ, un saludo común (*Hola, Sumino*); 殺っかい y 殺っぱり, lo que diga el inglés (*de muerte*, *Como era de esperar*).
- **Nozomi:** *tú*, *Takumi*; a Moko le dice *Moko*.
- **Eva:** *usted* con Takumi mientras es prisionera y sigue la etiqueta; después, trato directo (*tú*) cuando se quita la máscara de cortesía. A Kirifuji (*Nozomi*) la llama por el nombre de pila, como a una hija.
- **Kamyuhn:** niña altiva que habla como una sacerdotisa de época (*necio*, *insolente*, *¡cómo osan!*); *yo*, sin vosotros.

