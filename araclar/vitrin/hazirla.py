#!/usr/bin/env python3
"""
Panel ekran görüntüsünden site için "vitrin" görseli hazırlar (yalnızca geliştirme aracı, yayına girmez).

Adımlar:
  1) Gizli bilgileri (mağaza adı, ürün adları) bulanıklaştırır
  2) Görüntüyü 16:10 oranında kırpar (sağdaki boş alan ve bildirim pencereleri gider)
  3) Yakın çekim bölgesini ayırır
  4) vitrin.js ile koyu, ışıklı zeminde pencere + yakın çekim kartı olarak çizer
  5) site/gorseller/ekran/<ad>-1600.webp ve <ad>-800.webp dosyalarını yazar

Kullanım:
  python3 araclar/vitrin/hazirla.py araclar/vitrin/sitedeki-ekranlar.json   (sitedeki bütün ekranlar)
  python3 araclar/vitrin/hazirla.py araclar/vitrin/ornek-ayar.json          (yeni ekran için örnek)

Gerekenler: Python 3 + Pillow, Node.js + Playwright (Claude Code bulut oturumunda hazır gelir).
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CIKTI = os.path.join(KOK, "site", "gorseller", "ekran")


def bulaniklastir(im, kutu, yaricap=7, kose=8):
    x0, y0, x1, y1 = [int(v) for v in kutu]
    bolge = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(yaricap))
    maske = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius=kose, fill=255)
    im.paste(bolge, (x0, y0), maske)


def kirp_16_10(im, sag_sinir=None):
    """Görüntüyü 16:10 yapar. Sağdaki boş alan atılır (sag_sinir verilmişse o x değerinden sonrası,
    verilmemişse yüksekliğe göre fazla kalan kısım). Görüntü dar kalırsa alttan kesilir; geniş
    kalırsa üst satır tekrarlanarak yükseklik tamamlanır (panelin üst zemini düz renk olduğu için iz kalmaz)."""
    w, h = im.size
    w = min(w, int(sag_sinir)) if sag_sinir else min(w, round(h * 1.6))
    im = im.crop((0, 0, w, h))
    hedef = round(w / 1.6)
    if hedef <= h:
        return im.crop((0, 0, w, hedef))
    yeni = Image.new("RGB", (w, hedef))
    yeni.paste(im.crop((0, 0, w, 1)).resize((w, hedef - h)), (0, 0))
    yeni.paste(im, (0, hedef - h))
    return yeni


def main():
    ayarlar = json.load(open(sys.argv[1], encoding="utf-8"))
    gecici = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_gecici")  # git dışında
    os.makedirs(gecici, exist_ok=True)
    cizim = []
    for a in ayarlar:
        # Göreli yollar ayar dosyasının bulunduğu klasöre göre okunur
        kaynak = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), a["kaynak"])
        im = Image.open(kaynak).convert("RGB")
        for kutu in a.get("bulanik", []):
            bulaniklastir(im, kutu)
        ana = kirp_16_10(im, a.get("genislik_siniri"))
        ana_yol = os.path.join(gecici, f"ana-{a['ad']}.png")
        yakin_yol = os.path.join(gecici, f"yakin-{a['ad']}.png")
        ana.save(ana_yol)
        im.crop(tuple(a["yakin"])).save(yakin_yol)
        cizim.append({"ad": a["ad"], "ana": ana_yol, "yakin": yakin_yol,
                      "etiket": a["etiket"], "genislik": a.get("yakin_genislik", 740)})
    is_yolu = os.path.join(gecici, "cizim.json")
    json.dump(cizim, open(is_yolu, "w", encoding="utf-8"), ensure_ascii=False)
    subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vitrin.js"), is_yolu, gecici], check=True)
    for c in cizim:
        png = Image.open(os.path.join(gecici, f"vitrin-{c['ad']}.png")).convert("RGB")
        png.save(os.path.join(CIKTI, f"{c['ad']}-1600.webp"), "WEBP", quality=84, method=6)
        png.resize((800, 500), Image.LANCZOS).save(os.path.join(CIKTI, f"{c['ad']}-800.webp"), "WEBP", quality=84, method=6)
        print("yazıldı:", c["ad"])


if __name__ == "__main__":
    main()
