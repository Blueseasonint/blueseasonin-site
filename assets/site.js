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
  var years = doc.querySelectorAll('[data-since]');
  for (var i = 0; i < years.length; i++) {
    var since = parseInt(years[i].getAttribute('data-since'), 10);
    if (since) years[i].textContent = (new Date().getFullYear() - since) + '+';
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
