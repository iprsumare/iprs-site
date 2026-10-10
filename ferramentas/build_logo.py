"""Gera as versões vetoriais do logo da 2ª IPR Sumaré.
Espaço de coordenadas: o mesmo do PNG original 320x320 (centro do globo em 160,171.5)."""
import json, math, os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom
from skimage import measure
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

S = os.path.dirname(os.path.abspath(__file__))  # Montserrat-ExtraBold.ttf e land.json (Natural Earth) ficam aqui
SRC = os.path.join(S, "..", "logo", "legado") + "/"
OUT = os.path.join(S, "..", "logo") + "/"
os.makedirs(OUT, exist_ok=True)

CX, CY = 160.0, 171.5
R_GLOBE = 115.0
R_INNER_RING = (115.0, 119.2)
R_OUTER_RING = (123.0, 130.7)
R_BASE = 139.4
CAP = 12.0
ANG_START, ANG_END = 188.0, -8.0

AZUL = "#102A43"; CEU = "#4FB8CF"; PRETO = "#0B0D10"; BRANCO = "#FFFFFF"
TERRA = "#1F4B70"

def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")

# ---------- Monograma (geometria medida no logo oficial IPRB, unidades do PNG 400px) ----------
MONO_SRC = " ".join([
    # i (duas hastes com pingos)
    "M110.1,184.1H128.7V313.6H110.1Z M110.1,140.6H128.7V166.9H110.1Z",
    "M139.1,184.1H157.75V313.6H139.1Z M139.1,140.6H157.75V166.9H139.1Z",
    # bojo externo do R
    "M171,100.25H222.75A54.25,54.25 0 0 1 222.75,208.75H171Z",
    "M171,116.25H222.2A37.875,37.875 0 0 1 222.2,192H171Z",
    # bojo interno
    "M171,124.1H221.5A30.25,30.25 0 0 1 221.5,184.6H171Z",
    "M171,141H216.2A13.875,13.875 0 0 1 216.2,168.75H171Z",
    # perna 1
    "M171,219.9H204.1A44.9,44.9 0 0 1 249,264.8V313.6H230V269.65A34.05,34.05 0 0 0 195.95,235.6H171Z",
    # perna 2
    "M227.1,219.75H248.3A52.8,52.8 0 0 1 276.75,266.6V313.6H258.1V266.6A50.9,50.9 0 0 0 227.1,219.75Z",
])
MONO_BBOX = (110.1, 100.25, 276.75, 313.6)
MS = 165.0 / (MONO_BBOX[3] - MONO_BBOX[1])          # altura do monograma
MONO_X0 = 233.5 - (MONO_BBOX[2] - MONO_BBOX[0]) * MS  # canto inferior direito dentro do globo
MONO_TF = f"translate({f(MONO_X0)},92) scale({MS:.5f}) translate({-MONO_BBOX[0]},{-MONO_BBOX[1]})"

def monogram(fill):
    return f'<path transform="{MONO_TF}" fill="{fill}" fill-rule="evenodd" d="{MONO_SRC}"/>'

# ---------- Chamas (vetorizadas do logo IPRS) ----------
def catmull_to_bezier(pts):
    n = len(pts); d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(p2[0])},{f(p2[1])}"
    return d + "Z"

def trace_flames():
    im = np.asarray(Image.open(SRC + "iprs-logo-antigo-320px.png").convert("RGBA")).astype(float)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    mn = np.minimum(np.minimum(r, g), b); mx = np.maximum(np.maximum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    xx = np.arange(320)[None, :].repeat(320, 0)
    m = ((sat > 0.5) & (r > 170) & (r > b + 80) & (xx < 150)).astype(float)
    K = 8
    big = gaussian_filter(zoom(m, K, order=1), 11)
    paths = []
    for c in measure.find_contours(big, 0.5):
        if len(c) < 200:
            continue
        c = measure.approximate_polygon(c, tolerance=4.0)[:-1]
        pts = [((p[1] + 0.5) / K - 0.5 + FLAME_DX, (p[0] + 0.5) / K - 0.5) for p in c]
        paths.append(catmull_to_bezier(pts))
    return " ".join(paths)

FLAME_DX = -16.0  # chamas um pouco à esquerda, cobrindo só o pingo do i
FLAMES = trace_flames()
FLAME_GRAD = (f'<linearGradient id="chama" gradientUnits="userSpaceOnUse" x1="76" y1="208" x2="116" y2="70">'
              '<stop offset="0" stop-color="#FFCB3D"/><stop offset=".5" stop-color="#F7931E"/>'
              '<stop offset="1" stop-color="#E23B2E"/></linearGradient>')

def flames(fill, gap=None):
    # gap: cor do respiro entre as chamas e o monograma
    g = f'<path fill="none" stroke="{gap}" stroke-width="3.2" stroke-linejoin="round" d="{FLAMES}"/>' if gap else ""
    return g + f'<path fill="{fill}" d="{FLAMES}"/>'

# ---------- Globo (Natural Earth 110m, projeção ortográfica centrada em Sumaré) ----------
LAT0, LON0 = math.radians(-22.82), math.radians(-47.27)

def ortho(lon, lat):
    lon, lat = math.radians(lon), math.radians(lat)
    cosc = math.sin(LAT0) * math.sin(lat) + math.cos(LAT0) * math.cos(lat) * math.cos(lon - LON0)
    x = math.cos(lat) * math.sin(lon - LON0)
    y = math.cos(LAT0) * math.sin(lat) - math.sin(LAT0) * math.cos(lat) * math.cos(lon - LON0)
    if cosc < 0:  # lado de trás: projeta na borda
        n = math.hypot(x, y) or 1; x, y = x / n, y / n
    return CX + x * R_GLOBE, CY - y * R_GLOBE, cosc >= 0

def land_path():
    data = json.load(open(os.path.join(S, "land.json")))
    out = []
    for feat in data["features"]:
        geom = feat["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        for poly in polys:
            for ring in poly:
                pr = [ortho(lon, lat) for lon, lat in ring]
                if not any(v for _, _, v in pr):
                    continue
                out.append("M" + "L".join(f"{f(x)},{f(y)}" for x, y, _ in pr) + "Z")
    return " ".join(out)

LAND = land_path()

def graticule():
    lines = []
    for lon in range(-180, 180, 30):
        pts = [ortho(lon, lat) for lat in range(-90, 91, 3)]
        seg = [];
        for x, y, v in pts:
            if v: seg.append(f"{f(x)},{f(y)}")
            elif seg: lines.append("M" + "L".join(seg)); seg = []
        if seg: lines.append("M" + "L".join(seg))
    for lat in range(-60, 61, 30):
        pts = [ortho(lon, lat) for lon in range(-180, 181, 3)]
        seg = []
        for x, y, v in pts:
            if v: seg.append(f"{f(x)},{f(y)}")
            elif seg: lines.append("M" + "L".join(seg)); seg = []
        if seg: lines.append("M" + "L".join(seg))
    return " ".join(lines)

GRAT = graticule()

# ---------- Texto em curva (Montserrat ExtraBold convertida em contorno) ----------
FONT = TTFont(os.path.join(S, "Montserrat-ExtraBold.ttf"))
GS = FONT.getGlyphSet(); CMAP = FONT.getBestCmap(); HMTX = FONT["hmtx"]
TEXT = "2ª IGREJA PRESBITERIANA RENOVADA DE SUMARÉ"

def arc_text(fill):
    k = CAP / 700.0
    glyphs = []
    for ch in TEXT:
        gn = CMAP[ord(ch)]; adv = HMTX[gn][0]
        pen = SVGPathPen(GS); GS[gn].draw(pen)
        glyphs.append((ch, adv, pen.getCommands()))
    total = sum(a for _, a, _ in glyphs) * k
    span = math.radians(ANG_START - ANG_END) * R_BASE
    # o primeiro e o último glifo contam só metade na extensão angular
    track = (span - (total - (glyphs[0][1] + glyphs[-1][1]) * k / 2)) / (len(glyphs) - 1)
    out = []; d = -glyphs[0][1] * k / 2
    for ch, adv, cmd in glyphs:
        w = adv * k; mid = d + w / 2
        th = math.radians(ANG_START) - mid / R_BASE
        px, py = CX + R_BASE * math.cos(th), CY - R_BASE * math.sin(th)
        if cmd:
            out.append(f'<path transform="translate({f(px)},{f(py)}) rotate({90 - math.degrees(th):.3f}) '
                       f'scale({k:.5f},{-k:.5f}) translate({-adv / 2},0)" d="{cmd}"/>')
        d += w + track
    return f'<g fill="{fill}">' + "".join(out) + "</g>"

# ---------- Montagem ----------
def ring(r0, r1, color):
    return f'<circle cx="{CX}" cy="{CY}" r="{f((r0 + r1) / 2)}" fill="none" stroke="{color}" stroke-width="{f(r1 - r0)}"/>'

def globe_color():
    return (f'<clipPath id="globo"><circle cx="{CX}" cy="{CY}" r="{R_GLOBE}"/></clipPath>'
            f'<g clip-path="url(#globo)"><circle cx="{CX}" cy="{CY}" r="{R_GLOBE}" fill="{AZUL}"/>'
            f'<path fill="{TERRA}" d="{LAND}"/>'
            f'<path fill="none" stroke="{CEU}" stroke-opacity=".22" stroke-width=".6" d="{GRAT}"/></g>')

def svg(body, vb, title, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'<title>{title}</title><defs>{FLAME_GRAD}{defs}</defs>{body}</svg>\n')

VB_FULL = "0 11 320 295"
VB_SYMBOL = f"{f(CX - 132)} {f(CY - 132)} 264 264"
TITLE = "2ª Igreja Presbiteriana Renovada de Sumaré"

def color_logo(ink, with_text=True):
    body = ""
    if with_text:
        body += arc_text(ink)
    body += ring(*R_OUTER_RING, ink) + globe_color() + ring(*R_INNER_RING, ink)
    body += monogram(BRANCO) + flames("url(#chama)", AZUL)
    return body

def mono_logo(ink, with_text=True):
    # uma cor só: monograma vazado e chamas separadas por um respiro
    mask = (f'<mask id="vazado" maskUnits="userSpaceOnUse" x="0" y="0" width="320" height="320">'
            f'<rect width="320" height="320" fill="#fff"/>{monogram("#000")}'
            f'<path fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round" d="{FLAMES}"/>'
            f'<path fill="#000" d="{FLAMES}"/></mask>')
    body = ""
    if with_text:
        body += arc_text(ink)
    body += (f'<g mask="url(#vazado)">{ring(*R_OUTER_RING, ink)}'
             f'<circle cx="{CX}" cy="{CY}" r="{R_INNER_RING[1]}" fill="{ink}"/></g>')
    return body, mask

files = {
    "iprs-logo-cor.svg": svg(color_logo(PRETO), VB_FULL, TITLE),
    "iprs-logo-cor-negativo.svg": svg(color_logo(BRANCO), VB_FULL, TITLE),
    "iprs-simbolo-cor.svg": svg(color_logo(PRETO, False), VB_SYMBOL, TITLE),
    "iprs-simbolo-cor-negativo.svg": svg(color_logo(BRANCO, False), VB_SYMBOL, TITLE),
}
for name, ink in [("preto", PRETO), ("branco", BRANCO), ("azul", AZUL)]:
    b, m = mono_logo(ink); files[f"iprs-logo-{name}.svg"] = svg(b, VB_FULL, TITLE, m)
    b, m = mono_logo(ink, False); files[f"iprs-simbolo-{name}.svg"] = svg(b, VB_SYMBOL, TITLE, m)

for name, content in files.items():
    open(OUT + name, "w", encoding="utf-8").write(content)
    print(name, len(content))
