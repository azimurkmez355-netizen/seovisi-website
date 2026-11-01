# Yayın ve alan adı kurulumu

Bu rehber `seovisi.com.tr` sitesini internete açmak için adım adım ne yapacağınızı anlatır.
Teknik bilgi gerekmez; sırayla ilerleyin. Bir adımda takılırsanız ekran görüntüsüyle Claude'a sorun.

> **Önemli:** `app.seovisi.com.tr` kaydı başka bir sunucuyu (uygulama panelini) gösteriyor.
> Bu rehberdeki hiçbir adımda **o kayda dokunulmaz**: değeri değiştirilmez, silinmez, taşınmaz.
> Değişen yalnızca `seovisi.com.tr` ve `www.seovisi.com.tr` olur.

> **Yalnızca test etmek istiyorsanız:** 2. ve 3. adımlar yeterlidir. Site birkaç dakika içinde
> `seovisi-website.pages.dev` gibi bir deneme adresinde açılır; telefondan ve bilgisayardan
> deneyebilirsiniz. Alan adına (DNS) dokunmanız gerekmez. Her güncellemede bu adres de kendiliğinden
> yenilenir.

---

## 1. Nerede yayınlayalım? (karşılaştırma)

Site düz HTML dosyalarından oluşuyor; bu yüzden aşağıdakilerin hepsinde çalışır.

| | **Cloudflare Pages** (önerilen) | Netlify | GitHub Pages |
|---|---|---|---|
| Ücret | Ücretsiz | Ücretsiz plan var | Ücretsiz |
| Trafik sınırı | Statik site için pratikte sınırsız | Aylık kredi sınırı var; dolarsa site ay sonuna kadar durabilir | Aylık 100 GB civarı esnek sınır |
| Her güncellemede | Otomatik yayın, sınır sorunu yok | Her yayın kredi harcar | Otomatik yayın (ek ayar gerekir) |
| Türkiye'ye hız | İstanbul'da sunucusu var | İyi | İyi |
| `seovisi.com.tr` (www'siz) adresi | Alan adının DNS yönetimi Cloudflare'e taşınır (ücretsiz) | DNS'te iki kayıt değişir | DNS'te birkaç kayıt değişir |
| "App Store'da incele" tek yerden değişir mi? | Evet (`site/_redirects`) | Evet | Hayır, her sayfada ayrı değişir |
| Güvenlik başlıkları (`site/_headers`) | Evet | Evet | Hayır |
| Ticari ürün sitesi | Uygun | Uygun | GitHub'ın kuralları ticari ürün sitelerini pek desteklemiyor |

**Önerim: Cloudflare Pages.** Ücretsiz, trafik sınırı derdi yok, Türkiye'de hızlı ve sitenin bütün
özellikleri (tek yerden App Store adresi, güvenlik başlıkları, temiz adresler, özel 404 sayfası)
orada hiç ayar gerektirmeden çalışıyor. Tek ek iş: alan adının DNS yönetimini Cloudflare'e taşımak.
Bu ücretsizdir; aşağıda `app` kaydı bozulmadan nasıl yapılacağı adım adım anlatılıyor.

---

## 2. Cloudflare hesabı açın

1. <https://dash.cloudflare.com/sign-up> adresinden ücretsiz hesap açın ve e-postanızı doğrulayın.

## 3. Siteyi GitHub'dan bağlayın

1. Cloudflare panelinde soldaki menüden **Workers & Pages**'e girin.
2. **Create** (Oluştur) düğmesine basın ve **Pages** sekmesini seçin.
3. **Connect to Git** (Git'e bağla) → **GitHub**'ı seçin. GitHub izin isterse
   `azimurkmez355-netizen/seovisi-website` deposuna erişim verin.
4. Depo olarak **seovisi-website**'ı seçin ve **Begin setup**'a basın.
5. Ayarları şöyle girin:
   - **Project name:** `seovisi-website`
   - **Production branch:** `main`
   - **Framework preset:** `None`
   - **Build command:** boş bırakın
   - **Build output directory:** `site`
6. **Save and Deploy**'a basın. Bir iki dakika içinde site
   `https://seovisi-website.pages.dev` gibi bir deneme adresinde açılır.

> **Ekranda "Pages" seçeneği yoksa:** Cloudflare menüleri zamanla değişebiliyor. Yalnızca
> **Workers** görüyorsanız **Import a repository** (depo içe aktar) ile aynı depoyu seçin ve
> ayarlara dokunmadan devam edin. Depodaki `wrangler.jsonc` dosyası, yayınlanacak klasörün `site`
> olduğunu Cloudflare'e zaten söylüyor. Sonraki adımlar aynıdır; yalnızca "Custom domains" menüsü
> Worker'ın **Settings → Domains & Routes** bölümünde olur.

**Kontrol:** Deneme adresini açın; sayfalar, menü ve görseller görünüyor olmalı.
(Deneme adresi arama motorlarına kapalıdır, merak etmeyin.)

## 4. Alan adının DNS yönetimini Cloudflare'e taşıyın

Bu bölümde `app.seovisi.com.tr` kaydını **aynen koruyacağız.**

### 4a. Önce mevcut kayıtların fotoğrafını çekin

1. Alan adını aldığınız firmanın paneline girin (ya da DNS'i şu an kim yönetiyorsa onunkine).
2. **DNS kayıtları** sayfasını açın ve **bütün kayıtların ekran görüntüsünü alın.** Özellikle:
   - `app` kaydı: türünü (A ya da CNAME) ve değerini not edin.
   - `MX` kayıtları: `@seovisi.com.tr` uzantılı e-posta kullanıyorsanız bunlar e-postanızı taşır.
   - `TXT` kayıtları: e-posta doğrulama (SPF, DKIM) ve Google doğrulaması gibi kayıtlar.
3. Firmanın panelinde **DNSSEC** açıksa şimdilik **kapatın** (açık kalırsa taşıma sırasında site ve
   uygulama paneli erişilemez hâle gelebilir). İsterseniz taşıma bittikten sonra Cloudflare'de
   yeniden açabilirsiniz.

### 4b. Alan adını Cloudflare'e ekleyin

1. Cloudflare panelinde **Add a domain** (alan adı ekle) → `seovisi.com.tr` yazın.
2. **Free** (ücretsiz) planı seçin.
3. Cloudflare mevcut kayıtları tarayıp bir liste gösterir. Bu listeyi 4a'daki ekran görüntünüzle
   **satır satır karşılaştırın.** Eksik olan varsa **Add record** ile aynen ekleyin.
4. **`app` kaydı için:**
   - Türü ve değeri ekran görüntünüzdekiyle **birebir aynı** olmalı. Değiştirmeyin, silmeyin.
   - **Proxy status** sütunundaki bulutu **gri (DNS only)** yapın. Böylece uygulama paneline giden
     trafik bugün olduğu gibi doğrudan kendi sunucusuna gider; Cloudflare araya girmez.
5. `MX` ve `TXT` kayıtları da aynen kalmalı. Bunlarda da bulut gri olmalıdır.
6. `seovisi.com.tr` (kök, `@`) ya da `www` için eski bir kayıt varsa şimdilik dokunmayın;
   5. adımda Cloudflare bunları siteye yönlendirmeyi kendisi önerecek.

### 4c. Nameserver'ları değiştirin

1. Cloudflare size iki adres verir (örnek: `ada.ns.cloudflare.com`, `bob.ns.cloudflare.com`).
2. Alan adını aldığınız firmanın panelinde **Nameserver / DNS sunucuları** ayarına girin ve mevcut
   adresleri Cloudflare'in verdiği iki adresle değiştirin.
3. `.com.tr` alan adlarında bu değişiklik birkaç saat sürebilir. Cloudflare değişikliği görünce
   size e-posta atar ve alan adı **Active** (etkin) olur.

**Kontrol:** Alan adı etkin olunca `https://app.seovisi.com.tr` adresini açın. Uygulama paneli eskisi
gibi açılıyor olmalı. Açılmıyorsa Cloudflare'deki `app` kaydını ekran görüntünüzle tekrar
karşılaştırın (tür, değer, gri bulut).

## 5. Siteyi alan adına bağlayın

1. **Workers & Pages** → **seovisi-website** projesi → **Custom domains** → **Set up a custom domain**.
2. `seovisi.com.tr` yazın → **Continue** → **Activate domain**. Cloudflare gerekli kaydı kendisi ekler.
3. Aynı adımları `www.seovisi.com.tr` için tekrarlayın.
4. Birkaç dakika içinde ikisi de **Active** olur ve HTTPS (kilit simgesi) kendiliğinden gelir.

## 6. www'yu www'suz adrese yönlendirin

Sitenin asıl adresi `https://seovisi.com.tr`. `www` ile gelenler oraya yönlendirilmeli.

1. Cloudflare'de `seovisi.com.tr` alan adına girin → **Rules** (Kurallar) → **Redirect Rules**
   → **Create rule** (kural oluştur).
2. Hazır şablon varsa **Redirect from WWW to root** (www'dan köke yönlendir) şablonunu seçin ve kaydedin.
3. Şablon yoksa elle girin:
   - **Rule name:** `www'dan köke`
   - **If incoming requests match:** Custom filter expression → **Hostname** `equals`
     `www.seovisi.com.tr`
   - **Then:** URL redirect → **Type:** Dynamic → **Expression:**
     `concat("https://seovisi.com.tr", http.request.uri.path)`
   - **Status code:** `301` · **Preserve query string:** işaretli
4. **Deploy** (kaydet).

Ek olarak **SSL/TLS → Edge Certificates → Always Use HTTPS** seçeneğini açın. Bu ayar yalnızca
Cloudflare'in araya girdiği (turuncu bulutlu) adresleri etkiler; gri bulutlu `app` kaydı etkilenmez.

> **Yapmayın:** Cloudflare'de HSTS ayarını "Include subdomains" (alt alan adlarını dahil et) ile
> açmayın. Bu, `app.seovisi.com.tr`'yi de etkiler. Sitenin kendi HSTS ayarı zaten yalnızca
> `seovisi.com.tr` için geçerli olacak şekilde hazırlandı.

## 7. Son kontroller

Hepsini telefondan ve bilgisayardan deneyin:

- [ ] `https://seovisi.com.tr` açılıyor, kilit simgesi var.
- [ ] `https://www.seovisi.com.tr` → `https://seovisi.com.tr` adresine geçiyor.
- [ ] `http://seovisi.com.tr` (s'siz) → `https://` adresine geçiyor.
- [ ] `https://seovisi.com.tr/ozellikler` açılıyor; `.../ozellikler.html` yazınca `/ozellikler`'e geçiyor.
- [ ] `https://seovisi.com.tr/olmayan-bir-sayfa` özel 404 sayfasını gösteriyor.
- [ ] **`https://app.seovisi.com.tr` uygulama paneli eskisi gibi çalışıyor.**
- [ ] `@seovisi.com.tr` e-postası kullanıyorsanız e-posta gönderip alabiliyorsunuz.

## 8. Google Search Console (önerilir)

1. <https://search.google.com/search-console> → **Mülk ekle** → **Alan adı** → `seovisi.com.tr`.
2. Google bir `TXT` kaydı verir. Cloudflare → `seovisi.com.tr` → **DNS** → **Add record** →
   Type `TXT`, Name `@`, Content: Google'ın verdiği metin → kaydedin → Google'da **Doğrula**.
   (Bu yeni bir kayıttır; `app` kaydına dokunmaz.)
3. Doğrulandıktan sonra soldan **Site haritaları** → `sitemap.xml` yazıp gönderin.

İsterseniz aynısını Bing Webmaster Tools için de yapabilirsiniz (Google Search Console'dan içe
aktarma seçeneği var).

---

## Site nasıl güncellenir?

GitHub'daki `main` dalına her yeni değişiklik geldiğinde Cloudflare siteyi birkaç dakika içinde
kendiliğinden yeniden yayınlar. Sizin bir şey yapmanız gerekmez. Bir güncelleme sorun çıkarırsa
Cloudflare'de **Deployments** sekmesinden önceki sürüme tek tıkla geri dönebilirsiniz
(**Rollback**).

## Bir şeyler ters giderse

- **Site açılmıyor ama `app` çalışıyor:** 5. adımdaki "Custom domains" durumunu kontrol edin.
- **`app.seovisi.com.tr` açılmıyor:** Cloudflare → DNS'te `app` kaydının türünü, değerini ve gri
  bulutu ekran görüntünüzle karşılaştırın. Çözemezseniz alan adı firmanızın panelinde nameserver'ları
  eski adreslere geri yazarak her şeyi önceki hâline döndürebilirsiniz (birkaç saat sürebilir).
- **E-posta gelmiyor:** `MX` ve `TXT` kayıtlarını ekran görüntünüzle karşılaştırın.
