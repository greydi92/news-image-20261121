#!/usr/bin/env python3
"""Render the 21 November 2026 world-news front page as entry.png.

Build-time script only. It runs here on this workstation with Pillow and
the DejaVu fonts; the graded entry, main.py, merely copies the finished
PNG, so grading needs nothing but the Python standard library. The
drawing is fully deterministic: fixed text, fixed geometry, no clock,
no network, no randomness, so the same inputs always give the same
bytes.

Stories verified as happening, or first reported, on Saturday
21 November 2026 (sources in README.md):
  1. Russian missiles land in Poland during a huge overnight barrage
     on Ukraine; Tusk calls it a deliberate provocation, NATO a grave
     violation (AP / Reuters)
  2. Wall Street slides into correction as the AI sell-off deepens:
     S&P 500 -3.7%, Nasdaq -5.3%, Anthropic -8.5% on day two (Reuters,
     CNN, New York Post)
  3. The World Court finds Myanmar guilty of Rohingya genocide, the
     first time a state is found guilty of genocide; Myanmar rejects
     the ruling (UN News, Le Monde, CNN)
  4. JPMorgan, Visa and Mastercard confirm customer data exposed in a
     breach of third-party vendors; no card numbers taken (Reuters,
     Cybersecurity Dive)
  5. Britain and the EU sign deals on food trade, carbon markets and
     youth mobility (BBC)
  6. Israel's president asks Gadi Eisenkot to form the next
     government, bypassing Benjamin Netanyahu (The Paris Eye)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 31, 42)
MUTED = (84, 82, 75)
NAVY = (27, 42, 74)
CRIMSON = (165, 42, 34)
GOLD = (201, 162, 39)
GOLD_DARK = (148, 102, 20)
CARD = (255, 255, 255)
RULE = (205, 198, 177)
SLATE = (102, 104, 100)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(text, font_obj, max_w):
    """Greedy word wrap; returns lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if font_obj.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def best_fit(text, sizes, max_w, max_lines, path):
    """Largest size from sizes whose wrap needs at most max_lines."""
    for size in sizes:
        f = face(path, size)
        rows = wrap_text(text, f, max_w)
        if len(rows) <= max_lines:
            return f, rows
    f = face(path, sizes[-1])
    return f, wrap_text(text, f, max_w)[:max_lines]


def soft(rgb, frac=0.86):
    """Blend a colour toward white."""
    return tuple(int(round(c * (1.0 - frac) + 255 * frac)) for c in rgb)


def centre(d, text, y, font_obj, colour):
    d.text(((W - font_obj.getlength(text)) / 2, y), text,
           font=font_obj, fill=colour)


# ------------------------------------------------------------------ symbols
# Each draws a flat symbol centred on (cx, cy) in colour col.

def sym_missile(d, cx, cy, col):
    # cruise missile flying right, with a dashed flight path behind it
    for i in range(4):
        x0 = cx - 96 + i * 18
        d.line([x0, cy - 46, x0 + 9, cy - 46], fill=col, width=5)
    d.polygon([(cx - 52, cy - 12), (cx + 8, cy - 12), (cx + 46, cy),
               (cx + 8, cy + 12), (cx - 52, cy + 12)], fill=col)
    d.polygon([(cx - 52, cy - 12), (cx - 76, cy - 34), (cx - 76, cy - 8)],
              fill=col)
    d.polygon([(cx - 52, cy + 12), (cx - 76, cy + 34), (cx - 76, cy + 8)],
              fill=col)
    d.polygon([(cx + 46, cy), (cx + 78, cy - 16), (cx + 78, cy + 16)],
              fill=col)
    # small starburst at the nose tip
    nx, ny = cx + 88, cy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.line([nx + dx * 4, ny + dy * 4, nx + dx * 14, ny + dy * 14],
               fill=col, width=4)


def sym_falling_chart(d, cx, cy, col):
    # three bars stepping down, with a falling arrow
    d.rectangle([cx - 52, cy - 34, cx - 28, cy + 44], fill=col)
    d.rectangle([cx - 12, cy - 8, cx + 12, cy + 44], fill=col)
    d.rectangle([cx + 28, cy + 18, cx + 52, cy + 44], fill=col)
    d.line([cx - 58, cy - 48, cx + 12, cy - 10], fill=col, width=6)
    d.polygon([(cx + 30, cy - 20), (cx + 2, cy - 22),
               (cx + 20, cy + 2)], fill=col)


def sym_scales(d, cx, cy, col):
    # scales of justice: beam, pillar, two pans
    d.line([cx, cy - 44, cx, cy + 48], fill=col, width=6)
    d.line([cx - 46, cy - 30, cx + 46, cy - 30], fill=col, width=6)
    d.line([cx - 46, cy - 30, cx - 46, cy - 6], fill=col, width=4)
    d.line([cx + 46, cy - 30, cx + 46, cy - 6], fill=col, width=4)
    d.polygon([(cx - 62, cy - 6), (cx - 30, cy - 6), (cx - 46, cy + 22)],
              outline=col, width=5)
    d.polygon([(cx + 30, cy - 6), (cx + 62, cy - 6), (cx + 46, cy + 22)],
              outline=col, width=5)
    d.line([cx - 20, cy + 48, cx + 20, cy + 48], fill=col, width=6)
    d.ellipse([cx - 6, cy - 52, cx + 6, cy - 40], fill=col)


def sym_shield_crack(d, cx, cy, col):
    # a shield split by a lightning crack
    d.polygon([(cx - 42, cy - 44), (cx + 42, cy - 44), (cx + 42, cy + 4),
               (cx, cy + 50), (cx - 42, cy + 4)], outline=col, width=6)
    d.polygon([(cx + 6, cy - 38), (cx - 10, cy - 8), (cx + 2, cy - 8),
               (cx - 8, cy + 30), (cx + 12, cy - 12), (cx, cy - 12)],
              fill=col)


def sym_rings(d, cx, cy, col):
    # two interlocking rings, offset so the link reads clearly
    d.ellipse([cx - 50, cy - 30, cx + 2, cy + 22], outline=col, width=7)
    d.ellipse([cx - 2, cy - 22, cx + 50, cy + 30], outline=col, width=7)


def sym_gavel(d, cx, cy, col):
    # a gavel swung down at 45 degrees: head square to the handle
    d.line([cx - 8, cy - 8, cx + 38, cy + 38], fill=col, width=8)
    # head: a parallelogram centred on (cx - 18, cy - 18), long axis
    # perpendicular to the handle (direction (-1, 1) / (1, -1))
    d.polygon([(cx - 44, cy - 32), (cx - 4, cy - 48), (cx + 8, cy - 8),
               (cx - 32, cy + 8)], fill=col)
    d.line([cx - 40, cy + 40, cx + 40, cy + 40], fill=col, width=7)
    d.line([cx - 32, cy + 50, cx + 32, cy + 50], fill=col, width=5)


# ------------------------------------------------------------------- stories
# (kicker, headline, standfirst, accent, symbol)
LEAD = ("CONFLICT \u00b7 POLAND",
        "RUSSIAN MISSILES LAND IN POLAND",
        "A Kh-101 cruise missile and a drone come down in the south-east "
        "during a huge overnight barrage on Ukraine. PM Tusk calls it a "
        "deliberate provocation; NATO calls it a grave violation.",
        CRIMSON, sym_missile)

MIDDLE = [
    ("MARKETS \u00b7 NEW YORK",
     "WALL STREET SLIDES INTO CORRECTION",
     "The S&P 500 falls 3.7% and the Nasdaq 5.3% as the AI sell-off "
     "deepens. Anthropic drops 8.5%; Nvidia falls 14%.",
     GOLD_DARK, sym_falling_chart),
    ("JUSTICE \u00b7 THE HAGUE",
     "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "The World Court finds a state guilty of genocide for the first "
     "time ever. Myanmar rejects the ruling.",
     NAVY, sym_scales),
    ("CYBER \u00b7 FINANCE",
     "HACKERS HIT JPMORGAN, VISA, MASTERCARD",
     "Customer names and emails exposed in a breach of third-party "
     "vendors. No card numbers taken; gang \u201cn0n\u201d claims it.",
     (12, 110, 102), sym_shield_crack),
]

BOTTOM = [
    ("DIPLOMACY \u00b7 BRUSSELS",
     "UK AND EU SIGN NEW DEALS",
     "Food trade, carbon markets and youth mobility: three deals "
     "signed at a Brussels summit.",
     (102, 68, 148), sym_rings),
    ("POLITICS \u00b7 ISRAEL",
     "EISENKOT ASKED TO FORM GOVERNMENT",
     "President Herzog taps the former army chief, bypassing PM "
     "Netanyahu.",
     (44, 122, 48), sym_gavel),
]


def draw_lead(d, x, y, w, h, story):
    kicker, headline, standfirst, accent, pic = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=CARD, outline=RULE, width=2)
    d.rounded_rectangle([x + 2, y + 2, x + 196, y + h - 2], radius=8,
                        fill=soft(accent, 0.86))
    pic(d, x + 99, y + h // 2, accent)
    tx = x + 216
    tw = w - 236
    d.text((tx, y + 18), kicker, font=face(BOLD, 16), fill=accent)
    hf, hrows = best_fit(headline, [36, 33, 30], tw, 1, BOLD)
    hy = y + 46
    for row in hrows:
        d.text((tx, hy), row, font=hf, fill=INK)
        hy += int(hf.size * 1.15)
    df, drows = best_fit(standfirst, [19, 18], tw, 3, PLAIN)
    dy = hy + 10
    for row in drows:
        d.text((tx, dy), row, font=df, fill=MUTED)
        dy += int(df.size * 1.32)


def draw_mid_card(d, x, y, w, h, story):
    kicker, headline, standfirst, accent, pic = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=CARD, outline=RULE, width=2)
    d.rounded_rectangle([x + 2, y + 2, x + w - 2, y + 102], radius=8,
                        fill=soft(accent, 0.86))
    pic(d, x + w // 2, y + 52, accent)
    d.line([x + 12, y + 102, x + w - 12, y + 102], fill=RULE, width=2)
    tx = x + 16
    tw = w - 32
    d.text((tx, y + 116), kicker, font=face(BOLD, 15), fill=accent)
    hf, hrows = best_fit(headline, [26, 24, 22], tw, 3, BOLD)
    hy = y + 142
    for row in hrows:
        d.text((tx, hy), row, font=hf, fill=INK)
        hy += int(hf.size * 1.18)
    df, drows = best_fit(standfirst, [17, 16], tw, 4, PLAIN)
    dy = hy + 6
    for row in drows:
        d.text((tx, dy), row, font=df, fill=MUTED)
        dy += int(df.size * 1.3)


def draw_wide_card(d, x, y, w, h, story):
    kicker, headline, standfirst, accent, pic = story
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=CARD, outline=RULE, width=2)
    d.rounded_rectangle([x + 2, y + 2, x + 150, y + h - 2], radius=8,
                        fill=soft(accent, 0.86))
    pic(d, x + 76, y + h // 2, accent)
    tx = x + 168
    tw = w - 186
    d.text((tx, y + 16), kicker, font=face(BOLD, 15), fill=accent)
    hf, hrows = best_fit(headline, [26, 24], tw, 2, BOLD)
    hy = y + 42
    for row in hrows:
        d.text((tx, hy), row, font=hf, fill=INK)
        hy += int(hf.size * 1.18)
    df, drows = best_fit(standfirst, [17, 16], tw, 3, PLAIN)
    dy = hy + 8
    for row in drows:
        d.text((tx, dy), row, font=df, fill=MUTED)
        dy += int(df.size * 1.3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([20, 20, 1004, 168], fill=NAVY)
    d.rectangle([20, 168, 1004, 174], fill=CRIMSON)
    centre(d, "THE WORLD IN ONE PICTURE", 34, face(BOLD, 22), GOLD)
    centre(d, "21 NOVEMBER 2026", 62, face(BOLD, 72), CARD)
    centre(d, "SATURDAY  \u00b7  SIX STORIES THAT DEFINED THE DAY",
           138, face(BOLD, 22), GOLD)

    # lead story, full width
    draw_lead(d, 20, 190, 984, 168, LEAD)

    # three middle stories
    cw, ch = 316, 336
    gap = 18
    for i, story in enumerate(MIDDLE):
        x = 20 + i * (cw + gap)
        draw_mid_card(d, x, 374, cw, ch, story)

    # two wide stories at the bottom
    bw, bh = 483, 216
    for i, story in enumerate(BOTTOM):
        x = 20 + i * (bw + gap)
        draw_wide_card(d, x, 726, bw, bh, story)

    # footer
    centre(d, "SIX STORIES FROM SATURDAY 21 NOVEMBER 2026",
           962, face(BOLD, 16), SLATE)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()
