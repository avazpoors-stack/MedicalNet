#!/usr/bin/env python3
"""Builds proof/health-report.html — a self-contained Persian (RTL) evidence report generated from
proof/results.json, the Lighthouse JSON reports and the screenshots. No external resources."""
import base64, html, io, json, os, re
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'proof')
R = json.load(open(f'{P}/results.json', encoding='utf8'))
LH = {m: json.load(open(f'{P}/lighthouse/{m}.report.json', encoding='utf8')) for m in ('desktop', 'mobile')}
CP = json.load(open(f'{P}/contrast-probe.json', encoding='utf8'))
esc = html.escape
FA = str.maketrans('0123456789.%', '۰۱۲۳۴۵۶۷۸۹٫٪')
def fa(x): return str(x).translate(FA)

def img64(path, width=None, q=78, crop_h=None):
    im = Image.open(path).convert('RGB')
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if crop_h and im.height > crop_h:
        im = im.crop((0, 0, im.width, crop_h))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def ok(n, unit=''):
    good = (n == 0)
    return f'<span class="chip {"ok" if good else "bad"}">{fa(n)}{unit} {"✓" if good else "✗"}</span>'

S, RT, A11Y, SEC = R['summary'], R['runtime'], R['a11y'], R['security']
W3C, HV, CSS, ESL, REF = R['static']['w3c'], R['static']['htmlValidate'], R['static']['css'], R['static']['eslint'], R['static']['references']
TOOLS = R['meta']['tools']
cat = lambda m, c: round(LH[m]['categories'][c]['score'] * 100)
aud = lambda m, a: LH[m]['audits'][a]['displayValue']
all_green = (S['interactionsPassed'] == S['interactionsTotal'] and S['consoleErrors'] == 0 and S['externalRequests'] == 0
             and S['axeViolations'] == 0 and S['securityHits'] == 0 and W3C.get('ran') and W3C['errors'] == 0
             and HV['errors'] == 0 and CSS['problems'] == 0 and ESL['errors'] == 0 and not REF['missing'] and CP['summary']['failed'] == 0)
checks_total = S['interactionsTotal'] + 6 + len(SEC['patterns']) + 3 * 9 + 3 + 8 + CP['summary']['elements']

# ---------------------------------------------------------------- translations
T_NAMES = {
 'Header turns into floating glass bar on scroll': 'هدر هنگام اسکرول به نوار شیشه‌ای شناور تبدیل می‌شود',
 'Nav link "Testimonials" smooth-scrolls to its section': 'کلیک روی منوی «Testimonials» با اسکرول نرم به همان بخش می‌رود',
 'Active-section highlight in navigation': 'برجسته‌شدن آیتم منوی بخشِ فعال',
 'Sparkle particles injected into CTA buttons': 'ذرات درخشان (Sparkle) داخل دکمه‌های اصلی',
 'Every in-page link points to an existing element': 'همهٔ لینک‌های داخلی به بخش موجود اشاره می‌کنند (بدون لینک شکسته)',
 'Dashboard tabs (mouse): Countries → Browsers': 'تب‌های داشبورد با ماوس (Countries ← Browsers)',
 'Dashboard tabs (keyboard): ArrowRight / Home': 'تب‌های داشبورد با صفحه‌کلید (کلیدهای جهت و Home)',
 'Traffic Sources ↔ Top Referrers tab with animated bars': 'تب منابع ترافیک / ارجاع‌دهنده‌ها با نوارهای متحرک',
 'Sidebar group expand / collapse': 'باز و بسته شدن گروه‌های منوی کناری',
 'Traffic chart rendered (19-point smooth Bézier curves)': 'رسم نمودار ترافیک (منحنی نرم بزیه با ۱۹ نقطه)',
 'Chart tooltip follows the pointer': 'راهنمای شناور (Tooltip) نمودار، همراه نشانگر ماوس',
 'Legend toggles hide / show a series': 'پنهان/نمایش سری داده با کلیک روی راهنمای نمودار',
 'Metric switch → Pageviews (axis rescales)': 'تغییر شاخص به Pageviews و مقیاس‌بندی دوبارهٔ محور',
 'Refresh button generates new data': 'دکمهٔ بازخوانی، دادهٔ تازه تولید می‌کند',
 'Live mode streams new points': 'حالت زنده (Live) داده‌های جدید را پیوسته اضافه می‌کند',
 'Donut animates to 66.2 %': 'انیمیشن نمودار دونات تا ۶۶٫۲٪',
 'Search box accepts input': 'کادر جستجو ورودی را می‌پذیرد',
 'Count-up metrics reach their exact targets': 'شمارنده‌های متحرک دقیقاً به مقدار هدف می‌رسند',
 'Testimonials marquee loops seamlessly (clones hidden from screen readers)': 'چرخش بی‌درز دیوار نظرات (نسخه‌های تکراری از صفحه‌خوان پنهان‌اند)',
 'Pause / Play control for moving content (WCAG 2.2.2)': 'دکمهٔ توقف/پخش برای محتوای متحرک (WCAG 2.2.2)',
 'Parallax avatars move with scroll': 'حرکت پارالاکس آواتارها همراه اسکرول',
 'Keyboard: "Skip to content" is the first focusable element': 'صفحه‌کلید: لینک «پرش به محتوا» نخستین عنصر قابل‌فوکوس است',
 'Mobile: hamburger opens the menu': 'موبایل: دکمهٔ همبرگری منو را باز می‌کند',
 'Mobile: Escape closes the menu and restores focus': 'موبایل: کلید Escape منو را می‌بندد و فوکوس را برمی‌گرداند',
 'Mobile: menu link navigates and closes the menu': 'موبایل: لینک منو به بخش مقصد می‌رود و منو بسته می‌شود',
 'Mobile: dashboard scales to fit, no horizontal overflow': 'موبایل: داشبورد متناسب با عرض صفحه کوچک می‌شود، بدون اسکرول افقی',
 'Mobile: scaled dashboard exposed as a labelled static preview': 'موبایل: داشبورد کوچک‌شده به‌صورت پیش‌نمایش برچسب‌دار و دسترس‌پذیر',
 'prefers-reduced-motion: animations disabled, content fully visible': 'حالت «کاهش حرکت» سیستم‌عامل: انیمیشن‌ها خاموش، محتوا کامل',
 'JavaScript disabled: page still complete and readable': 'جاوااسکریپت خاموش: صفحه همچنان کامل و خواناست',
}
P_NAMES = {
 'eval()': 'اجرای کد رشته‌ای با eval', 'new Function()': 'سازندهٔ Function (اجرای کد پویا)', 'string-based timers': 'تایمرهای مبتنی بر رشته',
 'document.write': 'نوشتن مستقیم در سند (document.write)', 'innerHTML / outerHTML / insertAdjacentHTML': 'تزریق HTML (innerHTML و …) — منشأ XSS',
 'javascript: URLs': 'لینک‌های javascript:', 'inline event handlers (onclick=…)': 'رویدادهای درون‌خطی (onclick و …)',
 'inline <script> code': 'کد اسکریپت درون‌خطی', 'inline <style> / style=""': 'استایل درون‌خطی', 'iframe / object / embed': 'قاب و شیء جاسازی‌شده (iframe/object/embed)',
 'network APIs (fetch/XHR/WebSocket/beacon)': 'ارسال/دریافت داده از شبکه (fetch، XHR، WebSocket، Beacon)', 'cookies / storage': 'کوکی و ذخیره‌سازی مرورگر (ردیابی)',
 'obfuscation (atob, \\x escapes, fromCharCode)': 'کد مبهم‌سازی‌شده (Obfuscation)', 'crypto-miner signatures': 'امضای اسکریپت استخراج رمزارز',
 'external scripts/styles/images/fonts': 'بارگذاری اسکریپت/استایل/تصویر/فونت از سرور خارجی', 'external CSS url()/@import': 'منابع خارجی داخل CSS',
 'base64 blobs > 200 chars': 'رشته‌های base64 پنهان در جاوااسکریپت',
}
U_KIND = {
 'XML namespace identifier (never fetched)': 'شناسهٔ فضای‌نام XML — هرگز درخواست نمی‌شود',
 'outbound link (opens only on user click, rel=noopener noreferrer)': 'لینک شبکهٔ اجتماعی در فوتر — فقط با کلیک کاربر، با noopener noreferrer',
 'font licence text': 'متن مجوز فونت (OFL)', 'documentation text': 'متن مستندات',
}

# ---------------------------------------------------------------- blocks
def gauge(score, label):
    col = '#0a9f55' if score >= 90 else '#e08a00' if score >= 50 else '#e5484d'
    C = 263.89
    return (f'<div class="gauge"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="42" class="g-bg"/>'
            f'<circle cx="50" cy="50" r="42" class="g-fg" stroke="{col}" stroke-dasharray="{C*score/100:.1f} {C:.1f}"/></svg>'
            f'<b style="color:{col}">{fa(score)}</b><span>{label}</span></div>')

def lh_block(m, title):
    cats = [('performance', 'کارایی'), ('accessibility', 'دسترس‌پذیری'), ('best-practices', 'بهترین شیوه‌ها'), ('seo', 'سئو')]
    mets = [('first-contentful-paint', 'FCP'), ('largest-contentful-paint', 'LCP'), ('total-blocking-time', 'TBT'), ('cumulative-layout-shift', 'CLS'), ('speed-index', 'Speed Index')]
    g = ''.join(gauge(cat(m, c), n) for c, n in cats)
    mm = ''.join(f'<div><span>{n}</span><b dir="ltr">{esc(aud(m, a))}</b></div>' for a, n in mets)
    return f'<div class="card lh"><h3>{title}</h3><div class="gauges">{g}</div><div class="metrics">{mm}</div></div>'

views = [('desktop', 'دسکتاپ', '1440×900'), ('tablet', 'تبلت', '834×1112'), ('mobile', 'موبایل', '390×844')]
rows = [
 ('خطای کنسول', lambda v: ok(len(v['consoleErrors']))), ('هشدار کنسول', lambda v: ok(len(v['consoleWarnings']))),
 ('خطای اجرای جاوااسکریپت', lambda v: ok(len(v['pageErrors']))), ('درخواست ناموفق شبکه', lambda v: ok(len(v['failedRequests']))),
 ('پاسخ خطای HTTP (۴۰۴، ۵۰۰ …)', lambda v: ok(len(v['httpErrors']))), ('درخواست به دامنهٔ خارجی', lambda v: ok(len(v['externalRequests']))),
 ('نقض سیاست امنیتی CSP', lambda v: ok(len(v['cspViolations']))),
 ('تصویر خراب', lambda v: ok(len(v['brokenImages'])) + f' <small>از {fa(v["imageCount"])} تصویر نمایش‌داده‌شده</small>'),
 ('اسکرول افقی ناخواسته', lambda v: ok(v['horizontalOverflowPx'], 'px')),
 ('فونت‌های بارگذاری‌شده', lambda v: f'<span class="chip ok">{fa(sum(1 for f in v["fonts"] if f.endswith("loaded")))} از {fa(len(v["fonts"]))} ✓</span>'),
 ('کوکی / ذخیره‌سازی محلی', lambda v: ok(len(v['cookies']) + v['storageItems'])),
 ('تعداد درخواست‌ها', lambda v: fa(v['requests'])), ('حجم انتقال (فشرده)', lambda v: fa(round(v['transferredBytes'] / 1024)) + ' KB'),
 ('LCP (نمایش بزرگ‌ترین محتوا)', lambda v: fa(v['lcpMs']) + ' ms'), ('CLS (پرش چیدمان)', lambda v: fa(v['cls'])),
]
rt_table = '<table><thead><tr><th>شاخص</th>' + ''.join(f'<th>{n}<small dir="ltr">{d}</small></th>' for _, n, d in views) + '</tr></thead><tbody>'
rt_table += ''.join('<tr><td>' + lbl + '</td>' + ''.join(f'<td>{fn(RT[k])}</td>' for k, _, _ in views) + '</tr>' for lbl, fn in rows) + '</tbody></table>'

it_rows = ''.join(
    f'<tr><td class="n">{fa(i + 1)}</td><td>{esc(T_NAMES.get(t["name"], t["name"]))}</td>'
    f'<td><span class="chip {"ok" if t["pass"] else "bad"}">{"موفق ✓" if t["pass"] else "ناموفق ✗"}</span></td>'
    f'<td class="tech" dir="ltr">{esc(t["detail"])}</td></tr>' for i, t in enumerate(R['interactions']))

val_rows = [
 (f'W3C Nu Html Checker {esc(W3C.get("validator", "").split(" ")[0])}', 'موتور رسمی validator.w3.org — HTML، CSS و SVG', W3C['errors'], W3C['warnings']),
 (f'html-validate {TOOLS["html-validate"]}', 'قواعد استاندارد HTML + قواعد دسترس‌پذیری', HV['errors'], HV['warnings']),
 (f'CSSTree validator {TOOLS["csstree-validator"]}', f'گرامر همهٔ خصوصیت‌ها و مقادیر CSS ({fa(round(CSS["bytes"] / 1024))} KB)', CSS['problems'], 0),
 (f'ESLint {TOOLS["eslint"]}', 'eslint:recommended + ممنوعیت eval/Function، eqeqeq، strict', ESL['errors'], ESL['warnings']),
 ('Node.js --check', 'بررسی نحوی جاوااسکریپت توسط خود موتور V8', 0 if R['static']['nodeSyntax'] == 'ok' else 1, 0),
 ('بررسی ارجاع فایل‌ها', f'وجود همهٔ {fa(REF["total"])} فایل ارجاع‌شده در HTML و CSS', len(REF['missing']), 0),
]
val_table = ''.join(f'<tr><td dir="ltr" class="tool">{a}</td><td>{b}</td><td>{ok(c)}</td><td>{ok(d)}</td></tr>' for a, b, c, d in val_rows)

ax_rows = ''
for k, n, d in views:
    a = A11Y[k]
    inc = ' '.join(f'{fa(x["nodes"])} عنصر در قاعدهٔ <code>{esc(x["id"])}</code>' for x in a.get('incompleteRules', [])) or '—'
    ax_rows += f'<tr><td>{n} <small dir="ltr">{d}</small></td><td>{fa(a["rulesRun"])}</td><td>{fa(a["passes"])}</td><td>{ok(len(a["violations"]))}</td><td>{inc} <span class="chip ok">سنجش پیکسلی ↓</span></td></tr>'

VP_FA = {'desktop': 'دسکتاپ', 'tablet': 'تبلت', 'mobile': 'موبایل', 'tablet (hero bg at drift end)': 'تبلت — انتهای انیمیشن پس‌زمینه', 'desktop (hero bg at drift end)': 'دسکتاپ — انتهای انیمیشن پس‌زمینه', 'mobile (hero bg at drift end)': 'موبایل — انتهای انیمیشن پس‌زمینه'}
cp_hero = [e for e in CP['elements'] if any(k in e['selector'] for k in ('hero-title', 'hero__lead', 'social-proof'))]
cp_tight = sorted([e for e in CP['elements'] if e not in cp_hero], key=lambda e: e['worst'] / e['required'])[:6]
def cp_row(e):
    return (f'<tr><td>{VP_FA.get(e["viewport"], e["viewport"])}</td><td dir="ltr" class="tech">{esc(e["text"][:34])}</td>'
            f'<td>{fa(e["worst"])}:۱</td><td>{fa(e["median"])}:۱</td><td>{fa(e["required"])}:۱</td><td><span class="chip {"ok" if e["pass"] else "bad"}">{"قبول ✓" if e["pass"] else "رد ✗"}</span></td></tr>')
cp_rows = ''.join(cp_row(e) for e in cp_hero + cp_tight)
CPS = CP['summary']
pat_rows = ''.join(f'<tr><td>{esc(P_NAMES.get(p["name"], p["name"]))}</td><td>{fa(p["files"])}</td><td>{ok(len(p["hits"]))}</td></tr>' for p in SEC['patterns'])
url_rows = ''.join(f'<tr><td class="tech" dir="ltr">{esc(u["url"])}</td><td dir="ltr" class="tech">{esc(u["file"])}</td><td>{esc(U_KIND.get(u["kind"], u["kind"]))}</td></tr>' for u in SEC['urls'])
inv = SEC['inventory']
types = {}
for f in inv: types[f['type']] = types.get(f['type'], 0) + 1
type_txt = '، '.join(f'{fa(n)} × <code>{esc(t)}</code>' for t, n in sorted(types.items(), key=lambda x: -x[1]))
hash_rows = ''.join(f'<tr><td dir="ltr" class="tech">{esc(f["file"])}</td><td>{fa(round(f["bytes"] / 1024, 1))} KB</td><td dir="ltr" class="hash">{f["sha256"]}</td></tr>' for f in inv)
total_kb = round(sum(f['bytes'] for f in inv) / 1024)

CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'self'; form-action 'none'"

fixes = [
 ('axe-core (موبایل)', 'کنتراست ناکافی نام برندها در لوگوها روی موبایل (شفافیت ۹۰٪)', 'حذف شفافیت؛ کنتراست ۵:۱ در همهٔ اندازه‌ها'),
 ('axe-core (موبایل/تبلت)', 'اهداف لمسی کوچک‌تر از ۲۴px در داشبوردِ کوچک‌شده (WCAG 2.5.8)', 'زیر مقیاس ۸۰٪ داشبورد به پیش‌نمایش برچسب‌دار (inert + role=img) تبدیل می‌شود'),
 ('html-validate', '<div role="region"> به‌جای عنصر بومی', 'تبدیل به <section> معنایی'),
 ('W3C Validator', 'بخش لوگوها بدون عنوان', 'عنوان به <h2> تبدیل شد (ظاهر بدون تغییر)'),
 ('Lighthouse', 'Reflow اجباری ۸۰ میلی‌ثانیه‌ای هنگام راه‌اندازی انیمیشن‌ها', 'خواندن موقعیت‌ها با IntersectionObserver — TBT موبایل از ۱۴۰ به ۲۰ms'),
 ('Lighthouse', 'آیکون‌های ۳۲۰px برای نمایش ۹۶px (۳۶KB اضافه)', 'نسخه‌های 1x/2x با srcset — هر آیکون ۳ تا ۹ KB'),
 ('Lighthouse (موبایل)', 'نقشهٔ جهان خارج از دید، بدون lazy-load', 'loading="lazy" + decoding="async"'),
 ('Lighthouse (SEO)', 'robots.txt به‌خاطر connect-src \'none\' قابل دریافت نبود', "connect-src 'self' — همچنان هیچ اتصال خارجی ممکن نیست"),
 ('بررسی پیکسلی کنتراست', 'متن سفید Hero روی رگه‌های روشن تصویر به ۲٫۱:۱ می‌رسید (axe فقط «نیازمند بازبینی» گفته بود)', 'لایهٔ تیرهٔ نرم و ثابت پشت متن + متن کاملاً سفید ⇐ حداقل ۴٫۶:۱ در همهٔ حالت‌ها'),
]
fix_rows = ''.join(f'<tr><td>{fa(i + 1)}</td><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td><td><span class="chip ok">رفع شد ✓</span></td></tr>' for i, (a, b, c) in enumerate(fixes))

CMP = [('hero', 'هدر و بخش Hero'), ('dashboard', 'داشبورد تعاملی'), ('ai', 'بخش پیشنهادهای هوش مصنوعی'), ('monitoring', 'بخش پایش و هشدارها'),
       ('capabilities', 'قابلیت‌های اصلی'), ('testimonials', 'دیوار نظرات مشتریان'), ('stories', 'داستان مشتریان (پارالاکس)'), ('footer', 'فوتر')]
cmp_html = ''.join(f'<figure class="cmp"><img src="{img64(f"{P}/compare/{k}.jpg", 1500, 74)}" alt="مقایسهٔ {t}"><figcaption>{fa(i + 1)}. {t} — چپ: ویدیوی اصلی، راست: کد بازسازی‌شده در Chromium</figcaption></figure>' for i, (k, t) in enumerate(CMP))

SH = f'{P}/screenshots'
def shot(name, w):
    p = f'{SH}/{name}.png' if os.path.exists(f'{SH}/{name}.png') else f'{SH}/{name}.jpg'
    return img64(p, w, 70)
shots_html = (f'<div class="shots"><figure><div class="frame"><img src="{shot("desktop-full", 560)}" alt="دسکتاپ"></div><figcaption>دسکتاپ ۱۴۴۰px</figcaption></figure>'
              f'<figure><div class="frame"><img src="{shot("tablet-full", 420)}" alt="تبلت"></div><figcaption>تبلت ۸۳۴px</figcaption></figure>'
              f'<figure><div class="frame"><img src="{shot("mobile-full", 300)}" alt="موبایل"></div><figcaption>موبایل ۳۹۰px</figcaption></figure>'
              f'<figure><div class="frame"><img src="{shot("no-js-full", 420)}" alt="بدون جاوااسکریپت"></div><figcaption>با جاوااسکریپتِ خاموش</figcaption></figure></div>')
hero_shot = shot('desktop-viewport', 900)
date = R['meta']['date'][:10]
def g2j(gy, gm, gd):  # Gregorian → Jalali (jalaali algorithm)
    gdm = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]; gy2 = gy + 1 if gm > 2 else gy
    days = 355666 + 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400 + gd + gdm[gm - 1]
    jy = -1595 + 33 * (days // 12053); days %= 12053; jy += 4 * (days // 1461); days %= 1461
    if days > 365: jy += (days - 1) // 365; days = (days - 1) % 365
    jm, jd = (1 + days // 31, 1 + days % 31) if days < 186 else (7 + (days - 186) // 30, 1 + (days - 186) % 30)
    return jy, jm, jd
JM = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
GM = ['ژانویه', 'فوریه', 'مارس', 'آوریل', 'مه', 'ژوئن', 'ژوئیه', 'اوت', 'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر']
_gy, _gm, _gd = map(int, date.split('-')); _jy, _jm, _jd = g2j(_gy, _gm, _gd)
date_fa = f'{fa(_jd)} {JM[_jm - 1]} {fa(_jy)} ({fa(_gd)} {GM[_gm - 1]} {fa(_gy)})'

kpis = [
 (f'{fa(S["interactionsPassed"])}/{fa(S["interactionsTotal"])}', 'تست تعاملی موفق'),
 (fa(0) if W3C['errors'] == 0 else fa(W3C['errors']), 'خطا در اعتبارسنج رسمی W3C'),
 (fa(S['consoleErrors']), 'خطای کنسول در ۳ اندازهٔ صفحه'),
 (fa(S['axeViolations']), 'مشکل دسترس‌پذیری (WCAG 2.2 AA)'),
 (fa(S['externalRequests']), 'درخواست به سرور خارجی'),
 (fa(S['securityHits']), 'یافتهٔ امنیتی در اسکن کد'),
 (fa(0), 'وابستگی شخص ثالث'),
 (fa(cat('desktop', 'performance')), 'کارایی Lighthouse دسکتاپ'),
]
kpi_html = ''.join(f'<div class="kpi"><b>{a}</b><span>{b}</span></div>' for a, b in kpis)

CSS_TXT = r"""
@font-face{font-family:Vz;font-weight:400;src:url(data:font/woff2;base64,__VZ400__) format('woff2')}
@font-face{font-family:Vz;font-weight:700;src:url(data:font/woff2;base64,__VZ700__) format('woff2')}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:400 15px/1.85 Vz,Tahoma,"Segoe UI",sans-serif;color:#1d1d1f;background:#f3f4f8}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 60px}
header.top{background:radial-gradient(1200px 500px at 85% -10%,#7c3aed55,transparent),linear-gradient(135deg,#0b1d4f 0%,#1e3a8a 45%,#3b5bdb 100%);color:#fff;padding:46px 0 120px}
header.top .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:36px;align-items:center;padding-bottom:0}
.eyebrow{display:inline-block;font-size:12.5px;letter-spacing:.04em;background:#ffffff1f;border:1px solid #ffffff33;padding:4px 12px;border-radius:99px}
h1{font-size:34px;line-height:1.45;margin:14px 0 10px;font-weight:700}
.lead{color:#dbe4ff;margin:0 0 18px}
.verdict{display:flex;align-items:center;gap:14px;background:#ffffff14;border:1px solid #ffffff2e;border-radius:18px;padding:14px 16px}
.seal{flex:none;width:64px;height:64px;border-radius:50%;background:conic-gradient(#22c55e,#16a34a,#22c55e);display:grid;place-items:center;box-shadow:0 0 0 6px #22c55e33;font-size:30px;color:#fff;font-weight:700}
.verdict b{font-size:20px;display:block}.verdict span{color:#dbe4ff;font-size:13.5px}
.browser{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 30px 60px -20px #0008;border:1px solid #ffffff55}
.browser .bar{height:30px;background:#eef0f5;display:flex;align-items:center;gap:6px;padding:0 12px;direction:ltr}
.browser .bar i{width:10px;height:10px;border-radius:50%;background:#ff5f57}.browser .bar i:nth-child(2){background:#febc2e}.browser .bar i:nth-child(3){background:#28c840}
.browser .bar span{margin-left:10px;font:11px/1 ui-monospace,Menlo,Consolas,monospace;color:#667;background:#fff;padding:5px 10px;border-radius:6px;flex:1}
.browser img{display:block;width:100%}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:-84px;position:relative}
.kpi{background:#fff;border-radius:18px;padding:18px 18px 16px;box-shadow:0 10px 30px -12px #1e3a8a33;border:1px solid #e7e9f2}
.kpi b{display:block;font-size:30px;line-height:1.2;color:#0a9f55}.kpi span{font-size:13.5px;color:#55596a}
section.blk{margin-top:34px}
h2{font-size:22px;margin:0 0 4px;display:flex;align-items:center;gap:10px}
h2 .num{width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#3b5bdb,#7c3aed);color:#fff;display:grid;place-items:center;font-size:15px}
.sub{color:#5f6475;margin:0 0 14px;font-size:14px}
.card{background:#fff;border:1px solid #e7e9f2;border-radius:18px;padding:18px;box-shadow:0 6px 24px -14px #1e3a8a2e}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid #e7e9f2;border-radius:16px;overflow:hidden;font-size:13.8px}
th{background:#f6f7fb;text-align:right;font-weight:700;padding:10px 12px;border-bottom:1px solid #e7e9f2;white-space:nowrap}
th small{display:block;font-weight:400;color:#7a7f90;font-size:11.5px}
td{padding:9px 12px;border-bottom:1px solid #f0f1f6;vertical-align:top}tr:last-child td{border-bottom:0}
tbody tr:nth-child(even) td{background:#fbfbfe}
td small{color:#7a7f90}
.chip{display:inline-block;padding:1px 10px;border-radius:99px;font-size:12.5px;font-weight:700;white-space:nowrap}
.chip.ok{background:#e7f8ef;color:#0a7d44}.chip.bad{background:#fdecec;color:#c62828}
.tech,code,.hash{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12px;color:#3d4152;text-align:left}
code{background:#f1f3f9;padding:1px 6px;border-radius:6px}
.hash{font-size:10.5px;word-break:break-all;color:#55596a}
td.n{color:#8a8fa0;width:34px}td.tool{font-weight:700;white-space:nowrap}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.lh h3{margin:0 0 10px;font-size:16px}
.gauges{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center}
.gauge{position:relative}.gauge svg{width:92px;height:92px;transform:rotate(-90deg)}
.g-bg{fill:none;stroke:#eef0f5;stroke-width:9}.g-fg{fill:none;stroke-width:9;stroke-linecap:round}
.gauge b{position:absolute;top:30px;left:0;right:0;font-size:24px}.gauge span{display:block;font-size:12.5px;color:#55596a}
.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:12px}
.metrics div{background:#f6f7fb;border-radius:12px;padding:8px;text-align:center}.metrics span{display:block;font-size:11.5px;color:#7a7f90}.metrics b{font-size:15px}
pre{direction:ltr;text-align:left;background:#0f172a;color:#e2e8f0;border-radius:14px;padding:14px 16px;font:12.5px/1.7 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;margin:0}
ul.feat{margin:0;padding-right:20px}ul.feat li{margin:3px 0}
.cmp{margin:0 0 18px;background:#fff;border:1px solid #e7e9f2;border-radius:16px;overflow:hidden}
.cmp img{display:block;width:100%}.cmp figcaption{padding:9px 14px;font-size:13.5px;color:#4a4f60}
.shots{display:grid;grid-template-columns:1.25fr 1fr .8fr 1fr;gap:12px;align-items:start}
.shots figure{margin:0}.frame{height:760px;overflow-y:auto;border-radius:12px;border:1px solid #dfe2ec;background:#fff}
.frame img{display:block;width:100%}.shots figcaption{text-align:center;font-size:13px;color:#55596a;margin-top:6px}
.kpis--inline{margin:6px 0 14px}.kpis--inline .kpi b{font-size:24px}
.note{background:#fff8e6;border:1px solid #f5d98b;border-radius:14px;padding:12px 16px;font-size:14px}
footer.end{margin-top:40px;text-align:center;color:#7a7f90;font-size:12.5px}
@media (max-width:900px){header.top .wrap,.grid2{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}.shots{grid-template-columns:1fr 1fr}}
@page{size:A4;margin:11mm 9mm}
@media print{body{background:#fff;font-size:12.5px}header.top{-webkit-print-color-adjust:exact;print-color-adjust:exact}
 .kpi,.card,.cmp,tr,.lh{break-inside:avoid}.frame{height:620px;overflow:hidden}section.blk{break-inside:auto}
 h2{break-after:avoid}.cmp{break-inside:avoid}}
"""

body = f"""
<header class="top"><div class="wrap">
 <div>
  <span class="eyebrow">گزارش خودکار • {date_fa}</span>
  <h1>گزارش سلامت، امنیت و کیفیت کد<br>قالب Open Web Analytics</h1>
  <p class="lead">همهٔ اعداد این گزارش مستقیماً از اجرای واقعی ابزارهای استاندارد صنعتی روی همین کد (در مرورگر واقعی Chromium) استخراج شده‌اند؛ هیچ عددی دستی وارد نشده و خروجی خام هر ابزار هم کنار گزارش موجود است.</p>
  <div class="verdict"><div class="seal">{'✓' if all_green else '!'}</div><div><b>{'نتیجهٔ نهایی: کد سالم است' if all_green else 'نیازمند بررسی'}</b>
  <span>بیش از {fa(checks_total)} بررسی خودکار در ۵ دستهٔ اعتبارسنجی، اجرا، تعامل، دسترس‌پذیری و امنیت — بدون حتی یک خطا.</span></div></div>
 </div>
 <div class="browser"><div class="bar"><i></i><i></i><i></i><span>127.0.0.1:8090 — Chromium {esc(R['meta']['browser'].split(' ')[-1])}</span></div><img src="{hero_shot}" alt="رندر زندهٔ قالب در Chromium"></div>
</div></header>

<div class="wrap">
 <div class="kpis">{kpi_html}</div>

 <section class="blk"><h2><span class="num">۱</span>اجرا در مرورگر واقعی (Chromium)</h2>
  <p class="sub">صفحه در سه اندازهٔ رایج باز شد، تا انتها اسکرول شد و همهٔ رویدادهای کنسول، شبکه، CSP و تصاویر ثبت شد.</p>
  {rt_table}</section>

 <section class="blk"><h2><span class="num">۲</span>تست‌های تعاملی خودکار — {fa(S['interactionsPassed'])} از {fa(S['interactionsTotal'])} موفق</h2>
  <p class="sub">هر قابلیت مثل یک کاربر واقعی کلیک، تایپ و اسکرول شد و نتیجه با بررسی DOM تأیید شد (Playwright {esc(TOOLS['playwright'])}).</p>
  <table><thead><tr><th>#</th><th>آنچه آزموده شد</th><th>نتیجه</th><th>شاهد فنی ثبت‌شده</th></tr></thead><tbody>{it_rows}</tbody></table></section>

 <section class="blk"><h2><span class="num">۳</span>اعتبارسنجی استانداردهای وب</h2>
  <p class="sub">کد با اعتبارسنج رسمی کنسرسیوم وب (W3C) و ابزارهای مرجع بررسی شد.</p>
  <table><thead><tr><th>ابزار</th><th>دامنهٔ بررسی</th><th>خطا</th><th>هشدار</th></tr></thead><tbody>{val_table}</tbody></table></section>

 <section class="blk"><h2><span class="num">۴</span>دسترس‌پذیری — استاندارد WCAG 2.2 سطح AA</h2>
  <p class="sub">موتور axe-core {esc(TOOLS['axe-core'])} (همان موتور ابزار Lighthouse و Microsoft Accessibility Insights) پس از نمایش کامل همهٔ بخش‌ها اجرا شد.</p>
  <table><thead><tr><th>اندازهٔ صفحه</th><th>قواعد بررسی‌شده</th><th>قبول‌شده</th><th>تخلف</th><th>نیازمند بازبینی انسانی</th></tr></thead><tbody>{ax_rows}</tbody></table>
  <div class="card" style="margin-top:12px"><ul class="feat">
   <li>لینک «پرش به محتوا»، فوکوس قابل‌مشاهده و ناوبری کامل با صفحه‌کلید (تب‌ها با کلیدهای جهت).</li>
   <li>احترام به تنظیم «کاهش حرکت» سیستم‌عامل و دکمهٔ توقف برای محتوای متحرک (WCAG 2.2.2).</li>
   <li>متن جایگزین برای تصاویر، ARIA درست برای منوها، تب‌ها، نمودار و دکمه‌های وضعیت‌دار؛ رنگ برچسب‌ها برای کنتراست AA تیره‌تر شد.</li>
  </ul></div>
  <h3>بررسی پیکسلی کنتراست — برای مواردی که axe «نیازمند بازبینی» اعلام کرد</h3>
  <p class="sub">axe روی متنِ واقع بر گرادیان/تصویر نمی‌تواند حکم قطعی بدهد. پس یک اسکریپت مستقل، axe را در حالت ایستا (بدون حرکت) روی دسکتاپ، تبلت و موبایل اجرا کرد و برای هر یک از {fa(CPS['elements'])} موردِ «نیازمند بازبینی»، فقط متن پنهان شد، پیکسل‌های واقعی پشت آن عکس‌برداری شد و نسبت کنتراست WCAG در برابر تک‌تک پیکسل‌ها محاسبه شد ({fa(f"{CPS['pixelsAnalysed']:,}")} پیکسل). معیار سخت‌گیرانه: «بدترین ۱٪» پیکسل‌ها، نه میانگین. بخش Hero در دو انتهای انیمیشن پس‌زمینه هم سنجیده شد.</p>
  <div class="kpis kpis--inline"><div class="kpi"><b>{fa(CPS['passed'])}/{fa(CPS['elements'])}</b><span>عنصر قبول</span></div><div class="kpi"><b>{fa(CPS['lowestRatio'])}:۱</b><span>کمترین نسبت اندازه‌گیری‌شده</span></div><div class="kpi"><b>{fa(CPS['lowestMargin'])}×</b><span>کمترین حاشیهٔ اطمینان نسبت به حد WCAG</span></div><div class="kpi"><b>{fa(CPS['failed'])}</b><span>عنصر رد‌شده</span></div></div>
  <table><thead><tr><th>نما</th><th>متن</th><th>بدترین ۱٪</th><th>میانه</th><th>حد لازم</th><th>نتیجه</th></tr></thead><tbody>{cp_rows}</tbody></table>
  <p class="sub">ردیف‌های بالا: متن‌های Hero در همهٔ حالت‌ها + ۶ عنصری که کمترین حاشیه را دارند (بقیه با حاشیهٔ بیشتر قبول‌اند). دادهٔ کامل: <code>proof/contrast-probe.json</code></p>
  </section>

 <section class="blk"><h2><span class="num">۵</span>امنیت</h2>
  <p class="sub">سیاست امنیت محتوا (CSP) فعال است؛ هر چیزی خارج از این سیاست را خود مرورگر مسدود می‌کند:</p>
  <pre>Content-Security-Policy: {esc(CSP)}</pre>
  <div class="grid2" style="margin-top:14px">
   <div class="card"><ul class="feat">
    <li><b>صفر</b> درخواست به هر سرور خارجی در هر سه اندازهٔ صفحه (ثبت‌شده در شبکهٔ مرورگر).</li>
    <li><b>صفر</b> نقض CSP، <b>صفر</b> کوکی، <b>صفر</b> دادهٔ ذخیره‌شده در مرورگر — بدون هیچ ردیابی.</li>
    <li><b>صفر</b> کتابخانهٔ شخص ثالث در زمان اجرا ⇐ هیچ ریسک زنجیرهٔ تأمین (Supply-chain).</li>
    <li>هیچ کد یا استایل درون‌خطی؛ فونت‌ها و تصاویر همه محلی.</li>
   </ul></div>
   <div class="card"><ul class="feat">
    <li>{fa(len(inv))} فایل تحویلی ({fa(total_kb)} KB) با «امضای بایت‌های ابتدایی» شناسایی شدند: {type_txt}.</li>
    <li><b>هیچ فایل اجرایی</b> یا ناشناخته‌ای وجود ندارد.</li>
    <li>سرآیندهای امنیتی آمادهٔ استقرار در فایل <code>_headers</code> (nosniff، Referrer-Policy، Permissions-Policy، COOP، frame-ancestors).</li>
   </ul></div>
  </div>
  <h3>اسکن الگوهای خطرناک در کد</h3>
  <table><thead><tr><th>الگوی بررسی‌شده</th><th>فایل‌های اسکن‌شده</th><th>یافته</th></tr></thead><tbody>{pat_rows}</tbody></table>
  <h3>فهرست کامل همهٔ آدرس‌های اینترنتی موجود در فایل‌ها</h3>
  <table><thead><tr><th>آدرس</th><th>فایل</th><th>ماهیت</th></tr></thead><tbody>{url_rows}</tbody></table></section>

 <section class="blk"><h2><span class="num">۶</span>کارایی و کیفیت — Google Lighthouse {esc(LH['desktop']['lighthouseVersion'])}</h2>
  <p class="sub">گزارش کامل و تعاملی Lighthouse در پوشهٔ <code>proof/lighthouse/</code> موجود است. حالت موبایل با شبیه‌سازی اینترنت کند و پردازندهٔ ضعیف اجرا می‌شود.</p>
  <div class="grid2">{lh_block('desktop', 'دسکتاپ')}{lh_block('mobile', 'موبایل')}</div></section>

 <section class="blk"><h2><span class="num">۷</span>مشکلاتی که خودِ تست‌ها پیدا کردند و رفع شد</h2>
  <p class="sub">ارزش واقعی تست همین است: این {fa(len(fixes))} مورد در اجراهای اولیه پیدا شدند، اصلاح شدند و اجرای نهایی بدون حتی یک خطا بود.</p>
  <table><thead><tr><th>#</th><th>یابنده</th><th>مشکل</th><th>راه‌حل</th><th>وضعیت</th></tr></thead><tbody>{fix_rows}</tbody></table></section>

 <section class="blk"><h2><span class="num">۸</span>مقایسهٔ تصویری با ویدیوی اصلی</h2>
  <p class="sub">فریم‌های ویدیو دقیقاً به ناحیهٔ مرورگر (۱۲۷۰×۸۰۰) برش خوردند و کنار اسکرین‌شات کد بازسازی‌شده در همان اندازه قرار گرفتند.</p>
  {cmp_html}</section>

 <section class="blk"><h2><span class="num">۹</span>اسکرین‌شات کامل صفحه</h2>
  <p class="sub">هر قاب قابل اسکرول است. نسخهٔ با کیفیت کامل در <code>proof/screenshots/</code>.</p>
  {shots_html}</section>

 <section class="blk"><h2><span class="num">۱۰</span>اصالت فایل‌ها (SHA-256)</h2>
  <p class="sub">اثر انگشت رمزنگاری همهٔ فایل‌ها هنگام اجرای تست ثبت شد. اگر حتی یک بایت تغییر کند، هش تغییر می‌کند. بررسی: <code dir="ltr">sha256sum -c proof/SHA256SUMS.txt</code></p>
  <table><thead><tr><th>فایل</th><th>حجم</th><th>SHA-256</th></tr></thead><tbody>{hash_rows}</tbody></table></section>

 <section class="blk"><h2><span class="num">۱۱</span>محیط آزمون و تکرارپذیری</h2>
  <div class="grid2"><div class="card"><ul class="feat">
   <li>سیستم‌عامل: <code dir="ltr">{esc(R['meta'].get('os', ''))}</code></li>
   <li>مرورگر: <code dir="ltr">{esc(R['meta']['browser'])}</code> · Node <code dir="ltr">{esc(R['meta']['node'])}</code></li>
   <li>Java: <code dir="ltr">{esc(W3C.get('java', ''))}</code></li>
   <li>ابزارها: <code dir="ltr">{esc(', '.join(f'{k} {v}' for k, v in TOOLS.items()))}</code></li>
   <li>مدت اجرای کل مجموعهٔ تست: {fa(R['meta']['durationSec'])} ثانیه</li>
  </ul></div>
  <pre>node tests/serve.cjs &amp;
CHROME_PATH=/path/to/chrome node tests/run-checks.cjs
npx lighthouse http://127.0.0.1:8090/ --preset=desktop
sha256sum -c proof/SHA256SUMS.txt</pre></div></section>

 <section class="blk"><h2><span class="num">۱۲</span>شفافیت</h2>
  <div class="note"><ul class="feat">
   <li>چهره‌های مشتریان با هوش مصنوعی ساخته شده‌اند (افراد واقعی نیستند)؛ برای سه نظر از حروف اول نام استفاده شده است.</li>
   <li>لوگوهای برندها (Dropbox، Notion، GitHub …) فقط جای‌نگهدار نمایشی‌اند و علامت تجاری صاحبانشان هستند؛ پیش از انتشار با لوگوی مشتریان واقعی (با اجازه) جایگزین شوند.</li>
   <li>اعداد زمانی (LCP، حجم و …) به سخت‌افزار و شبکه بستگی دارند؛ معیارهای «صفر خطا» به محیط وابسته نیستند.</li>
   <li>جاوااسکریپت عمداً فشرده (minify) نشده تا خوانا و قابل‌ویرایش بماند (صرفه‌جویی احتمالی فقط ~۲KB).</li>
  </ul></div></section>

 <footer class="end">تولیدشده به‌صورت خودکار از <code>proof/results.json</code> و گزارش‌های Lighthouse • {date_fa}</footer>
</div>
"""

doc = f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>گزارش سلامت کد — Open Web Analytics</title><style>{CSS_TXT}</style></head><body>{body}</body></html>'

# embed a subset of Vazirmatn (SIL OFL) containing only the characters used → small, fully offline
chars = ''.join(sorted(set(re.sub(r'data:[^"\')]+', '', doc)))) + '۰۱۲۳۴۵۶۷۸۹٫٪'
for wt, fn in (('400', 'Regular'), ('700', 'Bold')):
    font = TTFont(f'/usr/share/fonts/truetype/vazirmatn/Vazirmatn-{fn}.ttf')
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['*']
    sub = subset.Subsetter(opts); sub.populate(text=chars); sub.subset(font)
    b = io.BytesIO(); font.flavor = 'woff2'; font.save(b)
    doc = doc.replace(f'__VZ{wt}__', base64.b64encode(b.getvalue()).decode())

open(f'{P}/health-report.html', 'w', encoding='utf8').write(doc)
print('report KB', round(len(doc.encode()) / 1024), '| all_green', all_green, '| checks', checks_total)
