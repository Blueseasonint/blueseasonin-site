(function () {
  'use strict';
  var doc = document;
  var isHe = (doc.documentElement.lang || '').toLowerCase().indexOf('he') === 0;

  /* Mobile navigation */
  var header = doc.querySelector('header');
  var navBar = header && header.querySelector('.nav');
  var links = header && header.querySelector('.nav-links');
  if (navBar && links) {
    if (!links.id) links.id = 'primary-nav';
    var btn = doc.createElement('button');
    btn.type = 'button';
    btn.className = 'nav-toggle';
    btn.setAttribute('aria-controls', links.id);
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', isHe ? 'פתיחת תפריט' : 'Open menu');
    btn.innerHTML = '<span></span><span></span><span></span>';
    navBar.appendChild(btn);

    var setOpen = function (open) {
      links.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? (isHe ? 'סגירת תפריט' : 'Close menu') : (isHe ? 'פתיחת תפריט' : 'Open menu'));
    };
    btn.addEventListener('click', function () { setOpen(!links.classList.contains('is-open')); });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setOpen(false); btn.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 980) setOpen(false); });
  }

  /* Compact header after scrolling */
  if (header) {
    var onScroll = function () { header.classList.toggle('is-compact', window.scrollY > 40); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* "22+ years" stays correct every year */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var years = doc.querySelectorAll('[data-since]');
  for (var i = 0; i < years.length; i++) {
    (function (el) {
      var since = parseInt(el.getAttribute('data-since'), 10);
      if (!since) return;
      var target = new Date().getFullYear() - since;
      if (reduce || !window.requestAnimationFrame) { el.textContent = target + '+'; return; }
      var start = null, dur = 1400;
      var step = function (t) {
        if (start === null) start = t;
        var k = Math.min((t - start) / dur, 1);
        var eased = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(target * eased) + '+';
        if (k < 1) window.requestAnimationFrame(step);
      };
      el.textContent = '0+';
      window.requestAnimationFrame(step);
    })(years[i]);
  }

  /* Scroll progress bar */
  if (!reduce) {
    var bar = doc.createElement('div');
    bar.className = 'scroll-progress';
    bar.setAttribute('aria-hidden', 'true');
    doc.body.appendChild(bar);
    var ticking = false;
    var update = function () {
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty('--p', h > 0 ? Math.min(window.scrollY / h, 1).toFixed(4) : 0);
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* Reveal on scroll */
  if (!reduce && 'IntersectionObserver' in window) {
    var sel = '.section-head, .about-image, .about-text, .timeline-item, .activity, .principle, ' +
              '.leader-visual, .leader-text, .portfolio-v2-head, .company-card, .investment-focus, ' +
              '.investment-philosophy, .media-card, .contact-box, .contact-details, .metric, .intro-card, .press-grid > *';
    var items = doc.querySelectorAll(sel);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    for (var j = 0; j < items.length; j++) {
      var node = items[j];
      var siblings = node.parentElement ? node.parentElement.children : [];
      var idx = Array.prototype.indexOf.call(siblings, node);
      node.style.setProperty('--d', (Math.min(Math.max(idx, 0), 5) * 0.08).toFixed(2) + 's');
      node.classList.add('reveal');
      io.observe(node);
    }
  }


  /* Floating WhatsApp button: show after the hero, hide while the contact form is on screen */
  var fab = doc.querySelector('.fab-whatsapp');
  if (fab) {
    var contactEl = doc.getElementById('contact');
    var contactVisible = false;
    var syncFab = function () { fab.classList.toggle('is-visible', window.scrollY > 520 && !contactVisible); };
    if (contactEl && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { contactVisible = en[0].isIntersecting; syncFab(); }, { threshold: 0.15 }).observe(contactEl);
    }
    window.addEventListener('scroll', syncFab, { passive: true });
    syncFab();
  }

  /* Prevent double submit */
  var form = doc.querySelector('.callback-form');
  if (form) {
    form.addEventListener('submit', function () {
      var b = form.querySelector('button[type="submit"]');
      if (b && form.checkValidity()) { b.disabled = true; }
    });
    window.addEventListener('pageshow', function () {
      var b = form.querySelector('button[type="submit"]');
      if (b) b.disabled = false;
    });
  }
})();
