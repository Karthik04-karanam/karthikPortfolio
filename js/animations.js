/* Motion layer — runs before main.js so it can prepare elements first. */
(() => {
  'use strict';
  const root = document.documentElement;
  const loader = document.getElementById('intro-loader');
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { loader && loader.remove(); return; }
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const once = (els, fn, threshold = 0.5) => {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); fn(e.target); } }), { threshold });
    els.forEach(el => io.observe(el));
  };
  root.classList.add('fx-ready');

  const prepareHero = () => {
    const name = $('.hero-name');
    if (name) {
      const text = name.textContent.trim().replace(/\s+/g, ' ');
      name.setAttribute('aria-label', text);
      name.textContent = '';
      let ci = 0;
      text.split(' ').forEach((w, wi, arr) => {
        const word = document.createElement('span');
        word.className = 'word'; word.setAttribute('aria-hidden', 'true');
        [...w].forEach(ch => { const c = document.createElement('span'); c.className = 'char'; c.style.setProperty('--ci', ci++); c.textContent = ch; word.appendChild(c); });
        name.appendChild(word);
        if (wi < arr.length - 1) name.appendChild(document.createTextNode(' '));
      });
    }
    $$('.hero-content-col, .hero-visual-wrapper').forEach(el => el.classList.remove('fade-in-up'));
    ['.hero-eyebrow', '.hero-headline', '.hero-description', '.hero-actions-group', '.hero-meta-strip', '.hero-visual-wrapper']
      .forEach((s, i) => { const el = $(s); if (el) { el.classList.add('hero-anim'); el.style.setProperty('--i', i + 1); } });
  };

  const typeEyebrow = () => {
    const span = $('.hero-eyebrow span');
    if (!span) return;
    const full = span.textContent.trim();
    const phrases = full.split('|').map(s => s.trim()).filter(Boolean);
    if (phrases.length < 2) return;
    span.setAttribute('aria-label', full);
    const label = document.createElement('span'), caret = document.createElement('i');
    caret.className = 'caret';
    span.textContent = ''; span.append(label, caret);
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    (async () => {
      let i = 0;
      for (;;) {
        const p = phrases[i++ % phrases.length];
        for (let n = 1; n <= p.length; n++) { label.textContent = p.slice(0, n); await sleep(55); }
        await sleep(1800);
        for (let n = p.length; n >= 0; n--) { label.textContent = p.slice(0, n); await sleep(28); }
        await sleep(250);
      }
    })();
  };

  const assignReveals = () => {
    const map = { '.about-left-col': 'left', '.about-right-col': 'right', '.why-card': 'flip', '.skill-cat-card': 'zoom', '.project-card': 'rise', '.process-step-card': 'zoom', '.cert-card': 'flip', '.edu-timeline-item': 'left', '.cta-banner-card': 'zoom' };
    Object.entries(map).forEach(([s, v]) => $$(s).forEach(el => el.dataset.reveal = v));
    $$('.skill-chips-container').forEach(c => $$('.skill-chip', c).forEach((chip, i) => chip.style.setProperty('--ci', i)));
  };

  const runLoader = () => {
    const ready = () => { root.classList.add('fx-ready'); document.body.classList.add('is-ready'); };
    if (!loader) return ready();
    const minWait = new Promise(r => setTimeout(r, 1200));
    const assets = Promise.race([Promise.all([document.fonts ? document.fonts.ready : 0, new Promise(r => document.readyState === 'complete' ? r() : addEventListener('load', r))]), new Promise(r => setTimeout(r, 2800))]);
    Promise.all([minWait, assets]).then(() => {
      loader.classList.add('is-done');
      setTimeout(ready, 350);
      setTimeout(() => loader.remove(), 1100);
    });
  };

  const cursorGlow = () => {
    if (!fine) return;
    const g = document.createElement('div'); g.className = 'cursor-glow'; g.setAttribute('aria-hidden', 'true'); document.body.appendChild(g);
    let tx = innerWidth / 2, ty = innerHeight / 2, x = tx, y = ty;
    addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; g.style.opacity = 1; }, { passive: true });
    document.addEventListener('mouseleave', () => g.style.opacity = 0);
    (function loop() { x += (tx - x) * .12; y += (ty - y) * .12; g.style.transform = `translate(${x}px,${y}px)`; requestAnimationFrame(loop); })();
  };

  const heroNetwork = () => {
    const hero = $('#hero');
    if (!hero) return;
    const cv = document.createElement('canvas'); cv.className = 'hero-canvas'; cv.setAttribute('aria-hidden', 'true');
    hero.insertBefore(cv, hero.firstChild);
    const ctx = cv.getContext('2d');
    let w, h, pts = [], run = false, m = { x: -999, y: -999 };
    const size = () => {
      const r = hero.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2);
      w = r.width; h = r.height; cv.width = w * d; cv.height = h * d; ctx.setTransform(d, 0, 0, d, 0, 0);
      const n = Math.round(Math.min(90, Math.max(24, w * h / 16000)) * (fine ? 1 : .55));
      pts = Array.from({ length: n }, () => ({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .5, vy: (Math.random() - .5) * .5, r: 1 + Math.random() * 1.4, c: Math.random() < .7 ? '0,210,255' : '129,140,248' }));
    };
    const frame = () => {
      if (!run) return;
      ctx.clearRect(0, 0, w, h);
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
        const dx = m.x - p.x, dy = m.y - p.y, md = Math.hypot(dx, dy);
        if (md < 170) { p.x += dx * .006; p.y += dy * .006; ctx.strokeStyle = `rgba(${p.c},${(1 - md / 170) * .6})`; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(m.x, m.y); ctx.stroke(); }
        ctx.fillStyle = `rgba(${p.c},.8)`; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill();
      }
      for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
        const d = Math.hypot(pts[i].x - pts[j].x, pts[i].y - pts[j].y);
        if (d < 125) { ctx.strokeStyle = `rgba(0,210,255,${(1 - d / 125) * .28})`; ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.stroke(); }
      }
      requestAnimationFrame(frame);
    };
    const toggle = on => { if (on && !run) { run = true; frame(); } else if (!on) run = false; };
    size(); addEventListener('resize', size);
    hero.addEventListener('mousemove', e => { const r = hero.getBoundingClientRect(); m.x = e.clientX - r.left; m.y = e.clientY - r.top; });
    hero.addEventListener('mouseleave', () => m = { x: -999, y: -999 });
    new IntersectionObserver(([e]) => toggle(e.isIntersecting)).observe(hero);
    document.addEventListener('visibilitychange', () => toggle(!document.hidden));
  };

  const tilt = () => {
    if (!fine) return;
    const set = (sel, max, lift) => $$(sel).forEach(el => {
      el.classList.add('fx-tilt');
      const glow = document.createElement('span'); glow.className = 'fx-glow'; glow.setAttribute('aria-hidden', 'true'); el.appendChild(glow);
      const trans = t => `transform ${t}, border-color .25s, background-color .25s, box-shadow .25s`;
      let raf;
      el.addEventListener('mouseenter', () => { el.style.transition = trans('.12s ease-out'); el.style.transitionDelay = '0s'; });
      el.addEventListener('mousemove', e => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          const r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
          el.style.setProperty('--mx', px * r.width + 'px'); el.style.setProperty('--my', py * r.height + 'px');
          el.style.transform = `perspective(900px) rotateX(${(.5 - py) * max}deg) rotateY(${(px - .5) * max}deg) translateY(${lift}px)`;
        });
      });
      el.addEventListener('mouseleave', () => { cancelAnimationFrame(raf); el.style.transition = trans('.6s cubic-bezier(.16,1,.3,1)'); el.style.transform = ''; });
    });
    set('.why-card, .skill-cat-card, .cert-card, .process-step-card, .edu-card, .metric-box', 8, -4);
    set('.project-card', 3, -4);
    const pc = $('.portrait-container');
    if (pc) {
      pc.addEventListener('mousemove', e => { const r = pc.getBoundingClientRect(); pc.style.transition = 'transform .1s'; pc.style.transform = `perspective(1000px) rotateX(${(.5 - (e.clientY - r.top) / r.height) * 12}deg) rotateY(${((e.clientX - r.left) / r.width - .5) * 14}deg)`; });
      pc.addEventListener('mouseleave', () => { pc.style.transition = 'transform .8s cubic-bezier(.16,1,.3,1)'; pc.style.transform = ''; });
    }
  };

  const buttons = () => {
    $$('.btn').forEach(b => b.addEventListener('click', e => {
      const r = b.getBoundingClientRect(), s = Math.max(r.width, r.height) * 2, d = document.createElement('span');
      d.className = 'ripple'; d.style.cssText = `width:${s}px;height:${s}px;left:${e.clientX - r.left - s / 2}px;top:${e.clientY - r.top - s / 2}px`;
      b.appendChild(d); setTimeout(() => d.remove(), 650);
    }));
    if (!fine) return;
    $$('.hero-actions-group .btn, .btn-nav-cta, .cta-buttons-row .btn').forEach(b => {
      b.addEventListener('mousemove', e => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .25}px,${(e.clientY - r.top - r.height / 2) * .35}px)`; });
      b.addEventListener('mouseleave', () => b.style.transform = '');
    });
  };

  const counters = () => $$('.metric-number').forEach(el => {
    const node = [...el.childNodes].find(n => n.nodeType === 3 && /\d/.test(n.nodeValue));
    const m = node && node.nodeValue.trim().match(/^([\d.]+)(.*)$/);
    if (!m) return;
    const target = parseFloat(m[1]), dec = (m[1].split('.')[1] || '').length, suf = m[2];
    node.nodeValue = (0).toFixed(dec) + suf;
    once([el], () => {
      const t0 = performance.now();
      (function tick(t) {
        const p = Math.min((t - t0) / 1500, 1), e = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
        node.nodeValue = (target * e).toFixed(dec) + suf;
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
    }, 0.6);
  });

  const scramble = () => once($$('.section-title, .about-heading, .cta-heading').filter(el => !el.children.length), el => el.classList.add('tw-go'), 0.7);
  const splitTitles = () => $$('.section-title, .about-heading, .cta-heading').filter(el => !el.children.length).forEach(el => {
    const t = el.textContent.trim().replace(/\s+/g, ' ');
    el.setAttribute('aria-label', t); el.textContent = '';
    t.split(' ').forEach((w, i, arr) => {
      const o = document.createElement('span'), n = document.createElement('span');
      o.className = 'tw'; n.className = 'tw-in'; n.style.setProperty('--wi', i); n.textContent = w; o.setAttribute('aria-hidden', 'true'); o.appendChild(n); el.appendChild(o);
      if (i < arr.length - 1) el.appendChild(document.createTextNode(' '));
    });
  });

  const codeLines = () => {
    const code = $('.code-snippet code'), box = $('.code-window-container');
    if (!code || !box) return;
    code.innerHTML = code.innerHTML.split('\n').map((l, i) => `<span class="code-line" style="--li:${i}">${l || ' '}</span>`).join('');
    once([box], el => el.classList.add('typing'), 0.4);
  };

  const timelines = () => {
    const pt = $('.process-timeline');
    if (pt) once([pt], el => el.classList.add('in-view'), 0.3);
    const et = $('.education-timeline');
    if (et) {
      const upd = () => { const r = et.getBoundingClientRect(); et.style.setProperty('--edu', Math.min(1, Math.max(0, (innerHeight * .75 - r.top) / r.height)).toFixed(3)); };
      addEventListener('scroll', upd, { passive: true }); upd();
    }
  };

  const parallax = () => {
    const amb = $('.hero-ambient-lighting'), vis = $('.hero-visual-wrapper');
    let tick = false;
    addEventListener('scroll', () => {
      if (tick) return; tick = true;
      requestAnimationFrame(() => {
        const y = Math.min(scrollY, innerHeight);
        if (amb) amb.style.transform = `translate(-50%,${y * .25}px)`;
        if (vis) vis.style.translate = `0 ${y * -.08}px`;
        tick = false;
      });
    }, { passive: true });
  };

  const init = () => {
    try { prepareHero(); assignReveals(); splitTitles(); runLoader(); } catch (e) { /* safety */ document.body.classList.add('is-ready'); loader && loader.remove(); }
    setTimeout(() => { document.body.classList.add('is-ready'); loader && loader.remove(); }, 6000);
    
    const wait = setInterval(() => { if (document.body.classList.contains('is-ready')) { clearInterval(wait); setTimeout(typeEyebrow, 1400); } }, 100);
    cursorGlow(); heroNetwork(); tilt(); buttons(); counters(); scramble(); codeLines(); timelines(); parallax();
  };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', init) : init();
})();
