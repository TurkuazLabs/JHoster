# 📄 Dosya Yolu: E:\JHoster\app\changelog\CHANGELOG.md
# 📌 Amac: JHoster surum degisikliklerini kaydeder
# 📌 Modul - Markdown
# Version: 3.76.0
# Aciklama: Proje geneli surum notlarini tutar

Bagimli Oldugu Katman: Config | Service | Repo | Tool | View


## v3.73.1 - Settings Tab Menu Restore

- Sol sidebar ana menu korunur.
- Settings icinde tab menu tekrar kullanilir.
- General, Services, License, Hosts, Appearance ve Advanced ayarlari ayrilir.
- Ana ekran kalabaliklasmadan ayar penceresi daha okunur hale getirilir.


## v3.73.1 - Left Sidebar UI

- Normal mod sol sidebar ana menuye tasindi.
- Kalabalik Command Center hero gorunumu normal akistan kaldirildi.
- New Site sol menude ana giris noktasi oldu.
- Sag icerik alani secilen menuye gore sade sayfa olarak calisir.

## v3.73.1 - Modern Command Center UI

- Desktop normal UI modern Command Center akisiyle guncellendi.
- Ust bolume modern hero, stack flow pillleri ve Environment Snapshot rail eklendi.
- New Site Wizard stack secim alani premium kart/pill gorunumune alindi.
- Light tema glass-style kartlar, daha yumusak shadow ve premium rozetlerle modernlestirildi.
- Tab menu kaldirma karari korunur; LauncherView icinde `TabPane` veya `new Tab` kullanilmaz.
- Backend Quick App, hosts auto ve license servislerine dokunulmadan UI katmani yenilendi.

## v3.69.0 - New Site Wizard UI

- Normal mod tab akisi `New Site` sekmesiyle guncellendi.
- New Test Site paneli wizard akisi ve sag preview paneli ile iyilestirildi.
- Local URL, proje klasoru, hosts mode ve hosts issue bilgileri ayni ekranda gorunur hale getirildi.
- Mevcut menu ve JHoster Deck tasarimi korunarak yalnizca light tema polish eklendi.

## v3.68.0 - Hosts Auto UI

- New Test Site kartina hosts auto saglik rozeti ve Inspect Hosts butonu eklendi.
- Settings penceresine Hosts sekmesi eklendi.
- Desktop hosts auto inspect, repair-plan ve repair servis katmani eklendi.
- Agent inspect cevabina UI count alanlari eklendi.

## v3.67.0 - Hosts Auto Inspect and Repair

- Added hosts auto inspect endpoint.
- Added hosts auto repair-plan and repair endpoints.
- Added missing, stale, wrong IP, duplicate and external conflict reporting.
- Kept manual, Docker and Laragon hosts entries outside the managed block untouched.

## v3.66.0 - Hosts Auto Sync and New Test Site

- Agent tarafina `hosts-auto` endpoint grubu eklendi.
- Quick App create ve Project create akislarina otomatik hosts sync sonucu eklendi.
- Windows hosts yazimi admin ve platform kontrolu ile guvenli hale getirildi.
- Snapshot hosts auto test dosyasi `snapshot/hosts/hosts-auto/hosts.jhoster` olarak belirlendi.
- Desktop Quick App karti New Test Site akisi olarak sade mesajlarla guncellendi.
- Ana menu ve JHoster Deck akisi korunur.

## v3.65.0 - Pro Feature Registry UI

- Agent license summary cevabina `feature_registry` listesi eklendi.
- Core ve Pro Module ayrimi merkezi PlanGateService icinde uretildi.
- Community planda site limiti Included, gelismis SSL/DNS/Backup/AI modulleri Pro Locked olarak doner.
- Desktop LicensePlanSummary feature status alanlariyla genisletildi.
- Settings > License sekmesinde feature registry satirlari gorunur hale getirildi.
- Ana menu ve JHoster Deck akisi korunur.

## v3.58.1 - Visible Dev Mode UX Patch

- Dev Mode acildiginda sol menude ayri DEVELOPER grubu gorunur.
- Ust barda DEV MODE ACTIVE rozeti daha belirgin hale getirildi.
- Developer Tools sayfasina uyarili bilgi bandi eklendi.
- Settings penceresine sadece Dev Mode acikken Developer sekmesi eklendi.
- Normal UI developer endpoint butonlarindan temiz kalmaya devam eder.

## v3.58.0 - Dev Mode Gate

- Shift basili acilista Dev Mode algisi eklendi.
- `--dev`, `-Djhoster.dev=true` ve `JHOSTER_DEV_MODE=1` alternatif acilis yollari eklendi.
- Raw agent endpoint butonlari normal UI'dan kaldirildi.
- Developer Tools menusu sadece Dev Mode aktifken gorunur hale getirildi.
- Normal UI daha sade ve son kullanici odakli kalacak sekilde duzenlendi.


## v3.58.0 - Package Downloader Controller Fix

- LauncherController icindeki Package Downloader buton handler compile hatasi duzeltildi.
- Catalog, Plan, Download ve Install aksiyonlari LauncherView sonuc alanina baglandi.


## v3.55.1 - Settings Menu Service Selection

- Settings butonu Laragon benzeri ayar penceresi acacak sekilde guncellendi.
- General ve Services and Ports sekmeleri eklendi.
- Apache/Nginx aktif web server secimi ayar penceresine tasindi.
- Start All kapsaminda Apache, Nginx, MySQL, PHP ve Mailpit servis secimleri kaydedilebilir hale geldi.
- Secimler `data/jhoster/desktop_service_selection_settings.json` dosyasinda saklanir.
- Disabled servislerin Start/Restart butonlari UI tarafinda pasif hale getirilir.

## v3.54.0 - Active Web Server Mode Settings

- Apache/Nginx secimi Ayarlar/System Overview alanindan yapilabilir hale getirildi.
- Start All artik secili aktif web server profilini okur.
- Secili profil Apache ise Apache baslar ve Nginx durur; secili profil Nginx ise Nginx baslar ve Apache durur.
- Backend process guard, secili web server disindaki Apache/Nginx start ve restart isteklerini bloke eder.
- Apache ve Nginx ortak `www` document root metadata bilgisini kullanir.
- `web_server_profile_registry.json` profile_records formatina tasindi.

# Changelog

## v3.73.1 - Desktop API Route Compile Fix

- `QUICK_APP_PLAN_ROUTE` eksik sabiti `DesktopApiConfig` icine eklendi.
- `LauncherView.java` compile hatasi giderildi.
- Ana sol sidebar ve Settings tab menu tasarimi korunmustur.



## v3.53.1 Web Server Port Guard

- Apache ve Nginx icin 80/443 public port cakisma korumasi eklendi.
- Nginx calisirken Apache ayni public portlarla baslatilamaz; Apache calisirken Nginx ayni public portlarla baslatilamaz.
- Start All akisi varsayilan public web server olarak Apache baslatir ve Nginx'i otomatik baslatmaz.
- App registry Apache ve Nginx port metadata degerleriyle guncellendi.


## v3.53.0 Button Wiring Revision

- Clean dashboard uzerindeki visible button, tab ve sidebar aksiyonlari controller handler ile baglandi.
- Planned runtime adapter safe state-control start/stop davranisi kazandi.
- Settings, Logs ve Manage Services aksiyonlari calisir hale getirildi.

## v3.52.0 - Clean Desktop Dashboard

- Ana dashboard kalabaligi azaltildi.
- Ust arama, global durum rozeti ve profil alani eklendi.
- Ozet kartlari Agent, Stack Profile, Workspace Root ve Overall Health olarak sade hale getirildi.
- Services paneli tablo duzenine cekildi.
- Runtime Versions, Quick App, Workflow ve Diagnostics ileri alanlari tab yapisina tasindi.
- Alt bolum Quick Actions, Activity Log ve System Overview olarak yeniden duzenlendi.


## v3.51.0 - Desktop Laragon UI Revision

- Compact dashboard servis satirlarina Start, Stop ve Restart butonlari eklendi.
- Quick Actions alani dashboard alt dock yapisina cekildi.
- Portable Tools dock eklendi.
- Bin, Cmder, Git Bash, Notepad++, Ngrok, Composer ve Yarn Desktop UI uzerinden acilir hale getirildi.
- Veritabani butonunun HeidiSQL Portable davranisi korundu.



## v3.47.0 - Portable Bin Layout

- Laragon benzeri `bin` klasor standardi eklendi.
- Tray `Araclar` menusune portable tool girisleri eklendi.
- HeidiSQL, Cmder, Git Bash, Notepad++, Ngrok, Composer ve Yarn pathleri standart hale getirildi.
- Redis, Memcached ve Sendmail placeholder servis kayitlari eklendi.

## v3.46.0 - Desktop Tray Menu

- Laragon benzeri sistem tepsisi menusu eklendi.
- Pencere kapatma davranisi tray'e gizleme olarak ayarlandi.
- Web, www, hizli uygulama, araclar, servisler, runtime, profil, secenekler ve cikis menuleri eklendi.
- Veritabani menusu HeidiSQL Portable aksiyonuna baglandi.

## v3.45.0 - Compact Dashboard Redesign

- Desktop ana ekran Laragon benzeri compact dashboard duzenine cekildi.
- Servis listesi version/port/status satirlariyla daha okunur hale getirildi.
- Quick action butonlari sag dock alanina tasindi.
- Agent kontrol butonlari compact ana alan icine alindi.

## v3.42.0 - Quick App v1

- Quick App endpointleri eklendi.
- Scaffold-only template sistemi eklendi.
- PHP Empty, Laravel, WordPress, OpenCart 3.x ve Node/Vite template listesi eklendi.
- Desktop Quick App paneli eklendi.
- Quick App agent ve desktop testleri eklendi.

## v3.42.0 - Desktop Runtime Manager

- Runtime active endpointleri eklendi.
- Desktop Runtime Manager karti eklendi.
- PHP, Node ve Python aktif runtime secimi UI uzerinden baglandi.
- Runtime manager compile testi eklendi.

## v3.40.0 - Real Process Profile

- Windows process probe tool eklendi.
- Process inspect endpointi eklendi.
- Status endpointine `prefer_real` parametresi eklendi.
- Guarded real adapter preflight ve status cevaplarina `real_process_probe` eklendi.
- Desktop status aksiyonu inspect endpointine baglandi.



## v3.35.0 - Desktop Workflow Summary UI

- JavaFX Desktop workflow bridge icin summary strip eklendi.
- Active profile, status, run count, lock count, step count ve last run bilgileri ayri alanda gosterilir hale geldi.
- `WorkflowDesktopSummary`, `JsonTextExtractorTool` ve `WorkflowResultFormatterService` eklendi.
- Ham JSON log korunurken kullaniciya okunabilir ozet verildi.


## v3.34.1 - Desktop CSS Warning Patch

- JavaFX CSS parser uyarisina neden olan `-fx-font-weight: 650;` degeri `700` yapildi.
- Desktop CSS syntax guard testi eklendi.
- JavaFX run scriptinde `JAVA_HOME` sirasi duzeltildi.


## v3.11.0

- Project manager eklendi.
- Project registry repository eklendi.
- Project path tool eklendi.
- `/api/v1/www` endpointleri eklendi.
- JavaFX launcher icin Projects butonu eklendi.

## v3.10.0

- Runtime version manager eklendi.

## v3.9.0

- Local package installer eklendi.

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.13.0

- Nginx virtual host publish katmani eklendi.
- Dry-run, backup, checksum ve publish registry akisi eklendi.


## v3.14.0

- Nginx validate katmani eklendi.
- Publish edilen config icin internal static scan dogrulama eklendi.
- Validate endpointleri, registry ve test scripti eklendi.


## v3.15.0

- Nginx reload katmani eklendi.
- Validate sonrasi guvenli simulated reload akisi eklendi.
- Reload registry ve test scripti eklendi.


- v3.16.0: Hosts publish snapshot katmani eklendi.


## v3.17.0

- Hosts apply katmani eklendi.
- Admin privilege tool eklendi.
- Snapshot apply ve real Windows hosts apply ayrimi eklendi.
- Backup ve rollback endpointleri eklendi.
- JavaFX launcher icin Hosts Apply butonu eklendi.


## v3.18.0

- Nginx executable detection katmani eklendi.
- Env path, snapshot path ve standart Windows path adaylari taranir.
- `nginx -v` ve `nginx -t` sadece command label olarak planlanir.
- Shell execution kapali kalir.


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.


## v3.20.0 - Nginx Real Reload Adapter

- Nginx real validate sonrasinda nginx -s reload adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve guard modunda kalir.
- Son real validate `valid` degilse real reload reddedilir.
- Yeni endpoint grubu: `/api/v1/nginx-real-reload`.

- v3.21.0 - Nginx execution preflight katmani eklendi.


## v3.22.0 - Web Server Profiles

- Nginx ve Apache secimini merkezi profile katmanina alan endpoint grubu eklendi.
- Apache secenegi profil seviyesinde gorunur hale getirildi.
- JavaFX launcher icin Web Servers butonu eklendi.
- Yeni endpoint grubu: `/api/v1/web-server-profiles`.


## v3.23.0 - Derin Analiz ve Temizlik

- Paket temizligi, audit raporu ve Apache profile guard eklendi.


## v3.24.0 - Apache Virtual Host Generator

- Apache virtual host generator ve `/api/v1/apache-vhosts` endpoint grubu eklendi.
- Apache vhost registry ve snapshot dosya uretimi eklendi.
- Apache profil kaydina vhost generator hazir bilgisi eklendi.


## v3.30.0 - Web Server Unified Workflow

- Active web server profile secimine gore unified workflow endpointleri eklendi.
- Generate, publish, validate ve reload adimlari tek noktadan sirali calisir.
- Workflow registry, test scripti ve dokumantasyon eklendi.


## v3.31.0 - Web Server Workflow Rollback Guard

- Unified workflow icin `rollback_on_failure` guard eklendi.
- Publish sonrasi validate veya reload hatasinda snapshot publish config geri alinir.
- Manuel rollback endpointi eklendi: `/api/v1/web-server-workflow/{project_code}/rollback`.
- Rollback tool, test scripti ve dokumantasyon eklendi.


## v3.34.0 - Desktop Workflow Bridge

- JavaFX Desktop arayuzune unified web server workflow bridge eklendi.
- Active profile, plan, dry-run, runs ve locks aksiyonlari Desktop uzerinden kullanilabilir hale geldi.
- Desktop API route config, HTTP request tool ve workflow modelleri eklendi.
- Guvenli varsayilanlar korundu: `dry_run=true`, `allow_real_execution=false`.


## v3.37.0 - Process Real Preflight Guard

- Process manager preflight endpointi eklendi.
- Process manager restart endpointi eklendi.
- allow_real_execution guard parametresi start, stop ve restart akislari icin eklendi.
- Guarded local process adapter katmani eklendi.
- Desktop Service Manager satirlarina Preflight butonu eklendi.

## v3.36.0 - Desktop Service Manager UI

- JavaFX Desktop ana ekrana Service Manager paneli eklendi.
- Apache, Nginx, MySQL ve PHP icin status/start/stop/restart aksiyonlari eklendi.
- Agent app registry varsayilan service kayitlariyla dolduruldu.
- Guvenli simulated state ile Laragon benzeri temel servis kontrol deneyimi baslatildi.
- Real Windows process calistirma sonraki surume birakildi.

## v3.40.0 - Service Manager Real Process Profile

- Real process profil endpointleri eklendi.
- Install path ve `real_process.enabled` ayari dry-run guard ile yonetilir hale geldi.
- Test: `agent/test-process-real-profile.ps1`.


## v3.43.0 - Folder Standard, Desktop Wireframe ve Quick Actions

- JHoster klasor standardi dokumani eklendi.
- JHoster Desktop ana ekran wireframe dokumani eklendi.
- Desktop ana ekrana Laragon benzeri Quick Actions paneli eklendi.
- Veritabani butonu HeidiSQL Portable acacak sekilde baglandi.
- Web, Terminal, Root, Projects ve Logs hizli butonlari eklendi.
- HeidiSQL Portable icin `bin/heidisql` yer tutucu klasoru eklendi.

## v3.44.0 - Compact Dashboard ve Mailpit Service

- Desktop Quick Actions paneline Start All, Stop All ve Mailpit eklendi.
- Service Manager tarafina Mailpit status/preflight/start/stop/restart satiri eklendi.
- Agent registry icine Mailpit placeholder servis kaydi eklendi.
- HeidiSQL Portable Veritabani butonu korundu.
## v3.56.0 - UI Completion and Dynamic Pages

- Dashboard body now switches between Overview, Services, Runtime Versions, Quick App, Workflow, Diagnostics, Tools and Logs pages.
- Sidebar navigation now changes the visible content instead of only opening external routes or appending log text.
- Settings dialog was polished into a Laragon-like General / Services and Ports window.
- Service selection rows now show enable checkbox, port, SSL port and note in one clean row.
- Activity Log content is preserved while switching pages.
- Quick Actions remains above Services in the Overview page.



## v3.58.0 - Package Downloader

- Otomatik package downloader endpointleri eklendi.
- Package registry, cache download ve bin install akisi eklendi.
- Desktop Runtime Versions sayfasina Package Downloader paneli eklendi.

## v3.61.0 - Launcher Bootstrap + GitHub Release Check

- Splash acilis akisi eklendi.
- GitHub latest release kontrolu eklendi.
- MainApp launcher bootstrap akisini baslatacak sekilde guncellendi.
- Gercek updater sonraki guvenli asamaya birakildi.

## v3.61.1 - Splash and Deck UI Polish

- Splash minimum visible duration was added so launcher does not disappear instantly.
- Normal mode desktop window was enlarged for the Studio Deck layout.
- Window title now includes version and Community edition.
- Normal mode header now shows JHoster Desktop, v3.61.1 and Community badge.
- Right side graphical system overview panel was added.
- Stack and open action buttons were recolored and grouped.
- Service start, stop and restart buttons were given clearer visual colors.



## v3.76.0 - Release Cleanup ve API Audit

- Release paketinden 156 adet `__pycache__/*.pyc` dosyasi temizlendi.
- `routes.txt` FastAPI route yuzeyinden yeniden uretildi ve header eklendi.
- Agent API, `routes.txt` ve DesktopApiConfig uyumu icin `test-api-surface-audit.py` eklendi.
- Kritik API endpointleri FastAPI TestClient ile smoke test edildi.
- Release cleanliness guard scripti eklendi.
- Ana sol sidebar, Settings tablari ve Logs tablari korunmustur.

## v3.74.0 - Logs Tabs UI

- Sol sidebar ana menu korunmustur.
- Logs sayfasi uygulama bazli tab menu yapisina alinmistir.
- Desktop, Agent, Apache, Nginx, MySQL, PHP, Mailpit ve System tablari eklenmistir.
- Clear ve Open File aksiyonlari secili tab uzerinden calisir.
- Servis log entry routing Apache/Nginx ayrimi yapacak sekilde guncellenmistir.

## v3.76.0 - Modern Clean UI ve API Kontrol

- Sol sidebar menu gruplari sade hale getirildi.
- Calismayan topbar search/alert/profil gorselleri kaldirildi.
- Topbar canli status kartlarina cevrildi.
- Sadece bilgi veren bazi sayfalar calisan aksiyon kartlariyla guncellendi.
- API audit ve temizlik kontrolu tekrarlandi.
