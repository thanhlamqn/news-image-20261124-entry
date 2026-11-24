#!/usr/bin/env python3
"""Render the news-image-20261124 entry: one 1024x1024 newspaper front page
summing up the world news of Tuesday 24 November 2026.

Every story below was reported on 24 November 2026 (Reuters, AP, AFP, SCMP,
The Japan Times). The image is drawn with Pillow only; output is deterministic
(no timestamps, no randomness) so re-running produces identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 24, 22)
RED = (178, 34, 34)
GREEN = (34, 120, 40)
BLUE = (28, 68, 128)
GOLD = (176, 132, 24)
GREY = (96, 96, 92)
LIGHT = (233, 228, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to fit max_w pixels; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip_icon(draw, x, y, s):
    """A green AI chip with pins, an upward chart line and NVDA +31%.
    All inner geometry scales with s."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=max(8, s // 10),
                           fill=(118, 185, 0), outline=INK, width=4)
    pin_w, pin_l = max(6, s // 14), max(8, s // 12)
    for i in range(5):  # pins, top and bottom
        px = x + s // 6 + i * (s * 2 // 3) // 4 - pin_w // 2
        draw.rectangle([px, y - pin_l, px + pin_w, y], fill=INK)
        draw.rectangle([px, y + s, px + pin_w, y + s + pin_l], fill=INK)
    for j in range(5):  # pins, left and right
        py = y + s // 6 + j * (s * 2 // 3) // 4 - pin_w // 2
        draw.rectangle([x - pin_l, py, x, py + pin_w], fill=INK)
        draw.rectangle([x + s, py, x + s + pin_l, py + pin_w], fill=INK)
    inset = s // 5
    draw.rounded_rectangle([x + inset, y + inset, x + s - inset,
                            y + s - inset], radius=10, fill=(24, 60, 10))
    draw.text((x + s // 2, y + int(s * 0.33)), "NVDA",
              font=font(SANS_B, int(s * 0.20)),
              fill=(255, 255, 255), anchor="ma")
    draw.text((x + s // 2, y + int(s * 0.57)), "+31%",
              font=font(SANS_B, int(s * 0.22)),
              fill=(255, 255, 255), anchor="ma")


def ship_icon(draw, x, y, s, color):
    """A warship on waves, drawn from simple shapes."""
    u = s / 64.0
    draw.polygon([(x + 6 * u, y + 40 * u), (x + 58 * u, y + 40 * u),
                  (x + 50 * u, y + 52 * u), (x + 14 * u, y + 52 * u)],
                 fill=color)
    draw.rectangle([x + 26 * u, y + 26 * u, x + 38 * u, y + 40 * u],
                   fill=color)
    draw.rectangle([x + 31 * u, y + 12 * u, x + 33 * u, y + 26 * u],
                   fill=color)
    draw.polygon([(x + 33 * u, y + 12 * u), (x + 44 * u, y + 18 * u),
                  (x + 33 * u, y + 20 * u)], fill=RED)
    for i, wx in enumerate([2, 20, 38]):
        draw.arc([x + wx * u, y + 54 * u, x + (wx + 16) * u, y + 62 * u],
                 start=180, end=360, fill=BLUE, width=max(2, int(2 * u)))


def satellite_icon(draw, x, y, s, color):
    """A satellite with two solar panels and a signal arc."""
    u = s / 64.0
    draw.rectangle([x + 6 * u, y + 28 * u, x + 20 * u, y + 36 * u],
                   fill=color)
    draw.rectangle([x + 28 * u, y + 26 * u, x + 36 * u, y + 38 * u],
                   fill=color)
    draw.rectangle([x + 44 * u, y + 28 * u, x + 58 * u, y + 36 * u],
                   fill=color)
    draw.line([x + 20 * u, y + 32 * u, x + 28 * u, y + 32 * u],
              fill=color, width=max(2, int(3 * u)))
    draw.line([x + 36 * u, y + 32 * u, x + 44 * u, y + 32 * u],
              fill=color, width=max(2, int(3 * u)))
    draw.line([x + 32 * u, y + 26 * u, x + 32 * u, y + 14 * u],
              fill=color, width=max(2, int(3 * u)))
    draw.ellipse([x + 29 * u, y + 10 * u, x + 35 * u, y + 16 * u],
                 fill=RED)
    draw.arc([x + 40 * u, y + 6 * u, x + 58 * u, y + 24 * u],
             start=270, end=90, fill=RED, width=max(2, int(3 * u)))


def blast_icon(draw, x, y, s, color):
    """An explosion starburst."""
    import math
    cx, cy = x + s / 2, y + s / 2
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        r = s * 0.48 if i % 2 == 0 else s * 0.20
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13],
                 fill=(255, 214, 64))


def gavel_icon(draw, x, y, s, color):
    """Scales of justice: beam, post and two pans."""
    u = s / 64.0
    draw.rectangle([x + 30 * u, y + 12 * u, x + 34 * u, y + 50 * u],
                   fill=color)
    draw.rectangle([x + 10 * u, y + 16 * u, x + 54 * u, y + 20 * u],
                   fill=color)
    draw.polygon([(x + 26 * u, y + 12 * u), (x + 38 * u, y + 12 * u),
                  (x + 32 * u, y + 6 * u)], fill=color)
    for cx in (14, 50):
        draw.line([x + cx * u, y + 20 * u, x + (cx - 8) * u, y + 36 * u],
                  fill=color, width=max(2, int(2 * u)))
        draw.line([x + cx * u, y + 20 * u, x + (cx + 8) * u, y + 36 * u],
                  fill=color, width=max(2, int(2 * u)))
        draw.pieslice([x + (cx - 9) * u, y + 34 * u, x + (cx + 9) * u,
                       y + 48 * u], start=0, end=180, fill=color)
    draw.rectangle([x + 20 * u, y + 52 * u, x + 44 * u, y + 56 * u],
                   fill=color)


def chat_icon(draw, x, y, s, color):
    """A chat bubble with AI inside."""
    draw.rounded_rectangle([x + 4, y + 10, x + s - 4, y + s - 18],
                           radius=12, fill=color)
    draw.polygon([(x + 16, y + s - 18), (x + 16, y + s - 2),
                  (x + 32, y + s - 18)], fill=color)
    draw.text((x + s // 2, y + s // 2 - 6), "AI", font=font(SANS_B, 26),
              fill=(255, 255, 255), anchor="mm")


def flag_icon(draw, x, y, s, color):
    """Two crossed flags on poles."""
    u = s / 64.0
    draw.line([x + 14 * u, y + 8 * u, x + 14 * u, y + 56 * u],
              fill=INK, width=max(2, int(3 * u)))
    draw.line([x + 50 * u, y + 8 * u, x + 50 * u, y + 56 * u],
              fill=INK, width=max(2, int(3 * u)))
    draw.polygon([(x + 14 * u, y + 10 * u), (x + 34 * u, y + 16 * u),
                  (x + 14 * u, y + 24 * u)], fill=RED)
    draw.polygon([(x + 50 * u, y + 10 * u), (x + 30 * u, y + 16 * u),
                  (x + 50 * u, y + 24 * u)], fill=color)
    draw.rectangle([x + 8 * u, y + 54 * u, x + 56 * u, y + 58 * u],
                   fill=GOLD)


ICONS = {"chip": chip_icon, "ship": ship_icon, "satellite": satellite_icon,
         "blast": blast_icon, "gavel": gavel_icon, "chat": chat_icon,
         "flag": flag_icon}


def icon_tile(fn, color):
    """Render an icon function onto a transparent 64x64 tile."""
    tile = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    fn(ImageDraw.Draw(tile), 0, 0, 64, color)
    return tile


def panel(img, draw, x, y, w, h, kicker, headline, deck, accent, icon):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 32], fill=accent)
    draw.text((x + 12, y + 16), kicker, font=font(SANS_B, 18),
              fill=(255, 255, 255), anchor="lm")
    tile = icon_tile(ICONS[icon], (255, 255, 255)).resize((26, 26),
                                                          Image.LANCZOS)
    img.paste(tile, (x + w - 34, y + 3), tile)
    hl = wrap(draw, headline, font(SANS_B, 24), w - 24)
    draw_lines(draw, hl, x + 12, y + 44, font(SANS_B, 24), INK, 27)
    dk = wrap(draw, deck, font(SANS, 18), w - 24)
    draw_lines(draw, dk, x + 12, y + 44 + len(hl) * 27 + 8,
               font(SANS, 18), (52, 52, 48), 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # Masthead
    d.text((W // 2, 56), "THE WORLD IN ONE PICTURE",
           font=font(SERIF_B, 46), fill=INK, anchor="ma")
    d.text((W // 2, 100), "THE DAY'S NEWS  ·  IN ONE IMAGE",
           font=font(SANS_B, 18), fill=RED, anchor="ma")
    d.rectangle([28, 126, W - 29, 172], fill=INK)
    d.text((W // 2, 149), "TUESDAY  ·  24 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=(255, 255, 255), anchor="mm")

    # Lead story: Nvidia
    lx, ly, lw, lh = 28, 184, W - 56, 234
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 34], fill=GREEN)
    d.text((lx + 12, ly + 17), "LEAD  ·  MARKETS & AI",
           font=font(SANS_B, 19), fill=(255, 255, 255), anchor="lm")
    chip_icon(d, lx + 24, ly + 58, 150)
    tx = lx + 250
    head = wrap(d, "HUANG IS BACK AT NVIDIA", font(SANS_B, 44), lw - 274)
    draw_lines(d, head, tx, ly + 50, font(SANS_B, 44), INK, 50)
    deck = ("Board reinstates Jensen Huang as chief executive after "
            "pressure from President Trump, 11 days after he resigned. "
            "Shares soar 31%, adding about $950bn; the Nasdaq jumps 6.5%.")
    dl = wrap(d, deck, font(SANS, 23), lw - 274)
    draw_lines(d, dl, tx, ly + 50 + len(head) * 50 + 10,
               font(SANS, 23), (52, 52, 48), 28)

    # Rows of three panels
    pw, ph, gap = 304, 234, 16
    y2, y3 = 430, 676
    row2 = [
        ("WAR AT SEA", "Ukraine sinks Russian warship off Libya",
         "Sea drones strike Benghazi port; a cargo ship is hit and a "
         "helicopter destroyed, Kyiv says.", BLUE, "ship"),
        ("SPACE ALARM", "NATO: Russia may launch a nuclear space weapon",
         "Allies warn Moscow could put an anti-satellite weapon in "
         "orbit within weeks.", RED, "satellite"),
        ("KYIV UNDER FIRE", "Russian strikes kill 15 near Kyiv",
         "Overnight barrage follows Putin's vow of a 'painful' reply "
         "to bridge damage.", (120, 60, 20), "blast"),
    ]
    row3 = [
        ("WASHINGTON", "Trump orders federal executions sped up",
         "President directs the Justice Department to expedite death "
         "sentences.", INK, "gavel"),
        ("TECH ON TRIAL", "States sue Musk firms over Grok images",
         "US states allege the AI chatbot generated sexualised images "
         "of people.", (90, 40, 110), "chat"),
        ("MANILA", "Trump offers Philippines $2.4bn defence aid",
         "Package to boost self-defence comes with conditions "
         "attached.", (0, 110, 110), "flag"),
    ]
    for i, (k, h, dk, acc, ic) in enumerate(row2):
        panel(img, d, 28 + i * (pw + gap), y2, pw, ph, k, h, dk, acc, ic)
    for i, (k, h, dk, acc, ic) in enumerate(row3):
        panel(img, d, 28 + i * (pw + gap), y3, pw, ph, k, h, dk, acc, ic)

    # Footer ticker + sources
    d.rectangle([28, 922, W - 29, 968], fill=INK)
    d.text((W // 2, 936), "ALSO TODAY:  India–EU trade pact set for 16 Dec signing  ·  "
           "Storms threaten messy Thanksgiving travel",
           font=font(SANS_B, 15), fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 956), "UN chief: AI risk rules within a year  ·  "
           "GTA VI hacker jailed 7 years",
           font=font(SANS_B, 15), fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 986), "Sources: Reuters · AP · AFP · SCMP · The Japan Times — "
           "all stories reported on 24 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="mm")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
