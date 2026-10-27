# Guía de estilo

Reglas para toda traducción. Los términos fijos están en [GLOSSARY.md](GLOSSARY.md).

## Principio general

La referencia es el **japonés original** (`app_text00`/`patch_text00`; `thl.py export` lo muestra como `JP:`): se traduce el sentido y el tono, no palabra por palabra.
El inglés (columna `string 4` en `message/`) ayuda con las frases japonesas difíciles, pero cuando se aparta del japonés (chistes nuevos, paráfrasis, partes agregadas o quitadas) se sigue el japonés.
**Los nombres son la excepción:** los que inventó o cambió el inglés se toman del inglés (*Revive-O-Matic*, *Penúltima Academia de Defensa*, *Juez*), según el criterio 2 de [GLOSSARY.md](GLOSSARY.md#nombres-propios).
Lo que el japonés ya escribe en inglés se deja en inglés, tal como lo escribe (*SAFETY*, *EXTREME & DESPAIR*, *Nice DEATH*).
Basarse en el japonés no es japonizar: se localiza al español. Nada de honoríficos japoneses (-san, -kun, -sama, -sensei...) ni giros calcados.
Se traduce **frase por frase**: si se cambia una palabra, se revisa que el resto de la oración siga concordando y suene natural.

## Español neutro

Español neutro, sin regionalismos de España ni de ningún país de América.

### Ustedes

El plural es siempre *ustedes*, nunca *vosotros*: verbos en 3.ª persona del plural, pronombres *los/las*, *les* y *se* (*se lo dije*), posesivo *su* o *de ustedes* si *su* queda ambiguo.
Imperativo con el subjuntivo (*descansen*, *vayan*, *esperen*). Si la frase queda ambigua con *ellos*, reformularla.

### Vocabulario

Elegir según el contexto y el registro del personaje.

| Evitar (España) | Usar |
|---|---|
| vale | está bien, de acuerdo, bueno, okey (según el tono) |
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

- **Nombres:** cada personaje llama a los demás como en japonés (apellido o nombre de pila). Los honoríficos se localizan según la tabla de [GLOSSARY.md](GLOSSARY.md#cómo-se-llaman-los-personajes).
- **Tú** por defecto entre estudiantes.
- **Usted** solo si el personaje habla formalmente en japonés. Hoy lo usan sobre todo Ima (っす, con *Sr./Srta.*), Kyoshika (でござる, con *don/doña*) y Ginzaki (です/ます con todos); NIGOU y Eva, a veces (verificar contra el japonés caso por caso).
  Mantener el mismo tratamiento entre dos personajes durante todo el juego.
- **Ustedes** para el plural, siempre.
- **Cursos:** 高校 = *preparatoria* (*último año de preparatoria*, 高校３年), 中学 = *secundaria* (*tercero de secundaria*).
- **Tablero de exploración:** Takumi narra en primera persona, como el japonés (*Encontré una colmena*); los avisos del sistema van como en el resto de la interfaz (*Obtuviste: X.*) y las opciones, en infinitivo y en un solo renglón (*Estirar la mano.*).

## Tono y voz de los personajes

Mantener los tics de cada personaje según el inglés (cortes, tartamudeos *"N-No"*, jerga, muletillas, groserías).
No suavizar ni intensificar las groserías: igualar la intensidad del original.
Risas fijas, como el inglés: SIREI *Juafafafaj* (ちゅふふ), NIGOU *Juofofofoj* (la misma ちゅふふ; el inglés le dio otra), Darumi *Kyohohoho* (きょっきょっきょ), Kurara *Kijijijí* (キシシシ), Yugamu *Ufufu* (うふふ). Darumi habla de sí misma en tercera persona, como el japonés (*Darumi no entiende...*).

## Formato

- Signos de apertura obligatorios: `¿` y `¡`. Si la línea continúa una frase de la línea anterior (empieza en minúscula), el signo de apertura va en la anterior.
- Combinados: `¡¿...?!` cuando el inglés usa `?!`. Varios signos de cierre llevan la misma cantidad de apertura: `¡¡FUERA!!`.
- Comillas: siempre rectas `"..."` (no `«»` ni `“”`). Donde las usa el japonés (「」, 『』); las que agrega el inglés, solo si aclaran que alguien cita o dice algo.
  El punto final va **fuera** de las comillas (`"...lo que yo diga".`); `?`, `!` y `...` van dentro si son de lo citado.
- Puntos suspensivos: tres puntos `...` (como el original), sin espacio antes.
- Tartamudeo: `P-Por favor`, con mayúscula repetida si la palabra la lleva.
- Gritos en MAYÚSCULAS como en el inglés.
- **Códigos de control intactos**: `{fc(57e4f1)...}`, `{ft1}`, `%s`, etc. Ni traducir ni mover lo que está dentro de las llaves salvo el texto visible.
- Saltos de línea: respetar los del original; si el español es mucho más largo, puede no entrar en pantalla (lo avisan los chequeos `largo` y `ancho`).

### Estudiantes de la Penúltima Academia

- **NIGOU:** habla casual como SIREI (*tú*, *Takumi*); le dice *Su Excelencia SIREI* a SIREI.
- **Kyoshika:** *usted* con todos y *don/doña* + nombre (*doña Kurara*, *doña Nozomi*); a veces habla de sí misma por el nombre. Mezcla referencias de manga y ninjas con su habla de época.
- **Kurara:** *tú*, insultos constantes (*plebeyo*, *pobretón*, *Inclina la cabeza, idiota*).
- **Yugamu:** *tú*, *Sumino*; cambia *hacer* por *matar* en sus frases (殺る). Formas fijas: 殺ぁ *Buenas muertes*, 殺れ殺れ *Válgame la muerte*, 殺っかい *muertificante*, 殺っぱり *como era de matar*.
- **Nozomi:** *tú*, *Sumino*; a Moko le dice *Moko*.
- **Eva:** *usted* con Takumi mientras es prisionera y sigue la etiqueta; después, trato directo (*tú*) cuando se quita la máscara de cortesía. A Kirifuji (*Nozomi*) la llama por el nombre de pila, como a una hija.
- **Kamyuhn:** niña altiva que habla como una sacerdotisa de época (*necio*, *insolente*, *¡cómo osan!*); *yo*, sin vosotros.

