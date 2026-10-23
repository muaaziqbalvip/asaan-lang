# آسان لینگ — Asaan Lang

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-emerald.svg)](CHANGELOG.md)
[![Made in Pakistan](https://img.shields.io/badge/Made%20in-Pakistan%20🇵🇰-brightgreen.svg)](#)

**Pakistan ki apni programming language.**  
Soch Urdu mein. Code Urdu / Roman-Urdu mein. Website bhi isi zubaan se.

**Developer:** [Muaaz Iqbal](https://mizanora.vercel.app) · Punjab, Pakistan · 2026  
**Profile / store:** [mizanora.vercel.app](https://mizanora.vercel.app) · **GitHub:** [muaaziqbalvip](https://github.com/muaaziqbalvip)  
**Public site (Google):** [asaan-lang.vercel.app](https://asaan-lang.vercel.app) · [SEO.md](SEO.md)

```asaan
naam = lo "Aap ka naam? "
agar naam != "" to
    likho "Khush Amdeed, " + naam + "!"
warna
    likho "Mehman, salaam!"
bas
```

```asaan
لکھو "السلام علیکم دنیا!"
```

---

## Kyun Asaan Lang?

Python seekhne se pehle aksar **English** seekhni padti hai. Asaan Lang pehle **soch** seekhati hai — variables, loops, decisions — apni zubaan mein. Jab dimagh ready ho, Python asaan lagti hai.

| | |
|---|---|
| Zubaan | Roman-Urdu **aur** Urdu script |
| Audience | Beginners, schools, Urdu-medium students |
| Errors | Roman-Urdu mein, line number ke saath |
| Bonus | Isi language se HTML website compile |

Poori dictionary: **[FEATURES.md](FEATURES.md)**

---

## Install (Python ki tarah)

Pehle [Python 3.8+](https://www.python.org/downloads/) — Windows par setup mein **"Add python.exe to PATH"** tick karein.

### Linux / macOS

```bash
git clone https://github.com/muaaziqbalvip/asaan-lang.git
cd asaan-lang
chmod +x install.sh
./install.sh
```

### Windows

1. Repo download / clone
2. `install.bat` par double-click
3. **Nayi** Command Prompt kholo

### pip (developers)

```bash
cd asaan-lang
pip install -e .
```

Hatana: `uninstall.sh` / `uninstall.bat`

### Bina install

```bash
python3 asaan.py examples/hello.asaan
python3 asaan.py --studio
```

---

## Istamaal — saare tareeqe

Install ke baad **kisi bhi folder** se:

```bash
asaan                          # REPL  (bahar: niklo)
asaan meri.asaan               # file chalao
asaan -e "likho 1+2"           # ek line
asaan --web site.asaan -o site.html
asaan --studio                 # playground  http://localhost:8080
asaan --version                # Asaan Lang 1.1 — Muaaz Iqbal
asaan --help
```

### Playground (web)

```bash
asaan --studio
```

| URL | Kya hai |
|---|---|
| http://localhost:8080/ | Editor + examples + live run |
| http://localhost:8080/site | Website **jo khud Asaan Lang se bani** |
| http://localhost:8080/school | Kasur Academy demo site |

---

## Language — 30 second

| Kaam | Code |
|---|---|
| Print / input | `likho "Salaam"` · `naam = lo "Naam? "` |
| If | `agar x > 5 to … aur agar … warna … bas` |
| Loops | `har i se 1 tak 10 to` · `dohrao 5 to` · `jabtak` |
| List | `dost = ["Ali", "Fatima"]` · `dost[1]` pehla |
| Dict | `talib = {naam: "Ali", umar: 14}` |
| Function | `kaam jama(a, b) wapis a + b bas` |
| Random | `ittifaq(1, 6)` |
| Errors | `koshish … pakro g … bas` |
| Import | `lao "lib_hisab.asaan"` |
| Web | `safha` `unwan` `para` `card` `button` `footer` |

Mukammal table: [FEATURES.md](FEATURES.md)

---

## Examples

```bash
asaan examples/hello.asaan      # salaam + input
asaan examples/grades.asaan     # aur agar
asaan examples/fehrist.asaan    # lists
asaan examples/kitab.asaan      # dictionaries
asaan examples/dice.asaan       # random + dohrao
asaan examples/koshish.asaan    # try/catch + lao
asaan examples/guess.asaan      # chhota game
asaan examples/urdu.asaan       # خالص اردو
asaan --web examples/website.asaan -o site.html
```

---

## Project layout

```
asaan-lang/
├── asaan.py           # compiler / interpreter
├── studio.py          # playground server
├── studio/index.html  # IDE UI
├── examples/          # .asaan programs
├── install.sh / install.bat
├── FEATURES.md        # poori dictionary
├── LICENSE            # MIT — Muaaz Iqbal
└── PUBLISH.md         # GitHub par daalne ka tareeqa
```

---

## Requirements

- Python 3.8+ (sirf standard library — koi pip package zaroori nahi)
- Playground ke liye browser

---

## Google / Vercel (viral)

SEO site `web/` mein hai — sitemap, robots, JSON-LD, Open Graph.

```text
Vercel → Import github.com/muaaziqbalvip/asaan-lang
Root Directory: web
```

Phir Search Console mein `https://asaan-lang.vercel.app/sitemap.xml` submit. Steps: [SEO.md](SEO.md)

Mizanora family: [web/ecosystem.html](https://asaan-lang.vercel.app/ecosystem)

## Cite / credit

Agar research, school, ya video mein use karein:

> Iqbal, Muaaz. (2026). *Asaan Lang: an Urdu/Roman-Urdu educational programming language*. MIT License. Kasur, Punjab, Pakistan.

See [CITATION.cff](CITATION.cff) and [AUTHORS](AUTHORS).

---

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) · Issues aur PRs welcome.

## License

[MIT](LICENSE) © 2026 **Muaaz Iqbal**

GitHub par daalne ke steps: **[PUBLISH.md](PUBLISH.md)**
