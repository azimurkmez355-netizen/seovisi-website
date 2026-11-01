# Ürün bilgisi — sitedeki içeriğin tek kaynağı

Bu dosya, site sahibinin verdiği ürün bilgisinin aynısıdır. Sitedeki bütün bilgiler buradan gelir.
Burada olmayan bir özellik, rakam, müşteri yorumu ya da vaat siteye eklenmez. Ürün değişirse
önce bu dosya güncellenir, sonra site.

## seovisi nedir

Ideasoft altyapısındaki e-ticaret mağazaları için bir SEO ve katalog bakım uygulaması. Ideasoft App
Store'da yıllık abonelikle satılacak. Uygulamanın paneli ayrı bir projede ve `app.seovisi.com.tr`
adresinde çalışıyor; bu repo onunla kod paylaşmıyor. Tanıtım sitesi `seovisi.com.tr` (ve
`www.seovisi.com.tr`) adresinde açılacak.

Hedef kitle: Ideasoft'ta mağazası olan her sektörden işletme. Ton: sade, güven veren, teknik olmayan
mağaza sahibine hitap eden Türkçe.

## Hazır özellikler

- **Genel bakış:** her ürünün SEO, görsel ve kategori durumu, mağaza SEO puanı, önem sırasına göre yapılacaklar.
- **Ürün SEO'su:** eksik ürünlere başlık, meta açıklama ve ürün açıklaması hazırlanır; mağaza sahibi kontrol edip gönderir.
- **Kategori analizi:** yanlış kategorideki ve kategorisiz ürünler bulunur, açılması önerilen yeni alt kategoriler gösterilir; düzeltme tek tıkla. Mağazanın kendi ürünlerinden öğrenir, her sektörde çalışır.
- **Görseli eksik ürünler listesi.**
- **Açıklama şablonları:** 4 görünüm (sade, bantlı, çizgili, kutulu), ana renk (sitenin tema rengi önerilir), bölümleri açma / kapama / sıralama, kapanış metni, canlı önizleme ve SEO puanı tahmini. Açıklamalar mağazanın kendi görünümünde olur. Eski açıklamalar yeni şablona toplu ve yedekli geçirilebilir.
- **Yeni ürün otopilotu:** mağazaya eklenen yeni ürünler fark edilir, SEO'su ve kategorisi hazırlanır; onaylı ya da otomatik gönderim. Otomatikte bile yalnızca emin olunan öneriler yazılır, şüpheliler onaya kalır.
- **Uyarılar:** fiyatı 0 olan ürün, hatalı indirim, alış fiyatının altında satış, kategorisine göre aşırı fiyat, yayında ama stokta yok.
- **Kopya ürün tespiti:** aynı stok kodu, barkod, ad, sayfa başlığı ya da meta açıklama.
- **Kırık bağlantı ve 404 taraması** (sitenin herkese açık sayfaları üzerinden).
- **Aylık rapor** (panelde, yazdırılabilir / PDF) ve ücretli paketlerde **haftalık otomatik tarama**.

## Yakında

Sitede ya hiç yok ya da açıkça "Yakında" etiketiyle:

- Yapay zekâ ile ürüne özel açıklama ve marka sesi seçimi
- Özellik doldurma (renk, malzeme, beden gibi bilgileri ürün adından ek alanlara yazma)
- Aylık raporun e-postayla gönderimi

## Nasıl çalışır

Ideasoft App Store'dan kurulur → mağaza Ideasoft üzerinden tanınır (ayrı şifre yok) → 4 adımlı kurulum
sihirbazı (mağaza adı ve marka, açıklama görünümü, ilk tarama ve özet, paket bilgisi) → öneriler
incelenir ve onaylanır. Panel Ideasoft yönetim panelinin içinde açılır, istenirse ayrı sekmede tam
ekran da çalışır.

## Güvenlik

- Tarama ve analiz mağazada hiçbir şeyi değiştirmez; mağazaya yalnızca onaylanan değişiklikler yazılır.
- Yazmadan önce ürün yeniden okunur; yazdıktan sonra fiyat, stok, ürün adı gibi alanlar kontrol edilir. Biri değişmişse ürün eski hâline döndürülür ve işlem durur.
- Her değişiklik yedeklenir ve tek tuşla geri alınabilir.
- Mağaza erişim anahtarları şifreli saklanır; her mağaza yalnızca kendi verisini görür.
- Uygulama kaldırılınca mağazanın verileri 30 gün sonra tamamen silinir.

## Paketler (ürün sayısına göre)

- **Ücretsiz analiz:** sorunları görür, düzeltme gönderemez.
- **Başlangıç:** 1.000 ürüne kadar · **İşletme:** 5.000 ürüne kadar · **Uzman:** 10.000 ürüne kadar.
  Ücretli paketlerin hepsinde SEO gönderimi, kategori düzeltme, yeni kategori açma ve otopilot var.
- Yıllık ödeme ana seçenek. Fiyat yazılmaz, henüz kesinleşmedi: "Fiyatlar ve satın alma Ideasoft App
  Store'da" denir. Sitede ödeme alınmaz.
- Abonelik biterse analiz ve geri alma açık kalır, mağazaya yazma kapanır.

## Vaat

Kullanılacak vaat: **"Google'ın önerdiği temel kuralları ürünlerinize eksiksiz uygular."**
"Sizi Google'da 1. sıraya çıkarırız" gibi sıralama vaadi yok.

## Marka

- Renkler (açık zemin): yazı / koyu `#15161A`, yeşil (tamam) `#1E9E5A`, mavi (vurgu) `#2F4BF0`, boş kare (gri) `#D3D6DD`.
- Renkler (koyu zemin): arka plan `#14151B`, yazı `#FFFFFF`, yeşil `#2BC071`, mavi `#5A70FF`, boş kare `#3A3D47`.
- Logo "Tarama ızgarası": 3×3 kareden oluşan bir ızgara ve yanında "seovisi" yazısı (Plus Jakarta Sans ExtraBold).
- Yazı tipi: Plus Jakarta Sans (repoda barındırılır).
