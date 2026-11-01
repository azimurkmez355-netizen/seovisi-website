# Vitrin görselleri (panel ekran görüntüleri)

Sitedeki panel ekran görüntüleri düz konmaz: koyu, ışıklı bir zeminde pencere olarak durur ve sağ
altta önemli bir bölüm, üstünde kısa bir etiketle yakın çekim kartında öne çıkar. Bu klasör, yeni bir
ekran görüntüsü geldiğinde aynı görünümü üretir. Yayına girmez.

Gerekenler: Python 3 + Pillow, Node.js + Playwright (Claude Code bulut oturumunda hazır gelir).

1. Ekran görüntüsündeki gizli bilgilerin (mağaza adı, ürün adları, stok kodları) koordinatlarını
   bulun ve `bulanik` listesine yazın: `[x0, y0, x1, y1]` (orijinal görüntünün pikselleri).
   Kenar çubuğundaki mağaza adı genellikle `[34, 70, 108, 94]` civarındadır.
2. `genislik_siniri` (isteğe bağlı): sağdaki boş alan ve bildirim pencereleri bu x değerinden sonra
   kesilir (panel içeriği ~1495 px'e kadar). Yazılmazsa görüntü yüksekliğine göre 16:10 kırpılır.
   Görüntü 16:10'dan dar kalırsa alttan kesilir, geniş kalırsa üstüne panel zemini eklenir.
3. `yakin`: yakın çekim kartına girecek bölge `[x0, y0, x1, y1]` (orijinal görüntünün pikselleri);
   `yakin_genislik`: kartın genişliği (700–880 arası iyi durur); `etiket`: kartın üstündeki kısa yazı.
   Etiket yalnızca `URUN-BILGISI.md`'deki bilgilerden yazılır.
4. Çalıştırın: `python3 araclar/vitrin/hazirla.py araclar/vitrin/ornek-ayar.json`
   Çıktı: `site/gorseller/ekran/<ad>-1600.webp` ve `<ad>-800.webp` (eskisinin üstüne yazar).
5. `site/*.html` içinde o ekranın `<figure class="vitrin" data-yer-tutucu=...>` işaretini ve
   `YER-TUTUCU` yorumunu kaldırın, alt metni gerçek ekranı anlatacak şekilde yazın.
   `python3 araclar/kontrol.py` ile kontrol edin; `YAPILACAKLAR.md` listesinden ekranı düşün.

Sitedeki dört gerçek ekranın ayarları (kaynak görüntüler depoda değil):

| Ekran | genislik_siniri | yakin | yakin_genislik | etiket |
|---|---|---|---|---|
| genel-bakis | — | `[596, 200, 1160, 436]` | 720 | SEO haritası · her kare bir ürün |
| uyarilar | 1500 | `[878, 190, 1496, 396]` | 760 | Fiyat, stok, kopya ve kırık bağlantı uyarıları |
| kategori-analizi | — | `[280, 88, 976, 312]` | 740 | Kategori analizi ve düzeltme |
| otopilot | — | `[286, 292, 1160, 518]` | 760 | Onaylı ya da otomatik gönderim |
