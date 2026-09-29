"""Generates placeholder logos. Replace Image/Logo.png with your own branding any time."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out = Path(__file__).parent / "Image"
out.mkdir(exist_ok=True)


def make(name, fg, bg):
    img = Image.new("RGBA", (600, 200), bg)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSerif.ttf", 64)
    except OSError:
        font = ImageFont.load_default(size=64)
    d.text((300, 100), "LegalEase", fill=fg, font=font, anchor="mm")
    img.save(out / name)


make("Logo.png", (30, 30, 30, 255), (255, 255, 255, 255))
make("inverseLogo.png", (255, 255, 255, 255), (14, 17, 23, 255))
print("Logos created in", out)
