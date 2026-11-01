# Yayın ve alan adı kurulumu (Vercel)

Bu rehber `seovisi.com.tr` sitesini Vercel'de internete açmak için adım adım ne yapacağınızı
anlatır. Teknik bilgi gerekmez; sırayla ilerleyin. Bir adımda takılırsanız ekran görüntüsüyle
Claude'a sorun. (Vercel menülerinin adları zamanla değişebilir; benzer adlı düğmeyi arayın.)

> **Önemli:** `app.seovisi.com.tr` kaydı başka bir sunucuyu (uygulama panelini) gösteriyor.
> Bu rehberdeki hiçbir adımda **o kayda dokunulmaz**: değeri değiştirilmez, silinmez, taşınmaz.
> Değişen yalnızca `seovisi.com.tr` ve `www.seovisi.com.tr` olur.

> **Plan seçimi:** Vercel'in ücretsiz planı (**Hobby**) yalnızca kişisel ve ticari olmayan kullanım
> içindir. Bir ürünü tanıtan şirket sitesi ticari kullanım sayılır; bu yüzden Vercel'de **Pro** plan
> gerekir (aylık ücretli, güncel fiyat: <https://vercel.com/pricing>). Ücretsiz ve ticari kullanıma
> açık bir yer isterseniz site Cloudflare Pages'te de çalışır; Claude'a söylemeniz yeterli.

> **Yalnızca test etmek istiyorsanız:** 1. ve 2. adımlar yeterlidir. Site birkaç dakika içinde
> `seovisi-website.vercel.app` gibi bir deneme adresinde açılır. Bu adres arama motorlarına
> kapalıdır. Alan adına (DNS) dokunmanız gerekmez.

Sitenin bütün Vercel ayarları depodaki **`vercel.json`** dosyasındadır: yayınlanan klasör (`site`),
temiz adresler (`/ozellikler`), "App Store'da incele" yönlendirmesi ve güvenlik başlıkları.
Vercel panelinde bunlar için ayrıca bir şey yapmanız gerekmez.

---

## 1. Vercel hesabı açın

1. <https://vercel.com/signup> adresine girin ve **Continue with GitHub** (GitHub ile devam et)
   seçeneğiyle, siteyi tutan GitHub hesabınızla giriş yapın.
2. Hesap türü sorulursa **Pro**'yu seçin (yukarıdaki "Plan seçimi" notuna bakın).

## 2. Siteyi GitHub'dan içe aktarın

1. Vercel panelinde **Add New…** (Yeni ekle) → **Project** (Proje).
2. **Import Git Repository** listesinde **seovisi-website**'ı bulun → **Import**.
   GitHub izin isterse `azimurkmez355-netizen/seovisi-website` deposuna erişim verin.
3. Açılan ayar ekranında:
   - **Project Name:** `seovisi-website`
   - **Framework Preset:** `Other`
   - **Root Directory:** değiştirmeyin (`./`)
   - **Build and Output Settings** ve **Environment Variables:** dokunmayın, boş kalsın.
4. **Deploy**'a basın. Bir iki dakika içinde "Congratulations" ekranı gelir. Site
   `https://seovisi-website.vercel.app` gibi bir deneme adresinde açılır.

**Kontrol:** Deneme adresini telefondan ve bilgisayardan açın; sayfalar, menü ve görseller görünüyor
olmalı. `/olmayan-bir-sayfa` yazınca sitenin kendi 404 sayfası gelmeli.

### Kapalı kalması gerekenler

Sitenin kuralı: çerez, ölçüm aracı ve dış betik yok. Bu yüzden Vercel'de:

- **Analytics** (Web Analytics) ve **Speed Insights** bölümlerinde **Enable** (aç) demeyin. İkisi de
  siteye ölçüm betiği ekler; açılırsa önce gizlilik ve çerez metinleri güncellenmelidir.
- İsteğe bağlı: proje ayarlarındaki **Vercel Toolbar** seçeneğini kapatabilirsiniz. Açık kalırsa
  yalnızca deneme adreslerinde sizin gördüğünüz bir araç çubuğu çıkar; asıl siteyi etkilemez.

## 3. Alan adını Vercel'e ekleyin

1. Projeye girin → **Domains** bölümü (sol menüde ya da **Settings → Domains**) → **Add Domain**.
2. `seovisi.com.tr` yazın ve ekleyin.
3. Vercel `www` için seçenek sunarsa **`www.seovisi.com.tr`'yi `seovisi.com.tr`'ye yönlendiren**
   seçeneği seçin. (Vercel genellikle tersini, yani www'yu asıl adres yapmayı önerir. Bu sitenin asıl
   adresi www'suz `seovisi.com.tr`; arama motorlarına da öyle bildirildi.)
4. Bu seçenek çıkmazsa `www.seovisi.com.tr`'yi ayrıca ekleyin. Sonra listede onun yanındaki **Edit**
   (Düzenle) → **Redirect to** (Yönlendir) → `seovisi.com.tr` seçin. Kalıcı yönlendirme
   (**308** ya da **301**) seçili olsun → **Save**.
5. İki adın yanında **Invalid Configuration** (geçersiz yapılandırma) yazması normaldir: DNS kayıtları
   henüz eklenmedi. Vercel her biri için hangi kaydın gerektiğini gösterir:
   - `seovisi.com.tr` için bir **A** kaydı (değer bir IP adresi, çoğu projede `76.76.21.21`),
   - `www.seovisi.com.tr` için bir **CNAME** kaydı (değer bu projeye özel, `…vercel-dns…com` gibi).

   **Değerleri Vercel'in ekranından kopyalayın**; bu rehberdeki örneklere değil, oradakine güvenin.

> **Yapmayın:** Vercel "nameserver'ları Vercel'e taşı" (Vercel DNS) seçeneği de sunabilir. Bunu
> **seçmeyin.** Taşıma, `app` kaydını ve e-posta kayıtlarını yeniden kurmayı gerektirir; bize yalnızca
> iki kayıt eklemek yetiyor.

## 4. DNS'e iki kayıt ekleyin

Bu bölümde `app.seovisi.com.tr` kaydına **dokunulmaz.** Yalnızca kök (`@`) ve `www` kayıtları değişir.

1. Alan adının DNS kayıtlarını yönettiğiniz panele girin: alan adını aldığınız firmanın paneli ya
   da DNS'i başka bir hizmette (ör. Cloudflare) tutuyorsanız orası.
2. Değişiklikten önce **bütün kayıtların ekran görüntüsünü alın.** Bir sorun olursa geri dönmek için
   gerekir. Özellikle `app` kaydının türünü ve değerini not edin.
3. **Kök (`@`, ya da adı boş olan) kayıt:**
   - Kök için zaten bir **A** kaydı varsa değerini Vercel'in verdiği IP ile değiştirin; yoksa yeni
     ekleyin: **Tür** `A` · **Ad** `@` · **Değer** Vercel'in gösterdiği IP.
   - Kök için başka **A** kayıtları da varsa onları silin; Vercel'inki tek kalmalı.
   - Kök için bir **AAAA** kaydı varsa silin. Vercel bunu desteklemez ve doğrulamayı engeller.
4. **`www` kaydı:** **Tür** `CNAME` · **Ad** `www` · **Değer** Vercel'in gösterdiği adres.
   `www` için eski bir kayıt varsa onu bununla değiştirin.
5. **Başka hiçbir kayda dokunmayın:** `app`, `MX` (e-posta) ve `TXT` kayıtları aynen kalır.
6. DNS'iniz **Cloudflare**'deyse bu iki kayıtta bulut **gri (DNS only)** olmalı. Turuncu kalırsa
   Vercel güvenlik sertifikası (HTTPS) alamaz.
7. Kaydedin. Birkaç dakika ile birkaç saat içinde (`.com.tr`'de biraz uzun sürebilir) Vercel'deki
   iki ad **Valid Configuration** olur ve HTTPS (kilit simgesi) kendiliğinden gelir.

**Kontrol:** `https://app.seovisi.com.tr` uygulama paneli eskisi gibi açılıyor olmalı.

## 5. HTTPS ve yönlendirmeler

Bunları Vercel kendisi yapar; sizin bir şey yapmanız gerekmez:

- `http://` ile gelenler `https://` adresine geçer.
- `www` ile gelenler `seovisi.com.tr`'ye geçer (3. adımdaki ayar).
- HSTS güvenlik ayarı yalnızca `seovisi.com.tr` için geçerlidir; `app.seovisi.com.tr`'yi etkilemez.

> **Yapmayın:** `vercel.json` dosyasına `includeSubDomains` içeren bir HSTS ayarı eklemeyin; bu
> `app.seovisi.com.tr`'yi de etkiler. (`python3 araclar/kontrol.py` bunu hata olarak yakalar.)

## 6. Son kontroller

Hepsini telefondan ve bilgisayardan deneyin:

- [ ] `https://seovisi.com.tr` açılıyor, kilit simgesi var.
- [ ] `https://www.seovisi.com.tr` → `https://seovisi.com.tr` adresine geçiyor.
- [ ] `http://seovisi.com.tr` (s'siz) → `https://` adresine geçiyor.
- [ ] `https://seovisi.com.tr/ozellikler` açılıyor; `.../ozellikler.html` yazınca `/ozellikler`'e geçiyor.
- [ ] `https://seovisi.com.tr/olmayan-bir-sayfa` sitenin kendi 404 sayfasını gösteriyor.
- [ ] "Ideasoft App Store'da incele" düğmesi doğru yere gidiyor (adres gelene kadar "hazırlanıyor" sayfası).
- [ ] **`https://app.seovisi.com.tr` uygulama paneli eskisi gibi çalışıyor.**
- [ ] `@seovisi.com.tr` e-postası kullanıyorsanız e-posta gönderip alabiliyorsunuz.

## 7. Google Search Console (önerilir)

1. <https://search.google.com/search-console> → **Mülk ekle** → **Alan adı** → `seovisi.com.tr`.
2. Google bir `TXT` kaydı verir. 4. adımdaki DNS panelinde **yeni bir kayıt** ekleyin:
   **Tür** `TXT` · **Ad** `@` · **Değer** Google'ın verdiği metin → kaydedin → Google'da **Doğrula**.
   (Bu yeni bir kayıttır; `app` kaydına dokunmaz.)
3. Doğrulandıktan sonra soldan **Site haritaları** → `sitemap.xml` yazıp gönderin.

İsterseniz aynısını Bing Webmaster Tools için de yapabilirsiniz (Google Search Console'dan içe
aktarma seçeneği var).

---

## Ideasoft App Store adresi gelince

Sitedeki bütün "Ideasoft App Store'da incele" düğmeleri `/app-store` adresine gider. Bu adresin
nereye yönleneceği yalnızca `vercel.json` dosyasındaki şu satırda yazar:

```json
"destination": "/app-store-yakinda",
```

Adres belli olunca bu satır `"destination": "https://…(App Store'daki seovisi sayfası)…",` olur.
Adresi Claude'a vermeniz yeterli.

## Site nasıl güncellenir?

GitHub'daki `main` dalına her yeni değişiklik geldiğinde Vercel siteyi birkaç dakika içinde
kendiliğinden yeniden yayınlar. Sizin bir şey yapmanız gerekmez. Bir güncelleme sorun çıkarırsa
Vercel'de **Deployments** sekmesinde önceki sürümün menüsünden (**⋯**) **Instant Rollback** ile
önceki hâline dönebilirsiniz.

## Bir şeyler ters giderse

- **Vercel'de ad "Invalid Configuration" olarak kalıyor:** A ve CNAME değerlerini Vercel'in
  ekranındakiyle karşılaştırın. Kök için başka A ya da AAAA kaydı kalmadığından emin olun. DNS
  Cloudflare'deyse bulut gri olmalı. Alan adında `CAA` kaydı varsa `letsencrypt.org` için izin
  gerekir. `.com.tr` alan adlarında değişikliğin görünmesi birkaç saat sürebilir.
- **`app.seovisi.com.tr` açılmıyor:** Bu rehber `app` kaydına dokunmaz. DNS panelinde `app`
  kaydını 4. adımdaki ekran görüntünüzle karşılaştırın (tür ve değer aynı mı?).
- **E-posta gelmiyor:** `MX` ve `TXT` kayıtlarını ekran görüntünüzle karşılaştırın.
- **Site eski hâliyle görünüyor:** Vercel'de **Deployments** sekmesinde son yayının **Ready**
  (hazır) olduğunu kontrol edin; tarayıcıda sayfayı yenileyin.
