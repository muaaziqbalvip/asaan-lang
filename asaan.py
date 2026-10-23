#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asaan Lang v1.1  🇵🇰
Pakistan ki apni ASAAN programming language.
Developer: Muaaz Iqbal  ·  Kasur, Punjab, Pakistan  ·  MIT License

usage:
    asaan                     interactive REPL
    asaan program.asaan       file chalao
    asaan -e "likho 1+2"      ek line (python -c ki tarah)
    asaan --web site.asaan -o site.html
    asaan --studio            playground browser mein
    asaan --version
    asaan --home              install folder
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import sys
import time
from datetime import datetime


def asaan_home() -> str:
    env = os.environ.get("ASAAN_HOME")
    if env:
        return env
    return os.path.dirname(os.path.abspath(__file__))


VERSION = "1.2"
AUTHOR = "Muaaz Iqbal"


class AsaanError(Exception):
    """Asaan zubaan mein ghalti ka paighaam."""


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


# ---------------- Lexer ----------------

KEYWORDS = {
    # Roman Urdu
    "likho": "PRINT", "likhsath": "PRINTNL", "lo": "INPUT",
    "agar": "IF", "warna": "ELSE", "bas": "END", "to": "TO",
    "jabtak": "WHILE", "har": "FOR", "se": "SE", "tak": "TAK",
    "qadam": "QADAM", "andar": "ANDAR",
    "dohrao": "REPEAT",
    "kaam": "FUNC", "wapis": "RETURN",
    "torho": "BREAK", "jaari": "CONTINUE",
    "koshish": "TRY", "pakro": "CATCH",
    "lao": "IMPORT",
    "aur": "AND", "ya": "OR", "nahi": "NOT",
    "sach": "TRUE", "jhoot": "FALSE", "khaali": "NONE",
    # Web
    "safha": "PAGE", "unwan": "HEADING", "unwan2": "HEADING2",
    "para": "PARA", "card": "CARD", "badge": "BADGE",
    "rabta": "LINK", "button": "BUTTON", "lakir": "HR",
    "code_dikhao": "CODEBLOCK", "footer": "FOOTER",
    "tasveer": "IMAGE", "peeche": "BG", "accent": "ACCENT",
    "wasf": "DESC", "lekhak": "AUTHOR", "link_web": "CANONICAL",
    # Urdu script
    "لکھو": "PRINT", "لکھساتھ": "PRINTNL", "لو": "INPUT",
    "اگر": "IF", "ورنہ": "ELSE", "بس": "END", "تو": "TO",
    "جبتک": "WHILE", "ہر": "FOR", "سے": "SE", "تک": "TAK",
    "قدم": "QADAM", "اندر": "ANDAR",
    "دہراؤ": "REPEAT",
    "کام": "FUNC", "واپس": "RETURN",
    "توڑو": "BREAK", "جاری": "CONTINUE",
    "کوشش": "TRY", "پکڑو": "CATCH",
    "لاؤ": "IMPORT",
    "اور": "AND", "یا": "OR", "نہیں": "NOT",
    "سچ": "TRUE", "جھوٹ": "FALSE", "خالی": "NONE",
    "صفحہ": "PAGE", "عنوان": "HEADING", "عنوان۲": "HEADING2",
    "پیرا": "PARA", "کارڈ": "CARD", "بیج": "BADGE",
    "رابطہ": "LINK", "بٹن": "BUTTON", "لکیر": "HR",
    "کوڈ": "CODEBLOCK", "فوٹر": "FOOTER",
    "وصف": "DESC", "لکھاری": "AUTHOR", "لنک_ویب": "CANONICAL",
    "تصویر": "IMAGE", "پیچھے": "BG", "نمایاں": "ACCENT",
}

TOKEN_RE = re.compile(
    r'(?P<MSTRING>"""[\s\S]*?""")'
    r"|(?P<MSTRING2>'''[\s\S]*?''')"
    r'|(?P<STRING>"(?:\\.|[^"\n])*")'
    r"|(?P<STRING2>'(?:\\.|[^'\n])*')"
    r"|(?P<NUMBER>\d+(?:\.\d+)?)"
    r"|(?P<OP>\*\*|==|!=|<=|>=|\+=|-=|\*=|/=|%=|[+\-*/%(),<>=\[\]{}:])"
    r"|(?P<NEWLINE>\n)"
    r"|(?P<SKIP>[ \t\r]+)"
    r"|(?P<COMMENT>\#[^\n]*)"
    r"|(?P<WORD>[^\W\d](?:\w|[\u200c\u200d])*)"
    r"|(?P<MISMATCH>.)",
    re.UNICODE,
)

URDU_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789",
)


def unescape(quoted: str) -> str:
    if quoted.startswith('"""') or quoted.startswith("'''"):
        inner = quoted[3:-3]
        if inner.startswith("\n"):
            inner = inner[1:]
    else:
        inner = quoted[1:-1]
    out = []
    i = 0
    while i < len(inner):
        if inner[i] == "\\" and i + 1 < len(inner):
            nxt = inner[i + 1]
            mapping = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'"}
            out.append(mapping.get(nxt, nxt))
            i += 2
        else:
            out.append(inner[i])
            i += 1
    return "".join(out)


def tokenize(code: str):
    tokens = []
    line = 1
    for m in TOKEN_RE.finditer(code):
        kind = m.lastgroup
        val = m.group()
        if kind == "NEWLINE":
            tokens.append(("NEWLINE", val, line))
            line += 1
        elif kind in ("SKIP", "COMMENT"):
            pass
        elif kind == "WORD":
            tokens.append((KEYWORDS.get(val, "IDENT"), val, line))
        elif kind == "MISMATCH":
            raise AsaanError(f"Ghalti line {line}: '{val}' samajh nahi aaya")
        else:
            tokens.append((kind, val, line))
            if kind in ("MSTRING", "MSTRING2"):
                line += val.count("\n")
    tokens.append(("EOF", "", line))
    return tokens


# ---------------- Parser ----------------

class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0

    def peek(self):
        return self.toks[self.pos]

    def lookahead(self, n=1):
        i = self.pos + n
        if i >= len(self.toks):
            return self.toks[-1]
        return self.toks[i]

    def advance(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t

    def at(self, typ, val=None):
        t = self.peek()
        if t[0] != typ:
            return False
        return val is None or t[1] == val

    def expect(self, typ, val=None, msg=""):
        t = self.peek()
        if t[0] != typ or (val is not None and t[1] != val):
            raise AsaanError(
                f"Ghalti line {t[2]}: {msg or ('umeed thi ' + repr(val or typ) + ', mila ' + repr(t[1]))}"
            )
        return self.advance()

    def skip_newlines(self):
        while self.at("NEWLINE"):
            self.advance()

    def is_elif(self):
        return self.at("AND") and self.lookahead()[0] == "IF"

    def stmt_end(self):
        t = self.peek()
        return t[0] in ("NEWLINE", "EOF", "END", "ELSE", "CATCH") or self.is_elif()

    def parse(self):
        stmts = []
        self.skip_newlines()
        while not self.at("EOF"):
            stmts.append(self.statement())
            self.skip_newlines()
        return ("program", stmts)

    def block(self):
        stmts = []
        self.skip_newlines()
        while not (self.at("END") or self.at("ELSE") or self.at("CATCH") or self.at("EOF") or self.is_elif()):
            stmts.append(self.statement())
            self.skip_newlines()
        return stmts

    def arglist_optional(self, required=True):
        if self.stmt_end():
            if required:
                t = self.peek()
                raise AsaanError(f"Ghalti line {t[2]}: yahan koi value likhni chahiye thi")
            return []
        args = [self.expr()]
        while self.at("OP", ","):
            self.advance()
            args.append(self.expr())
        return args

    def statement(self):
        t = self.peek()
        if t[0] == "PRINT":
            self.advance()
            return ("print", self.arglist_optional(required=False), True)
        if t[0] == "PRINTNL":
            self.advance()
            return ("print", self.arglist_optional(required=False), False)
        if t[0] == "IF":
            return self.if_stmt()
        if t[0] == "WHILE":
            self.advance()
            cond = self.expr()
            self.expect("TO", msg="'jabtak' wali shart ke baad 'to' likhna zaroori hai")
            body = self.block()
            self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
            return ("while", cond, body)
        if t[0] == "FOR":
            return self.for_stmt()
        if t[0] == "REPEAT":
            self.advance()
            n = self.expr()
            self.expect("TO", msg="'dohrao 5 to' is tarah likho")
            body = self.block()
            self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
            return ("repeat", n, body)
        if t[0] == "TRY":
            return self.try_stmt()
        if t[0] == "IMPORT":
            self.advance()
            return ("import", self.expr())
        if t[0] == "FUNC":
            self.advance()
            name = self.expect("IDENT", msg="'kaam' ke baad naam likho")[1]
            self.expect("OP", "(", msg="naam ke baad ( ) lagao")
            params = []
            if not self.at("OP", ")"):
                params.append(self.param())
                while self.at("OP", ","):
                    self.advance()
                    params.append(self.param())
            self.expect("OP", ")", msg="bracket band karo )")
            seen_def = False
            for n, d in params:
                if d is not None:
                    seen_def = True
                elif seen_def:
                    raise AsaanError(f"Ghalti: '{n}' se pehle default value wale parameter aa chuke hain")
            body = self.block()
            self.expect("END", msg="yeh kaam 'bas' likh kar khatam karo")
            return ("func", name, params, body)
        if t[0] == "RETURN":
            self.advance()
            if self.stmt_end():
                return ("return", ("none",))
            return ("return", self.expr())
        if t[0] == "BREAK":
            self.advance()
            return ("break",)
        if t[0] == "CONTINUE":
            self.advance()
            return ("continue",)
        if t[0] in WEB_STMT:
            kind = WEB_STMT[t[0]]
            self.advance()
            required = kind not in ("lakir",)
            return ("web", kind, self.arglist_optional(required=required))

        node = self.expr()
        if self.at("OP", "="):
            self.advance()
            return ("store", node, self.expr())
        AUG = {"+=": "+", "-=": "-", "*=": "*", "/=": "/", "%=": "%"}
        if self.at("OP") and self.peek()[1] in AUG:
            op = AUG[self.advance()[1]]
            return ("augstore", node, op, self.expr())
        return ("expr", node)

    def param(self):
        name = self.expect("IDENT", msg="parameter ka naam likho")[1]
        if self.at("OP", "="):
            self.advance()
            return (name, self.expr())
        return (name, None)

    def try_stmt(self):
        self.advance()
        body = self.block()
        err_var = None
        catch_b = []
        if self.at("CATCH"):
            self.advance()
            if self.at("IDENT"):
                err_var = self.advance()[1]
            catch_b = self.block()
        self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
        return ("try", body, err_var, catch_b)

    def if_stmt(self):
        self.advance()
        branches = []
        cond = self.expr()
        self.expect("TO", msg="'agar' ke baad shart aur phir 'to' likho")
        branches.append((cond, self.block()))
        while self.is_elif():
            self.advance()
            self.advance()
            cond = self.expr()
            self.expect("TO", msg="'aur agar' ke baad shart aur phir 'to' likho")
            branches.append((cond, self.block()))
        else_b = []
        if self.at("ELSE"):
            self.advance()
            else_b = self.block()
        self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
        return ("if", branches, else_b)

    def for_stmt(self):
        self.advance()
        var = self.expect("IDENT", msg="'har' ke baad variable ka naam likho")[1]
        if self.at("ANDAR"):
            self.advance()
            it = self.expr()
            self.expect("TO", msg="'har x andar list to' is tarah likho")
            body = self.block()
            self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
            return ("foreach", var, it, body)
        self.expect("SE", msg="'har i se 1 tak 10 to' is tarah likho")
        start = self.expr()
        self.expect("TAK", msg="'har i se 1 tak 10 to' is tarah likho")
        end = self.expr()
        step = ("num", 1)
        if self.at("QADAM"):
            self.advance()
            step = self.expr()
        self.expect("TO", msg="aakhir mein 'to' likhna zaroori hai")
        body = self.block()
        self.expect("END", msg="yeh block 'bas' likh kar khatam karo")
        return ("for", var, start, end, step, body)

    def expr(self):
        return self.or_expr()

    def or_expr(self):
        node = self.and_expr()
        while self.at("OR"):
            self.advance()
            node = ("or", node, self.and_expr())
        return node

    def and_expr(self):
        node = self.not_expr()
        while self.at("AND"):
            self.advance()
            node = ("and", node, self.not_expr())
        return node

    def not_expr(self):
        if self.at("NOT"):
            self.advance()
            return ("not", self.not_expr())
        return self.cmp_expr()

    def cmp_expr(self):
        node = self.add_expr()
        if self.at("ANDAR"):
            self.advance()
            return ("in", node, self.add_expr())
        comps = ("==", "!=", "<", ">", "<=", ">=")
        if not (self.at("OP") and self.peek()[1] in comps):
            return node
        parts = []
        while self.at("OP") and self.peek()[1] in comps:
            op = self.advance()[1]
            right = self.add_expr()
            parts.append((op, right))
        if len(parts) == 1:
            return ("bin", parts[0][0], node, parts[0][1])
        return ("chain", node, parts)

    def add_expr(self):
        node = self.mul_expr()
        while self.at("OP") and self.peek()[1] in ("+", "-"):
            op = self.advance()[1]
            node = ("bin", op, node, self.mul_expr())
        return node

    def mul_expr(self):
        node = self.pow_expr()
        while self.at("OP") and self.peek()[1] in ("*", "/", "%"):
            op = self.advance()[1]
            node = ("bin", op, node, self.pow_expr())
        return node

    def pow_expr(self):
        node = self.unary()
        if self.at("OP", "**"):
            self.advance()
            node = ("bin", "**", node, self.pow_expr())
        return node

    def unary(self):
        if self.at("OP", "-"):
            self.advance()
            return ("neg", self.unary())
        return self.postfix(self.primary())

    def postfix(self, node):
        while self.at("OP", "["):
            self.advance()
            idx = self.expr()
            self.expect("OP", "]", msg="] band karo")
            node = ("index", node, idx)
        return node

    def primary(self):
        t = self.peek()
        if t[0] == "NUMBER":
            self.advance()
            num = t[1].translate(URDU_DIGITS)
            return ("num", float(num) if "." in num else int(num))
        if t[0] in ("STRING", "STRING2", "MSTRING", "MSTRING2"):
            self.advance()
            return ("str", unescape(t[1]))
        if t[0] == "TRUE":
            self.advance()
            return ("bool", True)
        if t[0] == "FALSE":
            self.advance()
            return ("bool", False)
        if t[0] == "NONE":
            self.advance()
            return ("none",)
        if t[0] == "INPUT":
            self.advance()
            nxt = self.peek()
            if nxt[0] in (
                "STRING", "STRING2", "MSTRING", "MSTRING2",
                "NUMBER", "IDENT", "TRUE", "FALSE", "NONE", "INPUT",
            ) or (nxt[0] == "OP" and nxt[1] == "("):
                return ("input", self.postfix(self.primary()))
            return ("input", ("str", ""))
        if t[0] == "IDENT":
            self.advance()
            if self.at("OP", "("):
                self.advance()
                args = []
                if not self.at("OP", ")"):
                    args.append(self.expr())
                    while self.at("OP", ","):
                        self.advance()
                        args.append(self.expr())
                self.expect("OP", ")", msg="bracket band karo )")
                return ("call", t[1], args)
            return ("var", t[1])
        if t[0] == "OP" and t[1] == "(":
            self.advance()
            node = self.expr()
            self.expect("OP", ")", msg="bracket band karo )")
            return node
        if t[0] == "OP" and t[1] == "[":
            self.advance()
            items = []
            if not self.at("OP", "]"):
                items.append(self.expr())
                while self.at("OP", ","):
                    self.advance()
                    items.append(self.expr())
            self.expect("OP", "]", msg="] band karo")
            return ("list", items)
        if t[0] == "OP" and t[1] == "{":
            self.advance()
            pairs = []
            if not self.at("OP", "}"):
                pairs.append(self.dict_item())
                while self.at("OP", ","):
                    self.advance()
                    if self.at("OP", "}"):
                        break
                    pairs.append(self.dict_item())
            self.expect("OP", "}", msg="} band karo")
            return ("dict", pairs)
        raise AsaanError(f"Ghalti line {t[2]}: '{t[1]}' yahan samajh nahi aaya")

    def dict_item(self):
        if self.at("IDENT") and self.lookahead()[0] == "OP" and self.lookahead()[1] == ":":
            key = ("str", self.advance()[1])
        else:
            key = self.expr()
        self.expect("OP", ":", msg="kitab mein key ke baad : lagao, masalan {naam: \"Ali\"}")
        return (key, self.expr())


WEB_STMT = {
    "PAGE": "safha",
    "HEADING": "unwan",
    "HEADING2": "unwan2",
    "PARA": "para",
    "CARD": "card",
    "BADGE": "badge",
    "LINK": "rabta",
    "BUTTON": "button",
    "HR": "lakir",
    "CODEBLOCK": "code_dikhao",
    "FOOTER": "footer",
    "IMAGE": "tasveer",
    "BG": "peeche",
    "ACCENT": "accent",
    "DESC": "wasf",
    "AUTHOR": "lekhak",
    "CANONICAL": "link_web",
}


# ---------------- Runtime helpers ----------------

def is_true(v):
    if v is None or v is False:
        return False
    if v == 0 or v == "":
        return False
    if v == [] or v == {}:
        return False
    return True


def show(v):
    if v is True:
        return "sach"
    if v is False:
        return "jhoot"
    if v is None:
        return "khaali"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    if isinstance(v, dict):
        inner = ", ".join(show(k) + ": " + show(val) for k, val in v.items())
        return "{" + inner + "}"
    return str(v)


def qisam_name(v):
    if v is None:
        return "khaali"
    if isinstance(v, bool):
        return "sach-jhoot"
    if isinstance(v, (int, float)):
        return "adad"
    if isinstance(v, str):
        return "lafz"
    if isinstance(v, list):
        return "fehrist"
    if isinstance(v, dict):
        return "kitab"
    return "maloom-nahi"


def html_esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class WebBuilder:
    def __init__(self):
        self.active = False
        self.title = "Asaan Safha"
        self.bg = "#07140f"
        self.accent = "#3dd68c"
        self.parts = []
        self._cards = []
        self.footer_text = ""
        self.description = "Asaan Lang se bani website — Muaaz Iqbal / Mizanora"
        self.author = "Muaaz Iqbal"
        self.canonical = ""

    def flush_cards(self):
        if self._cards:
            self.parts.append(("cards", list(self._cards)))
            self._cards = []

    def add(self, kind, args):
        self.active = True
        if kind == "safha":
            self.title = show(args[0]) if args else self.title
            return
        if kind == "peeche":
            self.bg = show(args[0]) if args else self.bg
            return
        if kind == "accent":
            self.accent = show(args[0]) if args else self.accent
            return
        if kind == "wasf":
            self.description = show(args[0]) if args else self.description
            return
        if kind == "lekhak":
            self.author = show(args[0]) if args else self.author
            return
        if kind == "link_web":
            self.canonical = show(args[0]) if args else self.canonical
            return
        if kind == "card":
            title = show(args[0]) if args else ""
            body = show(args[1]) if len(args) > 1 else ""
            self._cards.append((title, body))
            return
        if kind == "footer":
            self.flush_cards()
            self.footer_text = show(args[0]) if args else ""
            return
        self.flush_cards()
        self.parts.append((kind, args))

    def render(self):
        self.flush_cards()
        accent = html_esc(self.accent)
        bg = html_esc(self.bg)
        body_parts = []
        for kind, args in self.parts:
            if kind == "unwan":
                body_parts.append(f'<h1 class="hero">{html_esc(show(args[0]))}</h1>')
            elif kind == "unwan2":
                body_parts.append(f"<h2>{html_esc(show(args[0]))}</h2>")
            elif kind == "para":
                body_parts.append(f"<p class='lead'>{html_esc(show(args[0]))}</p>")
            elif kind == "badge":
                body_parts.append(f"<span class='badge'>{html_esc(show(args[0]))}</span>")
            elif kind == "lakir":
                body_parts.append("<hr/>")
            elif kind == "code_dikhao":
                body_parts.append(f"<pre class='code'>{html_esc(show(args[0]))}</pre>")
            elif kind == "rabta":
                text = html_esc(show(args[0]))
                href = html_esc(show(args[1])) if len(args) > 1 else "#"
                top = ' target="_top"' if show(args[1] if len(args) > 1 else "#").startswith("/") else ""
                body_parts.append(f'<p><a class="link" href="{href}"{top}>{text}</a></p>')
            elif kind == "button":
                text = html_esc(show(args[0]))
                href = html_esc(show(args[1])) if len(args) > 1 else "#"
                top = ' target="_top"' if show(args[1] if len(args) > 1 else "#").startswith("/") else ""
                body_parts.append(f'<p><a class="btn" href="{href}"{top}>{text}</a></p>')
            elif kind == "tasveer":
                src = html_esc(show(args[0]))
                alt = html_esc(show(args[1])) if len(args) > 1 else ""
                body_parts.append(f'<img class="pic" src="{src}" alt="{alt}"/>')
            elif kind == "cards":
                cards = []
                for title, body in args:
                    cards.append(
                        f'<article class="card"><h3>{html_esc(title)}</h3>'
                        f"<p>{html_esc(body)}</p></article>"
                    )
                body_parts.append('<div class="grid">' + "".join(cards) + "</div>")
        footer = ""
        if self.footer_text:
            footer = f"<footer>{html_esc(self.footer_text)}</footer>"
        desc = html_esc(self.description)
        author = html_esc(self.author)
        canon = html_esc(self.canonical)
        canon_tag = f'<link rel="canonical" href="{canon}"/>' if canon else ""
        og_url = f'<meta property="og:url" content="{canon}"/>' if canon else ""
        ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": self.title,
            "description": self.description,
            "author": {"@type": "Person", "name": self.author, "url": "https://mizanora.vercel.app"},
            "inLanguage": "ur",
        }
        if canon:
            ld["url"] = self.canonical
        ld_json = json.dumps(ld, ensure_ascii=False)
        return f"""<!DOCTYPE html>
<html lang="ur">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html_esc(self.title)}</title>
<meta name="description" content="{desc}"/>
<meta name="author" content="{author}"/>
<meta name="robots" content="index,follow"/>
<meta property="og:title" content="{html_esc(self.title)}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="website"/>
<meta name="twitter:card" content="summary_large_image"/>
{canon_tag}
{og_url}
<script type="application/ld+json">{ld_json}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&family=Syne:wght@700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root {{ --accent: {accent}; --bg: {bg}; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  min-height: 100vh;
  font-family: "IBM Plex Sans", "Noto Nastaliq Urdu", system-ui, sans-serif;
  background:
    radial-gradient(1200px 700px at 10% -10%, #0b3d2e 0%, transparent 55%),
    radial-gradient(900px 500px at 110% 10%, #1a4d2e55 0%, transparent 50%),
    var(--bg);
  color: #e8f6ee;
  line-height: 1.7;
}}
body::before {{
  content: "";
  position: fixed; inset: 0; pointer-events: none; opacity: .07;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='72' height='72'><path fill='%233dd68c' d='M36 4 L40 28 L64 36 L40 44 L36 68 L32 44 L8 36 L32 28 Z'/></svg>");
}}
.wrap {{ max-width: 920px; margin: 0 auto; padding: 72px 24px 48px; position: relative; }}
.hero {{
  font-family: "Noto Nastaliq Urdu", "Syne", serif;
  font-size: clamp(2.4rem, 7vw, 4.6rem);
  line-height: 1.45;
  color: #f7ffe9;
  text-shadow: 0 10px 40px #0008;
  margin: 12px 0 8px;
}}
h2 {{
  font-family: "Syne", sans-serif;
  font-size: 1.6rem;
  margin: 42px 0 12px;
  color: var(--accent);
  letter-spacing: .02em;
}}
.lead {{ font-size: 1.15rem; max-width: 62ch; color: #cfe7d8; margin: 10px 0 22px; }}
.badge {{
  display: inline-block;
  border: 1px solid color-mix(in srgb, var(--accent) 70%, white 10%);
  color: var(--accent);
  padding: 4px 12px;
  border-radius: 999px;
  font-size: .78rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  background: #0c241b;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 28px 0;
}}
.card {{
  background: linear-gradient(180deg, #123528cc, #0a1f16ee);
  border: 1px solid #2a6a4d66;
  border-radius: 18px;
  padding: 22px 20px;
  box-shadow: 0 20px 50px #0005;
}}
.card h3 {{ font-family: "Syne", "Noto Nastaliq Urdu", sans-serif; font-size: 1.25rem; color: #f4ffe8; margin-bottom: 8px; }}
.card p {{ color: #c5ddcf; font-size: .98rem; }}
.code {{
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  background: #07110c;
  border: 1px solid #1e4a36;
  border-left: 4px solid var(--accent);
  border-radius: 12px;
  padding: 18px 20px;
  overflow: auto;
  color: #d6ffe8;
  margin: 12px 0 24px;
  white-space: pre-wrap;
}}
.btn {{
  display: inline-block;
  background: var(--accent);
  color: #062015 !important;
  font-weight: 700;
  text-decoration: none;
  padding: 12px 22px;
  border-radius: 999px;
  margin: 8px 8px 8px 0;
  box-shadow: 0 10px 30px color-mix(in srgb, var(--accent) 40%, transparent);
}}
.link {{ color: var(--accent); font-weight: 600; }}
.pic {{ max-width: 100%; border-radius: 16px; margin: 12px 0; border: 1px solid #2a6a4d66; }}
hr {{ border: 0; border-top: 1px solid #2a6a4d66; margin: 32px 0; }}
footer {{ margin-top: 56px; color: #8eaea0; font-size: .9rem; border-top: 1px solid #1e4a36; padding-top: 18px; }}
</style>
</head>
<body>
  <div class="wrap">
    {''.join(body_parts)}
    {footer}
  </div>
</body>
</html>
"""


class Env:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise AsaanError(f"Ghalti: '{name}' naam ki koi cheez nahi mili (pehle banao, phir use karo)")

    def set(self, name, val):
        self.vars[name] = val


def _as_index(obj, idx):
    if not isinstance(obj, (list, str)):
        raise AsaanError(f"Ghalti: '{show(obj)}' par index nahi lag sakta (fehrist ya lafz do)")
    if isinstance(idx, bool) or not isinstance(idx, (int, float)) or int(idx) != idx:
        raise AsaanError("Ghalti: index poora number hona chahiye (Asaan Lang mein pehla item 1 hai)")
    i = int(idx)
    n = len(obj)
    if n == 0:
        raise AsaanError("Ghalti: fehrist/lafz khaali hai")
    if i < 1 or i > n:
        raise AsaanError(f"Ghalti: index {i} galat hai — 1 se {n} tak do (pehla item 1 hota hai)")
    return i - 1


def _getitem(obj, idx):
    if isinstance(obj, dict):
        if idx in obj:
            return obj[idx]
        if isinstance(idx, str) is False:
            s = show(idx)
            if s in obj:
                return obj[s]
        raise AsaanError(f"Ghalti: kitab mein '{show(idx)}' wali kunji nahi mili")
    return obj[_as_index(obj, idx)]


def _setitem(obj, idx, val):
    if isinstance(obj, dict):
        obj[idx] = val
        return
    if isinstance(obj, list):
        obj[_as_index(obj, idx)] = val
        return
    raise AsaanError("Ghalti: lafz (string) ke andar seedha badlav nahi ho sakta")


def _num(v, name):
    try:
        if isinstance(v, bool):
            raise TypeError
        return float(v)
    except (TypeError, ValueError):
        raise AsaanError(f"Ghalti: '{name}' ke liye number do")


def _safe_rel_file(name, source_dir=None):
    name = str(name).strip()
    if not name:
        raise AsaanError("Ghalti: file ka naam khaali hai")
    base = os.path.basename(name.replace("\\", "/"))
    if not base or base in (".", ".."):
        raise AsaanError("Ghalti: galat file naam")
    dirs = []
    if source_dir:
        dirs.append(source_dir)
    dirs.append(os.getcwd())
    dirs.append(os.path.join(asaan_home(), "examples"))
    return base, dirs


def _builtin_adad(args):
    if len(args) != 1:
        raise AsaanError('Ghalti: \'adad\' ko 1 cheez do, masalan adad("25")')
    v = args[0]
    if isinstance(v, bool):
        return 1 if v else 0
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip().translate(URDU_DIGITS)
    try:
        return int(s) if "." not in s else float(s)
    except ValueError:
        raise AsaanError(f"Ghalti: '{args[0]}' adad (number) nahi hai")


def _builtin_lafz(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: 'lafz' ko 1 cheez do")
    return show(args[0])


def _builtin_lambai(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: 'lambai' ko 1 cheez do")
    v = args[0]
    if isinstance(v, (str, list, dict)):
        return len(v)
    raise AsaanError("Ghalti: 'lambai' sirf lafz, fehrist ya kitab ki hoti hai")


def _builtin_shamil(args):
    if len(args) != 2:
        raise AsaanError("Ghalti: shamil(fehrist, cheez) — 2 cheezein do")
    lst, item = args
    if not isinstance(lst, list):
        raise AsaanError("Ghalti: 'shamil' ke liye pehli cheez fehrist honi chahiye")
    lst.append(item)
    return lst


def _builtin_nikaal(args):
    if len(args) not in (1, 2):
        raise AsaanError("Ghalti: nikaal(fehrist) ya nikaal(fehrist, index)")
    lst = args[0]
    if not isinstance(lst, list):
        raise AsaanError("Ghalti: 'nikaal' ke liye fehrist do")
    if not lst:
        raise AsaanError("Ghalti: khaali fehrist se nikaal nahi ho sakta")
    if len(args) == 1:
        return lst.pop()
    i = _as_index(lst, args[1])
    return lst.pop(i)


def _builtin_mila(args):
    if len(args) not in (1, 2):
        raise AsaanError("Ghalti: mila(fehrist) ya mila(fehrist, jorne_wala)")
    lst = args[0]
    sep = show(args[1]) if len(args) == 2 else ""
    if not isinstance(lst, list):
        raise AsaanError("Ghalti: 'mila' ke liye fehrist do")
    return sep.join(show(x) for x in lst)


def _builtin_golo(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: golo(number)")
    try:
        return round(float(args[0]))
    except (TypeError, ValueError):
        raise AsaanError("Ghalti: golo ke liye number do")


def _builtin_bari(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: bari(lafz)")
    return show(args[0]).upper()


def _builtin_choti(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: choti(lafz)")
    return show(args[0]).lower()


def _builtin_qisam(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: qisam(cheez)")
    return qisam_name(args[0])


def _builtin_ittifaq(args):
    if len(args) == 0:
        return random.random()
    if len(args) == 1:
        b = int(_num(args[0], "ittifaq"))
        if b < 1:
            raise AsaanError("Ghalti: ittifaq(n) mein n kam az kam 1 ho")
        return random.randint(1, b)
    if len(args) == 2:
        a, b = int(_num(args[0], "ittifaq")), int(_num(args[1], "ittifaq"))
        if a > b:
            a, b = b, a
        return random.randint(a, b)
    raise AsaanError("Ghalti: ittifaq() ya ittifaq(6) ya ittifaq(1, 6)")


def _builtin_chuno(args):
    if len(args) != 1 or not isinstance(args[0], list) or not args[0]:
        raise AsaanError("Ghalti: chuno(fehrist) — khaali fehrist nahi")
    return random.choice(args[0])


def _builtin_quwwat(args):
    if len(args) != 2:
        raise AsaanError("Ghalti: quwwat(a, b) masalan quwwat(2, 8)")
    return _num(args[0], "quwwat") ** _num(args[1], "quwwat")


def _builtin_jazar(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: jazar(number)")
    n = _num(args[0], "jazar")
    if n < 0:
        raise AsaanError("Ghalti: manfi number ka jazar nahi")
    r = math.sqrt(n)
    return int(r) if r.is_integer() else r


def _builtin_mutlaq(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: mutlaq(number)")
    return abs(_num(args[0], "mutlaq"))


def _builtin_kam(args):
    if not args:
        raise AsaanError("Ghalti: kam(...) ke liye numbers/fehrist do")
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    try:
        return min(args)
    except TypeError:
        raise AsaanError("Ghalti: kam() in cheezon ka muqabla nahi kar sakta")


def _builtin_zyada(args):
    if not args:
        raise AsaanError("Ghalti: zyada(...) ke liye numbers/fehrist do")
    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]
    try:
        return max(args)
    except TypeError:
        raise AsaanError("Ghalti: zyada() in cheezon ka muqabla nahi kar sakta")


def _builtin_baanto(args):
    if len(args) not in (1, 2) or not isinstance(args[0], str):
        raise AsaanError("Ghalti: baanto(lafz) ya baanto(lafz, \",\")")
    sep = args[1] if len(args) == 2 else None
    if sep is None:
        return args[0].split()
    return args[0].split(str(sep))


def _builtin_badlo(args):
    if len(args) != 3:
        raise AsaanError("Ghalti: badlo(lafz, purana, naya)")
    return show(args[0]).replace(show(args[1]), show(args[2]))


def _builtin_hissa(args):
    if len(args) not in (2, 3):
        raise AsaanError("Ghalti: hissa(cheez, shuru) ya hissa(cheez, shuru, akhir)")
    obj = args[0]
    if not isinstance(obj, (list, str)):
        raise AsaanError("Ghalti: hissa sirf fehrist/lafz par")
    a = int(_num(args[1], "hissa"))
    b = int(_num(args[2], "hissa")) if len(args) == 3 else len(obj)
    i = _as_index(obj, a)
    j = _as_index(obj, b)
    if j < i:
        i, j = j, i
    return obj[i : j + 1]


def _builtin_kunjiyan(args):
    if len(args) != 1 or not isinstance(args[0], dict):
        raise AsaanError("Ghalti: kunjiyan(kitab)")
    return list(args[0].keys())


def _builtin_qadren(args):
    if len(args) != 1 or not isinstance(args[0], dict):
        raise AsaanError("Ghalti: qadren(kitab)")
    return list(args[0].values())


def _builtin_waqt(args):
    if args:
        raise AsaanError("Ghalti: waqt() — khali brackets")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _builtin_soja(args):
    if len(args) != 1:
        raise AsaanError("Ghalti: soja(seconds)")
    n = _num(args[0], "soja")
    if n < 0:
        n = 0
    if n > 3:
        n = 3
    time.sleep(n)
    return n


def _make_file_builtins(interp):
    def parho(args):
        if len(args) != 1:
            raise AsaanError("Ghalti: parho(\"file.txt\")")
        base, dirs = _safe_rel_file(args[0], interp.source_dir)
        for d in dirs:
            p = os.path.join(d, base)
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as f:
                    return f.read()
        raise AsaanError(f"Ghalti: file nahi mili: {base}")

    def likhdo(args):
        if len(args) != 2:
            raise AsaanError("Ghalti: likhdo(\"file.txt\", text)")
        base, dirs = _safe_rel_file(args[0], interp.source_dir)
        p = os.path.join(dirs[0] if dirs else os.getcwd(), base)
        with open(p, "w", encoding="utf-8") as f:
            f.write(show(args[1]))
        return p

    def jordo(args):
        if len(args) != 2:
            raise AsaanError("Ghalti: jordo(\"file.txt\", text)")
        base, dirs = _safe_rel_file(args[0], interp.source_dir)
        p = os.path.join(dirs[0] if dirs else os.getcwd(), base)
        with open(p, "a", encoding="utf-8") as f:
            f.write(show(args[1]))
        return p

    return {
        "parho": parho, "پڑھو": parho,
        "likhdo": likhdo, "لکھدو": likhdo,
        "jordo": jordo, "جوڑدو": jordo,
    }


STATIC_BUILTINS = {
    "adad": _builtin_adad, "عدد": _builtin_adad,
    "lafz": _builtin_lafz, "لفظ": _builtin_lafz,
    "lambai": _builtin_lambai, "لمبائی": _builtin_lambai,
    "shamil": _builtin_shamil, "شامل": _builtin_shamil,
    "nikaal": _builtin_nikaal, "نکال": _builtin_nikaal,
    "mila": _builtin_mila, "ملا": _builtin_mila,
    "golo": _builtin_golo, "گولو": _builtin_golo,
    "bari": _builtin_bari, "بڑی": _builtin_bari,
    "choti": _builtin_choti, "چھوٹی": _builtin_choti,
    "qisam": _builtin_qisam, "قسم": _builtin_qisam,
    "ittifaq": _builtin_ittifaq, "اتفاق": _builtin_ittifaq,
    "chuno": _builtin_chuno, "چنو": _builtin_chuno,
    "quwwat": _builtin_quwwat, "قوت": _builtin_quwwat,
    "jazar": _builtin_jazar, "جذر": _builtin_jazar,
    "mutlaq": _builtin_mutlaq, "مطلق": _builtin_mutlaq,
    "kam": _builtin_kam, "کم": _builtin_kam,
    "zyada": _builtin_zyada, "زیادہ": _builtin_zyada,
    "baanto": _builtin_baanto, "بانتو": _builtin_baanto,
    "badlo": _builtin_badlo, "بدلو": _builtin_badlo,
    "hissa": _builtin_hissa, "حصہ": _builtin_hissa,
    "kunjiyan": _builtin_kunjiyan, "کنجیاں": _builtin_kunjiyan,
    "qadren": _builtin_qadren, "قدریں": _builtin_qadren,
    "waqt": _builtin_waqt, "وقت": _builtin_waqt,
    "soja": _builtin_soja, "سوجا": _builtin_soja,
}


class Interpreter:
    def __init__(self, input_fn=None, output_fn=None, max_steps=200_000, source_dir=None):
        self.global_env = Env()
        self.functions = {}
        self.input_fn = input_fn or input
        self.output_fn = output_fn or (lambda s, end="\n": print(s, end=end, flush=True))
        self.web = WebBuilder()
        self.steps = 0
        self.max_steps = max_steps
        self.source_dir = source_dir or os.getcwd()
        self.loaded = set()
        self.builtins = dict(STATIC_BUILTINS)
        self.builtins.update(_make_file_builtins(self))

    def tick(self):
        self.steps += 1
        if self.steps > self.max_steps:
            raise AsaanError("Ghalti: program bahut lamba chal gaya (shayad infinite loop hai?)")

    def run(self, node, env=None):
        env = env or self.global_env
        self.tick()
        kind = node[0]
        if kind == "program":
            for s in node[1]:
                self.run(s, env)
        elif kind == "print":
            parts = [show(self.eval(a, env)) for a in node[1]]
            nl = node[2] if len(node) > 2 else True
            self.output_fn(" ".join(parts), end="\n" if nl else "")
        elif kind == "store":
            self.store(node[1], self.eval(node[2], env), env)
        elif kind == "augstore":
            _, target, op, right = node
            cur = self.eval(target, env)
            self.store(target, self.apply(op, cur, self.eval(right, env)), env)
        elif kind == "expr":
            self.eval(node[1], env)
        elif kind == "repeat":
            _, nnode, body = node
            n = int(self.eval(nnode, env))
            if n < 0:
                raise AsaanError("Ghalti: dohrao ke liye 0 ya us se bara number do")
            for _ in range(n):
                self.tick()
                try:
                    for s in body:
                        self.run(s, env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
        elif kind == "try":
            _, body, err_var, catch_b = node
            try:
                for s in body:
                    self.run(s, env)
            except AsaanError as e:
                if err_var:
                    env.set(err_var, str(e))
                if not catch_b:
                    raise
                for s in catch_b:
                    self.run(s, env)
        elif kind == "import":
            self._import_file(self.eval(node[1], env), env)
        elif kind == "if":
            _, branches, else_b = node
            ran = False
            for cond, body in branches:
                if is_true(self.eval(cond, env)):
                    for s in body:
                        self.run(s, env)
                    ran = True
                    break
            if not ran:
                for s in else_b:
                    self.run(s, env)
        elif kind == "while":
            _, cond, body = node
            while is_true(self.eval(cond, env)):
                self.tick()
                try:
                    for s in body:
                        self.run(s, env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
        elif kind == "for":
            _, var, start, end, step, body = node
            s = int(self.eval(start, env))
            e = int(self.eval(end, env))
            st = int(self.eval(step, env))
            if st == 0:
                raise AsaanError("Ghalti: qadam 0 nahi ho sakta")
            i = s
            cmp = (lambda a, b: a <= b) if st > 0 else (lambda a, b: a >= b)
            while cmp(i, e):
                self.tick()
                env.set(var, i)
                try:
                    for stmt in body:
                        self.run(stmt, env)
                except ContinueSignal:
                    i += st
                    continue
                except BreakSignal:
                    break
                i += st
        elif kind == "foreach":
            _, var, it, body = node
            seq = self.eval(it, env)
            if isinstance(seq, dict):
                seq = list(seq.keys())
            elif isinstance(seq, str):
                seq = list(seq)
            if not isinstance(seq, list):
                raise AsaanError("Ghalti: 'har x andar ...' ke liye fehrist, kitab ya lafz do")
            for item in seq:
                self.tick()
                env.set(var, item)
                try:
                    for stmt in body:
                        self.run(stmt, env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
        elif kind == "func":
            self.functions[node[1]] = (node[2], node[3])
        elif kind == "return":
            raise ReturnSignal(self.eval(node[1], env))
        elif kind == "break":
            raise BreakSignal()
        elif kind == "continue":
            raise ContinueSignal()
        elif kind == "web":
            _, wkind, args = node
            vals = [self.eval(a, env) for a in args]
            self.web.add(wkind, vals)
        return None

    def store(self, target, val, env):
        if target[0] == "var":
            env.set(target[1], val)
            return
        if target[0] == "index":
            obj = self.eval(target[1], env)
            idx = self.eval(target[2], env)
            _setitem(obj, idx, val)
            return
        raise AsaanError("Ghalti: is jagah value rakh nahi sakte (variable ya fehrist[index] likho)")

    def _import_file(self, name, env):
        base, dirs = _safe_rel_file(name, self.source_dir)
        if not base.endswith(".asaan"):
            base_try = [base + ".asaan", base]
        else:
            base_try = [base]
        path = None
        for d in dirs:
            for b in base_try:
                p = os.path.join(d, b)
                if os.path.isfile(p):
                    path = os.path.abspath(p)
                    break
            if path:
                break
        if not path:
            raise AsaanError(f"Ghalti: lao ke liye file nahi mili: {base}")
        if path in self.loaded:
            return
        self.loaded.add(path)
        with open(path, encoding="utf-8") as f:
            code = f.read()
        old = self.source_dir
        self.source_dir = os.path.dirname(path)
        try:
            tree = Parser(tokenize(code)).parse()
            self.run(tree, env)
        finally:
            self.source_dir = old

    def eval(self, node, env):
        self.tick()
        kind = node[0]
        if kind == "num":
            return node[1]
        if kind == "str":
            return node[1]
        if kind == "bool":
            return node[1]
        if kind == "none":
            return None
        if kind == "list":
            return [self.eval(x, env) for x in node[1]]
        if kind == "dict":
            d = {}
            for k, v in node[1]:
                d[self.eval(k, env)] = self.eval(v, env)
            return d
        if kind == "chain":
            left = self.eval(node[1], env)
            for op, right_node in node[2]:
                right = self.eval(right_node, env)
                if not is_true(self.apply(op, left, right)):
                    return False
                left = right
            return True
        if kind == "var":
            return env.get(node[1])
        if kind == "input":
            prompt = self.eval(node[1], env)
            prompt = "" if prompt is None else str(prompt)
            try:
                return self.input_fn(prompt)
            except EOFError:
                raise AsaanError("Ghalti: input khatam ho gaya")
        if kind == "neg":
            return -self.eval(node[1], env)
        if kind == "not":
            return not is_true(self.eval(node[1], env))
        if kind == "or":
            l = self.eval(node[1], env)
            return l if is_true(l) else self.eval(node[2], env)
        if kind == "and":
            l = self.eval(node[1], env)
            return self.eval(node[2], env) if is_true(l) else l
        if kind == "in":
            a = self.eval(node[1], env)
            b = self.eval(node[2], env)
            if isinstance(b, list):
                return a in b
            if isinstance(b, dict):
                return a in b
            if isinstance(b, str):
                return show(a) in b
            raise AsaanError("Ghalti: 'andar' ke liye fehrist, kitab ya lafz do")
        if kind == "bin":
            _, op, l, r = node
            return self.apply(op, self.eval(l, env), self.eval(r, env))
        if kind == "index":
            return _getitem(self.eval(node[1], env), self.eval(node[2], env))
        if kind == "call":
            _, name, args = node
            vals = [self.eval(a, env) for a in args]
            if name in self.builtins:
                return self.builtins[name](vals)
            if name not in self.functions:
                raise AsaanError(f"Ghalti: '{name}' naam ka koi kaam (function) nahi mila")
            params, body = self.functions[name]
            required = sum(1 for p in params if p[1] is None)
            if len(vals) < required or len(vals) > len(params):
                raise AsaanError(
                    f"Ghalti: '{name}' ko {required} se {len(params)} cheezein chahiye, {len(vals)} milein"
                )
            fenv = Env(self.global_env)
            for i, (p, default) in enumerate(params):
                if i < len(vals):
                    fenv.set(p, vals[i])
                else:
                    fenv.set(p, self.eval(default, env))
            try:
                for s in body:
                    self.run(s, fenv)
            except ReturnSignal as rs:
                return rs.value
            return None
        raise AsaanError("Ghalti: androoni masla " + kind)

    def apply(self, op, a, b):
        try:
            if op == "+":
                if isinstance(a, list) and isinstance(b, list):
                    return a + b
                if isinstance(a, dict) and isinstance(b, dict):
                    merged = dict(a)
                    merged.update(b)
                    return merged
                if isinstance(a, str) or isinstance(b, str):
                    return show(a) + show(b)
                return a + b
            if op == "**":
                return a ** b
            if op == "-":
                return a - b
            if op == "*":
                if isinstance(a, str) and isinstance(b, (int, float)) and not isinstance(b, bool):
                    return a * int(b)
                if isinstance(b, str) and isinstance(a, (int, float)) and not isinstance(a, bool):
                    return b * int(a)
                if isinstance(a, list) and isinstance(b, (int, float)) and not isinstance(b, bool):
                    return a * int(b)
                return a * b
            if op == "/":
                return a / b
            if op == "%":
                return a % b
            if op == "==":
                return a == b
            if op == "!=":
                return a != b
            if op == "<":
                return a < b
            if op == ">":
                return a > b
            if op == "<=":
                return a <= b
            if op == ">=":
                return a >= b
        except TypeError:
            raise AsaanError(f"Ghalti: '{show(a)}' aur '{show(b)}' par '{op}' nahi lag sakta")
        except ZeroDivisionError:
            raise AsaanError("Ghalti: sifar (0) se taqseem nahi ho sakti!")


def run_code(code, interp=None, source_path=None):
    interp = interp or Interpreter(
        source_dir=os.path.dirname(os.path.abspath(source_path)) if source_path else os.getcwd()
    )
    if source_path:
        interp.source_dir = os.path.dirname(os.path.abspath(source_path))
    try:
        tree = Parser(tokenize(code)).parse()
        interp.run(tree)
    except ReturnSignal:
        raise AsaanError("'wapis' sirf 'kaam' ke andar use hota hai")
    except BreakSignal:
        raise AsaanError("'torho' sirf loop (har/jabtak) ke andar use hota hai")
    except ContinueSignal:
        raise AsaanError("'jaari' sirf loop (har/jabtak) ke andar use hota hai")
    return interp


def run_program(code, inputs=None, max_steps=200_000, source_path=None):
    """Playground/API ke liye: dict return karta hai."""
    out = []
    inputs = list(inputs or [])
    idx = [0]

    def input_fn(prompt=""):
        if prompt:
            out.append(prompt)
        if idx[0] >= len(inputs):
            raise AsaanError(
                "Ghalti: 'lo' ke liye input nahi mila. Playground ke Input box mein lines likho."
            )
        val = inputs[idx[0]]
        idx[0] += 1
        return val

    def output_fn(s, end="\n"):
        out.append("" if s is None else str(s))
        if end:
            out.append(end)

    src_dir = os.path.dirname(os.path.abspath(source_path)) if source_path else os.getcwd()
    interp = Interpreter(input_fn=input_fn, output_fn=output_fn, max_steps=max_steps, source_dir=src_dir)
    try:
        run_code(code, interp, source_path=source_path)
        if interp.web.active:
            interp.web.flush_cards()
        return {
            "ok": True,
            "output": "".join(out),
            "html": interp.web.render() if interp.web.active else "",
            "error": None,
            "version": VERSION,
        }
    except AsaanError as e:
        return {
            "ok": False,
            "output": "".join(out),
            "html": interp.web.render() if interp.web.active else "",
            "error": str(e),
            "version": VERSION,
        }


def _repl_open_blocks(toks):
    depth = 0
    for i, t in enumerate(toks):
        if t[0] in ("IF", "WHILE", "FOR", "FUNC", "REPEAT", "TRY"):
            if t[0] == "IF" and i > 0 and toks[i - 1][0] == "AND":
                continue
            depth += 1
        elif t[0] == "END":
            depth -= 1
    return depth


def repl():
    print(f"=== Asaan Lang v{VERSION}  🇵🇰  ·  {AUTHOR} ===")
    print("Urdu/Roman-Urdu mein code likho. Bahar nikalne ke liye 'niklo' likho.\n")
    interp = Interpreter()
    buf = []
    while True:
        try:
            line = input("asaan> " if not buf else "  ...> ")
        except (EOFError, KeyboardInterrupt):
            print("\nKhuda Hafiz! 👋")
            break
        if line.strip() == "niklo" and not buf:
            print("Khuda Hafiz! 👋")
            break
        buf.append(line)
        src = "\n".join(buf)
        try:
            toks = tokenize(src)
        except AsaanError as e:
            print("❌", e)
            buf = []
            continue
        if _repl_open_blocks(toks) > 0:
            continue
        buf = []
        if not src.strip():
            continue
        try:
            run_code(src, interp)
        except AsaanError as e:
            print("❌", e)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        repl()
        return
    if argv[0] in ("-h", "--help", "madad"):
        print(__doc__)
        return
    if argv[0] in ("--version", "-v"):
        print(f"Asaan Lang {VERSION} — {AUTHOR}")
        return
    if argv[0] in ("--home",):
        print(asaan_home())
        return
    if argv[0] in ("--studio", "studio"):
        from studio import main as studio_main
        studio_main()
        return
    if argv[0] in ("-e", "-c"):
        if len(argv) < 2:
            print("❌ -e ke baad code likho")
            return
        try:
            run_code(argv[1])
        except AsaanError as e:
            print("❌", e)
        return
    if argv[0] == "--web":
        if len(argv) < 2:
            print("❌ --web ke baad file.asaan likho")
            return
        path = argv[1]
        out_path = None
        if "-o" in argv:
            i = argv.index("-o")
            if i + 1 < len(argv):
                out_path = argv[i + 1]
        try:
            with open(path, encoding="utf-8") as f:
                code = f.read()
        except FileNotFoundError:
            print(f"❌ File nahi mili: {path}")
            return
        result = run_program(code, source_path=path)
        if not result["ok"]:
            print("❌", result["error"])
            return
        html = result["html"]
        if not html:
            print("❌ Is program ne koi website nahi banayi. 'safha' / 'unwan' / 'para' use karo.")
            if result["output"]:
                print(result["output"], end="")
            return
        if out_path:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ Website ban gayi: {out_path}")
        else:
            sys.stdout.write(html)
        return
    if argv[0] == "--json":
        payload = json.loads(sys.stdin.read() or "{}")
        print(json.dumps(run_program(payload.get("code", ""), payload.get("inputs") or []), ensure_ascii=False))
        return

    path = argv[0]
    try:
        with open(path, encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File nahi mili: {path}")
        return
    try:
        run_code(code, source_path=path)
    except AsaanError as e:
        print("❌", e)


if __name__ == "__main__":
    main()
