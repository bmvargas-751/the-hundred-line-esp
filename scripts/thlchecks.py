"""Chequeos automáticos sobre la vista unificada. Cada chequeo devuelve (nombre, detalle) por línea."""
import re
from collections import Counter

import thldatos as td

CODE = re.compile(r"\{[a-z]+\d*(?:\([^)]*\))?|\}|%[sd]")
EN_WORDS = re.compile(r"\b(the|you|and|what|this|that|is|are|was|don't|I'm|it's|with|for|have|just|gonna)\b", re.I)
VISIBLE = re.compile(r"\{[a-z]+\d*(?:\([^)]*\))?|\}")

# Formas que no deben aparecer, con la forma correcta (ver GLOSSARY.md y STYLE.md).
# Cada regla se aplica solo si el inglés tiene el término original (el primer patrón).
TERMS = [
    (r"Last Defense Academy", r"Academia de Defensa Final|Academia (?:de )?(?:la )?Última Defensa", "Última Academia de Defensa"),
    (r"Shion Bomb", r"[Bb]omba de Shion|Shion Bomb", "Bomba Shion"),
    (r"\bEnd Turn\b", r"[Ff]inalizar (?:el )?turno", "Terminar turno"),
    (r"Undying Flame", r"[Ll]lamas (?:[Ii]mperecederas|[Ii]nmortales|[Ii]nextinguibles)", "Llamas Eternas"),
    (r"Bio Lab", r"\b[Bb]iolaboratorio\b|\b[Ll]ab biológico\b", "laboratorio biológico"),
    (r"Futuran", r"\b[Ff]uturian[oa]s?\b|\b[Ff]uturamos\b", "futuranos"),
    (r"World Death", r"Muerte (?:Mundial|Global)|muerte mundial", "Muerte del Mundo"),
    (r"\bMorgue\b", r"\bdepósito\b", "morgue"),
    (r"\bMistress\b", r"\b(?:Sra\.|[Ss]eñora|[Aa]ma|reina) (?=Hiruko|Tsubasa)|\b[Ll]a ama\b|\b[Ee]l ama\b", "Reina + nombre"),
    (r"\bBP\b", r"\bPP\b|\bPH\b", "BP"),
    (r"V'ehxness|Dahl'xia|Zen'ta", r"\b(?:Vehxness|Dahlxia|Zenta)\b", "con apóstrofo (V'ehxness, Dahl'xia, Zen'ta)"),
    # Nombres que inventó o cambió el inglés (criterio 2 del glosario)
    (r"Second-to-Last|Second Academy", r"Segunda Academia|Academia de (?:la )?Penúltima|Penúltima Academia de la Defensa",
     "Penúltima Academia de Defensa"),
    (r"Revive-O-Matic", r"[Mm]áquina de resurrección|[Rr]esucitador|[Rr]eanimador|\b(?:[Ll]a|[Uu]na)\s+Revive-O-Matic",
     "el Revive-O-Matic"),
    (r"Gift-O-Matic", r"[Mm]áquina de regalos|[Rr]egalador|\b(?:[Ll]a|[Uu]na)\s+Gift-O-Matic", "el Gift-O-Matic"),
    (r"Ration-O-Matic", r"[Mm]áquina de cocina|[Rr]acionador|\b(?:[Ll]a|[Uu]na)\s+Ration-O-Matic", "el Ration-O-Matic"),
    (r"Candy-O-Matic", r"\b(?:[Ll]a|[Uu]na)\s+Candy-O-Matic", "el Candy-O-Matic"),
    (r"Infuser", r"[Ii]nfusor|espada de hemoánima", "Infuser"),
    (r"Paragon", r"[Pp]arang[óo]n|[Ee]ncarnaci[óo]n|\b[Ll]a Paragon", "el Paragon de X"),
    (r"Supreme Commander", r"Gran General", "Comandante Suprema"),
    (r"Sister Dearest", r"\b[Hh]ermanita\b|[Hh]ermana querida|\bquerida hermana", "queridísima hermana"),
    (r"Brother Dearest", r"\b[Hh]ermanito\b|[Hh]ermano querido|\bquerido hermano", "queridísimo hermano"),
    (r"[Ss]ponsor", r"[Oo]rganizador|Alianza VS", "patrocinador / Alianza Antipatrocinador"),
]
# Términos que se deciden por el japonés (GLOSSARY.md): la regla se aplica si el japonés tiene el término.
LAT = r"(?<![A-Za-zＡ-Ｚａ-ｚ])"  # sin letra latina antes (el japonés pega las siglas a los kanji)
JP_TERMS = [
    (r"殿", r"\b(?:Sir|Lady|Sr\.|Srta\.|[Mm]aese) (?=[A-Z])", "don / doña + nombre de pila"),
    (r"先生", r"\b(?:Sr\.|Srta\.|Sra\.) (?=[A-Z])", "profesor"),
    (r"閣下", r"[Hh]onorable", "Su Excelencia"),
    (r"サイワイの箱", r"[Bb]endici[óo]n", "Caja de la Dicha"),
    (r"ワザワイの箱", r"[Cc]alamidad", "Caja de la Desdicha"),
    (r"様", r"[Ss]oberan[oa]", "mi señora"),
    (r"名簿", r"[Bb]olet[íi]n de notas|[Bb]oletas? de calificaciones", "Registro"),
    (r"ＳＩＲＥＩ|ＮＩＧＯＵ", r"\b(?:Sirei|Nigou)\b", "SIREI / NIGOU, en mayúsculas"),
    (r"ＴＬ", r"[Ll]íneas? (?:temporal|de tiempo)", "TL"),
    (r"ＰＬ", r"\bMSP\b|\bPLM\b|[Ss]alto [Pp]aralelo", "PL / dispositivo PL"),
    (r"パラレリープ", r"[Ss]alto [Pp]aralelo|\bMSP\b", "Parallel Leap"),
    (r"リープスーツ", r"[Tt]raje de salto", "Leap Suit"),
    (r"ブラッドスペース|ＢＳ波", r"[Ee]spacio [Ss]angriento", "Blood Space / ondas BS"),
    (r"ＱＢリキッド", r"[Ll]íquido QB", "QB Liquid"),
    (r"青春ＴＬ", r"[Jj]uventud|mayoría de edad|[Mm]aduraci[óo]n", "TL de la Madurez"),
    (r"殺人鬼ＴＬ", r"Asesino(?! en [Ss]erie)", "TL del Asesino en Serie"),
    (r"東京団地", r"\bCRT\b|\bTRC\b", "Complejo Residencial de Tokio, sin sigla"),
    (r"特防隊", r"\bUDE\b|\bSDU\b", "Unidad de Defensa Especial, sin sigla"),
    (LAT + r"[HＨ][PＰ]", r"\bPV\b", "HP"),
    (LAT + r"[AＡ][PＰ]", r"\bPA\b", "AP"),
    (r"VOLTAGE", r"[Vv]oltaje|VOLTAJE", "VOLTAGE"),
    (r"WAVE", r"[Oo]leada|OLEADA", "WAVE"),
    (r"Lv", r"\b[Nn]v\.|\b[Nn]iv\.|\bNivel \d", "Lv"),
    (r"MAX", r"MÁX", "MAX"),
    (r"ナイスDEATH", r"¡Bien!", "Nice DEATH"),
    (r"我駆力", r"\b(?:el|del|al|nuestro|este|ese|un) hemoánima", "la hemoánima (femenino)"),
    # Frases delicadas: siguen al inglés (revisión final, ver STYLE.md); no deben volver las formas provisorias
    (r"∞態", r"Forma Infinita", "¡Sangre de mi vínculo, libérate! / lo que diga el inglés"),
    (r"殺れ殺れ", r"[Vv]álgame", "como el inglés (Por el amor de la muerte...)"),
    (r"殺ぁ", r"[Bb]uenas muertes|Matarile", "un saludo, como el inglés"),
    (r"ガンマフィール", r"Gammafeel", "Gammaphiel"),
    (r"死斑番号", r"[Nn]úmeros? mortuorios?", "código de livor mortis"),
    (r"神の再臨", r"regreso de Dios", "la Segunda Venida"),
    (r"ドルメン式", r"de estilo dolmen", "Terapia de Reconstrucción Cognitiva Dolménica"),
]
JP_TERMS = [(re.compile(jp), re.compile(es), fix) for jp, es, fix in JP_TERMS]
TERMS = [(re.compile(en), re.compile(es), fix) for en, es, fix in TERMS]

VOSOTROS = re.compile(
    r"\b(?:vosotr[oa]s|vuestr[oa]s?|os)\b"
    r"|\b\w+(?:áis|éis)\b"
    # imperativo (-ad/-ed/-id, con pronombre opcional), sin sustantivos como verdad, mitad, pared, usted
    r"|\b(?!(?:\w*(?:dad|tad)|pared|red|sed|usted|merced|césped|huésped|Madrid|David|lid|vid|ardid|adalid)\b)"
    r"\w{2,}(?:ad|ed|id)(?:me|nos|lo|la|los|las|le|les)?(?=\s*[!.,?…]|\s*$)"
    r"|\b(?!caos\b)\w{3,}aos\b|\bidos\b"
    r"|\b(?:estad|venid|mirad|esperad|escuchad|dejad|tened|haced|decid|poned|salid|seguid|volved|traed|sacad|id a)\b",
    re.I)
PENINSULAR = re.compile(
    r"\b(vale|tío|tía|venga|guay|mola\w*|coger|cog[ií]\w*|ordenador|móvil|pasta|majo|maja|gilipollas|joder|"
    r"hostia\w*|pillar|pill[eé]\w*|flipa\w*|chaval\w*|enfad\w+|puls(?:a|as|ar|ando|ado|aste|e|en|ó)|vídeos?|ratón|bombona|"
    r"gafas|bañador\w*|nevera\w*|fard(?:ar|ando|ado|aba\w*|ó|a|as|an|e|es|en)|moter[oa]s?|tragaperras|aparc\w+|jerséis|jersey|auriculares|"
    r"setas?|coches?|cubos? de basura|marcapáginas|ambientador\w*|megafonía)\b", re.I)


def codes(s):
    return Counter(CODE.findall(s))


def visible(s):
    # {chr} y %s se muestran como un nombre: se reemplazan por una palabra antes de quitar los códigos
    return VISIBLE.sub("", re.sub(r"\{chr\}|%[sd]", "X", s))


SPACING = re.compile(r"  |\s+[,.;:!?](?!\.)|\.\.\.\.")
SENTENCE = re.compile(r"[a-záéíóúñ']{3,} [a-záéíóúñ']{3,}")


def original_broken(en):
    """El inglés ya tiene los códigos mal (llaves desbalanceadas, anidados o con espacios): no se marca."""
    depth = 0
    for tok in CODE.findall(en):
        if tok.startswith("{fc"):
            if depth or " " in tok:
                return True
            depth += 1
        elif tok == "}":
            if not depth:
                return True
            depth -= 1
    return depth != 0


def check_line(r):
    en, es = r["en"], r["es"]
    out = []
    if not en.strip():
        return out
    if not es.strip():
        out.append(("vacia", "sin texto en español"))
        return out
    if es == en:
        # dos palabras seguidas en minúscula: es una frase, no un nombre ni una onomatopeya
        if SENTENCE.search(visible(en)) and not re.search(r"[぀-ヿ一-鿿]", en):
            out.append(("sin_traducir", "igual al inglés"))
        return out
    ce, cs = codes(en), codes(es)
    if ce != cs and not original_broken(en):
        missing = ce - cs
        extra = cs - ce
        out.append(("codigos", f"faltan {dict(missing)} sobran {dict(extra)}".replace("{}", "-")))
    if len(EN_WORDS.findall(es)) >= 3 and len(EN_WORDS.findall(es)) >= len(es.split()) / 4:
        out.append(("ingles_mezclado", "parece tener frases en inglés"))
    le, ls = len(visible(en)), len(visible(es))
    if ls > le * 1.6 + 20:
        out.append(("largo", f"{ls} vs {le} caracteres"))
    # Solo importa si hay saltos manuales (interfaz): el renglón más largo no debe pasar al del inglés
    if "\n" in en.strip():
        we = max(len(x) for x in visible(en).split("\n"))
        ws = max(len(x) for x in visible(es).split("\n"))
        if ws > we * 1.1 + 2:
            out.append(("ancho", f"renglón más largo: ES {ws}, EN {we} caracteres"))
    # una línea que empieza en minúscula continúa la frase anterior, que ya tiene el signo de apertura
    if not re.match(r"[\s.…—]*[a-záéíóúñ]", visible(es)):
        if es.count("?") > es.count("¿"):
            out.append(("falta_apertura", "falta ¿"))
        if es.count("!") > es.count("¡"):
            out.append(("falta_apertura", "falta ¡"))
    # comillas donde las pone el japonés (「」『』“”); las que solo agrega el inglés no se exigen
    jp = r.get("jp") or ""
    if re.search(r'["“”]', en) and '"' not in es and (not jp or re.search(r'[「」『』“”"]', jp)):
        out.append(("comillas", "el inglés tiene comillas y el español no"))
    if re.search(r"[«»“”]", es):
        out.append(("comillas", "usar comillas rectas \"...\""))
    if SPACING.search(visible(es)) and not SPACING.search(visible(en)):
        out.append(("espacios", "espacios o puntos de más"))
    for en_rx, rx, fix in TERMS:
        m = en_rx.search(en) and rx.search(es)
        if m:
            out.append(("glosario", f"'{m.group(0)}' -> {fix}"))
    jp = r.get("jp", "")
    for jp_rx, rx, fix in (JP_TERMS if td.VERSION == "jp" else ()):
        m = jp and jp_rx.search(jp) and rx.search(es)
        if m:
            out.append(("japones", f"'{m.group(0)}' -> {fix}"))
    for name, rx in (("vosotros", VOSOTROS), ("peninsular", PENINSULAR)):
        found = sorted({m.group(0).lower() for m in rx.finditer(es)})
        if found:
            out.append((name, ", ".join(found)))
    return out
