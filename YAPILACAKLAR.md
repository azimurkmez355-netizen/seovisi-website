# Yapılacaklar — bütün yer tutucular tek listede

Sitede henüz gerçek bilgisi olmayan her şey burada. Bilgiyi Claude'a verdiğinizde ilgili satır
güncellenir ve bu listeden düşer. (Teknik not: kodda her yer tutucunun yanında `YER-TUTUCU` yazar;
`python3 araclar/kontrol.py` hepsini listeler.)

## 1. Bilgi bekleyenler

| # | Ne? | Nerede görünüyor? | Hangi dosyada değişecek? | Durum |
|---|---|---|---|---|
| 1 | **Ideasoft App Store adresi** | Bütün "Ideasoft App Store'da incele" düğmeleri | Yalnızca `site/_redirects` (tek satır) | Bekliyor. Düğmeler şimdilik "sayfa hazırlanıyor" bilgisine gidiyor |
| 2 | **E-posta adresi** | İletişim sayfası, hukuki sayfalar, yapısal veri | `site/iletisim.html` | **Tamam:** azimurkmez355@gmail.com |
| 3 | **WhatsApp / telefon** | İletişim sayfası, hukuki sayfalar, yapısal veri | `site/iletisim.html` | **Tamam:** +90 535 553 40 92 (WhatsApp düğmesi de bu numaraya gidiyor; numarada WhatsApp açık) |
| 4 | **Şirket bilgileri** (unvan, adres, vergi dairesi ve no, MERSİS no) | 3 hukuki sayfa | `site/kullanim-kosullari.html`, `site/gizlilik-ve-kvkk.html`, `site/cerez-politikasi.html` | Bekliyor. E-posta ve telefon eklendi |
| 5 | **Hukuki metinler** (avukat yazacak) | Kullanım koşulları · Gizlilik politikası ve KVKK aydınlatma metni · Çerez politikası | Aynı 3 dosya | Bekliyor. Sayfalarda "Taslak" uyarısı var ve arama motorlarına kapalılar |
| 6 | **Panel ekran görüntüleri** (aşağıdaki liste) | Ana sayfa, Özellikler, Nasıl çalışır | `site/gorseller/ekran/` | **8'den 6'sı geldi.** Sitede yer tutucu olarak yalnızca Kurulum sihirbazı kaldı (Nasıl çalışır sayfası); Geri alma isteğe bağlı |
| 7 | **Örnek sonuçlar** (önce / sonra ölçümü) | Ana sayfanın "Örnek sonuçlar" bölümü | `site/index.html` (`ornek-sonuclar` bölümü) | Bekliyor. Yayından önce ya doldurun ya da gizleyin (aşağıya bakın) |
| 8 | **Fiyatlar** (kesinleşince, isterseniz) | Paketler sayfası | `site/paketler.html` içindeki işaretli "PAKET BİLGİLERİ" bloğu | Şimdilik "Fiyatlar ve satın alma Ideasoft App Store'da" yazıyor |
| — | Logo ve ikonlar | Her sayfa | `site/marka/` | **Tamam:** gönderdiğiniz logo paketinden eklendi |
| 9 | **Ideasoft logosunun daha keskin sürümü** (isteğe bağlı) | "Ideasoft App Store" düğmeleri, bağlantı görseli | `site/marka/ideasoft/` | Gönderdiğiniz PNG kullanılıyor (dairenin dışı şeffaf yapıldı, logoya dokunulmadı). SVG ya da büyük boyutlu sürümünüz varsa daha net görünür |

### Ekran görüntüleri listesi

Bilgisayarda tam ekran alınmış, yatay bir ekran görüntüsü yeterli (ne kadar büyükse o kadar net).
PNG olarak gönderebilirsiniz; Claude gizli bilgileri bulanıklaştırır, vitrin görünümüne getirir ve
hızlı yüklenen WebP biçiminde iki boyutta yerleştirir.

| Ekran | Dosya adı | Kullanıldığı sayfalar | Durum |
|---|---|---|---|
| Genel bakış | `genel-bakis` | Ana sayfa (panel turu), Özellikler, Nasıl çalışır | **Tamam** |
| Uyarılar | `uyarilar` | Ana sayfa (panel turu), Özellikler | **Tamam** |
| Kategori analizi | `kategori-analizi` | Ana sayfa (panel turu), Özellikler | **Tamam** |
| Yeni ürün otopilotu | `otopilot` | Ana sayfa (panel turu), Özellikler | **Tamam** |
| Ürün SEO'su (hazırlanan başlık, meta açıklama ve açıklamanın kontrol edilip gönderildiği ekran) | `urun-seo` | Ana sayfa (panel turu), Özellikler | **Tamam** |
| Açıklama şablonu (görünüm seçimi ve canlı önizleme) | `aciklama-sablonu` | Ana sayfa (panel turu), Özellikler | **Tamam** |
| Kurulum sihirbazı (4 adım) | `kurulum-sihirbazi` | Nasıl çalışır | Bekliyor |
| Değişiklik geçmişi ve tek tuşla geri alma | `geri-alma` | Şu an kullanılmıyor (isteğe bağlı) | Bekliyor |

Gönderdiğiniz **Görseller** ekranında henüz tarama yapılmadığı için tablo boş görünüyor; bu yüzden
şimdilik kullanmadım. Tarama sonrası bir görüntüsünü gönderirseniz ekleriz. Aylık rapor da isteğe
bağlı olarak eklenebilir.

**Not:** Görüntülerdeki mağaza adı, ürün adları ve stok kodları **bulanıklaştırıldı**. Görüntüler
"vitrin" görünümünde: koyu, ışıklı bir zeminde pencere olarak duruyor, önemli bölüm yakın çekim
kartında büyütülüyor. Sağdaki boş alan ve ekran alıntısı aracı bildirimi kırpıldı. Ürün sayıları ve
puanlar, isteğiniz üzerine görünür bırakıldı. Açıklama şablonu ekranındaki örnek açıklamada geçen
marka adı (başka bir firmanın markası) da bulanıklaştırıldı. Yeni gönderdiğiniz ekranlar da aynı
şekilde hazırlanır (teknik not: `araclar/vitrin/`).

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
- [x] İletişim bilgileri (2, 3) eklendi

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
7. **Ana sayfadaki canlı "ürün taraması" paneli ve çizimler:** Bunlar ekran görüntüsü değil, ne
   yaptığımızı anlatan temsilî çizimlerdir. Paneldeki sütunlar (SEO, Kategori, Görsel, Fiyat) ve
   durumlar (Tamam, İşlem bekliyor, Eksik) özellik listenizden alındı. Kategori çizimindeki
   "Ayakkabı / Bot / Spor ayakkabı" örnek adlardır ve üzerinde "Örnek" etiketi var. Panelin gerçek
   görünümü farklıysa çizimleri ona yaklaştırabilirim.
8. **Arama sonuçlarında yıldız görünmez:** Ana sayfada istenen `SoftwareApplication` yapısal verisi
   var, ama Google yazılımlarda yıldızlı / zengin sonuç göstermek için kullanıcı puanı ister. Sahte
   puan eklenmedi; bu yüzden zengin sonuç çıkmayabilir. Gerçek puanlar olunca eklenebilir.
   Ücretsiz analiz, yapısal veride "0 TL" teklif olarak işaretli.
9. **Ideasoft logosu:** İsteğiniz üzerine "Ideasoft App Store" düğmelerine ve seovisi ⇄ Ideasoft
   bağlantı görseline eklendi. Ideasoft'un logo kullanımıyla ilgili kuralları ya da izin şartı varsa
   (en küçük boyut, boşluk, renk gibi) bana iletin, ona göre ayarlayayım.

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
