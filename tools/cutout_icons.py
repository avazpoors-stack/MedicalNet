# Robust icon cut-out: fit a quadratic background surface to the border band, flood-fill from edges, soft alpha.
import numpy as np, cv2
from PIL import Image
SRC = "/home/user/template_check/gen"; DST = "/home/user/owa-template/assets/img/icons"
def cutout(name, size=320):
    a = np.asarray(Image.open(f"{SRC}/icon-{name}.png").convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]; xn, yn = xx / w, yy / h
    band = np.zeros((h, w), bool); m = int(0.05 * min(h, w))
    band[:m] = band[-m:] = True; band[:, :m] = band[:, -m:] = True
    A = np.stack([np.ones_like(xn), xn, yn, xn * xn, yn * yn, xn * yn], -1)
    bg = np.zeros_like(a)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A[band], a[..., c][band], rcond=None)
        bg[..., c] = A @ coef
    diff = np.abs(a - bg).max(axis=2)
    cand = (diff < 14).astype(np.uint8)
    n, labels = cv2.connectedComponents(cand, connectivity=4)
    edge = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))) - {0}
    bgmask = np.isin(labels, list(edge))
    alpha = np.where(bgmask, np.clip((diff - 5) / 9.0, 0, 1), 1.0).astype(np.float32)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    # un-matte: remove background colour from semi-transparent edge pixels
    al = np.clip(alpha[..., None], 1e-3, 1)
    fg = np.clip((a - bg * (1 - al)) / al, 0, 255)
    ys, xs = np.where(alpha > 0.1)
    pad = int(0.03 * max(h, w))
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, h); x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, w)
    rgba = np.dstack([fg, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    out = Image.fromarray(rgba, "RGBA"); out.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(out, ((size - out.width) // 2, (size - out.height) // 2), out)
    for px in (96, 192):  # 1x / 2x for the 96px display size
        canvas.resize((px, px), Image.LANCZOS).save(f"{DST}/{name}-{px}.webp", quality=88, method=6)
    return canvas
tiles = []
for n in ("shield", "rocket", "cloud"):
    im = cutout(n)
    bgc = Image.new("RGBA", im.size, (228, 234, 245, 255)); bgc.alpha_composite(im); tiles.append(bgc.convert("RGB"))
prev = Image.new("RGB", (960, 320)); [prev.paste(t, (i * 320, 0)) for i, t in enumerate(tiles)]
prev.save("/home/user/template_check/shots/icons_preview.jpg", quality=80); print("icons ok")
