#!/usr/bin/env python3
"""
seovisi.com.tr — yerel önizleme sunucusu (yalnızca geliştirme için, yayına girmez).

Cloudflare Pages'in davranışını taklit eder:
  - temiz adresler: /ozellikler -> site/ozellikler.html, /ozellikler.html -> /ozellikler (308)
  - site/_redirects ve site/_headers dosyalarını okur
  - bulunamayan adreslerde site/404.html'i 404 koduyla gösterir
  - metin dosyalarını sıkıştırır (gzip)

Kullanım:
  python3 araclar/onizleme.py            # http://localhost:8080
  python3 araclar/onizleme.py 8090       # başka bir port

Yalnızca Python'un standart kütüphanesini kullanır; kurulum gerekmez.
"""
import gzip
import http.server
import mimetypes
import os
import re
import sys
from urllib.parse import urlsplit, unquote

KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
KOK = os.path.abspath(KOK)

mimetypes.add_type("application/manifest+json", ".webmanifest")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")

SIKISTIR = ("text/", "application/javascript", "application/json", "application/manifest+json",
            "application/xml", "image/svg+xml")


def yonlendirmeleri_oku():
    kurallar = []
    yol = os.path.join(KOK, "_redirects")
    if not os.path.exists(yol):
        return kurallar
    for satir in open(yol, encoding="utf-8"):
        satir = satir.strip()
        if not satir or satir.startswith("#"):
            continue
        parca = satir.split()
        kaynak, hedef = parca[0], parca[1]
        kod = int(parca[2]) if len(parca) > 2 else 302
        kurallar.append((kaynak, hedef, kod))
    return kurallar


def basliklari_oku():
    kurallar = []  # (desen, [(ad, deger)])
    yol = os.path.join(KOK, "_headers")
    if not os.path.exists(yol):
        return kurallar
    gecerli = None
    for satir in open(yol, encoding="utf-8"):
        if not satir.strip() or satir.strip().startswith("#"):
            continue
        if not satir.startswith((" ", "\t")):
            desen = satir.strip()
            gecerli = (desen, [])
            kurallar.append(gecerli)
        elif gecerli is not None:
            ad, _, deger = satir.strip().partition(":")
            gecerli[1].append((ad.strip(), deger.strip()))
    return kurallar


def desen_uyar(desen, yol):
    if desen.startswith("http"):
        return False  # alan adına bağlı kurallar yerelde uygulanmaz
    rx = "^" + re.escape(desen).replace(r"\*", ".*") + "$"
    return re.match(rx, yol) is not None


class Isleyici(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **k):
        super().__init__(*a, directory=KOK, **k)

    def log_message(self, fmt, *args):
        sys.stderr.write("[onizleme] " + (fmt % args) + "\n")

    def do_HEAD(self):
        self.isle(govde_gonder=False)

    def do_GET(self):
        self.isle(govde_gonder=True)

    def yonlendir(self, hedef, kod):
        self.send_response(kod)
        self.send_header("Location", hedef)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def isle(self, govde_gonder):
        parca = urlsplit(self.path)
        yol = unquote(parca.path)
        sorgu = ("?" + parca.query) if parca.query else ""

        for kaynak, hedef, kod in yonlendirmeleri_oku():
            if yol == kaynak:
                return self.yonlendir(hedef, kod)

        # Temiz adres kuralları
        if yol.endswith("/index.html"):
            return self.yonlendir(yol[: -len("index.html")] + sorgu, 308)
        if yol.endswith(".html"):
            return self.yonlendir(yol[: -len(".html")] + sorgu, 308)
        if yol != "/" and yol.endswith("/") and os.path.isfile(os.path.join(KOK, yol.strip("/") + ".html")):
            return self.yonlendir(yol.rstrip("/") + sorgu, 308)

        dosya = None
        aday = os.path.normpath(os.path.join(KOK, yol.lstrip("/")))
        if not aday.startswith(KOK):
            aday = None
        if aday:
            if os.path.isdir(aday) and os.path.isfile(os.path.join(aday, "index.html")):
                dosya = os.path.join(aday, "index.html")
            elif os.path.isfile(aday) and not os.path.basename(aday).startswith("_"):
                dosya = aday
            elif os.path.isfile(aday + ".html"):
                dosya = aday + ".html"

        durum = 200
        if dosya is None:
            durum = 404
            dosya = os.path.join(KOK, "404.html")

        tur = mimetypes.guess_type(dosya)[0] or "application/octet-stream"
        if tur.startswith("text/") or tur in ("application/javascript", "application/json", "application/manifest+json", "image/svg+xml", "application/xml"):
            tur += "; charset=utf-8"
        veri = open(dosya, "rb").read()

        kodlama = None
        if "gzip" in (self.headers.get("Accept-Encoding") or "") and tur.startswith(SIKISTIR):
            veri = gzip.compress(veri, 6)
            kodlama = "gzip"

        self.send_response(durum)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        if kodlama:
            self.send_header("Content-Encoding", kodlama)
            self.send_header("Vary", "Accept-Encoding")
        onbellek = "public, max-age=0, must-revalidate"
        for desen, basliklar in basliklari_oku():
            if desen_uyar(desen, yol):
                for ad, deger in basliklar:
                    if ad.lower() == "cache-control":
                        onbellek = deger
                    else:
                        self.send_header(ad, deger)
        self.send_header("Cache-Control", onbellek)
        self.end_headers()
        if govde_gonder:
            self.wfile.write(veri)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    sunucu = http.server.ThreadingHTTPServer(("127.0.0.1", port), Isleyici)
    print(f"seovisi önizleme: http://localhost:{port}  (durdurmak için Ctrl+C)")
    try:
        sunucu.serve_forever()
    except KeyboardInterrupt:
        pass
