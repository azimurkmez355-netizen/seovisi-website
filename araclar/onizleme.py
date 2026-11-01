#!/usr/bin/env python3
"""
seovisi.com.tr — yerel önizleme sunucusu (yalnızca geliştirme için, yayına girmez).

Vercel'in davranışını taklit eder; ayarları depo kökündeki vercel.json dosyasından okur:
  - cleanUrls: /ozellikler -> site/ozellikler.html, /ozellikler.html -> /ozellikler (308)
  - trailingSlash: false -> /ozellikler/ -> /ozellikler (308)
  - redirects ve headers bölümleri (has: host koşulu dahil)
  - bulunamayan adreslerde site/404.html'i 404 koduyla gösterir
  - metin dosyalarını sıkıştırır (gzip)

Not: vercel.json'daki "source" desenleri burada düzenli ifade olarak okunur. Bu sitedeki
biçimler ("/(.*)", "/fontlar/(.*)", "/app-store") için Vercel ile aynı sonucu verir; ":ad" gibi
adlandırılmış parametreler desteklenmez.

Kullanım:
  python3 araclar/onizleme.py            # http://localhost:8080
  python3 araclar/onizleme.py 8090       # başka bir port

Yalnızca Python'un standart kütüphanesini kullanır; kurulum gerekmez.
"""
import gzip
import http.server
import json
import mimetypes
import os
import re
import sys
from urllib.parse import urlsplit, unquote

DEPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
AYAR_DOSYASI = os.path.join(DEPO, "vercel.json")


def ayarlar():
    """vercel.json her istekte yeniden okunur; değişiklik için sunucuyu yeniden başlatmak gerekmez."""
    try:
        with open(AYAR_DOSYASI, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


KOK = os.path.join(DEPO, ayarlar().get("outputDirectory", "site"))

mimetypes.add_type("application/manifest+json", ".webmanifest")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")

SIKISTIR = ("text/", "application/javascript", "application/json", "application/manifest+json",
            "application/xml", "image/svg+xml")


def kosullar_tutuyor(kural, istek_basliklari):
    for k in kural.get("has", []):
        if k.get("type") == "host":
            host = (istek_basliklari.get("Host") or "").split(":")[0]
            if not re.fullmatch(k.get("value", ".*"), host):
                return False
        else:
            return False  # başka koşul türleri yerelde değerlendirilmez
    return True


def kaynak_uyar(kaynak, yol):
    return re.fullmatch(kaynak, yol) is not None


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
        ayar = ayarlar()
        parca = urlsplit(self.path)
        yol = unquote(parca.path)
        sorgu = ("?" + parca.query) if parca.query else ""

        # trailingSlash: false -> sondaki eğik çizgi kaldırılır
        if ayar.get("trailingSlash") is False and yol != "/" and yol.endswith("/"):
            return self.yonlendir(yol.rstrip("/") + sorgu, 308)

        # cleanUrls -> .html uzantısı kaldırılır
        if ayar.get("cleanUrls"):
            if yol.endswith("/index.html"):
                return self.yonlendir(yol[: -len("index.html")] + sorgu, 308)
            if yol.endswith(".html"):
                return self.yonlendir(yol[: -len(".html")] + sorgu, 308)

        # redirects
        for kural in ayar.get("redirects", []):
            if kaynak_uyar(kural["source"], yol) and kosullar_tutuyor(kural, self.headers):
                kod = kural.get("statusCode") or (308 if kural.get("permanent", True) else 307)
                return self.yonlendir(kural["destination"], kod)

        dosya = None
        aday = os.path.normpath(os.path.join(KOK, yol.lstrip("/")))
        if not aday.startswith(KOK):
            aday = None
        if aday:
            if os.path.isdir(aday) and os.path.isfile(os.path.join(aday, "index.html")):
                dosya = os.path.join(aday, "index.html")
            elif os.path.isfile(aday):
                dosya = aday
            elif ayar.get("cleanUrls") and os.path.isfile(aday + ".html"):
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
        onbellek = "public, max-age=0, must-revalidate"  # Vercel'in statik dosyalar için varsayılanı
        for kural in ayar.get("headers", []):
            if kaynak_uyar(kural["source"], yol) and kosullar_tutuyor(kural, self.headers):
                for b in kural["headers"]:
                    if b["key"].lower() == "cache-control":
                        onbellek = b["value"]
                    else:
                        self.send_header(b["key"], b["value"])
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
