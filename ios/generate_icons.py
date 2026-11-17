#!/usr/bin/env python3
"""Generate the AppIcon PNGs for the Shuangyu iOS app.

Runs on the GitHub Actions macOS runner (no binary assets in the repo).
Draws: dark-navy rounded square, white CJK glyph, blue underline bar.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "Shuangyu", "Assets.xcassets", "AppIcon.appiconset")

NAVY = (15, 23, 42, 255)
BLUE = (37, 99, 235, 255)
WHITE = (255, 255, 255, 255)

# macOS CJK fonts that contain the glyph (first one that exists wins)
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def find_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # rounded-rect background (radius ~22% like iOS icons)
    r = int(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=NAVY)
    font_path = find_font()
    if font_path:
        font = ImageFont.truetype(font_path, int(size * 0.52))
        # draw the glyph centered in the upper ~2/3
        tw = d.textlength("译", font=font)
        x = (size - tw) / 2
        y = size * 0.10
        d.text((x, y), "译", font=font, fill=WHITE)
    # blue underline bar
    bar_h = max(2, int(size * 0.027))
    bar_w = int(size * 0.39)
    bar_x = (size - bar_w) // 2
    bar_y = int(size * 0.80)
    d.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h],
                        radius=bar_h // 2, fill=BLUE)
    return img


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    # 1024 must be opaque RGB for the App Store
    big = draw_icon(1024)
    bg = Image.new("RGBA", (1024, 1024), NAVY)
    bg.alpha_composite(big)
    bg.convert("RGB").save(os.path.join(OUTDIR, "icon-1024.png"))
    for s in (180, 120, 87, 80, 60, 58, 40, 29, 20):
        draw_icon(s).save(os.path.join(OUTDIR, f"icon-{s}.png"))
    print("icons generated in", OUTDIR)


if __name__ == "__main__":
    main()
