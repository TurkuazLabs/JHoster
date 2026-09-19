# 📄 Dosya Yolu: E:\JHoster\ROADMAP.md
# 📌 Amac: JHoster gelistirme yol haritasini tanimlar
# 📌 Modul - Markdown
# Version: 3.76.1
# Aciklama: v3.76.1 tutarlilik patch sonrasi stack installer, vhost publish ve database wizard planini tanimlar
# Bagimli Oldugu Katman: View

# JHoster Roadmap

## Tamamlanan

- v3.76.1: Desktop aktif kaynak header path duzeltmeleri, source header guard ve roadmap tutarlilik patch
- v3.76.0: Release cleanup, gereksiz dosya temizligi, routes.txt normalize ve API surface audit
- v3.74.0: Logs sayfasi uygulama bazli tab menu ve log klasor mapping
- v3.71.0: Modern Command Center UI, hero alan, environment snapshot ve New Site Wizard premium polish
- v3.70.0: Fullscreen no-tab stack wizard, Apache/Nginx + MySQL/PHP/Mailpit secimi
- v3.69.0: New Site Wizard UI ve preview paneli
- v3.68.0: Hosts Auto UI, New Test Site hosts rozeti, Settings Hosts sekmesi ve real hosts repair butonlari
- v3.67.0: Hosts auto inspect, repair-plan, repair ve conflict raporlama
- v3.66.0: Hosts auto sync, New Test Site UX hint, JHoster managed hosts blok ve route entegrasyonu
- v3.65.0: Pro feature registry UI, Settings License feature satirlari ve agent feature_registry cevabi
- v3.64.0: Desktop License Status UI, Settings License sekmesi ve license refresh entegrasyonu
- v3.63.0: Community 5 site limiti, Pro sinirsiz altyapi ve lisans state endpointi

- v3.2.x: Agent boot ve root endpoint
- v3.3.0: Component manifest catalog
- v3.4.0: Safe plan executor
- v3.5.0: Cache, checksum, safe extract
- v3.6.0: App registry
- v3.7.0: Process manager
- v3.8.0: Service adapter layer
- v3.9.0: Local package installer
- v3.10.0: Runtime version manager
- v3.11.0: Project manager
- v3.12.0: Virtual host snapshot generator

## Siradaki

- v3.77.0: Stack secimine gore runtime installer, vhost publish ve database create wizard baglantisi

- v3.13.0: hosts file plan layer
- v3.14.0: nginx config apply adapter hazirligi
- v3.15.0: PHP runtime adapter ilk gercek kontrol

## v3.14.0

- Nginx validate snapshot katmani tamamlandi.
- Sonraki adim: gercek Nginx adapter ile `nginx -t` plan ve reload dry-run katmani.
- v3.16.0: Hosts publish snapshot akisi tamamlandi.

## v3.17.0

- Hosts apply admin, backup ve rollback katmani tamamlandi.
- Snapshot apply varsayilan olarak korunur.
- Gercek Windows hosts apply icin admin kontrolu hazirdir.

## v3.18.0

- Nginx real adapter icin guvenli executable path tespiti tamamlandi.
- Shell execution kapali kalacak sekilde path discovery ve registry eklendi.

## Siradaki adim

- Nginx real validate adapter icin `nginx -t` komutunu kontrollu calistirma plani.
- PHP runtime adapter icin ilk gercek binary kontrolu.

## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.

## v3.20.0

- Nginx real reload adapter eklendi.
- Real reload, son real validate `valid` olmadan calismaz.
- Sonraki adim: real validate icin kullanici onayli calistirma profili ve rollback UI.

# v3.22.0 Web Server Profiles

- Nginx ve Apache secimi icin merkezi web server profile katmani eklendi.
- Sonraki adim Apache vhost generator ve publish zinciridir.

# v3.24.0 Audit ve Temizlik

- v3.22.0 paketi derin analizden gecirildi.
- Paket state temizligi yapildi.
- Apache planned profile guard eklendi.
- Siradaki adim: Apache vhost generator ile adapter zincirini baslatmak.

## v3.24.0

- Apache virtual host generator eklendi.
- Apache publish/validate/reload henuz guard altindaki sonraki adimdir.

## v3.30.0

- Web server unified workflow tamamlandi.
- Sonraki adim: JavaFX ekranda profile secimi ve tek workflow butonu baglantisi.

## v3.31.0

- Web server unified workflow rollback guard tamamlandi.
- Sonraki adim: JavaFX ekranda active profile secimi, tek workflow butonu ve son workflow sonuc paneli.

## v3.32.0

- Web server unified workflow run tracking tamamlandi.
- Sonraki adim: JavaFX tarafinda tek workflow butonu, run gecmisi ve step detay paneli.

## v3.33.0

- Web server unified workflow lock guard tamamlandi.
- Ayni proje icin ayni anda ikinci workflow baslatma engellendi.
- Sonraki adim: JavaFX tarafinda tek workflow butonu, run gecmisi, step detaylari ve aktif lock paneli.

## v3.43.0 Sonrasi

1. Runtime PATH shim / launcher wrapper
2. Quick App v1: PHP empty, Laravel, WordPress, OpenCart 3.x
3. Database Manager v1
4. Auto SSL local CA

## v3.42.0 Notu

Quick App v1 tamamlandi. Sira olarak Quick Add paket katalogu, DB manager veya Auto SSL katmanina gecilebilir.

## v3.43.0 Notu

- Klasor standardi belirlendi.
- Desktop wireframe plani eklendi.
- Quick action bar eklendi.
- Veritabani butonu HeidiSQL Portable acacak sekilde baglandi.
- Sonraki adim: Mailpit, Database Manager ve SSL Manager paneli.

## Yeni Plan Sirasi

1. Community limit kontrolunu UI uyarisi ile daha gorunur yapmak.
2. License Settings sayfasini mevcut menu yapisini bozmadan ayarlar akisi altina almak.
3. Pro icin otomatik yedek, gelismis SSL, gelismis DNS ve AI/Ollama modul kapilarini feature registry ile hazirlamak.
4. Servis modullerini tek seferde degil, runtime ailelerine gore surumlu ve testli ilerletmek.

## v3.70.0 Tamamlandi

- Fullscreen maximized desktop acilis.
- Normal mod ana tab menu kaldirildi.
- Tek sayfa control panel akisi olusturuldu.
- New Site Wizard icine Apache/Nginx + MySQL/PHP/Mailpit stack secimi eklendi.

## v3.73.1 Tamamlandi

- Modern Command Center hero alani eklendi.
- Environment Snapshot ve preset kartlari eklendi.
- New Site Wizard stack secimi daha modern kart/pill gorunumune alindi.
- Light tema korunarak UI premium glass-style kartlarla guncellendi.

## v3.73.1 Siradaki Plan

- Secilen stack'e gore runtime installer baglantisi.
- Apache/Nginx vhost publish aksiyonunu New Site create sonrasi otomatik planlama.
- MySQL secildiyse database olusturma wizard adimi.

## v3.73.1 Tamamlandi

- Sol sidebar ana navigasyon korundu.
- Settings penceresi tab menu ile sade hale getirildi.
- License, Hosts, Appearance ve Advanced ayarlari ayri sekmelere tasindi.

## v3.74.0 Siradaki Plan

- New Site Wizard icinde stack secimine bagli gercek Apache/Nginx vhost publish akisi.
- MySQL seciliyse database create plan/dry-run akisi.
- PHP seciliyse runtime version secim dropdown baglantisi.

## v3.74.0 Tamamlandi

- Logs sayfasi uygulama bazli tab menu yapisina gecti.
- Servis loglari Apache/Nginx/MySQL/PHP/Mailpit olarak ayrildi.
- Sonraki adim: log dosyalarindan gercek tail/read entegrasyonu.

- v3.76.0: Sol sidebar sadeleme, calismayan topbar elemanlarini kaldirma, topbar status kartlari ve API audit tekrar kontrolu.
