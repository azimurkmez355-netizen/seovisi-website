# seovisi-website

`seovisi.com.tr` (ve `www.seovisi.com.tr`) tanıtım sitesi. seovisi, Ideasoft altyapısındaki
e-ticaret mağazaları için SEO ve katalog bakım uygulaması; Ideasoft App Store'da yıllık abonelikle
satılır. Uygulama paneli ayrı bir projededir (`app.seovisi.com.tr`); bu repo onunla kod paylaşmaz.

Site sahibi teknik değil: onunla **sade Türkçe** konuş. Bir konuda emin değilsen sor, uydurma.

## İçerik nereden geliyor

Sitedeki bütün bilgiler **`URUN-BILGISI.md`** dosyasından gelir. Orada olmayan özellik, rakam,
müşteri yorumu ya da vaat siteye eklenmez. Ürün değişirse önce o dosyayı güncelle.
Henüz gelmemiş bilgiler (App Store adresi, iletişim, şirket bilgisi, ekran görüntüleri, örnek
sonuçlar, hukuki metinler) **`YAPILACAKLAR.md`** listesindedir; doldurulan maddeyi oradan düşür.

## Kesin kurallar

- Sıralama vaadi yok ("Google'da 1. sıraya çıkarırız" gibi). Kullanılacak vaat:
  **"Google'ın önerdiği temel kuralları ürünlerinize eksiksiz uygular."**
- Rakip firmaların adı sitede geçmez.
- Uydurma müşteri, yorum, logo, istatistik, ödül yok.
- Ideasoft'un logosu kullanılmaz; adı düz metin olarak anılır ("Ideasoft").
- "Yakında" özellikleri ya hiç yazılmaz ya da açıkça "Yakında" etiketiyle yazılır.
- Fiyat yazılmaz (kesinleşmedi): "Fiyatlar ve satın alma Ideasoft App Store'da." Sitede ödeme alınmaz.
- Panel ekran görüntüleri gelene kadar açıkça işaretli yer tutucu kullanılır.
- Çerez, analiz aracı, dış betik yok. Eklenirse önce çerez bildirimi ve politika güncellenir.

## Teknik çerçeve

- Düz HTML + tek CSS + çok az saf JavaScript. **Derleme adımı, npm paketi, çerçeve yok.**
  `site/` klasörü olduğu gibi yayınlanır (Cloudflare Pages, çıktı klasörü `site`).
- Dışarıya istek yok: yazı tipi (Plus Jakarta Sans) `site/fontlar/` içinde. Google Fonts, CDN,
  dış betik kullanma (KVKK).
- `site/_headers` sıkı bir CSP içerir: **satır içi `<style>`, `style="..."` ve satır içi betik
  kullanma.** JSON-LD (`application/ld+json`) serbest.
- Temiz adresler: bağlantıları `.html` olmadan yaz (`/ozellikler`, `/paketler#...`).
- Üst bölüm (header) ve alt bölüm (footer) her sayfada tekrar eder; birini değiştirirsen hepsini
  değiştir. Etkin menü öğesi `aria-current="page"` ile işaretlenir.
- Bütün "Ideasoft App Store'da incele" bağlantıları `/app-store` adresine gider; gerçek adres
  yalnızca `site/_redirects` dosyasında değişir.
- Paket bilgisi (ad, ürün sınırı, özellik, fiyat) yalnızca `site/paketler.html` içindeki
  "PAKET BİLGİLERİ" bloğunda yazar; başka sayfada tekrar etme.
- Yer tutucuların yanında `YER-TUTUCU` yorumu bulunur.

## SEO kuralları (bu bir SEO ürününün sitesi)

- Her sayfada benzersiz `<title>` ve meta açıklama, `canonical` (`https://seovisi.com.tr/...`),
  `lang="tr"`, Open Graph ve Twitter kartı, paylaşım görseli (`site/gorseller/paylasim/`).
- Tek `<h1>`, başlık sırası atlanmaz.
- Görsellerde `alt`, `width`, `height`; içerik görselleri WebP ve `loading="lazy"`. Ekran
  görüntüleri iki boyutta: `ad-800.webp` ve `ad-1600.webp` (`srcset` ile).
- Yapısal veri: ana sayfada `Organization` + `WebSite` + `SoftwareApplication`, SSS'de `FAQPage`
  (SSS metni değişirse JSON-LD'yi de değiştir).
- Yeni sayfa: `site/sitemap.xml`'e ekle. Taslak / bilgi sayfaları `noindex` olur ve site haritasına
  girmez (şu an: hukuki sayfalar, `app-store-yakinda`, `404`).
- Hedef: Lighthouse'ta performans, erişilebilirlik, en iyi uygulamalar ve SEO 95+ (şu an 100).

## Klasör yapısı

```
site/                 yayınlanan klasör
  *.html              sayfalar (index, ozellikler, nasil-calisir, paketler, sss, iletisim,
                      kullanim-kosullari, gizlilik-ve-kvkk, cerez-politikasi, app-store-yakinda, 404)
  css/site.css        bütün stiller (renkler en üstte değişken olarak)
  js/site.js          yalnızca mobil menü
  fontlar/            Plus Jakarta Sans (Latin + Türkçe alt küme) ve OFL lisansı
  marka/              logo, işaret, favicon, uygulama ikonları
  gorseller/ekran/    panel ekran görüntüleri (şimdilik yer tutucular)
  gorseller/paylasim/ sayfa başına paylaşım (Open Graph) görselleri, 1200×630
  _headers, _redirects, robots.txt, sitemap.xml, site.webmanifest, favicon.ico
araclar/              yayına girmez
  onizleme.py         yerel önizleme (Cloudflare Pages'i taklit eder): python3 araclar/onizleme.py
  kontrol.py          site kontrolü: python3 araclar/kontrol.py
URUN-BILGISI.md       içeriğin tek kaynağı
YAPILACAKLAR.md       yer tutucular ve sahibin kontrol edeceği kararlar
KURULUM.md            yayın ve DNS adımları
wrangler.jsonc        yalnızca Cloudflare Workers ile yayınlanırsa kullanılır
```

## Çalışma şekli

- Her değişiklikten sonra `python3 araclar/kontrol.py` çalıştır; hata kalmasın. Görünümü
  `python3 araclar/onizleme.py` ile masaüstü ve mobil boyutta kontrol et.
- Site sahibi commit'lerin **sorulmadan** yapılmasını istiyor: anlamlı her adımdan sonra Türkçe
  mesajla commit'le ve `main` dalına gönder. `main` Cloudflare'e bağlanınca her gönderim siteyi
  yayına alır.
- `app.seovisi.com.tr` ile ilgili DNS kaydına hiçbir talimatta dokunulmaz.
