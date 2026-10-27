"""Arregla las letras del español en las fuentes del menú (commonfont.bin y commonfont2.bin, dentro de app_1).

Esas fuentes son japonesas: las letras normales son angostas (ancho 500), pero á é í ó ú ñ ü, sus mayúsculas,
¿ y ¡ vienen de otro diseño más ancho y se ven "gordas" al lado de las demás. Aquí se rehacen con el mismo ancho:
la letra angosta más el acento del diseño original, centrado encima; ¿ y ¡ son ? y ! girados.

Uso: python3 -I scripts/thlfuente.py <fuente.bin> [<salida.bin>]   (sin salida, la reescribe)
Solo usa la biblioteca estándar: lo usa el instalador sobre la copia del juego de cada persona.
"""
import struct
import sys
from pathlib import Path

ARCHIVE = "app_1"  # app_1.dx11.mvgl: recursos del idioma inglés
FONTS = ("commonfont.bin", "commonfont2.bin")
ACCENTED = {  # letra con tilde: letra base angosta
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u",
    "Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ñ": "N", "Ü": "U",
}
INVERTED = {"¿": "?", "¡": "!"}
GAP = 40  # separación entre una mayúscula y su acento


# ---------- lectura y escritura de la fuente ----------

def read_tables(data):
    num = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num):
        tag, _, off, length = struct.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tables[tag.decode("latin-1")] = data[off:off + length]
    return data[:4], tables


def checksum(blob):
    blob += b"\0" * (-len(blob) % 4)
    return sum(struct.unpack(f">{len(blob) // 4}I", blob)) & 0xFFFFFFFF


def write_font(version, tables):
    tags = sorted(tables)
    num = len(tags)
    entry = 1 << (num.bit_length() - 1)
    header = version + struct.pack(">HHHH", num, entry * 16, entry.bit_length() - 1, num * 16 - entry * 16)
    head = bytearray(tables["head"])
    head[8:12] = b"\0\0\0\0"  # checkSumAdjustment se calcula al final
    tables = dict(tables, head=bytes(head))
    offset = len(header) + 16 * num
    directory, body = b"", b""
    for tag in tags:
        blob = tables[tag]
        directory += struct.pack(">4sIII", tag.encode("latin-1"), checksum(blob), offset + len(body), len(blob))
        body += blob + b"\0" * (-len(blob) % 4)
    font = bytearray(header + directory + body)
    adjust = (0xB1B0AFBA - checksum(bytes(font))) & 0xFFFFFFFF
    pos = font.find(tables["head"], len(header) + len(directory))
    font[pos + 8:pos + 12] = struct.pack(">I", adjust)
    return bytes(font)


def cmap_lookup(cmap, chars):
    """Glifo de cada carácter, con la subtabla Unicode de formato 4 (o 12)."""
    want = {ord(c) for c in chars}
    found = {}
    num = struct.unpack(">H", cmap[2:4])[0]
    for i in range(num):
        pid, eid, off = struct.unpack(">HHI", cmap[4 + 8 * i:12 + 8 * i])
        fmt = struct.unpack(">H", cmap[off:off + 2])[0]
        if fmt == 4:
            seg = struct.unpack(">H", cmap[off + 6:off + 8])[0] // 2
            p = off + 14
            ends = struct.unpack(f">{seg}H", cmap[p:p + 2 * seg])
            p += 2 * seg + 2
            starts = struct.unpack(f">{seg}H", cmap[p:p + 2 * seg])
            p += 2 * seg
            deltas = struct.unpack(f">{seg}h", cmap[p:p + 2 * seg])
            p += 2 * seg
            ros = struct.unpack(f">{seg}H", cmap[p:p + 2 * seg])
            for u in want:
                for s in range(seg):
                    if starts[s] <= u <= ends[s]:
                        if ros[s] == 0:
                            g = (u + deltas[s]) & 0xFFFF
                        else:
                            a = p + 2 * s + ros[s] + 2 * (u - starts[s])
                            g = struct.unpack(">H", cmap[a:a + 2])[0]
                            g = (g + deltas[s]) & 0xFFFF if g else 0
                        if g:
                            found.setdefault(chr(u), g)
                        break
        elif fmt == 12:
            groups = struct.unpack(">I", cmap[off + 12:off + 16])[0]
            for k in range(groups):
                s0, e0, g0 = struct.unpack(">III", cmap[off + 16 + 12 * k:off + 28 + 12 * k])
                for u in want:
                    if s0 <= u <= e0:
                        found.setdefault(chr(u), g0 + u - s0)
    return found


# ---------- glifos simples ----------

def decode_glyph(blob):
    """Glifo simple -> lista de contornos [(x, y, en_curva), ...]."""
    if not blob:
        return []
    ncont = struct.unpack(">h", blob[:2])[0]
    if ncont < 0:
        raise ValueError("glifo compuesto")
    ends = struct.unpack(f">{ncont}H", blob[10:10 + 2 * ncont])
    p = 10 + 2 * ncont
    ilen = struct.unpack(">H", blob[p:p + 2])[0]
    p += 2 + ilen
    npts = ends[-1] + 1 if ncont else 0
    flags = []
    while len(flags) < npts:
        f = blob[p]
        p += 1
        flags.append(f)
        if f & 8:
            flags += [f] * blob[p]
            p += 1
    coords = []
    for short, same in ((2, 16), (4, 32)):
        v, vals = 0, []
        for f in flags:
            if f & short:
                d = blob[p]
                p += 1
                v += d if f & same else -d
            elif not f & same:
                v += struct.unpack(">h", blob[p:p + 2])[0]
                p += 2
            vals.append(v)
        coords.append(vals)
    pts = [(x, y, bool(f & 1)) for x, y, f in zip(coords[0], coords[1], flags)]
    out, start = [], 0
    for e in ends:
        out.append(pts[start:e + 1])
        start = e + 1
    return out


def encode_glyph(contours):
    """Contornos -> glifo simple, sin instrucciones de hinting."""
    pts = [p for c in contours for p in c]
    xs = [round(p[0]) for p in pts]
    ys = [round(p[1]) for p in pts]
    ends, n = [], 0
    for c in contours:
        n += len(c)
        ends.append(n - 1)
    flags, xb, yb = [], b"", b""
    px = py = 0
    for (x, y, on) in zip(xs, ys, [p[2] for p in pts]):
        f = 1 if on else 0
        dx, dy = x - px, y - py
        if dx == 0:
            f |= 16
        elif -255 <= dx <= 255:
            f |= 2 | (16 if dx > 0 else 0)
            xb += bytes([abs(dx)])
        else:
            xb += struct.pack(">h", dx)
        if dy == 0:
            f |= 32
        elif -255 <= dy <= 255:
            f |= 4 | (32 if dy > 0 else 0)
            yb += bytes([abs(dy)])
        else:
            yb += struct.pack(">h", dy)
        flags.append(f)
        px, py = x, y
    blob = struct.pack(">hhhhh", len(contours), min(xs), min(ys), max(xs), max(ys))
    blob += struct.pack(f">{len(ends)}H", *ends) + struct.pack(">H", 0) + bytes(flags) + xb + yb
    return blob + b"\0" * (-len(blob) % 4)


def bbox(contours):
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def move(contours, dx=0, dy=0):
    return [[(x + dx, y + dy, on) for x, y, on in c] for c in contours]


def split_marks(contours):
    """Separa el acento (contornos por encima del cuerpo de la letra) del cuerpo."""
    body_top = max(max(p[1] for p in c) for c in contours if min(p[1] for p in c) < 300)
    marks = [c for c in contours if min(p[1] for p in c) > body_top]
    body = [c for c in contours if c not in marks]
    return body, marks


# ---------- arreglo ----------

def patch_font(data):
    version, t = read_tables(data)
    long_loca = struct.unpack(">h", t["head"][50:52])[0] == 1
    num_glyphs = struct.unpack(">H", t["maxp"][4:6])[0]
    n_hmetrics = struct.unpack(">H", t["hhea"][34:36])[0]
    loca_fmt = f">{num_glyphs + 1}{'I' if long_loca else 'H'}"
    loca = [o * (1 if long_loca else 2) for o in struct.unpack(loca_fmt, t["loca"])]
    glyphs = [t["glyf"][loca[i]:loca[i + 1]] for i in range(num_glyphs)]
    hmtx = bytearray(t["hmtx"])

    def advance(g):
        return struct.unpack(">H", hmtx[4 * min(g, n_hmetrics - 1):4 * min(g, n_hmetrics - 1) + 2])[0]

    gid = cmap_lookup(t["cmap"], "".join(ACCENTED) + "".join(ACCENTED.values()) + "".join(INVERTED) + "".join(INVERTED.values()))
    new = {}
    for ch, base_ch in ACCENTED.items():
        if ch not in gid or base_ch not in gid:
            continue
        body, marks = split_marks(decode_glyph(glyphs[gid[ch]]))
        base = decode_glyph(glyphs[gid[base_ch]])
        if base_ch == "i":  # la i pierde su punto
            base = [c for c in base if min(p[1] for p in c) < 300]
        if not marks:
            continue
        bx0, by0, bx1, by1 = bbox(base)
        mx0, my0, mx1, my1 = bbox(marks)
        dx = (bx0 + bx1) / 2 - (mx0 + mx1) / 2
        dy = max(0, by1 + GAP - my0) if ch.isupper() else 0  # en mayúsculas, el acento sube por encima de la letra
        new[gid[ch]] = (base + move(marks, dx, dy), advance(gid[base_ch]))
    for ch, base_ch in INVERTED.items():
        if ch not in gid or base_ch not in gid:
            continue
        wide = decode_glyph(glyphs[gid[ch]])
        base = decode_glyph(glyphs[gid[base_ch]])
        adv = advance(gid[base_ch])
        c = bbox(wide)[1] + bbox(base)[3]  # misma altura que el signo original
        new[gid[ch]] = ([[(adv - x, c - y, on) for x, y, on in cont] for cont in base], adv)

    max_pts = struct.unpack(">H", t["maxp"][6:8])[0]
    max_cont = struct.unpack(">H", t["maxp"][8:10])[0]
    for g, (contours, adv) in new.items():
        glyphs[g] = encode_glyph(contours)
        x0 = bbox(contours)[0]
        if g < n_hmetrics:
            hmtx[4 * g:4 * g + 4] = struct.pack(">Hh", adv, round(x0))
        else:  # comparte el ancho del último registro: solo se puede tocar el lsb
            o = 4 * n_hmetrics + 2 * (g - n_hmetrics)
            hmtx[o:o + 2] = struct.pack(">h", round(x0))
        max_pts = max(max_pts, sum(len(c) for c in contours))
        max_cont = max(max_cont, len(contours))

    glyf, offsets = b"", []
    for blob in glyphs:
        offsets.append(len(glyf))
        glyf += blob + b"\0" * (-len(blob) % 4)
    offsets.append(len(glyf))
    if not long_loca and offsets[-1] > 0x1FFFE:
        raise ValueError("la fuente no entra en loca corto")
    t["glyf"] = glyf
    t["loca"] = struct.pack(loca_fmt, *(o if long_loca else o // 2 for o in offsets))
    t["hmtx"] = bytes(hmtx)
    maxp = bytearray(t["maxp"])
    maxp[6:10] = struct.pack(">HH", max_pts, max_cont)
    t["maxp"] = bytes(maxp)
    return write_font(version, t), len(new)


def patch_dir(folder):
    """Arregla las fuentes dentro de app_1 desempaquetado; devuelve cuántas letras rehízo."""
    total = 0
    for name in FONTS:
        path = Path(folder) / name
        data, n = patch_font(path.read_bytes())
        path.write_bytes(data)
        total += n
    return total


def main():
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    data, n = patch_font(src.read_bytes())
    dst.write_bytes(data)
    print(f"{src.name}: {n} letras rehechas")


if __name__ == "__main__":
    main()
