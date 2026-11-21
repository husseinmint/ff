"""مقطع عرضي – EP03 الفشار – style v3 (layered collage on riso plate)."""
import sys; sys.path.insert(0, '../ep01_cattongue')
from m3 import *
import m3, subprocess, re, random
from scipy import ndimage as ndi

HERE3 = os.path.dirname(os.path.abspath(__file__))
def P(n): return os.path.join(HERE3, n)

# ------------------------------------------------------------------ voice segments
SEG_T = [(0.00,0.87),(1.15,2.75),(3.08,3.71),(3.99,5.61),(5.92,8.51),(8.80,10.33),(10.60,12.69),(12.98,14.22),(14.42,16.27),
 (16.60,17.27),(17.48,19.18),(19.36,20.52),(20.75,22.23),(22.52,22.98),(23.28,26.06),(26.32,28.61),(28.85,30.81),(31.03,31.89),
 (32.14,33.95),(34.12,35.04),(35.29,37.38),(37.62,38.18),(38.46,41.04),(41.38,42.00),(42.32,44.27),(44.50,46.34),(46.53,47.89),
 (48.10,51.24),(51.59,52.09),(52.38,55.29),(55.55,58.23),(58.41,59.12),(59.36,62.56),(62.92,64.67),(64.94,67.31),(67.52,69.13),
 (69.42,69.76),(70.00,71.17),(71.37,72.74),(73.08,74.78)]
SEG_X = ['هذه الطقّة…','ليست صوت تشقّق القشرة!','والقفزة…','ليست من قوة الانفجار!','اضغط لايك… ولنقطع حبة الفشار معًا.',
 'للحبة قشرة صلبة،','لا يكاد يعبرها الماء أو البخار.','وفي داخلها نشا،','فيه قليل من الماء المحبوس.','نسخّنها…',
 'فيتحول الماء إلى بخار،','ولا يجد مخرجًا.','فيرتفع الضغط داخلها…','إلى كم؟','إلى نحو تسعة أضعاف ضغط الهواء حولنا!',
 'ويلين النشا… حتى يصير كالعجين.','وعند نحو مئة وثمانين درجة…','تنشقّ القشرة!','يندفع النشا رغوةً بيضاء،','ثم يتصلّب…',
 'كل ذلك أسرع من رمشة عين.','وحجمها؟','قد يصير أكبر من الحبة بأربعين مرة.','أما القفزة؟','يخرج من النشا جزء كالساق…',
 'يصطدم بالمقلاة، وينضغط،','ثم يرتدّ كالنابض.','فتقفز الحبة وتدور في الهواء… كلاعب جمباز.','والطقّة؟',
 'رصدها باحثان في فرنسا بكاميرا فائقة السرعة.','فوجدا أن الصوت لا يأتي مع تشقّق القشرة…','بل بعده.',
 'ويرجّحان أنه صوت البخار المحبوس وهو يهرب!','وتلك الحبات العنيدة في القاع؟','قشرة معيبة يتسرّب منها البخار…',
 'أو ماء لا يكفي للضغط.','إذن،','كل حبة فشار…','طنجرة ضغط صغيرة.','فتذكّر في المرة القادمة…']
SEG = [(a, b, x) for (a, b), x in zip(SEG_T, SEG_X)]
DUR = 75.0

WT = []; cid = 0
for s, e, txt in SEG:
    ws = txt.split(); n = len(ws); k = max(1, math.ceil(n / 4)); per = math.ceil(n / k)
    L = [len(w.strip('،…!؟:.')) + 1.5 for w in ws]; tot = sum(L); t = s
    grp = [i // per for i in range(n)]
    for i in range(n - 1):
        if grp[i] != grp[i + 1] and ws[i] in ('في', 'من', 'إلى', 'حتى', 'مع', 'عن', 'على'): grp[i] = grp[i + 1]
    for i, w in enumerate(ws):
        d = (e - s) * L[i] / tot; WT.append((w, t, t + d, cid + grp[i])); t += d
    cid += k
CH = {}
for i, (w, a, b, c) in enumerate(WT): CH.setdefault(c, []).append(i)
def cap_at(t):
    cur = None
    for c, ids in CH.items():
        if WT[ids[0]][1] - .05 <= t <= WT[ids[-1]][2] + .35: cur = c
    if cur is None: return None
    ids = CH[cur]; act = -1
    for j, i in enumerate(ids):
        if WT[i][1] <= t < WT[i][2] + .02: act = j
    return [WT[i][0] for i in ids], act

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

# ---- kernel family at a fixed working width: bubbles grow from their centres
KW = 520
_K = {}
def _kprep():
    if _K: return
    k1 = rs(A('A1_kernel'), KW); k3 = rs(A('A3_bubbles'), KW).resize(k1.size, Image.LANCZOS)
    a1 = np.asarray(k1).astype(np.float32); a3 = np.asarray(k3).astype(np.float32)
    rm = red_mask(k3); rm = ndi.binary_opening(rm, iterations=1)
    D = ndi.distance_transform_edt(rm); R = ndi.maximum_filter(D, size=31)
    G = np.where(rm, D / np.maximum(R, 1), 0)
    # region of the bubble cluster (for the soft crossfade of surrounding hatching)
    zone = ndi.gaussian_filter(ndi.binary_dilation(rm, iterations=10).astype(np.float32), 4)
    _K.update(a1=a1, a3=a3, G=G, rm=rm, zone=zone)
def kernel_img(p):
    """p 0..1: water droplets (small) -> steam bubbles (full)."""
    _kprep(); p = round(clamp(p) * 40) / 40
    key = ('kern', p)
    if key in _RS: return _RS[key]
    a1, a3, G, rm, zone = _K['a1'], _K['a3'], _K['G'], _K['rm'], _K['zone']
    out = a1.copy()
    if p > 0:
        z = zone[..., None] * clamp((p - .4) / .5)
        out[..., :3] = a1[..., :3] * (1 - z) + a3[..., :3] * z
        vis = (G >= 1 - p * 1.0) & rm
        out[vis, :3] = a3[vis, :3]
        # where bubbles not yet grown inside the zone show cream (no stray red)
        notyet = rm & ~vis
        out[notyet, :3] = a1[notyet, :3] * (1 - clamp((p - .4) / .5)) + np.array([241, 234, 220]) * clamp((p - .4) / .5)
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA'); _RS[key] = im; return im

def crack_img():
    if 'crk' not in _RS:
        k1 = rs(A('A1_kernel'), KW); _RS['crk'] = A('A3B_crack').resize((int(KW * 1144 / 1052 * .96), int(k1.height * 1.0)), Image.LANCZOS)
    return _RS['crk']

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

# ------------------------------------------------------------------ geometry
AX, AY = W / 2, PY0 + 650          # art anchor (kernel centre)
CIRC = {}                            # filled per scene

def circle_state(t):
    """one back circle that persists and morphs: (cx,cy,r,col)."""
    keys = [(5.9, AX, AY, 0, NAVY), (6.3, AX, AY, 330, NAVY), (16.6, AX, AY, 330, NAVY), (17.0, AX, AY, 350, RED),
            (20.6, AX, AY, 350, RED), (21.0, 380, AY + 20, 270, RED), (26.2, 380, AY + 20, 270, RED), (26.6, AX, AY, 330, NAVY),
            (28.7, AX, AY, 330, NAVY), (29.1, 420, AY, 300, NAVY), (31.4, 420, AY, 300, NAVY), (31.6, AX, AY, 0, NAVY),
            (37.4, AX, AY, 0, RED), (37.9, AX + 60, AY - 60, 300, RED), (41.2, AX + 60, AY - 60, 300, RED), (41.5, AX, AY, 0, NAVY),
            (62.8, AX, AY, 0, NAVY), (64.8, AX, AY, 0, NAVY), (65.2, AX, AY, 330, RED), (69.3, AX, AY, 330, RED),
            (69.7, AX, AY, 360, NAVY), (74.2, AX, AY, 360, NAVY), (74.4, AX, AY, 0, NAVY)]
    if t < keys[0][0] or t > keys[-1][0]: return None
    for (t0, x0, y0, r0, c0), (t1, x1, y1, r1, c1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            q = eio((t - t0) / max(1e-3, t1 - t0));
            return x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, r0 + (r1 - r0) * q, c0 + (c1 - c0) * q
    return None

def breathe(t, t0, t1, a=1.0, b=1.04):
    return a + (b - a) * eio((t - t0) / max(.1, t1 - t0))

def enter(t, t0, d=.5):
    """spring entrance 0->1 with <=4% overshoot."""
    p = clamp((t - t0) / d)
    return 1 - math.exp(-7 * p) * math.cos(6 * p) if p < 1 else 1.0

# ------------------------------------------------------------------ scenes
CUTS = [8.65, 41.25, 51.45]          # red section-cut chapter openings
SCENES = []
def scene(t0):
    def deco(f): SCENES.append((t0, f)); return f
    return deco

@scene(0.0)
def s_hook(c, t):
    # colour photo of the burst, prints into halftone on «والقفزة»
    k = 1.0
    cm = 1 - clamp((t - 3.0) / .5)
    jump = 0
    if t > 3.08:
        q = clamp((t - 3.08) / .9); jump = -120 * math.sin(math.pi * q)
    z = 1.0 + .05 * clamp(t / 5.9)
    halftone_photo(c, 'img/P1_hook.jpg', W / 2, PY0 + PH / 2 + 60 + jump, PW * .98, PH * 1.0, k, z=z * 1.4, color_mix=cm)
    # «ليست صوت تشقّق القشرة» : red ring + strike on the hull
    if 1.15 <= t < 3.0:
        p = clamp((t - 1.3) / .45)
        hx, hy = W / 2 - 30, PY0 + PH / 2 + 330
        ring(c, hx, hy, 230, p, col=REDt, width=7, start=200)
        if t > 1.85:
            q = eoc((t - 1.85) / .2)
            def fn(d, im): d.line([(hx - 170, hy + 150), (hx - 170 + 340 * q, hy + 150 - 300 * q)], fill=REDt, width=9)
            draw_on(c, fn)
    if t > 3.08:
        ring(c, W / 2, PY0 + PH / 2 + 30 + jump, 360, clamp((t - 4.0) / .6), col=NAVYt, width=3)
    if t < 1.15: headline(c, 'لوحة ٠٣ · الفشار', 'هذه الطقّة…', 0.1, t, accent='الطقّة…')
    else: headline(c, 'لوحة ٠٣ · الفشار', 'ليست صوت القشرة' if t < 3.0 else 'ولا القفزة!', 1.15 if t < 3.0 else 3.08, t,
             accent='القشرة' if t < 3.0 else 'القفزة!')
    flash(c, t, 0.0, .07, PAPER, .5)

@scene(5.92)
def s_like(c, t):
    e = enter(t, 5.95)
    layer(c, 'A1_kernel', AX, AY + 40 * (1 - e), KW * (.92 + .08 * e) * breathe(t, 5.9, 8.6, 1, 1.03), alpha=clamp((t - 5.92) / .2))
    # like pill
    dt = t - 5.92; press = 1 - .12 * math.sin(math.pi * clamp((t - 6.5) / .3)); sc = press * eoc(dt / .3)
    if sc > 0:
        f = kufi(54, 'Black'); m = text_img('اضغط لايك', f, None, pad=30); h, w = m.shape
        bx, by = W / 2, PY0 + 150; rw, rh = int((w + 60) * sc), int((h + 10) * sc)
        pill = ((XX - bx) / (rw / 2)) ** 2 + ((YY - by) / (rh / 2)) ** 8 < 1
        c[pill] = RED; stamp(c, m, PAPER, bx, by, sc)
    if t > 7.15:   # «ولنقطع» – the red line cuts the kernel
        xl = PX1 - (PX1 - PX0) * eoc((t - 7.2) / .3); section_line(c, AY, PX1 + 10, xl)

@scene(8.80)
def s_anatomy(c, t):
    s = breathe(t, 8.8, 16.6, 1.0, 1.04)
    p = 0.0 if t < 14.42 else .5 * eoc((t - 14.5) / .9)
    layer(c, None, AX, AY + 20, KW * .9 * s, img=kernel_img(p))
    if t < 12.98:
        headline(c, 'لوحة ٠٣ · التشريح', 'قشرة صلبة', 8.85, t, accent='صلبة', out_t=12.75)
    else:
        headline(c, 'لوحة ٠٣ · التشريح', 'نشا… وماء محبوس', 13.0, t, accent='ماء')
    # tags: one at a time
    if 9.1 <= t < 12.9:
        tag(c, 'القشرة', (AX - KW * .47 * s - PX0) / PW, (AY - 120 - PY0) / PH, .16, .80, (t - 9.1) / .8, life=4)
    if 13.1 <= t < 14.4:
        tag(c, 'النشا', (AX - 60 - PX0) / PW, (AY - 120 - PY0) / PH, .18, .85, (t - 13.1) / .8, life=4)
    if 14.9 <= t < 16.6:
        tag(c, 'ماء', (AX + 95 - PX0) / PW, (AY + 60 - PY0) / PH, .84, .86, (t - 14.9) / .8, life=4)

@scene(16.60)
def s_heat(c, t):
    p = .5 + .5 * eoc((t - 17.6) / 1.6)
    jit = 0
    if t > 19.36: jit = 3 * math.sin(t * 47) * clamp((t - 19.36) / .3)
    layer(c, None, AX + jit, AY - 60, KW * .82 * breathe(t, 16.6, 20.75, 1, 1.03), img=kernel_img(p))
    # pan + flames rise in from the bottom
    e = enter(t, 16.7, .6)
    py = PY1 - 120 + 200 * (1 - e)
    pan = A('K1_pan')
    if True:
        im = rs(pan, 640, 'K1_pan')
        if int(t * 12) % 2 == 0: im = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_LEFT_RIGHT)
        flick = 1 + .015 * math.sin(t * 37)
        paste(c, rs(pan, 640 * flick, None), AX, py, alpha=clamp((t - 16.65) / .25))
    headline(c, 'لوحة ٠٣ · الحرارة', 'الماء يصير بخارًا', 17.5, t, accent='بخارًا')

@scene(20.75)
def s_pressure(c, t):
    kx, ky = 380, AY + 20
    shake = 0
    if t > 23.28: shake = 2.5 * math.sin(t * 61) * clamp((t - 23.3) / 1.8)
    layer(c, None, kx + shake, ky, KW * .72 * breathe(t, 20.75, 26.3, 1, 1.05), img=kernel_img(1.0))
    e = enter(t, 20.85, .55)
    gx, gy, gw = 790, AY + 30 + 160 * (1 - e), 330
    layer(c, 'G1_gauge', gx, gy, gw, alpha=clamp((t - 20.8) / .2))
    # needle
    gim_h = gw * 1880 / 1617
    cx_, cy_ = gx, gy - gim_h / 2 + gim_h * .474
    R = gw * .30
    prog = 0.0
    if t > 23.28: prog = eoc((t - 23.28) / 1.8)
    ang = -135 + 235 * prog + (6 * math.sin(clamp((t - 25.08) / .6) * math.pi * 2) * math.exp(-max(0, t - 25.08) * 4) if t > 25.08 else 0)
    ang += math.sin(t * 40) * (.5 + 2 * prog) * (1 if t > 23.28 else 0)
    a = math.radians(ang - 90)
    def fn(d, im):
        ex, ey = cx_ + R * math.cos(a), cy_ + R * math.sin(a)
        d.line([(cx_, cy_), (ex, ey)], fill=NAVYt, width=6)
        d.line([(cx_ + (ex - cx_) * .75, cy_ + (ey - cy_) * .75), (ex, ey)], fill=REDt, width=8)
        d.ellipse([cx_ - 14, cy_ - 14, cx_ + 14, cy_ + 14], fill=NAVYt)
    if t > 20.9: draw_on(c, fn)
    n = int(round(1 + 8 * prog)) if t > 23.28 else 1
    if t >= 22.52:
        headline(c, 'لوحة ٠٣ · الضغط', 'إلى كم؟' if t < 23.28 else 'تسعة أضعاف', 22.52 if t < 23.28 else 23.28, t, accent='كم؟' if t < 23.28 else 'تسعة')
    else:
        headline(c, 'لوحة ٠٣ · الضغط', 'يرتفع الضغط', 20.8, t, accent='الضغط')
    if t > 23.28:
        big_number(c, '×' + ar_num(n), gx, gy + gw * .62 + 40, 23.28, t, size=110)

@scene(26.32)
def s_dough(c, t):
    z = .92 * breathe(t, 26.32, 28.85, 1, 1.04)
    im = kernel_img(1.0)
    w = KW * z
    # wobble: displace the image slightly (dough)
    wob = 4 * math.sin(t * 9) * clamp((t - 26.5) / .5)
    paste(c, rs(im, w, None).transform(rs(im, w, None).size, Image.AFFINE, (1, .015 * math.sin(t * 7), 0, .012 * math.sin(t * 5), 1, wob), Image.BICUBIC), AX, AY + 20)
    headline(c, 'لوحة ٠٣ · النشا', 'يصير كالعجين', 26.4, t, accent='كالعجين')

@scene(28.85)
def s_temp(c, t):
    kx, ky = 430, AY + 10
    pulse = 1.0
    if t > 30.4: pulse = 1 + .03 * math.sin((t - 30.4) * 2 * math.pi * (6 + 10 * (t - 30.4)))
    if t < 31.03:
        layer(c, None, kx, ky, KW * .8 * pulse, img=kernel_img(1.0))
    else:
        im = crack_img(); paste(c, rs(im, KW * .8 * im.width / KW, None), kx, ky)
    # thermometer
    e = enter(t, 28.95, .55)
    th_h = 760; th_w = th_h * 411 / 2098; tx, ty = 830, AY + 10 + 140 * (1 - e)
    layer(c, 'T1_thermo', tx, ty, th_w, alpha=clamp((t - 28.9) / .2))
    q = (eoc((t - 29.2) / 1.6) ** 1.3) if t > 29.2 else 0
    top0 = ty - th_h / 2 + th_h * .76; top1 = ty - th_h / 2 + th_h * .14
    yt = top0 + (top1 - top0) * q
    cxr = tx - th_w / 2 + th_w * .49
    c[int(yt):int(top0) + 2, int(cxr - 6):int(cxr + 6)] = RED
    deg = int(round(20 + 160 * q))
    headline(c, 'لوحة ٠٣ · الحرارة', 'مئة وثمانون درجة' if t < 31.03 else 'تنشقّ القشرة!', 28.9 if t < 31.03 else 31.03, t,
             accent='درجة' if t < 31.03 else 'تنشقّ')
    if t > 29.2:
        big_number(c, ar_num(deg) + '°', kx, PY1 - 75, 29.2, t, size=96, col=NAVY if q < .98 else RED)
    flash(c, t, 31.03, .07, RED, .3)

DEBRIS = [(random.Random(i).uniform(-1, 1), random.Random(i + 99).uniform(-1.2, -.2), random.Random(i + 7).uniform(18, 30),
           random.Random(i + 3).uniform(-25, 25), random.Random(i + 5).uniform(26, 52)) for i in range(16)]
@scene(31.55)
def s_burst(c, t):
    dt = t - 31.55
    # sprite sequence – no crossfades
    if dt < .1:
        im, sc = crack_img(), .8 * 1144 / 1052
        paste(c, rs(im, KW * sc, None), AX, AY)
    elif t < 34.12:
        s = 1.0 + .45 * (1 - math.exp(-dt * 9)) - .15 * clamp((dt - .2) / .4)
        layer(c, 'A4_burst', AX, AY + 40, 470 * s * breathe(t, 32, 34.1, 1, 1.03))
    else:
        layer(c, 'F1_alt', AX, AY + 30, 480 * breathe(t, 34.1, 37.6, 1, 1.04))
    # debris from the hull
    if 0 <= dt < .9:
        for (vx, vy, sp, spin, sz) in DEBRIS:
            x = AX + vx * sp * dt * 30; y = AY + 60 + vy * sp * dt * 30 + .5 * 1300 * dt * dt
            a = 1 - clamp((dt - .5) / .4)
            w = int(sz); frag = A('A1_kernel').crop((200, 300, 200 + 140, 300 + 90)).resize((w, int(w * .6)))
            frag.putalpha(Image.fromarray((np.asarray(frag)[..., 3] * a).astype(np.uint8)))
            paste(c, frag, x, y, 1.0, rot=spin * dt * 30)
    # steam puffs
    if 0 <= dt < .8:
        for j, (ox, oy) in enumerate([(-120, -40), (130, -60), (-60, -160), (90, -190), (0, 80), (-170, 60)]):
            r = 30 + 80 * eoc(dt / .8) * (.6 + .1 * j); a = .5 * (1 - clamp(dt / .8))
            disc(c, AX + ox * (1 + dt), AY + oy * (1 + dt), r, RED, a * .5)
    if t < 34.12:
        headline(c, 'لوحة ٠٣ · الانفجار', 'رغوة بيضاء', 32.14, t, accent='رغوة')
    elif t < 35.29:
        headline(c, 'لوحة ٠٣ · الانفجار', 'ثم تتصلّب', 34.12, t, accent='تتصلّب')
    else:
        headline(c, 'لوحة ٠٣ · السرعة', 'أسرع من رمشة عين', 35.29, t, accent='رمشة')
    flash(c, t, 31.55, .07, RED, .3)

@scene(37.62)
def s_x40(c, t):
    dt = t - 37.62
    sx, sy = 250, AY + 220
    layer(c, 'A1_kernel', sx, sy, 130 if t < 38.6 else 70)
    # 40 small kernels fly into the flake; the flake prints in step
    n = 0
    t0 = 38.6
    for i in range(40):
        ti = t0 + i * .055
        if t < ti: continue
        q = clamp((t - ti) / .35)
        if q >= 1: n += 1; continue
        e = 1 - (1 - q) ** 3
        rr = random.Random(i)
        tx_, ty_ = AX + 60 + rr.uniform(-170, 170), AY - 60 + rr.uniform(-170, 150)
        x = sx + (tx_ - sx) * e; y = sy + (ty_ - sy) * e - 140 * math.sin(math.pi * e)
        layer(c, 'A1_kernel', x, y, 48)
    if n > 0: layer(c, 'F1_alt', AX + 60, AY - 60, 460 * (.25 + .75 * eoc(n / 40)))
    tdone = t0 + 39 * .055 + .35
    headline(c, 'لوحة ٠٣ · الحجم', 'وحجمها؟' if t < tdone else 'أربعون ضعفًا', 37.65 if t < tdone else tdone, t, accent='أربعون')
    if t > t0:
        big_number(c, '×' + ar_num(max(1, n)), AX + 250, PY1 - 90, t0, t, size=110)

PAN_W = 760
@scene(41.38)
def s_jump(c, t):
    panx, pany = AX, PY1 - 150
    layer(c, 'K1_pan', panx, pany, PAN_W)
    pan_h = PAN_W * 668 / 2068
    floor = pany - pan_h / 2 + pan_h * .30
    fw = 300
    fh = fw * 1568 / 1245
    if t < 44.5:
        e = enter(t, 41.5, .5)
        layer(c, 'F1_leg', panx - 40, floor - fh / 2 + 120 * (1 - e) * 0, fw, alpha=clamp((t - 41.45) / .2))
        if 42.4 < t < 44.4:
            tag(c, 'ساق من النشا', (panx - 40 + 10 - PX0) / PW, (floor - 60 - PY0) / PH, .78, .22, (t - 42.4) / .8, life=3)
    elif t < 46.53:
        sq = 1 - .06 * math.sin(math.pi * clamp((t - 44.5) / .25))
        layer(c, 'F1B_pressed', panx - 40, floor - fh * sq / 2, fw)
    elif t < 48.1:
        # coiled spring: slight squash wobble then release
        q = (t - 46.53)
        k = 1 - .05 * math.exp(-q * 3) * math.cos(q * 18)
        layer(c, 'F1B_pressed', panx - 40, floor - fh * k / 2, fw)
    else:
        q = clamp((t - 48.1) / 1.6)
        # time ramp: slow at the top
        qq = q + .18 * math.sin(2 * math.pi * q) / (2 * math.pi) * -1
        x0, y0 = panx - 40, floor - fh / 2
        x1 = x0 + 260
        X = x0 + (x1 - x0) * qq; Y = y0 - 400 * math.sin(math.pi * qq)
        rot = -400 * qq
        # trail
        for j, lag in enumerate([.06, .12, .18, .24]):
            qj = max(0, qq - lag)
            Xj = x0 + (x1 - x0) * qj; Yj = y0 - 400 * math.sin(math.pi * qj)
            if Yj < PY0 + 330: continue
            layer(c, 'F1_leg', Xj, Yj, fw * .9, alpha=.28 - j * .06, rot=-400 * qj)
        # dotted arc
        def fn(d, im):
            for i in range(0, int(60 * qq)):
                u = i / 60; ax_ = x0 + (x1 - x0) * u; ay_ = y0 - 400 * math.sin(math.pi * u)
                if i % 2 == 0: d.ellipse([ax_ - 4, ay_ - 4, ax_ + 4, ay_ + 4], fill=REDt)
        draw_on(c, fn)
        layer(c, 'F1_leg', X, Y, fw, rot=rot)
        if t > 49.6:
            layer(c, 'J1_acrobat', PX0 + 190, PY0 + 430, 250, alpha=clamp((t - 49.6) / .4) * .95)
    if t < 44.5:
        headline(c, 'لوحة ٠٣ · القفزة', 'ساق من النشا', 41.4, t, accent='ساق')
    elif t < 48.1:
        headline(c, 'لوحة ٠٣ · القفزة', 'تنضغط… وترتدّ', 44.5, t, accent='وترتدّ')
    else:
        headline(c, 'لوحة ٠٣ · القفزة', 'كلاعب جمباز', 48.1, t, accent='جمباز')

FR = ['A1_kernel', 'A3B_crack', 'A4_burst', 'F1_alt']
@scene(51.59)
def s_sound(c, t):
    headline(c, 'لوحة ٠٣ · الصوت', 'والطقّة؟' if t < 52.38 else ('كاميرا فائقة السرعة' if t < 55.55 else 'الصوت يأتي بعدها'),
             51.6 if t < 52.38 else (52.38 if t < 55.55 else 55.55), t, accent='والطقّة؟' if t < 52.38 else ('السرعة' if t < 55.55 else 'بعدها'))
    # film strip of frames
    fy = AY - 40 + (PY0 + 380 - (AY - 40)) * eio((t - 55.1) / .5); fw = 190
    for i, n in enumerate(FR):
        ti = 51.75 + i * .2
        if t < ti: continue
        e = enter(t, ti, .4)
        fx = PX1 - 140 - i * 225
        lit = 55.55 <= t and ((t - 56.0) * 1.0 >= i * .45)
        c[int(fy - 115):int(fy + 115), int(fx - 105):int(fx + 105)] = c[int(fy - 115):int(fy + 115), int(fx - 105):int(fx + 105)] * .0 + (NAVY if lit else PAPER - 8)
        def fn(d, im, fx=fx):
            d.rectangle([fx - 105, fy - 115, fx + 105, fy + 115], outline=NAVYt, width=3)
            for k in range(6):
                d.rectangle([fx - 100 + k * 36, fy - 110, fx - 86 + k * 36, fy - 100], fill=PAPERt if lit else NAVYt)
                d.rectangle([fx - 100 + k * 36, fy + 100, fx - 86 + k * 36, fy + 110], fill=PAPERt if lit else NAVYt)
        draw_on(c, fn)
        layer(c, n, fx, fy + 30 * (1 - e), 150 if n != 'A4_burst' else 150)
    # timeline + waveform
    if t > 55.55:
        y0 = AY + 170; xL, xR = PX1 - 80, PX0 + 80     # RTL: time runs right -> left
        prog = clamp((t - 55.6) / 1.5)
        def fn2(d, im):
            d.line([(xL, y0 + 120), (xL + (xR - xL) * eoc((t - 55.55) / .4), y0 + 120)], fill=NAVYt, width=3)
            for k, lab in enumerate(['٠', '٥٠', '١٠٠', '١٥٠', '٢٠٠']):
                x = xL + (xR - xL) * k / 4
                d.line([(x, y0 + 112), (x, y0 + 128)], fill=NAVYt, width=3)
                d.text((x, y0 + 158), lab, font=kufi(34, 'SemiBold'), fill=NAVYt, anchor='mm', direction='rtl', language='ar')
            d.text((W / 2, y0 + 200), 'ملّي ثانية', font=kufi(32, 'SemiBold'), fill=NAVYt, anchor='mm', direction='rtl', language='ar')
            # waveform drawn up to playhead
            ph = xL + (xR - xL) * prog
            pts = []
            N = 220
            for i in range(N + 1):
                u = i / N; x = xL + (xR - xL) * u
                if (x - ph) * (xR - xL) > 0: break
                amp = 2 + 1.5 * math.sin(i * 1.7)
                if u > .5 and t > 58.41:
                    k_ = (u - .5) / .5; amp = 150 * math.exp(-k_ * 6) * abs(math.sin(i * 2.3)) + 2
                pts.append((x, y0 + 40 + amp * (1 if i % 2 else -1)))
            if len(pts) > 1: d.line(pts, fill=NAVYt, width=3)
            # crack marker at 0
            if t > 56.4:
                d.line([(xL, y0 - 70), (xL, y0 + 110)], fill=NAVYt, width=3)
                d.text((xL, y0 - 95), 'انكسار', font=kufi(42, 'Bold'), fill=NAVYt, anchor='mm', direction='rtl', language='ar')
            if t > 58.41:
                xm = xL + (xR - xL) * .5
                d.line([(xm, y0 - 120), (xm, y0 + 110)], fill=REDt, width=5)
                d.text((xm, y0 - 145), 'الطقّة', font=kufi(46, 'Black'), fill=REDt, anchor='mm', direction='rtl', language='ar')
                if t > 58.8:
                    q = eoc((t - 58.8) / .4)
                    d.line([(xL, y0 - 40), (xL + (xm - xL) * q, y0 - 40)], fill=REDt, width=4)
                    if q > .9: d.text(((xL + xm) / 2, y0 + 2), '١٠٠ ملّي ثانية', font=kufi(40, 'Bold'), fill=REDt, anchor='mm', direction='rtl', language='ar')
            d.line([(ph, y0 - 30), (ph, y0 + 110)], fill=REDt if prog < 1 else NAVYt, width=2)
        draw_on(c, fn2)
    if t > 59.36:
        # steam escaping – the kernel with steam jets in the last film frame lights up
        pass
    flash(c, t, 58.41, .07, RED, .3)

@scene(62.92)
def s_duds(c, t):
    if t < 64.94:
        k = eoc((t - 62.95) / .6)
        halftone_photo(c, 'img/P2_bowl.jpg', AX, AY - 20, PW * .95, PH * .95, k, z=1.3 * breathe(t, 62.9, 64.9, 1, 1.12), magenta=True)
        headline(c, 'لوحة ٠٣ · الحبات العنيدة', 'الحبات العنيدة', 62.95, t, accent='العنيدة')
    elif t < 67.52:
        e = enter(t, 64.95, .5)
        layer(c, 'A15_leak', AX, AY + 30 * (1 - e), 520 * breathe(t, 64.94, 67.5, 1, 1.04))
        headline(c, 'لوحة ٠٣ · الحبات العنيدة', 'قشرة معيبة', 64.95, t, accent='معيبة')
    else:
        p = 1 - .75 * eoc((t - 67.6) / 1.2)
        layer(c, None, AX, AY, KW * breathe(t, 67.5, 69.4, 1, 1.03), img=kernel_img(p))
        headline(c, 'لوحة ٠٣ · الحبات العنيدة', 'ماء لا يكفي', 67.55, t, accent='يكفي')

@scene(69.42)
def s_outro(c, t):
    layer(c, None, AX - 110, AY + 30, KW * .78 * breathe(t, 69.4, 74.3, 1, 1.04), img=kernel_img(1.0))
    e = enter(t, 70.0, .55)
    gx = 835; gy = AY - 170 + 120 * (1 - e)
    layer(c, 'G1_gauge', gx, gy, 220, alpha=clamp((t - 70.0) / .2))
    gim_h = 220 * 1880 / 1617; cx_, cy_ = gx, gy - gim_h / 2 + gim_h * .474; R = 220 * .30
    ang = -135 + 235 * eoc((t - 70.3) / 1.0) + math.sin(t * 40) * 2
    a = math.radians(ang - 90)
    def fn(d, im):
        ex, ey = cx_ + R * math.cos(a), cy_ + R * math.sin(a)
        d.line([(cx_, cy_), (ex, ey)], fill=NAVYt, width=5); d.line([(cx_ + (ex - cx_) * .7, cy_ + (ey - cy_) * .7), (ex, ey)], fill=REDt, width=7)
        d.ellipse([cx_ - 11, cy_ - 11, cx_ + 11, cy_ + 11], fill=NAVYt)
    if t > 70.0: draw_on(c, fn)
    headline(c, 'لوحة ٠٣ · الخلاصة', 'طنجرة ضغط صغيرة', 70.0, t, accent='ضغط')

@scene(74.30)
def s_loop(c, t):
    halftone_photo(c, 'img/P1_hook.jpg', W / 2, PY0 + PH / 2 + 60, PW * .98, PH, 1.0, z=1.4, color_mix=clamp((t - 74.3) / .25))

# ------------------------------------------------------------------ frame
SC_T = [s[0] for s in SCENES]
def scene_at(t):
    i = max(j for j, s in enumerate(SCENES) if s[0] <= t + 1e-6); return i, SCENES[i]

def plate_render(i, t):
    c = paper_canvas()
    cs = circle_state(t)
    if cs and cs[2] > 1: disc(c, cs[0], cs[1], cs[2], cs[3])
    if cs and cs[2] > 30 and SCENES[i][1].__name__ not in ('s_hook', 's_loop', 's_duds'):
        ring(c, cs[0], cs[1], cs[2] + 46, clamp((t - SCENES[i][0]) / .8), col=NAVYt, width=2, start=-90)
    SCENES[i][1](c, t)
    return c

def frame(t):
    i, (t0, fn) = scene_at(t)
    c = plate_render(i, t)
    # drift-dissolve from previous scene (default transition) – 10 frames
    TD = .33
    if i > 0 and t - t0 < TD and not any(abs(t0 - x) < .3 for x in CUTS) and fn.__name__ not in ('s_burst', 's_loop'):
        prev = plate_render(i - 1, t0 - .001)
        q = (t - t0) / TD; off = int(30 * eio(q))
        pv = prev[PY0:PY1, PX0:PX1]; pv = np.roll(pv, -off, 0)
        c[PY0:PY1, PX0:PX1] = pv * (1 - eio(q)) + c[PY0:PY1, PX0:PX1] * eio(q)
    # red section-cut chapter openings
    for tc in CUTS:
        if tc - .27 <= t < tc + .45:
            j = max(k for k, s in enumerate(SCENES) if s[0] <= tc - .3)
            if t < tc:
                xl = PX1 - (PX1 - PX0) * eio((t - (tc - .27)) / .27)
                section_line(c, PY0 + PH // 2, PX1 + 10, xl)
            else:
                old = plate_render(j, tc - .3)[PY0:PY1, PX0:PX1]
                q = eio(clamp((t - tc) / .43)); sh = int(PH * .55 * q); mid = PH // 2
                comp = c[PY0:PY1, PX0:PX1].copy()
                y1 = mid - sh
                if y1 > 0: comp[:y1] = old[:mid][mid - y1:]
                y2 = mid + sh
                if y2 < PH: comp[y2:] = old[mid:][:PH - y2]
                c[PY0:PY1, PX0:PX1] = comp
                if q < 1: section_line(c, PY0 + PH // 2, PX1 + 10, PX0 - 10)
    dx, dy = 0, 0
    for tt in (31.55, 58.41):
        ox, oy = shake_off(t, tt); dx += ox; dy += oy
    if dx or dy:
        c[PY0:PY1, PX0:PX1] = np.roll(np.roll(c[PY0:PY1, PX0:PX1], int(dy), 0), int(dx), 1)
    chrome(c, t, '٠٣', 'الفشار')
    pw = int(PW * t / DUR); c[PY1 + 10:PY1 + 16, PX1 - pw:PX1] = RED
    cp = cap_at(t)
    if cp: caption(c, *cp)
    return np.clip(c, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'stills':
        ts = [float(x) for x in sys.argv[2].split(',')]
        ims = [Image.fromarray(frame(t)) for t in ts]
        cols = 6; th = [im.resize((360, 640)) for im in ims]
        rows = (len(th) + cols - 1) // cols; sheet = Image.new('RGB', (cols * 360, rows * 640), 'white')
        for j, im in enumerate(th): sheet.paste(im, ((j % cols) * 360, (j // cols) * 640))
        sheet.save(sys.argv[3], quality=85)
    elif mode == 'one':
        Image.fromarray(frame(float(sys.argv[2]))).save(sys.argv[3])
    elif mode == 'video':
        a, b, out = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for f in range(int(round((b - a) * FPS))): p.stdin.write(frame(a + f / FPS).tobytes())
        p.stdin.close(); p.wait()
