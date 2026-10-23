# Contribute to Asaan Lang

Developer / maintainer: **Muaaz Iqbal** (Kasur, Punjab, Pakistan)

Shukriya ke aap is language ko barhana chahte hain. Chhoti PRs welcome hain.

## Setup

```bash
git clone https://github.com/muaaziqbalvip/asaan-lang.git
cd asaan-lang
python3 asaan.py examples/hello.asaan
# ya
./install.sh
```

## Rules

1. Naye keyword ke **Roman-Urdu aur Urdu-script dono** aliases likho.
2. Error messages **Roman-Urdu** mein hon, line number ke saath.
3. `examples/` mein kam az kam 1 chalti misaal add karo.
4. Purane examples mat todo (`hello`, `ginti`, `kaam`, `urdu`, `website`).
5. Index **1-based** hi rehne do — yeh design faisla hai.

## PR bhejne se pehle

```bash
python3 asaan.py examples/hello.asaan
python3 asaan.py examples/kitab.asaan
python3 asaan.py examples/koshish.asaan
python3 asaan.py --web examples/website.asaan -o /tmp/site.html
```

Sawal? README padho, ya GitHub Issue kholo.
