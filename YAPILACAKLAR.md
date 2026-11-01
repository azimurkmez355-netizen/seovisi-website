# Yapılacaklar — bütün yer tutucular tek listede

Sitede henüz gerçek bilgisi olmayan her şey burada. Bilgiyi Claude'a verdiğinizde ilgili satır
güncellenir ve bu listeden düşer. (Teknik not: kodda her yer tutucunun yanında `YER-TUTUCU` yazar;
`python3 araclar/kontrol.py` hepsini listeler.)

## 1. Bilgi bekleyenler

| # | Ne? | Nerede görünüyor? | Hangi dosyada değişecek? | Durum |
|---|---|---|---|---|
| 1 | **Ideasoft App Store adresi** | Bütün "Ideasoft App Store'da incele" düğmeleri | Yalnızca `site/_redirects` (tek satır) | Bekliyor. Düğmeler şimdilik "sayfa hazırlanıyor" bilgisine gidiyor |
| 2 | **E-posta adresi** | İletişim sayfası | `site/iletisim.html` | Bekliyor |
| 3 | **WhatsApp numarası** | İletişim sayfası | `site/iletisim.html` | Bekliyor |
| 4 | **Şirket bilgileri** (unvan, adres, vergi dairesi ve no, MERSİS no, e-posta, telefon) | 3 hukuki sayfa | `site/kullanim-kosullari.html`, `site/gizlilik-ve-kvkk.html`, `site/cerez-politikasi.html` | Bekliyor |
| 5 | **Hukuki metinler** (avukat yazacak) | Kullanım koşulları · Gizlilik politikası ve KVKK aydınlatma metni · Çerez politikası | Aynı 3 dosya | Bekliyor. Sayfalarda "Taslak" uyarısı var ve arama motorlarına kapalılar |
| 6 | **Panel ekran görüntüleri** (aşağıdaki liste) | Ana sayfa, Özellikler, Nasıl çalışır | `site/gorseller/ekran/` | Bekliyor. Yerlerinde açıkça "YER TUTUCU" yazan görseller var |
| 7 | **Örnek sonuçlar** (önce / sonra ölçümü) | Ana sayfanın "Örnek sonuçlar" bölümü | `site/index.html` (`ornek-sonuclar` bölümü) | Bekliyor. Yayından önce ya doldurun ya da gizleyin (aşağıya bakın) |
| 8 | **Fiyatlar** (kesinleşince, isterseniz) | Paketler sayfası | `site/paketler.html` içindeki işaretli "PAKET BİLGİLERİ" bloğu | Şimdilik "Fiyatlar ve satın alma Ideasoft App Store'da" yazıyor |
| — | Logo ve ikonlar | Her sayfa | `site/marka/` | **Tamam:** gönderdiğiniz logo paketinden eklendi |

### Ekran görüntüleri listesi

Önerilen boyut **1600 × 1000 piksel** (yatay, 16:10). PNG olarak gönderebilirsiniz; Claude bunları
hızlı yüklenen WebP biçimine çevirip iki boyutta yerleştirir.

| Ekran | Dosya adı | Kullanıldığı sayfalar |
|---|---|---|
| Genel bakış (ürünlerin SEO / görsel / kategori durumu, mağaza SEO puanı, yapılacaklar) | `genel-bakis` | Özellikler, Nasıl çalışır |
| Ürün SEO'su (hazırlanan başlık, meta açıklama ve açıklamanın kontrol edilip gönderildiği ekran) | `urun-seo` | Özellikler |
| Kategori analizi (yanlış / kategorisiz ürünler, önerilen alt kategoriler) | `kategori-analizi` | Ana sayfa, Özellikler |
| Açıklama şablonu (görünüm seçimi ve canlı önizleme) | `aciklama-sablonu` | Ana sayfa, Özellikler |
| Yeni ürün otopilotu (onaylı / otomatik gönderim ayarı) | `otopilot` | Ana sayfa, Özellikler |
| Uyarılar (fiyat, indirim, stok uyarıları listesi) | `uyarilar` | Özellikler |
| Kurulum sihirbazı (4 adım) | `kurulum-sihirbazi` | Nasıl çalışır |
| Değişiklik geçmişi ve tek tuşla geri alma | `geri-alma` | Ana sayfa |

İsteğe bağlı (şu an sitede yerleri yok, gelirse eklenebilir): kopya ürünler, kırık bağlantılar,
aylık rapor, görseli eksik ürünler.

Ekran görüntülerinde gerçek müşteri ya da mağaza bilgisi görünmemesine dikkat edin (örnek / test
mağazası kullanın).

### Örnek sonuçlar bölümünü gizlemek

Ölçüm bitmeden siteyi yayına alacaksanız `site/index.html` içinde şu satırı bulun:

```html
<section class="bolum" id="ornek-sonuclar"
```

ve `<section` kelimesinden hemen sonra `hidden` ekleyin:

```html
<section hidden class="bolum" id="ornek-sonuclar"
```

Ya da Claude'a "örnek sonuçları gizle" demeniz yeterli.

### Hukuki metinler gelince

Her sayfada: taslak uyarısı kaldırılır, `noindex` satırı silinir (sayfa arama motorlarına açılır),
sayfa `site/sitemap.xml` listesine eklenir. Claude bunları birlikte yapar.

## 2. Yayından önce

- [ ] `KURULUM.md`'deki adımlar (Cloudflare, DNS, www yönlendirmesi, Search Console)
- [ ] App Store adresi (1) gelmeden yayına çıkılacaksa düğmeler "sayfa hazırlanıyor" bilgisine gider; bu bilinçli bir geçici durumdur
- [ ] Örnek sonuçlar (7) dolduruldu ya da gizlendi
- [ ] Hukuki metinler (4, 5) eklendi ya da taslak hâliyle yayına çıkılması kabul edildi
- [ ] İletişim bilgileri (2, 3) eklendi

## 3. Sizin kontrol etmeniz gereken kararlar

Size soru sormadan ilerlemem istendiği için bazı konularda kendim karar verdim. Lütfen göz atın:

1. **"Ideasoft" yazımı:** Sitede sizin metninizdeki gibi "Ideasoft" yazdım. Markanın resmi yazımı
   "IdeaSoft" ise söyleyin, her yerde değiştiririm.
2. **10.000'den fazla ürünü olan mağazalar:** Sitede bu konuda hiçbir şey yazmıyor. Böyle mağazalar
   için ne söylemek istersiniz (ör. "bize yazın")?
3. **Ücretsiz analizin kapsamı:** Yalnızca "sorunları görür, düzeltme gönderemez" yazdım. Ürün
   sınırı ya da kapsamı farklıysa söyleyin.
4. **Aylık rapor hangi pakette?** Metinde pakete bağlanmadığı için paket kartlarına yazmadım.
   Haftalık otomatik taramayı ise "ücretli paketlerde" olarak yazdım.
5. **Aylık ödeme:** "Yıllık ödeme ana seçenek" dediniz; sitede yalnızca "yıllık abonelik" geçiyor.
   Aylık seçenek de olacaksa ekleyelim.
6. **Ek SSS soruları:** İstediğiniz 7 sorunun yanına sizin metninizdeki bilgilerle şunları ekledim:
   kurulum, panel nerede açılır, hangi sektörler, Google'da ilk sıra (sıralama sözü verilmediğini
   açıklıyor), otomatik gönderim güvenli mi, fiyatlar. İstemediğiniz olursa çıkarırım.
7. **Ana sayfadaki kontrol ızgarası:** "seovisi her ürünü bu başlıklarda kontrol eder" altında 9
   başlık var: sayfa başlığı, meta açıklama, ürün açıklaması, kategori, görsel, kopya ürün, fiyat,
   indirim, stok. Hepsi özellik listenizden; yine de doğru olup olmadığına bakın.
8. **Arama sonuçlarında yıldız görünmez:** Ana sayfada istenen `SoftwareApplication` yapısal verisi
   var, ama Google yazılımlarda yıldızlı / zengin sonuç göstermek için kullanıcı puanı ister. Sahte
   puan eklenmedi; bu yüzden zengin sonuç çıkmayabilir. Gerçek puanlar olunca eklenebilir.
   Ücretsiz analiz, yapısal veride "0 TL" teklif olarak işaretli.

## 4. Avukat için bilgi

Hukuki metinleri yazacak kişiye iletebileceğiniz teknik bilgiler:

- Site şu anda **çerez, analiz aracı, dış betik ve form içermiyor.** Yazı tipi de sitenin kendi
  sunucusundan geliyor (Google Fonts kullanılmıyor).
- Site Cloudflare üzerinde yayınlanacak; barındırma hizmetleri ziyaretçi IP adreslerini teknik
  kayıtlarında (log) tutabilir.
- Sitede ödeme alınmıyor; satın alma Ideasoft App Store üzerinden yapılıyor.
- Uygulama tarafı (`app.seovisi.com.tr`): mağaza erişim anahtarları şifreli saklanıyor, her mağaza
  yalnızca kendi verisini görüyor, uygulama kaldırılınca mağazanın verileri 30 gün sonra tamamen
  siliniyor, mağazaya yalnızca onaylanan değişiklikler yazılıyor ve her değişiklik yedekleniyor.
- İleride analiz aracı ya da çerez eklenirse çerez bildirimi ve çerez politikası o zaman güncellenecek.
