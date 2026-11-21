"""Animated CTA props in riso ink (navy + red, slight misregistration)."""
import math
from PIL import Image, ImageDraw
from wide import *

MIS = (3, 2)
def _two_ink(mn, mr, seed=0):
    """compose navy mask + red mask (offset) into RGBA sprite."""
    w, h = mn.size
    im = Image.new('RGBA', (w + 6, h + 6), (0, 0, 0, 0))
    n = Image.new('RGBA', mn.size, NAVY + (0,)); n.putalpha(ink_mask(mn, seed + 1))
    r = Image.new('RGBA', mr.size, RED + (0,)); r.putalpha(ink_mask(mr, seed + 2))
    im.alpha_composite(n, (0, 0)); im.alpha_composite(r, MIS)
    return im

def like_pill(press, count_old='١٢٫٤ ألف', count_new='١٢٫٥ ألف'):
    """press 0..1: 0 idle, >0.0 clicked (thumb fills red, burst grows & fades)."""
    w, h = 460, 150
    mn = Image.new('L', (w, h), 0); mr = Image.new('L', (w, h), 0)
    dn = ImageDraw.Draw(mn); dr = ImageDraw.Draw(mr)
    dn.rounded_rectangle((6, 6, w - 6, h - 6), radius=69, outline=255, width=5)
    on = press > 0
    sc = 1 + 0.18 * math.sin(math.pi * clamp(press / 0.35)) if on else 1
    s = int(96 * sc)
    th = icon('thumb-up', s, 'filled' if on else 'outline', 1.8)
    (mr if on else mn).paste(255, (348 - s // 2, 75 - s // 2), th)
    dn.line([(272, 30), (272, 120)], fill=255, width=3)
    dn.text((140, 75), count_new if on else count_old, font=ku(46), fill=255, anchor='mm', **AR)
    if on:
        b = clamp(press / 0.6); a = 1 - clamp((press - 0.45) / 0.4)
        if a > 0:
            m2 = Image.new('L', (w, h), 0); d2 = ImageDraw.Draw(m2)
            for k in range(8):
                ang = math.radians(k * 45 + 22)
                r0, r1 = 58 + 26 * b, 72 + 34 * b
                d2.line([(348 + r0 * math.cos(ang), 75 + r0 * math.sin(ang)),
                         (348 + r1 * math.cos(ang), 75 + r1 * math.sin(ang))], fill=int(255 * a), width=6)
            mr = ImageChops.lighter(mr, m2)
    return _two_ink(mn, mr, 5)

def sub_pill(press):
    w, h = 520, 150
    mn = Image.new('L', (w, h), 0); mr = Image.new('L', (w, h), 0)
    if press <= 0:
        d = ImageDraw.Draw(mr); d.rounded_rectangle((6, 6, w - 6, h - 6), radius=69, fill=255)
        d.text((300, 72), 'اشترِك', font=ku(56, 'Black'), fill=0, anchor='mm', **AR)
        mr.paste(0, (80, 35), icon('bell', 80, 'outline', 2.2))
    else:
        d = ImageDraw.Draw(mn); d.rounded_rectangle((6, 6, w - 6, h - 6), radius=69, outline=255, width=5)
        d.text((310, 72), 'مشترك', font=ku(54), fill=255, anchor='mm', **AR)
        ring = math.sin(press * 28) * 18 * (1 - clamp(press))
        b = icon('bell-ringing', 84, 'filled').rotate(ring, resample=Image.BICUBIC, center=(42, 8))
        mr.paste(255, (78, 33), b)
    return _two_ink(mn, mr, 7)

def cursor_sprite(click=0.0):
    s = int(90 * (1 - 0.15 * math.sin(math.pi * clamp(click))))
    m = icon('pointer', s, 'filled')
    im = Image.new('RGBA', m.size, NAVY + (0,)); im.putalpha(ink_mask(m, 9)); return im
