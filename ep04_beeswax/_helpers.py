"""مقطع عرضي – EP03 الفشار – style v3 (layered collage on riso plate)."""
import sys; sys.path.insert(0, '../ep01_cattongue')
from m3 import *
import m3, subprocess, re, random
from scipy import ndimage as ndi

HERE3 = os.path.dirname(os.path.abspath(__file__))
def P(n): return os.path.join(HERE3, n)

# ------------------------------------------------------------------ assets
_A = {}
def A(n):
    if n not in _A: _A[n] = Image.open(P(f'cut/{n}.png')).convert('RGBA')
    return _A[n]
_RS = {}
def rs(im, w, key=None):
    w = max(2, int(round(w)))
    k = (key, w) if key else None
    if k and k in _RS: return _RS[k]
    h = max(2, int(round(im.height * w / im.width)))
    r = im.resize((w, h), Image.LANCZOS if w < im.width * .6 else Image.BILINEAR)
    if k:
        if len(_RS) > 400: _RS.clear()
        _RS[k] = r
    return r

def paste(c, im, cx, cy, alpha=1.0, rot=0.0, clip=True):
    """alpha-blend RGBA PIL image centred at (cx,cy) into float canvas c (clipped to plate)."""
    if alpha <= 0.003: return
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    x0 = int(round(cx - w / 2)); y0 = int(round(cy - h / 2))
    bx0, by0, bx1, by1 = (PX0 + 3, PY0 + 3, PX1 - 3, PY1 - 3) if clip else (0, 0, W, H)
    X0, Y0, X1, Y1 = max(bx0, x0), max(by0, y0), min(bx1, x0 + w), min(by1, y0 + h)
    if X1 <= X0 or Y1 <= Y0: return
    s = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]; m = s[..., 3:4] / 255 * alpha
    sub = c[Y0:Y1, X0:X1]; sub[:] = sub * (1 - m) + s[..., :3] * m

def layer(c, n, cx, cy, w, alpha=1.0, rot=0.0, img=None):
    im = img if img is not None else A(n)
    paste(c, rs(im, w, None if img is not None else n), cx, cy, alpha, rot)

def red_mask(im):
    a = np.asarray(im).astype(np.int16)
    return ((a[..., 0] > 170) & (a[..., 1] < 120) & (a[..., 2] < 110) & (a[..., 3] > 100))

# ------------------------------------------------------------------ drawing primitives
def disc(c, cx, cy, r, col, alpha=1.0):
    if r <= 1 or alpha <= 0: return
    x0, x1 = int(max(PX0, cx - r - 2)), int(min(PX1, cx + r + 2)); y0, y1 = int(max(PY0, cy - r - 2)), int(min(PY1, cy + r + 2))
    if x1 <= x0 or y1 <= y0: return
    yy_, xx_ = np.mgrid[y0:y1, x0:x1]
    m = np.clip(r - np.sqrt((xx_ - cx) ** 2 + (yy_ - cy) ** 2) + .5, 0, 1)[..., None] * alpha
    sub = c[y0:y1, x0:x1]; g = GR[y0:y1, x0:x1, None] * .5
    sub[:] = sub * (1 - m) + (col + g) * m

def ring(c, cx, cy, r, prog, col=NAVYt, width=3, start=-90):
    if prog <= 0: return
    def fn(d, im):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 360 * clamp(prog), fill=col, width=width)
        if prog > .02:
            a = math.radians(start + 360 * clamp(prog)); d.ellipse([cx + r * math.cos(a) - 7, cy + r * math.sin(a) - 7, cx + r * math.cos(a) + 7, cy + r * math.sin(a) + 7], fill=REDt)
    draw_on(c, fn)

HEADF = AMIRI(76); KICKF = kufi(28, 'Medium')
def headline(c, kicker, words, t0, t, accent=None, out_t=None):
    """kicker + headline, word-by-word rise; accent word in vermilion."""
    dt = t - t0
    if dt < 0: return
    fade = 1.0 if out_t is None else 1 - clamp((t - out_t) / .25)
    if fade <= 0: return
    ws = words.split(); n = len(ws)
    sp = HEADF.getlength(' ', direction='rtl', language='ar')
    wl = [HEADF.getlength(w, direction='rtl', language='ar') for w in ws]; tot = sum(wl) + sp * (n - 1)
    hy = PY0 + 150
    def fn(d, im):
        ka = clamp(dt / .3) * fade
        if kicker and ka > 0:
            col = tuple(int(PAPER[i] + (NAVY[i] - PAPER[i]) * ka * .8) for i in range(3))
            d.text((W / 2, PY0 + 62), kicker, font=KICKF, fill=col, anchor='mm', direction='rtl', language='ar')
            lw = 70 * eoc(dt / .5)
            kb = d.textbbox((W / 2, PY0 + 62), kicker, font=KICKF, anchor='mm', direction='rtl', language='ar')
            d.line([(kb[0] - 18 - lw, PY0 + 64), (kb[0] - 18, PY0 + 64)], fill=col, width=2)
            d.line([(kb[2] + 18, PY0 + 64), (kb[2] + 18 + lw, PY0 + 64)], fill=col, width=2)
        x = W / 2 + tot / 2
        for i, (w, l) in enumerate(zip(ws, wl)):
            q = eoc((dt - .12 - i * .14) / .35) * fade
            if q > 0:
                acc = accent is not None and (w == accent or accent in w)
                base = RED if acc else NAVY
                col = tuple(int(PAPER[j] + (base[j] - PAPER[j]) * q) for j in range(3))
                d.text((x, hy + 18 * (1 - q)), w, font=HEADF, fill=col, anchor='rm', direction='rtl', language='ar')
            x -= l + sp
    draw_on(c, fn)

COUNTF = AMIRI(150)
def big_number(c, s, cx, cy, t0, t, col=RED, size=150, out_t=None):
    dt = t - t0
    if dt < 0: return
    a = clamp(dt / .1) * (1 if out_t is None else 1 - clamp((t - out_t) / .2))
    if a <= 0: return
    m = text_img(s, AMIRI(size), None); sc = 1.25 - .25 * spring(dt / .45)
    stamp(c, m, PAPER, cx + 4, cy + 4, sc, a)
    stamp(c, m, col, cx, cy, sc, a)

def ar_num(n):
    return str(n).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))

def halftone_photo(c, path, cx, cy, wbox, hbox, k, z=1.0, color_mix=0.0, magenta=False, ox=0, oy=0):
    """photo on light bg printed as navy halftone (k = print-in 0..1); color_mix shows real colour."""
    im = load(P(path)).convert('RGB')
    s = min(wbox / im.width, hbox / im.height) * z
    r = im.resize((int(im.width * s), int(im.height * s)), Image.BILINEAR)
    a = np.asarray(r).astype(np.float32); h, w = a.shape[:2]
    x0 = int(cx - w / 2) + ox; y0 = int(cy - h / 2) + oy
    X0, Y0, X1, Y1 = max(PX0 + 3, x0), max(PY0 + 3, y0), min(PX1 - 3, x0 + w), min(PY1 - 3, y0 + h)
    a = a[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]; hh, ww = a.shape[:2]
    rr, gg, bb = a[..., 0], a[..., 1], a[..., 2]
    L = (.3 * rr + .59 * gg + .11 * bb) / 255
    dens = np.clip((0.86 - L) * 1.9, 0, 1) ** .8
    dot = DOT[(Y0 - PY0) % 6: (Y0 - PY0) % 6 + hh, :ww] if False else _dotgrid(Y0, X0, hh, ww)
    nv = (dot < dens * (1.55 if magenta else 1.25) * k).astype(np.float32)
    rd = np.zeros_like(nv)
    if magenta:
        mg = np.clip((np.minimum(rr, bb) - gg - 40) / 40, 0, 1)
        rd = mg * (dot < 1.2 * k); nv = nv * (1 - mg)
    sub = c[Y0:Y1, X0:X1]
    if color_mix < 1:
        base = sub.copy()
        base[:] = base * (1 - rd[..., None]) + RED * rd[..., None]
        base[:] = base * (1 - nv[..., None] * .92) + NAVY * nv[..., None] * .92
    else:
        base = sub
    if color_mix > 0:
        # real colour, with paper-coloured background keyed by brightness similarity
        bgd = np.abs(a - PAPER).sum(2) < 40
        colr = np.where(bgd[..., None], sub, a)
        sub[:] = base * (1 - color_mix) + colr * color_mix
    else:
        sub[:] = base

_DG = {}
def _dotgrid(Y0, X0, hh, ww):
    yy_, xx_ = np.mgrid[Y0:Y0 + hh, X0:X0 + ww].astype(np.float32)
    u = (xx_ + yy_) / np.sqrt(2); v = (xx_ - yy_) / np.sqrt(2)
    return np.sqrt(((u % 6) - 3) ** 2 + ((v % 6) - 3) ** 2) / (6 * .7071)

def flash(c, t, t0, dur=.07, col=RED, a=.30):
    if t0 <= t < t0 + dur: c[PY0:PY1, PX0:PX1] = c[PY0:PY1, PX0:PX1] * (1 - a) + col * a

def shake_off(t, t0, amp=8, dur=.27):
    if not (t0 <= t < t0 + dur): return 0, 0
    k = math.exp(-(t - t0) / (dur / 3)); return amp * k * math.sin(90 * (t - t0)), amp * k * math.cos(77 * (t - t0))

