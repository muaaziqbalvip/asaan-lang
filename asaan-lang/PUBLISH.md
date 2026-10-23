# GitHub par publish — step by step

Asaan Lang ka source **pehle se tayyar** hai. Aap sirf GitHub par daalte hain.

Developer: **Muaaz Iqbal**

## 1) GitHub account

https://github.com/signup

## 2) Nayi empty repo banao

1. https://github.com/new
2. **Repository name:** `asaan-lang`
3. Public select karo
4. **README / License mat add karo** (humare files pehle se hain)
5. Create repository

## 3) Apne computer se push

GitHub jo commands dikhata hai, unki jagah yeh chalao (account: **muaaziqbalvip**):

```bash
cd asaan-lang

git init
git add .
git commit -m "Asaan Lang v1.1 by Muaaz Iqbal"
git branch -M main
git remote add origin https://github.com/muaaziqbalvip/asaan-lang.git
git push -u origin main
```

Agar GitHub SSH use karte ho:

```bash
git remote add origin git@github.com:muaaziqbalvip/asaan-lang.git
git push -u origin main
```

## 4) Repo settings (recommended)

- **About:** `Pakistan ki apni Urdu/Roman-Urdu programming language`
- Topics: `urdu` `pakistan` `programming-language` `education` `roman-urdu`
- LICENSE pehle se MIT hai — GitHub khud detect karega

## 5) Release + ZIP (optional)

GitHub → Releases → Draft a new release

- Tag: `v1.1.0`
- Title: `Asaan Lang v1.1.0 — Muaaz Iqbal`
- ZIP jo is project ke saath diya gaya hai, usay attach kar sakte ho
  (`Asaan-Lang-v1.1-Muaaz-Iqbal.zip`)

## 6) Logo / social preview (optional)

Settings → General → Social preview: koi 1280×640 image.

---

Push ke baad log aise use karenge:

```bash
git clone https://github.com/muaaziqbalvip/asaan-lang.git
cd asaan-lang
./install.sh          # Linux/Mac
# Windows: install.bat
asaan -e "likho \"Salaam, duniya!\""
```
