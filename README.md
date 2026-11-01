# seovisi-website

[seovisi.com.tr](https://seovisi.com.tr) tanıtım sitesi. seovisi, Ideasoft mağazaları için SEO ve
katalog bakım uygulamasıdır.

Site düz HTML ve CSS'ten oluşur; derleme adımı yoktur. Yayınlanan dosyalar `site/` klasöründedir.

| Dosya | Ne işe yarar? |
|---|---|
| [`KURULUM.md`](KURULUM.md) | Siteyi yayına alma ve alan adı (DNS) adımları |
| [`YAPILACAKLAR.md`](YAPILACAKLAR.md) | Henüz eklenmemiş bilgiler (yer tutucular) ve kontrol edilecek kararlar |
| [`URUN-BILGISI.md`](URUN-BILGISI.md) | Sitedeki içeriğin tek kaynağı |
| [`CLAUDE.md`](CLAUDE.md) | Siteyi düzenleyen yapay zekâ için kurallar |

## Bilgisayarda önizleme

Python 3 yüklü bir bilgisayarda depo klasöründe:

```bash
python3 araclar/onizleme.py
```

Ardından tarayıcıda <http://localhost:8080> adresini açın. Kontrol için:

```bash
python3 araclar/kontrol.py
```
