#!/usr/bin/env python3
"""
MedicalNet — Module Pages Generator
Builds the 6 dedicated module pages (hospital, technicians, marketplace,
students, odr, academy) from a single shared template.

Shared chrome (SVG sprite, footer) is extracted from index.html so there is
exactly one source of truth. Page content lives in tools/pages_content.py.

Usage:  python3 tools/build_pages.py
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pages_content import PAGES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE_URL = 'https://avazpoors-stack.github.io/MedicalNet/'
OG_IMAGE = BASE_URL + 'assets/img/og-image.jpg'

index_html = (ROOT / 'index.html').read_text(encoding='utf-8')
SPRITE = re.search(r'<svg class="sprite".*?</svg>', index_html, re.S).group(0)
FOOTER = re.search(r'<footer class="footer.*?</footer>', index_html, re.S).group(0)

# ---- Chrome ------------------------------------------------------------
NAV = [
    ('index.html', 'خانه'),
    ('hospital.html', 'پنل بیمارستان'),
    ('technicians.html', 'پنل تکنسین'),
    ('marketplace.html', 'بازارگاه B2B'),
    ('students.html', 'هاب دانشجویی'),
    ('odr.html', 'داوری آنلاین'),
    ('academy.html', 'آکادمی'),
]
NAV_MOBILE = [
    ('index.html', 'خانه'),
    ('hospital.html', 'پنل بیمارستان و مراکز درمانی'),
    ('technicians.html', 'پنل تکنسین‌ها و تعمیرکاران'),
    ('marketplace.html', 'بازارگاه B2B تأمین‌کنندگان'),
    ('students.html', 'هاب دانشگاه و دانشجویان'),
    ('odr.html', 'میز داوری آنلاین (ODR)'),
    ('academy.html', 'آکادمی و رسانه تخصصی'),
]


def ic(name):
    return f'<svg class="ic" aria-hidden="true"><use href="#{name}"/></svg>'


ROLES = [
    ('hospital.html', 'بیمارستان', 'hospital.html'),
    ('technicians.html', 'تکنسین', 'technicians.html'),
    ('marketplace.html', 'تأمین‌کننده', 'marketplace.html'),
    ('students.html', 'دانشجوی کارآموز', 'students.html'),
]


def render_role_bar(current_file):
    btns = []
    for href, label, page in ROLES:
        active = page == current_file
        cls = 'role-switch__btn is-active' if active else 'role-switch__btn'
        btns.append(f'        <a class="{cls}" href="{href}">{label}</a>')
    return f'''    <div class="role-bar" id="role-bar">
      <div class="role-bar__inner">
        <span class="role-bar__label">ورود به عنوان:</span>
        <nav class="role-switch" aria-label="انتخاب نقش کاربری و ورود به پیشخوان متناظر">
{chr(10).join(btns)}
        </nav>
      </div>
      <button class="role-bar__toggle" type="button" aria-controls="role-bar" aria-expanded="true" aria-label="بستن نوار انتخاب نقش">
        <svg class="ic" aria-hidden="true"><use href="#i-close"/></svg>
      </button>
    </div>
    <button class="role-bar__reopen" type="button" aria-controls="role-bar" aria-expanded="false" aria-label="باز کردن نوار انتخاب نقش">
      ورود به عنوان
      <svg class="ic" aria-hidden="true"><use href="#i-chevron-down"/></svg>
    </button>
'''


def render_header(current_file):
    links = []
    for href, label in NAV:
        active = href == current_file
        cls = 'nav__link is-active' if active else 'nav__link'
        cur = ' aria-current="page"' if active else ''
        links.append(f'        <a class="{cls}" href="{href}"{cur}>{label}</a>')
    mlinks = []
    for href, label in NAV_MOBILE:
        mlinks.append(f'      <a href="{href}">{label}</a>')
    return f'''  <!-- ============ Header & Navigation ============ -->
  <header class="site-header" id="site-header">
    <div class="site-header__inner">
      <a class="brand" href="index.html" aria-label="مدیکال‌نت — صفحه اصلی پلتفرم ملی مهندسی بالینی">
        <svg class="brand__mark" viewBox="0 0 112 48" aria-hidden="true"><use href="#logo-mark"/></svg>
        <div class="brand__text-group">
          <span class="brand__name">مدیکال‌نت</span>
          <span class="brand__sub">سامانه جامع مهندسی بالینی و بازارگاه B2B تجهیزات پزشکی</span>
        </div>
      </a>
      <nav class="nav" aria-label="ناوبری اصلی پلتفرم">
        <span class="nav__pill" aria-hidden="true"></span>
{chr(10).join(links)}
      </nav>
      <div class="site-header__actions">
        <span class="badge-version" title="نسخه عملیاتی منطبق بر مقاله پژوهشی">نسخه عملیاتی ۳.۴.۰</span>
        <a href="index.html#modules" class="btn btn--dark btn--sm" data-sparkle>
          <span>ورود به پورتال</span>
          {ic('i-arrow-right')}
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="باز کردن منو">
          {ic('i-menu')}
        </button>
      </div>
    </div>
{render_role_bar(current_file)}    <div class="mobile-menu" id="mobile-menu" hidden>
{chr(10).join(mlinks)}
      <div class="mobile-menu__actions">
        <a href="index.html#modules" class="btn btn--dark btn--sm mobile-menu-btn">انتخاب پیشخوان نقش شما</a>
      </div>
    </div>
  </header>
'''


def render_head(p):
    url = BASE_URL + p['file']
    return f'''<!doctype html>
<html lang="fa" dir="rtl" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{p['title']}</title>
  <meta name="description" content="{p['desc']}">
  <meta name="theme-color" content="#1d4ed8">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['desc']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="نمای پیشخوان سامانه مدیکال‌نت — پلتفرم ملی مهندسی بالینی و بازارگاه B2B تجهیزات پزشکی">
  <meta property="og:locale" content="fa_IR">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{p['title']}">
  <meta name="twitter:description" content="{p['desc']}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap">
  <link rel="preload" href="assets/fonts/outfit-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/dm-sans-var.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/medicalnet-components.css">
  <link rel="stylesheet" href="assets/css/rtl-override.css">
  <link rel="stylesheet" href="assets/css/module-pages.css">
  <script src="assets/js/rolebar-state.js"></script>
  <script src="assets/js/main.js" defer></script>
</head>
<body id="top">
  <a class="skip-link" href="#main">پرش به محتوای اصلی</a>

  {SPRITE}
'''


def render_feature(f, idx):
    rev = ' feature-block--reverse' if idx % 2 else ''
    fid = f' id="{f["id"]}"' if f.get('id') else ''
    checks = ''.join(
        f'        <li>{ic("i-check")}<span>{c}</span></li>' for c in f['checks'])
    note = ''
    if f.get('note'):
        n_icon, n_text = f['note']
        note = f'      <p class="feature-note">{ic(n_icon)}<span>{n_text}</span></p>'
    return f'''    <article class="feature-block{rev}"{fid} data-reveal>
      <div class="feature-block__copy">
        <span class="feature-block__kicker">{ic(f['kicker_icon'])}{f['kicker']}</span>
        <h2 class="feature-block__title">{f['title']}</h2>
        <p class="feature-block__desc">{f['desc']}</p>
        <ul class="feature-checklist">
{checks}
        </ul>
{note}      </div>
      <div class="mock-panel">
        <div class="mock-panel__bar">
          <div class="mock-panel__dots"><i></i><i></i><i></i></div>
          <span class="mock-panel__name">{f['panel_name']}</span>
        </div>
        <div class="mock-panel__body">
{f['panel']}        </div>
      </div>
    </article>
'''


TG_BANNER = '''    <div class="tg-banner" data-reveal>
      <div class="tg-banner__inner">
        <div class="tg-banner__ic">{icon}</div>
        <div class="tg-banner__body">
          <p class="tg-banner__t">پل ارتباطی پشتیبان — ربات تلگرام متصل به سامانه</p>
          <p class="tg-banner__d">نسخه سبک (Lightweight Fallback) مدیکال‌نت برای شرایط کندی اینترنت: {desc}</p>
        </div>
        <div class="tg-banner__stats">
          <div class="tg-stat"><b>{s1b}</b>{s1l}</div>
          <div class="tg-stat"><b>{s2b}</b>{s2l}</div>
        </div>
      </div>
    </div>
'''


def render_strip(current_file):
    chips = []
    labels = {
        'hospital.html': ('i-activity', 'پنل بیمارستان'),
        'technicians.html': ('i-tool', 'پنل تکنسین'),
        'marketplace.html': ('i-cart', 'بازارگاه B2B'),
        'students.html': ('i-users', 'هاب دانشجویی'),
        'odr.html': ('i-target', 'داوری آنلاین'),
        'academy.html': ('i-file-chart', 'آکادمی'),
    }
    for f, (icon, label) in labels.items():
        if f == current_file:
            chips.append(f'      <span class="strip-chip strip-chip--active">{ic(icon)}{label} (صفحه فعلی)</span>')
        else:
            chips.append(f'      <a class="strip-chip" href="{f}">{ic(icon)}{label}</a>')
    return f'''    <nav class="modules-strip" aria-label="سایر ماژول‌های پلتفرم">
      <p class="modules-strip__t">حرکت بین ماژول‌های شش‌گانه</p>
      <div class="modules-strip__chips">
{chr(10).join(chips)}
      </div>
    </nav>
'''


def render_cta(c):
    btns = ''.join(
        f'          <a href="{h}" class="{cls}" data-sparkle>{ic(icon)}<span>{t}</span></a>'
        for h, cls, icon, t in c['btns'])
    return f'''    <section class="module-cta" aria-labelledby="pcta-title">
      <h2 class="module-cta__t" id="pcta-title">{c['title']}</h2>
      <p class="module-cta__d">{c['desc']}</p>
      <div class="module-hero__actions">
{btns}
      </div>
    </section>
'''


def render_page(p):
    stats = ''.join(
        f'        <div class="mini-stat">{ic(icon)}<span><b>{b}</b> {label}</span></div>'
        for icon, b, label in p['stats'])
    ctas = ''.join(
        f'          <a href="{h}" class="{cls}" data-sparkle>{ic(icon)}<span>{t}</span></a>'
        for h, cls, icon, t in p['ctas'])
    features = ''.join(render_feature(f, i) for i, f in enumerate(p['features']))
    tg = ''
    if p.get('tg'):
        tg = TG_BANNER.format(
            icon=ic('i-chat'), desc=p['tg_desc'],
            s1b=p['tg_stats'][0][0], s1l=p['tg_stats'][0][1],
            s2b=p['tg_stats'][1][0], s2l=p['tg_stats'][1][1])

    footer = (FOOTER
              .replace('href="#case-studies"', 'href="index.html#case-studies"')
              .replace('href="#academic-foundation"', 'href="index.html#academic-foundation"')
              .replace('href="#top"', 'href="index.html"'))

    return (render_head(p) + '\n' + render_header(p['file']) + f'''
  <main id="main" class="page">

    <!-- ============ Module hero ============ -->
    <section class="module-hero" aria-labelledby="module-hero-title">
      <div class="module-hero__inner">
        <div class="module-hero__badges">
          <span class="module-badge">{ic('i-grid')}ماژول {p['no']} از ۶ — {p['module_family']}</span>
          <span class="role-chip">{ic('i-users')}{p['role']}</span>
        </div>
        <h1 class="module-hero__title" id="module-hero-title">{p['hero_title']}</h1>
        <p class="module-hero__lead">{p['hero_lead']}</p>
        <div class="module-hero__actions">
{ctas}
        </div>
        <div class="module-hero__stats">
{stats}
        </div>
      </div>
    </section>
{p.get('custom_top', '')}
    <!-- ============ Module features ============ -->
{features}
{tg}{render_strip(p['file'])}{render_cta(p['cta'])}  </main>

  {footer}
</body>
</html>
''')


def main():
    for p in PAGES:
        out = ROOT / p['file']
        out.write_text(render_page(p), encoding='utf-8')
        print(f'built {p["file"]:18s} {out.stat().st_size:>8,} bytes')


if __name__ == '__main__':
    main()
