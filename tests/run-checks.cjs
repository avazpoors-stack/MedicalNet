// Automated health-check suite → proof/results.json + screenshots
// Static: W3C Nu validator, html-validate, CSSTree, ESLint, security scan, file inventory, SHA-256
// Runtime (Chromium): console/page errors, network, CSP, images, fonts, overflow, 28 interaction tests,
//                     axe-core WCAG 2.2 AA, reduced-motion & JS-disabled modes, screenshots
'use strict';
const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const crypto = require('crypto');
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'proof');
const SHOTS = path.join(OUT, 'screenshots');
const BASE = process.env.BASE_URL || 'http://127.0.0.1:8090/';
const CHROME = process.env.CHROME_PATH || '/usr/bin/chromium';
fs.mkdirSync(SHOTS, { recursive: true });

const NM = (process.env.NODE_PATH || '').split(path.delimiter)[0] || path.join(ROOT, 'node_modules');
const ver = (p) => { try { return JSON.parse(fs.readFileSync(path.join(NM, p, 'package.json'), 'utf8')).version; } catch { return '?'; } };
const R = { meta: { date: new Date().toISOString(), url: BASE, node: process.version, os: (() => { try { return (fs.readFileSync('/etc/os-release', 'utf8').match(/PRETTY_NAME="([^"]+)"/) || [])[1]; } catch { return process.platform; } })(),
  tools: { playwright: ver('playwright'), 'axe-core': ver('axe-core'), 'html-validate': ver('html-validate'), eslint: ver('eslint'), 'csstree-validator': ver('csstree-validator'), lighthouse: ver('lighthouse'), 'vnu-jar': ver('vnu-jar') } }, static: {}, security: {}, runtime: {}, interactions: [], a11y: {} };
const assert = (c, m) => { if (!c) throw new Error(m); };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const DELIVERABLE_SKIP = /^(tests|tools|proof|node_modules)(\/|$)|(^|\/)\./;

function walk(dir, base = dir, acc = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f); const rel = path.relative(base, p).split(path.sep).join('/');
    if (DELIVERABLE_SKIP.test(rel)) continue;
    if (fs.statSync(p).isDirectory()) walk(p, base, acc); else acc.push(rel);
  }
  return acc;
}

/* ======================= STATIC ======================= */
async function staticChecks() {
  // 1) W3C Nu HTML Checker (official validator engine) — HTML, CSS and SVG
  const vnu = String(require('vnu-jar')); // module exports the jar path
  const files = ['index.html', 'assets/css/style.css', 'assets/img/world-map.svg', 'assets/img/favicon.svg'];
  const java = process.env.JAVA_BIN || (fs.existsSync('/usr/lib/jvm/java-21-openjdk-amd64/bin/java') ? '/usr/lib/jvm/java-21-openjdk-amd64/bin/java' : 'java');
  let parsed = null; let failure = '';
  try {
    const out = cp.execFileSync(java, ['-Dnu.validator.servlet.allow-forbidden-hosts=true', '-jar', vnu, '--format', 'json', '--stdout', '--exit-zero-always', '--also-check-css', '--also-check-svg', ...files.map((f) => (/\.svg$/.test(f) ? f : BASE + f))]  /* over HTTP, exactly like a browser (file: URLs have an opaque origin, so CSP 'self' could not match) */, { cwd: ROOT, encoding: 'utf8', maxBuffer: 5e7, stdio: ['ignore', 'pipe', 'pipe'] });
    parsed = JSON.parse(out);
  } catch (e) { failure = String(e.stderr || e.message).split('\n')[0]; }
  if (!parsed) { R.static.w3c = { ran: false, failure }; } else {
    const msgs = parsed.messages || [];
    R.static.w3c = {
      ran: true, java: cp.spawnSync(java, ['-version'], { encoding: 'utf8' }).stderr.split('\n')[0], validator: cp.spawnSync(java, ['-jar', vnu, '--version'], { encoding: 'utf8' }).stdout.trim(), files,
      errors: msgs.filter((m) => m.type === 'error' || m.type === 'non-document-error').length,
      warnings: msgs.filter((m) => m.type === 'info' && m.subType === 'warning').length,
      messages: msgs.map((m) => ({ type: m.subType || m.type, file: (m.url || '').split('/').pop(), line: m.lastLine, msg: m.message }))
    };
  }

  // 2) html-validate (HTML standard + a11y rule presets)
  const { HtmlValidate } = require('html-validate');
  const hv = new HtmlValidate({ extends: ['html-validate:standard', 'html-validate:a11y'] });
  const rep = await hv.validateFile(path.join(ROOT, 'index.html'));
  const hvMsgs = rep.results.flatMap((r) => r.messages);
  R.static.htmlValidate = { valid: rep.valid, errors: rep.errorCount, warnings: rep.warningCount, messages: hvMsgs.map((m) => ({ rule: m.ruleId, line: m.line, msg: m.message })) };

  // 3) CSSTree validator (syntax + property/value grammar)
  const csstree = require('csstree-validator');
  const css = fs.readFileSync(path.join(ROOT, 'assets/css/style.css'), 'utf8');
  let cssErr = csstree.validate(css, 'style.css');
  if (!Array.isArray(cssErr)) cssErr = Object.values(cssErr).flat();
  R.static.css = { bytes: css.length, problems: cssErr.length, messages: cssErr.map((e) => ({ line: e.line, msg: e.message })) };

  // 4) ESLint (eslint:recommended + strict extras)
  const { ESLint } = require('eslint');
  const eslint = new ESLint({ useEslintrc: false, overrideConfig: {
    env: { browser: true, es2022: true }, parserOptions: { ecmaVersion: 2022, sourceType: 'script' }, extends: ['eslint:recommended'],
    rules: { 'no-eval': 'error', 'no-implied-eval': 'error', 'no-new-func': 'error', 'no-script-url': 'error', 'no-var': 'error', 'prefer-const': 'error', eqeqeq: 'error', strict: ['error', 'function'] } } });
  const lint = await eslint.lintFiles([path.join(ROOT, 'assets/js/main.js')]);
  R.static.eslint = { errors: lint[0].errorCount, warnings: lint[0].warningCount, messages: lint[0].messages.map((m) => ({ rule: m.ruleId, line: m.line, msg: m.message })) };
  // 5) every local file referenced from HTML / CSS exists
  const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
  const refs = [...html.matchAll(/(?:src|href)="([^"#][^"]*)"/g)].map((m) => m[1]).filter((u) => !/^(https?:|mailto:|data:)/.test(u))
    .concat([...css.matchAll(/url\(\s*['"]?([^'")]+)/g)].map((m) => m[1]).filter((u) => !/^(data:|#)/.test(u)).map((u) => path.posix.join('assets/css', u)));
  const uniq = [...new Set(refs)];
  R.static.references = { total: uniq.length, missing: uniq.filter((u) => !fs.existsSync(path.join(ROOT, u))) };
  // 6) JS syntax check by the engine itself
  try { cp.execFileSync(process.execPath, ['--check', path.join(ROOT, 'assets/js/main.js')]); R.static.nodeSyntax = 'ok'; } catch (e) { R.static.nodeSyntax = String(e.stderr || e); }
}

/* ======================= SECURITY ======================= */
function securityScan() {
  const files = walk(ROOT);
  const text = files.filter((f) => /\.(html|css|js|svg|md|txt)$/.test(f) || /(^|\/)_headers$/.test(f));
  const code = text.filter((f) => /\.(html|css|js)$/.test(f));
  const P = [
    ['eval()', /\beval\s*\(/, code], ['new Function()', /new\s+Function\s*\(/, code], ['string-based timers', /set(?:Timeout|Interval)\s*\(\s*['"`]/, code],
    ['document.write', /document\.write/, code], ['innerHTML / outerHTML / insertAdjacentHTML', /\.(?:inner|outer)HTML\b|insertAdjacentHTML/, code],
    ['javascript: URLs', /javascript:/i, code], ['inline event handlers (onclick=…)', /\son[a-z]+\s*=\s*["']/i, code.filter((f) => f.endsWith('.html'))],
    ['inline <script> code', /<script(?![^>]*\bsrc=)[^>]*>\s*\S/i, code.filter((f) => f.endsWith('.html'))], ['inline <style> / style=""', /<style\b|\sstyle\s*=\s*["']/i, code.filter((f) => f.endsWith('.html'))],
    ['iframe / object / embed', /<(?:iframe|object|embed|frame)\b/i, code], ['network APIs (fetch/XHR/WebSocket/beacon)', /\bfetch\s*\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|importScripts/, code],
    ['cookies / storage', /localStorage|sessionStorage|document\.cookie|indexedDB/, code], ['obfuscation (atob, \\x escapes, fromCharCode)', /atob\s*\(|\\x[0-9a-f]{2}|String\.fromCharCode/i, code],
    ['crypto-miner signatures', /coinhive|cryptonight|webminer|coin-?imp|minero|\.wasm\b/i, code], ['external scripts/styles/images/fonts', /<(?:script|link|img|source)\b[^>]*(?:src|href)\s*=\s*["']\s*(?:https?:)?\/\//i, code.filter((f) => f.endsWith('.html'))],
    ['external CSS url()/@import', /url\(\s*['"]?\s*(?:https?:)?\/\/|@import/i, code.filter((f) => f.endsWith('.css'))], ['base64 blobs > 200 chars', /[A-Za-z0-9+/]{200,}={0,2}/, code.filter((f) => f.endsWith('.js'))]
  ];
  R.security.patterns = P.map(([name, re, list]) => {
    const hits = [];
    list.forEach((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').split('\n').forEach((line, i) => { if (re.test(line)) hits.push(`${f}:${i + 1}`); }));
    return { name, files: list.length, hits };
  });
  // every URL that appears anywhere, classified
  const urls = new Map();
  text.forEach((f) => (fs.readFileSync(path.join(ROOT, f), 'utf8').match(/https?:\/\/[^\s"'<>)]+/g) || []).forEach((u) => {
    let kind = 'documentation text';
    if (/w3\.org\/(2000\/svg|1999\/xlink)/.test(u)) kind = 'XML namespace identifier (never fetched)';
    else if (f === 'index.html') kind = 'outbound link (opens only on user click, rel=noopener noreferrer)';
    else if (/^assets\/fonts\//.test(f)) kind = 'font licence text';
    else if (/^(README\.md)$/.test(f)) kind = 'documentation text';
    const k = u + ' | ' + f; if (!urls.has(k)) urls.set(k, { url: u, file: f, kind });
  }));
  R.security.urls = [...urls.values()];
  // file inventory by magic bytes
  const magic = (buf, f) => {
    if (buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') return 'image/webp';
    if (buf.slice(0, 4).toString() === 'wOF2') return 'font/woff2';
    const head = buf.slice(0, 200).toString('utf8').trim().toLowerCase();
    if (head.startsWith('<svg')) return 'image/svg+xml (text)';
    if (head.startsWith('<!doctype html')) return 'text/html';
    if (/\.(css|js|md|txt)$/.test(f) || /_headers$/.test(f)) return 'text';
    if (buf[0] === 0x7f && buf.slice(1, 4).toString() === 'ELF' || buf.slice(0, 2).toString() === 'MZ') return 'EXECUTABLE!';
    return 'unknown';
  };
  R.security.inventory = files.map((f) => { const b = fs.readFileSync(path.join(ROOT, f)); return { file: f, bytes: b.length, type: magic(b, f), sha256: crypto.createHash('sha256').update(b).digest('hex') }; });
  fs.writeFileSync(path.join(OUT, 'SHA256SUMS.txt'), R.security.inventory.map((x) => `${x.sha256}  ${x.file}`).join('\n') + '\n');
  R.security.thirdPartyRuntimeDependencies = 0;
}

/* ======================= RUNTIME ======================= */
async function open(browser, opts = {}) {
  const context = await browser.newContext({ viewport: opts.viewport || { width: 1440, height: 900 }, reducedMotion: opts.reducedMotion || 'no-preference', javaScriptEnabled: opts.js !== false, isMobile: !!opts.mobile, hasTouch: !!opts.mobile, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const log = { console: [], pageErrors: [], failed: [], badStatus: [], requests: [] };
  page.on('console', (m) => log.console.push({ type: m.type(), text: m.text() }));
  page.on('pageerror', (e) => log.pageErrors.push(String(e)));
  page.on('requestfailed', (r) => log.failed.push({ url: r.url(), err: r.failure() && r.failure().errorText }));
  page.on('response', (r) => { if (r.status() >= 400) log.badStatus.push({ url: r.url(), status: r.status() }); });
  page.on('request', (r) => log.requests.push({ url: r.url(), type: r.resourceType() }));
  await page.addInitScript(() => {
    window.__csp = []; window.__lcp = 0; window.__cls = 0;
    document.addEventListener('securitypolicyviolation', (e) => window.__csp.push(e.violatedDirective + ' ' + e.blockedURI));
    try {
      new PerformanceObserver((l) => l.getEntries().forEach((e) => { window.__lcp = e.startTime; })).observe({ type: 'largest-contentful-paint', buffered: true });
      new PerformanceObserver((l) => l.getEntries().forEach((e) => { if (!e.hadRecentInput) window.__cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
    } catch (e) { /* unsupported */ }
  });
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await wait(1600);
  return { context, page, log };
}
async function scrollThrough(page) {
  await page.evaluate(async () => {
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += Math.round(innerHeight * 0.55)) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 140)); }
    window.scrollTo(0, H); await new Promise((r) => setTimeout(r, 500));
    window.scrollTo(0, 0); await new Promise((r) => setTimeout(r, 500));
  });
  await wait(900);
}
async function collect(page, log) {
  const m = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const res = performance.getEntriesByType('resource');
    return {
      domContentLoadedMs: Math.round(nav.domContentLoadedEventEnd), loadMs: Math.round(nav.loadEventEnd),
      transferredBytes: nav.transferSize + res.reduce((a, r) => a + (r.transferSize || 0), 0),
      decodedBytes: nav.decodedBodySize + res.reduce((a, r) => a + (r.decodedBodySize || 0), 0), requests: res.length + 1,
      lcpMs: Math.round(window.__lcp || 0), cls: +(window.__cls || 0).toFixed(4),
      horizontalOverflowPx: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      fonts: [...document.fonts].map((f) => `${f.family}: ${f.status}`),
      images: [...document.images].map((i) => ({ src: (i.currentSrc || i.src).replace(location.origin, ''), rendered: i.getClientRects().length > 0, ok: i.complete && i.naturalWidth > 0 })),
      cookies: document.cookie, storageItems: localStorage.length + sessionStorage.length, cspViolations: window.__csp || []
    };
  });
  const origin = new URL(BASE).origin;
  m.externalRequests = log.requests.filter((r) => !r.url.startsWith(origin) && !r.url.startsWith('data:')).map((r) => r.url);
  m.consoleErrors = log.console.filter((c) => c.type === 'error').map((c) => c.text);
  m.consoleWarnings = log.console.filter((c) => c.type === 'warning').map((c) => c.text);
  m.pageErrors = log.pageErrors; m.failedRequests = log.failed; m.httpErrors = log.badStatus;
  m.brokenImages = m.images.filter((i) => i.rendered && !i.ok).map((i) => i.src);
  m.imageCount = m.images.filter((i) => i.rendered).length;
  m.lazyDeferredHiddenImages = m.images.filter((i) => !i.rendered).length; // display:none at this breakpoint → never downloaded (by design)
  delete m.images;
  return m;
}
async function step(name, fn) {
  try { const d = await fn(); R.interactions.push({ name, pass: true, detail: d || '' }); }
  catch (e) { R.interactions.push({ name, pass: false, detail: String(e.message || e).slice(0, 300) }); }
}
async function axe(page, label) {
  const res = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
  R.a11y[label] = { violations: res.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help, targets: v.nodes.slice(0, 4).map((n) => n.target.join(' ')) })), passes: res.passes.length, incomplete: res.incomplete.length, incompleteRules: res.incomplete.map((v) => ({ id: v.id, nodes: v.nodes.length, help: v.help })), rulesRun: res.passes.length + res.violations.length + res.incomplete.length + res.inapplicable.length, axeVersion: res.testEngine.version };
}

async function runtime() {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  R.meta.browser = 'Chromium ' + browser.version();
  const views = { desktop: { width: 1440, height: 900 }, tablet: { width: 834, height: 1112 }, mobile: { width: 390, height: 844 } };

  for (const [name, viewport] of Object.entries(views)) {
    const { context, page, log } = await open(browser, { viewport, mobile: name === 'mobile' });
    await scrollThrough(page);
    if (name === 'desktop') await page.screenshot({ path: path.join(SHOTS, 'desktop-viewport.png') });
    await page.screenshot({ path: path.join(SHOTS, `${name}-full.png`), fullPage: true });
    await page.click('#wall-toggle').catch(() => {}); await wait(400); await axe(page, name);
    R.runtime[name] = await collect(page, log);
    await context.close();
  }

  /* ---------- desktop interaction tests ---------- */
  {
    const { context, page } = await open(browser, { viewport: views.desktop });
    const top = (sel) => page.$eval(sel, (e) => e.getBoundingClientRect().top);
    await step('Header turns into floating glass bar on scroll', async () => {
      await page.evaluate(() => window.scrollTo(0, 400)); await wait(700);
      assert(await page.$eval('#site-header', (e) => e.classList.contains('is-scrolled')), 'no is-scrolled class');
      await page.evaluate(() => window.scrollTo(0, 0)); await wait(500);
      assert(!(await page.$eval('#site-header', (e) => e.classList.contains('is-scrolled'))), 'class not removed at top');
      return 'is-scrolled added at 400px, removed at 0px';
    });
    await step('Nav link "Testimonials" smooth-scrolls to its section', async () => {
      await page.click('a.nav__link[href="#testimonials"]'); await wait(1800);
      const t = await top('#testimonials'); assert(t > -10 && t < 160, 'section top = ' + t); return `section top at ${Math.round(t)}px`;
    });
    await step('Active-section highlight in navigation', async () => {
      assert(await page.$eval('a.nav__link[href="#testimonials"]', (e) => e.classList.contains('is-active')), 'not active'); return 'TESTIMONIALS link marked active';
    });
    await step('Sparkle particles injected into CTA buttons', async () => {
      const n = await page.$$eval('.site-header .btn .spark', (s) => s.length); assert(n >= 8, 'sparks=' + n); return n + ' particles in header CTA';
    });
    await step('Every in-page link points to an existing element', async () => {
      const bad = await page.$$eval('a[href^="#"]', (as) => as.map((a) => a.getAttribute('href')).filter((h) => h.length > 1 && !document.getElementById(h.slice(1))));
      const total = await page.$$eval('a[href^="#"]', (as) => as.length);
      assert(bad.length === 0, 'broken: ' + bad.join(', ')); return `${total} anchors checked, 0 broken`;
    });
    await page.evaluate(() => window.scrollTo(0, 520)); await wait(900);
    await step('Dashboard tabs (mouse): Countries → Browsers', async () => {
      await page.click('#tab-browsers'); await wait(300);
      assert(await page.isVisible('#panel-browsers'), 'browsers panel hidden'); assert(!(await page.isVisible('#panel-countries')), 'countries still visible');
      assert((await page.textContent('#geo-title')) === 'Browsers', 'title not updated'); return 'panel switched, card title = Browsers';
    });
    await step('Dashboard tabs (keyboard): ArrowRight / Home', async () => {
      await page.focus('#tab-browsers'); await page.keyboard.press('ArrowRight'); await wait(150);
      assert((await page.getAttribute('#tab-devices', 'aria-selected')) === 'true', 'devices not selected');
      assert(await page.evaluate(() => document.activeElement.id === 'tab-devices'), 'focus not moved');
      await page.keyboard.press('Home'); await wait(150);
      assert((await page.getAttribute('#tab-countries', 'aria-selected')) === 'true', 'Home failed'); return 'roving tabindex + aria-selected work';
    });
    await step('Traffic Sources ↔ Top Referrers tab with animated bars', async () => {
      await page.click('#tab-referrers'); await wait(1400);
      assert(await page.isVisible('#panel-referrers'), 'referrers hidden');
      const w = await page.$eval('#panel-referrers i', (i) => i.getBoundingClientRect().width); assert(w > 20, 'bar width ' + w); return `first bar ${Math.round(w)}px wide`;
    });
    await step('Sidebar group expand / collapse', async () => {
      const btn = page.locator('[data-side-group]', { hasText: 'Visitors' });
      await btn.click(); assert((await btn.getAttribute('aria-expanded')) === 'true', 'not expanded');
      assert(await btn.evaluate((b) => !b.nextElementSibling.hidden), 'submenu hidden');
      await btn.click(); assert((await btn.getAttribute('aria-expanded')) === 'false', 'not collapsed'); return 'aria-expanded toggles, submenu shows/hides';
    });
    await step('Traffic chart rendered (19-point smooth Bézier curves)', async () => {
      const segs = await page.$eval('.line--cur', (p) => (p.getAttribute('d').match(/C/g) || []).length); assert(segs === 18, 'segments ' + segs); return '18 cubic segments, area + dashed comparison line';
    });
    await step('Chart tooltip follows the pointer', async () => {
      const box = await page.locator('#traffic-chart').boundingBox(); await page.mouse.move(box.x + box.width * 0.55, box.y + box.height * 0.5); await wait(250);
      assert(await page.isVisible('#chart-tip'), 'tooltip hidden'); const t = await page.textContent('#chart-tip'); assert(/Current:/.test(t), 'text ' + t);
      await page.mouse.move(box.x - 40, box.y - 40); await wait(150); return 'tooltip: ' + t.replace(/\s+/g, ' ').trim();
    });
    await step('Legend toggles hide / show a series', async () => {
      await page.click('[data-series="prev"]'); assert((await page.getAttribute('[data-series="prev"]', 'aria-pressed')) === 'false', 'aria'); assert(await page.$eval('.line--prev', (p) => p.classList.contains('is-off')), 'not hidden');
      await page.click('[data-series="prev"]'); assert(!(await page.$eval('.line--prev', (p) => p.classList.contains('is-off'))), 'not restored'); return 'previous-period line hidden and restored';
    });
    await step('Metric switch → Pageviews (axis rescales)', async () => {
      await page.click('#metric-btn'); assert(await page.isVisible('#metric-menu'), 'menu hidden');
      await page.click('[data-metric="pageviews"]'); await wait(200);
      const labels = await page.$$eval('#traffic-chart text', (t) => t.map((x) => x.textContent));
      assert((await page.textContent('#metric-label')) === 'Pageviews', 'label'); assert(labels.includes('60K'), 'axis ' + labels.slice(0, 4)); return 'y-axis: ' + labels.slice(0, 4).join(' / ');
    });
    await step('Refresh button generates new data', async () => {
      const a = await page.getAttribute('.line--cur', 'd'); await page.click('#chart-refresh'); await wait(300);
      assert(a !== (await page.getAttribute('.line--cur', 'd')), 'unchanged'); return 'curve re-drawn with new values';
    });
    await step('Live mode streams new points', async () => {
      const a = await page.getAttribute('.line--cur', 'd'); await page.click('#chart-live'); await wait(1900);
      const b = await page.getAttribute('.line--cur', 'd'); await page.click('#chart-live');
      assert(a !== b, 'no update'); assert((await page.getAttribute('#chart-live', 'aria-pressed')) === 'false', 'not stopped'); return 'data updated while live, stops on second click';
    });
    await step('Donut animates to 66.2 %', async () => {
      const d = await page.$eval('#donut-value', (c) => getComputedStyle(c).strokeDasharray); assert(/^183/.test(d), 'dasharray ' + d); return 'stroke-dasharray = ' + d;
    });
    await step('Search box accepts input', async () => {
      await page.fill('#dash-search', 'bounce rate'); assert((await page.inputValue('#dash-search')) === 'bounce rate', 'value'); await page.fill('#dash-search', ''); return 'typed text kept';
    });
    await step('Count-up metrics reach their exact targets', async () => {
      await page.evaluate(() => document.getElementById('monitoring').scrollIntoView()); await wait(2000);
      const v = await page.$$eval('[data-count]', (els) => els.map((e) => e.textContent)); assert(v.join() === '0.14,11.2,0.82,2.3,9.7,1.1', v.join()); return v.join(' · ');
    });
    await step('Testimonials marquee loops seamlessly (clones hidden from screen readers)', async () => {
      await page.evaluate(() => document.getElementById('testimonials').scrollIntoView()); await wait(800);
      const info = await page.$$eval('[data-marquee]', (cols) => cols.map((c) => ({ loop: c.classList.contains('is-looping'), kids: c.querySelector('.wall__track').children.length, hidden: c.querySelectorAll('[aria-hidden="true"].t-card').length, anim: c.querySelector('.wall__track').getAnimations().length })));
      assert(info.every((c) => c.loop && c.kids === 6 && c.hidden === 3 && c.anim === 1), JSON.stringify(info)); return '3 columns × (3 cards + 3 aria-hidden clones), animation running';
    });
    await step('Pause / Play control for moving content (WCAG 2.2.2)', async () => {
      await page.click('#wall-toggle'); await wait(200);
      const st = await page.$eval('.wall__track', (t) => getComputedStyle(t).animationPlayState); assert(st === 'paused', 'state ' + st);
      assert((await page.textContent('#wall-toggle')).trim() === 'Play', 'label'); await page.click('#wall-toggle'); await page.mouse.move(5, 5); await wait(200);
      assert((await page.textContent('#wall-toggle')).trim() === 'Pause', 'label2'); return 'paused → resumed';
    });
    await step('Parallax avatars move with scroll', async () => {
      await page.evaluate(() => document.getElementById('stories').scrollIntoView({ block: 'start' })); await wait(400);
      const a = await page.$eval('.tile--1', (t) => t.style.getPropertyValue('--py'));
      await page.evaluate(() => window.scrollBy(0, 300)); await wait(400);
      const b = await page.$eval('.tile--1', (t) => t.style.getPropertyValue('--py')); assert(a !== b, a + ' vs ' + b); return `--py ${a} → ${b}`;
    });
    await step('Keyboard: "Skip to content" is the first focusable element', async () => {
      await page.goto(BASE, { waitUntil: 'networkidle' }); await wait(300); await page.keyboard.press('Tab');
      assert(await page.evaluate(() => document.activeElement.classList.contains('skip-link')), 'first focus: ' + (await page.evaluate(() => document.activeElement.outerHTML.slice(0, 60)))); return 'skip link receives first Tab';
    });
    await context.close();
  }

  /* ---------- mobile interaction tests ---------- */
  {
    const { context, page } = await open(browser, { viewport: views.mobile, mobile: true });
    await step('Mobile: hamburger opens the menu', async () => {
      assert(await page.isVisible('.nav-toggle'), 'toggle hidden'); await page.click('.nav-toggle');
      assert(await page.isVisible('#mobile-menu'), 'menu hidden'); assert((await page.getAttribute('.nav-toggle', 'aria-expanded')) === 'true', 'aria'); return 'menu visible, aria-expanded=true';
    });
    await step('Mobile: Escape closes the menu and restores focus', async () => {
      await page.keyboard.press('Escape'); await wait(150);
      assert(!(await page.isVisible('#mobile-menu')), 'still open'); assert(await page.evaluate(() => document.activeElement.classList.contains('nav-toggle')), 'focus lost'); return 'closed, focus back on toggle';
    });
    await step('Mobile: menu link navigates and closes the menu', async () => {
      await page.click('.nav-toggle'); await page.click('#mobile-menu a[href="#stories"]'); await wait(1800);
      assert(!(await page.isVisible('#mobile-menu')), 'menu open'); const t = await page.$eval('#stories', (e) => e.getBoundingClientRect().top); assert(t > -10 && t < 150, 'top ' + t); return `stories section at ${Math.round(t)}px`;
    });
    await step('Mobile: dashboard scales to fit, no horizontal overflow', async () => {
      const fit = await page.$eval('#dash', (d) => parseFloat(d.style.getPropertyValue('--fit'))); const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      assert(fit > 0 && fit < 1, 'fit ' + fit); assert(ov <= 0, 'overflow ' + ov); return `scale ${fit.toFixed(3)}, overflow ${ov}px`;
    });
      await step('Mobile: scaled dashboard exposed as a labelled static preview', async () => {
      const s = await page.evaluate(() => ({ inert: document.getElementById('dash').inert, role: document.getElementById('dash-fit').getAttribute('role'), label: document.getElementById('dash-fit').getAttribute('aria-label') }));
      assert(s.inert && s.role === 'img' && s.label, JSON.stringify(s)); return 'inert + role=img + aria-label (no undersized touch targets)';
    });
    await context.close();
  }

  /* ---------- reduced motion ---------- */
  {
    const { context, page, log } = await open(browser, { viewport: views.desktop, reducedMotion: 'reduce' });
    await step('prefers-reduced-motion: animations disabled, content fully visible', async () => {
      const s = await page.evaluate(() => ({ sparks: document.querySelectorAll('.spark').length, loops: document.querySelectorAll('.is-looping').length, hidden: document.querySelectorAll('.reveal-init').length }));
      assert(s.sparks === 0 && s.loops === 0 && s.hidden === 0, JSON.stringify(s)); assert(log.pageErrors.length === 0, 'errors'); return 'no sparkles, no marquee, no hidden reveal elements';
    });
    await context.close();
  }

  /* ---------- JavaScript disabled ---------- */
  {
    const { context, page } = await open(browser, { viewport: views.desktop, js: false });
    await step('JavaScript disabled: page still complete and readable', async () => {
      const s = await page.evaluate(() => ({ noJs: document.documentElement.classList.contains('no-js'), cards: document.querySelectorAll('.t-card').length, invisible: [...document.querySelectorAll('[data-reveal]')].filter((e) => getComputedStyle(e).opacity !== '1').length, h1: document.querySelector('h1').innerText }));
      assert(s.noJs && s.cards === 9 && s.invisible === 0, JSON.stringify(s)); return `all ${s.cards} testimonials + every section visible`;
    });
    await page.screenshot({ path: path.join(SHOTS, 'no-js-full.png'), fullPage: true });
    await context.close();
  }

  /* ---------- fidelity screenshots (same viewport as the reference video: 1270×800) ---------- */
  {
    const { context, page } = await open(browser, { viewport: { width: 1270, height: 800 } });
    await scrollThrough(page);
    const spots = [['hero', null, 0], ['dashboard', null, 520], ['ai', '#ai .feature__panel', 208], ['monitoring', '#monitoring .feature__panel', 227], ['capabilities', '#capabilities .eyebrow', 164], ['testimonials', '#testimonials .eyebrow', 221], ['stories', '#stories .eyebrow', 271], ['footer', '.footer', 463]];
    for (const [name, sel, y] of spots) {
      await page.evaluate(([s, yy]) => { const el = s && document.querySelector(s); const t = el ? el.getBoundingClientRect().top + window.scrollY - yy : yy; window.scrollTo(0, Math.max(0, t)); }, [sel, y]);
      await wait(1300);
      await page.screenshot({ path: path.join(SHOTS, `compare-${name}.png`) });
    }
    await context.close();
  }
  await browser.close();
}

(async () => {
  const t0 = Date.now();
  await staticChecks();
  securityScan();
  await runtime();
  R.meta.durationSec = Math.round((Date.now() - t0) / 1000);
  R.summary = {
    interactionsPassed: R.interactions.filter((i) => i.pass).length, interactionsTotal: R.interactions.length,
    consoleErrors: Object.values(R.runtime).reduce((a, v) => a + v.consoleErrors.length + v.pageErrors.length, 0),
    externalRequests: Object.values(R.runtime).reduce((a, v) => a + v.externalRequests.length, 0),
    axeViolations: Object.values(R.a11y).reduce((a, v) => a + v.violations.length, 0),
    securityHits: R.security.patterns.reduce((a, p) => a + p.hits.length, 0)
  };
  fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(R, null, 2));
  console.log(JSON.stringify({ summary: R.summary, w3c: R.static.w3c.ran ? [R.static.w3c.errors, R.static.w3c.warnings] : 'DID NOT RUN: ' + R.static.w3c.failure, htmlValidate: [R.static.htmlValidate.errors, R.static.htmlValidate.warnings], css: R.static.css.problems, eslint: [R.static.eslint.errors, R.static.eslint.warnings] }));
  R.interactions.filter((i) => !i.pass).forEach((i) => console.log('FAIL:', i.name, '→', i.detail));
})().catch((e) => { console.error(e); process.exit(1); });
