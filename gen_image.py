#!/usr/bin/env python3
"""Render the front-page infographic for Saturday 21 November 2026.

Draws one 1024x1024 PNG with Pillow: a newspaper masthead, one lead
story, two middle stories and three lower stories, all verified news
from that day. Run from the entry directory; writes entry.png beside
this file. No network, no input files.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

PAPER = (246, 241, 227)
INK = (31, 36, 48)
SOFT_INK = (74, 78, 88)
CARD = (255, 255, 255)
CARD_EDGE = (198, 190, 168)
RED = (179, 38, 30)
NAVY = (31, 56, 100)
GOLD = (146, 104, 12)
TEAL = (15, 118, 110)
PURPLE = (107, 33, 168)
GREEN = (22, 101, 52)
PALE_RED = (253, 236, 236)
PALE_BLUE = (232, 238, 248)
PALE_GOLD = (248, 240, 214)
PALE_TEAL = (224, 242, 240)
PALE_PURPLE = (240, 232, 250)
PALE_GREEN = (228, 242, 230)
FOOTER_GREY = (110, 108, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def serif_bold(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def sans_bold(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def wrap_lines(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(draw, x, y, width, text, font, fill, leading, align="left"):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap_lines(draw, text, font, width):
        if align == "center":
            lx = x + (width - draw.textlength(line, font=font)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_centred(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def star_points(cx, cy, outer, inner, spikes=8, tilt=-math.pi / 2):
    pts = []
    for i in range(spikes * 2):
        r = outer if i % 2 == 0 else inner
        a = tilt + i * math.pi / spikes
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rotated_point(cx, cy, dx, dy, angle):
    c, s = math.cos(angle), math.sin(angle)
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def missile_and_blast(draw, box):
    """Slim diagonal missile crossing a burst star, pale red panel."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    draw.rectangle(box, fill=PALE_RED)
    draw.polygon(star_points(cx - 62, cy + 8, 44, 17), fill=(244, 196, 116))
    draw.polygon(star_points(cx - 62, cy + 8, 26, 10), fill=(250, 220, 150))
    ang = -math.radians(28)
    nose = rotated_point(cx, cy, 96, 0, ang)
    tail_top = rotated_point(cx, cy, -62, -13, ang)
    tail_bot = rotated_point(cx, cy, -62, 13, ang)
    mid_top = rotated_point(cx, cy, 26, -11, ang)
    mid_bot = rotated_point(cx, cy, 26, 11, ang)
    fin_top = rotated_point(cx, cy, -78, -34, ang)
    fin_bot = rotated_point(cx, cy, -78, 34, ang)
    fin_mid = rotated_point(cx, cy, -48, -9, ang)
    fin_mid2 = rotated_point(cx, cy, -48, 9, ang)
    draw.polygon([nose, mid_top, tail_top, fin_top, fin_mid, tail_bot,
                  fin_bot, fin_mid2, mid_bot], fill=RED)
    draw.polygon([rotated_point(cx, cy, -62, -6, ang),
                  rotated_point(cx, cy, -92, -3, ang),
                  rotated_point(cx, cy, -62, 6, ang)], fill=(122, 22, 18))
    for k in range(3):
        off = k * 14
        draw.line([rotated_point(cx, cy, -104 - k * 5, -40 + off, ang),
                   rotated_point(cx, cy, -84 - k * 5, -40 + off, ang)],
                  fill=RED, width=4)
    bx, by = cx + 88, cy - 72
    draw.polygon(star_points(bx, by, 22, 9), fill=RED)
    draw.text((bx - 5, by - 13), "!", font=sans_bold(22),
              fill=(255, 255, 255))


def falling_chart(draw, box):
    """Line chart diving down over three bars; fits a ~92px strip."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PALE_GOLD)
    base = y1 - 10
    gx = x0 + 18
    for h in (40, 30, 20):
        draw.rectangle([gx, base - h, gx + 28, base], fill=(178, 134, 34))
        gx += 42
    pts = [(x0 + 24, y0 + 14), (x0 + 80, y0 + 32), (x0 + 140, y0 + 28),
           (x0 + 200, y0 + 62), (x0 + 244, y1 - 16)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
    draw.polygon([(x0 + 244, y1 - 16), (x0 + 222, y1 - 24),
                  (x0 + 228, y1 - 2)], fill=RED)
    label = "-3.7%"
    lw = draw.textlength(label, font=sans_bold(20))
    draw.text((x1 - lw - 14, y0 + 8), label, font=sans_bold(20), fill=RED)


def scales_of_justice(draw, box):
    """A balance scale: post, beam, two hanging pans, base."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    draw.rectangle(box, fill=PALE_BLUE)
    top = y0 + 6
    draw.line([cx, top, cx, y1 - 16], fill=NAVY, width=6)
    draw.line([cx - 70, top + 8, cx + 70, top + 8], fill=NAVY, width=5)
    draw.ellipse([cx - 7, top - 6, cx + 7, top + 8], fill=NAVY)
    for side in (-1, 1):
        px = cx + side * 70
        draw.line([px, top + 8, px - 22, top + 42], fill=NAVY, width=3)
        draw.line([px, top + 8, px + 22, top + 42], fill=NAVY, width=3)
        draw.line([px, top + 8, px, top + 42], fill=NAVY, width=3)
        draw.pieslice([px - 25, top + 36, px + 25, top + 64],
                      start=0, end=180, fill=NAVY)
    draw.polygon([(cx - 28, y1 - 16), (cx + 28, y1 - 16), (cx, y1 - 34)],
                 fill=NAVY)
    draw.rectangle([cx - 44, y1 - 16, cx + 44, y1 - 6], fill=NAVY)


def medallion(draw, cx, cy, colour, glyph):
    """Small coloured disc holding a white mini pictogram."""
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=colour)
    glyph(draw, cx, cy)


def mini_padlock(draw, cx, cy):
    draw.arc([cx - 10, cy - 16, cx + 10, cy + 4], start=180, end=360,
             fill=(255, 255, 255), width=4)
    draw.rounded_rectangle([cx - 13, cy - 2, cx + 13, cy + 18],
                           radius=3, fill=(255, 255, 255))
    draw.ellipse([cx - 3, cy + 3, cx + 3, cy + 9], fill=TEAL)
    draw.polygon([(cx - 2, cy + 7), (cx + 2, cy + 7), (cx + 4, cy + 14),
                  (cx - 4, cy + 14)], fill=TEAL)


def mini_globe(draw, cx, cy):
    draw.ellipse([cx - 17, cy - 17, cx + 17, cy + 17],
                 outline=(255, 255, 255), width=3)
    draw.ellipse([cx - 7, cy - 17, cx + 7, cy + 17],
                 outline=(255, 255, 255), width=2)
    draw.line([cx - 17, cy, cx + 17, cy], fill=(255, 255, 255), width=2)


def mini_ballot(draw, cx, cy):
    draw.rectangle([cx - 14, cy - 2, cx + 14, cy + 18], fill=(255, 255, 255))
    draw.rectangle([cx - 8, cy - 6, cx + 8, cy - 2], fill=(255, 255, 255))
    draw.text((cx - 8, cy + 1), "✓", font=sans_bold(16), fill=GREEN)


def card_frame(draw, box):
    draw.rounded_rectangle(box, radius=10, fill=CARD, outline=CARD_EDGE,
                           width=2)


def kicker_and_headline(draw, x, y, width, tag, colour, headline, size):
    draw.text((x, y), tag, font=sans_bold(17), fill=colour)
    y += 26
    return draw_block(draw, x, y, width, headline, sans_bold(size), INK,
                      size + 6)


def build_canvas():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 1013, 1013], outline=INK, width=2)

    # ---- Masthead -------------------------------------------------
    draw_centred(d, 512, 24, "THE WORLD IN ONE PICTURE",
                 serif_bold(42), INK)
    d.rectangle([60, 88, 964, 92], fill=RED)
    d.rectangle([60, 96, 964, 98], fill=RED)
    draw_centred(d, 512, 106, "SATURDAY  ·  21 NOVEMBER 2026",
                 sans_bold(29), RED)

    # ---- Lead story: Poland ---------------------------------------
    card_frame(d, [26, 150, 998, 392])
    missile_and_blast(d, [27, 151, 280, 391])
    tx = 302
    y = kicker_and_headline(d, tx, 166, 670, "CONFLICT  ·  POLAND", RED,
                            "RUSSIAN MISSILE LANDS IN POLAND", 37)
    y += 8
    draw_block(d, tx, y, 670,
               "A Kh-101 cruise missile and a drone came down in the "
               "south-east during a huge overnight attack on Ukraine — "
               "400+ drones and 110 missiles, at least eight killed. "
               "Poland's PM calls it a deliberate provocation; NATO, a "
               "grave violation.",
               sans(20), SOFT_INK, 26)

    # ---- Middle row: Markets + Justice ----------------------------
    mid_y0, mid_y1 = 406, 672
    middle = [
        ([26, mid_y0, 505, mid_y1], falling_chart, "MARKETS  ·  NEW YORK",
         GOLD, "WALL STREET FALLS INTO CORRECTION",
         "The S&P 500 drops 3.7% and the Nasdaq 5.3% as the AI sell-off "
         "deepens. Anthropic slides 8.5% on its second day listed; "
         "Nvidia falls 14%."),
        ([519, mid_y0, 998, mid_y1], scales_of_justice,
         "JUSTICE  ·  THE HAGUE", NAVY, "MYANMAR FOUND GUILTY OF GENOCIDE",
         "The World Court rules a state guilty of genocide for the "
         "first time ever, over the Rohingya. Myanmar rejects the "
         "verdict."),
    ]
    for box, art, tag, colour, head, body in middle:
        card_frame(d, box)
        art(d, [box[0] + 1, box[1] + 1, box[2] - 1, box[1] + 93])
        cx = (box[0] + box[2]) / 2
        inner = box[2] - box[0] - 44
        y = box[1] + 102
        tw = d.textlength(tag, font=sans_bold(16))
        d.text((cx - tw / 2, y), tag, font=sans_bold(16), fill=colour)
        y += 26
        y = draw_block(d, box[0] + 22, y, inner, head, sans_bold(25), INK,
                       30, align="center")
        draw_block(d, box[0] + 22, y + 8, inner, body, sans(18), SOFT_INK,
                   22, align="center")

    # ---- Bottom row: Cyber, Diplomacy, Politics -------------------
    bot_y0, bot_y1 = 686, 946
    slots = [
        ([26, bot_y0, 340, bot_y1], TEAL, mini_padlock,
         "CYBER  ·  FINANCE", "HACKERS STRIKE JPMORGAN, VISA, MASTERCARD",
         "Customer names and emails leak via outside suppliers. No card "
         "numbers are taken. A gang calling itself “n0n” claims it."),
        ([355, bot_y0, 669, bot_y1], PURPLE, mini_globe,
         "DIPLOMACY  ·  BRUSSELS", "UK AND EU SIGN THREE NEW DEALS",
         "Food trade, carbon markets and youth mobility: three "
         "agreements are signed at a summit in Brussels."),
        ([684, bot_y0, 998, bot_y1], GREEN, mini_ballot,
         "POLITICS  ·  ISRAEL", "EISENKOT ASKED TO FORM A GOVERNMENT",
         "President Herzog turns to the former army chief to build a "
         "coalition, passing over Prime Minister Netanyahu."),
    ]
    for box, colour, glyph, tag, head, body in slots:
        card_frame(d, box)
        medallion(d, box[0] + 37, box[1] + 37, colour, glyph)
        inner = box[2] - box[0] - 30
        d.text((box[0] + 66, box[1] + 28), tag, font=sans_bold(15),
               fill=colour)
        y = box[1] + 66
        y = draw_block(d, box[0] + 15, y, inner, head, sans_bold(23), INK,
                       28, align="center")
        draw_block(d, box[0] + 15, y + 7, inner, body, sans(17), SOFT_INK,
                   22, align="center")

    # ---- Footer ----------------------------------------------------
    draw_centred(d, 512, 960,
                 "Sources: AP · Reuters · BBC · UN News · CNN · Le Monde",
                 sans(16), FOOTER_GREY)
    draw_centred(d, 512, 982,
                 "All six stories first reported on Saturday 21 November 2026",
                 sans_bold(16), FOOTER_GREY)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "entry.png")
    build_canvas().save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
