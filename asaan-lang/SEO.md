# Google tak pohanchana — Asaan Lang + Mizanora

Developer: **Muaaz Iqbal** · Store: https://mizanora.vercel.app · GitHub: https://github.com/muaaziqbalvip

## 1) Vercel par site (public URL)

1. https://github.com/muaaziqbalvip/asaan-lang push karo
2. [vercel.com](https://vercel.com) → Add New → Project → yeh repo
3. **Root Directory:** `web`
4. Deploy → URL: `https://asaan-lang.vercel.app`

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
