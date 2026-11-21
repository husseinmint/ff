"""مقطع عرضي — 16:9 long-form engine (style v3 wide).
Layers: paper -> world layers (camera + parallax) -> chrome (fixed) -> captions/source -> transition overlay.
"""
import math, os, io, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import cairosvg

W, H = 1920, 1080
SAFE = (96, 54, 1824, 1026)
PAPER = (247, 238, 223);  # measured from owner's background plate
CREAM_ENGRAVING = (241, 234, 220); NAVY = (30, 42, 120); RED = (242, 54, 29)
FD = '/home/claude/eps/maqta3/fonts/'
TAB = '/tmp/tab/package/icons/'
AR = dict(direction='rtl', language='ar')
FPS = 30

_fc = {}
def ku(s, w='Bold'):
    k = ('ku', s, w)
    if k not in _fc:
        f = ImageFont.truetype(FD + 'NotoKufiArabic[wght].ttf', s); f.set_variation_by_name(w); _fc[k] = f
    return _fc[k]
def am(s):
    k = ('am', s)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + 'Amiri-Bold.ttf', s)
    return _fc[k]
def lat(s, bold=True):
    k = ('lat', s, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''), s)
    return _fc[k]

# ---------------- easing ----------------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / max(1e-6, t1 - t0))
def eio(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def spring(x, k=7.0, z=0.45):
    x = clamp(x)
    if x >= 1: return 1.0
    return 1 - math.exp(-z * k * x * 1.6) * math.cos(k * x * 1.15) * (1 - x) ** 0.3 if x > 0 else 0.0
def lerp(a, b, x): return a + (b - a) * x

# ---------------- paper ----------------
_rng = np.random.default_rng(7)
_g = _rng.normal(0, 5.5, (H, W, 1)) + _rng.normal(0, 2.5, (H // 4 + 1, W // 4 + 1, 1)).repeat(4, 0).repeat(4, 1)[:H, :W]
PAPER_IMG = Image.open('/home/claude/eps/maqta3/long01_digestion/bg/bg_clean_1920.png').convert('RGB')

# ---------------- riso ink ----------------
_grain = np.random.default_rng(11).random((H + 200, W + 200))
def ink_mask(mask, seed=0):
    a = np.asarray(mask).astype(np.float32) / 255
    h, w = a.shape; ox, oy = (seed * 37) % 150, (seed * 53) % 150
    n = _grain[oy:oy + h, ox:ox + w]
    a = a * (0.84 + 0.16 * n)
    return Image.fromarray((a * 255).astype('uint8'))

def stamp(base, mask, color, xy=(0, 0), alpha=1.0, seed=0):
    """paint a mask in ink colour onto RGB base (in place)."""
    m = ink_mask(mask, seed)
    if alpha < 1: m = m.point(lambda v: int(v * alpha))
    base.paste(Image.new('RGB', mask.size, color), (int(round(xy[0])), int(round(xy[1]))), m)

# ---------------- icons ----------------
_ic = {}
def icon(name, size, style='outline', stroke=2.0):
    k = (name, size, style, stroke)
    if k not in _ic:
        svg = open(TAB + style + '/' + name + '.svg').read().replace('currentColor', '#000')
        if style == 'outline': svg = svg.replace('stroke-width="2"', 'stroke-width="%s"' % stroke)
        png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
        _ic[k] = Image.open(io.BytesIO(png)).convert('RGBA').split()[3]
    return _ic[k]

# ---------------- assets / cut-outs ----------------
_asset = {}
def asset(path):
    if path not in _asset:
        im = Image.open(path).convert('RGBA'); _asset[path] = im
    return _asset[path]

def placeholder(w, h, label, sub='(صورة مؤقتة)'):
    """Labelled stand-in for a generated engraving that hasn't arrived yet."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=PAPER + (255,), outline=NAVY + (255,), width=3)
    for y in range(18, h - 10, 22): d.line([(16, y), (w - 16, y)], fill=(205, 198, 186, 255), width=1)
    d.text((w / 2, h / 2 - 22), label, font=ku(30), fill=NAVY + (255,), anchor='mm', **AR)
    d.text((w / 2, h / 2 + 24), sub, font=ku(22, 'Medium'), fill=NAVY + (255,), anchor='mm', **AR)
    return im

# ---------------- world layer / camera ----------------
class World:
    """Draw in world coords on 4 depth planes; camera applied per plane with parallax."""
    PAR = {'back': 0.5, 'mid': 0.8, 'hero': 1.0, 'front': 1.2}
    def __init__(s):
        s.planes = {k: Image.new('RGBA', (W, H), (0, 0, 0, 0)) for k in s.PAR}
    def d(s, plane): return ImageDraw.Draw(s.planes[plane])
    def paste(s, plane, im, xy, alpha=1.0, shadow=False):
        if alpha <= 0: return
        if shadow:
            im, (ox, oy) = paper_shadow(im); xy = (xy[0] + ox, xy[1] + oy)
        if alpha < 1:
            im = im.copy(); a = im.split()[3].point(lambda v: int(v * alpha)); im.putalpha(a)
        s.planes[plane].alpha_composite(im, (int(round(xy[0])), int(round(xy[1]))))
    def render(s, base, cam, clip_top=134):
        out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        s._render(out, cam)
        if clip_top:
            m = out.split()[3]; ImageDraw.Draw(m).rectangle([0, 0, W, clip_top], fill=0); out.putalpha(m)
        base.alpha_composite(out)
    def _render(s, base, cam):
        """cam = dict(zoom, cx, cy, dx, dy). zoom about (cx,cy) + pan (dx,dy) scaled by parallax."""
        for k, f in s.PAR.items():
            pl = s.planes[k]
            if pl.getbbox() is None: continue
            z = 1 + (cam.get('zoom', 1) - 1) * f
            bx, by = 0, 0  # line boil removed (owner feedback)
            dx = cam.get('dx', 0) * f + bx; dy = cam.get('dy', 0) * f + by
            cx, cy = cam.get('cx', W / 2), cam.get('cy', H / 2)
            if abs(z - 1) < 1e-4 and abs(dx) < .01 and abs(dy) < .01:
                base.alpha_composite(pl); continue
            if abs(z - 1) < 1e-4:
                base.alpha_composite(pl, (int(round(dx)), int(round(dy)))) if dx >= 0 and dy >= 0 else base.alpha_composite(pl.transform((W, H), Image.AFFINE, (1, 0, -dx, 0, 1, -dy))); continue
            # inverse affine: src = (dst - c - d)/z + c
            a = 1 / z; c = cx - (cx + dx) / z; f2 = cy - (cy + dy) / z
            t = pl.transform((W, H), Image.AFFINE, (a, 0, c, 0, a, f2), resample=Image.BICUBIC)
            base.alpha_composite(t)

# ---------------- safety ----------------
class SafetyError(Exception): pass
def assert_safe(box, name):
    x0, y0, x1, y1 = box
    if x0 < SAFE[0] - 1 or y0 < SAFE[1] - 1 or x1 > SAFE[2] + 1 or y1 > SAFE[3] + 1:
        raise SafetyError('%s outside safe area: %s' % (name, box))

# ---------------- chrome ----------------
NAV_X0, NAV_X1, NAV_Y = 600, 1320, 70
def nav_x(i):  # i = 0..6, station 1 at right (RTL)
    return NAV_X1 - i * (NAV_X1 - NAV_X0) / 6

def chrome(img, station, station_p=1.0, kicker='لوحة · الهضم'):
    """station: 1..7 current; station_p 0..1 progress of the red marker arriving."""
    d = ImageDraw.Draw(img)
    d.text((1824, NAV_Y), 'مقطع عرضي', font=ku(26), fill=NAVY, anchor='rm', **AR)
    d.text((96, NAV_Y), kicker, font=ku(24, 'Medium'), fill=NAVY, anchor='lm', **AR)
    d.line([(NAV_X0, NAV_Y), (NAV_X1, NAV_Y)], fill=NAVY, width=2)
    for i in range(7):
        x = nav_x(i); r = 9
        if i < station - 1: d.ellipse([x - r, NAV_Y - r, x + r, NAV_Y + r], fill=NAVY)
        else: d.ellipse([x - r, NAV_Y - r, x + r, NAV_Y + r], fill=PAPER, outline=NAVY, width=2)
    # red marker travels from previous station to current
    xa = nav_x(max(0, station - 2)); xb = nav_x(station - 1)
    x = lerp(xa, xb, eio(station_p)) if station > 1 else xb
    rr = 12 + 3 * math.sin(math.pi * clamp(station_p))
    d.ellipse([x - rr, NAV_Y - rr, x + rr, NAV_Y + rr], fill=RED)
    d.text((960, 106), '%s / ٧' % '١٢٣٤٥٦٧'[station - 1], font=ku(22), fill=RED, anchor='mm', **AR)
    d.line([(96, 130), (1824, 130)], fill=NAVY, width=1)

def handle_badge(img, alpha=1.0):
    w, h = 200, 46
    m_n = Image.new('L', (w, h), 0); dn = ImageDraw.Draw(m_n)
    dn.rounded_rectangle((2, 2, w - 3, h - 3), radius=21, outline=255, width=2)
    dn.text((w / 2, h / 2), '@maqta3', font=lat(22), fill=255, anchor='mm')
    x, y = 96, 972; assert_safe((x, y, x + w, y + h), 'handle')
    stamp(img, m_n, NAVY, (x, y), alpha, 1)

def source_line(img, text, alpha):
    if alpha <= 0 or not text: return
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    col = NAVY + (int(175 * alpha),)
    lab = 'المصدر:'; lw = od.textlength(lab, font=ku(22, 'Medium'), **AR)
    od.text((1824, 1000), lab, font=ku(22, 'Medium'), fill=col, anchor='rm', **AR)
    od.text((1824 - lw - 12, 1000), text, font=lat(22, False), fill=col, anchor='rm')
    bb = ov.getbbox()
    if bb: assert_safe(bb, 'source line')
    img.alpha_composite(ov)

def caption(img, words, t, t0, t1, accent=()):
    """words revealed one by one between t0..t1 (first 70% of window), RTL, centred."""
    if t < t0 or t > t1 + 0.25: return
    f = ku(46); d = ImageDraw.Draw(img)
    n = len(words); span = (t1 - t0) * 0.7
    widths = [d.textlength(w + ' ', font=f, **AR) for w in words]
    tot = sum(widths); x = 960 + tot / 2
    fade = 1 - prog(t, t1, t1 + 0.25)
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i, w in enumerate(words):
        p = prog(t, t0 + span * i / n, t0 + span * i / n + 0.18)
        if p > 0:
            c = RED if i in accent else NAVY
            od.text((x, 912 + 10 * (1 - eout(p))), w, font=f, fill=c + (int(255 * p * fade),), anchor='rm', **AR)
        x -= widths[i]
    ul = eout(prog(t, t0, t0 + 0.4))
    od.line([(960 - tot / 2 * ul, 964), (960 + tot / 2 * ul, 964)], fill=NAVY + (int(255 * fade),), width=2)
    bb = ov.getbbox()
    if bb: assert_safe(bb, 'caption')
    img.alpha_composite(ov)

# ---------------- transitions ----------------
def red_cut(img, p):
    """3 staggered red slabs wipe in right->left (cover by p=0.5), then wipe out leftwards."""
    if p <= 0 or p >= 1: return
    d = ImageDraw.Draw(img)
    for k in range(3):
        y0 = k * H / 3 - 1; y1 = (k + 1) * H / 3 + 1
        qi = eio(clamp((p - k * 0.06) / 0.38))           # cover
        qo = eio(clamp((p - 0.55 - k * 0.06) / 0.33))    # reveal
        xl = lerp(W + 100, -200, qi); xr = lerp(W + 200, -200, qo)
        if xr > xl:
            d.polygon([(xl, y0), (xr, y0), (xr - 90, y1), (xl - 90, y1)], fill=RED)

def flash(img, p, strength=0.55):
    if p <= 0 or p >= 1: return
    a = strength * (1 - p) ** 2
    img.alpha_composite(Image.new('RGBA', (W, H), PAPER + (int(255 * a),)))

def shake(t, t0, dur=0.35, amp=6):
    p = prog(t, t0, t0 + dur)
    if p <= 0 or p >= 1: return 0, 0
    e = (1 - p) ** 2 * amp
    return e * math.sin(t * 91), e * math.cos(t * 77)

# ---------------- render helpers ----------------
def new_frame():
    return PAPER_IMG.convert('RGBA')

def disc_rgba(r, color, alpha=1.0, seed=0):
    m = Image.new('L', (2 * r + 2, 2 * r + 2), 0)
    ImageDraw.Draw(m).ellipse((1, 1, 2 * r, 2 * r), fill=255)
    m = ink_mask(m, seed)
    if alpha < 1: m = m.point(lambda v: int(v * alpha))
    im = Image.new('RGBA', m.size, color + (0,)); im.putalpha(m); return im

# ================= v2 upgrades =================
BOIL_FPS = 10   # line boil: new jitter every 3 frames at 30fps
def boil_step(t): return int(t * BOIL_FPS)
def boil_off(t, plane, amp=1.2):
    s = boil_step(t) * 7 + hash(plane) % 97
    r = np.random.default_rng(s); return r.uniform(-amp, amp), r.uniform(-amp, amp)

def paper_shadow(im, off=(9, 11), alpha=0.20, blur=2.5):
    """cut-paper drop shadow: navy, offset down-right, under the sprite."""
    a = im.split()[3]
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), NAVY + (0,))
    m = Image.new('L', sh.size, 0); m.paste(a, (off[0] + 4, off[1] + 4))
    m = m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
    sh.putalpha(m)
    out = Image.new('RGBA', sh.size, (0, 0, 0, 0)); out.alpha_composite(sh); out.alpha_composite(im, (4, 4))
    return out, (-4, -4)

def red_cut_card(img, p, num, name):
    """station number printed on the red slabs while the screen is covered."""
    a = clamp(1 - abs(p - 0.5) / 0.16)
    if a <= 0: return
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    s = 1 + 0.06 * (p - 0.5) / 0.16
    f = am(int(300 * s)); col = PAPER + (int(255 * a),)
    d.text((960, 470), num, font=f, fill=col, anchor='mm', **AR)
    d.text((960, 700), name, font=ku(58), fill=col, anchor='mm', **AR)
    d.line([(960 - 120 * a, 760), (960 + 120 * a, 760)], fill=col, width=3)
    d.text((960, 300), 'المحطة', font=ku(34, 'Medium'), fill=col, anchor='mm', **AR)
    img.alpha_composite(ov)

AD = '٠١٢٣٤٥٦٧٨٩'
def slot_number(target, p, font, color, cell_h=None, start=None):
    """target like '١٫٥'. Each digit column scrolls down through digits and lands with overshoot.
    Returns RGBA sprite."""
    d0 = ImageDraw.Draw(Image.new('L', (4, 4)))
    ch = cell_h or int(font.size * 1.25)
    widths = [d0.textlength(c, font=font) for c in target]
    w = int(sum(widths)) + 8
    im = Image.new('RGBA', (w, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = 4; n = len(target)
    for i, c in enumerate(target):
        cw = widths[i]
        if c in AD:
            k = AD.index(c); q = clamp((p - (n - 1 - i) * 0.12) / 0.75)
            spins = 2 + (n - 1 - i)
            pos = (spins * 10 + k) * eout(q) if q < 1 else spins * 10 + k
            if 0 < q < 1: pos += 0.18 * math.sin(q * math.pi * 2.2) * (1 - q)
            base = int(math.floor(pos)); fr = pos - base
            for j in (0, 1):
                digit = AD[(base + j) % 10]
                y = ch / 2 + (j - fr) * ch
                d.text((x + cw / 2, y), digit, font=font, fill=color + (255,), anchor='mm')
        else:
            d.text((x + cw / 2, ch / 2), c, font=font, fill=color + (int(255 * clamp(p * 3)),), anchor='mm')
        x += cw
    return im

def trip_clock(img, label_old, label_new, p, alpha=1.0):
    """chrome trip clock left of the navigator: rolls old -> new label."""
    x = 560; y = NAV_Y
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    ic = icon('clock', 30, 'outline', 2.2)
    ov.paste(Image.new('RGBA', ic.size, RED + (255,)), (x - 30, y - 15), ic)
    f = ku(24); q = eio(p)
    box = Image.new('RGBA', (240, 50), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    if q < 1: bd.text((236, 25 + 40 * q), label_old, font=f, fill=NAVY + (int(255 * (1 - q)),), anchor='rm', **AR)
    if q > 0: bd.text((236, 25 - 40 * (1 - q)), label_new, font=f, fill=NAVY + (int(255 * q),), anchor='rm', **AR)
    ov.alpha_composite(box, (x - 40 - 240, y - 25))
    if alpha < 1:
        a = ov.split()[3].point(lambda v: int(v * alpha)); ov.putalpha(a)
    img.alpha_composite(ov)

def caption_k(img, words, t, t0, t1, accent=()):
    """karaoke caption: words appear in sequence; the word being spoken gets a red bar under it."""
    if t < t0 or t >= t1: return
    f = ku(46); d = ImageDraw.Draw(img)
    n = len(words); span = (t1 - t0) * 0.8
    widths = [d.textlength(w + ' ', font=f, **AR) for w in words]
    tot = sum(widths); x = 960 + tot / 2
    fade = 1 - prog(t, t1 - 0.12, t1)
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    cur = min(n - 1, int((t - t0) / (span / n))) if t < t0 + span else -1
    for i, w in enumerate(words):
        ws = t0 + span * i / n
        p = prog(t, ws, ws + 0.16)
        if p > 0:
            c = RED if i in accent else NAVY
            od.text((x, 912 + 8 * (1 - eout(p))), w, font=f, fill=c + (int(255 * p * fade),), anchor='rm', **AR)
            if i == cur:
                ww = d.textlength(w, font=f, **AR)
                od.rounded_rectangle((x - ww, 960, x, 967), radius=3, fill=RED + (int(255 * fade),))
        x -= widths[i]
    bb = ov.getbbox()
    if bb: assert_safe(bb, 'caption')
    img.alpha_composite(ov)


# station transition with hold: wipe-in 0.45 s, hold HOLD s, wipe-out 0.45 s
CUT_IN, CUT_HOLD, CUT_OUT = 0.45, 1.3, 0.45
def station_cut(img, t, t_start, num, name):
    """t_start = when the wipe begins. Returns True while the screen is fully covered."""
    lt = t - t_start; tot = CUT_IN + CUT_HOLD + CUT_OUT
    if lt <= 0 or lt >= tot: return False
    if lt < CUT_IN: p = 0.5 * lt / CUT_IN
    elif lt < CUT_IN + CUT_HOLD: p = 0.5
    else: p = 0.5 + 0.5 * (lt - CUT_IN - CUT_HOLD) / CUT_OUT
    red_cut(img, min(p, 0.999))
    # card: fades in during first 0.25 s of hold, out in last 0.2 s
    a = clamp((lt - CUT_IN + 0.05) / 0.25) * (1 - clamp((lt - CUT_IN - CUT_HOLD + 0.2) / 0.2))
    if a > 0:
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); col = PAPER + (int(255 * a),)
        s_ = 0.94 + 0.06 * eout(clamp((lt - CUT_IN) / CUT_HOLD))
        d.text((960, 300), 'المحطة', font=ku(34, 'Medium'), fill=col, anchor='mm', **AR)
        d.text((960, 480), num, font=am(int(300 * s_)), fill=col, anchor='mm', **AR)
        d.text((960, 700), name, font=ku(58), fill=col, anchor='mm', **AR)
        u = eout(clamp((lt - CUT_IN - 0.1) / 0.4))
        d.line([(960 - 120 * u, 760), (960 + 120 * u, 760)], fill=col, width=3)
        img.alpha_composite(ov)
    return CUT_IN <= lt <= CUT_IN + CUT_HOLD


def match_cream(im, tol=22):
    """Recolour the engraving's cream paper (#F1EADC) to the background plate's cream so cut-outs sit flush."""
    a = np.asarray(im.convert('RGBA')).astype(np.float32)
    rgb = a[..., :3]; d = np.abs(rgb - np.array(CREAM_ENGRAVING)).max(-1)
    w = np.clip(1 - d / tol, 0, 1)[..., None]
    rgb[:] = rgb + w * (np.array(PAPER) - np.array(CREAM_ENGRAVING))
    return Image.fromarray(a.clip(0, 255).astype('uint8'), 'RGBA')

def chip(img, box, radius=8):
    """small paper label cut from the clean centre of the plate (keeps chrome readable over halftone)."""
    x0, y0, x1, y1 = [int(v) for v in box]; w, h = x1 - x0, y1 - y0
    sh = Image.new('L', (w, h), 0); ImageDraw.Draw(sh).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=60)
    img.paste(Image.new('RGBA', (w, h), NAVY + (255,)), (x0 + 4, y0 + 5), sh.filter(ImageFilter.GaussianBlur(3)))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    img.paste(PAPER_IMG.crop((800, 400, 800 + w, 400 + h)).convert('RGBA'), (x0, y0), m)
