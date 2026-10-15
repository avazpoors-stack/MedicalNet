# Image pipeline: hero colour-grade, 3D icon cut-out (alpha), avatar crops -> WebP
import os, numpy as np, cv2
from PIL import Image
SRC = "/home/user/template_check/gen"; DST = "/home/user/owa-template/assets/img"
# 1) Hero background: shift periwinkle -> cobalt blue, slight saturation boost
im = Image.open(f"{SRC}/hero-bg.png").convert("RGB")
hsv = np.array(im.convert("HSV")).astype(np.int16)
hsv[..., 0] = (hsv[..., 0] - 7) % 256
hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255)
Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB").save(f"{DST}/hero-bg.webp", quality=80, method=6)
# 2) Icons: flood-fill background from the borders -> soft alpha -> tight crop
def cutout(name, size=320):
    a = np.asarray(Image.open(f"{SRC}/icon-{name}.png").convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    diff = np.abs(a - bg).max(axis=2)
    cand = (diff < 16).astype(np.uint8)
    n, labels = cv2.connectedComponents(cand, connectivity=4)
    edge = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))) - {0}
    bgmask = np.isin(labels, list(edge)) & (cand == 1)
    alpha = np.where(bgmask, np.clip((diff - 4) / 12.0, 0, 1), 1.0)
    alpha = cv2.GaussianBlur(alpha.astype(np.float32), (3, 3), 0)
    ys, xs = np.where(alpha > 0.06)
    pad = int(0.06 * max(h, w))
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, h); x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, w)
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    out = Image.fromarray(rgba, "RGBA"); out.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(out, ((size - out.width) // 2, (size - out.height) // 2), out)
    canvas.save(f"{DST}/icons/{name}.webp", quality=88, method=6)
for n in ("shield", "rocket", "cloud"): cutout(n)
# 3) Avatars: head-and-shoulders square crop, 240px WebP
for f in sorted(os.listdir(SRC)):
    if f.startswith("p0") and f.endswith(".png"):
        im = Image.open(f"{SRC}/{f}").convert("RGB"); W, H = im.size
        s = int(min(W, H) * 0.78); l = (W - s) // 2; t = int((H - s) * 0.30)
        im.crop((l, t, l + s, t + s)).resize((240, 240), Image.LANCZOS).save(f"{DST}/avatars/{f.split('-')[1].replace('.png','')}.webp", quality=80, method=6)
print("images ok")
