# IT Digitalize — Website

Static website, English + Arabic. No server needed.

| Page | English | Arabic |
|---|---|---|
| Home | `index.html` | `ar/index.html` |
| Services (About box at the top, then the 4 service areas) | `services.html` | `ar/services.html` |
| Pricing — "What does your office need?" + order cart + monthly plans | `pricing.html` | `ar/pricing.html` |
| Contact | `contact.html` | `ar/contact.html` |

Shared files: `css/style.css`, `js/main.js` (all pages), `js/pricing.js` (pricing page).

## Language
- First visit: the site opens in the browser's language (Arabic browser → `/ar/`, anything else → English).
- Clicking **EN / عربي** switches pages and is remembered for next time.
- Search engines are never redirected; each language has its own URL, `canonical` and `hreflang` tags.

## Publish on GitHub Pages (it-digitalize.online)
1. Create a repository and upload **everything in this folder** (keep `CNAME` and `.nojekyll`; `tools/` is optional).
2. Repository → **Settings → Pages** → Source: *Deploy from a branch* → branch `main`, folder `/ (root)`.
3. Custom domain: `it-digitalize.online` (already in the `CNAME` file) → tick **Enforce HTTPS** once it is available.
4. At your domain provider add DNS records:
   - 4 × **A** for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **CNAME** for `www` → `<your-github-username>.github.io`
5. Submit `https://it-digitalize.online/sitemap.xml` in Google Search Console.

Other hosting: upload the same files to the root, so `index.html` is at `https://it-digitalize.online/`.

## Contact form (one-time activation)
Send a test message from the contact form after uploading. FormSubmit emails **it.digitalize@outlook.com**
an activation link (check Junk too) — click **Activate Form**. After that every request arrives in that inbox.
Optional: replace the email in `js/main.js` → `FORM_INBOX` with the random alias FormSubmit gives you.

## Editing
- **Prices**: `js/pricing.js` → `PRODUCTS` and `PLANS`. Which items show for each choice: `GOAL_ITEMS`.
- **Text (both languages)**: edit `tools/build.py` (English and Arabic side by side), then from this folder run
  `python tools/build.py .` — it regenerates the 8 pages, `sitemap.xml` and `robots.txt`.
  Requires Python 3 and `pip install beautifulsoup4`.

## Credits
Icons: Lucide (ISC), inline. Photos: Unsplash (free licence). Hero background: the Cloudinary image from the original site.
