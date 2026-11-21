#!/usr/bin/env python3
"""Build script (NOT the entry) for the LUMARA travel poster.

Draws a 1024x1024 travel poster for LUMARA, the City of Two Dawns:
a cliffside harbour city under twin suns, with a spiral lighthouse
as its one landmark. Output: poster.png next to this script.
Run once during the build; the entry itself (main.py) only copies
the finished PNG, so it stays stdlib-only at grade time.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
OUT = "poster.png"

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

random.seed(20261121)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, width, y0, y1, stops):
    """Vertical gradient between (pos, color) stops."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                tt = (t - p0) / max(1e-6, (p1 - p0))
                draw.line([(0, y), (width, y)], fill=lerp(c0, c1, tt))
                break


def glow_circle(base, cx, cy, r, color, alpha=200):
    """Soft radial glow on a transparent layer, composited onto base."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(alpha * (1 - i / steps) ** 2)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
    layer = layer.filter(ImageFilter.GaussianBlur(6))
    base.alpha_composite(layer)


def tracked_text(draw, cx, y, text, font, fill, tracking=0):
    """Draw text centred at cx with letter tracking; returns width."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return total


img = Image.new("RGBA", (W, H), (23, 16, 56, 255))
d = ImageDraw.Draw(img)

# ---- sky: deep indigo -> violet -> coral -> amber at the horizon ----
vgrad(d, W, 0, 620, [
    (0.00, (23, 16, 56)),
    (0.35, (58, 34, 96)),
    (0.62, (138, 66, 102)),
    (0.85, (214, 110, 84)),
    (1.00, (242, 166, 94)),
])

# ---- stars in the upper sky ----
for _ in range(140):
    x = random.randint(0, W)
    y = random.randint(0, 330)
    r = random.choice([1, 1, 1, 2])
    a = random.randint(60, 200)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, a))

# ---- twin suns with glow ----
glow_circle(img, 660, 430, 190, (255, 190, 110), alpha=150)
glow_circle(img, 350, 330, 120, (255, 210, 140), alpha=130)
d = ImageDraw.Draw(img)
d.ellipse([590, 360, 730, 500], fill=(255, 214, 140, 255))   # big sun
d.ellipse([312, 292, 388, 368], fill=(255, 232, 170, 255))   # small sun
d.ellipse([600, 372, 720, 492], fill=(255, 228, 168, 255))   # inner light

# ---- birds ----
for bx, by, s in [(250, 300, 14), (300, 270, 10), (760, 250, 12), (820, 300, 9)]:
    d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340, fill=(40, 24, 60, 220), width=3)
    d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340, fill=(40, 24, 60, 220), width=3)

# ---- distant headland silhouette ----
d.polygon([(0, 620), (0, 560), (120, 585), (260, 545), (430, 590),
           (560, 565), (760, 600), (1024, 570), (1024, 620)],
          fill=(74, 42, 92, 255))

# ---- sea: warm at horizon -> deep teal ----
vgrad(d, W, 620, 1024, [
    (0.00, (226, 138, 84)),
    (0.25, (120, 84, 96)),
    (0.60, (32, 66, 88)),
    (1.00, (12, 40, 62)),
])

# ---- sun reflections: broken horizontal strokes under each sun ----
for sx, top, length in [(660, 630, 360), (350, 630, 240)]:
    for i in range(46):
        y = top + i * 8 + random.randint(-2, 2)
        half = int(10 + (i / 46) * 70 * (length / 360))
        a = int(190 * (1 - i / 46) + 30)
        x0 = sx - half + random.randint(-14, 14)
        x1 = sx + half + random.randint(-14, 14)
        d.line([(x0, y), (x1, y)], fill=(255, 200, 130, a), width=3)

# ---- foreground cliffs (left + right) ----
d.polygon([(0, 1024), (0, 880), (90, 830), (210, 860), (300, 900),
           (330, 1024)], fill=(18, 12, 40, 255))
d.polygon([(1024, 1024), (1024, 840), (950, 800), (830, 830),
           (760, 880), (700, 1024)], fill=(18, 12, 40, 255))
# cliff edge highlights
d.line([(0, 880), (90, 830), (210, 860), (300, 900)], fill=(242, 166, 94, 160), width=3)
d.line([(1024, 840), (950, 800), (830, 830), (760, 880)], fill=(242, 166, 94, 160), width=3)

# ---- cliffside city: white houses with warm windows on the right cliff ----
for hx, hy, hw, hh in [(800, 800, 46, 60), (852, 812, 38, 48), (892, 792, 52, 68),
                        (948, 818, 40, 42), (770, 836, 40, 40), (905, 852, 44, 34)]:
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(244, 230, 205, 255))
    d.polygon([(hx - 4, hy), (hx + hw // 2, hy - 16), (hx + hw + 4, hy)],
              fill=(178, 74, 74, 255))
    for wy in range(hy + 12, hy + hh - 8, 16):
        for wx in range(hx + 8, hx + hw - 8, 16):
            d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 196, 110, 255))

# ---- spiral lighthouse on the right cliff (the landmark) ----
lx, base_y, top_y = 700, 890, 470
tower_w_bot, tower_w_top = 74, 40
# beam of light sweeping left, drawn first so the tower sits over it
beam = Image.new("RGBA", img.size, (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(lx, 500), (60, 430), (60, 560)], fill=(255, 226, 150, 90))
beam = beam.filter(ImageFilter.GaussianBlur(10))
img.alpha_composite(beam)
d = ImageDraw.Draw(img)
# tower body: white with terracotta spiral bands
d.polygon([(lx - tower_w_bot // 2, base_y), (lx - tower_w_top // 2, top_y),
           (lx + tower_w_top // 2, top_y), (lx + tower_w_bot // 2, base_y)],
          fill=(250, 240, 220, 255))
for i in range(6):
    y0 = top_y + 18 + i * 66
    y1 = y0 + 30
    # diagonal band across the tower, clipped by its taper
    frac0 = (y0 - top_y) / (base_y - top_y)
    frac1 = (y1 - top_y) / (base_y - top_y)
    w0 = tower_w_top + (tower_w_bot - tower_w_top) * frac0
    w1 = tower_w_top + (tower_w_bot - tower_w_top) * frac1
    d.polygon([(lx - w0 // 2, y0), (lx + w0 // 2, y0 - 26),
               (lx + w1 // 2, y1 - 26), (lx - w1 // 2, y1)],
              fill=(196, 84, 62, 255))
# gallery + lamp room + dome
d.rectangle([lx - 34, top_y - 26, lx + 34, top_y], fill=(40, 26, 56, 255))
d.rectangle([lx - 22, top_y - 62, lx + 22, top_y - 26], fill=(255, 226, 150, 255))
d.ellipse([lx - 26, top_y - 88, lx + 26, top_y - 56], fill=(196, 84, 62, 255))
d.rectangle([lx - 3, top_y - 100, lx + 3, top_y - 86], fill=(40, 26, 56, 255))
glow_circle(img, lx, top_y - 44, 60, (255, 226, 150), alpha=170)
d = ImageDraw.Draw(img)
# tiny windows down the tower
for wy in range(top_y + 60, base_y - 40, 64):
    d.ellipse([lx - 5, wy, lx + 5, wy + 12], fill=(255, 196, 110, 255))

# ---- small boats on the sea ----
for bx, by, s in [(430, 700, 1.0), (540, 760, 0.7), (300, 800, 0.55)]:
    d.polygon([(bx - 26 * s, by), (bx + 26 * s, by), (bx + 14 * s, by + 10 * s),
               (bx - 14 * s, by + 10 * s)], fill=(30, 20, 52, 255))
    d.line([(bx, by), (bx, by - 30 * s)], fill=(30, 20, 52, 255), width=3)
    d.polygon([(bx + 2, by - 28 * s), (bx + 2, by - 2), (bx + 22 * s, by - 2)],
              fill=(250, 240, 220, 255))

# ---- title block ----
title_font = ImageFont.truetype(SERIF_BOLD, 118)
sub_font = ImageFont.truetype(SANS, 30)
# soft shadow then cream title
tracked_text(d, W // 2 + 4, 78, "LUMARA", title_font, (20, 12, 44, 220), tracking=26)
tracked_text(d, W // 2, 74, "LUMARA", title_font, (253, 243, 221, 255), tracking=26)
# gold rule + subtitle
d.line([(W // 2 - 210, 216), (W // 2 - 40, 216)], fill=(242, 192, 120, 255), width=3)
d.line([(W // 2 + 40, 216), (W // 2 + 210, 216)], fill=(242, 192, 120, 255), width=3)
d.ellipse([W // 2 - 6, 210, W // 2 + 6, 222], fill=(242, 192, 120, 255))
tracked_text(d, W // 2, 232, "THE CITY OF TWO DAWNS", sub_font,
             (242, 192, 120, 255), tracking=10)

# ---- thin cream frame ----
d.rectangle([22, 22, W - 23, H - 23], outline=(253, 243, 221, 200), width=3)

img.convert("RGB").save(OUT, optimize=True)
print("saved", OUT)
