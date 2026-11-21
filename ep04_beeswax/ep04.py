"""مقطع عرضي – EP04 شمع النحل – style v3."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _helpers import *

GEO = json.load(open(P('geom.json')))
GL = sorted(GEO['B2_glands'], key=lambda p: p[0])[:8]
CELLS = []
for p in GEO['cells']:
    if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > .05 for q in CELLS): CELLS.append(p)

# ------------------------------------------------------------------ voice
SEG_T = [(0,1.29),(1.53,2.56),(2.83,3.74),(3.96,5.27),(5.59,6.24),(6.40,7.88),(8.15,9.57),(9.74,11.18),(11.44,12.38),(12.60,15.27),
 (15.46,17.04),(17.24,18.27),(18.56,20.17),(20.33,21.91),(22.10,23.57),(23.86,25.70),(25.95,26.96),(27.23,28.03),(28.27,29.58),(29.87,30.73),
 (30.94,35.66),(35.94,39.13),(39.39,41.04),(41.30,42.31),(42.55,43.85),(44.01,45.28),(45.53,49.33),(49.53,51.70),(51.89,58.04),(58.27,62.26),
 (62.47,63.76),(64.04,64.57),(64.76,65.80),(66.07,69.29),(69.47,70.88),(71.09,74.16),(74.41,74.86),(75.03,76.27),(76.48,77.50),(77.75,80.33),(80.51,81.19)]
SEG_X = ['هذه السداسيّات…','وُلدت دوائر!','والشمع نفسه…','خرج من بطن نحلة.','اضغط لايك…','ولنقطع نحلةً معًا.','تحت بطن النحلة العاملة…',
 'ثماني غدد للشمع.','تفرز سائلًا…','يتصلّب على صفائح لامعة كالمرآة.','فيصير قشورًا بيضاء…','أرقّ من ورقة.','تلتقطها النحلة بساقها،',
 'وتمرّرها حتى فمها…','ثم تمضغها لتلين.','وكم قشرةً في غرام واحد؟','أكثر من ألف!','وفي الكيلوغرام؟','نحو مليون قشرة.','والثمن أغلى:',
 'لصنع كيلوغرام من الشمع… يستهلك النحل نحو ثمانية كيلوغرامات من العسل.','فلماذا يرمي بعضنا هذا الشمع… ويأكله آخرون؟','سنحسم الخلاف بعد قليل.',
 'أما السداسيّات؟','تبني النحلات الخلايا…','دوائر متلاصقة.','ثم تسخّنها بأجسامها… حتى نحو خمس وأربعين درجة.','فيلين الشمع وينساب ببطء.',
 'ويرجّح باحثون أن الجدران تنشدّ وحدها… فتصير سداسية، كفقاعات صابون متلاصقة.','والمدهش: السداسيّ يقسم المساحة بأقصر جدران ممكنة… أي بأقل شمع.',
 'والآن… هل يُؤكل الشمع؟','نعم،','إنه آمن،','وتُلمَّع به بعض الحلوى باسم:','إي تسعمئة وواحد.','لكن جسمك لا يكاد يهضمه… فلا غذاء فيه.',
 'وأنت…','تأكله أم ترميه؟','اكتب في التعليقات.','وفي المرة القادمة التي ترى فيها قرص عسل…','تذكّر:']
SEG = [(a, b, x) for (a, b), x in zip(SEG_T, SEG_X)]
DUR = 81.6
WT = []; cid = 0
for s, e, txt in SEG:
    ws = txt.split(); n = len(ws); k = max(1, math.ceil(n / 4)); per = math.ceil(n / k)
    L = [len(w.strip('،…!؟:.')) + 1.5 for w in ws]; tot = sum(L); t = s
    grp = [i // per for i in range(n)]
    for i in range(n - 1):
        if grp[i] != grp[i + 1] and ws[i] in ('في', 'من', 'إلى', 'حتى', 'مع', 'عن', 'على', 'أن', 'لا', 'التي'): grp[i] = grp[i + 1]
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

# ------------------------------------------------------------------ helpers
AX, AY = W / 2, PY0 + 640
def breathe(t, t0, t1, a=1.0, b=1.04): return a + (b - a) * eio((t - t0) / max(.1, t1 - t0))
def enter(t, t0, d=.5):
    p = clamp((t - t0) / d); return 1 - math.exp(-7 * p) * math.cos(6 * p) if p < 1 else 1.0
BEE_W = 1544 / 2048            # bee bbox fraction of the canvas
def bee(c, n, cx, cy, w, alpha=1.0, rot=0.0):
    """draw bee image n so the BEE is w px wide, canvas centred on (cx,cy)."""
    layer(c, n, cx, cy, w / BEE_W, alpha, rot)
def bee_pt(fx, fy, cx, cy, w):
    Wc = w / BEE_W; return cx + (fx - .5) * Wc, cy + (fy - .5) * Wc

def bubble(c, txt, cx, cy, p, col=NAVY, tail=1):
    if p <= 0: return
    f = kufi(62, 'Bold'); m = text_img(txt, f, None, pad=26); h, w = m.shape; sc = .85 + .15 * enter(p, 0, 1)
    bw, bh = (w + 40) * sc, (h + 10) * sc
    def fn(d, im):
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], radius=28, fill=PAPERt, outline=tuple(int(v) for v in col), width=4)
        d.polygon([(cx + 30 * tail, cy + bh / 2 - 2), (cx + 60 * tail, cy + bh / 2 + 34), (cx + 70 * tail, cy + bh / 2 - 2)], fill=PAPERt, outline=tuple(int(v) for v in col))
    draw_on(c, fn); stamp(c, m, col, cx, cy, sc)

def hexpts(cx, cy, R, q, rr):
    pts = []
    for i in range(72):
        a = 2 * math.pi * i / 72
        # hexagon radius in direction a (flat-top)
        k = math.pi / 3; aa = (a % k) - k / 2
        rh = R * math.cos(math.pi / 6) / math.cos(aa)
        r = rr + (rh - rr) * q
        pts.append((cx + r * math.cos(a + math.pi / 6), cy + r * math.sin(a + math.pi / 6)))
    return pts

def circle_state(t):
    keys = [(2.7, AX, AY, 0, NAVY), (3.1, AX, AY, 340, NAVY), (8.0, AX, AY, 340, NAVY), (8.4, AX + 40, AY + 20, 360, NAVY), (18.4, AX + 40, AY + 20, 360, NAVY),
            (18.8, AX, AY, 340, NAVY), (23.7, AX, AY, 340, NAVY), (24.0, AX, AY, 0, NAVY),
            (41.2, AX, AY, 0, NAVY), (41.5, AX, AY, 380, NAVY), (45.3, AX, AY, 380, NAVY), (45.6, AX, AY, 0, NAVY),
            (51.7, AX, AY, 0, NAVY), (52.1, AX, AY, 380, RED), (58.1, AX, AY, 380, RED), (58.4, AX, AY, 0, RED),
            (71.0, AX, AY, 0, RED), (71.3, AX, AY + 20, 340, RED), (74.3, AX, AY + 20, 340, RED), (74.6, AX, AY, 0, RED),
            (77.6, AX, AY, 0, NAVY), (78.0, AX, AY, 380, NAVY), (80.9, AX, AY, 380, NAVY), (81.05, AX, AY, 0, NAVY)]
    if t < keys[0][0] or t > keys[-1][0]: return None
    for (t0, x0, y0, r0, c0), (t1, x1, y1, r1, c1) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            q = eio((t - t0) / max(1e-3, t1 - t0)); return x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, r0 + (r1 - r0) * q, c0 + (c1 - c0) * q

def comb(c, n, cx, cy, w, alpha=1.0): layer(c, n, cx, cy, w, alpha)
def cell_xy(p, cx, cy, w): return cx + (p[0] - .5) * w, cy + (p[1] - .5) * w

# ------------------------------------------------------------------ scenes
CUTS = [8.0, 41.15, 62.32]
SCENES = []
def scene(t0):
    def deco(f): SCENES.append((t0, f)); return f
    return deco

@scene(0.0)
def s_hook(c, t):
    if t < 1.53:
        halftone_photo(c, 'img/P1_hook.jpg', W / 2, PY0 + PH / 2 + 40, PW * .98, PH, 1.0, z=1.35 * (1 + .03 * t), color_mix=1.0)
        headline(c, 'لوحة ٠٤ · الشمع', 'هذه السداسيّات…', 0.1, t, accent='السداسيّات…')
    else:
        # engraving: hexagons morph back into circles («وُلدت دوائر»)
        q = eio((t - 1.6) / .8)
        cw = 800
        comb(c, 'H2_hex', AX, AY + 10, cw, 1 - q)
        comb(c, 'H1_circles', AX, AY + 10, cw, q)
        R = .0925 * cw; rr = .062 * cw
        def fn(d, im):
            for p in CELLS:
                x, y = cell_xy(p, AX, AY + 10, cw)
                d.line(hexpts(x, y, R, 1 - q, rr) + [hexpts(x, y, R, 1 - q, rr)[0]], fill=REDt if q > .05 else NAVYt, width=4)
        if q < 1: draw_on(c, fn)
        headline(c, 'لوحة ٠٤ · الشمع', 'وُلدت دوائر!', 1.53, t, accent='دوائر!')
        flash(c, t, 1.53, .07, RED, .3)

@scene(2.83)
def s_bee(c, t):
    e = enter(t, 2.85)
    w = 600 * breathe(t, 2.8, 8.0, 1, 1.03)
    bee(c, 'B1_bee', AX, AY + 40 * (1 - e), w, alpha=clamp((t - 2.83) / .2))
    if t > 3.96:
        bee(c, 'B3_scales', AX, AY, w, alpha=clamp((t - 3.96) / .3))
    if t < 5.59:
        headline(c, 'لوحة ٠٤ · الشمع', 'خرج من بطن نحلة' if t > 3.96 else 'والشمع نفسه…', 3.96 if t > 3.96 else 2.85, t, accent='بطن' if t > 3.96 else 'الشمع')
    dt = t - 5.59; press = 1 - .12 * math.sin(math.pi * clamp((t - 6.0) / .3)); sc = press * eoc(dt / .3)
    if sc > 0:
        f = kufi(54, 'Black'); m = text_img('اضغط لايك', f, None, pad=30); h, ww = m.shape
        bx, by = W / 2, PY0 + 150; rw, rh = int((ww + 60) * sc), int((h + 10) * sc)
        pill = ((XX - bx) / (rw / 2)) ** 2 + ((YY - by) / (rh / 2)) ** 8 < 1
        c[pill] = RED; stamp(c, m, PAPER, bx, by, sc)
    if t > 6.6:
        xl = PX1 - 20 - (PX1 - PX0 - 40) * eoc((t - 6.65) / .3); section_line(c, AY, PX1 - 20, xl)

BW = 640
@scene(8.15)
def s_glands(c, t):
    cx, cy = AX + 40, AY + 20
    w = BW * breathe(t, 8.15, 15.46, 1, 1.03)
    bee(c, 'B1_bee', cx, cy, w)
    bee(c, 'B2_glands', cx, cy, w, alpha=clamp((t - 9.6) / .35))
    # pulse ring on each gland, ticking ١..٨
    n = 0
    for i, (fx, fy) in enumerate(GL):
        ti = 9.8 + i * .17
        if t >= ti:
            n += 1; q = (t - ti) / .5
            if q < 1:
                x, y = bee_pt(fx, fy, cx, cy, w)
                def fn(d, im, x=x, y=y, q=q):
                    r = 14 + 26 * q; a = int(255 * (1 - q))
                    d.ellipse([x - r, y - r, x + r, y + r], outline=REDt, width=4)
                draw_on(c, fn)
    if t >= 9.8:
        big_number(c, ar_num(max(1, n)), PX1 - 150, PY1 - 150, 9.8, t, size=140)
    if t < 11.44:
        headline(c, 'لوحة ٠٤ · الغدد', 'ثماني غدد للشمع' if t > 9.74 else 'تحت بطن النحلة', 9.74 if t > 9.74 else 8.2, t, accent='ثماني' if t > 9.74 else 'بطن')
    else:
        headline(c, 'لوحة ٠٤ · الغدد', 'صفائح كالمرآة', 11.44, t, accent='كالمرآة')
        if t > 12.7:
            fx, fy = GL[3]; x, y = bee_pt(fx, fy, cx, cy, w)
            tag(c, 'مرآة الشمع', (x - PX0) / PW, (y - PY0) / PH, .30, .84, (t - 12.7) / .8, life=4)

@scene(15.46)
def s_scales(c, t):
    cx, cy = AX + 40, AY + 20
    w = BW * breathe(t, 15.46, 18.56, 1.0, 1.04)
    bee(c, 'B2_glands', cx, cy, w)
    bee(c, 'B3_scales', cx, cy, w, alpha=eoc((t - 15.5) / .6))
    # one scale floats out, enlarged, beside a «paper» edge
    if t > 17.0:
        e = enter(t, 17.05, .55)
        layer(c, 'S1_scale', PX0 + 200, PY1 - 210 + 60 * (1 - e), 230, alpha=clamp((t - 17.0) / .2), rot=-12)
        def fn(d, im):
            x0, y = PX0 + 90, PY1 - 90
            d.line([(x0, y), (x0 + 220 * eoc((t - 17.3) / .4), y)], fill=NAVYt, width=3)
        draw_on(c, fn)
    headline(c, 'لوحة ٠٤ · القشور', 'قشور بيضاء' if t < 17.24 else 'أرقّ من ورقة', 15.5 if t < 17.24 else 17.24, t, accent='قشور' if t < 17.24 else 'أرقّ')

PATH = [(0.60, 0.61), (0.52, 0.66), (0.42, 0.68), (0.32, 0.67), (0.23, 0.64)]
def path_pt(u):
    u = clamp(u) * (len(PATH) - 1); i = min(int(u), len(PATH) - 2); f = u - i
    (x0, y0), (x1, y1) = PATH[i], PATH[i + 1]; return x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
@scene(18.56)
def s_relay(c, t):
    cx, cy = AX + 30, AY + 10; w = 700
    if t < 20.33: bee(c, 'B4_leg', cx, cy, w)
    else: bee(c, 'B5_mouth', cx, cy, w)
    # dotted path + travelling scale
    if 19.2 < t < 22.1:
        u = eio((t - 19.4) / 2.2)
        def fn(d, im):
            for k in range(0, int(u * 40) + 1):
                fx, fy = path_pt(k / 40); x, y = bee_pt(fx, fy + .06, cx, cy, w)
                if k % 2 == 0: d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=REDt)
        draw_on(c, fn)
        fx, fy = path_pt(u); x, y = bee_pt(fx, fy + .06, cx, cy, w)
        layer(c, 'S1_scale', x, y + 40, 70, rot=120 * u)
        ring(c, x, y + 40, 46, 1, col=REDt, width=3)
    if t > 22.1:   # chewing wobble
        fx, fy = GEO['B5_mouth'][0]; x, y = bee_pt(fx, fy, cx, cy, w)
        for k in range(3):
            q = ((t - 22.1) * 3 - k * .3) % 1
            r = 20 + 50 * q
            def fn2(d, im, r=r, q=q):
                d.arc([x - r, y - r, x + r, y + r], -60, 60, fill=REDt, width=3)
            if q < .9: draw_on(c, fn2)
    if t < 20.33: headline(c, 'لوحة ٠٤ · الرحلة', 'بساقها…', 18.6, t, accent='بساقها…')
    elif t < 22.1: headline(c, 'لوحة ٠٤ · الرحلة', 'حتى فمها', 20.35, t, accent='فمها')
    else: headline(c, 'لوحة ٠٤ · الرحلة', 'تمضغها لتلين', 22.1, t, accent='تمضغها')

RAIN = [(random.Random(i).uniform(-60, 60), random.Random(i + 50).uniform(0, 1), random.Random(i + 9).uniform(14, 24), random.Random(i + 3).uniform(-200, 200)) for i in range(140)]
@scene(23.86)
def s_count(c, t):
    bx, by, bw = AX, AY - 10, 720
    # tilt beam slightly by count
    k = clamp((t - 25.95) / 1.0)
    layer(c, 'BAL_balance', bx, by, bw)
    # gram weight on left pan, scales piling on right pan
    lpx, rpx, pany = bx - bw * .3, bx + bw * .3, by + bw * .21
    e = enter(t, 24.2, .45)
    layer(c, 'W1_weight', lpx, pany - 60 - 80 * (1 - e), 70, alpha=clamp((t - 24.15) / .15))
    n = 0
    for i, (dx, ph, sz, spin) in enumerate(RAIN):
        ti = 25.95 + ph * 1.0
        if t < ti: continue
        q = clamp((t - ti) / .45); n += 1
        y0, y1 = PY0 + 260, pany - 30 - (i % 7) * 3 - (i // 35) * 8
        y = y0 + (y1 - y0) * q * q
        big = 1 + 1.5 * eoc((t - 28.27) / .4) if t > 28.27 else 1
        layer(c, 'S1_scale', rpx + dx * (.4 + .6 * q) * big, y - (big - 1) * (i % 9) * 6, sz * min(big, 1.6), rot=spin * q)
    cnt = int(round(1100 * eoc((t - 25.95) / 1.0))) if t > 25.95 else 0
    if t < 25.95:
        headline(c, 'لوحة ٠٤ · العدد', 'كم قشرة في غرام؟', 23.9, t, accent='غرام؟')
    elif t < 27.23:
        headline(c, 'لوحة ٠٤ · العدد', 'أكثر من ألف!', 25.95, t, accent='ألف!')
        big_number(c, ar_num(cnt), AX, PY1 - 75, 25.95, t, size=110)
    else:
        headline(c, 'لوحة ٠٤ · العدد', 'نحو مليون قشرة' if t > 28.27 else 'وفي الكيلوغرام؟', 28.27 if t > 28.27 else 27.23, t, accent='مليون' if t > 28.27 else 'الكيلوغرام؟')
        if t > 28.27: big_number(c, 'مليون', AX, PY1 - 80, 28.27, t, size=120)
        else: big_number(c, ar_num(1100), AX, PY1 - 75, 25.95, t, size=110)

@scene(29.87)
def s_cost(c, t):
    headline(c, 'لوحة ٠٤ · الثمن', 'والثمن أغلى' if t < 30.94 else ('كيلو من الشمع…' if t < 33.0 else 'ثمانية كيلو عسل!'),
             29.9 if t < 30.94 else (30.94 if t < 33.0 else 33.0), t, accent='أغلى' if t < 30.94 else ('الشمع…' if t < 33.0 else 'ثمانية'))
    # wax at the top (1 kg) – the scale sprite stands in as the wax
    e = enter(t, 30.95, .5)
    wy = AY - 60 + (PY0 + 330 - (AY - 60)) * eio((t - 31.8) / .4)
    layer(c, 'X1_block', AX, wy, (340 - 120 * eio((t - 31.8) / .4)) * e if e > .02 else 4, alpha=clamp((t - 30.95) / .2))
    if t > 31.4: big_number(c, '١ كغ شمع', AX, wy + 150 - 10 * eio((t - 31.8) / .4), 31.4, t, size=64, col=NAVY)
    # 8 jars stamp in (4x2) on «ثمانية كيلوغرامات»
    n = 0
    for i in range(8):
        ti = 32.0 + i * .14
        if t < ti: continue
        n += 1; ee = enter(t, ti, .35)
        x = AX - 300 + (i % 4) * 200; y = AY + 20 + (i // 4) * 185
        layer(c, 'J1_jar', x, y - 30 * (1 - ee), 115)
    if n: big_number(c, ar_num(n) + ' كغ عسل', AX, PY1 - 60, 32.0, t, size=64, col=RED)
    flash(c, t, 34.6, .07, RED, .25)

@scene(35.94)
def s_debate(c, t):
    halftone_photo(c, 'img/P2_spoon.jpg', AX, AY + 40, PW * .95, PH * .9, eoc((t - 35.95) / .5), z=2.0)
    bubble(c, 'أرميه!', PX0 + 230, PY0 + 330, (t - 36.6) / .4, NAVY, tail=1)
    bubble(c, 'آكله!', PX1 - 230, PY0 + 470, (t - 37.9) / .4, RED, tail=-1)
    if t < 39.39: headline(c, 'لوحة ٠٤ · الخلاف', 'ترميه أم تأكله؟', 35.95, t, accent='تأكله؟')
    else: headline(c, 'لوحة ٠٤ · الخلاف', 'نحسمه بعد قليل', 39.4, t, accent='نحسمه')

CW = 820
@scene(41.30)
def s_cells(c, t):
    comb(c, 'H1_circles', AX, AY + 20, CW * breathe(t, 41.3, 45.53, 1, 1.03))
    s = breathe(t, 41.3, 45.53, 1, 1.03)
    def fn(d, im):
        for i, p in enumerate(sorted(CELLS, key=lambda p: (p[0] - .48) ** 2 + (p[1] - .48) ** 2)):
            q = clamp((t - 43.9 - i * .05) / .35)
            if q <= 0: continue
            x, y = cell_xy(p, AX, AY + 20, CW * s); r = .066 * CW * s
            d.arc([x - r, y - r, x + r, y + r], -90, -90 + 360 * q, fill=REDt, width=4)
    draw_on(c, fn)
    headline(c, 'لوحة ٠٤ · الخلايا', 'أما السداسيّات؟' if t < 44.01 else 'دوائر متلاصقة', 41.35 if t < 44.01 else 44.01, t, accent='السداسيّات؟' if t < 44.01 else 'دوائر')

@scene(45.53)
def s_heat(c, t):
    # chain of hanging bees (same generated bee, stacked) + thermometer
    for k in range(2):
        e = enter(t, 45.6 + k * .25, .5)
        bee(c, 'B6_hang', PX0 + 280 + k * 20, PY0 + 400 + k * 330 - 120 * (1 - e), 300, alpha=clamp((t - 45.6 - k * .25) / .2))
    th_h = 700; th_w = th_h * 411 / 2098; tx, ty = PX1 - 200, AY + 40
    layer(c, 'T1_thermo', tx, ty, th_w, alpha=clamp((t - 45.6) / .2))
    q = eoc((t - 46.6) / 2.4) if t > 46.6 else 0
    top0 = ty - th_h / 2 + th_h * .76; top1 = ty - th_h / 2 + th_h * .38
    yt = top0 + (top1 - top0) * q; cxr = tx - th_w / 2 + th_w * .49
    c[int(yt):int(top0) + 2, int(cxr - 6):int(cxr + 6)] = RED
    if t > 46.6: big_number(c, ar_num(int(round(20 + 25 * q))) + '°', tx - 160, PY1 - 140, 46.6, t, size=110, col=RED if q > .98 else NAVY)
    # warm comb glimpse
    if t > 49.53:
        a = clamp((t - 49.55) / .4)
        im = rs(A('H1_circles'), 380, 'H1s')
        wob = 3 * math.sin(t * 8)
        im2 = im.transform(im.size, Image.AFFINE, (1, .02 * math.sin(t * 5), 0, 0, 1, wob), Image.BICUBIC)
        paste(c, im2, AX + 40, AY + 120, alpha=a)
    headline(c, 'لوحة ٠٤ · الحرارة', 'خمس وأربعون درجة' if t < 49.53 else 'يلين الشمع', 45.6 if t < 49.53 else 49.55, t, accent='درجة' if t < 49.53 else 'يلين')

@scene(51.89)
def s_morph(c, t):
    q = eio((t - 53.2) / 2.2) if t > 53.2 else 0
    comb(c, 'H1_circles', AX, AY + 20, CW, 1 - clamp((q - .2) / .8))
    comb(c, 'H2_hex', AX, AY + 20, CW, clamp((q - .2) / .8))
    R = .0925 * CW; rr = .066 * CW
    if 0 < q < 1:
        def fn(d, im):
            for i, p in enumerate(sorted(CELLS, key=lambda p: (p[0] - .48) ** 2 + (p[1] - .48) ** 2)):
                qq = clamp(q * 1.3 - i * .015)
                x, y = cell_xy(p, AX, AY + 20, CW); pts = hexpts(x, y, R * .93, qq, rr)
                d.line(pts + [pts[0]], fill=NAVYt, width=3)
        draw_on(c, fn)
    flash(c, t, 55.45, .07, RED, .3)
    headline(c, 'لوحة ٠٤ · السرّ', 'الجدران تنشدّ وحدها' if t < 55.4 else 'فتصير سداسية', 51.95 if t < 55.4 else 55.4, t, accent='وحدها' if t < 55.4 else 'سداسية')

def tile(d, kind, cx, cy, s, prog, col):
    if kind == 'c':
        for i in range(-1, 2):
            for j in range(-1, 2):
                x, y = cx + i * s * 1.0, cy + j * s * 1.0
                if prog > 0: d.arc([x - s / 2, y - s / 2, x + s / 2, y + s / 2], -90, -90 + 360 * prog, fill=col, width=4)
    elif kind == 's':
        for i in range(-1, 2):
            for j in range(-1, 2):
                x, y = cx + i * s * .89, cy + j * s * .89; h = s * .89 / 2
                L = [(x - h, y - h), (x + h, y - h), (x + h, y + h), (x - h, y + h), (x - h, y - h)]
                if prog > 0: d.line(L[:1 + max(1, int(4 * prog))], fill=col, width=4)
    else:
        R = s * .55
        for (i, j) in [(0, 0), (1, 0), (-1, 0), (.5, .87), (-.5, .87), (.5, -.87), (-.5, -.87)]:
            x, y = cx + i * R * 1.732, cy + j * R * 1.732
            pts = [(x + R * math.cos(math.pi / 6 + k * math.pi / 3), y + R * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(7)]
            if prog > 0: d.line(pts[:1 + max(1, int(6 * prog))], fill=col, width=4)
@scene(58.27)
def s_walls(c, t):
    p = [clamp((t - 58.5 - k * .5) / 1.0) for k in range(3)]
    def fn(d, im):
        tile(d, 'c', PX1 - 200, AY - 40, 76, p[0], NAVYt)
        tile(d, 's', W / 2, AY - 40, 76, p[1], NAVYt)
        tile(d, 'h', PX0 + 210, AY - 40, 76, p[2], REDt if t > 60.4 else NAVYt)
        F = kufi(32, 'Bold')
        for x, lab in [(PX1 - 160, 'فراغات'), (W / 2, '١٠٠'), (PX0 + 170, '٩٣')]:
            pass
    draw_on(c, fn)
    if t > 59.6: big_number(c, 'فراغات', PX1 - 200, AY + 200, 59.6, t, size=60, col=NAVY)
    if t > 60.0: big_number(c, '١٠٠', W / 2, AY + 200, 60.0, t, size=72, col=NAVY)
    if t > 60.4:
        big_number(c, '٩٣', PX0 + 210, AY + 200, 60.4, t, size=72, col=RED)
        ring(c, PX0 + 210, AY - 40, 150, clamp((t - 60.5) / .6), col=REDt, width=4)
    if t > 60.9: big_number(c, 'أقلّ شمع', AX, PY1 - 90, 60.9, t, size=70, col=RED)
    headline(c, 'لوحة ٠٤ · الهندسة', 'أقصر جدران ممكنة', 58.3, t, accent='أقصر')

@scene(62.47)
def s_eat(c, t):
    cm = clamp((t - 62.6) / .5)
    halftone_photo(c, 'img/P2_spoon.jpg', AX, AY + 80, PW * .95, PH * .9, 1.0, z=1.5 * breathe(t, 62.4, 71, 1, 1.05), color_mix=cm)
    if 64.04 < t < 69.47:
        e = enter(t, 64.04, .35)
        def fn(d, im):
            x, y, r = PX1 - 170, PY0 + 330, 80 * e
            d.ellipse([x - r, y - r, x + r, y + r], outline=REDt, width=7)
            d.line([(x - r * .45, y), (x - r * .1, y + r * .4), (x + r * .5, y - r * .4)], fill=REDt, width=9)
        draw_on(c, fn)
    if t > 69.47:   # E901 stamp
        dt = t - 69.47; sc = 1.6 - .6 * eoc(dt / .2)
        def fn2(d, im):
            x, y, r = PX1 - 200, AY - 140, 120 * sc
            d.ellipse([x - r, y - r, x + r, y + r], fill=PAPERt, outline=REDt, width=8)
            d.ellipse([x - r * .82, y - r * .82, x + r * .82, y + r * .82], outline=REDt, width=3)
            d.text((x, y), 'E901', font=kufi(int(72 * sc), 'Black'), fill=REDt, anchor='mm')
        draw_on(c, fn2)
    flash(c, t, 69.47, .07, RED, .25)
    if t < 64.04: headline(c, 'لوحة ٠٤ · الحسم', 'هل يُؤكل الشمع؟', 62.5, t, accent='يُؤكل')
    elif t < 66.07: headline(c, 'لوحة ٠٤ · الحسم', 'نعم، آمن', 64.04, t, accent='آمن')
    else: headline(c, 'لوحة ٠٤ · الحسم', 'يُلمّع الحلوى', 66.1, t, accent='الحلوى')

@scene(71.09)
def s_gut(c, t):
    gh = 820; gw = gh * 1147 / 2105
    layer(c, 'D1_gut', AX, AY + 10, gw * .85 * breathe(t, 71.1, 74.4, 1, 1.03), alpha=clamp((t - 71.1) / .2))
    # a wax flake travels down unchanged
    u = eio((t - 71.6) / 2.4)
    path = [(AX + 20, AY - 340), (AX + 20, AY - 160), (AX + 110, AY - 90), (AX, AY + 60), (AX - 60, AY + 200), (AX + 10, AY + 380)]
    v = u * (len(path) - 1); i = min(int(v), len(path) - 2); f = v - i
    x = path[i][0] + (path[i + 1][0] - path[i][0]) * f; y = path[i][1] + (path[i + 1][1] - path[i][1]) * f
    if 71.6 < t: layer(c, 'S1_scale', x, y, 80, rot=40 * u)
    headline(c, 'لوحة ٠٤ · الهضم', 'لا يكاد يُهضم', 71.1, t, accent='يُهضم')
    if t > 73.0: big_number(c, '٠ غذاء', PX1 - 170, AY - 280, 73.0, t, size=90, col=RED)

@scene(74.41)
def s_cta(c, t):
    halftone_photo(c, 'img/P2_spoon.jpg', AX, AY + 40, PW * .95, PH * .9, eoc((t - 74.45) / .4), z=2.0)
    bubble(c, 'آكله!', PX1 - 230, PY0 + 360, (t - 75.05) / .3, RED, tail=-1)
    bubble(c, 'أرميه!', PX0 + 230, PY0 + 360, (t - 75.6) / .3, NAVY, tail=1)
    headline(c, 'لوحة ٠٤ · رأيك', 'اكتب في التعليقات' if t > 76.48 else 'تأكله أم ترميه؟', 76.48 if t > 76.48 else 74.45, t,
             accent='التعليقات' if t > 76.48 else 'ترميه؟')

@scene(77.75)
def s_out(c, t):
    comb(c, 'H2_hex', AX, AY + 20, CW * breathe(t, 77.7, 81, 1, 1.04))
    bee(c, 'B1_bee', AX + 160, AY - 300, 300, alpha=clamp((t - 78.0) / .3) * .98)
    headline(c, 'لوحة ٠٤ · تذكّر', 'قرص عسل' if t < 80.51 else 'تذكّر:', 77.8 if t < 80.51 else 80.51, t, accent='عسل' if t < 80.51 else 'تذكّر:')

@scene(81.05)
def s_loop(c, t):
    halftone_photo(c, 'img/P1_hook.jpg', W / 2, PY0 + PH / 2 + 40, PW * .98, PH, 1.0, z=1.35, color_mix=clamp((t - 81.05) / .2))

# ------------------------------------------------------------------ frame
def scene_at(t):
    i = max(j for j, s in enumerate(SCENES) if s[0] <= t + 1e-6); return i, SCENES[i]
NO_RING = ('s_hook', 's_loop', 's_debate', 's_eat', 's_cta', 's_count', 's_cost', 's_walls', 's_gut', 's_heat')
def plate_render(i, t):
    c = paper_canvas()
    cs = circle_state(t)
    if cs and cs[2] > 1: disc(c, cs[0], cs[1], cs[2], cs[3])
    if cs and cs[2] > 30 and SCENES[i][1].__name__ not in NO_RING:
        ring(c, cs[0], cs[1], cs[2] + 46, clamp((t - SCENES[i][0]) / .8), col=NAVYt, width=2)
    SCENES[i][1](c, t); return c

def frame(t):
    i, (t0, fn) = scene_at(t)
    c = plate_render(i, t)
    TD = .33
    if i > 0 and t - t0 < TD and not any(abs(t0 - x) < .3 for x in CUTS) and fn.__name__ not in ('s_loop', 's_walls'):
        prev = plate_render(i - 1, t0 - .001)
        q = (t - t0) / TD; off = int(30 * eio(q))
        pv = np.roll(prev[PY0:PY1, PX0:PX1], -off, 0)
        c[PY0:PY1, PX0:PX1] = pv * (1 - eio(q)) + c[PY0:PY1, PX0:PX1] * eio(q)
    for tc in CUTS:
        if tc - .27 <= t < tc + .45:
            j = max(k for k, s in enumerate(SCENES) if s[0] <= tc - .3)
            if t < tc:
                xl = PX1 - (PX1 - PX0) * eio((t - (tc - .27)) / .27); section_line(c, PY0 + PH // 2, PX1 + 10, xl)
            else:
                old = plate_render(j, tc - .3)[PY0:PY1, PX0:PX1]
                q = eio(clamp((t - tc) / .43)); sh = int(PH * .55 * q); mid = PH // 2
                comp = c[PY0:PY1, PX0:PX1].copy(); y1 = mid - sh
                if y1 > 0: comp[:y1] = old[:mid][mid - y1:]
                y2 = mid + sh
                if y2 < PH: comp[y2:] = old[mid:][:PH - y2]
                c[PY0:PY1, PX0:PX1] = comp
                if q < 1: section_line(c, PY0 + PH // 2, PX1 + 10, PX0 - 10)
    dx = dy = 0
    for tt in (1.53, 34.6, 55.45, 69.47):
        ox, oy = shake_off(t, tt); dx += ox; dy += oy
    if dx or dy: c[PY0:PY1, PX0:PX1] = np.roll(np.roll(c[PY0:PY1, PX0:PX1], int(dy), 0), int(dx), 1)
    chrome(c, t, '٠٤', 'شمع النحل')
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
