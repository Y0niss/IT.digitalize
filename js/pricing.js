/* ==========================================================================
   IT Digitalize — pricing page: "Set up my office" shop + monthly plans
   Prices are the suggested prices from IT_Digitalize_Pricing_List_2026.xlsx (EGP).
   To change a price, edit the number in PRODUCTS or PLANS below.
   ========================================================================== */
(function () {
  'use strict';
  var $ = function (s) { return document.querySelector(s); };
  var L = function () { return window.ITD ? window.ITD.lang() : 'en'; };
  var tr = function (o) { return o ? (o[L()] || o.en) : ''; };

  var CATS = [
    { id: 'networks', en: 'Network & CCTV', ar: 'الشبكة والكاميرات' },
    { id: 'servers', en: 'Server & backup', ar: 'السيرفر والباك أب' },
    { id: 'web', en: 'Website & email', ar: 'الموقع والإيميلات' },
    { id: 'devices', en: 'Computers', ar: 'الأجهزة' }
  ];

  /* type: 'fixed' one price | 'qty' price per unit | 'choice' pick one option | 'quote' priced after inspection
     included / extraPer: business email = price for the first `included` accounts + extraPer for each extra
     monthly: billed every month */
  var PRODUCTS = [
    { id: 'net', cat: 'networks', type: 'choice', en: 'Office network setup', ar: 'تجهيز شبكة المكتب',
      d: { en: 'Switches, router and cabling layout so every device in your office is connected.', ar: 'سويتشات وراوتر وتوزيع كابلات علشان كل أجهزة مكتبك تبقى متوصلة.' },
      options: [
        { en: 'Up to 5 devices', ar: 'حتى 5 أجهزة', price: 2000 },
        { en: '6 to 15 devices', ar: 'من 6 لـ 15 جهاز', price: 5000 },
        { en: 'More than 15 devices', ar: 'أكتر من 15 جهاز', price: 'quote' }
      ] },
    { id: 'points', cat: 'networks', type: 'qty', price: 300, en: 'Network points', ar: 'نقاط شبكة',
      unit: { en: 'point', ar: 'نقطة' }, d: { en: 'A wired network outlet installed and tested at each desk.', ar: 'نقطة شبكة سلكية تتركب وتتجرب عند كل مكتب.' } },
    { id: 'wifi', cat: 'networks', type: 'fixed', price: 700, en: 'Wi-Fi setup & security', ar: 'إعداد وتأمين الواي فاي',
      d: { en: 'Secure Wi-Fi with strong passwords and a separate guest network.', ar: 'واي فاي آمن بكلمات سر قوية وشبكة منفصلة للضيوف.' } },
    { id: 'wifiboost', cat: 'networks', type: 'fixed', price: 1000, en: 'Wi-Fi coverage boost', ar: 'تقوية تغطية الواي فاي',
      d: { en: 'Strong signal in every room (access points sold separately).', ar: 'إشارة قوية في كل أوضة (الأكسس بوينت بتتحسب لوحدها).' } },
    { id: 'cams', cat: 'networks', type: 'qty', price: 500, en: 'CCTV cameras installation', ar: 'تركيب كاميرات مراقبة',
      unit: { en: 'camera', ar: 'كاميرا' }, d: { en: 'Indoor or outdoor cameras installed in the right spots.', ar: 'كاميرات داخلية أو خارجية تتركب في الأماكن الصح.' } },
    { id: 'nvr', cat: 'networks', type: 'fixed', price: 1000, en: 'CCTV recorder + mobile viewing', ar: 'جهاز التسجيل + المشاهدة بالموبايل',
      d: { en: 'DVR/NVR setup and live view on your phone.', ar: 'إعداد DVR/NVR ومشاهدة مباشرة على موبايلك.' } },

    { id: 'server', cat: 'servers', type: 'fixed', price: 10000, en: 'Full office server setup', ar: 'تجهيز سيرفر المكتب بالكامل',
      d: { en: 'Windows Server, user accounts & domain, shared folders and permissions — ready to use.', ar: 'Windows Server وحسابات المستخدمين والدومين والمجلدات المشتركة والصلاحيات — جاهز للشغل.' } },
    { id: 'files', cat: 'servers', type: 'fixed', price: 1500, en: 'Shared folders & permissions', ar: 'مجلدات مشتركة وصلاحيات',
      d: { en: 'On a server you already have: shared folders with the right access for each team.', ar: 'على سيرفر موجود عندك: مجلدات مشتركة بصلاحيات مناسبة لكل فريق.' } },
    { id: 'backup', cat: 'servers', type: 'fixed', price: 2000, en: 'Automatic backup system', ar: 'نظام باك أب تلقائي',
      d: { en: 'Your data backed up automatically (storage sold separately).', ar: 'بياناتك بتتنسخ تلقائياً (وسائط التخزين بتتحسب لوحدها).' } },
    { id: 'rack', cat: 'servers', type: 'fixed', price: 2500, en: 'Rack installation & organizing', ar: 'تركيب وتنظيم الراك',
      d: { en: 'A tidy, labeled rack that is easy to maintain.', ar: 'راك منظم ومتعلّم وسهل في الصيانة.' } },
    { id: 'fix', cat: 'servers', type: 'fixed', price: 1000, en: 'Fix a server problem', ar: 'إصلاح مشكلة في السيرفر',
      d: { en: 'Diagnosis and repair (parts and licenses separate).', ar: 'تشخيص وإصلاح (قطع الغيار والتراخيص منفصلة).' } },

    { id: 'site', cat: 'web', type: 'choice', en: 'Website', ar: 'موقع إلكتروني',
      d: { en: 'Designed in-house, responsive, in Arabic and English.', ar: 'تصميم خاص بيك، متجاوب، بالعربي والإنجليزي.' },
      options: [
        { en: 'Landing page (1 page)', ar: 'صفحة هبوط (صفحة واحدة)', price: 3000 },
        { en: 'Business website', ar: 'موقع تعريفي', price: 6000 },
        { en: 'Professional company website', ar: 'موقع شركة احترافي', price: 20000 },
        { en: 'Online store', ar: 'متجر إلكتروني', price: 20000 }
      ] },
    { id: 'domain', cat: 'web', type: 'fixed', price: 1500, en: 'Domain & hosting setup', ar: 'إعداد الدومين والاستضافة',
      d: { en: 'We register your domain and connect it to hosting (fees paid separately).', ar: 'بنحجز الدومين ونربطه بالاستضافة (الرسوم بتتدفع لوحدها).' } },
    { id: 'email', cat: 'web', type: 'qty', price: 500, included: 3, extraPer: 100, min: 1, en: 'Business email accounts', ar: 'إيميلات باسم الشركة',
      unit: { en: 'account', ar: 'إيميل' }, d: { en: '500 EGP for up to 3 accounts, +100 EGP for each extra account.', ar: '500 جنيه لحد 3 إيميلات، و100 جنيه لكل إيميل زيادة.' } },
    { id: 'care', cat: 'web', type: 'fixed', price: 1000, monthly: true, en: 'Website care (monthly)', ar: 'متابعة الموقع (شهري)',
      d: { en: 'Updates, backups and small edits every month.', ar: 'تحديثات ونسخ احتياطي وتعديلات بسيطة كل شهر.' } },

    { id: 'newpc', cat: 'devices', type: 'qty', price: 400, en: 'New computer setup', ar: 'تجهيز جهاز جديد',
      unit: { en: 'computer', ar: 'جهاز' }, d: { en: 'Windows, user account and your team’s software — ready on day one.', ar: 'ويندوز وحساب المستخدم وبرامج فريقك — جاهز من أول يوم.' } },
    { id: 'reinstall', cat: 'devices', type: 'qty', price: 400, en: 'Windows & software reinstall', ar: 'تسطيب ويندوز وبرامج',
      unit: { en: 'computer', ar: 'جهاز' }, d: { en: 'Clean reinstall for slow or broken computers (licenses separate).', ar: 'تسطيب نظيف للأجهزة البطيئة أو اللي فيها مشاكل (التراخيص منفصلة).' } },
    { id: 'tuneup', cat: 'devices', type: 'qty', price: 500, en: 'Computer tune-up & repair', ar: 'صيانة وإصلاح سوفتوير للجهاز',
      unit: { en: 'computer', ar: 'جهاز' }, d: { en: 'Software problems diagnosed and fixed.', ar: 'تشخيص وإصلاح مشاكل السوفتوير.' } }
  ];
  // Which products show for each goal on the "What does your office need?" step
  var GOAL_ITEMS = {
    new: ['net', 'points', 'wifi', 'wifiboost', 'cams', 'nvr', 'server', 'backup', 'rack', 'site', 'domain', 'email', 'care', 'newpc'],
    upgrade: ['points', 'wifi', 'wifiboost', 'cams', 'nvr', 'files', 'backup', 'rack', 'fix', 'site', 'email', 'care', 'newpc', 'reinstall', 'tuneup'],
    web: ['site', 'domain', 'email', 'care']
  };
  var GOAL_TITLE = {
    new: { en: 'Everything a new office needs', ar: 'كل اللي مكتب جديد محتاجه' },
    upgrade: { en: 'Upgrade your office', ar: 'طوّر مكتبك' },
    web: { en: 'Your website', ar: 'موقعك' }
  };
  var goal = null;
  var visible = function (p) { return goal && GOAL_ITEMS[goal] && GOAL_ITEMS[goal].indexOf(p.id) > -1; };

  var INSPECTION = { id: 'inspect', type: 'fixed', price: 1500, en: 'Site inspection', ar: 'معاينة الموقع' };
  var FIRST_DISCOUNT = 500;

  var TXT = {
    egp: { en: 'EGP', ar: 'جنيه' },
    month: { en: '/ month', ar: '/ شهرياً' },
    per: { en: 'per', ar: 'لكل' },
    from: { en: 'from', ar: 'من' },
    quote: { en: 'Priced after inspection', ar: 'السعر بعد المعاينة' },
    add: { en: 'Add to order', ar: 'أضف للطلب' },
    update: { en: 'Update', ar: 'تحديث' },
    inCart: { en: 'In your order', ar: 'في طلبك' },
    remove: { en: 'Remove', ar: 'شيل' },
    added: { en: 'Added to your order', ar: 'اتضاف لطلبك' },
    removed: { en: 'Removed from your order', ar: 'اتشال من طلبك' },
    empty: { en: 'Your order is empty. Add what your office needs from the list.', ar: 'طلبك فاضي. ضيف اللي مكتبك محتاجه من القائمة.' },
    monthlyLine: { en: 'Plus monthly:', ar: 'وكمان شهرياً:' },
    addInspect: { en: '+ Add site inspection', ar: '+ أضف معاينة' },
    inspectAdded: { en: '✓ Inspection added', ar: '✓ المعاينة اتضافت' },
    firstOff: { en: 'First-time discount', ar: 'خصم أول مرة' },
    noItems: { en: 'Please add at least one item first.', ar: 'ضيف حاجة واحدة على الأقل الأول.' },
    msgHead: { en: 'Hi IT Digitalize, I would like a quote for:', ar: 'أهلاً IT Digitalize، محتاج عرض سعر لـ:' },
    estimate: { en: 'Estimated total', ar: 'الإجمالي التقريبي' },
    custom: { en: 'Custom quote', ar: 'عرض سعر مخصص' },
    customLine: { en: 'More than 30 devices — we prepare a custom plan.', ar: 'أكتر من 30 جهاز — بنجهزلك باقة مخصصة.' },
    base: { en: 'plan', ar: 'باقة' },
    extraHours: { en: 'Extra hours', ar: 'ساعات إضافية' },
    upTo: { en: 'Up to', ar: 'حتى' },
    devices: { en: 'devices', ar: 'جهاز' },
    msgPlan: { en: 'Hi IT Digitalize, I would like to start a monthly support plan:', ar: 'أهلاً IT Digitalize، عايز أبدأ باقة دعم شهري:' },
    hours: { en: 'working hours / day', ar: 'ساعات شغل في اليوم' }
  };

  var fmt = function (n) { return Number(n).toLocaleString(L() === 'ar' ? 'ar-EG' : 'en-US'); };
  var money = function (n) { return fmt(n) + ' ' + tr(TXT.egp); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var byId = function (id) { return id === 'inspect' ? INSPECTION : PRODUCTS.filter(function (p) { return p.id === id; })[0]; };

  /* ---------------- Cart state ---------------- */
  var cart = []; // { id, q, opt }
  var draft = {}; // per product: chosen qty / option before adding
  var activeCat = 'networks';
  try { var saved = JSON.parse(sessionStorage.getItem('itd-cart') || '[]'); if (Array.isArray(saved)) cart = saved.filter(function (c) { return byId(c.id); }); } catch (e) {}
  var save = function () { try { sessionStorage.setItem('itd-cart', JSON.stringify(cart)); } catch (e) {} };
  var inCart = function (id) { return cart.filter(function (c) { return c.id === id; })[0]; };

  function priceOf(p, q, opt) {
    if (p.type === 'quote') return null;
    if (p.type === 'choice') { var o = p.options[opt || 0]; return typeof o.price === 'number' ? o.price : null; }
    if (p.extraPer) return p.price + Math.max(0, q - p.included) * p.extraPer;
    return p.type === 'qty' ? p.price * q : p.price;
  }
  function priceLabel(p) {
    if (p.type === 'quote') return tr(TXT.quote);
    if (p.type === 'choice') {
      var nums = p.options.map(function (o) { return o.price; }).filter(function (x) { return typeof x === 'number'; });
      return tr(TXT.from) + ' ' + money(Math.min.apply(null, nums));
    }
    if (p.extraPer) return money(p.price) + ' (' + fmt(p.included) + ')';
    if (p.type === 'qty') return money(p.price) + ' ' + tr(TXT.per) + ' ' + tr(p.unit);
    return money(p.price) + (p.monthly ? ' ' + tr(TXT.month) : '');
  }
  function itemLabel(c) {
    var p = byId(c.id);
    var name = tr(p);
    if (p.type === 'choice') name += ' — ' + tr(p.options[c.opt || 0]);
    if (p.type === 'qty') name += ' × ' + fmt(c.q);
    return name;
  }
  function totals() {
    var once = 0, monthly = 0;
    cart.forEach(function (c) {
      var p = byId(c.id), v = priceOf(p, c.q, c.opt);
      if (v === null) return;
      if (p.monthly) monthly += v; else once += v;
    });
    if (inCart('inspect') && $('#c-first').checked) once -= FIRST_DISCOUNT;
    return { once: Math.max(0, once), monthly: monthly };
  }

  /* ---------------- Rendering ---------------- */
  function renderChips() {
    var cats = CATS.filter(function (c) { return PRODUCTS.some(function (p) { return p.cat === c.id && visible(p); }); });
    if (!cats.some(function (c) { return c.id === activeCat; }) && cats.length) activeCat = cats[0].id;
    $('#catChips').hidden = cats.length < 2;
    $('#catChips').innerHTML = cats.map(function (c) {
      var n = cart.filter(function (x) { var p = byId(x.id); return p.cat === c.id; }).length;
      return '<button type="button" role="tab" class="cat-chip" data-cat="' + c.id + '" aria-selected="' + (c.id === activeCat) + '">' + tr(c) + (n ? ' <span class="cat-chip__n">' + fmt(n) + '</span>' : '') + '</button>';
    }).join('');
  }

  function renderProducts() {
    var html = PRODUCTS.filter(function (p) { return p.cat === activeCat && visible(p); }).map(function (p) {
      var c = inCart(p.id), dr = draft[p.id] || {};
      var q = c ? c.q : (dr.q || (p.min || 1)), opt = c ? (c.opt || 0) : (dr.opt || 0);
      var control = '';
      if (p.type === 'qty') {
        control = '<div class="qty qty--sm"><button type="button" data-act="minus" aria-label="−">−</button><input type="number" min="1" max="500" value="' + q + '" data-act="q" aria-label="' + esc(tr(p.unit)) + '"><button type="button" data-act="plus" aria-label="+">+</button></div><span class="muted">' + tr(p.unit) + '</span>';
      } else if (p.type === 'choice') {
        control = '<div class="opts">' + p.options.map(function (o, i) {
          return '<label class="opt' + (i === opt ? ' is-on' : '') + '"><input type="radio" name="opt-' + p.id + '" value="' + i + '"' + (i === opt ? ' checked' : '') + ' data-act="opt"><span>' + tr(o) + '</span><b>' + (typeof o.price === 'number' ? money(o.price) : tr(TXT.quote)) + '</b></label>';
        }).join('') + '</div>';
      }
      var lineP = priceOf(p, q, opt);
      var btn = c
        ? '<span class="product__in">✓ ' + tr(TXT.inCart) + '</span><button type="button" class="product__rm" data-act="remove">' + tr(TXT.remove) + '</button>'
        : '<button type="button" class="btn btn--primary product__add" data-act="add">' + tr(TXT.add) + '</button>';
      return '<article class="product' + (c ? ' is-in' : '') + '" data-id="' + p.id + '">' +
        '<div class="product__top"><h4>' + tr(p) + '</h4><span class="product__price">' + priceLabel(p) + '</span></div>' +
        '<p>' + tr(p.d) + '</p>' +
        (control ? '<div class="product__control">' + control + '</div>' : '') +
        '<div class="product__foot"><span class="product__sum">' + (lineP === null ? tr(TXT.quote) : money(lineP) + (p.monthly ? ' ' + tr(TXT.month) : '')) + '</span><div class="product__btns">' + btn + '</div></div>' +
        '</article>';
    }).join('');
    $('#products').innerHTML = html;
  }

  function renderCart() {
    var box = $('#cartItems');
    if (!cart.length) box.innerHTML = '<p class="result__empty">' + tr(TXT.empty) + '</p>';
    else box.innerHTML = cart.map(function (c, i) {
      var p = byId(c.id), v = priceOf(p, c.q, c.opt);
      var stepper = p.type === 'qty'
        ? '<div class="qty qty--xs"><button type="button" data-cart="minus" data-i="' + i + '" aria-label="−">−</button><span>' + fmt(c.q) + '</span><button type="button" data-cart="plus" data-i="' + i + '" aria-label="+">+</button></div>' : '';
      var extra = '';
      if (c.id === 'inspect' && $('#c-first').checked) extra = '<div class="cart-item__sub">' + tr(TXT.firstOff) + ' − ' + money(FIRST_DISCOUNT) + '</div>';
      return '<div class="cart-item">' +
        '<div class="cart-item__main"><span class="cart-item__name">' + (p.type === 'choice' ? tr(p) + ' — ' + tr(p.options[c.opt || 0]) : tr(p)) + '</span>' + extra + stepper + '</div>' +
        '<div class="cart-item__side"><b>' + (v === null ? tr(TXT.quote) : money(v) + (p.monthly ? ' ' + tr(TXT.month) : '')) + '</b>' +
        '<button type="button" class="cart-item__rm" data-cart="rm" data-i="' + i + '" aria-label="' + tr(TXT.remove) + '" title="' + tr(TXT.remove) + '">' +
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button></div>' +
        '</div>';
    }).join('');
    var t = totals();
    $('#r-total').textContent = '≈ ' + fmt(t.once);
    $('#r-monthly').textContent = t.monthly ? tr(TXT.monthlyLine) + ' ' + money(t.monthly) + ' ' + tr(TXT.month) : '';
    $('#cartCount').textContent = fmt(cart.length);
    $('#barCount').textContent = fmt(cart.length);
    $('#barTotal').textContent = fmt(t.once);
    $('#cartBar').classList.toggle('is-visible', cart.length > 0);
    $('#firstWrap').hidden = !inCart('inspect');
    $('#r-clear').hidden = !cart.length;
    var ib = $('#addInspection');
    ib.textContent = inCart('inspect') ? tr(TXT.inspectAdded) : tr(TXT.addInspect);
    ib.disabled = !!inCart('inspect');
    $('#r-wa').href = 'https://wa.me/201123674523?text=' + encodeURIComponent(cart.length ? orderMessage() : tr(TXT.msgHead));
    save();
  }
  function renderShop() {
    if (goal && GOAL_TITLE[goal]) $('#goalTitle').textContent = tr(GOAL_TITLE[goal]);
    renderChips(); renderProducts(); renderCart();
  }

  var toastTimer;
  function toast(msg) {
    var t = $('#toast');
    t.textContent = msg;
    t.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove('is-on'); }, 1800);
  }

  function orderMessage() {
    var t = totals(), out = [tr(TXT.msgHead)];
    cart.forEach(function (c) {
      var p = byId(c.id), v = priceOf(p, c.q, c.opt);
      out.push('- ' + itemLabel(c) + ': ' + (v === null ? tr(TXT.quote) : money(v) + (p.monthly ? ' ' + tr(TXT.month) : '')));
    });
    if (inCart('inspect') && $('#c-first').checked) out.push('- ' + tr(TXT.firstOff) + ': − ' + money(FIRST_DISCOUNT));
    out.push(tr(TXT.estimate) + ': ≈ ' + money(t.once) + (t.monthly ? ' + ' + money(t.monthly) + ' ' + tr(TXT.month) : ''));
    return out.join('\n');
  }

  /* ---------------- Events ---------------- */
  $('#catChips').addEventListener('click', function (e) {
    var b = e.target.closest('[data-cat]');
    if (!b) return;
    activeCat = b.getAttribute('data-cat');
    renderChips(); renderProducts();
  });

  function clampQ(v) { return Math.max(1, Math.min(500, parseInt(v, 10) || 1)); }
  function setQ(card, p, q) {
    q = clampQ(q);
    var c = inCart(p.id);
    if (c) { c.q = q; renderCart(); renderChips(); }
    else { draft[p.id] = draft[p.id] || {}; draft[p.id].q = q; }
    card.querySelector('[data-act="q"]').value = q;
    var opt = c ? c.opt : (draft[p.id] && draft[p.id].opt) || 0;
    card.querySelector('.product__sum').textContent = money(priceOf(p, q, opt));
  }

  $('#products').addEventListener('click', function (e) {
    var el = e.target.closest('[data-act]');
    if (!el) return;
    var card = el.closest('.product'), p = byId(card.getAttribute('data-id'));
    var act = el.getAttribute('data-act');
    var input = card.querySelector('[data-act="q"]');
    if (act === 'minus') setQ(card, p, (input ? +input.value : 1) - 1);
    else if (act === 'plus') setQ(card, p, (input ? +input.value : 1) + 1);
    else if (act === 'add') {
      var dr = draft[p.id] || {};
      cart.push({ id: p.id, q: p.type === 'qty' ? clampQ(input ? input.value : 1) : 1, opt: p.type === 'choice' ? (dr.opt || 0) : 0 });
      delete draft[p.id];
      renderShop();
      toast(tr(TXT.added) + ': ' + tr(p));
    } else if (act === 'remove') {
      cart = cart.filter(function (c) { return c.id !== p.id; });
      renderShop();
      toast(tr(TXT.removed));
    }
  });
  $('#products').addEventListener('change', function (e) {
    var el = e.target, card = el.closest('.product');
    if (!card) return;
    var p = byId(card.getAttribute('data-id'));
    if (el.getAttribute('data-act') === 'q') setQ(card, p, el.value);
    if (el.getAttribute('data-act') === 'opt') {
      var opt = +el.value, c = inCart(p.id);
      if (c) c.opt = opt; else { draft[p.id] = draft[p.id] || {}; draft[p.id].opt = opt; }
      renderProducts(); renderCart();
    }
  });

  $('#cartItems').addEventListener('click', function (e) {
    var b = e.target.closest('[data-cart]');
    if (!b) return;
    var i = +b.getAttribute('data-i'), c = cart[i], act = b.getAttribute('data-cart');
    if (!c) return;
    if (act === 'rm') { cart.splice(i, 1); toast(tr(TXT.removed)); }
    if (act === 'minus') c.q = clampQ(c.q - 1);
    if (act === 'plus') c.q = clampQ(c.q + 1);
    renderShop();
  });
  $('#addInspection').addEventListener('click', function () {
    if (!inCart('inspect')) { cart.unshift({ id: 'inspect', q: 1, opt: 0 }); renderCart(); toast(tr(TXT.added) + ': ' + tr(INSPECTION)); }
  });
  $('#c-first').addEventListener('change', renderCart);
  $('#r-clear').addEventListener('click', function () { cart = []; renderShop(); });
  $('#r-request').addEventListener('click', function () {
    if (!cart.length) { $('#cartItems').innerHTML = '<p class="result__empty" style="color:#ff7a7a">' + tr(TXT.noItems) + '</p>'; return; }
    var first = byId(cart.filter(function (c) { return c.id !== 'inspect'; })[0] ? cart.filter(function (c) { return c.id !== 'inspect'; })[0].id : 'inspect');
    var map = { networks: 'Networks & CCTV', servers: 'Servers', web: 'Web', devices: 'IT Support' };
    goContact(orderMessage(), map[first.cat] || 'Other');
  });

  // ?cat= from the Services page, #plans from the Home page
  var qc = new URLSearchParams(location.search).get('cat');
  var startGoal = location.hash === '#plans' ? 'support' : ({ networks: 'new', servers: 'new', web: 'web', support: 'support' })[qc] || null;
  if (qc && CATS.some(function (c) { return c.id === qc; })) activeCat = qc;
  var PLANS = [
    { name: 'Basic', max: 5, price: 2000, f: [
      { en: 'Remote support', ar: 'دعم عن بُعد' }, { en: 'Basic follow-up during working hours', ar: 'متابعة أساسية خلال ساعات الشغل' }, { en: '1-hour response time', ar: 'رد خلال ساعة' }] },
    { name: 'Standard', max: 10, price: 3500, f: [
      { en: 'Remote support', ar: 'دعم عن بُعد' }, { en: 'Network, internet & printers follow-up', ar: 'متابعة الشبكة والإنترنت والطابعات' }, { en: 'Simple monthly report', ar: 'تقرير شهري مبسط' }] },
    { name: 'Business', max: 15, price: 5000, f: [
      { en: 'Remote support', ar: 'دعم عن بُعد' }, { en: 'Server & network monitoring', ar: 'متابعة السيرفر والشبكة' }, { en: 'Backup monitoring', ar: 'متابعة النسخ الاحتياطي' }] },
    { name: 'Enterprise', max: 30, price: 8000, f: [
      { en: 'Remote support', ar: 'دعم عن بُعد' }, { en: 'Custom, clearly defined scope of work', ar: 'نطاق شغل مخصص وواضح' }, { en: 'Server, network & backup monitoring', ar: 'متابعة السيرفر والشبكة والنسخ الاحتياطي' }] }
  ];


  /* ---------------- Monthly plans ---------------- */
  var dev = $('#p-dev'), hrs = $('#p-hrs');
  function planFor(n) { for (var i = 0; i < PLANS.length; i++) if (n <= PLANS[i].max) return PLANS[i]; return null; }
  function renderPlans() {
    var n = +dev.value, h = +hrs.value, p = planFor(n);
    $('#p-dev-out').textContent = n > 30 ? '30+' : fmt(n);
    $('#p-hrs-out').textContent = fmt(h);
    $('#p-picks').innerHTML = PLANS.map(function (pl) {
      return '<button type="button" class="plan-pick' + (p === pl ? ' is-active' : '') + '" data-max="' + pl.max + '"><strong>' + pl.name + '</strong><span>' + tr(TXT.upTo) + ' ' + fmt(pl.max) + ' ' + tr(TXT.devices) + '</span></button>';
    }).join('');
    var check = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
    if (!p) {
      $('#p-name').textContent = tr(TXT.custom);
      $('#p-features').innerHTML = '<li>' + check + tr(TXT.customLine) + '</li>';
      $('#p-lines').innerHTML = '<div class="result__line"><span>' + tr(TXT.customLine) + '</span></div>';
      $('#p-total').textContent = tr(TXT.custom);
      updatePlanWa(null, n, h, 0);
      return;
    }
    var extra = Math.max(0, h - 8) * 0.10 * p.price;
    var total = Math.round(p.price + extra);
    $('#p-name').textContent = p.name;
    $('#p-features').innerHTML = p.f.map(function (f) { return '<li>' + check + tr(f) + '</li>'; }).join('');
    var lh = '<div class="result__line"><span>' + (L() === 'ar' ? tr(TXT.base) + ' ' + p.name : p.name + ' ' + tr(TXT.base)) + ' (' + tr(TXT.upTo) + ' ' + fmt(p.max) + ' ' + tr(TXT.devices) + ')</span><b>' + money(p.price) + '</b></div>';
    if (extra) lh += '<div class="result__line"><span>' + tr(TXT.extraHours) + ' (' + fmt(h - 8) + ' × 10%)</span><b>' + money(Math.round(extra)) + '</b></div>';
    $('#p-lines').innerHTML = lh;
    $('#p-total').textContent = fmt(total);
    updatePlanWa(p, n, h, total);
  }
  function planMessage(p, n, h, total) {
    return tr(TXT.msgPlan) + '\n- ' + (p ? p.name : tr(TXT.custom)) + '\n- ' + (n > 30 ? '30+' : n) + ' ' + tr(TXT.devices) + '\n- ' + h + ' ' + tr(TXT.hours) +
      (p ? '\n' + tr(TXT.estimate) + ': ' + money(total) + ' ' + tr(TXT.month) : '');
  }
  var lastPlan = null;
  function updatePlanWa(p, n, h, total) {
    lastPlan = { p: p, n: n, h: h, total: total };
    $('#p-wa').href = 'https://wa.me/201123674523?text=' + encodeURIComponent(planMessage(p, n, h, total));
  }
  dev.addEventListener('input', renderPlans);
  hrs.addEventListener('input', renderPlans);
  $('#p-picks').addEventListener('click', function (e) {
    var b = e.target.closest('[data-max]');
    if (b) { dev.value = b.getAttribute('data-max'); renderPlans(); }
  });
  $('#p-request').addEventListener('click', function () {
    goContact(planMessage(lastPlan.p, lastPlan.n, lastPlan.h, lastPlan.total), 'Monthly support plan');
  });


  function goContact(message, service) {
    if (window.ITD && window.ITD.openConsult) window.ITD.openConsult({ message: message, service: service });
  }

  /* ---------------- Goal picker ("What does your office need?") ---------------- */
  var goalBtns = Array.prototype.slice.call(document.querySelectorAll('[data-goal]'));
  function selectGoal(g, scroll) {
    goal = g;
    goalBtns.forEach(function (b) {
      var on = b.getAttribute('data-goal') === g;
      b.setAttribute('aria-checked', on ? 'true' : 'false');
      b.classList.toggle('is-on', on);
    });
    $('#goalEmpty').hidden = !!g;
    $('#panel-plans').hidden = g !== 'support';
    $('#panel-services').hidden = !g || g === 'support';
    if (g && g !== 'support') renderShop();
    if (g === 'support') renderPlans();
    if (scroll) {
      var target = g === 'support' ? $('#panel-plans') : $('#panel-services');
      var top = target.getBoundingClientRect().top + window.pageYOffset - 110;
      if (target.getBoundingClientRect().top > window.innerHeight * 0.6) window.scrollTo({ top: top, behavior: 'smooth' });
    }
  }
  goalBtns.forEach(function (b, i) {
    b.addEventListener('click', function () { selectGoal(b.getAttribute('data-goal'), true); });
    b.addEventListener('keydown', function (e) {
      var d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
      if (!d) return;
      e.preventDefault();
      var n = goalBtns[(i + d + goalBtns.length) % goalBtns.length];
      n.focus(); selectGoal(n.getAttribute('data-goal'), false);
    });
  });

  /* ---------------- Init + language changes ---------------- */
  function renderAll() { if (goal && goal !== 'support') renderShop(); else renderCart(); renderPlans(); }
  if (startGoal) selectGoal(startGoal, false); else renderAll();
})();
