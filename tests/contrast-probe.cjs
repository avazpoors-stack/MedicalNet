// Pixel-level contrast verification for elements axe marks "needs review" (text on gradients/images/overlaps).
// For each element: hide its text (CSSOM, CSP-safe) → screenshot the exact text box → tests/contrast_probe.py
// computes the WCAG ratio of the text colour against every real background pixel.
'use strict';
const fs = require('fs'); const path = require('path');
const { chromium } = require('playwright'); const AxeBuilder = require('@axe-core/playwright').default;
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8090/';
const DIR = '/tmp/contrast-probe'; fs.rmSync(DIR, { recursive: true, force: true }); fs.mkdirSync(DIR, { recursive: true });
(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
  const meta = [];
  for (const [vp, viewport] of [['desktop', { width: 1440, height: 900 }], ['tablet', { width: 834, height: 1112 }], ['mobile', { width: 390, height: 844 }]]) {
    const page = await (await browser.newContext({ viewport, reducedMotion: 'reduce' })).newPage(); // reduced motion → static frames, no parallax drift
    await page.goto(BASE, { waitUntil: 'networkidle' }); await page.waitForTimeout(1200);
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 80)); } scrollTo(0, 0); });
    await page.waitForTimeout(800);
    const res = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    const nodes = (res.incomplete[0] && res.incomplete[0].nodes) || [];
    let i = 0;
    const passes = [['', nodes], [' (hero bg at drift end)', nodes.filter((n) => /hero|social-proof|btn--lg/.test(n.target.join(' ')) || n.html.includes('hero'))]];
    for (const [tag, list] of passes) {
    if (tag) await page.evaluate(() => { scrollTo(0, 0); document.querySelector('.hero__bg').style.setProperty('transform', 'scale(1.12) translate3d(-1.5%, 1%, 0)'); });
    for (const n of list) {
      const sel = n.target[n.target.length - 1];
      const info = await page.evaluate((s) => {
        const el = document.querySelector(s); if (!el) return null;
        el.scrollIntoView({ block: 'center' });
        const isSvg = el instanceof SVGElement; const cs = getComputedStyle(el);
        let boxes = [];
        if (isSvg) boxes = [el.getBoundingClientRect()]; else {
          const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let t;
          while ((t = w.nextNode())) { if (!t.textContent.trim()) continue; const rg = document.createRange(); rg.selectNodeContents(t); boxes.push(...rg.getClientRects()); }
        }
        const rects = boxes.map((q) => ({ x: Math.max(0, q.left), y: Math.max(0, q.top), width: Math.min(q.right, innerWidth) - Math.max(0, q.left), height: Math.min(q.bottom, innerHeight) - Math.max(0, q.top) })).filter((q) => q.width >= 2 && q.height >= 2);
        if (!rects.length) return null;
        const size = parseFloat(cs.fontSize); const bold = parseInt(cs.fontWeight, 10) >= 700;
        const color = isSvg ? cs.fill : cs.color;
        [el, ...el.querySelectorAll('*')].forEach((e) => { e.dataset.probeHidden = '1'; e.style.setProperty('color', 'transparent', 'important'); e.style.setProperty('-webkit-text-fill-color', 'transparent', 'important'); e.style.setProperty('text-shadow', 'none', 'important'); if (e instanceof SVGElement) e.style.setProperty('fill', 'transparent', 'important'); });
        return { color, size, bold, large: size >= 24 || (bold && size >= 18.66), text: ((el.innerText || el.textContent) || '').replace(/\s+/g, ' ').trim().slice(0, 40), rects };
      }, sel);
      if (!info) continue;
      await page.waitForTimeout(60);
      const files = [];
      for (const rect of info.rects) { const f = `${vp}${tag}-${i}-${files.length}.png`; await page.screenshot({ path: path.join(DIR, f), clip: rect }); files.push(f); }
      i++;
      await page.evaluate(() => document.querySelectorAll('[data-probe-hidden]').forEach((e) => { ['color', '-webkit-text-fill-color', 'text-shadow', 'fill'].forEach((p) => e.style.removeProperty(p)); delete e.dataset.probeHidden; }));
      meta.push({ viewport: vp + tag, selector: sel, files, reason: (n.any[0] && n.any[0].message || '').split(' due to ').pop().split(' because ').pop().replace(/\.$/, ''), ...info });
    }
    }
  }
  fs.writeFileSync(path.join(DIR, 'meta.json'), JSON.stringify(meta, null, 1));
  console.log('probed', meta.length);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
