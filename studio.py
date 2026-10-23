#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asaan Studio — playground + website server.
Developer: Muaaz Iqbal  ·  python3 studio.py  /  asaan --studio
"""

from __future__ import annotations

import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

def _find_root() -> str:
    env = os.environ.get("ASAAN_HOME")
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        env,
        here,
        os.path.expanduser("~/.asaan-lang"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "AsaanLang"),
        "/usr/local/share/asaan-lang",
    ]
    for p in candidates:
        if p and os.path.isdir(os.path.join(p, "studio")) and os.path.isdir(os.path.join(p, "examples")):
            return p
    return here


ROOT = _find_root()
STUDIO_DIR = os.path.join(ROOT, "studio")
EXAMPLES_DIR = os.path.join(ROOT, "examples")

sys.path.insert(0, ROOT)
from asaan import run_program, VERSION  # noqa: E402

EXAMPLE_META = [
    ("hello.asaan", "Salaam Duniya", "Pehla program + naam poochna"),
    ("hisab.asaan", "Pass / Fail", "agar-warna se number check"),
    ("grades.asaan", "Grades", "aur agar (else-if) grades"),
    ("ginti.asaan", "Ginti + Pehara", "har loop se table"),
    ("fehrist.asaan", "Fehrist", "lists, andar, qadam"),
            ("kaam.asaan", "Kaam (functions)", "apne functions banao"),
            ("kitab.asaan", "Kitab (dict)", "naam, umar, shehar record"),
            ("dice.asaan", "Dice + dohrao", "ittifaq random + dohrao"),
            ("koshish.asaan", "Koshish / pakro", "ghalti pakarna"),
            ("guess.asaan", "Guess game", "random number guess"),
            ("urdu.asaan", "خالص اردو", "Urdu script mein program"),
    ("website.asaan", "🌐 Official Site", "Asaan Lang se website"),
    ("school.asaan", "🏫 Kasur Academy", "School site Asaan se"),
]


def read_example(name: str) -> str:
    safe = os.path.basename(name)
    path = os.path.join(EXAMPLES_DIR, safe)
    if not os.path.isfile(path):
        raise FileNotFoundError(safe)
    with open(path, encoding="utf-8") as f:
        return f.read()


class Handler(BaseHTTPRequestHandler):
    server_version = "AsaanStudio/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[studio] " + (fmt % args) + "\n")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        # Live preview iframe ke liye — embedding mat roko
        self.send_header("X-Content-Type-Options", "nosniff")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            return self._file(os.path.join(STUDIO_DIR, "index.html"), "text/html; charset=utf-8")
        web_dir = os.path.join(ROOT, "web")
        if path in ("/robots.txt", "/sitemap.xml", "/llms.txt", "/humans.txt", "/og.jpg", "/manifest.webmanifest"):
            fp = os.path.join(web_dir, path.lstrip("/"))
            if os.path.isfile(fp):
                mime, _ = mimetypes.guess_type(fp)
                if path.endswith(".xml"):
                    mime = "application/xml"
                if path.endswith(".txt"):
                    mime = "text/plain; charset=utf-8"
                return self._file(fp, mime or "application/octet-stream")
        if path in ("/seo", "/official"):
            return self._file(os.path.join(web_dir, "index.html"), "text/html; charset=utf-8")
        if path == "/api/health":
            return self._json({"ok": True, "version": VERSION, "name": "Asaan Lang"})
        if path == "/api/examples":
            items = []
            for file, title, blurb in EXAMPLE_META:
                items.append({"file": file, "title": title, "blurb": blurb})
            return self._json({"examples": items})
        if path == "/api/example":
            name = (qs.get("file") or [""])[0]
            try:
                code = read_example(name)
            except FileNotFoundError:
                return self._json({"error": "example nahi mila"}, 404)
            return self._json({"file": os.path.basename(name), "code": code})
        if path in ("/site", "/site.html"):
            return self._generated("website.asaan")
        if path in ("/school", "/school.html"):
            return self._generated("school.asaan")

        # static from studio/
        rel = path.lstrip("/")
        candidate = os.path.normpath(os.path.join(STUDIO_DIR, rel))
        if candidate.startswith(STUDIO_DIR) and os.path.isfile(candidate):
            mime, _ = mimetypes.guess_type(candidate)
            return self._file(candidate, mime or "application/octet-stream")
        self._json({"error": "page nahi mili"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/run":
            return self._json({"error": "unknown endpoint"}, 404)
        length = int(self.headers.get("Content-Length") or 0)
        if length > 400_000:
            return self._json({"ok": False, "error": "Code bahut lamba hai"}, 413)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return self._json({"ok": False, "error": "JSON ghalat hai"}, 400)
        code = payload.get("code") or ""
        inputs = payload.get("inputs") or []
        if not isinstance(inputs, list):
            inputs = str(inputs).splitlines()
        inputs = [str(x) for x in inputs]
        result = run_program(code, inputs)
        return self._json(result)

    def _generated(self, example):
        try:
            code = read_example(example)
        except FileNotFoundError:
            return self._bytes(b"example nahi mila", "text/plain; charset=utf-8", 404)
        result = run_program(code)
        if not result["ok"]:
            html = f"<pre style='color:#fca5a5;background:#111;padding:24px'>❌ {result['error']}</pre>"
            return self._bytes(html.encode("utf-8"), "text/html; charset=utf-8", 400)
        html = result["html"] or "<p>Is program ne website nahi banayi.</p>"
        return self._bytes(html.encode("utf-8"), "text/html; charset=utf-8")

    def _json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _file(self, path, content_type):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _bytes(self, data: bytes, content_type: str, status=200):
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main(host="0.0.0.0", port=None):
    port = int(port or os.environ.get("PORT") or 8080)
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"🇵🇰 Asaan Studio v{VERSION}  →  http://{host}:{port}")
    print("   Playground:  /")
    print("   Website:     /site     (Asaan Lang se bani!)")
    print("   School:      /school")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStudio band.")


if __name__ == "__main__":
    main()
