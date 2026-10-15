# -*- coding: utf-8 -*-
"""Content definitions for the 6 MedicalNet module pages (used by tools/build_pages.py)."""

PAGES = [

# ════════════════════════════════ M1 — HOSPITAL ════════════════════════════════
{
 'file': 'hospital.html',
 'no': '۱', 'module_family': 'سوی تقاضا',
 'icon': 'i-activity',
 'title': 'پنل اختصاصی بیمارستان و مراکز درمانی | مدیکال‌نت',
 'desc': 'پیشخوان مهندسان پزشکی و مسئولان تجهیزات بیمارستان: ثبت فوری خرابی (SOS)، کارتابل مناقصه معکوس، کیف پول سپرده امن و شناسنامه دیجیتال تجهیزات.',
 'role': 'ویژه مهندسان پزشکی و مسئولان تجهیزات بیمارستان',
 'hero_title': 'پنل اختصاصی بیمارستان و مراکز درمانی (Hospital Dashboard)',
 'hero_lead': 'از لحظه‌ای که پرسنل بخش علامت خرابی را می‌بینند تا لحظه‌ای که دستگاه تست‌شده و سالم به چرخه درمان برمی‌گردد — همه‌چیز در یک پیشخوان: تیکت اضطراری، مناقصه معکوس خرید، حساب امانی و شناسنامه دیجیتال تجهیزات.',
 'stats': [
   ('i-zap', '۳۰ ثانیه', 'ثبت تیکت اضطراری'),
   ('i-clock', '۱.۸ تا ۴ ساعت', 'زمان حضور تکنسین منطقه‌ای'),
   ('i-shield', '۱۰۰٪', 'تسویه مشروط به تأیید فنی'),
 ],
 'ctas': [
   ('#f-sos', 'btn btn--dark btn--lg', 'i-zap', 'ثبت خرابی اضطراری'),
   ('marketplace.html', 'btn btn--light btn--lg', 'i-cart', 'مشاهده بازارگاه B2B'),
 ],
 'features': [
  {
   'kicker': 'تیکت اضطراری / SOS', 'kicker_icon': 'i-alert-triangle',
   'title': 'دکمه ثبت فوری خرابی (SOS) — فرم بسیار ساده و سریع',
   'desc': 'پرسنل بخش نیازی به فرم‌های طولانی و اصطلاحات فنی ندارند. انتخاب نوع دستگاه، کد اموال و یک عکس یا وویس کوتاه؛ سیستم بقیه را انجام می‌دهد.',
   'checks': [
     'انتخاب سریع نوع دستگاه: مانیتور علائم حیاتی، پمپ سرم، تخت، اکسیژن‌ساز، فشارسنج و…',
     'درج کد اموال برای اتصال خودکار به شناسنامه دیجیتال همان دستگاه',
     'بارگذاری عکس یا وویس شرح خرابی — بدون تایپ توضیح فنی',
     'ارسال آنی درخواست برای نزدیک‌ترین تکنسین‌های دارای تیک آبی در همان شهر (بجنورد، شیروان یا منطقه)',
   ],
   'note': ('i-info', 'اولویت‌بندی هوشمند: تیکت‌های بخش‌های حیاتی ICU و اتاق عمل در صف دیسپچینگ منطقه‌ای در بالاترین اولویت قرار می‌گیرند.'),
   'panel_name': 'medicalnet.ir / sos — ثبت تیکت اضطراری',
   'panel': '''<div class="mock-field">
  <label>نوع دستگاه</label>
  <div class="mock-select"><svg class="ic" aria-hidden="true"><use href="#i-chevron-down"/></svg>مانیتور علائم حیاتی (پایش بیمار)</div>
</div>
<div class="mock-row">
  <div class="mock-field">
    <label>کد اموال</label>
    <div class="mock-input" dir="ltr">IR-1404-AMH-2213</div>
  </div>
  <div class="mock-field">
    <label>بخش</label>
    <div class="mock-input">ICU — بیمارستان امام حسن (ع)</div>
  </div>
</div>
<div class="mock-file-drop">
  <svg class="ic" aria-hidden="true"><use href="#i-phone"/></svg>
  پیوست عکس یا وویس شرح خرابی (اختیاری)
  <span class="mock-tag-row"><span class="mock-tag">📷 عکس صفحه دستگاه</span><span class="mock-tag">🎙️ وویس ۲۰ ثانیه‌ای پرستار</span></span>
</div>
<button class="sos-btn" type="button"><span class="pulse"></span>ثبت فوری و ارسال به تکنسین‌های نزدیک</button>
<p class="mock-hint">پس از ثبت، ۴ تکنسین تیک‌آبی شهر شما به‌صورت هم‌زمان مطلع می‌شوند</p>''',
  },
  {
   'kicker': 'کارتابل خرید', 'kicker_icon': 'i-trending-down',
   'title': 'کارتابل مناقصه معکوس خرید ملزومات و قطعات',
   'desc': 'به‌جای تماس‌های تلفنی و استعلام‌های قیمتی چندروزه، استعلام حجمی خود را ثبت کنید و تماشا کنید که شرکت‌ها در جدول رقابتی قیمت‌هایشان را لحظه‌به‌لحظه پایین می‌آورند.',
   'checks': [
     'ثبت استعلام حجمی اقلام مصرفی: سرنگ، لوله سرم، کاف فشارسنج، انکودر مانیتور یا لامپ UV',
     'مشاهده لحظه‌ای کاهش قیمت‌ها توسط شرکت‌ها در جدول رقابتی شفاف',
     'انتخاب خودکار بهترین پیشنهاد از نظر قیمت، گارانتی و زمان تحویل',
     'تاریخچه کامل قیمت‌ها برای مذاکره و بودجه‌بندی دوره بعد',
   ],
   'note': ('i-shield', 'فقط تأمین‌کنندگان احراز صلاحیت‌شده با هویت رسمی به مناقصه دسترسی دارند؛ قیمت‌دهی صوری و دلالی در تالار فیلتر می‌شود.'),
   'panel_name': 'استعلام شماره INQ-14040921 — مناقصه معکوس زنده',
   'panel': '''<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;">
  <span class="mock-tag mock-tag--active">۲٬۴۰۰ عدد کاف فشارسنج بزرگسال</span>
  <span class="countdown-chip"><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>پایان مناقصه: ۲۲ دقیقه</span>
</div>
<table class="auction-table">
  <thead><tr><th>تأمین‌کننده</th><th class="hide-sm">پیشنهاد قبلی</th><th>آخرین پیشنهاد</th><th class="hide-sm">کاهش</th><th></th></tr></thead>
  <tbody>
    <tr><td class="bid-co">شرکت مهندسی پزشکی سلامت گستر</td><td class="hide-sm"><span class="bid-old">۹۸٬۰۰۰</span></td><td><span class="bid-new">۹۱٬۵۰۰ تومان</span></td><td class="hide-sm"><span class="bid-drop"><svg class="ic" aria-hidden="true"><use href="#i-trending-down"/></svg>٪۶.۶</span></td><td><span class="auction-best-chip">برنده لحظه‌ای</span></td></tr>
    <tr><td class="bid-co">پترو تجارت ایرانیان</td><td class="hide-sm"><span class="bid-old">۱۰۴٬۰۰۰</span></td><td><span class="bid-new">۹۴٬۲۰۰ تومان</span></td><td class="hide-sm"><span class="bid-drop"><svg class="ic" aria-hidden="true"><use href="#i-trending-down"/></svg>٪۹.۴</span></td><td></td></tr>
    <tr><td class="bid-co">مهرگان مد شریف</td><td class="hide-sm">—</td><td>۹۷٬۸۰۰ تومان</td><td class="hide-sm">—</td><td></td></tr>
  </tbody>
</table>
<p class="mock-hint">انتخاب خودکار: ارزان‌ترین پیشنهاد منطبق با مشخصات فنی و گارانتی</p>''',
   'reverse': True,
  },
  {
   'kicker': 'تسویه امن', 'kicker_icon': 'i-wallet',
   'title': 'کیف پول سپرده امن (Escrow Wallet)',
   'desc': 'وجه قرارداد تعمیر یا خرید قطعه به حساب امانی مدیکال‌نت واریز و بلوکه می‌شود — تا زمانی که بیمارستان سلامت دستگاه را تست و تأیید نکند، حتی یک ریال به حساب تکنسین یا فروشنده واریز نمی‌شود.',
   'checks': [
     'واریز وجه قرارداد به حساب امانی و بلوکه‌شدن آن پیش از شروع کار',
     'آزادسازی وجه فقط پس از تأیید فنی سرپرست تجهیزات و پروتکل پذیرش بالینی',
     'مسیر شفاف بودجه: از تخصیص تا تسویه نهایی، قابل ارائه به حسابرسی بیمارستان',
     'اتصال مستقیم به میز داوری آنلاین در صورت اختلاف فنی',
   ],
   'panel_name': 'کیف پول امانی — قرارداد شماره ESC-1404-551',
   'panel': '''<div class="escrow-balance">
  <div class="escrow-balance__lbl">مبلغ تضمین‌شده در حساب امانی<b>۴۸٬۵۰۰٬۰۰۰ تومان</b></div>
  <span class="escrow-balance__state"><svg class="ic" aria-hidden="true"><use href="#i-shield"/></svg>بلوکه — منتظر تأیید فنی</span>
</div>
<div class="escrow-steps">
  <div class="escrow-step escrow-step--done"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span class="escrow-step__t">واریز به امانی</span><span class="escrow-step__d">تأیید شد</span></div>
  <div class="escrow-step escrow-step--done"><svg class="ic" aria-hidden="true"><use href="#i-tool"/></svg><span class="escrow-step__t">انجام تعمیر</span><span class="escrow-step__d">تکمیل کار</span></div>
  <div class="escrow-step"><svg class="ic" aria-hidden="true"><use href="#i-activity"/></svg><span class="escrow-step__t">تست بالینی ۲۴ ساعته</span><span class="escrow-step__d">در جریان…</span></div>
  <div class="escrow-step"><svg class="ic" aria-hidden="true"><use href="#i-wallet"/></svg><span class="escrow-step__t">آزادسازی وجه</span><span class="escrow-step__d">پس از تأیید</span></div>
</div>''',
  },
  {
   'kicker': 'حافظه فنی بیمارستان', 'kicker_icon': 'i-file-chart',
   'title': 'شناسنامه دیجیتال تجهیزات (Asset Log)',
   'desc': 'هر دستگاه بیمارستان یک پرونده زنده دارد: از روز نصب تا آخرین خرابی. دیگر هیچ دانش فنی با رفتن یک کارمند از بیمارستان خارج نمی‌شود.',
   'checks': [
     'بایگانی کامل سوابق خرابی و ریشه‌یابی هر دستگاه بر پایه کد اموال',
     'تاریخچه تعمیرات، قطعات تعویض‌شده و هزینه‌های واقعی هر دستگاه',
     'زمان‌بندی خودکار بازرسی‌های دوره‌ای (PM) با یادآوری پیش از موعد',
     'خروجی آماری برای مدیران: گران‌ترین دستگاه‌ها، پرمصرف‌ترین قطعات و تصمیم تعمیر در برابر خرید',
   ],
   'panel_name': 'شناسنامه دستگاه — مانیتور علائم حیاتی مارکتون M5500',
   'panel': '''<div class="asset-timeline">
  <div class="asset-tl-item asset-tl-item--ok"><span class="asset-tl-item__date">۱۴۰۴/۰۷/۰۲ — بازرسی دوره‌ای</span><span class="asset-tl-item__t">PM سوم سالانه انجام شد</span><span class="asset-tl-item__d">کالیبراسیون کامل + تست ایمنی الکتریکی IEC 62353 — نتیجه: سالم</span></div>
  <div class="asset-tl-item asset-tl-item--warn"><span class="asset-tl-item__date">۱۴۰۴/۰۴/۱۸ — خرابی</span><span class="asset-tl-item__t">خرابی پنل نمایش (شت SN3)</span><span class="asset-tl-item__d">تعمیر توسط تکنسین تیک‌آبی گره بجنورد — تعویض درایور LED — هزینه از حساب امانی</span></div>
  <div class="asset-tl-item"><span class="asset-tl-item__date">۱۴۰۳/۱۱/۰۹ — نصب اولیه</span><span class="asset-tl-item__t">راه‌اندازی و پذیرش بالینی</span><span class="asset-tl-item__d">آموزش پرسنل ICU + ثبت در سیستم FT (مدیریت دارایی فیزیکی)</span></div>
</div>
<p class="mock-hint">بازرسی دوره‌ای بعدی: ۱۴۰۴/۱۰/۰۲ — یادآوری خودکار ارسال می‌شود</p>''',
   'reverse': True,
  },
 ],
 'tg': True,
 'tg_desc': 'پرسنل بیمارستان در شرایط کندی اینترنت بدون باز کردن سایت، خرابی را از چت‌بات ثبت می‌کنند و نتیجه دیسپچینگ همان لحظه به گوشی‌شان می‌رسد.',
 'tg_stats': [('۳۰ ثانیه', 'ثبت خرابی از چت'), ('آنی', 'وضعیت تیکت‌ها')],
 'cta': {
   'title': 'آماده‌اید پیشخوان بیمارستان خود را راه‌اندازی کنید؟',
   'desc': 'از بیمارستان امام حسن (ع) بجنورد تا بزرگ‌ترین مراکز دانشگاهی کشور — مدیکال‌نت در ۱۴ گره منطقه‌ای مستقر است و اعزام تکنسین بومی از همان شهر شما انجام می‌شود.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('technicians.html', 'btn btn--dark btn--lg', 'i-tool', 'تکنسین‌های تیک‌آبی کدامند؟'),
   ],
 },
},

# ════════════════════════════════ M2 — TECHNICIANS ════════════════════════════════
{
 'file': 'technicians.html',
 'no': '۲', 'module_family': 'سوی عرضه فنی',
 'icon': 'i-tool',
 'title': 'پنل تکنسین‌ها و تعمیرکاران محلی | مدیکال‌نت',
 'desc': 'پیشخوان مهندسان بالینی، تعمیرکاران آزاد و کارگاه‌های فنی بومی: احراز صلاحیت و تیک آبی، رادار نقشه خرابی‌ها و مدیریت کارآموز.',
 'role': 'ویژه مهندسان بالینی، تعمیرکاران آزاد و کارگاه‌های فنی بومی',
 'hero_title': 'پنل تکنسین‌ها و تعمیرکاران محلی (Technician Portal)',
 'hero_lead': 'دیگر لازم نیست ماه‌ها منتظر پیمانکار پایتخت بمانید. مدیکال‌نت تکنسین بومی هر منطقه را احراز صلاحیت می‌کند، نشان اصالت می‌دهد و تیکت‌های خرابی بیمارستان‌های اطراف را مستقیم روی گوشی شما می‌آورد.',
 'stats': [
   ('i-map-pin', '۱۴ گره', 'پوشش منطقه‌ای کشور'),
   ('i-trend', '۲٪ کارمزد', 'فقط از فروشنده — خدمات فنی معاف'),
   ('i-users', '۱ کارآموز', 'قابل همراهی در هر مأموریت'),
 ],
 'ctas': [
   ('#f-verify', 'btn btn--dark btn--lg', 'i-shield', 'شروع احراز صلاحیت'),
   ('students.html', 'btn btn--light btn--lg', 'i-users', 'کارآموز می‌خواهم'),
 ],
 'features': [
  {
   'kicker': 'اعتمادسازی', 'kicker_icon': 'i-shield',
   'title': 'میز کار احراز صلاحیت و نشان اصالت (تیک آبی)',
   'desc': 'مشکل اصلی بازار پراکنده تعمیرات، نبود معیار اعتماد است. مدیکال‌نت با راستی‌آزمایی دانشگاه آزاد، تکنسین‌های واقعی را از مدعیان جدا می‌کند.',
   'checks': [
     'بارگذاری مدارک تحصیلی، دوره‌های فنی‌وحرفه‌ای یا سوابق تجربی',
     'راستی‌آزمایی مستقل مدارک توسط دانشگاه آزاد',
     'فعال‌سازی نشان تیک آبی روی پروفایل پس از تأیید',
     'رتبه‌بندی ادامه‌دار بر اساس کیفیت تعمیر، رعایت زمان‌بندی و رضایت بیمارستان',
   ],
   'note': ('i-info', 'پروفایل تیک‌آبی در ارجاع هوشمند سفارش‌ها اولویت دارد؛ هرچه رتبه بالاتر، تیکت‌های حیاتی‌تر به شما می‌رسد.'),
   'panel_name': 'پروفایل تکنسین — وضعیت احراز صلاحیت',
   'panel': '''<div class="verify-steps">
  <div class="verify-step"><span class="verify-step__n">۱</span><div><p class="verify-step__t">بارگذاری مدارک</p><p class="verify-step__d">مدرک کاردانی الکترونیک + گواهی دوره پمپ سرم وستات + ۳ سال سابقه کارگاه</p></div></div>
  <div class="verify-step"><span class="verify-step__n">۲</span><div><p class="verify-step__t">راستی‌آزمایی دانشگاه آزاد</p><p class="verify-step__d">بررسی مدرک، مصاحبه فنی تلفنی و تأیید سوابق کارگاه — ۲ روز کاری</p></div></div>
  <div class="verify-step"><span class="verify-step__n">۳</span><div><p class="verify-step__t">فعال‌سازی نشان اصالت</p><p class="verify-step__d">نشان روی پروفایل شما برای همه بیمارستان‌های منطقه قابل مشاهده است</p></div></div>
</div>
<div style="display:flex;justify-content:center;"><span class="bluetick"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>تکنسین تیک‌آبی — گره بجنورد</span></div>''',
  },
  {
   'kicker': 'دریافت سفارش', 'kicker_icon': 'i-map-pin',
   'title': 'رادار و نقشه اعلان خرابی‌ها',
   'desc': 'تیکت‌های ثبت‌شده توسط بیمارستان‌های اطراف، به‌صورت زنده روی نقشه رادار شما ظاهر می‌شوند؛ قیمت و زمان حضور پیشنهادی‌تان را ثبت کنید و منتظر انتخاب بیمارستان بمانید.',
   'checks': [
     'مشاهده تیکت‌های خرابی بیمارستان‌های حوالی روی نقشه شهر و منطقه',
     'ثبت قیمت پیشنهادی + زمان حضور (مثلاً ظرف ۲ ساعت در محل)',
     'نمایش فاصله، نوع دستگاه، اولویت بالینی و بودجه حدودی هر تیکت',
     'پذیرش خودکار مأموریت‌های اضطراری ICU برای نزدیک‌ترین تیک‌آبی آنلاین',
   ],
   'panel_name': 'رادار خرابی‌ها — شعاع ۵۰ کیلومتری بجنورد',
   'panel': '''<div class="radar-list">
  <div class="radar-item"><span class="radar-item__pin"><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg></span><div class="radar-item__body"><span class="radar-item__t">بیمارستان امام حسن (ع) — مانیتور علائم حیاتی ICU</span><span class="radar-item__d"><span><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>۲.۱ کیلومتر</span><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>فوری (کمتر از ۲ ساعت)</span></span></div><span class="radar-chip">ثبت پیشنهاد</span></div>
  <div class="radar-item"><span class="radar-item__pin"><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg></span><div class="radar-item__body"><span class="radar-item__t">درمانگاه شیروان — پمپ سرم وستات</span><span class="radar-item__d"><span><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>۴۳ کیلومتر</span><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>امروز</span></span></div><span class="radar-chip">ثبت پیشنهاد</span></div>
  <div class="radar-item"><span class="radar-item__pin radar-item__pin--warn"><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg></span><div class="radar-item__body"><span class="radar-item__t">بیمارستان ولیعصر (عج) — تخت جراحی هیدرولیک</span><span class="radar-item__d"><span><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg>۵۱ کیلومتر</span><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>فردا صبح</span></span></div><span class="radar-chip">ثبت پیشنهاد</span></div>
</div>
<p class="mock-hint">پیشنهادها در جدول رقابتی بیمارستان به‌صورت ناشناس رقابت می‌کنند</p>''',
   'reverse': True,
  },
  {
   'kicker': 'مزیت دوطرفه', 'kicker_icon': 'i-users',
   'title': 'بخش مدیریت کارآموز',
   'desc': 'در هر مأموریت بیمارستانی می‌توانید یک دانشجوی کارآموز مهندسی پزشکی را با خود همراه ببرید: شما امتیاز کاربری و تخفیف آبونمان می‌گیرید، دانشجو تجربه عملیاتی واقعی.',
   'checks': [
     'تأیید و همراه‌بردن یک دانشجوی کارآموز در مأموریت‌های بیمارستانی',
     'کسب امتیاز کاربری برای هر مأموریت همراهی‌دار',
     'تخفیف پلکانی در آبونمان سالانه پنل تکنسین',
     'سهم‌گذاری تجربه با نسل بعد؛ تقویت شبکه مهندسان بالینی منطقه',
   ],
   'panel_name': 'کارآموز مأموریت BMC-1404-883',
   'panel': '''<div class="mentor-flow">
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-users"/></svg><span class="mentor-step__t">درخواست دانشجو</span><span class="mentor-step__d">انتخاب از لیست دانشجویان مهارت‌محور همان شهر</span></div>
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg><span class="mentor-step__t">همراهی در بیمارستان</span><span class="mentor-step__d">حضور تحت نظارت در تعمیر مانیتور ICU</span></div>
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-star"/></svg><span class="mentor-step__t">دریافت امتیاز</span><span class="mentor-step__d">+۱۵ امتیاز معادل ۲۰٪ تخفیف آبونمان</span></div>
</div>
<p class="mock-hint">دانشجو پس از مأموریت موفق، امضای مهارت شما را در گواهینامه خود می‌گیرد</p>''',
  },
 ],
 'tg': True,
 'tg_desc': 'هشدارهای تعمیر و مناقصه‌های جدید منطقه، همان لحظه به‌صورت نوتیفیکیشن تلگرام به گوشی شما می‌رسد — بدون باز کردن مرورگر.',
 'tg_stats': [('آنی', 'اعلان تیکت‌های جدید'), ('۰ ریال', 'هزینه دریافت نوتیفیکیشن')],
 'cta': {
   'title': 'تکنسین بومی هستید؟ جای شما در شبکه مدیکال‌نت خالی است',
   'desc': 'ثبت‌نام و احراز صلاحیت رایگان است؛ کارمزدی از خدمات فنی شما گرفته نمی‌شود — کارمزد ۲٪ فقط از فروشندگان کالاست.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('hospital.html', 'btn btn--dark btn--lg', 'i-activity', 'پیشخوان بیمارستان‌ها'),
   ],
 },
},

# ════════════════════════════════ M3 — MARKETPLACE ════════════════════════════════
{
 'file': 'marketplace.html',
 'no': '۳', 'module_family': 'سوی عرضه کالا',
 'icon': 'i-cart',
 'title': 'تالار مناقصه و بازارگاه تأمین‌کنندگان B2B | مدیکال‌نت',
 'desc': 'پیشخوان واردکنندگان، تولیدکنندگان، داروخانه‌ها و فروشندگان قطعات یدکی: مناقصات معکوس زنده، مدیریت توکن‌های اعتباری و فروشگاه قطعات.',
 'role': 'ویژه واردکنندگان، تولیدکنندگان، داروخانه‌ها و فروشندگان قطعات یدکی',
 'hero_title': 'تالار مناقصه و بازارگاه تأمین‌کنندگان (B2B Marketplace)',
 'hero_lead': 'مستقیم و بدون واسطه با بیمارستان‌های کشور معامله کنید: درخواست‌های خرید عمده را ببینید، در مناقصه معکوس قیمت بدهید و غرفه اختصاصی قطعات خود را راه بیندازید.',
 'stats': [
   ('i-cart', '۳ دسته', 'قطعات یدکی، مصرفی، سرمایه‌ای'),
   ('i-trending-down', 'کارمزد ۲٪', 'فقط از فروشنده کالای پذیرفته‌شده'),
   ('i-shield', 'تسویه امانی', 'بدون ریسک نکول بیمارستان'),
 ],
 'ctas': [
   ('#f-auction', 'btn btn--dark btn--lg', 'i-trending-down', 'ورود به تالار مناقصات'),
   ('#f-shop', 'btn btn--light btn--lg', 'i-cart', 'راه‌اندازی غرفه فروش'),
 ],
 'features': [
  {
   'kicker': 'حراج معکوس', 'kicker_icon': 'i-trending-down',
   'title': 'تالار مناقصات معکوس زنده',
   'desc': 'لیست درخواست‌های خرید عمده بیمارستان‌ها را مشاهده کنید و تا پایان مهلت، قیمت‌های کاهشی خود را ثبت کنید — رقابت شفاف، برنده واقعی.',
   'checks': [
     'مشاهده لیست درخواست‌های خرید عمده بیمارستان‌ها با مشخصات فنی کامل',
     'ثبت قیمت‌های کاهشی تا پایان مهلت مناقصه، بدون تماس تلفنی',
     'نمایش زنده رتبه پیشنهاد شما نسبت به رقبا (بدون افشای هویت)',
     'اعلان خودکار به برنده و اتصال مستقیم به قرارداد و تسویه امانی',
   ],
   'note': ('i-shield', 'قیمت‌دهی صوری و دلالی در تالار فیلتر می‌شود: هر شرکت باید برای باز کردن هر مناقصه یک توکن اعتباری مصرف کند.'),
   'panel_name': 'تالار مناقصات باز — امروز',
   'panel': '''<div class="radar-list">
  <div class="radar-item"><span class="radar-item__pin"><svg class="ic" aria-hidden="true"><use href="#i-cart"/></svg></span><div class="radar-item__body"><span class="radar-item__t">۵٬۰۰۰ عدد سرنگ ۵cc — ۱۲ بیمارستان استان خراسان شمالی</span><span class="radar-item__d"><span class="countdown-chip"><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۴ ساعت باقی‌مانده</span><span>۱۷ شرکت حاضر</span></span></div><span class="radar-chip">شروع رقابت</span></div>
  <div class="radar-item"><span class="radar-item__pin"><svg class="ic" aria-hidden="true"><use href="#i-cart"/></svg></span><div class="radar-item__body"><span class="radar-item__t">۴۰ عدد لامپ UV گرمایی دستگاه ضدعفونی — بیمارستان امام حسن (ع)</span><span class="radar-item__d"><span class="countdown-chip"><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۲۲ دقیقه باقی‌مانده</span><span>۵ شرکت حاضر</span></span></div><span class="radar-chip">شروع رقابت</span></div>
  <div class="radar-item"><span class="radar-item__pin radar-item__pin--warn"><svg class="ic" aria-hidden="true"><use href="#i-cart"/></svg></span><div class="radar-item__body"><span class="radar-item__t">۲ عدد انکودر مانیتور مارکتون M5500 — مرکز درمانی ولیعصر (عج)</span><span class="radar-item__d"><span class="countdown-chip"><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۱ روز باقی‌مانده</span><span>۲ شرکت حاضر</span></span></div><span class="radar-chip">شروع رقابت</span></div>
</div>''',
  },
  {
   'kicker': 'فیلتر کیفیت', 'kicker_icon': 'i-star',
   'title': 'مدیریت توکن‌های مناقصه',
   'desc': 'برای باز کردن هر مناقصه و ثبت نرخ، یک توکن اعتباری مصرف می‌شود؛ همین مکانیزم ساده، دلالان و قیمت‌های فیک را از تالار بیرون می‌کند و وقت بیمارستان و فروشنده واقعی را آزاد می‌کند.',
   'checks': [
     'خرید بسته‌های اعتباری توکن متناسب با حجم فعالیت شرکت',
     'مصرف یک توکن برای باز کردن هر مناقصه و ثبت نرخ',
     'بازگشت خودکار توکن در صورت لغو مناقصه توسط بیمارستان',
     'گزارش شفاف مصرف توکن‌ها و بازدهی هر مناقصه برای شرکت',
   ],
   'panel_name': 'بسته‌های اعتباری توکن',
   'panel': '''<div class="token-grid">
  <div class="token-card"><span class="token-card__n">۱۰ <small>توکن</small></span><span class="token-card__p">استارتر</span><span class="token-card__d">مناسب شروع فعالیت و تست بازار — ۳ ماه اعتبار</span></div>
  <div class="token-card token-card--hot"><span class="token-card__ribbon">پرمصرف‌ترین</span><span class="token-card__n">۵۰ <small>توکن</small></span><span class="token-card__p">حرفه‌ای</span><span class="token-card__d">برای شرکت‌های فعال در مناقصات استانی — ۶ ماه اعتبار</span></div>
  <div class="token-card"><span class="token-card__n">۲۰۰ <small>توکن</small></span><span class="token-card__p">سازمانی</span><span class="token-card__d">برای واردکنندگان و تولیدکنندگان سراسری — ۱۲ ماه اعتبار</span></div>
</div>
<p class="mock-hint">توکن مصرفی فقط در صورت مشاهده مشخصات کامل مناقصه کسر می‌شود</p>''',
   'reverse': True,
  },
  {
   'kicker': 'غرفه اختصاصی', 'kicker_icon': 'i-grid',
   'title': 'فروشگاه قطعات و ملزومات',
   'desc': 'غرفه اختصاصی خود را راه بیندازید و قطعات یدکی نو یا استوک تست‌شده را با قیمت شفاف به بیمارستان‌ها و تکنسین‌های سراسر کشور بفروشید.',
   'checks': [
     'فروش قطعات یدکی نو با فاکتور رسمی و گارانتی',
     'فروش استوک تست‌شده با درج شفاف وضعیت و نتایج تست',
     'دسته‌بندی تخصصی: جک و پدال تخت، قطعات الکترونیک، زئولیت اکسیژن‌ساز و…',
     'تسویه امانی: پول شما پس از تأیید تحویل توسط بیمارستان آزاد می‌شود',
   ],
   'panel_name': 'غرفه شما — دسته‌بندی محصولات',
   'panel': '''<div class="shop-grid">
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-tool"/></svg></span><div><div class="shop-item__t">جک و پدال تخت جراحی</div><div class="shop-item__d">۴۲ قلم — نو و استوک تست‌شده</div></div></div>
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-zap"/></svg></span><div><div class="shop-item__t">قطعات الکترونیک و برد</div><div class="shop-item__d">درایور LED، ماژول پمپ، منبع تغذیه</div></div></div>
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-activity"/></svg></span><div><div class="shop-item__t">زئولیت اکسیژن‌ساز PSA</div><div class="shop-item__d">ساکشن‌شده بسته ۱۰ کیلویی — تحویل ۴۸ ساعته</div></div></div>
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-search"/></svg></span><div><div class="shop-item__t">انکودر و سنسور مانیتور</div><div class="shop-item__d">سازگار با مارکتون، زیمنس، درگر</div></div></div>
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-target"/></svg></span><div><div class="shop-item__t">کاف، پوآر و ملزومات فشارسنج</div><div class="shop-item__d">فروش عمده به ۱۲ بیمارستان</div></div></div>
  <div class="shop-item"><span class="shop-item__ic"><svg class="ic" aria-hidden="true"><use href="#i-file-chart"/></svg></span><div><div class="shop-item__t">لامپ UV و قطعات ضدعفونی</div><div class="shop-item__d">اصلی ژاپن — با تست عملکرد</div></div></div>
</div>''',
  },
 ],
 'tg': True,
 'tg_desc': 'مناقصه‌های جدیدِ مرتبط با حوزه فعالیت شرکت شما، همان لحظه به‌صورت نوتیفیکیشن تلگرام اعلام می‌شود تا هیچ فرصتی از دست نرود.',
 'tg_stats': [('آنی', 'اعلان مناقصه‌های جدید'), ('هدفمند', 'فقط حوزه فعالیت شما')],
 'cta': {
   'title': 'شرکت شما، بدون واسطه در کنار بیمارستان‌های کشور',
   'desc': 'احراز هویت رسمی، توکن اعتباری و تسویه امانی — سه لایه اطمینانی که معامله B2B پزشکی را از تماس‌های تلفنی به قرارداد شفاف تبدیل می‌کند.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('hospital.html', 'btn btn--dark btn--lg', 'i-activity', 'پیشخوان بیمارستان‌ها'),
   ],
 },
},

# ════════════════════════════════ M4 — STUDENTS ════════════════════════════════
{
 'file': 'students.html',
 'no': '۴', 'module_family': 'سوی توسعه سرمایه انسانی',
 'icon': 'i-users',
 'title': 'هاب دانشگاه، دانشجویان و کارآموزان | مدیکال‌نت',
 'desc': 'پیشخوان دانشجویان و فارغ‌التحصیلان مهندسی پزشکی: پروفایل مهارت‌محور بدون نیاز به سابقه کار، تطبیق کارآموزی بالینی و گواهینامه مهارت.',
 'role': 'ویژه دانشجویان و فارغ‌التحصیلان مهندسی پزشکی — تحت نظارت دانشگاه آزاد',
 'hero_title': 'هاب دانشگاه، دانشجویان و کارآموزان (Student & Career Hub)',
 'hero_lead': 'مسئله کلاسیک بازار کار: «بدون سابقه استخدام نمی‌شوی، بدون استخدام سابقه نمی‌گیری». مدیکال‌نت با نظارت دانشگاه آزاد این چرخه را می‌شکند — با مهارت‌های ملموس به‌جای رزومه خالی.',
 'stats': [
   ('i-users', '۱۰۰٪', 'پروفایل مبتنی بر مهارت، نه سابقه'),
   ('i-check', 'تأیید دانشگاه', 'نظارت علمی بر فرآیند کارآموزی'),
   ('i-star', 'گواهینامه', 'مهارت بالینی پس از مأموریت‌های واقعی'),
 ],
 'ctas': [
   ('#f-profile', 'btn btn--dark btn--lg', 'i-users', 'ساخت پروفایل مهارتی'),
   ('#f-mentor', 'btn btn--light btn--lg', 'i-search', 'یافتن استاد کارآموزی'),
 ],
 'features': [
  {
   'kicker': 'جایگزین رزومه سنتی', 'kicker_icon': 'i-star',
   'title': 'پروفایل مهارت‌محور (بدون نیاز به سابقه کار)',
   'desc': 'به‌جای فهرست مشاغل خالی، مهارت‌های ملموس آزمایشگاهی‌تان را ثبت کنید؛ همین مهارت‌ها شما را در سیستم تطبیق کارآموزی به تکنسین‌های مناسب وصل می‌کند.',
   'checks': [
     'ثبت مهارت‌های عملی آزمایشگاهی به‌جای رزومه سنتی',
     'کار با هویه و لحیم‌کاری قطعات الکترونیکی',
     'تست قطعات با مولتی‌متر و عیب‌یابی مدار',
     'کالیبراسیون فشارسنج و تعمیر برد در محیط کنترل‌شده',
   ],
   'note': ('i-info', 'هر مهارت با تأیید آزمایشگاه دانشگاه یا استاد کارآموزی مهر اعتبار می‌گیرد و در پروفایل شما نمایش داده می‌شود.'),
   'panel_name': 'پروفایل مهارتی — دانشجوی مهندسی پزشکی',
   'panel': '''<div class="skill-chips">
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>کار با هویه و لحیم‌کاری SMD</span>
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>تست قطعات با مولتی‌متر</span>
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>کالیبراسیون فشارسنج دیجیتال</span>
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>تعمیر برد منبع تغذیه</span>
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>عیب‌یابی پمپ سرم</span>
  <span class="skill-chip"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>خواندن شماتیک الکترونیکی</span>
</div>
<p class="mock-hint">مهارت‌ها پس از هر مأموریت بیمارستانی موفق، به‌صورت خودکار تکمیل می‌شوند</p>''',
  },
  {
   'kicker': 'پل تجربه', 'kicker_icon': 'i-compass',
   'title': 'سامانه تطبیق کارآموزی بالینی (Mentor Matching)',
   'desc': 'سیستم بر اساس مهارت‌ها، شهر و حوزه علاقه، شما را به تکنسین‌های تیک‌آبی همان منطقه وصل می‌کند تا در محیط واقعی بیمارستان تجربه عملیاتی جمع کنید.',
   'checks': [
     'اتصال به تکنسین‌های دارای تیک آبی در شهر یا منطقه شما',
     'حضور نظارت‌شده در مأموریت‌های واقعی تعمیر بیمارستانی',
     'انتخاب حوزه تمرکز: تجهیزات ICU، اتاق عمل، آزمایشگاه یا دیالیز',
     'هماهنگی سه‌جانبه دانشجو، تکنسین و دانشگاه آزاد',
   ],
   'panel_name': 'تطبیق کارآموزی — فرآیند ۳ مرحله‌ای',
   'panel': '''<div class="mentor-flow">
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-search"/></svg><span class="mentor-step__t">۱. ثبت مهارت و شهر</span><span class="mentor-step__d">مثلاً لحیم‌کاری + بجنورد</span></div>
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-users"/></svg><span class="mentor-step__t">۲. اتصال به تکنسین تیک‌آبی</span><span class="mentor-step__d">انتخاب از میان ۱۲ استاد بالینی منطقه</span></div>
  <div class="mentor-step"><svg class="ic" aria-hidden="true"><use href="#i-map-pin"/></svg><span class="mentor-step__t">۳. حضور در بیمارستان</span><span class="mentor-step__d">مأموریت‌های واقعی زیر نظارت مستقیم</span></div>
</div>
<p class="mock-hint">تکنسین برای همراهی شما امتیاز و تخفیف آبونمان دریافت می‌کند — برد برد دوطرفه</p>''',
   'reverse': True,
  },
  {
   'kicker': 'خروجی قابل ارائه', 'kicker_icon': 'i-file-chart',
   'title': 'گواهینامه مهارت بالینی',
   'desc': 'پس از گذراندن موفق مأموریت‌های تعمیراتی، گواهینامه مهارت بالینی با امضای تکنسین ناظر و تأیید دانشگاه آزاد صادر می‌شود — سندی که کارفرما واقعی می‌فهمد.',
   'checks': [
     'صدور گواهینامه پس از هر مأموریت موفق با جزئیات تجهیزات کارشده',
     'امضای الکترونیک تکنسین ناظر + تأیید دانشگاه آزاد',
     'سابقه‌ای زنده و قابل استناد برای استخدام و مصاحبه‌ها',
     'قابلیت ارائه آنلاین لینک گواهینامه برای کارفرمایان',
   ],
   'panel_name': 'نمونه گواهینامه مهارت بالینی',
   'panel': '''<div class="cert-card">
  <span class="cert-card__seal"><svg class="ic" aria-hidden="true"><use href="#i-star"/></svg></span>
  <p class="cert-card__t">گواهینامه مهارت بالینی — مدیکال‌نت</p>
  <p class="cert-card__d">دارنده این گواهینامه با موفقیت در ۶ مأموریت تعمیراتی (مانیتور علائم حیاتی، پمپ سرم و تخت جراحی) زیر نظارت تکنسین تیک‌آبی شرکت کرده و مهارت‌های لحیم‌کاری، عیب‌یابی و کالیبراسیون وی تأیید گردید.</p>
  <span class="bluetick"><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>تأیید دانشگاه آزاد — واحد بجنورد</span>
</div>''',
  },
 ],
 'tg': False,
 'cta': {
   'title': 'از آزمایشگاه دانشگاه تا اتاق ICU — مسیرتان را امروز شروع کنید',
   'desc': 'هاب دانشجویی مدیکال‌نت زیر نظارت دانشگاه آزاد اداره می‌شود؛ تجربه‌ای که در هیچ کلاس درسی به دست نمی‌آید.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('technicians.html', 'btn btn--dark btn--lg', 'i-tool', 'استادان کارآموزی (تکنسین‌ها)'),
   ],
 },
},

# ════════════════════════════════ M5 — ODR ════════════════════════════════
{
 'file': 'odr.html',
 'no': '۵', 'module_family': 'حاکمیت داده و اعتماد',
 'icon': 'i-target',
 'title': 'میز داوری آنلاین و حل اختلاف (ODR) | مدیکال‌نت',
 'desc': 'سامانه حل اختلاف فنی مدیکال‌نت: ثبت پرونده اختلاف، کارتابل هیئت داوری ۳ نفره و صدور رای قطعی ظرف ۴۸ ساعت بدون نیاز به دادگاه.',
 'role': 'تضمین امنیت معاملات برای بیمارستان، تکنسین و فروشنده',
 'hero_title': 'میز داوری آنلاین و حل اختلاف (Online Dispute Resolution)',
 'hero_lead': 'اگر قطعه کار نکرد یا دستگاه پس از ۲۴ ساعت دوباره سوخت، بحث و جدل تمام است: وجه در حساب امانی بلوکه مانده و یک هیئت داوری تخصصی ۳ نفره ظرف ۴۸ ساعت رای قطعی صادر می‌کند — بدون نیاز به دادگاه و هزینه وکیل.',
 'stats': [
   ('i-clock', '۴۸ ساعت', 'حداکثر زمان صدور رای قطعی'),
   ('i-users', '۳ داور', 'دانشگاه + بیمارستان + نظام مهندسی'),
   ('i-wallet', '۰ ریال', 'خروج وجه بدون رای — غیرممکن'),
 ],
 'ctas': [
   ('#f-dispute', 'btn btn--dark btn--lg', 'i-alert-triangle', 'ثبت پرونده اختلاف'),
   ('#f-panel', 'btn btn--light btn--lg', 'i-users', 'آشنایی با هیئت داوری'),
 ],
 'features': [
  {
   'kicker': 'شروع پرونده', 'kicker_icon': 'i-alert-triangle',
   'title': 'ثبت پرونده اختلاف فنی',
   'desc': 'بیمارستان دکمه «گزارش عیب / توقیف وجه» را می‌زند؛ وجه باقی‌مانده قرارداد همان لحظه در حساب امانی مسدود می‌شود و پرونده با تمام مدارک فنی تشکیل می‌گردد.',
   'checks': [
     'ثبت اختلاف با یک کلیک: گزارش عیب یا خرابی مجدد پس از تحویل',
     'توقیف خودکار وجه در حساب امانی تا پایان داوری',
     'پیوست خودکار مدارک: عکس‌ها، وویس‌ها، گزارش تکنسین و شناسنامه دستگاه',
     'اطلاع‌رسانی هم‌زمان به طرفین با مهلت پاسخ‌گویی مشخص',
   ],
   'note': ('i-info', 'سناریوی نمونه: دستگاه پس از تعمیر ۲۴ ساعته دوباره سوخت — بیمارستان گزارش می‌دهد، وجه بلوکه می‌شود، داوری آغاز می‌شود.'),
   'panel_name': 'پرونده اختلاف DSP-1404-019 — در حال بررسی',
   'panel': '''<div class="dispute-flow">
  <div class="dispute-step"><svg class="ic" aria-hidden="true"><use href="#i-alert-triangle"/></svg><span class="dispute-step__t">۱. گزارش عیب</span><span class="dispute-step__d">دکمه «گزارش عیب / توقیف وجه» توسط بیمارستان</span></div>
  <div class="dispute-step"><svg class="ic" aria-hidden="true"><use href="#i-wallet"/></svg><span class="dispute-step__t">۲. توقیف وجه</span><span class="dispute-step__d">۱۸٬۰۰۰٬۰۰۰ تومان در حساب امانی مسدود شد</span></div>
  <div class="dispute-step"><svg class="ic" aria-hidden="true"><use href="#i-file-chart"/></svg><span class="dispute-step__t">۳. تشکیل پرونده</span><span class="dispute-step__d">مدارک فنی، قرارداد و گزارش ۲۴ ساعته پیوست شد</span></div>
</div>
<p class="mock-hint">پرونده ظرف حداکثر ۶ ساعت به هیئت داوری ارجاع می‌شود</p>''',
  },
  {
   'kicker': 'ترکیب داوری', 'kicker_icon': 'i-users',
   'title': 'کارتابل هیئت داوری ۳ نفره',
   'desc': 'هر پرونده توسط سه داور متخصص بررسی می‌شود: نماینده دانشگاه، کارشناس تجهیزات بیمارستان و متخصص نظام مهندسی — نه قاضی عمومی، بلکه افرادی که مدار را می‌فهمند.',
   'checks': [
     'نماینده دانشگاه — مرجع علمی و نظارت بر فرآیند',
     'کارشناس تجهیزات پزشکی بیمارستان — داوری فنی موردی',
     'متخصص نظام مهندسی پزشکی — مرجع استاندارد و ایمنی',
     'بررسی مدارک، شنیدن توضیحات طرفین و بازبینی فیزیکی تجهیز در صورت نیاز',
   ],
   'panel_name': 'هیئت داوری پرونده DSP-1404-019',
   'panel': '''<div class="odr-seats">
  <div class="odr-seat"><span class="odr-seat__av"><svg class="ic" aria-hidden="true"><use href="#i-file-chart"/></svg></span><span class="odr-seat__t">نماینده دانشگاه آزاد</span><span class="odr-seat__d">مرجع علمی — تأیید فرآیند و مدارک</span></div>
  <div class="odr-seat"><span class="odr-seat__av"><svg class="ic" aria-hidden="true"><use href="#i-activity"/></svg></span><span class="odr-seat__t">کارشناس تجهیزات بیمارستان</span><span class="odr-seat__d">داوری فنی — بررسی عیب گزارش‌شده</span></div>
  <div class="odr-seat"><span class="odr-seat__av"><svg class="ic" aria-hidden="true"><use href="#i-shield"/></svg></span><span class="odr-seat__t">متخصص نظام مهندسی</span><span class="odr-seat__d">مرجع استاندارد — انطباق با ضوابط فنی</span></div>
</div>
<p class="mock-hint">داوران از شبکه تیک‌آبی هر منطقه و به‌صورت گردشی انتخاب می‌شوند</p>''',
   'reverse': True,
  },
  {
   'kicker': 'نتیجه نهایی', 'kicker_icon': 'i-clock',
   'title': 'صدور رای قطعی ظرف ۴۸ ساعت',
   'desc': 'رای داوری قطعی است و همان‌لحظه اجرا می‌شود: وجه آزاد شده به نفع تعمیرکار واریز می‌شود یا به حساب بیمارستان برمی‌گردد — بدون پرونده قضایی، بدون تأخیر چندماهه.',
   'checks': [
     'حداکثر ۴۸ ساعت از تشکیل پرونده تا رای قطعی',
     'آزادسازی وجه به نفع تعمیرکار در صورت احراز کیفیت کار',
     'عودت وجه به بیمارستان در صورت اثبات قصور فنی یا قطعه معیوب',
     'ثبت رای در پرونده اعتباری طرفین برای معاملات بعدی',
   ],
   'panel_name': 'رای قطعی — پرونده DSP-1404-019',
   'panel': '''<div class="odr-ruling">
  <svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>
  <span><strong>رای هیئت (نمونه):</strong> عیب مجدد ناشی از خرابی قطعه استوک فروشنده و نه خطای تعمیرکار بوده است. بدین ترتیب ۱۸٬۰۰۰٬۰۰۰ تومان وجه بلوکه‌شده به حساب بیمارستان عودت و فروشنده ملزم به تعویض قطعه با نمونه نو می‌گردد. — صادره در ۲۶ ساعت</span>
</div>
<p class="mock-hint">اجرای رای همان لحظه توسط سامانه امانی انجام می‌شود</p>''',
  },
 ],
 'tg': False,
 'cta': {
   'title': 'معامله‌ای که هرگز طرفش ضرر نمی‌کند',
   'desc': 'حساب امانی + داوری تخصصی ۴۸ ساعته = بودجه عمومی بیمارستان دیگر در میانه جدل‌های فنی بلوکه نمی‌شود.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('hospital.html', 'btn btn--dark btn--lg', 'i-activity', 'پیشخوان بیمارستان‌ها'),
   ],
 },
},

# ════════════════════════════════ M6 — ACADEMY ════════════════════════════════
{
 'file': 'academy.html',
 'no': '۶', 'module_family': 'دانش و رسانه',
 'icon': 'i-file-chart',
 'title': 'آکادمی و رسانه تخصصی مدیکال‌نت | Knowledge Base & Media',
 'desc': 'پایگاه مقالات و راهنماهای نگهداری پیشگیرانه (PM)، چک‌لیست‌های کالیبراسیون، ترویج شأن صنفی مهندسی پزشکی و اخبار تخصصی آیمد و استانداردهای روز سلامت.',
 'role': 'ویژه همه بازیگران اکوسیستم و علاقه‌مندان مهندسی پزشکی',
 'hero_title': 'آکادمی و رسانه تخصصی (Knowledge Base & Media)',
 'hero_lead': 'پلتفرمی که فقط ابزار می‌دهد و دانش نمی‌آموزد، نصفه‌است. آکادمی مدیکال‌نت مرجع تخصصی مهندسان بالینی کشور است: از چک‌لیست گام‌به‌گام کالیبراسیون تا تحلیل استانداردهای جهانی — همه به زبان فارسی و قابل استناد.',
 'stats': [
   ('i-file-chart', '۷ مقاله', 'پایه علمی داوری‌شده بین‌المللی'),
   ('i-check', 'چک‌لیست PM', 'قابل استفاده در بازرسی‌های واقعی'),
   ('i-zap', 'به‌روز', 'اخبار آیمد و استانداردهای روز'),
 ],
 'ctas': [
   ('#f-kb', 'btn btn--dark btn--lg', 'i-file-chart', 'مرور پایگاه دانش'),
   ('#f-promo', 'btn btn--light btn--lg', 'i-zap', 'رسانه و شأن صنفی'),
 ],
 'features': [
  {
   'kicker': 'پایگاه دانش', 'kicker_icon': 'i-file-chart',
   'title': 'پایگاه مقالات و راهنماهای نگهداری پیشگیرانه (PM)',
   'desc': 'مقالات کاربردی و چک‌لیست‌های گام‌به‌گام که مهندس بالینی می‌تواند فردا صبح در بازرسی واقعی از آن‌ها استفاده کند — نه مقاله‌های ترجمه‌شده‌ی کلیشه‌ای.',
   'checks': [
     'چک‌لیست‌های گام‌به‌گام کالیبراسیون تجهیزات پرتکرار بیمارستانی',
     'راهنمای کار با ابزار: مولتی‌متر، آنالایزر ایمنی الکتریکی و شیم‌تست',
     'پروتکل‌های نگهداری پیشگیرانه (PM) فصلی برای هر خانواده تجهیزات',
     'بانک خطاهای رایج و ریشه‌یابی آن‌ها بر پایه سواقع Asset Log پلتفرم',
   ],
   'panel_name': 'تازه‌های پایگاه دانش',
   'panel': '''<div class="article-grid">
  <div class="article-card"><span class="article-card__cat">چک‌لیست PM</span><p class="article-card__t">کالیبراسیون فشارسنج دیجیتال در ۹ گام استاندارد</p><p class="article-card__d">از کنترل ممبران تا تست نشتی کاف — همراه با جدول مقادیر مرجع و تلرانس مجاز.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۱۲ دقیقه مطالعه</span><span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>قابل چاپ برای بازرسی</span></div></div>
  <div class="article-card"><span class="article-card__cat article-card__cat--blue">راهنمای ابزار</span><p class="article-card__t">تست ایمنی الکتریکی تجهیزات با استاندارد IEC 62353</p><p class="article-card__d">تفاوت روش تست متد alternaive و روش direct — نمودار جریان تصمیم‌گیری برای تجهیزات کلاس CF.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۱۸ دقیقه مطالعه</span><span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>مطابق اداره کل IMED</span></div></div>
  <div class="article-card"><span class="article-card__cat article-card__cat--green">عیب‌یابی</span><p class="article-card__t">۱۰ خطای رایج پمپ‌های سرم و راه‌حل‌های فنی آن‌ها</p><p class="article-card__d">از انسداد حسگر فشار تا خرابی ولپوست — بر پایه ۱٬۲۰۰ پرونده واقعی ثبت‌شده در پلتفرم.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۱۵ دقیقه مطالعه</span><span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>مبتنی بر داده واقعی</span></div></div>
  <div class="article-card"><span class="article-card__cat">نگهداشت</span><p class="article-card__t">زمان‌بندی PM فصلی اکسیژن‌سازهای سانترال PSA</p><p class="article-card__d">تعویض زئولیت، بازرسی کمپرسور و کالیبراسیون سنسور خلأ — با چرخه‌های پیشنهادی کارخانه و تجربه بومی.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۲۲ دقیقه مطالعه</span><span><svg class="ic" aria-hidden="true"><use href="#i-check"/></svg>همراه چک‌لیست PDF</span></div></div>
</div>''',
  },
  {
   'kicker': 'رسانه تخصصی', 'kicker_icon': 'i-zap',
   'title': 'ترویج شأن صنفی مهندسی پزشکی',
   'desc': 'مهندسی بالینی در کشور هنوز در سایه است. آکادمی مدیکال‌نت روایت این حرفه را می‌سازد: فناوری‌ها، افراد و استانداردهایی که سلامت میلیون‌ها بیمار را نامرئی نگه می‌دارند.',
   'checks': [
     'معرفی فناوری‌های نوین تجهیزات پزشکی و تحلیل کاربرد بالینی آن‌ها',
     'اخبار تخصصی اداره کل تجهیزات پزشکی (IMED) و بخشنامه‌های جدید',
     'پوشش استانداردهای روز سلامت: ISO 13485، IEC 60601 و به‌روزرسانی‌ها',
     'روایت‌سازی از موفقیت‌های مهندسان بالینی بومی در مناطق مختلف کشور',
   ],
   'panel_name': 'خط رسانه — تازه‌ها',
   'panel': '''<div class="article-grid">
  <div class="article-card"><span class="article-card__cat article-card__cat--blue">اخبار IMED</span><p class="article-card__t">به‌روزرسانی ضوابط احراز صلاحیت تعمیرکاران تجهیزات ویژه</p><p class="article-card__d">مروری بر تغییرات جدید بخشنامه و تأثیر آن بر کارتابل احراز صلاحیت پلتفرم.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۷ دقیقه مطالعه</span></div></div>
  <div class="article-card"><span class="article-card__cat article-card__cat--green">فناوری</span><p class="article-card__t">نگهداشت پیش‌بینانه (PdM) با تحلیل ارتعاش و اینترنت اشیا</p><p class="article-card__d">چطور سنسورهای ارزان می‌توانستند خرابی یاتاقان سنتریفیوژ را دو هفته زودتر بگویند.</p><div class="article-card__meta"><span><svg class="ic" aria-hidden="true"><use href="#i-clock"/></svg>۱۴ دقیقه مطالعه</span></div></div>
</div>''',
   'reverse': True,
  },
 ],
 'tg': False,
 'cta': {
   'title': 'دانش فنی، پایتخت نامرئی هر بیمارستان است',
   'desc': 'آکادمی مدیکال‌نت با نظارت دانشگاه و شبکه تیک‌آبی تولید محتوا می‌کند؛ مقاله یا چک‌لیست موردنیازتان را از تیم فنی درخواست دهید.',
   'btns': [
     ('index.html#modules', 'btn btn--light btn--lg', 'i-grid', 'مشاهده سایر ماژول‌ها'),
     ('index.html', 'btn btn--dark btn--lg', 'i-arrow-right', 'بازگشت به صفحه اصلی'),
   ],
 },
},
]
