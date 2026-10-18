#!/usr/bin/env python3
"""One-shot updater: adds the 6-module architecture to the landing page.
(Kept in tools/ for traceability; run once — subsequent edits go to index.html directly.)
"""
import sys

P = 'about.html'
s = open(P, encoding='utf-8').read()
orig = s

def rep(old, new, count=1):
    global s
    if old not in s:
        sys.exit('PATTERN NOT FOUND:\n' + old[:120])
    s = s.replace(old, new, count)

# 1) module-pages.css
rep('<link rel="stylesheet" href="assets/css/rtl-override.css">',
    '<link rel="stylesheet" href="assets/css/rtl-override.css">\n'
    '  <link rel="stylesheet" href="assets/css/module-pages.css">')

# 2) desktop nav: 9 section anchors -> 7 module links
rep('''        <a class="nav__link" href="#hero">خانه</a>
        <a class="nav__link" href="#dashboard">پیشخوان CMMS</a>
        <a class="nav__link" href="#capabilities">ارکان سه‌گانه</a>
        <a class="nav__link" href="#regional-nodes">شبکه ۱۴ گره</a>
        <a class="nav__link" href="#monitoring">مانیتورینگ و عیب‌یابی</a>
        <a class="nav__link" href="#ecosystem">بازیگران</a>
        <a class="nav__link" href="#business-model">مدل اقتصادی ۲٪</a>
        <a class="nav__link" href="#case-studies">تجارب بالینی</a>
        <a class="nav__link" href="#academic-foundation">مبانی نظری</a>''',
    '''        <a class="nav__link is-active" href="#hero" aria-current="page">خانه</a>
        <a class="nav__link" href="hospital.html">پنل بیمارستان</a>
        <a class="nav__link" href="technicians.html">پنل تکنسین</a>
        <a class="nav__link" href="marketplace.html">بازارگاه B2B</a>
        <a class="nav__link" href="students.html">هاب دانشجویی</a>
        <a class="nav__link" href="odr.html">داوری آنلاین</a>
        <a class="nav__link" href="academy.html">آکادمی</a>''')

# 3) mobile menu links
rep('''      <a href="#hero">خانه</a>
      <a href="#dashboard">پیشخوان CMMS</a>
      <a href="#capabilities">ارکان سه‌گانه</a>
      <a href="#regional-nodes">شبکه ۱۴ گره</a>
      <a href="#monitoring">مانیتورینگ و عیب‌یابی</a>
      <a href="#ecosystem">بازیگران</a>
      <a href="#business-model">مدل اقتصادی ۲٪</a>
      <a href="#case-studies">تجارب بالینی</a>
      <a href="#academic-foundation">مبانی نظری</a>''',
    '''      <a href="#hero">خانه</a>
      <a href="hospital.html">پنل بیمارستان و مراکز درمانی</a>
      <a href="technicians.html">پنل تکنسین‌ها و تعمیرکاران</a>
      <a href="marketplace.html">بازارگاه B2B تأمین‌کنندگان</a>
      <a href="students.html">هاب دانشگاه و دانشجویان</a>
      <a href="odr.html">میز داوری آنلاین (ODR)</a>
      <a href="academy.html">آکادمی و رسانه تخصصی</a>''')

# 4) hero CTAs -> module pages
rep('<a href="#dashboard" class="btn btn--light btn--lg" data-sparkle>',
    '<a href="hospital.html" class="btn btn--light btn--lg" data-sparkle>')
rep('<a href="#ecosystem" class="btn btn--dark btn--lg" data-sparkle>',
    '<a href="#modules" class="btn btn--dark btn--lg" data-sparkle>')

# 5) header + mobile portal buttons -> module chooser
rep('<a href="#dashboard" class="btn btn--dark btn--sm" data-sparkle>',
    '<a href="#modules" class="btn btn--dark btn--sm" data-sparkle>')
rep('<a href="#dashboard" class="btn btn--dark btn--sm mobile-menu-btn">',
    '<a href="#modules" class="btn btn--dark btn--sm mobile-menu-btn">')

# 6) insert the 6-module overview section before the capabilities section
MODULES = '''    <!-- ============ ۲/الف. شش ماژول پلتفرم — هر نقش، یک پیشخوان اختصاصی ============ -->
    <section class="section modules-section" id="modules" aria-labelledby="modules-title" role="region">
      <header class="section__head" data-reveal>
        <p class="eyebrow eyebrow--blue">معماری ماژولار پلتفرم چندسویه</p>
        <h2 class="h2" id="modules-title">شش ماژول یکپارچه؛ هر بازیگر، پیشخوان اختصاصی خود</h2>
        <p class="lead">مدیکال‌نت یک پلتفرم چندوجهی (Multi-Sided Platform) است: مسئول تجهیزات بیمارستان، تکنسین، تأمین‌کننده، دانشجو و داور — هر کاربر بر اساس نقش خود وارد پیشخوان اختصاصی می‌شود</p>
      </header>
      <div class="modules-grid">
        <a class="module-card" href="hospital.html" data-reveal>
          <span class="module-card__no">M1</span>
          <div class="module-card__icon"><svg class="ic" aria-hidden="true"><use href="#i-activity"/></svg></div>
          <h3 class="module-card__title">پنل اختصاصی بیمارستان و مراکز درمانی</h3>
          <p class="module-card__desc">ویژه مهندسان پزشکی و مسئولان تجهیزات بیمارستان: از ثبت فوری خرابی تا تسویه امن خرید.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>دکمه ثبت فوری خرابی (تیکت اضطراری SOS)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>کارتابل مناقصه معکوس خرید ملزومات و قطعات</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>کیف پول سپرده امن (Escrow) و شناسنامه دیجیتال تجهیزات</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
        <a class="module-card" href="technicians.html" data-reveal>
          <span class="module-card__no">M2</span>
          <div class="module-card__icon module-card__icon--teal"><svg class="ic" aria-hidden="true"><use href="#i-tool"/></svg></div>
          <h3 class="module-card__title">پنل تکنسین‌ها و تعمیرکاران محلی</h3>
          <p class="module-card__desc">ویژه مهندسان بالینی، تعمیرکاران آزاد و کارگاه‌های فنی بومی هر منطقه.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>میز کار احراز صلاحیت و نشان اصالت (تیک آبی)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>رادار و نقشه اعلان خرابی‌های اطراف با ثبت پیشنهاد</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>مدیریت کارآموز و کسب امتیاز و تخفیف آبونمان</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
        <a class="module-card" href="marketplace.html" data-reveal>
          <span class="module-card__no">M3</span>
          <div class="module-card__icon module-card__icon--violet"><svg class="ic" aria-hidden="true"><use href="#i-cart"/></svg></div>
          <h3 class="module-card__title">تالار مناقصه و بازارگاه تأمین‌کنندگان B2B</h3>
          <p class="module-card__desc">ویژه واردکنندگان، تولیدکنندگان، داروخانه‌ها و فروشندگان قطعات یدکی.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>تالار مناقصات معکوس زنده با ثبت قیمت‌های کاهشی</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>مدیریت توکن‌های اعتباری مناقصه (حذف قیمت‌های فیک)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>فروشگاه قطعات نو و استوک تست‌شده</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
        <a class="module-card" href="students.html" data-reveal>
          <span class="module-card__no">M4</span>
          <div class="module-card__icon module-card__icon--rose"><svg class="ic" aria-hidden="true"><use href="#i-users"/></svg></div>
          <h3 class="module-card__title">هاب دانشگاه، دانشجویان و کارآموزان</h3>
          <p class="module-card__desc">ویژه دانشجویان و فارغ‌التحصیلان مهندسی پزشکی تحت نظارت دانشگاه آزاد.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>پروفایل مهارت‌محور بدون نیاز به سابقه کار</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>سامانه تطبیق کارآموزی بالینی (Mentor Matching)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>صدور گواهینامه مهارت بالینی پس از مأموریت‌ها</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
        <a class="module-card" href="odr.html" data-reveal>
          <span class="module-card__no">M5</span>
          <div class="module-card__icon module-card__icon--amber"><svg class="ic" aria-hidden="true"><use href="#i-target"/></svg></div>
          <h3 class="module-card__title">میز داوری آنلاین و حل اختلاف (ODR)</h3>
          <p class="module-card__desc">تضمین امنیت معاملات و جلوگیری از اتلاف بودجه بیمارستان بدون نیاز به دادگاه.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>ثبت پرونده اختلاف فنی و توقیف وجه امانی</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>کارتابل هیئت داوری ۳ نفره (دانشگاه، بیمارستان، نظام مهندسی)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>صدور رای قطعی حداکثر ظرف ۴۸ ساعت</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
        <a class="module-card" href="academy.html" data-reveal>
          <span class="module-card__no">M6</span>
          <div class="module-card__icon module-card__icon--slate"><svg class="ic" aria-hidden="true"><use href="#i-file-chart"/></svg></div>
          <h3 class="module-card__title">آکادمی و رسانه تخصصی (Knowledge Base)</h3>
          <p class="module-card__desc">مرجع دانش مهندسی پزشکی و ترویج شأن صنفی در سطح ملی.</p>
          <ul class="module-card__list">
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>پایگاه مقالات و راهنماهای نگهداری پیشگیرانه (PM)</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>چک‌لیست‌های گام‌به‌گام کالیبراسیون و کار با ابزار</span></li>
            <li><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span>اخبار تخصصی آیمد و استانداردهای روز سلامت</span></li>
          </ul>
          <span class="module-card__cta">ورود به ماژول <svg class="ic" aria-hidden="true"><use href="#i-arrow-right"/></svg></span>
        </a>
      </div>

      <!-- Supporting bridge: Telegram bot -->
      <div class="tg-banner" data-reveal>
        <div class="tg-banner__inner">
          <div class="tg-banner__ic"><svg class="ic" aria-hidden="true"><use href="#i-chat"/></svg></div>
          <div class="tg-banner__body">
            <p class="tg-banner__t">پل ارتباطی پشتیبان — ربات تلگرام متصل به سامانه</p>
            <p class="tg-banner__d">نسخه سبک (Lightweight Fallback) مدیکال‌نت برای شرایط کندی اینترنت: پرسنل بیمارستان بدون باز کردن سایت، خرابی را ثبت می‌کنند و تکنسین‌ها نوتیفیکیشن مناقصه و هشدار تعمیر را همان لحظه روی گوشی دریافت می‌کنند.</p>
          </div>
          <div class="tg-banner__stats">
            <div class="tg-stat"><b>۳۰ ثانیه</b>ثبت خرابی از چت</div>
            <div class="tg-stat"><b>آنی</b>اطلاع‌رسانی مناقصه‌ها</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============ ۳. ارکان سه‌گانه و قابلیت‌های بنیادین ============ -->'''
rep('    <!-- ============ ۳. ارکان سه‌گانه و قابلیت‌های بنیادین ============ -->', MODULES)

# 7) footer: modules column
rep('''          <li><a href="#dashboard">پیشخوان مدیریت CMMS بیمارستان</a></li>
          <li><a href="#capabilities">ارکان سه‌گانه و شناسنامه دیجیتال</a></li>
          <li><a href="#regional-nodes">شبکه ۱۴ گره منطقه‌ای دانشگاهی</a></li>
          <li><a href="#monitoring">موتور عیب‌یابی و پایش خطاهای بالینی</a></li>
          <li><a href="#business-model">مدل اقتصادی ۲٪ و پروتکل امانی</a></li>''',
    '''          <li><a href="hospital.html">پنل بیمارستان و مراکز درمانی</a></li>
          <li><a href="technicians.html">پنل تکنسین‌ها و تعمیرکاران</a></li>
          <li><a href="marketplace.html">بازارگاه B2B و مناقصه معکوس</a></li>
          <li><a href="students.html">هاب دانشگاه و دانشجویان</a></li>
          <li><a href="odr.html">میز داوری آنلاین (ODR)</a></li>
          <li><a href="academy.html">آکادمی و رسانه تخصصی</a></li>''')

# 8) footer: players column -> per-portal pages
rep('''          <li><a href="#ecosystem">پورتال مراکز درمانی و بیمارستان‌ها</a></li>
          <li><a href="#ecosystem">پورتال مهندسان و تکنسین‌های بالینی</a></li>
          <li><a href="#ecosystem">پورتال تأمین‌کنندگان و تولیدکنندگان</a></li>
          <li><a href="#case-studies">تجارب بالینی و داستان‌های استقرار</a></li>
          <li><a href="#academic-foundation">سنتز ۷ مقاله ژورنالی داوری‌شده</a></li>''',
    '''          <li><a href="hospital.html">پورتال مراکز درمانی و بیمارستان‌ها</a></li>
          <li><a href="technicians.html">پورتال مهندسان و تکنسین‌های بالینی</a></li>
          <li><a href="marketplace.html">پورتال تأمین‌کنندگان و تولیدکنندگان</a></li>
          <li><a href="students.html">پورتال دانشجویان و کارآموزان</a></li>
          <li><a href="#case-studies">تجارب بالینی و داستان‌های استقرار</a></li>
          <li><a href="#academic-foundation">سنتز ۷ مقاله ژورنالی داوری‌شده</a></li>''')

open(P, 'w', encoding='utf-8').write(s)
print('index.html updated OK —', len(orig), '->', len(s), 'bytes')
