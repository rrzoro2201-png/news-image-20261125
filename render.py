#!/usr/bin/env python3
"""The Daily Chronicle - 25 November 2026. One-page illustrated newspaper.
Draws a dense 1024x1024 front page with PIL: masthead, big-number strip,
region bars, three illustrated leads, a 10-story picture grid, a world map
with story dots, and a numbered list of 22 more stories (35 in all).
Pure stdlib + Pillow; no network, no external assets.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (252, 252, 252)
INK = (17, 17, 17)
RULE = (17, 17, 17)
MUTED = (110, 110, 110)
RED = (220, 38, 38)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=4):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def hline(draw, x0, x1, y, w=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 11)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + 15


# ---------------------------------------------------------------- regions
REGIONS = [
    ("NORTH AMERICA", (178, 34, 34)),
    ("EUROPE", (31, 80, 160)),
    ("MIDDLE EAST", (196, 132, 16)),
    ("ASIA-PACIFIC", (34, 120, 64)),
    ("AFRICA", (110, 60, 150)),
    ("MARKETS & TECH", (14, 130, 130)),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 24  # margin

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 10], fill=INK)
f_mast = font(SANS_B, 48)
title = "The Daily Chronicle"
tw = d.textlength(title, font=f_mast)
d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
d.rectangle([(W + tw) / 2 + 12, 30, (W + tw) / 2 + 42, 60], fill=RED)
hline(d, MX, W - MX, 84, 3)
f_sub = font(SANS, 12)
d.text((MX, 90), "No. 329  \u00b7  EST. 2021", font=f_sub, fill=MUTED)
dateline = "WEDNESDAY, 25 NOVEMBER 2026"
dw = d.textlength(dateline, font=font(SANS_B, 12))
d.text(((W - dw) / 2, 90), dateline, font=font(SANS_B, 12), fill=INK)
d.text((W - MX - d.textlength("35 STORIES \u00b7 6 REGIONS", font=f_sub), 90),
       "35 STORIES \u00b7 6 REGIONS", font=f_sub, fill=MUTED)

# ---------------------------------------------------------------- big numbers
NUMBERS = [
    ("+31.5%", "NVIDIA SHARES SURGE"),
    ("700,000", "RUSSIAN TROOPS KILLED IN UKRAINE WAR"),
    ("74,746", "GAZA DEATH TOLL, HEALTH OFFICIALS SAY"),
    ("$43.9B", "CROWDSTRIKE TO BUY ZSCALER"),
]
y0, y1 = 108, 162
col_w = (W - 2 * MX) / 4
for i, (num, label) in enumerate(NUMBERS):
    x = MX + i * col_w
    d.rounded_rectangle([x, y0, x + col_w - 10, y1], radius=8,
                        fill=(242, 242, 242))
    fn = font(SANS_B, 28)
    d.text((x + 10, y0 + 5), num, font=fn, fill=RED if i == 0 else INK)
    para(d, x + 10, y0 + 38, label, font(SANS_B, 9), col_w - 26, fill=MUTED, leading=1)

# ---------------------------------------------------------------- region bar
y = 168
x = MX
f_reg = font(SANS_B, 10)
for name, color in REGIONS:
    tw = d.textlength(name, font=f_reg)
    d.rounded_rectangle([x, y - 2, x + tw + 20, y + 14], radius=8, fill=color)
    d.text((x + 10, y), name, font=f_reg, fill=(255, 255, 255))
    x += tw + 20 + 10
hline(d, MX, W - MX, 186, 2)

# ---------------------------------------------------------------- hero: NVIDIA
HX, HY, HW, HH = MX, 194, 600, 176
# illustration panel: dark fab floor, glowing chip, rising chart
d.rounded_rectangle([HX, HY, HX + HW, HY + HH], radius=12, fill=(12, 26, 20))
# glow behind chip
for r, a in [(62, 18), (48, 26), (34, 38)]:
    d.ellipse([HX + 150 - r, HY + 88 - r, HX + 150 + r, HY + 88 + r],
              fill=(16, 90 + a, 50))
# chip body + pins
cx, cy, cw, ch = HX + 88, HY + 46, 124, 84
for px in range(6):
    for side in (0, 1):
        xx = cx - 14 + side * (cw + 14) if side else cx - 14
        d.rectangle([cx - 14 if side == 0 else cx + cw, cy + 12 + px * 13,
                     cx - 4 if side == 0 else cx + cw + 10, cy + 20 + px * 13],
                    fill=(120, 200, 140))
d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=8, fill=(24, 68, 44),
                    outline=(110, 230, 150), width=3)
d.rounded_rectangle([cx + 26, cy + 22, cx + cw - 26, cy + ch - 22], radius=4,
                    fill=(10, 40, 28), outline=(90, 200, 130), width=2)
d.text((cx + 38, cy + 34), "NVDA", font=font(SANS_B, 22), fill=(140, 255, 180))
# rising chart
pts = [(HX + 260, HY + 140), (HX + 330, HY + 128), (HX + 400, HY + 132),
       (HX + 470, HY + 96), (HX + 540, HY + 100), (HX + 610, HY + 44)]
d.line(pts, fill=(120, 255, 170), width=4)
d.polygon([(HX + 610, HY + 44), (HX + 624, HY + 44), (HX + 610, HY + 60)],
          fill=(120, 255, 170))
# burst
bx, by = HX + 540, HY + 40
for k in range(12):
    ang = k * math.pi / 6
    d.line([(bx + 26 * math.cos(ang), by + 26 * math.sin(ang)),
            (bx + 40 * math.cos(ang), by + 40 * math.sin(ang))],
           fill=(255, 210, 90), width=3)
d.ellipse([bx - 26, by - 26, bx + 26, by + 26], fill=(255, 210, 90))
d.text((bx - 22, by - 10), "$1 TN", font=font(SANS_B, 13), fill=(60, 40, 0))
d.text((HX + 8, HY + HH - 18), "ILLUSTRATION: THE FAB FLOOR, SANTA CLARA",
       font=font(SANS, 8), fill=(150, 180, 160))

# hero text, right of illustration
TX = HX + HW + 16
TW = W - MX - TX
kicker(d, TX, HY + 2, "Markets \u00b7 North America", REGIONS[0][1])
f_h1 = font(SANS_B, 30)
y = para(d, TX, HY + 20, "THE CHIP KING RETURNS", f_h1, TW, leading=2)
y = para(d, TX, y + 4,
         "Jensen Huang is back as Nvidia chief after a two-week ouster "
         "\u2014 and Wall Street roared. Shares leapt 31.5%, clawing back "
         "nearly $1 trillion in a single day.",
         font(SANS, 12), TW, leading=3)
y = para(d, TX, y + 4,
         "But the comeback comes with a summons: Congress wants answers "
         "on the spy affair and the chips that reached China.",
         font(SANS, 11), TW, fill=MUTED, leading=3)
d.text((TX, HY + HH - 14), "By the Markets Desk \u00b7 Continued on page 2",
       font=font(SANS, 9), fill=MUTED)
hline(d, MX, W - MX, HY + HH + 8, 1)

# ---------------------------------------------------------------- row 2: two panels
RY, RH = 384, 138
PW = (W - 2 * MX - 16) // 2


def panel_head(x, y, w, tag, color):
    kicker(d, x, y, tag, color)


# --- left: Benghazi warship
PX = MX
panel_head(PX, RY, PW, "Europe \u00b7 Africa \u00b7 War at sea", REGIONS[1][1])
IX, IY, IW, IH = PX, RY + 18, 300, 84
# sea + sky
d.rectangle([IX, IY, IX + IW, IY + IH], fill=(214, 232, 240))
d.rectangle([IX, IY + 52, IX + IW, IY + IH], fill=(38, 92, 138))
for wy in (58, 68, 78):
    for wx in range(0, IW, 46):
        d.arc([IX + wx, IY + wy, IX + wx + 34, IY + wy + 10], 0, 180,
              fill=(180, 215, 235), width=2)
# sun
d.ellipse([IX + IW - 44, IY + 6, IX + IW - 14, IY + 36], fill=(255, 196, 66))
# ship silhouette
d.polygon([(IX + 40, IY + 52), (IX + 250, IY + 52), (IX + 236, IY + 72),
           (IX + 56, IY + 72)], fill=(40, 44, 52))
d.rectangle([IX + 120, IY + 28, IX + 168, IY + 52], fill=(52, 56, 64))
d.rectangle([IX + 140, IY + 12, IX + 146, IY + 28], fill=(52, 56, 64))
d.line([(IX + 143, IY + 12), (IX + 143, IY + 2)], fill=(52, 56, 64), width=2)
# smoke + fire
for sx, sy, sr in [(IX + 130, IY + 26, 9), (IX + 122, IY + 18, 11),
                   (IX + 134, IY + 10, 8)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 118))
d.polygon([(IX + 196, IY + 52), (IX + 210, IY + 30), (IX + 224, IY + 52)],
          fill=(255, 120, 30))
d.rectangle([IX, IY + IH - 14, IX + 148, IY + IH], fill=(20, 40, 60))
d.text((IX + 6, IY + IH - 13), "BENGHAZI HARBOUR, LIBYA",
       font=font(SANS, 8), fill=(230, 240, 245))
f_h2 = font(SANS_B, 18)
y = para(d, PX, RY + 108, "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
         f_h2, PW, leading=1)
para(d, PX, y + 2,
     "Zelenskyy confirms Kyiv's drones struck 2,000 km from home. "
     "Moscow calls it terrorism and vows a response.",
     font(SANS, 10), PW, fill=MUTED, leading=2)

# --- right: COP31 collapse
PX2 = MX + PW + 16
panel_head(PX2, RY, PW, "Climate \u00b7 Europe", REGIONS[1][1])
IX, IY, IW, IH = PX2, RY + 18, 300, 84
d.rectangle([IX, IY, IX + IW, IY + IH], fill=(250, 214, 150))
d.rectangle([IX, IY + 56, IX + IW, IY + IH], fill=(196, 132, 60))
d.ellipse([IX + 24, IY + 8, IX + 76, IY + 60], fill=(255, 176, 40))
d.ellipse([IX + 34, IY + 18, IX + 66, IY + 50], fill=(255, 200, 90))
# cracked earth
for cx0 in (IX + 90, IX + 150, IX + 220, IX + 260):
    d.line([(cx0, IY + 56), (cx0 + 18, IY + 70), (cx0 + 6, IY + 84)],
           fill=(120, 70, 20), width=2)
# globe with crack
gx, gy, gr = IX + 210, IY + 30, 26
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(90, 160, 200),
          outline=(30, 80, 120), width=2)
d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 320, fill=(40, 120, 60),
      width=5)
d.line([(gx - 8, gy - 24), (gx + 2, gy - 6), (gx - 6, gy + 10), (gx + 8, gy + 24)],
       fill=(178, 34, 34), width=3)
d.text((IX + 6, IY + IH - 13), "ANTALYA, T\u00dcRKIYE",
       font=font(SANS, 8), fill=(90, 50, 10))
y = para(d, PX2, RY + 108, "COP31 COLLAPSES IN ANTALYA",
         f_h2, PW, leading=1)
para(d, PX2, y + 2,
     "Oil states block fossil-fuel phaseout language. No final deal \u2014 "
     "and no climate cash for the nations most at risk.",
     font(SANS, 10), PW, fill=MUTED, leading=2)
hline(d, MX, W - MX, 548, 1)

# ---------------------------------------------------------------- picture grid
GY = 552
GCOLS, GROWS = 5, 2
GW = (W - 2 * MX - (GCOLS - 1) * 10) // GCOLS
GH = 68


def icon(draw, x, y, kind, color):
    draw.rounded_rectangle([x, y, x + 52, y + 52], radius=8, fill=color)
    c = (255, 255, 255)
    if kind == "shield":  # CIA breach
        draw.polygon([(x + 26, y + 8), (x + 42, y + 14), (x + 42, y + 28),
                      (x + 26, y + 44), (x + 10, y + 28), (x + 10, y + 14)], fill=c)
        draw.line([(x + 19, y + 26), (x + 24, y + 32), (x + 33, y + 20)], fill=color, width=3)
    elif kind == "chip":  # Huawei
        draw.rectangle([x + 14, y + 14, x + 38, y + 38], fill=c)
        draw.rectangle([x + 21, y + 21, x + 31, y + 31], fill=color)
        for px in (18, 26, 34):
            draw.line([(x + px, y + 8), (x + px, y + 14)], fill=c, width=2)
            draw.line([(x + px, y + 38), (x + px, y + 44)], fill=c, width=2)
            draw.line([(x + 8, y + px), (x + 14, y + px)], fill=c, width=2)
            draw.line([(x + 38, y + px), (x + 44, y + px)], fill=c, width=2)
    elif kind == "tanker":  # Hormuz mines
        draw.polygon([(x + 8, y + 30), (x + 44, y + 30), (x + 38, y + 42),
                      (x + 12, y + 42)], fill=c)
        draw.rectangle([x + 28, y + 18, x + 36, y + 30], fill=c)
        draw.ellipse([x + 12, y + 12, x + 20, y + 20], fill=(255, 210, 90))
        draw.line([(x + 8, y + 46), (x + 44, y + 46)], fill=c, width=2)
    elif kind == "dove":  # Gaza
        draw.ellipse([x + 12, y + 22, x + 34, y + 34], fill=c)
        draw.polygon([(x + 32, y + 24), (x + 44, y + 14), (x + 40, y + 28)], fill=c)
        draw.ellipse([x + 28, y + 18, x + 34, y + 24], fill=c)
        draw.line([(x + 14, y + 40), (x + 38, y + 40)], fill=c, width=2)
    elif kind == "ballot":  # Punjab
        draw.rectangle([x + 12, y + 18, x + 40, y + 42], fill=c)
        draw.rectangle([x + 20, y + 12, x + 32, y + 18], fill=c)
        draw.line([(x + 17, y + 30), (x + 23, y + 36), (x + 35, y + 22)], fill=color, width=3)
    elif kind == "bat":  # cricket
        draw.line([(x + 14, y + 42), (x + 34, y + 14)], fill=c, width=6)
        draw.ellipse([x + 34, y + 8, x + 44, y + 18], fill=(255, 210, 90))
    elif kind == "coral":  # reef
        for bx, bh in [(14, 26), (24, 34), (34, 24)]:
            draw.line([(x + bx, y + 44), (x + bx, y + 44 - bh)], fill=c, width=4)
            draw.ellipse([x + bx - 4, y + 40 - bh, x + bx + 4, y + 48 - bh], fill=c)
    elif kind == "pad":  # GTA 6
        draw.rounded_rectangle([x + 10, y + 16, x + 42, y + 36], radius=8, fill=c)
        draw.ellipse([x + 16, y + 23, x + 21, y + 28], fill=color)
        draw.ellipse([x + 31, y + 23, x + 36, y + 28], fill=color)
        draw.line([(x + 24, y + 22), (x + 28, y + 22)], fill=color, width=2)
    elif kind == "mountain":  # Nepal aid
        draw.polygon([(x + 8, y + 42), (x + 22, y + 16), (x + 36, y + 42)], fill=c)
        draw.polygon([(x + 22, y + 16), (x + 28, y + 26), (x + 18, y + 26)], fill=color)
        draw.polygon([(x + 26, y + 42), (x + 38, y + 24), (x + 46, y + 42)], fill=(220, 220, 220))
    elif kind == "scope":  # Vera Rubin
        draw.line([(x + 12, y + 40), (x + 40, y + 14)], fill=c, width=5)
        draw.ellipse([x + 34, y + 8, x + 46, y + 20], fill=c)
        for sx, sy in [(16, 14), (26, 10), (40, 30)]:
            d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 210, 90))


GRID = [
    ("shield", (31, 80, 160), "CIA & ODNI BREACHED",
     "US spy agencies hit; unclassified data taken in cyber raid."),
    ("chip", (178, 34, 34), "HUAWEI GUILTY",
     "US jury convicts on trade-secret theft; racketeering cleared."),
    ("tanker", (196, 132, 16), "MINES IN HORMUZ",
     "Three tankers hit; shipping on edge as Gulf tensions rise."),
    ("dove", (110, 60, 150), "GAZA TOLL 74,746",
     "WAFA count rises as aid stalls and winter closes in."),
    ("ballot", (34, 120, 64), "PUNJAB PACT",
     "BJP and Akali Dal reunite ahead of the 2027 state vote."),
    ("bat", (14, 130, 130), "ENGLAND LEVEL T20",
     "Eight-wicket win over Australia; series tied 1\u20131."),
    ("coral", (200, 90, 40), "REEF REBORN",
     "Genetics work 'resurrects' 12 coral species on the Reef."),
    ("pad", (90, 60, 160), "GTA 6 IS OUT",
     "Rockstar's epic lands worldwide on PS5 and Xbox."),
    ("mountain", (60, 90, 40), "NEPAL AID PLEDGE",
     "India offers \u20b915,000 crore after devastating floods."),
    ("scope", (20, 40, 90), "VERA RUBIN SEES ALL",
     "First images 'stop the world', astronomers say."),
]
for i, (kind, color, head, deck) in enumerate(GRID):
    gx = MX + (i % GCOLS) * (GW + 10)
    gy = GY + (i // GCOLS) * (GH + 8)
    icon(d, gx, gy, kind, color)
    tx = gx + 60
    tw = GW - 60
    para(d, tx, gy + 1, head, font(SANS_B, 10), tw, leading=1)
    para(d, tx, gy + 26, deck, font(SANS, 9), tw, fill=MUTED, leading=1)
hline(d, MX, W - MX, GY + GROWS * GH + 8, 1)

# ---------------------------------------------------------------- world map
MY = 708
d.text((MX, MY), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
d.text((W - MX - d.textlength("25 NOVEMBER 2026 \u00b7 ALL TIMES LOCAL",
                              font=font(SANS, 9)), MY + 2),
       "25 NOVEMBER 2026 \u00b7 ALL TIMES LOCAL", font=font(SANS, 9), fill=MUTED)
MAPX, MAPY, MAPW, MAPH = MX, MY + 16, W - 2 * MX, 84


def ll(lon, lat):
    return (MAPX + (lon + 180) / 360 * MAPW,
            MAPY + (85 - lat) / 145 * MAPH)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-117, 32), (-125, 40), (-124, 48), (-140, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-70, -54), (-73, -40), (-75, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29),
     (25, -34), (18, -35), (12, -18), (9, -1), (-8, 4)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68),
     (45, 68), (50, 69), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40),
     (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    [(32, 70), (45, 68), (55, 69), (70, 72), (90, 75), (110, 76), (130, 72),
     (160, 70), (178, 66), (170, 60), (162, 56), (158, 50), (142, 45),
     (140, 40), (130, 35), (127, 33), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (75, 8),
     (70, 25), (60, 25), (55, 27), (50, 29), (48, 30), (44, 29), (40, 35),
     (36, 36), (32, 40), (30, 45), (28, 50), (30, 55), (30, 60)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]
for poly in CONTINENTS:
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=(224, 224, 224),
              outline=(190, 190, 190))
DOTS = [
    ("WASHINGTON", -77, 38.9, -4, -14),
    ("LONDON", -0.1, 51.5, -52, -6),
    ("KYIV", 30.5, 50.4, -28, -13),
    ("BENGHAZI", 20.1, 32.1, -58, 8),
    ("ANTALYA", 30.7, 36.9, 8, -13),
    ("TEHRAN", 51.4, 35.7, 6, -13),
    ("GAZA", 34.5, 31.5, -8, 10),
    ("DELHI", 77.2, 28.6, 6, 8),
    ("RIYADH", 46.7, 24.7, -6, 12),
    ("BEIJING", 116.4, 39.9, 6, -12),
]
for name, lon, lat, dx, dy in DOTS:
    x, y = ll(lon, lat)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=(255, 255, 255),
              width=1)
    d.text((x + dx, y + dy), name, font=font(SANS_B, 8), fill=INK)

# ---------------------------------------------------------------- 22 more stories
LY = 820
hline(d, MX, W - MX, LY - 6, 1)
d.text((MX, LY), "22 MORE STORIES", font=font(SANS_B, 12), fill=INK)
MORE = [
    "Russia calls the Libya ship strikes \u201cterrorism\u201d, vows a response",
    "NATO to send early-warning jets to Poland after missile reports",
    "Kushner: NATO-like guarantees for Ukraine are possible",
    "Kyiv flat hit by drones; 11 killed near the capital",
    "Iran rations power as its grid reels from strikes",
    "Iran faces winter gas shortage as war damage deepens",
    "Oxfam: pollution risks cover 99% of Gaza",
    "WFP: 266 million people face acute food insecurity",
    "Israeli army suicides hit a 16-year high: 23 in 2026",
    "Trump awards Giuliani the Medal of Freedom",
    "Trump blasts Newsom death-row commutations at the DOJ",
    "GOP breaks with Trump over Huang's return",
    "Congress to probe chip exports; 879,000 chips reached China",
    "Dell lifts outlook on a record AI-server quarter",
    "EU readies fresh sanctions on Russia",
    "Nepal PM ends India visit; \u20b915,000 crore aid pledged",
    "India factory activity hits a nine-month high",
    "Denmark court upholds \u201cghetto\u201d evictions",
    "RFE/RL back on shortwave for Afghan girls",
    "Houthi drone hits Riyadh tower; 11 hurt",
    "Venezuela reports public debt of $237.5B",
    "Asteroid eclipse snapped: Didymos shadows Dimorphos",
]
f_num = font(SANS, 10)
col2x = MX + (W - 2 * MX) // 2 + 8
for i, story in enumerate(MORE):
    col = 0 if i < 11 else 1
    row = i % 11
    x = MX if col == 0 else col2x
    y = LY + 18 + row * 14
    d.text((x, y), f"{i + 1}.", font=font(SANS_B, 10), fill=RED)
    d.text((x + 22, y), story, font=f_num, fill=INK)

# ---------------------------------------------------------------- footer
hline(d, MX, W - MX, 1000, 1)
d.text((MX, 1005),
       "DATE CHECK \u2014 Every story verified against reporting dated 25 November 2026.",
       font=font(SANS, 9), fill=MUTED)
d.text((W - MX - d.textlength("The Daily Chronicle \u00b7 One page, the whole world.",
                              font=font(SANS, 9)), 1005),
       "The Daily Chronicle \u00b7 One page, the whole world.",
       font=font(SANS, 9), fill=MUTED)

img.save("entry.png")
print("saved entry.png", img.size)
