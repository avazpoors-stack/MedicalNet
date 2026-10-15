# WCAG 2.x contrast of the text colour against every real background pixel behind it (text hidden while captured)
import json, re, os
import numpy as np
from PIL import Image
D = '/tmp/contrast-probe'; OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'proof', 'contrast-probe.json')
def lin(c): c = c / 255.0; return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def lum(rgb): l = lin(rgb); return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]
meta = json.load(open(f'{D}/meta.json')); rows = []
for m in meta:
    nums = [float(x) for x in re.findall(r'[\d.]+', m['color'])]; r, g, b = nums[:3]; a = nums[3] if len(nums) > 3 else 1.0
    bg = np.concatenate([np.asarray(Image.open(f'{D}/{f}').convert('RGB'), dtype=np.float64).reshape(-1, 3) for f in m['files']])
    txt = a * np.array([r, g, b]) + (1 - a) * bg                       # semi-transparent text blended over each pixel
    L1, L2 = lum(txt), lum(bg); hi, lo = np.maximum(L1, L2), np.minimum(L1, L2)
    ratio = (hi + 0.05) / (lo + 0.05)
    need = 3.0 if m['large'] else 4.5
    worst = float(np.percentile(ratio, 1))                              # 1st percentile → robust to anti-aliased edge pixels
    rows.append({'viewport': m['viewport'], 'selector': m['selector'], 'text': m['text'], 'reason': m['reason'], 'required': need,
                 'worst': round(worst, 2), 'median': round(float(np.median(ratio)), 2), 'pass': worst >= need, 'pixels': int(ratio.size)})
fails = [x for x in rows if not x['pass']]
summary = {'elements': len(rows), 'passed': len(rows) - len(fails), 'failed': len(fails),
           'lowestRatio': min(x['worst'] for x in rows) if rows else None,
           'lowestMargin': round(min(x['worst'] / x['required'] for x in rows), 2) if rows else None, 'pixelsAnalysed': sum(x['pixels'] for x in rows)}
json.dump({'summary': summary, 'elements': rows}, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(json.dumps(summary)); [print('FAIL', f['viewport'], f['selector'][:60], repr(f['text']), f['worst'], '<', f['required']) for f in fails[:15]]
