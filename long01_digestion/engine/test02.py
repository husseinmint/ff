"""Motion test (~20 s): map navigator -> red section-cut -> stomach plate -> like CTA.
Placeholders stand in for generated engravings until they arrive."""
import sys, os, math, subprocess
from PIL import Image, ImageDraw
from wide import *
from props_anim import like_pill, cursor_sprite

DUR = 20.0
T_CUT = 5.6            # red section-cut centre
T_S = T_CUT + 0.55     # stomach scene start (local 0)

# ---- tract map placeholder with authored station path (world coords) ----
MAP_W, MAP_H = 520, 860
MAP_X, MAP_Y = 960 - MAP_W // 2, 150
MAP = placeholder(MAP_W, MAP_H, 'خريطة القناة الهضمية (G1)')
# station points inside the map (relative), top->bottom
ST = [(0.50, 0.08), (0.50, 0.17), (0.50, 0.32), (0.62, 0.45), (0.48, 0.66), (0.30, 0.60), (0.50, 0.90)]
ST = [(MAP_X + u * MAP_W, MAP_Y + v * MAP_H) for u, v in ST]
STOMACH = placeholder(400, 490, 'صورة المعدة المحفورة (S1)')

def path_point(a, b, p):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p)

def scene_map(fr, t):
    w = World()
    w.paste('hero', MAP, (MAP_X, MAP_Y), shadow=True)
    d = w.d('front')
    # dotted route already travelled (stations 1->3) + current leg 3->4
    p = eio(prog(t, 1.2, 3.6))
    pts = ST[:3] + [path_point(ST[2], ST[3], p)]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]; L = math.dist(a, b); n = int(L / 14)
        for k in range(n + 1):
            x, y = path_point(a, b, k / max(1, n)); d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED + (255,))
    for i, (x, y) in enumerate(ST):
        done = i < 3 or (i == 3 and p >= 1)
        r = 13
        d.ellipse([x - r, y - r, x + r, y + r], fill=(NAVY if done else PAPER) + (255,), outline=NAVY + (255,), width=3)
    x, y = pts[-1]; rr = 16 + 4 * math.sin(t * 6)
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=RED + (255,))
    # station label pops when arriving
    lp = eout(prog(t, 3.6, 4.0))
    if lp > 0:
        d.text((ST[3][0] + 40, ST[3][1]), 'المحطة ٤ · المعدة', font=ku(30), fill=RED + (int(255 * lp),), anchor='lm', **AR)
    # camera: pull back then push toward station 4
    z = lerp(1.12, 1.0, eio(prog(t, 0, 1.2))) if t < 1.2 else lerp(1.0, 1.45, eio(prog(t, 3.9, T_CUT)))
    cam = dict(t=t, zoom=z, cx=ST[3][0], cy=ST[3][1])
    w.render(fr, cam)
    return prog(t, 1.2, 3.6)   # navigator marker progress

def scene_stomach(fr, t):
    """t = local time from scene start."""
    w = World()
    cx, cy = 560, 500
    # back circle springs in
    cp = spring(prog(t, 0.0, 0.9))
    if cp > 0:
        r = int(300 * cp); disc = disc_rgba(max(2, r), NAVY, 1, boil_step(t) % 5)
        w.paste('back', disc, (cx - r, cy - r), shadow=True)
    # orbit ring draws itself + red dot
    op = eout(prog(t, 0.25, 1.4))
    if op > 0:
        d = w.d('back'); R = 340
        d.arc([cx - R, cy - R, cx + R, cy + R], 200, 200 + 320 * op, fill=NAVY + (255,), width=2)
        a = math.radians(200 + 320 * op); d.ellipse([cx + R * math.cos(a) - 9, cy + R * math.sin(a) - 9, cx + R * math.cos(a) + 9, cy + R * math.sin(a) + 9], fill=RED + (255,))
    # hero enters from below with spring, then breathes
    hp = spring(prog(t, 0.45, 1.35))
    if hp > 0:
        br = 1 + 0.012 * math.sin(t * 1.3)
        im = STOMACH.resize((int(400 * br), int(490 * br)), Image.BICUBIC)
        w.paste('hero', im, (cx - im.width / 2, cy - im.height / 2 + 120 * (1 - hp)), alpha=clamp(hp * 1.5), shadow=True)
    # pH tag pops at 2.6 (with chrome shake)
    pp = spring(prog(t, 2.6, 3.2))
    if pp > 0:
        tag = Image.new('RGBA', (170, 90), (0, 0, 0, 0)); td = ImageDraw.Draw(tag)
        td.rounded_rectangle((4, 4, 166, 86), radius=6, outline=RED + (255,), width=3, fill=PAPER + (255,))
        td.text((150, 45), 'pH', font=lat(28), fill=RED + (255,), anchor='rm')
        sn = slot_number('١٫٥', prog(t, 2.6, 3.6), ku(34), RED, 44)
        tag.alpha_composite(sn, (14, 45 - 22))
        s = 0.6 + 0.4 * pp; tag = tag.resize((int(170 * s), int(90 * s)), Image.BICUBIC)
        w.paste('front', tag, (980 - tag.width / 2, 330 - tag.height / 2), alpha=clamp(pp * 2), shadow=True)
    # text column (front plane, light parallax)
    d = w.d('front')
    kp = eout(prog(t, 0.9, 1.3))
    if kp > 0:
        d.text((1824, 300), 'المحطة ٤ · المعدة', font=ku(30, 'Medium'), fill=RED + (int(255 * kp),), anchor='rm', **AR)
        d.line([(1824 - 260 * kp, 330), (1824, 330)], fill=RED + (255,), width=2)
    f = am(88)
    words = [('لماذا لا', NAVY, 1.2, (1824, 430)), ('تهضمُ', RED, 1.55, None), ('نفسَها؟', NAVY, 1.9, (1824, 545))]
    w1 = d.textlength('لماذا لا', font=f, **AR); words[1] = ('تهضمُ', RED, 1.55, (1824 - w1 - 22, 430))
    for txt, col, t0, (x, y) in words:
        q = eout(prog(t, t0, t0 + 0.35))
        if q > 0: d.text((x, y + 18 * (1 - q)), txt, font=f, fill=col + (int(255 * q),), anchor='rm', **AR)
    # like CTA (front plane)
    if 8.0 <= t <= 13.6:
        ip = spring(prog(t, 8.0, 8.7)); outp = eio(prog(t, 12.9, 13.6))
        click_t = 10.2; press = prog(t, click_t, click_t + 1.2) if t >= click_t else 0
        pill = like_pill(press)
        x = lerp(1900, 1180, ip) + lerp(0, 760, outp); y = 640
        w.paste('front', pill, (x, y), alpha=1 - outp, shadow=True)
        # cursor glides to thumb, clicks
        cp2 = eio(prog(t, 8.9, 10.1))
        tx, ty = x + 360, y + 92
        cxp, cyp = lerp(1760, tx, cp2), lerp(1000, ty, cp2)
        if t < 12.8:
            cs = cursor_sprite(prog(t, click_t - 0.05, click_t + 0.2))
            w.paste('front', cs, (cxp, cyp), alpha=1 - outp)
    # camera: slow push-in + gentle lateral drift (never fully still)
    cam = dict(t=t, zoom=1 + 0.05 * eio(prog(t, 0, 14)), cx=760, cy=520, dx=-10 * math.sin(t * 0.25), dy=0)
    w.render(fr, cam)

CAPS = [  # (words, t0, t1, accent idx) in scene-local time
    (['فلماذا', 'لا', 'تهضمُ'], 1.0, 3.4, (2,)),
    (['المعدةُ', 'نفسَها؟'], 3.4, 5.6, ()),
    (['السرُّ:', 'طبقةٌ', 'من', 'المُخاط'], 5.6, 7.9, (3,)),
    (['لايكٌ', 'صغيرٌ', 'يساعدُنا', 'كثيرًا'], 8.2, 10.6, (0,)),
    (['والرحلةُ', 'مستمرّة'], 10.6, 12.6, ()),
]

def frame(i):
    t = i / FPS
    fr = new_frame()
    if t < T_CUT:
        p = scene_map(fr, t); station, sp = 4, p
    else:
        lt = t - T_S
        if lt > -0.4: scene_stomach(fr, max(0, lt))
        station, sp = 4, 1.0
        for words, t0, t1, acc in CAPS: caption_k(fr, words, lt, t0, t1, acc)
        # source line: with the pH/acid fact, hidden during CTA
        sa = eout(prog(lt, 2.6, 2.9)) * (1 - eout(prog(lt, 7.8, 8.1)))
        source_line(fr, 'OpenStax, Anatomy & Physiology 2e', sa)
    # chrome (shake on pH hit)
    ch = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    chrome(ch, station, sp)
    sx, sy = shake(t - T_S, 2.6) if t >= T_CUT else (0, 0)
    fr.alpha_composite(ch, (int(sx), int(sy)))
    handle_badge_rgb = fr
    handle_badge(fr)
    trip_clock(fr, 'رحلة اللقمة: ثوانٍ', 'رحلة اللقمة: ساعتان', prog(t, 3.6, 4.1))
    if t >= T_CUT: flash(fr, prog(t - T_S, 2.6, 3.0), 0.35)
    red_cut(fr, prog(t, T_CUT - 0.8, T_CUT + 0.8))
    red_cut_card(fr, prog(t, T_CUT - 0.8, T_CUT + 0.8), '٤', 'المعدة')
    return fr.convert('RGB')

def render(a, b, out, scale=1.0):
    w, h = int(W * scale), int(H * scale)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (w, h), '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        im = frame(i)
        if scale != 1: im = im.resize((w, h), Image.LANCZOS)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        for tt in map(float, sys.argv[2:]): frame(int(tt * FPS)).save('still_%05.2f.png' % tt)
    else:
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        render(a, b, out, float(sys.argv[5]) if len(sys.argv) > 5 else 1.0)
