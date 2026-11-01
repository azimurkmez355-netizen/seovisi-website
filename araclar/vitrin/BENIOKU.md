# Vitrin görselleri (panel ekran görüntüleri)

Sitedeki panel ekran görüntüleri düz konmaz: koyu, ışıklı bir zeminde pencere olarak durur ve sağ
altta önemli bir bölüm, üstünde kısa bir etiketle yakın çekim kartında öne çıkar. Bu klasör, yeni bir
ekran görüntüsü geldiğinde aynı görünümü üretir. Yayına girmez.

Gerekenler: Python 3 + Pillow, Node.js + Playwright (Claude Code bulut oturumunda hazır gelir).

## Sitedeki ekranlar

- `kaynak/`: sitedeki ekranların **bulanıklaştırılmış** kaynak görüntüleri (kayıpsız WebP, sağdaki
  boş alan kırpılmış). Sahibinin gönderdiği bulanıklaştırılmamış görüntüler depoya **konmaz**.
- `sitedeki-ekranlar.json`: her ekranın yakın çekim bölgesi, kart genişliği ve etiketi.

Vitrin tasarımı (`vitrin.js`) değişirse hepsi tek komutla yeniden üretilir:
`python3 araclar/vitrin/hazirla.py araclar/vitrin/sitedeki-ekranlar.json`

## Yeni ekran eklemek

1. Ekran görüntüsündeki gizli bilgilerin (mağaza adı, ürün adları, stok kodları; örnek metinlerde
   geçen mağaza ve marka adları) koordinatlarını bulun ve `bulanik` listesine yazın:
   `[x0, y0, x1, y1]` (orijinal görüntünün pikselleri). Kenar çubuğundaki mağaza adı genellikle
   `[34, 67, 108, 94]` civarındadır. Sonucu mutlaka büyüterek kontrol edin.
2. `genislik_siniri` (isteğe bağlı): sağdaki boş alan ve bildirim pencereleri bu x değerinden sonra
   kesilir (panel içeriği ~1495 px'e kadar). Yazılmazsa görüntü yüksekliğine göre 16:10 kırpılır.
   Görüntü 16:10'dan dar kalırsa alttan kesilir, geniş kalırsa üstüne panel zemini eklenir.
3. `yakin`: yakın çekim kartına girecek bölge `[x0, y0, x1, y1]` (orijinal görüntünün pikselleri);
   bulanık yazı içermesin. `yakin_genislik`: kartın genişliği (700–880 arası iyi durur); `etiket`:
   kartın üstündeki kısa yazı. Etiket yalnızca `URUN-BILGISI.md`'deki bilgilerden yazılır.
4. Ayarı `ornek-ayar.json` gibi bir dosyaya yazıp çalıştırın:
   `python3 araclar/vitrin/hazirla.py <ayar-dosyası>`. Göreli yollar ayar dosyasının klasörüne göre
   okunur. Çıktı: `site/gorseller/ekran/<ad>-1600.webp` ve `<ad>-800.webp` (eskisinin üstüne yazar).
5. Bulanıklaştırılmış kaynağı `kaynak/<ad>.webp` olarak (kayıpsız) kaydedin ve ekranı
   `sitedeki-ekranlar.json` listesine ekleyin (orada `bulanik` gerekmez, kaynak zaten bulanık).
6. `site/*.html` içinde o ekranın `<figure class="vitrin" data-yer-tutucu=...>` işaretini ve
   `YER-TUTUCU` yorumunu kaldırın, alt metni gerçek ekranı anlatacak şekilde yazın.
   `python3 araclar/kontrol.py` ile kontrol edin; `YAPILACAKLAR.md` listesinden ekranı düşün.
