# Google tak pohanchana — Asaan Lang + Mizanora

Developer: **Muaaz Iqbal** · Store: https://mizanora.vercel.app · GitHub: https://github.com/muaaziqbalvip

## 1) Vercel par site (public URL)

Yeh repo **static site** hai (`public/`). Python interpreter Vercel par nahi chalta.

1. GitHub par latest `main` push karo
2. [vercel.com](https://vercel.com) → Project → **asaan-lang**
3. Settings → General:
   - **Framework Preset:** Other
   - **Root Directory:** *khaali* (repo root)
   - **Build Command:** `npm run build`  (ya Override OFF + default)
   - **Output Directory:** `public`
   - **Install Command:** `echo skip`  (optional)
4. Deploy

Agar error `PYTHON_ENTRYPOINT_NOT_FOUND` aaye to Framework Preset zaroor **Other** karo — Vercel `studio.py` ko ghalat function samajh raha hota hai.

Is folder mein pehle se hain:

- `web/index.html` `docs.html` `ecosystem.html` (crawlable HTML, hash nahi)
- `web/sitemap.xml` `robots.txt` `llms.txt` `og.jpg`
- JSON-LD (SoftwareApplication + Person + Organization)
- Open Graph / Twitter cards
- `hreflang` ur + en-PK

## 2) Google Search Console

1. https://search.google.com/search-console
2. URL prefix: `https://asaan-lang.vercel.app`
3. HTML tag ya DNS — Vercel domain verify
4. **Sitemaps** → `https://asaan-lang.vercel.app/sitemap.xml` submit
5. Mizanora store par bhi Asaan ka link do (footer / tools) taake Google ko internal authority mile:

   `Asaan Lang — Urdu programming: https://asaan-lang.vercel.app`

## 3) Viral / ranking signals

| Signal | Status |
|---|---|
| Unique title + description | haan |
| Canonical | haan |
| sitemap.xml + robots.txt | haan |
| Person/Org schema → mizanora.vercel.app | haan |
| Backlinks from Mizanora family | aap footer mein add karein |
| GitHub topics | `urdu` `pakistan` `programming-language` |
| Share `og.jpg` WhatsApp/X par | web/og.jpg |

Google ko index ke liye **public HTTPS** zaroori hai — local studio Google nahi padhta.
