"""Builds the IT Digitalize static site: 4 pages in English (site root) and Arabic (/ar/).

Every translatable element is written once here: English inline, Arabic next to it.
The English pages are written to the root and the Arabic pages to /ar/ (fully translated,
lang="ar" dir="rtl"), with canonical + hreflang tags, a sitemap with language alternates and robots.txt.

Usage:  python tools/build.py .      (run from the site folder)
"""
import os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/site"
AR = {}


def reg(key, ar):
    if key in AR and AR[key] != ar:
        raise SystemExit(f"duplicate key with different text: {key}")
    AR[key] = ar


def T(tag, key, en, ar, attrs="", html=False):
    reg(key, ar)
    a = "data-i18n-html" if html else "data-i18n"
    return f'<{tag} {a}="{key}"{(" " + attrs) if attrs else ""}>{en}</{tag}>'


def PH(key, en, ar):
    reg(key, ar)
    return f'data-i18n-ph="{key}" placeholder="{en}"'


def ATTR(key, attr, en, ar):
    """Translatable attribute such as aria-label or content."""
    reg(key, ar)
    return f'data-i18n-attr="{attr}:{key}" {attr}="{en}"'


# ---------------------------------------------------------------- icons (Lucide, ISC licence)
def svg(inner, size=24, sw=1.8, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')

IC = {
    "network": '<rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/><path d="M12 12V8"/>',
    "server": '<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><path d="M6 6h.01"/><path d="M6 18h.01"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "headset": '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "up": '<path d="m18 15-6-6-6 6"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "tag": '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r="1"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
}
WA_SVG = ('<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4a.5.5 0 0 0 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.1 5.1 0 0 0 1.1 2.7 11.6 11.6 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>')

PHONE = "+20 11 2367 4523"
PHONE_TEL = "+201123674523"
WA_LINK = "https://wa.me/201123674523"
PORTFOLIO_URL = "https://younis.website/"
SITE_URL = "https://it-digitalize.online/"
FACEBOOK = "https://www.facebook.com/I.T.Digitalize"
LINKEDIN = "https://www.linkedin.com/company/it-digitalize"
OG_IMAGE = "https://res.cloudinary.com/o4uwuwtd/image/upload/v1794246986/IT_Digitalize__Y2K_Tech_Dreamscape.png"
PAGE_FILE = {"home": "", "services": "services.html", "pricing": "pricing.html", "contact": "contact.html"}
UNSPLASH = "https://images.unsplash.com/{}?auto=format&fit=crop&w=1000&q=70"
IMG = {
    "networks": "photo-1683322499436-f4383dd59f5a",
    "cctv": "photo-1549109926-58f039549485",
    "servers": "photo-1695668548342-c0c1ad479aee",
    "web": "photo-1525547719571-a2d4ac8945e2",
    "support": "photo-1556761175-4b46a572b786",
    "case1": "photo-1631193816258-28b44b21e78b",
    "case2": "photo-1558494949-ef010cbdcc31",
    "case3": "photo-1498050108023-c5249f4df085",
}
def img(k): return UNSPLASH.format(IMG[k])

CATS = [  # id, icon, en, ar
    ("networks", "network", "Networks & CCTV", "الشبكات والكاميرات"),
    ("servers", "server", "Servers", "السيرفرات"),
    ("web", "globe", "Web", "الويب"),
    ("support", "headset", "IT Support", "الدعم الفني"),
]

# ---------------------------------------------------------------- shared parts
JSONLD = """
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"ProfessionalService","name":"IT Digitalize","url":"%s","logo":"https://res.cloudinary.com/o4uwuwtd/image/upload/v1793989055/ITDD.png","image":"%s","telephone":"+201123674523","areaServed":["Cairo","Giza","Egypt"],"address":{"@type":"PostalAddress","addressLocality":"Cairo","addressCountry":"EG"},"sameAs":["%s","%s"],"description":"Networks, CCTV, servers, websites and monthly IT support for businesses in Cairo & Giza."}
  </script>""" % (SITE_URL, OG_IMAGE, FACEBOOK, LINKEDIN)


LANG_SCRIPT = (
    "<script>(function(){var d=document.documentElement,cur=d.lang,alt=d.getAttribute('data-alt'),s=null;"
    "try{s=localStorage.getItem('itd-lang');}catch(e){}"
    "if(/bot|crawl|spider|slurp|lighthouse|preview|facebookexternalhit/i.test(navigator.userAgent))return;"
    "var b=((navigator.languages&&navigator.languages[0])||navigator.language||'en').toLowerCase();"
    "var want=s||(b.indexOf('ar')===0?'ar':'en');"
    "if(want!==cur&&alt){location.replace(new URL(alt,location.href).href+location.search+location.hash);}})();</script>")


def head(page, title_en, title_ar, desc_en, desc_ar):
    reg(f"meta.{page}.title", title_ar)
    reg(f"meta.{page}.desc", desc_ar)
    return f'''<!doctype html>
<html lang="en" dir="ltr" data-alt="@@ALT@@">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {LANG_SCRIPT}
  <title data-i18n="meta.{page}.title">{title_en}</title>
  <meta name="description" data-i18n-attr="content:meta.{page}.desc" content="{desc_en}">
  <link rel="canonical" href="@@CANON@@">
  <link rel="alternate" hreflang="en" href="{SITE_URL}{PAGE_FILE[page]}">
  <link rel="alternate" hreflang="ar" href="{SITE_URL}ar/{PAGE_FILE[page]}">
  <link rel="alternate" hreflang="x-default" href="{SITE_URL}{PAGE_FILE[page]}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="IT Digitalize">
  <meta property="og:title" data-i18n-attr="content:meta.{page}.title" content="{title_en}">
  <meta property="og:description" data-i18n-attr="content:meta.{page}.desc" content="{desc_en}">
  <meta property="og:url" content="@@CANON@@">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:locale" content="@@LOCALE@@">
  <meta property="og:locale:alternate" content="@@LOCALE_ALT@@">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#000000">
  <link rel="icon" type="image/png" href="https://res.cloudinary.com/o4uwuwtd/image/upload/v1793989055/ITDD.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="@@ASSET@@css/style.css">{JSONLD if page == "home" else ""}
</head>
<body>
'''


def header(active):
    def link(page, href, key, en, ar):
        cls = "nav__link is-active" if page == active else "nav__link"
        cur = ' aria-current="page"' if page == active else ""
        reg(key, ar)
        return f'<a class="{cls}" href="{href}" data-i18n="{key}"{cur}>{en}</a>'
    for cid, ic, en, ar in CATS:
        reg(f"cat.{cid}", ar)
    return f'''
  <div class="topbar">
    <div class="container">
      <span class="topbar__left" data-i18n="top.area">On-site in Cairo &amp; Giza  •  Online everywhere</span>
      <div class="topbar__right">
        <a href="tel:{PHONE_TEL}" class="ltr">{PHONE}</a>
        <div class="lang-switch" aria-label="Language">
          <a href="@@EN_URL@@" hreflang="en" lang="en" data-lang="en" @@EN_CUR@@>EN</a>
          <a href="@@AR_URL@@" hreflang="ar" lang="ar" data-lang="ar" @@AR_CUR@@>عربي</a>
        </div>
      </div>
    </div>
  </div>
  <header class="header" id="header">
    <div class="container">
      <a class="brand" href="index.html" aria-label="IT Digitalize home">IT<span>Digitalize</span></a>
      <nav class="nav" id="nav" aria-label="Main">
        {link("home", "index.html", "nav.home", "Home", "الرئيسية")}
        {link("services", "services.html", "nav.services", "Services", "الخدمات")}
        {link("pricing", "pricing.html", "nav.pricing", "Pricing", "الأسعار")}
        {link("contact", "contact.html", "nav.contact", "Contact", "تواصل معانا")}
        <a class="btn btn--primary nav__cta-mobile" href="pricing.html" data-i18n="cta.calc">Calculate your price</a>
      </nav>
      <a class="btn btn--primary header__cta" href="pricing.html" data-i18n="cta.calc">Calculate your price</a>
      <button class="nav-toggle" id="navToggle" type="button" aria-controls="nav" aria-expanded="false" {ATTR("a11y.menu", "aria-label", "Menu", "القائمة")}>{svg(IC["menu"], 22, 2)}</button>
    </div>
  </header>
'''


reg("top.area", "في الموقع بالقاهرة والجيزة  •  أونلاين في أي مكان")
reg("cta.calc", "احسب السعر")


def form_html(px):
    """Contact form. px = id prefix so the page section and the popup can both have one."""
    opts = [("", "form.opt.choose", "Choose a service", "اختار الخدمة")] + \
           [(en, f"form.opt.{cid}", en, ar) for cid, ic, en, ar in CATS] + \
           [("Monthly support plan", "form.opt.plan", "Monthly support plan", "باقة دعم شهري"),
            ("Site inspection", "form.opt.inspect", "Site inspection", "معاينة"),
            ("Other", "form.opt.other", "Other", "حاجة تانية")]
    options = "".join(
        f'<option value="{v}" data-i18n="{k}"{" disabled selected" if not v else ""}>{en}</option>'
        for v, k, en, ar in opts)
    for v, k, en, ar in opts:
        reg(k, ar)
    return f'''<form class="form js-contact-form" novalidate>
            <div class="form__row">
              <div class="field">
                {T("label", "form.name", "Name", "الاسم", f'for="{px}-name"')}
                <input id="{px}-name" name="name" type="text" autocomplete="name" required {PH("form.name.ph", "Your name", "اسمك")}>
              </div>
              <div class="field">
                {T("label", "form.phone", "Phone / WhatsApp", "الموبايل / واتساب", f'for="{px}-phone"')}
                <input id="{px}-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required {PH("form.phone.ph", "01x xxxx xxxx", "01x xxxx xxxx")}>
              </div>
            </div>
            <div class="field">
              {T("label", "form.service", "Service", "الخدمة", f'for="{px}-service"')}
              <select id="{px}-service" name="service" required>{options}</select>
            </div>
            <div class="field">
              {T("label", "form.msg", "Message", "رسالتك", f'for="{px}-msg"')}
              <textarea id="{px}-msg" name="message" required {PH("form.msg.ph", "Tell us about your office or the issue you have…", "احكيلنا عن مكتبك أو المشكلة اللي عندك…")}></textarea>
            </div>
            <input type="text" name="_honey" tabindex="-1" autocomplete="off" class="visually-hidden" aria-hidden="true">
            <button class="btn btn--primary btn--block" type="submit" data-i18n="form.send">Send request</button>
            <p class="form__status" role="status" aria-live="polite"></p>
          </form>'''


def info_html(cls=""):
    return f'''<div class="info-list {cls}">
            <a class="info" href="{WA_LINK}" target="_blank" rel="noopener">{WA_SVG}<div>{T("small", "info.wa", "WhatsApp", "واتساب")}<strong class="ltr">{PHONE}</strong></div></a>
            <a class="info" href="tel:{PHONE_TEL}">{svg(IC["phone"], 26)}<div>{T("small", "info.call", "Call us", "اتصل بينا")}<strong class="ltr">{PHONE}</strong></div></a>
            <div class="info">{svg(IC["pin"], 26)}<div>{T("small", "info.area", "Area", "المنطقة")}{T("strong", "info.area.v", "Cairo &amp; Giza  •  Online everywhere", "القاهرة والجيزة  •  أونلاين في أي مكان")}</div></div>
          </div>'''


def contact_block():
    return f'''
    <section class="section section--alt" id="contact">
      <div class="container">
        <header class="section-header reveal">
          {T("h2", "contact.title", "Free Consultation", "استشارة مجانية")}
          {T("p", "contact.sub", "Tell us what you need", "قولنا محتاج إيه")}
        </header>
        <div class="contact">
          {form_html("f")}
          {info_html("reveal")}
        </div>
      </div>
    </section>
'''


def footer():
    fb = svg('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>', 16, 2)
    li = svg('<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/>', 16, 2)
    wa = WA_SVG.replace('width="28" height="28"', 'width="16" height="16"')
    social = [(FACEBOOK, "Facebook", fb), (LINKEDIN, "LinkedIn", li), (WA_LINK, "WhatsApp", wa)]
    soc = "".join(f'<a href="{href}" target="_blank" rel="noopener" aria-label="{name}">{icon}</a>' for href, name, icon in social)
    return f'''
  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <a class="brand" href="index.html">IT<span>Digitalize</span></a>
        <nav class="footer__links" aria-label="Footer">
          <a href="index.html" data-i18n="nav.home">Home</a>
          <a href="services.html" data-i18n="nav.services">Services</a>
          <a href="pricing.html" data-i18n="nav.pricing">Pricing</a>
          <a href="contact.html" data-i18n="nav.contact">Contact</a>
          <button type="button" class="footer__consult" data-consult data-i18n="cta.consult">Free Consultation</button>
        </nav>
      </div>
      <div class="footer__bottom">
        <p>© <span id="year">2026</span> IT Digitalize. {T("span", "foot.rights", "All rights reserved.", "جميع الحقوق محفوظة.")}</p>
        <div class="social">{soc}</div>
      </div>
    </div>
  </footer>

  <div class="modal" id="consultModal" hidden>
    <div class="modal__backdrop" data-close></div>
    <div class="modal__dialog" role="dialog" aria-modal="true" aria-labelledby="consultTitle">
      <button class="modal__close" type="button" data-close {ATTR("a11y.close", "aria-label", "Close", "اقفل")}>×</button>
      <header class="modal__head">
        {T("h2", "modal.title", "Contact us now", "كلمنا دلوقتي", 'id="consultTitle"')}
        {T("p", "modal.sub", "Free consultation — tell us what you need and we’ll get back to you within 1 hour.", "استشارة مجانية — قولنا محتاج إيه وهنرد عليك خلال ساعة.")}
      </header>
      <div class="modal__body">
        {form_html("m")}
        {info_html("info-list--compact")}
      </div>
    </div>
  </div>

  <a class="fab-whatsapp" href="{WA_LINK}?text=Hi%20IT%20Digitalize%2C%20I%27d%20like%20to%20know%20more%20about%20your%20services" target="_blank" rel="noopener" {ATTR("a11y.wa", "aria-label", "Chat with us on WhatsApp", "كلمنا على واتساب")}>{WA_SVG}</a>
  <button class="fab-top" id="toTop" type="button" {ATTR("a11y.top", "aria-label", "Back to top", "ارجع لأول الصفحة")}>{svg(IC["up"], 20, 2.5)}</button>
'''


def scripts(*extra):
    tags = ['<script src="@@ASSET@@js/main.js"></script>']
    tags += [f'<script src="@@ASSET@@js/{e}"></script>' for e in extra]
    return "\n  " + "\n  ".join(tags) + "\n</body>\n</html>\n"


# ---------------------------------------------------------------- data
BOX_ITEMS = {
    "networks": [("Network cabling & setup", "تمديد وتجهيز الشبكات"), ("CCTV + mobile viewing", "كاميرات مراقبة ومشاهدة على الموبايل"),
                 ("Office network relocation", "نقل شبكة المكتب"), ("Wi-Fi boost & security", "تقوية وتأمين الواي فاي")],
    "servers": [("Windows Server & Active Directory", "Windows Server و Active Directory"), ("Server troubleshooting", "إصلاح أعطال السيرفرات"),
                ("Backup & data recovery", "باك أب واسترجاع البيانات"), ("Rack installation & organizing", "تركيب وتنظيم الراك")],
    "web": [("Business websites", "مواقع تعريفية للشركات"), ("E-commerce stores", "متاجر إلكترونية"),
            ("Landing pages", "صفحات هبوط (Landing Pages)"), ("Domain, hosting & email", "دومين واستضافة وإيميلات")],
    "support": [("Monthly support plans", "باقات دعم شهرية"), ("Remote & on-site support", "دعم عن بُعد وزيارات في الموقع"),
                ("Windows & software setup", "تثبيت ويندوز والبرامج"), ("Devices & printers setup", "إعداد الأجهزة والطابعات")],
}

SVC_PAGE = {
    "networks": {
        "img": "networks", "img_alt": ("Network cables connected to a switch", "كابلات شبكة متوصلة بسويتش"),
        "lead": ("Reliable wired and wireless networks, plus CCTV you can watch from your phone.",
                 "شبكات سلكية ولاسلكية ثابتة، وكاميرات مراقبة تتابعها من موبايلك."),
        "items": [
            ("Network cabling & setup", "تمديد وتجهيز الشبكات", "Structured cabling, switches and routers for small and growing offices.", "تمديد كابلات منظم وسويتشات وراوترات للمكاتب الصغيرة والمتوسعة."),
            ("Network points", "نقاط الشبكة", "New network points installed and tested where you need them.", "تركيب نقاط شبكة جديدة واختبارها في المكان اللي تحتاجه."),
            ("Router & switch configuration", "إعداد الراوتر والسويتش", "Clean, secure configuration for stable internet across the office.", "إعداد نظيف وآمن لإنترنت ثابت في كل المكتب."),
            ("Wi-Fi setup, boost & security", "إعداد وتقوية وتأمين الواي فاي", "Better coverage, strong passwords and a separate guest network.", "تغطية أحسن وكلمات سر قوية وشبكة منفصلة للضيوف."),
            ("CCTV installation", "تركيب كاميرات المراقبة", "Indoor and outdoor cameras installed and positioned properly.", "تركيب كاميرات داخلية وخارجية في الأماكن الصح."),
            ("DVR / NVR + mobile viewing", "إعداد DVR / NVR والمشاهدة بالموبايل", "Recording set up and connected to the app on your phone.", "إعداد التسجيل وربطه بالتطبيق على موبايلك."),
            ("Office network relocation", "نقل شبكة المكتب", "Moving to a new office? We move and rebuild your network with minimal downtime.", "بتنقل لمكتب جديد؟ بننقل الشبكة ونجهزها بأقل وقت توقف."),
        ]},
    "servers": {
        "img": "servers", "img_alt": ("Rack of servers in a server room", "راك سيرفرات في غرفة سيرفر"),
        "lead": ("Servers that are set up right, backed up and kept running.",
                 "سيرفرات متجهزة صح، عليها باك أب، وشغالة على طول."),
        "items": [
            ("Windows Server installation", "تنصيب Windows Server", "Clean installation and configuration of Windows Server.", "تنصيب وإعداد Windows Server بشكل نظيف."),
            ("Active Directory & domain", "Active Directory والدومين", "Central user accounts, logins and control for every device.", "إدارة مركزية للمستخدمين وتسجيل الدخول والتحكم في كل الأجهزة."),
            ("DNS / DHCP / Group Policy", "DNS / DHCP / GPO", "Core network services and policies configured properly.", "إعداد خدمات الشبكة الأساسية والسياسات بشكل صحيح."),
            ("File server & shared folders", "File Server والمجلدات المشتركة", "Shared folders with the right permissions for each team.", "مجلدات مشتركة بصلاحيات مناسبة لكل فريق."),
            ("Server troubleshooting", "إصلاح أعطال السيرفرات", "We diagnose and fix server problems fast.", "بنشخص مشاكل السيرفر ونحلها بسرعة."),
            ("Backup systems", "أنظمة الباك أب", "Automatic backups so you never lose your data.", "نسخ احتياطي تلقائي عشان بياناتك ما تضيعش."),
            ("Data recovery", "استرجاع البيانات", "Recovering lost data from damaged or failed storage.", "استرجاع البيانات المفقودة من وسائط التخزين التالفة."),
            ("Rack installation & organizing", "تركيب وتنظيم الراك", "A tidy, labeled rack that is easy to maintain.", "راك منظم ومتعلّم وسهل في الصيانة."),
        ]},
    "web": {
        "img": "web", "img_alt": ("Laptop on a desk", "لابتوب على مكتب"),
        "lead": ("Websites designed in-house — fast, responsive and in Arabic and English.",
                 "مواقع بنصممها بنفسنا — سريعة ومتجاوبة وبالعربي والإنجليزي."),
        "items": [
            ("Business websites", "مواقع تعريفية", "A clear, professional website that presents your business.", "موقع واضح واحترافي يعرّف بنشاطك."),
            ("Company websites", "مواقع الشركات الاحترافية", "Multi-page websites with your services, projects and contact forms.", "مواقع متعددة الصفحات فيها خدماتك ومشاريعك وفورم تواصل."),
            ("E-commerce stores", "متاجر إلكترونية", "Online stores with products, payments and shipping (WooCommerce).", "متاجر أونلاين بالمنتجات والدفع والشحن (WooCommerce)."),
            ("Landing pages", "صفحات الهبوط", "One focused page for a campaign, product or offer.", "صفحة واحدة مركزة لحملة أو منتج أو عرض."),
            ("Domain, hosting & business email", "الدومين والاستضافة والإيميلات", "We register, connect and set up everything for you.", "بنحجز ونربط ونجهز كل حاجة ليك."),
            ("Website maintenance", "صيانة وإدارة المواقع", "Monthly updates, backups and support for your website.", "تحديثات ونسخ احتياطي ودعم شهري لموقعك."),
        ]},
    "support": {
        "img": "support", "img_alt": ("IT specialist working at multiple monitors", "متخصص IT شغال قدام أكتر من شاشة"),
        "lead": ("Help when you need it — remotely, on-site, or every month with a support plan.",
                 "مساعدة وقت ما تحتاجها — عن بُعد، أو في الموقع، أو كل شهر بباقة دعم."),
        "items": [
            ("Monthly support plans", "باقات الدعم الشهري", "Ongoing care for your devices, network and servers.", "متابعة مستمرة لأجهزتك وشبكتك وسيرفراتك."),
            ("Remote support", "الدعم عن بُعد", "Most problems solved online, fast.", "أغلب المشاكل بتتحل أونلاين بسرعة."),
            ("On-site visits", "زيارات في الموقع", "Technical visits in Cairo & Giza — by visit, half day or full day.", "زيارات فنية في القاهرة والجيزة — بالزيارة أو نص يوم أو يوم كامل."),
            ("Windows & software installation", "تثبيت ويندوز والبرامج", "Clean installs of Windows and the software your team uses.", "تثبيت نظيف للويندوز والبرامج اللي فريقك بيستخدمها."),
            ("Software maintenance", "صيانة السوفتوير", "Slow or unstable devices diagnosed and fixed.", "تشخيص وإصلاح الأجهزة البطيئة أو اللي بتهنج."),
            ("New device & printer setup", "إعداد الأجهزة والطابعات", "New computers and printers ready to work from day one.", "أجهزة وطابعات جديدة جاهزة للشغل من أول يوم."),
        ]},
}

STEPS = [
    ("Contact us", "تواصل معانا", "WhatsApp, call or the form", "واتساب أو مكالمة أو الفورم"),
    ("Free consultation", "استشارة مجانية", "We understand your needs", "بنفهم احتياجاتك"),
    ("Site inspection", "معاينة الموقع", "We check your place", "بنعاين المكان"),
    ("Quote & setup", "عرض السعر والتنفيذ", "Clear price, fast execution", "سعر واضح وتنفيذ سريع"),
    ("Ongoing support", "دعم مستمر", "Monthly plans or on-demand", "باقات شهرية أو عند الطلب"),
]

FEATURES = [
    ("zap", "Fast response", "رد سريع", "We reply within 1 hour", "بنرد خلال ساعة"),
    ("tag", "Fair prices", "أسعار عادلة", "Clear pricing, no hidden costs", "أسعار واضحة من غير مصاريف مخفية"),
    ("layers", "All in one place", "كل حاجة في مكان واحد", "Networks, servers, web & support", "شبكات وسيرفرات وويب ودعم فني"),
    ("shield", "Ongoing care", "متابعة مستمرة", "Monthly plans that keep you running", "باقات شهرية تخلي شغلك ماشي"),
]


def steps_section():
    cards = "".join(f'''
          <div class="step reveal"><div class="step__num">{i}</div>{T("h3", f"step{i}.t", a, b)}{T("p", f"step{i}.d", c, d)}</div>'''
                    for i, (a, b, c, d) in enumerate(STEPS, 1))
    return f'''
    <section class="section" id="how">
      <div class="container">
        <header class="section-header reveal">
          {T("h2", "how.title", "How We Work", "إزاي بنشتغل")}
          {T("p", "how.sub", "Simple, clear steps — no surprises", "خطوات بسيطة وواضحة — من غير مفاجآت")}
        </header>
        <div class="steps">{cards}
        </div>
      </div>
    </section>
'''


def features_grid():
    return '<div class="features">' + "".join(f'''
          <div class="feature reveal">{svg(IC[ic], 32)}{T("h3", f"feat.{i}.t", a, b)}{T("p", f"feat.{i}.d", c, d)}</div>'''
        for i, (ic, a, b, c, d) in enumerate(FEATURES, 1)) + "\n        </div>"


# ---------------------------------------------------------------- pages
def page_home():
    boxes = ""
    for cid, ic, en, ar in CATS:
        lis = "".join(T("li", f"box.{cid}.{i}", e, a) for i, (e, a) in enumerate(BOX_ITEMS[cid], 1))
        boxes += f'''
          <a class="service-box" href="services.html#{cid}">
            <span class="service-box__icon">{svg(IC[ic], 42, 1.6)}</span>
            <h3 data-i18n="cat.{cid}">{en}</h3>
            <div class="service-box__body"><div class="service-box__inner"><ul>{lis}</ul>{T("span", "box.more", "Learn more →", "اعرف أكتر ←", 'class="service-box__more"')}</div></div>
          </a>'''
    chips = "".join(f'<span class="chip">{p}</span>' for p in ["Basic", "Standard", "Business", "Enterprise"])
    cases = [
        ("case1", "case.1", "IT setup", "تأسيس IT", "Full IT setup from zero — 50 employees", "تأسيس IT كامل من الصفر — 50 موظف",
         "Network, servers, CCTV and all workstations built from scratch for a growing company.",
         "شبكة وسيرفرات وكاميرات وكل الأجهزة اتجهزت من الصفر لشركة بتكبر.",
         "Office with rows of desks and computers", "مكتب فيه صفوف مكاتب وأجهزة كمبيوتر", "#consult", "Start a similar project →", "ابدأ مشروع زيه ←", False),
        ("case2", "case.2", "IT upgrade", "تطوير IT", "IT upgrade — 15 employees", "تطوير IT — 15 موظف",
         "Their network wasn’t working right. We rebuilt and stabilized it so the team can work without interruptions.",
         "الشبكة عندهم ما كانتش شغالة صح. ظبطناها وثبتناها عشان الفريق يشتغل من غير انقطاع.",
         "Network cables in a switch", "كابلات شبكة في سويتش", "#consult", "Fix my network →", "ظبط شبكتي ←", False),
        ("case3", "case.3", "Web", "ويب", "Our website portfolio", "معرض أعمال المواقع",
         "Websites we designed for businesses — browse the full portfolio.",
         "مواقع صممناها لشركات وأنشطة مختلفة — شوف كل الشغل.",
         "Laptop showing code", "لابتوب عليه كود", PORTFOLIO_URL, "Visit portfolio ↗", "شوف البورتفوليو ↗", True),
    ]
    case_html = ""
    for k, key, tag_en, tag_ar, h_en, h_ar, d_en, d_ar, alt_en, alt_ar, href, l_en, l_ar, ext in cases:
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        case_html += f'''
          <article class="case reveal">
            <img src="{img(k)}" {ATTR(key + ".alt", "alt", alt_en, alt_ar)} loading="lazy" width="1000" height="563">
            <div class="case__body">
              {T("span", key + ".tag", tag_en, tag_ar, 'class="case__tag"')}
              {T("h3", key + ".t", h_en, h_ar)}
              {T("p", key + ".d", d_en, d_ar)}
              {('<button type="button" class="case__link" data-consult data-i18n="' + key + '.l">' + l_en + '</button>') if href == "#consult" else ('<a class="case__link" href="' + href + '"' + tgt + ' data-i18n="' + key + '.l">' + l_en + '</a>')}
            </div>
          </article>'''
        reg(key + ".l", l_ar)
    web_checks = [("Responsive on mobile & desktop", "متجاوب على الموبايل والكمبيوتر"), ("Arabic + English", "عربي + إنجليزي"),
                  ("Domain, hosting & business email", "دومين واستضافة وإيميلات")]
    checks = "".join(f'<li>{svg(IC["check"], 18, 2.4)}<span data-i18n="web.c{i}">{e}</span></li>' for i, (e, a) in enumerate(web_checks, 1))
    for i, (e, a) in enumerate(web_checks, 1):
        reg(f"web.c{i}", a)
    return head("home", "IT Digitalize | IT Support, Networks, Servers & Websites in Cairo",
                "IT Digitalize | دعم فني وشبكات وسيرفرات ومواقع في القاهرة",
                "Networks, CCTV, servers, websites and monthly IT support for businesses of every size — on-site in Cairo & Giza and online everywhere.",
                "شبكات وكاميرات مراقبة وسيرفرات ومواقع ودعم فني شهري للشركات بكل أحجامها — في الموقع بالقاهرة والجيزة وأونلاين في أي مكان.") + header("home") + f'''
  <main>
    <section class="hero" id="top">
      <div class="container">
        <h1 class="reveal">
          {T("span", "hero.w1", "Fast", "دعم فني", 'class="c-blue"')}
          {T("span", "hero.w2", "IT support", "سريع", 'class="c-green"')}
          {T("span", "hero.w3", "for your", "لشغلك", 'class="c-blue"')}
          {T("span", "hero.w4", "business", "ولشركتك", 'class="c-green"')}
        </h1>
        {T("p", "hero.sub", "Networks, CCTV, servers, websites and monthly IT support — for businesses of every size, on-site in Cairo &amp; Giza and online everywhere.", "شبكات وكاميرات مراقبة وسيرفرات ومواقع ودعم فني شهري — للشركات بكل أحجامها، في الموقع بالقاهرة والجيزة وأونلاين في أي مكان.", 'class="reveal"')}
        <button type="button" class="btn btn--primary btn--lg reveal" data-consult data-i18n="cta.consult">Free Consultation</button>
      </div>
    </section>

    <section class="service-boxes" aria-labelledby="svcTitle">
      <h2 class="visually-hidden" id="svcTitle" data-i18n="nav.services">Services</h2>
      <div class="container">
        <div class="service-boxes__grid" id="serviceBoxes">{boxes}
        </div>
      </div>
    </section>
{steps_section()}
    <section class="section section--alt" id="plans">
      <div class="container">
        <div class="plans-band reveal">
          <div>
            {T("span", "plans.eyebrow", "Monthly support plans", "باقات الدعم الشهري", 'class="eyebrow"')}
            {T("h2", "plans.title", "Let us keep your IT running every month", "خلّينا نتابع الـ IT بتاعك كل شهر")}
            {T("p", "plans.sub", "Pick the plan that fits your number of devices and working hours — your price is calculated for you instantly.", "اختار الباقة اللي تناسب عدد أجهزتك وساعات شغلك — والسعر بيتحسب لك على طول.")}
            <div class="chips">{chips}</div>
          </div>
          <a class="btn btn--primary btn--lg" href="pricing.html#plans"><span data-i18n="plans.cta">Start your subscription now</span>{svg(IC["arrow"], 18, 2.2, "icon-flip")}</a>
        </div>
      </div>
    </section>

    <section class="section" id="web">
      <div class="container split">
        <div class="reveal">
          {T("span", "web.eyebrow", "Web design", "تصميم المواقع", 'class="eyebrow"')}
          {T("h2", "web.title", "Websites that bring you customers", "مواقع بتجيبلك عملاء")}
          {T("p", "web.sub", "Business websites, online stores and landing pages — designed in-house, fast on every device, in Arabic and English.", "مواقع تعريفية ومتاجر إلكترونية وصفحات هبوط — بنصممها بنفسنا، سريعة على كل الأجهزة، بالعربي والإنجليزي.")}
          <ul class="checklist">{checks}</ul>
          <a class="btn btn--primary" href="services.html#web" data-i18n="web.cta">Start your website</a>
        </div>
        <div class="mockup reveal" aria-hidden="true">
          <div class="laptop">
            <div class="laptop__screen"><div class="fake-site"><div class="fake-site__bar"><i></i><i></i><i></i><i></i></div><div class="fake-site__hero"><i></i><i></i></div><div class="fake-site__cards"><i></i><i></i><i></i></div></div></div>
            <div class="laptop__base"></div>
          </div>
          <div class="phone"><div class="fake-site"><div class="fake-site__bar"><i></i><i></i></div><div class="fake-site__hero"><i></i><i></i></div><div class="fake-site__cards"><i></i><i></i><i></i></div></div></div>
        </div>
      </div>
    </section>

    <section class="section section--alt" id="why">
      <div class="container">
        <header class="section-header reveal">
          {T("h2", "why.title", "Why IT Digitalize", "ليه IT Digitalize")}
          {T("p", "why.sub", "One trusted team for all your business technology", "فريق واحد تثق فيه لكل تكنولوجيا شغلك")}
        </header>
        {features_grid()}
      </div>
    </section>

    <section class="section" id="work">
      <div class="container">
        <header class="section-header reveal">
          {T("h2", "work.title", "Recent Work", "أحدث أعمالنا")}
          {T("p", "work.sub", "Real projects — client names kept private", "مشاريع حقيقية — من غير ذكر أسماء العملاء")}
        </header>
        <div class="cases">{case_html}
        </div>
      </div>
    </section>
{contact_block()}
  </main>
''' + footer() + scripts()


reg("cta.consult", "استشارة مجانية")
reg("box.more", "اعرف أكتر ←")


def page_services():
    body = ""
    for n, (cid, ic, en, ar) in enumerate(CATS):
        d = SVC_PAGE[cid]
        items = "".join(
            f'<li><strong data-i18n="svc.{cid}.{i}.t">{te}</strong><span data-i18n="svc.{cid}.{i}.d">{de}</span></li>'
            for i, (te, ta, de, da) in enumerate(d["items"], 1))
        for i, (te, ta, de, da) in enumerate(d["items"], 1):
            reg(f"svc.{cid}.{i}.t", ta); reg(f"svc.{cid}.{i}.d", da)
        rev = " svc--reverse" if n % 2 else ""
        alt = " section--alt" if n % 2 == 0 else ""
        body += f'''
    <section class="section{alt} svc-anchor" id="{cid}">
      <div class="container svc{rev}">
        <div class="svc__media reveal"><img src="{img(d["img"])}" {ATTR(f"svc.{cid}.alt", "alt", d["img_alt"][0], d["img_alt"][1])} loading="lazy" width="1000" height="750"></div>
        <div class="reveal">
          <h2>{svg(IC[ic], 34, 1.7)}<span data-i18n="cat.{cid}">{en}</span></h2>
          {T("p", f"svc.{cid}.lead", d["lead"][0], d["lead"][1])}
          <ul class="svc-list">{items}</ul>
          <a class="btn btn--primary" href="pricing.html?cat={cid}" data-i18n="cta.calc">Calculate your price</a>
        </div>
      </div>
    </section>'''
    about_list = "".join(f'<li>{svg(IC[ic], 26)}<div><strong data-i18n="feat.{i}.t">{a}</strong><span data-i18n="feat.{i}.d">{c}</span></div></li>'
                         for i, (ic, a, b, c, d) in enumerate(FEATURES, 1))
    for i, (ic, a, b, c, d) in enumerate(FEATURES, 1):
        reg(f"feat.{i}.t", b); reg(f"feat.{i}.d", d)
    return head("services", "Services | IT Digitalize", "الخدمات | IT Digitalize",
                "Networks & CCTV, servers, websites and IT support — everything your business needs from one team.",
                "شبكات وكاميرات وسيرفرات ومواقع ودعم فني — كل اللي شغلك محتاجه من فريق واحد.") + header("services") + f'''
  <main>
    <section class="page-hero">
      <div class="container">
        {T("h1", "svcp.title", "Our Services", "خدماتنا")}
        {T("p", "svcp.sub", "Everything your business needs, from one team", "كل اللي شغلك محتاجه، من فريق واحد")}
      </div>
    </section>

    <section class="section svc-anchor" id="about">
      <div class="container">
        <div class="about-box reveal">
          <div class="about-box__text">
            {T("span", "about.eyebrow", "About IT Digitalize", "عن IT Digitalize", 'class="eyebrow"')}
            {T("h2", "about.h", "Your IT department — without hiring one", "قسم الـ IT بتاعك — من غير ما تعيّن واحد")}
            {T("p", "about.p", "IT Digitalize plans, builds and looks after the technology businesses depend on: networks, CCTV, servers, websites and day-to-day IT support. Clear prices, fast response and one team you can call for everything.", "IT Digitalize بتخطط وتنفذ وتتابع التكنولوجيا اللي شغلك معتمد عليها: الشبكات والكاميرات والسيرفرات والمواقع والدعم الفني اليومي. أسعار واضحة ورد سريع وفريق واحد تكلمه في كل حاجة.")}
          </div>
          <ul class="about-box__list">{about_list}</ul>
        </div>
      </div>
    </section>
{body}
{steps_section()}
  </main>
''' + footer() + scripts()


GOALS = [
    ("new", "layers", "Starting a new business", "ببدأ بيزنس جديد", "Set up everything from zero: network, cameras, server, website and computers.", "جهّز كل حاجة من الصفر: الشبكة والكاميرات والسيرفر والموقع والأجهزة."),
    ("upgrade", "zap", "Upgrade what I have", "عايز أطوّر اللي عندي", "Improve your Wi-Fi, add cameras, back up your data or fix slow computers.", "قوّي الواي فاي، زوّد كاميرات، اعمل باك أب، أو صلّح الأجهزة البطيئة."),
    ("support", "headset", "I need IT support", "محتاج دعم فني", "A monthly plan that keeps your devices, network and server running.", "باقة شهرية تخلي أجهزتك وشبكتك وسيرفرك شغالين على طول."),
    ("web", "globe", "I need a website", "محتاج موقع", "A website, online store or landing page — plus domain and business email.", "موقع أو متجر إلكتروني أو صفحة هبوط — ومعاهم الدومين وإيميلات الشركة."),
]


def page_pricing():
    gh = ""
    for gid, ic, te, ta, de, da in GOALS:
        gh += (f'<button type="button" class="goal" role="radio" aria-checked="false" data-goal="{gid}">'
               f'<span class="goal__icon">{svg(IC[ic], 30, 1.7)}</span>'
               f'{T("strong", f"goal.{gid}.t", te, ta)}{T("span", f"goal.{gid}.d", de, da)}</button>')
    GOALS_HTML = gh
    return head("pricing", "Pricing & Calculator | IT Digitalize", "الأسعار والحاسبة | IT Digitalize",
                "Calculate the price of IT services and monthly support plans instantly.",
                "احسب سعر خدمات الـ IT وباقات الدعم الشهري على طول.") + header("pricing") + f'''
  <main>
    <section class="page-hero">
      <div class="container">
        {T("h1", "price.title", "Calculate Your Price", "احسب السعر")}
        {T("p", "price.sub", "Pick what you need and get an instant estimate", "اختار اللي محتاجه وشوف السعر التقريبي على طول")}
        <button type="button" class="btn btn--outline page-hero__btn" data-consult data-i18n="price.consult">Not sure? Get a free consultation</button>
      </div>
    </section>

    <section class="section" id="plans">
      <div class="container">
        <div class="goals-wrap">
          {T("h2", "shop.pick", "What does your office need?", "مكتبك محتاج إيه؟", 'class="goals__title"')}
          {T("p", "goals.sub", "Choose one — the options below change to match it.", "اختار واحدة — والاختيارات اللي تحت هتتغير على حسبها.", 'class="goals__sub"')}
          <div class="goals" id="goals" role="radiogroup" {ATTR("a11y.goals", "aria-label", "What does your office need?", "مكتبك محتاج إيه؟")}>
            {GOALS_HTML}
          </div>
        </div>
        <p class="goals__empty" id="goalEmpty" data-i18n="goals.empty">Choose an option above to see the services and prices.</p>

        <div class="panel" id="panel-services" hidden>
          <div class="shop">
            <div class="shop__main">
              <div class="start-box">
                <div>
                  {T("h3", "shop.inspect.t", "Want an exact price? Book a site inspection", "عايز سعر دقيق؟ احجز معاينة")}
                  {T("p", "shop.inspect.d", "We visit your office and give you a final quote — 1,500 EGP, 500 EGP off for first-time clients.", "بنزور مكتبك ونديك عرض سعر نهائي — 1,500 جنيه، وخصم 500 جنيه لأول مرة.")}
                </div>
                <button class="btn btn--primary" type="button" id="addInspection"></button>
              </div>
              <h3 class="shop__title" id="goalTitle"></h3>
              <div class="cat-chips" id="catChips" role="tablist" {ATTR("a11y.cats", "aria-label", "Categories", "الأقسام")}></div>
              <div class="products" id="products"></div>
            </div>
            <aside class="cart" id="cart" aria-live="polite">
              <div class="cart__head">
                {T("h3", "cart.title", "Your order", "طلبك")}
                <span class="cart__count" id="cartCount">0</span>
              </div>
              <div class="cart__items" id="cartItems"></div>
              <label class="check" id="firstWrap" hidden><input type="checkbox" id="c-first" checked> <span data-i18n="cart.first">First time with IT Digitalize (500 EGP off the inspection)</span></label>
              <div class="cart__total">
                {T("span", "cart.total", "Estimated total", "الإجمالي التقريبي")}
                <div><strong id="r-total">0</strong> {T("span", "egp", "EGP", "جنيه")}</div>
              </div>
              <p class="cart__monthly" id="r-monthly"></p>
              {T("p", "calc.note", "Labor only. Equipment, cables, materials and licenses are separate. Final price after inspection.", "سعر المصنعية فقط. الأجهزة والكابلات والخامات والتراخيص منفصلة. السعر النهائي بعد المعاينة.", 'class="result__note"')}
              <div class="result__actions">
                <button class="btn btn--primary" type="button" id="r-request" data-i18n="calc.request">Request this quote</button>
                <a class="btn btn--outline" id="r-wa" href="{WA_LINK}" target="_blank" rel="noopener" data-i18n="calc.wa">Send on WhatsApp</a>
                <button class="cart__clear" type="button" id="r-clear" data-i18n="cart.clear">Clear order</button>
              </div>
            </aside>
          </div>
          <a class="cart-bar" href="#cart" id="cartBar"><span><span data-i18n="cart.title">Your order</span> (<b id="barCount">0</b>)</span><span>≈ <b id="barTotal">0</b> <span data-i18n="egp">EGP</span></span></a>
          <div class="toast" id="toast" role="status" aria-live="polite"></div>
        </div>

        <div class="panel" id="panel-plans" hidden>
          <div class="calc">
            <div class="calc__card">
              <div class="field">
                <div class="range-head"><label for="p-dev" data-i18n="plan.devices">Number of devices</label><output id="p-dev-out">5</output></div>
                <input class="range" id="p-dev" type="range" min="1" max="40" value="5">
              </div>
              <div class="field">
                <div class="range-head"><label for="p-hrs" data-i18n="plan.hours">Your working hours per day</label><output id="p-hrs-out">8</output></div>
                <input class="range" id="p-hrs" type="range" min="8" max="16" value="8">
                {T("p", "plan.hours.n", "Plans cover 8 working hours. Each extra hour adds 10%.", "الباقات بتغطي 8 ساعات شغل. كل ساعة زيادة بتضيف 10%.", 'class="result__note"')}
              </div>
              <div class="plan-picks" id="p-picks"></div>
              <ul class="plan-features" id="p-features"></ul>
            </div>
            <aside class="result" aria-live="polite">
              <h3><span data-i18n="plan.your">Your plan:</span> <b id="p-name" style="color:#fff"></b></h3>
              <div class="result__lines" id="p-lines"></div>
              <div class="result__total"><strong id="p-total">0</strong> <span data-i18n="egp.month">EGP / month</span></div>
              {T("p", "plan.note", "Visits: 600 EGP + transport (up to 400 EGP), agreed at contract start. Response time: 1 hour.", "الزيارة: 600 جنيه + انتقالات (لحد 400 جنيه) بتتحدد في بداية التعاقد. وقت الاستجابة: ساعة.", 'class="result__note"')}
              <div class="result__actions">
                <button class="btn btn--primary" type="button" id="p-request" data-i18n="plan.request">Start this plan</button>
                <a class="btn btn--outline" id="p-wa" href="{WA_LINK}" target="_blank" rel="noopener" data-i18n="calc.wa">Send on WhatsApp</a>
              </div>
            </aside>
          </div>
        </div>

        <div class="notes">
          <div class="note reveal">{T("h3", "n1.t", "Free consultation", "استشارة مجانية")}{T("p", "n1.d", "Send us your needs and we’ll recommend the right specs — free.", "ابعتلنا احتياجاتك وهنقولك المواصفات المناسبة — ببلاش.")}</div>
          <div class="note reveal">{T("h3", "n2.t", "Equipment", "الأجهزة والخامات")}{T("p", "n2.d", "You buy the equipment; we can go with you to buy it for 1,000 EGP.", "انت بتشتري الأجهزة، وممكن ننزل معاك نشتريها مقابل 1,000 جنيه.")}</div>
          <div class="note reveal">{T("h3", "n3.t", "Emergencies", "الطوارئ")}{T("p", "n3.d", "Outside working hours: +50% of the visit price, or half a visit price if solved online.", "بره ساعات الشغل: +50% من سعر الزيارة، أو نص سعر الزيارة لو اتحلت أونلاين.")}</div>
        </div>
      </div>
    </section>
  </main>
''' + footer() + scripts("pricing.js")


reg("price.consult", "مش متأكد؟ خد استشارة مجانية")
reg("goals.empty", "اختار حاجة من فوق علشان تشوف الخدمات والأسعار.")
reg("cart.first", "أول مرة أتعامل مع IT Digitalize (خصم 500 جنيه على المعاينة)")
reg("cart.clear", "امسح الطلب")
reg("calc.request", "اطلب عرض السعر ده")
reg("calc.wa", "ابعته على واتساب")
reg("plan.devices", "عدد الأجهزة")
reg("plan.hours", "ساعات الشغل في اليوم")
reg("plan.your", "باقتك:")
reg("egp.month", "جنيه / شهرياً")
reg("plan.request", "ابدأ الباقة دي")


def page_contact():
    return head("contact", "Contact | IT Digitalize", "تواصل معانا | IT Digitalize",
                "Contact IT Digitalize — WhatsApp, phone or the form. Free consultation, reply within 1 hour.",
                "تواصل مع IT Digitalize — واتساب أو تليفون أو الفورم. استشارة مجانية ورد خلال ساعة.") + header("contact") + f'''
  <main>
    <section class="page-hero">
      <div class="container">
        {T("h1", "contactp.title", "Contact Us", "تواصل معانا")}
        {T("p", "contactp.sub", "Free consultation — tell us what you need and we’ll reply within 1 hour.", "استشارة مجانية — قولنا محتاج إيه وهنرد عليك خلال ساعة.")}
      </div>
    </section>
    <section class="section" id="contact">
      <div class="container">
        <div class="contact">
          {form_html("f")}
          {info_html("reveal")}
        </div>
      </div>
    </section>
  </main>
''' + footer() + scripts()


for k, v in {
    "form.send": "ابعت الطلب",
    "plans.cta": "ابدأ اشتراكك دلوقتي",
    "web.cta": "ابدأ موقعك",
    "nav.home": "الرئيسية",
}.items():
    reg(k, v)


# ---------------------------------------------------------------- write
from bs4 import BeautifulSoup

PAGE_KEY = {"index.html": "home", "services.html": "services", "pricing.html": "pricing", "contact.html": "contact"}
pages = {"index.html": page_home(), "services.html": page_services(), "pricing.html": page_pricing(), "contact.html": page_contact()}


def render(html, name, lang):
    """Fill the language-specific placeholders, translate to Arabic if needed and strip the i18n attributes."""
    ar = lang == "ar"
    path = PAGE_FILE[PAGE_KEY[name]]
    rep = {
        "@@ASSET@@": "../" if ar else "",
        "@@CANON@@": SITE_URL + ("ar/" if ar else "") + path,
        "@@ALT@@": ("../" + name) if ar else ("ar/" + name),
        "@@EN_URL@@": ("../" + name) if ar else name,
        "@@AR_URL@@": name if ar else ("ar/" + name),
        "@@EN_CUR@@": "" if ar else 'aria-current="true"',
        "@@AR_CUR@@": 'aria-current="true"' if ar else "",
        "@@LOCALE@@": "ar_EG" if ar else "en_US",
        "@@LOCALE_ALT@@": "en_US" if ar else "ar_EG",
    }
    for k, v in rep.items():
        html = html.replace(k, v)
    soup = BeautifulSoup(html, "html.parser")
    if ar:
        soup.html["lang"], soup.html["dir"] = "ar", "rtl"
    for el in soup.select("[data-i18n]"):
        if ar:
            el.string = AR[el["data-i18n"]]
        del el["data-i18n"]
    for el in soup.select("[data-i18n-html]"):
        if ar:
            el.clear()
            el.append(BeautifulSoup(AR[el["data-i18n-html"]], "html.parser"))
        del el["data-i18n-html"]
    for el in soup.select("[data-i18n-ph]"):
        if ar:
            el["placeholder"] = AR[el["data-i18n-ph"]]
        del el["data-i18n-ph"]
    for el in soup.select("[data-i18n-attr]"):
        attr, k = el["data-i18n-attr"].split(":")
        if ar:
            el[attr] = AR[k]
        del el["data-i18n-attr"]
    out = str(soup)
    if "@@" in out or "data-i18n" in out:
        raise SystemExit(f"unrendered placeholder in {lang}/{name}")
    return out


os.makedirs(os.path.join(OUT, "ar"), exist_ok=True)
for name, html in pages.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(render(html, name, "en"))
    with open(os.path.join(OUT, "ar", name), "w", encoding="utf-8") as f:
        f.write(render(html, name, "ar"))

with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
urls = ""
for p in PAGE_FILE.values():
    alts = (f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{p}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="ar" href="{SITE_URL}ar/{p}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}{p}"/>\n')
    for loc in (f"{SITE_URL}{p}", f"{SITE_URL}ar/{p}"):
        urls += f"  <url>\n    <loc>{loc}</loc>\n{alts}  </url>\n"
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
print("pages:", list(pages), "x2 (en + ar/)")
