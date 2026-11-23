/* ==========================================================================
   IT Digitalize — shared behaviour (all pages, English and /ar/)
   Language choice, navigation, scroll effects, service boxes,
   consultation popup, back-to-top and the contact form (FormSubmit).
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------------
     SETTINGS
     ------------------------------------------------------------------ */
  // Form messages are delivered to this inbox by FormSubmit (https://formsubmit.co) — free, no server needed.
  // The FIRST message sends an activation email to this inbox: open it and click "Activate Form".
  // After activating, FormSubmit gives you a random alias; you can put it here instead of the email
  // so the address is not visible in the page code.
  var FORM_INBOX = 'it.digitalize@outlook.com';

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var html = document.documentElement;
  var isAr = html.lang === 'ar';

  // Messages created by JavaScript (page text is already in the right language in the HTML)
  var MSG = {
    fields: ['Please fill in all fields.', 'من فضلك املا كل الخانات.'],
    phone: ['Please enter a valid phone number.', 'من فضلك اكتب رقم موبايل صحيح.'],
    setup: ['The form is not connected yet — please contact us on WhatsApp.', 'الفورم لسه مش متوصل — كلمنا على واتساب.'],
    sending: ['Sending…', 'جاري الإرسال…'],
    ok: ['Thank you! We received your request and will contact you within 1 hour.', 'شكراً! وصلنا طلبك وهنتواصل معاك خلال ساعة.'],
    fail: ['Something went wrong. Please try again or contact us on WhatsApp.', 'حصلت مشكلة. جرب تاني أو كلمنا على واتساب.']
  };
  var msg = function (k) { return MSG[k][isAr ? 1 : 0]; };
  window.ITD = { lang: function () { return isAr ? 'ar' : 'en'; } };

  /* ---------------- Language ---------------- */
  // The page opens in the browser language (script in <head>); a click on EN / عربي is remembered.
  $$('.lang-switch a').forEach(function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('itd-lang', a.getAttribute('data-lang')); } catch (e) {}
    });
  });

  /* ---------------- Header & nav ---------------- */
  var header = $('#header');
  var onScroll = function () {
    var y = window.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    var top = $('#toTop');
    if (top) top.classList.toggle('is-visible', y > 500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var nav = $('#nav'), toggle = $('#navToggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  if (nav) {
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('is-open'); }); });
  }

  /* ---------------- Back to top ---------------- */
  var toTop = $('#toTop');
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------------- Reveal + service boxes ---------------- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var boxes = $$('.service-box');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.15 });
    $$('.reveal').forEach(function (el) { io.observe(el); });

    // Boxes start with icon + title; once the user scrolls down to them they open one by one.
    var grid = $('#serviceBoxes');
    if (grid) {
      var opened = false;
      var openBoxes = function () {
        if (opened) return;
        opened = true;
        boxes.forEach(function (b, i) { setTimeout(function () { b.classList.add('is-open'); }, i * 220); });
      };
      var bio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && window.pageYOffset > 40) { openBoxes(); bio.disconnect(); }
        });
      }, { threshold: 0.6 });
      bio.observe(grid);
      window.addEventListener('scroll', function once() {
        if (window.pageYOffset > 120) { openBoxes(); window.removeEventListener('scroll', once); }
      }, { passive: true });
    }
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
    boxes.forEach(function (b) { b.classList.add('is-open'); });
  }

  /* ---------------- Footer year ---------------- */
  var y = $('#year');
  if (y) y.textContent = new Date().getFullYear();

  /* ---------------- Contact forms (page section + popup) ---------------- */
  function setupForm(form) {
    var status = $('.form__status', form);
    var setStatus = function (key, cls) {
      status.textContent = msg(key);
      status.className = 'form__status ' + (cls || '');
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form._honey.value) return; // spam bot
      var name = form.name.value.trim(), phone = form.phone.value.trim();
      var service = form.service.value, message = form.message.value.trim();
      if (!name || !phone || !service || !message) {
        setStatus('fields', 'is-error');
        return;
      }
      if (!/^[+\d][\d\s-]{7,}$/.test(phone)) {
        setStatus('phone', 'is-error');
        form.phone.focus();
        return;
      }
      if (!FORM_INBOX) {
        setStatus('setup', 'is-error');
        return;
      }
      var btn = $('button[type="submit"]', form);
      btn.disabled = true;
      setStatus('sending');
      var payload = {
        name: name, phone: phone, service: service, message: message,
        page: location.pathname.split('/').pop() || 'index.html',
        _subject: 'New request from the website — ' + service,
        _template: 'table',
        _captcha: 'false'
      };
      fetch('https://formsubmit.co/ajax/' + FORM_INBOX, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); }).then(function (res) {
        if (!res.ok || String(res.j.success) !== 'true') throw new Error(res.j.message || 'failed');
        form.reset();
        setStatus('ok', 'is-ok');
      }).catch(function () {
        setStatus('fail', 'is-error');
      }).then(function () { btn.disabled = false; });
    });
  }
  $$('.js-contact-form').forEach(setupForm);

  /* ---------------- Free consultation popup ---------------- */
  var modal = $('#consultModal'), lastFocus = null;
  function prefill(form, data) {
    if (!form || !data) return;
    if (data.message) form.message.value = data.message;
    if (data.service && $$('option', form.service).some(function (o) { return o.value === data.service; })) form.service.value = data.service;
  }
  function openConsult(data) {
    if (!modal) return;
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    var form = $('.js-contact-form', modal);
    prefill(form, data);
    setTimeout(function () { form.name.focus(); }, 50);
  }
  function closeConsult() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove('modal-open');
    if (lastFocus) lastFocus.focus();
  }
  window.ITD.openConsult = openConsult;
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-consult]');
    if (b) { e.preventDefault(); openConsult(); }
    if (e.target.closest('[data-close]')) closeConsult();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeConsult();
    if (e.key === 'Tab' && modal && !modal.hidden) {
      var f = $$('button, a[href], input:not(.visually-hidden), select, textarea', modal).filter(function (x) { return !x.disabled && x.offsetParent !== null; });
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
})();
