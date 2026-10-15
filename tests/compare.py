# Side-by-side: original video frame (browser area cropped, 1270x800 CSS px) vs recreation screenshot (same viewport)
import sys
from PIL import Image, ImageDraw, ImageFont
FR = '/home/user/template_check/frames'
SH = '/home/user/owa-template/proof/screenshots'
OUT = '/home/user/owa-template/proof/compare'
PAIRS = [('hero', 0), ('dashboard', 180), ('ai', 360), ('monitoring', 480), ('capabilities', 660), ('testimonials', 690), ('stories', 840), ('footer', 900)]
font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf', 30)
W, H, PAD, BAR = 1270, 800, 24, 64
thumbs = []
for name, f in PAIRS:
    orig = Image.open(f'{FR}/f_{f:04d}.jpg').convert('RGB').crop((85, 140, 85 + W, 140 + H))
    rec = Image.open(f'{SH}/compare-{name}.png' if __import__('os').path.exists(f'{SH}/compare-{name}.png') else f'{SH}/compare-{name}.jpg').convert('RGB').resize((W, H))
    c = Image.new('RGB', (W * 2 + PAD * 3, H + BAR + PAD), (17, 17, 22))
    d = ImageDraw.Draw(c)
    for i, (img, label, col) in enumerate([(orig, 'ORIGINAL (reference video)', (255, 159, 67)), (rec, 'RECREATION (this code, live Chromium)', (46, 204, 113))]):
        x = PAD + i * (W + PAD)
        d.rounded_rectangle((x, 14, x + 22, 36), 5, fill=col)
        d.text((x + 34, 10), label, font=font, fill=(240, 240, 245))
        c.paste(img, (x, BAR))
    c = c.resize((1800, round(c.height * 1800 / c.width)), Image.LANCZOS)
    c.save(f'{OUT}/{name}.jpg', quality=80, optimize=True, progressive=True)
    thumbs.append(rec.resize((635, 400)))
m = Image.new('RGB', (635 * 2, 400 * 4), 'white')
for i, t in enumerate(thumbs): m.paste(t, ((i % 2) * 635, (i // 2) * 400))
m.save('/home/user/template_check/shots/final_montage.jpg', quality=72)
print('compare ok', len(PAIRS))
