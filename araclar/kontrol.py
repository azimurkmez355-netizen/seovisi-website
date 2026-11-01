#!/usr/bin/env python3
"""
seovisi.com.tr — site kontrolü (yalnızca geliştirme için, yayına girmez).

Her değişiklikten sonra çalıştırın:
  python3 araclar/kontrol.py

Kontrol edilenler:
  - her sayfada tek <h1>, atlanmayan başlık sırası, lang="tr"
  - benzersiz <title> ve meta açıklama, canonical, Open Graph ve Twitter etiketleri
  - görsellerde alt, width ve height; görsel dosyalarının varlığı
  - site içi bağlantıların ve #çapaların karşılığı (_redirects dahil)
  - dış betik / stil / yazı tipi çağrısı olmaması
  - JSON-LD bloklarının geçerli JSON olması
  - sitemap.xml ile arama motoruna açık sayfaların birbirini tutması
  - yer tutucuların (YER-TUTUCU) listesi

Yalnızca Python'un standart kütüphanesini kullanır.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlsplit

KOK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
SITE = "https://seovisi.com.tr"


class Ayristirici(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self._title_ac = False
        self.meta = {}
        self.linkler = []          # (rel, href)
        self.basliklar = []        # seviye listesi
        self.idler = set()
        self.baglantilar = []      # href listesi
        self.gorseller = []        # attr sözlükleri
        self.betikler = []         # (type, src)
        self.jsonld = []
        self._jsonld_ac = False
        self._jsonld_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.idler.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._title_ac = True
            self.title = ""
        elif tag == "meta":
            anahtar = a.get("name") or a.get("property")
            if anahtar:
                self.meta[anahtar] = a.get("content", "")
        elif tag == "link":
            self.linkler.append((a.get("rel", ""), a.get("href", "")))
        elif re.fullmatch(r"h[1-6]", tag):
            self.basliklar.append(int(tag[1]))
        elif tag == "a":
            if "href" in a:
                self.baglantilar.append(a["href"])
        elif tag == "img":
            self.gorseller.append(a)
        elif tag == "script":
            self.betikler.append((a.get("type", ""), a.get("src")))
            if a.get("type") == "application/ld+json":
                self._jsonld_ac = True
                self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._title_ac = False
        elif tag == "script" and self._jsonld_ac:
            self.jsonld.append("".join(self._jsonld_buf))
            self._jsonld_ac = False

    def handle_data(self, data):
        if self._title_ac:
            self.title += data
        if self._jsonld_ac:
            self._jsonld_buf.append(data)


def sayfa_yolu(dosya):
    ad = os.path.relpath(dosya, KOK)
    if ad == "index.html":
        return "/"
    return "/" + ad[: -len(".html")]


def yonlendirmeler():
    k = {}
    yol = os.path.join(KOK, "_redirects")
    if os.path.exists(yol):
        for satir in open(yol, encoding="utf-8"):
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                parca = satir.split()
                k[parca[0]] = parca[1]
    return k


def hedef_dosya(yol):
    """Site içi bir adresin karşılığı olan dosya (yoksa None)."""
    if yol == "/":
        return os.path.join(KOK, "index.html")
    aday = os.path.join(KOK, yol.lstrip("/"))
    if os.path.isfile(aday):
        return aday
    if os.path.isfile(aday + ".html"):
        return aday + ".html"
    if os.path.isdir(aday) and os.path.isfile(os.path.join(aday, "index.html")):
        return os.path.join(aday, "index.html")
    return None


def main():
    hatalar, uyarilar = [], []
    sayfalar = {}
    for kok, _, dosyalar in os.walk(KOK):
        for d in dosyalar:
            if d.endswith(".html"):
                tam = os.path.join(kok, d)
                p = Ayristirici()
                p.feed(open(tam, encoding="utf-8").read())
                sayfalar[tam] = p

    yonler = yonlendirmeler()
    basliklar, aciklamalar = {}, {}
    indekslenebilir = set()

    for dosya, p in sorted(sayfalar.items()):
        ad = os.path.relpath(dosya, KOK)
        yol = sayfa_yolu(dosya)
        ozel = ad == "404.html"
        noindex = "noindex" in p.meta.get("robots", "")
        if not noindex:
            indekslenebilir.add(yol)

        if p.lang != "tr":
            hatalar.append(f"{ad}: <html lang> 'tr' değil")
        if not p.title:
            hatalar.append(f"{ad}: <title> yok")
        else:
            basliklar.setdefault(p.title.strip(), []).append(ad)
            if len(p.title) > 65:
                uyarilar.append(f"{ad}: başlık uzun ({len(p.title)} karakter)")
        acik = p.meta.get("description", "")
        if not acik:
            hatalar.append(f"{ad}: meta açıklama yok")
        else:
            aciklamalar.setdefault(acik, []).append(ad)
            if not 70 <= len(acik) <= 170:
                uyarilar.append(f"{ad}: meta açıklama uzunluğu {len(acik)} karakter")

        kanonik = [h for r, h in p.linkler if r == "canonical"]
        if not ozel:
            beklenen = SITE + yol
            if kanonik != [beklenen]:
                hatalar.append(f"{ad}: canonical {kanonik} (beklenen {beklenen})")
            if p.meta.get("og:url") != beklenen:
                hatalar.append(f"{ad}: og:url hatalı")
        for etiket in ("og:title", "og:description", "og:image", "og:image:alt", "twitter:card",
                       "twitter:title", "twitter:description", "twitter:image"):
            if not p.meta.get(etiket):
                hatalar.append(f"{ad}: {etiket} yok")
        og = p.meta.get("og:image", "")
        if og.startswith(SITE) and not hedef_dosya(og[len(SITE):]):
            hatalar.append(f"{ad}: paylaşım görseli bulunamadı: {og}")

        # Başlık sırası
        h1 = p.basliklar.count(1)
        if h1 != 1:
            hatalar.append(f"{ad}: {h1} adet <h1> var (1 olmalı)")
        onceki = 0
        for s in p.basliklar:
            if onceki and s > onceki + 1:
                hatalar.append(f"{ad}: başlık sırası atlıyor (h{onceki} -> h{s})")
            onceki = s

        # Görseller
        for g in p.gorseller:
            src = g.get("src", "")
            if "alt" not in g:
                hatalar.append(f"{ad}: alt metni olmayan görsel: {src}")
            if not g.get("width") or not g.get("height"):
                hatalar.append(f"{ad}: width/height eksik: {src}")
            for parca in [src] + [s.strip().split(" ")[0] for s in g.get("srcset", "").split(",") if s.strip()]:
                if parca.startswith("/") and not hedef_dosya(parca):
                    hatalar.append(f"{ad}: görsel dosyası yok: {parca}")
            if src.startswith("/gorseller/") and g.get("loading") != "lazy":
                uyarilar.append(f"{ad}: gecikmeli yüklenmeyen içerik görseli: {src}")
            if src.startswith("/gorseller/ekran/") and not src.endswith(".webp"):
                hatalar.append(f"{ad}: ekran görüntüsü WebP değil: {src}")

        # Dış kaynaklar
        for tur, src in p.betikler:
            if src and not src.startswith("/"):
                hatalar.append(f"{ad}: dış betik: {src}")
        for rel, href in p.linkler:
            if rel in ("stylesheet", "preload", "preconnect", "dns-prefetch") and not href.startswith("/"):
                hatalar.append(f"{ad}: dış kaynak ({rel}): {href}")

        # JSON-LD
        for blok in p.jsonld:
            try:
                json.loads(blok)
            except Exception as e:
                hatalar.append(f"{ad}: JSON-LD geçersiz: {e}")

        # Bağlantılar
        for href in p.baglantilar:
            if href.startswith(("mailto:", "tel:")):
                continue
            parca = urlsplit(href)
            if parca.scheme in ("http", "https"):
                if parca.netloc in ("seovisi.com.tr", "www.seovisi.com.tr"):
                    hatalar.append(f"{ad}: site içi bağlantı tam adresle yazılmış: {href}")
                continue
            hedef_yol = parca.path or yol
            if hedef_yol.endswith(".html"):
                hatalar.append(f"{ad}: .html uzantılı bağlantı (temiz adres kullanın): {href}")
            if hedef_yol in yonler:
                if parca.fragment:
                    hatalar.append(f"{ad}: yönlendirilen adreste çapa: {href}")
                continue
            hedef = hedef_dosya(hedef_yol)
            if not hedef:
                hatalar.append(f"{ad}: kırık bağlantı: {href}")
                continue
            if parca.fragment:
                hp = sayfalar.get(hedef)
                if hp is None or parca.fragment not in hp.idler:
                    hatalar.append(f"{ad}: çapa bulunamadı: {href}")

    for b, d in basliklar.items():
        if len(d) > 1:
            hatalar.append(f"aynı <title> birden fazla sayfada: {d}")
    for b, d in aciklamalar.items():
        if len(d) > 1:
            hatalar.append(f"aynı meta açıklama birden fazla sayfada: {d}")

    # _redirects hedefleri
    for kaynak, hedef in yonler.items():
        if hedef.startswith("/") and not hedef_dosya(urlsplit(hedef).path):
            hatalar.append(f"_redirects: {kaynak} -> {hedef} hedefi yok")

    # sitemap
    sm = open(os.path.join(KOK, "sitemap.xml"), encoding="utf-8").read()
    sm_yollar = {u[len(SITE):] or "/" for u in re.findall(r"<loc>(.*?)</loc>", sm)}
    for y in sorted(sm_yollar):
        if not hedef_dosya(y):
            hatalar.append(f"sitemap.xml: sayfası olmayan adres: {y}")
        elif y not in indekslenebilir:
            hatalar.append(f"sitemap.xml: arama motorlarına kapalı sayfa listede: {y}")
    for y in sorted(indekslenebilir - sm_yollar):
        hatalar.append(f"sitemap.xml: arama motorlarına açık sayfa listede yok: {y}")

    # Yer tutucular
    yer_tutucular = []
    for kok, _, dosyalar in os.walk(KOK):
        for d in sorted(dosyalar):
            if d.endswith((".html", ".xml", ".txt")) or d.startswith("_"):
                tam = os.path.join(kok, d)
                for no, satir in enumerate(open(tam, encoding="utf-8"), 1):
                    if "YER-TUTUCU" in satir:
                        yer_tutucular.append(f"{os.path.relpath(tam, KOK)}:{no}: {satir.strip()[:110]}")

    print(f"Kontrol edilen sayfa: {len(sayfalar)}  (arama motorlarına açık: {len(indekslenebilir)})")
    print(f"\nYer tutucular ({len(yer_tutucular)}):")
    for y in yer_tutucular:
        print("  -", y)
    if uyarilar:
        print(f"\nUyarılar ({len(uyarilar)}):")
        for u in uyarilar:
            print("  !", u)
    if hatalar:
        print(f"\nHATALAR ({len(hatalar)}):")
        for h in hatalar:
            print("  x", h)
        sys.exit(1)
    print("\nHata yok.")


if __name__ == "__main__":
    main()
