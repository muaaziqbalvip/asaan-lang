# Asaan Lang — Feature Dictionary

**Language:** Asaan Lang v1.1  
**Developer:** Muaaz Iqbal · Kasur, Punjab, Pakistan  
**License:** MIT

Index **1 se shuru** hota hai (`dost[1]` pehla item).

---

## 1. Chapna / Input

| Roman | اردو | Kaam | Misal |
|---|---|---|---|
| `likho` | `لکھو` | print (newline ke saath) | `likho "Salaam", 42` |
| `likhsath` | `لکھساتھ` | print, newline nahi | `likhsath "Score: "` |
| `lo` | `لو` | input (lafz) | `naam = lo "Naam? "` |

## 2. Faisla (if)

```asaan
agar number >= 90 to
    likho "A+"
aur agar number >= 50 to
    likho "Pass"
warna
    likho "Fail"
bas
```

| Roman | اردو |
|---|---|
| `agar … to` | `اگر … تو` |
| `aur agar` | `اور اگر` |
| `warna` | `ورنہ` |
| `bas` | `بس` |

Chain: `agar 1 < x < 10 to`

## 3. Loops

| Roman | اردو | Misal |
|---|---|---|
| `jabtak shart to … bas` | `جبتک` | while |
| `har i se 1 tak 10 to … bas` | `ہر … سے … تک` | inclusive range |
| `har i se 1 tak 10 qadam 2 to` | `قدم` | step |
| `har x andar list to` | `اندر` | foreach list/kitab/lafz |
| `dohrao 5 to … bas` | `دہراؤ` | repeat n times |
| `torho` | `توڑو` | break |
| `jaari` | `جاری` | continue |

## 4. Functions

```asaan
kaam salaam(naam = "Mehman")
    wapis "Khush Amdeed, " + naam
bas

likho salaam()
likho salaam("Fatima")
```

| Roman | اردو |
|---|---|
| `kaam naam(a, b = 1)` | `کام` |
| `wapis` | `واپس` |

## 5. Logic / values

| Roman | اردو | Matlab |
|---|---|---|
| `sach` `jhoot` | `سچ` `جھوٹ` | true / false |
| `khaali` | `خالی` | null |
| `aur` `ya` `nahi` | `اور` `یا` `نہیں` | and / or / not |
| `andar` | `اندر` | in (list, kitab, lafz) |

## 6. Fehrist (list)

```asaan
dost = ["Ali", "Fatima", "Ahmed"]
likho dost[1]          # Ali  (1-based)
shamil(dost, "Zainab")
nikaal(dost)
```

## 7. Kitab (dictionary)

```asaan
talib = {naam: "Ali", umar: 14, shehar: "Kasur"}
likho talib["naam"]
talib["grade"] = "A"
har k andar talib to
    likho k + " = " + talib[k]
bas
```

## 8. Hisab

`+  -  *  /  %  **`  
`+=  -=  *=  /=  %=`  
`==  !=  <  >  <=  >=`  
string + number khud jud jate hain: `"Jawab: " + 42`  
Urdu hindse: `۱۲۳`

## 9. Built-in functions

| Naam | اردو | Kaam |
|---|---|---|
| `adad(x)` | `عدد` | number banao |
| `lafz(x)` | `لفظ` | text banao |
| `lambai(x)` | `لمبائی` | length (lafz/list/kitab) |
| `shamil(list, x)` | `شامل` | append |
| `nikaal(list)` | `نکال` | pop |
| `mila(list, sep)` | `ملا` | join |
| `golo(n)` | `گولو` | round |
| `bari(s)` / `choti(s)` | `بڑی` / `چھوٹی` | upper / lower |
| `qisam(x)` | `قسم` | type name |
| `ittifaq()` / `ittifaq(6)` / `ittifaq(1,6)` | `اتفاق` | random |
| `chuno(list)` | `چنو` | random item |
| `quwwat(a,b)` | `قوت` | power (ya `**`) |
| `jazar(n)` | `جذر` | square root |
| `mutlaq(n)` | `مطلق` | abs |
| `kam(...)` / `zyada(...)` | `کم` / `زیادہ` | min / max |
| `baanto(s, ",")` | `بانتو` | split |
| `badlo(s, a, b)` | `بدلو` | replace |
| `hissa(s, 1, 3)` | `حصہ` | slice (1-based, inclusive) |
| `kunjiyan(kitab)` | `کنجیاں` | dict keys |
| `qadren(kitab)` | `قدریں` | dict values |
| `waqt()` | `وقت` | current date-time |
| `soja(n)` | `سوجا` | sleep (max 3s) |
| `parho("f.txt")` | `پڑھو` | read file |
| `likhdo("f.txt", t)` | `لکھدو` | write file |
| `jordo("f.txt", t)` | `جوڑدو` | append file |

## 10. Errors / modules

```asaan
koshish
    likho 10 / 0
pakro masla
    likho masla
bas

lao "lib_hisab.asaan"
```

| Roman | اردو |
|---|---|
| `koshish` / `pakro` | `کوشش` / `پکڑو` |
| `lao "file.asaan"` | `لاؤ` |
| `# comment` | comment |

## 11. Website compiler

```asaan
safha "Mera Site"
unwan "آسان لینگ"
para "Pakistan ki language"
card "Asaan", "10 minute mein shuru"
button "Playground", "/#studio"
footer "© 2026 Muaaz Iqbal"
```

| Command | Kaam |
|---|---|
| `safha` / `صفحہ` | page title |
| `unwan` `unwan2` | h1 / h2 |
| `para` | paragraph |
| `card` | card (auto grid) |
| `badge` | pill label |
| `button` `rabta` | links |
| `lakir` | hr |
| `code_dikhao` | code block (`"""` chalta hai) |
| `tasveer` | image |
| `peeche` `accent` | colors |
| `footer` | footer |

```bash
asaan --web examples/website.asaan -o site.html
```

## 12. CLI

```bash
asaan                     # REPL  (niklo se bahar)
asaan file.asaan          # run
asaan -e "likho 1+2"      # one-liner
asaan --web f.asaan -o o.html
asaan --studio            # playground :8080
asaan --version
asaan --home
asaan --help
```
