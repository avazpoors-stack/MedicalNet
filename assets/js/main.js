/*!
 * MedicalNet (مدیکال‌نت) — National Clinical Engineering & Healthcare B2B Platform
 * Interactive JavaScript & Data Visualization Engine
 * Vanilla JS · zero dependencies · strict CSP · no eval · accessible (WCAG 2.2.2 / 2.5.8)
 */
(() => {
  'use strict';

  const root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  /* ---------- Helpers & Utilities ---------- */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs = {}, parent = null) => {
    const el = document.createElementNS(SVG_NS, tag);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, String(v)));
    if (parent) parent.appendChild(el);
    return el;
  };
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const noop = () => {};
  const safe = (name, fn) => {
    try { return fn() || noop; } catch (err) { console.error('[MedicalNet] ' + name + ' failed:', err); return noop; }
  };
  const onVisible = (el, cb, threshold = 0.2) => {
    if (!el) return;
    if (!('IntersectionObserver' in window)) { cb(); return; }
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { io.disconnect(); cb(); }
    }, { threshold });
    io.observe(el);
  };
  const docTop = (el) => { let y = 0; for (let n = el; n; n = n.offsetParent) y += n.offsetTop; return y; };

  // Persian Number Formatting
  const toPersianDigits = (num) => {
    if (num === null || num === undefined) return '';
    return String(num).replace(/\d/g, (d) => '۰۱۲۳۴۵۶۷۸۹'[d]);
  };

  const formatPersianNumber = (val, decimals = 0, useComma = true) => {
    const num = Number(val);
    if (Number.isNaN(num)) return toPersianDigits(val);
    const fixed = num.toFixed(decimals);
    const parts = fixed.split('.');
    let intPart = parts[0];
    const decPart = parts[1];
    if (useComma) {
      intPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '،');
    }
    const formatted = decPart !== undefined && decimals > 0 ? `${intPart}.${decPart}` : intPart;
    return toPersianDigits(formatted);
  };

  const normalizeFarsi = (text) => {
    if (!text) return '';
    return String(text)
      .toLowerCase()
      .replace(/[\u064A\u0649]/g, 'ی')
      .replace(/[\u0643]/g, 'ک')
      .replace(/[\u0640]/g, '')
      .replace(/[\u064B-\u065F]/g, '')
      .trim();
  };

  /* ---------- 1. Header State ---------- */
  function initHeader() {
    const header = $('#site-header');
    if (!header) return noop;
    return () => header.classList.toggle('is-scrolled', window.scrollY > 24);
  }

  /* ---------- 2. Nav: Sliding Hover Pill + Active Section ---------- */
  function initNav() {
    const nav = $('.nav');
    if (!nav) return;
    const links = $$('.nav__link', nav);
    const movePill = (link) => {
      nav.style.setProperty('--pill-x', link.offsetLeft + 'px');
      nav.style.setProperty('--pill-w', link.offsetWidth + 'px');
      nav.classList.add('has-pill');
    };
    const restPill = () => {
      const active = $('.nav__link.is-active', nav);
      if (active) movePill(active); else nav.classList.remove('has-pill');
    };
    links.forEach((link) => {
      link.addEventListener('mouseenter', () => movePill(link));
      link.addEventListener('focus', () => movePill(link));
      link.addEventListener('blur', restPill);
    });
    nav.addEventListener('mouseleave', restPill);

    if (!('IntersectionObserver' in window)) return;
    const byId = new Map(links.map((l) => [l.getAttribute('href').slice(1), l]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const link = byId.get(entry.target.id);
        if (!link) return;
        if (entry.isIntersecting) links.forEach((l) => l.classList.toggle('is-active', l === link));
        else link.classList.remove('is-active');
      });
      if (!nav.matches(':hover')) restPill();
    }, { rootMargin: '-45% 0px -50% 0px' });
    byId.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }

  /* ---------- 3. Mobile Menu ---------- */
  function initMobileMenu() {
    const btn = $('.nav-toggle');
    const menu = $('#mobile-menu');
    if (!btn || !menu) return;
    const icon = $('use', btn);
    const setOpen = (open) => {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'بستن منو' : 'باز کردن منو');
      if (icon) icon.setAttribute('href', open ? '#i-close' : '#i-menu');
      menu.hidden = !open;
    };
    btn.addEventListener('click', () => setOpen(menu.hidden));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menu.hidden) { setOpen(false); btn.focus(); }
    });
    document.addEventListener('click', (e) => {
      if (!menu.hidden && !e.target.closest('.site-header')) setOpen(false);
    });
    const desktop = window.matchMedia('(min-width: 901px)');
    const onChange = (e) => { if (e.matches) setOpen(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onChange);
  }

  /* ---------- 4. Sparkle Particles Inside CTA Buttons ---------- */
  function initSparkles() {
    if (reduceMotion) return;
    $$('[data-sparkle]').forEach((btn) => {
      const count = btn.classList.contains('btn--lg') ? 12 : 8;
      for (let i = 0; i < count; i += 1) {
        const s = document.createElement('span');
        s.className = 'spark';
        s.setAttribute('aria-hidden', 'true');
        s.style.left = (6 + Math.random() * 88).toFixed(1) + '%';
        s.style.top = (22 + Math.random() * 68).toFixed(1) + '%';
        s.style.setProperty('--d', (2.2 + Math.random() * 2.6).toFixed(2) + 's');
        s.style.setProperty('--delay', (-Math.random() * 4).toFixed(2) + 's');
        s.style.setProperty('--dx', ((Math.random() - 0.5) * 16).toFixed(1) + 'px');
        btn.appendChild(s);
      }
    });
  }

  /* ---------- 5. Reveal on Scroll ---------- */
  function initReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    const probe = new IntersectionObserver((entries) => {
      const vh = window.innerHeight;
      entries.forEach((e) => {
        const el = e.target;
        probe.unobserve(el);
        if (e.boundingClientRect.top < vh * 0.95) return;
        const siblings = el.parentElement ? Array.from(el.parentElement.children).filter((c) => c.hasAttribute('data-reveal')) : [];
        const idx = siblings.indexOf(el);
        if (idx > 0) el.style.setProperty('--reveal-delay', (idx * 0.09).toFixed(2) + 's');
        el.classList.add('reveal-init');
        io.observe(el);
      });
    });
    $$('[data-reveal]').forEach((el) => probe.observe(el));
  }

  /* ---------- 6. Scroll-Linked Scale ---------- */
  function initScrollScale() {
    if (reduceMotion) return noop;
    const els = $$('[data-scroll-scale]');
    const items = els.map((el) => ({ el, top: docTop(el), h: el.offsetHeight }));
    els.forEach((el) => el.style.setProperty('--from', el.dataset.scrollScale));
    const measure = () => items.forEach((it) => { it.top = docTop(it.el); it.h = it.el.offsetHeight; });
    window.addEventListener('resize', measure, { passive: true });
    window.addEventListener('load', measure);
    return (vh) => {
      const sy = window.scrollY;
      items.forEach((it) => {
        const top = it.top - sy;
        if (top > vh || top + it.h < 0) return;
        const p = clamp(1 - (top - vh * 0.18) / (vh * 0.72), 0, 1);
        it.el.style.setProperty('--scroll-p', p.toFixed(3));
      });
    };
  }

  /* ---------- 7. Parallax Avatars ---------- */
  function initParallax() {
    const section = $('.stories');
    const tiles = $$('.tile[data-speed]');
    if (!section || !tiles.length || reduceMotion) return noop;
    return (vh) => {
      const r = section.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      const offset = r.top + r.height / 2 - vh / 2;
      tiles.forEach((t) => t.style.setProperty('--py', (-offset * parseFloat(t.dataset.speed)).toFixed(1) + 'px'));
    };
  }

  function initScrollLoop(handlers) {
    let ticking = false;
    const run = () => {
      ticking = false;
      const vh = window.innerHeight;
      handlers.forEach((h) => h(vh));
    };
    const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(run); } };
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request, { passive: true });
    run();
  }

  /* ---------- 8. Dashboard Dynamic Scaling ---------- */
  function initDashFit() {
    const fit = $('#dash-fit');
    const dash = $('#dash');
    if (!fit || !dash) return;
    const DESIGN_W = 1072;
    let lastW = -1;
    const apply = () => {
      const w = fit.clientWidth;
      if (w === lastW || w === 0) return;
      lastW = w;
      const s = Math.min(1, w / DESIGN_W);
      dash.style.setProperty('--fit', s.toFixed(4));
      // Measure actual rendered scrollHeight to prevent clipping CMMS work orders
      const fullH = Math.max(560, dash.scrollHeight);
      fit.style.setProperty('--dash-h', Math.round(fullH * s) + 'px');
      // Always allow interactive search & clicks
      dash.inert = false;
      fit.removeAttribute('role');
      fit.removeAttribute('aria-label');
    };
    apply();
    if ('ResizeObserver' in window) new ResizeObserver(apply).observe(fit);
    else window.addEventListener('resize', apply, { passive: true });
  }

  /* ---------- 9. Dashboard Sidebar Navigation ---------- */
  function initSidebar() {
    $$('[data-side-group]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        const sub = btn.nextElementSibling;
        if (sub) sub.hidden = open;
      });
    });
    const items = $$('[data-side-item]');
    items.forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      items.forEach((i) => { i.classList.remove('is-current'); i.removeAttribute('aria-current'); });
      a.classList.add('is-current');
      a.setAttribute('aria-current', 'page');
    }));
  }

  /* ---------- 10. Rotating Search Placeholder Hints ---------- */
  function initSearch() {
    const input = $('#dash-search');
    if (!input || reduceMotion) return;
    const tips = [
      'جست‌وجوی دستگاه اکسیژن‌ساز سانترال PSA (بخش ICU)...',
      'استعلام قطعه پدال هیدرولیک تخت جراحی با استاندارد ضدآب IPX8...',
      'پیگیری وضعیت تصویب بودجه و کارپردازی فلومترهای دیواری...',
      'سفارش سریع کاف، پوآر و گیج فشارسنج بالینی استاندارد...',
      'استعلام سوابق کالیبراسیون و آزمون ایمنی الکتریکی تخت بستری...'
    ];
    let i = 0;
    window.setInterval(() => {
      if (document.hidden || document.activeElement === input || input.value) return;
      input.classList.add('is-swapping');
      window.setTimeout(() => {
        i = (i + 1) % tips.length;
        input.placeholder = tips[i];
        input.classList.remove('is-swapping');
      }, 300);
    }, 4200);
  }

  /* ---------- 11. Interactive Hospital CMMS Work Order Manager ---------- */
  function initWorkOrders() {
    const container = $('.dash-workorders');
    const input = $('#dash-search');
    const grid = $('.wo-grid', container);
    if (!container || !grid) return;

    const cards = $$('.wo-card', grid);
    const countBadge = $('.badge-count', container);

    // Build Urgency Classification Map
    const getUrgency = (card) => {
      const badge = $('.wo-badge', card);
      const txt = badge ? badge.textContent : '';
      if (txt.includes('بحرانی')) return 'critical';
      if (txt.includes('فوری')) return 'urgent';
      if (txt.includes('ایمنی')) return 'safety';
      return 'medium';
    };

    // Inject Toolbar with Urgency Filter Tabs
    const toolbar = document.createElement('div');
    toolbar.className = 'wo-toolbar';
    toolbar.setAttribute('role', 'region');
    toolbar.setAttribute('aria-label', 'فیلتر فوریت بالینی دستورکارها');

    const tabsWrap = document.createElement('div');
    tabsWrap.className = 'wo-tabs';

    const categories = [
      { id: 'all', label: 'همه دستورکارها' },
      { id: 'critical', label: 'بحرانی (ICU)' },
      { id: 'urgent', label: 'فوری (جراحی)' },
      { id: 'safety', label: 'ایمنی بیمار' },
      { id: 'medium', label: 'متوسط و عادی' }
    ];

    let activeCategory = 'all';

    categories.forEach((cat) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'wo-tab-btn' + (cat.id === 'all' ? ' is-active' : '');
      btn.dataset.filter = cat.id;
      btn.textContent = cat.label;
      btn.setAttribute('aria-pressed', String(cat.id === 'all'));
      btn.addEventListener('click', () => {
        activeCategory = cat.id;
        $$('.wo-tab-btn', tabsWrap).forEach((b) => {
          const on = b === btn;
          b.classList.toggle('is-active', on);
          b.setAttribute('aria-pressed', String(on));
        });
        applyFilter();
      });
      tabsWrap.appendChild(btn);
    });

    toolbar.appendChild(tabsWrap);

    // Empty state container
    const emptyState = document.createElement('div');
    emptyState.className = 'wo-empty';
    emptyState.hidden = true;
    emptyState.setAttribute('role', 'status');
    emptyState.setAttribute('aria-live', 'polite');

    const emptyIcon = document.createElement('div');
    emptyIcon.className = 'wo-empty__icon';
    emptyIcon.textContent = '🔎';

    const emptyTitle = document.createElement('h4');
    emptyTitle.textContent = 'موردی با مشخصات جست‌وجو شده یافت نشد';

    const emptyText = document.createElement('p');
    emptyText.textContent = 'می‌توانید عبارت جست‌وجو را بازنشانی کنید یا شناسه پرونده دیگری مانند WO-2026، اکسیژن‌ساز، پدال یا ICU را جست‌وجو نمایید.';

    const emptyReset = document.createElement('button');
    emptyReset.type = 'button';
    emptyReset.className = 'wo-empty__reset';
    emptyReset.textContent = 'پاک کردن فیلترها و مشاهده همه';
    emptyReset.addEventListener('click', () => {
      if (input) input.value = '';
      activeCategory = 'all';
      $$('.wo-tab-btn', tabsWrap).forEach((b) => {
        const on = b.dataset.filter === 'all';
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', String(on));
      });
      applyFilter();
      if (input) input.focus();
    });

    emptyState.append(emptyIcon, emptyTitle, emptyText, emptyReset);

    // Insert toolbar and empty state into DOM
    const head = $('.card__head', container);
    if (head && head.nextSibling) {
      container.insertBefore(toolbar, head.nextSibling);
    } else {
      container.prepend(toolbar);
    }
    grid.appendChild(emptyState);

    // Add inspection hint & accessibility to cards
    cards.forEach((card) => {
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-haspopup', 'dialog');
      card.setAttribute('title', 'کلیک برای مشاهده جزئیات پرونده فنی و بالینی');

      const hint = document.createElement('div');
      hint.className = 'wo-card__action-hint';
      hint.textContent = 'مشاهده پرونده کامل ←';
      card.appendChild(hint);

      // Open inspection modal on click or Enter
      const triggerModal = () => openInspectionModal(card);
      card.addEventListener('click', triggerModal);
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerModal();
        }
      });
    });

    // Core Search & Filter Routine
    const applyFilter = () => {
      const q = normalizeFarsi(input ? input.value : '');
      let visibleCount = 0;

      cards.forEach((card) => {
        const cardText = normalizeFarsi(card.textContent);
        const matchesQuery = !q || cardText.includes(q);
        const cardUrgency = getUrgency(card);
        const matchesCategory = activeCategory === 'all' || cardUrgency === activeCategory;

        const isVisible = matchesQuery && matchesCategory;
        card.classList.toggle('is-hidden', !isVisible);
        if (isVisible) visibleCount += 1;
      });

      emptyState.hidden = visibleCount > 0;

      if (countBadge) {
        countBadge.textContent = `${toPersianDigits(visibleCount)} مورد نیازمند نظارت`;
      }
    };

    if (input) {
      input.addEventListener('input', applyFilter);
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }

    // Modal Builder
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    modalOverlay.setAttribute('role', 'dialog');
    modalOverlay.setAttribute('aria-modal', 'true');
    modalOverlay.setAttribute('aria-labelledby', 'modal-wo-title');
    modalOverlay.hidden = true;

    const modalDialog = document.createElement('div');
    modalDialog.className = 'modal-dialog';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'modal-close-btn';
    closeBtn.setAttribute('aria-label', 'بستن پنجره جزئیات');
    closeBtn.textContent = '✕';

    const modalHeader = document.createElement('div');
    modalHeader.className = 'modal-header';

    const modalBody = document.createElement('div');
    modalBody.className = 'modal-body';

    const modalFooter = document.createElement('div');
    modalFooter.className = 'modal-footer';

    const closeFooterBtn = document.createElement('button');
    closeFooterBtn.type = 'button';
    closeFooterBtn.className = 'btn btn--light btn--sm';
    closeFooterBtn.textContent = 'بستن پنجره';

    const printBtn = document.createElement('button');
    printBtn.type = 'button';
    printBtn.className = 'btn btn--dark btn--sm';
    printBtn.textContent = 'صدور گواهی پذیرش بالینی';
    printBtn.addEventListener('click', () => window.print());

    modalFooter.append(printBtn, closeFooterBtn);
    modalDialog.append(closeBtn, modalHeader, modalBody, modalFooter);
    modalOverlay.appendChild(modalDialog);
    document.body.appendChild(modalOverlay);

    let lastFocusedCard = null;

    const closeModal = () => {
      modalOverlay.classList.remove('is-open');
      modalOverlay.hidden = true;
      if (lastFocusedCard) {
        lastFocusedCard.focus();
        lastFocusedCard = null;
      }
    };

    closeBtn.addEventListener('click', closeModal);
    closeFooterBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !modalOverlay.hidden) closeModal();
    });

    const openInspectionModal = (card) => {
      lastFocusedCard = card;
      const idEl = $('.wo-card__id', card);
      const badgeEl = $('.wo-badge', card);
      const titleEl = $('.wo-card__title', card);
      const metaEl = $('.wo-card__meta', card);
      const defectEl = $('.wo-card__defect', card);
      const partEl = $('.wo-card__part', card);
      const statusEl = $('.wo-card__status', card);
      const etaEl = $('.wo-card__eta', card);
      const notesEl = $('.wo-card__notes', card);

      // Populate Header
      while (modalHeader.firstChild) modalHeader.removeChild(modalHeader.firstChild);
      const hId = document.createElement('div');
      hId.className = 'wo-card__id';
      hId.textContent = idEl ? idEl.textContent : '';
      if (badgeEl) {
        const b = badgeEl.cloneNode(true);
        b.style.display = 'inline-block';
        b.style.marginRight = '8px';
        hId.appendChild(b);
      }
      const hTitle = document.createElement('h3');
      hTitle.id = 'modal-wo-title';
      hTitle.className = 'modal-title';
      hTitle.textContent = titleEl ? titleEl.textContent : '';
      modalHeader.append(hId, hTitle);

      // Populate Body
      while (modalBody.firstChild) modalBody.removeChild(modalBody.firstChild);

      const makeRow = (label, content) => {
        const row = document.createElement('div');
        row.className = 'modal-row';
        const strong = document.createElement('strong');
        strong.textContent = label;
        const div = document.createElement('div');
        div.textContent = content;
        row.append(strong, div);
        return row;
      };

      if (metaEl) modalBody.appendChild(makeRow('موقعیت بالینی و مهندس ناظر:', metaEl.textContent.replace(/\s+/g, ' ').trim()));
      if (defectEl) modalBody.appendChild(makeRow('گزارش عیب‌یابی فنی و نشانه‌های بالینی:', defectEl.textContent.replace(/^شرح نقص:\s*/, '')));
      if (partEl) modalBody.appendChild(makeRow('قطعه یدکی استاندارد یا خدمت تخصصی مورد نیاز:', partEl.textContent.replace(/^قطعه یا خدمت موردنیاز:\s*/, '')));
      if (statusEl || etaEl) {
        const stText = (statusEl ? statusEl.textContent : '') + (etaEl ? ' | ' + etaEl.textContent : '');
        modalBody.appendChild(makeRow('گردش کار و وضعیت دیسپچینگ:', stText.replace(/\s+/g, ' ').trim()));
      }
      if (notesEl) modalBody.appendChild(makeRow('سوابق تاریخی و مقایسه با چرخه سنتی:', notesEl.textContent));

      modalOverlay.hidden = false;
      requestAnimationFrame(() => {
        modalOverlay.classList.add('is-open');
        closeBtn.focus();
      });
    };
  }

  /* ---------- 12. Dynamic SVG Chart Engine ---------- */
  const BASE_CUR = [25.0, 24.6, 24.2, 19.8, 22.4, 24.8, 22.9, 23.0, 28.9, 25.6, 26.2, 16.8, 17.2, 17.6, 12.6, 12.2, 10.1, 16.9, 15.4];
  const BASE_PREV = [13.4, 16.8, 18.6, 14.7, 17.4, 19.8, 17.3, 17.6, 22.6, 19.9, 18.4, 12.6, 13.6, 12.5, 9.6, 9.1, 6.6, 11.6, 10.6];
  const METRICS = {
    traffic: { label: 'شاخص تاب‌آوری و Uptime (%)', k: 1, unit: '٪' },
    pageviews: { label: 'سفارشات قطعات B2B', k: 1.9, unit: ' عدد' },
    sessions: { label: 'زمان پاسخ‌دهی گره‌ها (ساعت)', k: 1.32, unit: ' ساعت' }
  };
  const DAYS = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر'];

  function initChart() {
    const host = $('#traffic-chart');
    const tip = $('#chart-tip');
    if (!host || !tip) return;

    const W = host.clientWidth || 652;
    const H = host.clientHeight || 196;
    const PAD = { l: 34, r: 4, t: 8, b: 26 };
    const plotW = W - PAD.l - PAD.r;
    let metric = 'traffic';
    let cur = BASE_CUR.slice();
    let prev = BASE_PREV.slice();
    let yMax = 30;
    let liveTimer = null;
    const visible = { cur: true, prev: true };

    const chartSvg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, 'aria-hidden': 'true', focusable: 'false' });
    host.insertBefore(chartSvg, tip);
    const defs = svgEl('defs', {}, chartSvg);
    const grad = svgEl('linearGradient', { id: 'area-grad', x1: 0, y1: 0, x2: 0, y2: 1 }, defs);
    svgEl('stop', { offset: '0%', 'stop-color': '#5b8def', 'stop-opacity': 0.3 }, grad);
    svgEl('stop', { offset: '100%', 'stop-color': '#5b8def', 'stop-opacity': 0.02 }, grad);
    const clip = svgEl('clipPath', { id: 'chart-clip' }, defs);
    const clipRect = svgEl('rect', { x: 0, y: 0, width: reduceMotion ? W : 0, height: H }, clip);
    const axes = svgEl('g', {}, chartSvg);
    const plot = svgEl('g', { 'clip-path': 'url(#chart-clip)' }, chartSvg);
    const area = svgEl('path', { class: 'area', fill: 'url(#area-grad)' }, plot);
    const linePrev = svgEl('path', { class: 'line line--prev' }, plot);
    const lineCur = svgEl('path', { class: 'line line--cur' }, plot);
    const cursor = svgEl('line', { class: 'cursor', y1: PAD.t, y2: H - PAD.b, x1: 0, x2: 0 }, chartSvg);
    const dotPrev = svgEl('circle', { class: 'cursor-dot', r: 3.5, cx: 0, cy: 0 }, chartSvg);
    const dotCur = svgEl('circle', { class: 'cursor-dot', r: 3.5, cx: 0, cy: 0 }, chartSvg);
    const hit = svgEl('rect', { x: PAD.l, y: 0, width: plotW, height: H, fill: 'transparent' }, chartSvg);

    const k = () => METRICS[metric].k;
    const x = (i, n) => PAD.l + (i / (n - 1)) * plotW;
    const y = (v) => PAD.t + (1 - v / yMax) * (H - PAD.t - PAD.b);
    const toPts = (arr) => arr.map((v, i) => [x(i, arr.length), y(v * k())]);
    const smooth = (pts) => {
      let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`;
      for (let i = 0; i < pts.length - 1; i += 1) {
        const p0 = pts[i - 1] || pts[i];
        const p1 = pts[i];
        const p2 = pts[i + 1];
        const p3 = pts[i + 2] || p2;
        const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
        const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
        d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
      }
      return d;
    };

    function drawAxes() {
      while (axes.firstChild) axes.removeChild(axes.firstChild);
      const maxVal = Math.max(...cur, ...prev) * k();
      const step = Math.ceil(maxVal / 3 / 5) * 5;
      yMax = step * 3;
      for (let i = 0; i <= 3; i += 1) {
        const v = step * i;
        const t = svgEl('text', { x: 0, y: (y(v) + 3.5).toFixed(1) }, axes);
        t.textContent = v === 0 ? '0' : v + 'K';
      }
      DAYS.forEach((d, j) => {
        const t = svgEl('text', { x: (PAD.l + ((j + 0.5) / 7) * plotW).toFixed(1), y: H - 6, 'text-anchor': 'middle' }, axes);
        t.textContent = d;
      });
    }

    function drawLines() {
      const pc = toPts(cur);
      const dc = smooth(pc);
      lineCur.setAttribute('d', dc);
      linePrev.setAttribute('d', smooth(toPts(prev)));
      area.setAttribute('d', `${dc} L${pc[pc.length - 1][0].toFixed(1)},${H - PAD.b} L${pc[0][0].toFixed(1)},${H - PAD.b} Z`);
      lineCur.classList.toggle('is-off', !visible.cur);
      area.classList.toggle('is-off', !visible.cur);
      linePrev.classList.toggle('is-off', !visible.prev);
    }

    function sweep() {
      if (reduceMotion) { clipRect.setAttribute('width', W); return; }
      const start = performance.now();
      const dur = 1500;
      clipRect.setAttribute('width', 0);
      const step = (now) => {
        const t = clamp((now - start) / dur, 0, 1);
        clipRect.setAttribute('width', (W * (1 - Math.pow(1 - t, 3))).toFixed(1));
        if (t < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }

    function render(withSweep) {
      drawAxes();
      drawLines();
      if (withSweep) sweep();
    }

    /* Tooltip */
    const line = (txt) => { const d = document.createElement('div'); d.textContent = txt; return d; };
    hit.addEventListener('pointermove', (e) => {
      const rect = chartSvg.getBoundingClientRect();
      const px = ((e.clientX - rect.left) / rect.width) * W;
      const n = cur.length;
      const i = clamp(Math.round(((px - PAD.l) / plotW) * (n - 1)), 0, n - 1);
      const xx = x(i, n);
      cursor.setAttribute('x1', xx); cursor.setAttribute('x2', xx);
      dotCur.setAttribute('cx', xx); dotCur.setAttribute('cy', y(cur[i] * k()));
      dotPrev.setAttribute('cx', xx); dotPrev.setAttribute('cy', y(prev[i] * k()));
      dotCur.classList.toggle('is-off', !visible.cur);
      dotPrev.classList.toggle('is-off', !visible.prev);
      host.classList.add('is-hover');
      while (tip.firstChild) tip.removeChild(tip.firstChild);
      const title = document.createElement('b');
      title.textContent = DAYS[clamp(Math.floor((i / (n - 1)) * 7), 0, 6)];

      const curVal = (cur[i] * k()).toFixed(1);
      const prevVal = (prev[i] * k()).toFixed(1);
      const unit = METRICS[metric].unit || '';

      tip.append(
        title,
        line(`دوره جاری (مدیکال‌نت): ${formatPersianNumber(curVal, 1)} ${unit}`),
        line(`دوره گذشته (سنتی): ${formatPersianNumber(prevVal, 1)} ${unit}`)
      );
      tip.hidden = false;
      let tx = xx + 12;
      if (tx + tip.offsetWidth > W) tx = xx - 12 - tip.offsetWidth;
      tip.style.setProperty('--tx', tx.toFixed(0) + 'px');
      tip.style.setProperty('--ty', Math.max(0, y(Math.max(cur[i], prev[i]) * k()) - 62).toFixed(0) + 'px');
    });
    hit.addEventListener('pointerleave', () => { host.classList.remove('is-hover'); tip.hidden = true; });

    /* Metric Dropdown */
    const metricBtn = $('#metric-btn');
    const metricMenu = $('#metric-menu');
    const metricLabel = $('#metric-label');
    if (metricBtn && metricMenu && metricLabel) {
      const closeMenu = () => { metricMenu.hidden = true; metricBtn.setAttribute('aria-expanded', 'false'); };
      metricBtn.addEventListener('click', () => {
        const open = metricMenu.hidden;
        metricMenu.hidden = !open;
        metricBtn.setAttribute('aria-expanded', String(open));
      });
      metricMenu.addEventListener('click', (e) => {
        const b = e.target.closest('[data-metric]');
        if (!b) return;
        metric = b.dataset.metric;
        metricLabel.textContent = b.textContent.trim();
        $$('[data-metric]', metricMenu).forEach((m) => m.setAttribute('aria-current', String(m === b)));
        closeMenu();
        render(true);
        metricBtn.focus();
      });
      metricMenu.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeMenu(); metricBtn.focus(); } });
      document.addEventListener('click', (e) => { if (!metricMenu.hidden && !e.target.closest('.metric-select')) closeMenu(); });
    }

    /* Legend Toggles */
    $$('.legend-item').forEach((b) => b.addEventListener('click', () => {
      const s = b.dataset.series;
      visible[s] = !visible[s];
      b.setAttribute('aria-pressed', String(visible[s]));
      b.style.opacity = visible[s] ? '1' : '0.45';
      drawLines();
    }));

    /* Refresh Simulation with Spin */
    const refresh = $('#chart-refresh');
    if (refresh) refresh.addEventListener('click', () => {
      const jitter = (v) => +(v * (0.85 + Math.random() * 0.3)).toFixed(1);
      cur = BASE_CUR.map(jitter);
      prev = BASE_PREV.map(jitter);
      refresh.classList.remove('is-spinning');
      void refresh.offsetWidth;
      refresh.classList.add('is-spinning');
      render(true);
    });

    /* Live Mode Simulation */
    const liveBtn = $('#chart-live');
    if (liveBtn) liveBtn.addEventListener('click', () => {
      const on = liveBtn.getAttribute('aria-pressed') !== 'true';
      liveBtn.setAttribute('aria-pressed', String(on));
      liveBtn.classList.toggle('is-live', on);
      if (on) {
        liveTimer = window.setInterval(() => {
          if (document.hidden) return;
          const nc = clamp(cur[cur.length - 1] + (Math.random() - 0.45) * 5, 6, 29);
          const np = clamp(prev[prev.length - 1] + (Math.random() - 0.5) * 4, 4, 24);
          cur = cur.slice(1).concat(+nc.toFixed(1));
          prev = prev.slice(1).concat(+np.toFixed(1));
          render(false);
        }, 2200);
      } else {
        window.clearInterval(liveTimer);
        liveTimer = null;
      }
    });

    render(false);
    onVisible(host, sweep, 0.3);
  }

  /* ---------- 13. Donut Chart ---------- */
  function initDonut() {
    const c = $('#donut-value');
    if (!c) return;
    const C = 2 * Math.PI * 44;
    onVisible(c, () => { c.style.strokeDasharray = (C * 0.662).toFixed(1) + ' ' + C.toFixed(1); }, 0.3);
  }

  /* ---------- 14. Bars + Tabs ---------- */
  const fillBars = (ctx) => $$('i[data-w]', ctx).forEach((i) => i.style.setProperty('--w', i.dataset.w + '%'));
  const resetBars = (ctx) => $$('i[data-w]', ctx).forEach((i) => i.style.setProperty('--w', '0%'));

  function initBars() {
    $$('[data-bars]').forEach((list) => {
      const panel = list.closest('.tab-panel');
      if (panel && panel.hidden) return;
      onVisible(list, () => fillBars(list), 0.3);
    });
  }

  function initTabs() {
    $$('[data-tabs]').forEach((list) => {
      const tabs = $$('[role="tab"]', list);
      const card = list.closest('.card');
      const title = card ? $('#geo-title', card) : null;
      const select = (tab, focus) => {
        tabs.forEach((t) => {
          const on = t === tab;
          t.setAttribute('aria-selected', String(on));
          t.tabIndex = on ? 0 : -1;
          const panel = document.getElementById(t.getAttribute('aria-controls'));
          if (!panel) return;
          panel.hidden = !on;
          if (on) {
            resetBars(panel);
            requestAnimationFrame(() => requestAnimationFrame(() => fillBars(panel)));
          }
        });
        if (title) title.textContent = tab.textContent;
        if (focus) tab.focus();
      };
      tabs.forEach((t, i) => {
        t.addEventListener('click', () => select(t, false));
        t.addEventListener('keydown', (e) => {
          const map = { ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i - 1 + tabs.length) % tabs.length, Home: 0, End: tabs.length - 1 };
          if (e.key in map) { e.preventDefault(); select(tabs[map[e.key]], true); }
        });
      });
    });
  }

  /* ---------- 15. Regional Nodes Explorer & Sidebar Dispatch Sync ---------- */
  function initRegionalNodes() {
    const nodesSection = $('#regional-nodes');
    if (!nodesSection) return;
    const cards = $$('.node-card', nodesSection);

    // Dynamic focus & spotlight on click/hover
    cards.forEach((card) => {
      card.tabIndex = 0;
      card.setAttribute('role', 'article');
      card.addEventListener('mouseenter', () => {
        cards.forEach((c) => c.classList.remove('is-active'));
        card.classList.add('is-active');
      });
      card.addEventListener('click', () => {
        cards.forEach((c) => c.classList.remove('is-spotlight'));
        card.classList.add('is-spotlight');
        window.setTimeout(() => card.classList.remove('is-spotlight'), 2500);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          cards.forEach((c) => c.classList.remove('is-active', 'is-spotlight'));
          card.classList.add('is-active', 'is-spotlight');
        }
      });
    });

    // Sidebar Node Rows -> Spotlight in Regional Section
    const sideMap = {
      'تهران': 'NODE-THR',
      'اصفهان': 'NODE-ISF',
      'فارس': 'NODE-FRS',
      'خراسان': 'NODE-KHR'
    };

    $$('.side-node-row').forEach((row) => {
      row.setAttribute('role', 'button');
      row.tabIndex = 0;
      row.setAttribute('title', 'مشاهده جزئیات قطب و اعزام نیرو در نقشه ملی');

      const trigger = () => {
        const text = row.textContent;
        const key = Object.keys(sideMap).find((k) => text.includes(k));
        if (!key) return;
        const targetCode = sideMap[key];
        const targetCard = cards.find((c) => {
          const codeEl = $('.node-card__code', c);
          return codeEl && codeEl.textContent.includes(targetCode);
        });

        if (targetCard) {
          targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          cards.forEach((c) => c.classList.remove('is-active', 'is-spotlight'));
          targetCard.classList.add('is-active', 'is-spotlight');
          targetCard.focus();
        }
      };

      row.addEventListener('click', trigger);
      row.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          trigger();
        }
      });
    });
  }

  /* ---------- 16. Clinical Anomaly Alerts Severity Filter ---------- */
  function initAlerts() {
    const section = $('#monitoring');
    const alertsGrid = $('.alerts-grid', section);
    if (!section || !alertsGrid) return;

    const alertCards = $$('.alert-card', alertsGrid);
    if (!alertCards.length) return;

    // Build Severity Filter Toolbar
    const toolbar = document.createElement('div');
    toolbar.className = 'alert-toolbar';
    toolbar.setAttribute('role', 'region');
    toolbar.setAttribute('aria-label', 'فیلتر هشدارهای بالینی');

    const filters = [
      { id: 'all', label: 'همه هشدارها (۶)', cls: '' },
      { id: 'critical', label: 'مخاطره بحرانی (۱)', cls: 'alert-chip--critical' },
      { id: 'urgent', label: 'فوری و ایمنی بالینی (۲)', cls: 'alert-chip--urgent' },
      { id: 'warning', label: 'هشدار عملکردی و نشت (۲)', cls: 'alert-chip--warning' },
      { id: 'compliance', label: 'سنجه اعتباربخشی (۱)', cls: 'alert-chip--compliance' }
    ];

    filters.forEach((f) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = `alert-chip ${f.cls}` + (f.id === 'all' ? ' is-active' : '');
      chip.dataset.severity = f.id;
      chip.textContent = f.label;
      chip.setAttribute('aria-pressed', String(f.id === 'all'));

      chip.addEventListener('click', () => {
        $$('.alert-chip', toolbar).forEach((c) => {
          const on = c === chip;
          c.classList.toggle('is-active', on);
          c.setAttribute('aria-pressed', String(on));
        });

        alertCards.forEach((card) => {
          let match = false;
          if (f.id === 'all') {
            match = true;
          } else if (f.id === 'critical') {
            match = card.classList.contains('alert-card--critical');
          } else if (f.id === 'urgent') {
            match = card.classList.contains('alert-card--safety') || card.classList.contains('alert-card--surgical');
          } else if (f.id === 'warning') {
            match = card.classList.contains('alert-card--drift') || card.classList.contains('alert-card--facility');
          } else if (f.id === 'compliance') {
            match = card.classList.contains('alert-card--compliance');
          }
          card.classList.toggle('is-hidden', !match);
        });
      });

      toolbar.appendChild(chip);
    });

    alertsGrid.parentElement.insertBefore(toolbar, alertsGrid);
  }

  /* ---------- 17. Animated Number Count-Up (Persian Digits & Easing) ---------- */
  function initCounters() {
    if (reduceMotion) return;
    const vh = window.innerHeight;
    const countEls = $$('[data-count]');

    countEls.forEach((el) => {
      const target = parseFloat(el.dataset.count);
      const dec = parseInt(el.dataset.decimals || '0', 10);
      if (Number.isNaN(target)) return;

      // Check if already on screen at load time
      const initialTop = el.getBoundingClientRect().top;
      if (initialTop < vh) {
        el.textContent = formatPersianNumber(target, dec, true);
        return;
      }

      el.textContent = formatPersianNumber(0, dec, true);
      onVisible(el, () => {
        const start = performance.now();
        const duration = 1400;
        const step = (now) => {
          const p = clamp((now - start) / duration, 0, 1);
          // Ease-Out Quart
          const ease = 1 - Math.pow(1 - p, 4);
          const currentVal = target * ease;
          el.textContent = formatPersianNumber(currentVal, dec, true);
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = formatPersianNumber(target, dec, true);
        };
        requestAnimationFrame(step);
      }, 0.3);
    });
  }

  /* ---------- 18. Testimonials Marquee (Seamless Loop + WCAG 2.2.2 Control) ---------- */
  function initMarquee() {
    const wall = $('.wall');
    if (!wall) return;
    const toggle = $('#wall-toggle');
    if (reduceMotion) { if (toggle) toggle.hidden = true; return; }

    const cols = $$('[data-marquee]', wall);
    cols.forEach((col) => {
      const track = $('.wall__track', col);
      if (!track) return;
      Array.from(track.children).forEach((card) => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        track.appendChild(clone);
      });
      col.style.setProperty('--dur', (parseFloat(col.dataset.duration) || 40) + 's');
      col.classList.add('is-looping');
    });

    if (toggle) {
      const toggleMarquee = () => {
        const paused = wall.classList.toggle('is-paused');
        toggle.setAttribute('aria-pressed', String(paused));
        toggle.setAttribute('aria-label', paused ? 'پخش مجدد حرکت متحرک تجارب' : 'توقف حرکت متحرک تجارب');
        const span = $('span', toggle);
        if (span) span.textContent = paused ? 'پخش حرکت' : 'توقف حرکت';
        const use = $('use', toggle);
        if (use) use.setAttribute('href', paused ? '#i-play' : '#i-pause');
      };

      toggle.addEventListener('click', toggleMarquee);
      toggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleMarquee();
        }
      });
    }
  }

  /* ---------- 19. Footer Year ---------- */
  function initYear() {
    const y = $('#year');
    if (y) y.textContent = toPersianDigits(new Date().getFullYear());
  }

  /* ---------- Boot Orchestration ---------- */
  function init() {
    safe('sparkles', initSparkles);
    safe('nav', initNav);
    safe('mobileMenu', initMobileMenu);
    safe('reveal', initReveal);
    safe('dashFit', initDashFit);
    safe('sidebar', initSidebar);
    safe('search', initSearch);
    safe('workOrders', initWorkOrders);
    safe('chart', initChart);
    safe('donut', initDonut);
    safe('tabs', initTabs);
    safe('bars', initBars);
    safe('regionalNodes', initRegionalNodes);
    safe('alerts', initAlerts);
    safe('counters', initCounters);
    safe('marquee', initMarquee);
    safe('year', initYear);
    const handlers = [safe('header', initHeader), safe('scrollScale', initScrollScale), safe('parallax', initParallax)];
    safe('scrollLoop', () => initScrollLoop(handlers));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
