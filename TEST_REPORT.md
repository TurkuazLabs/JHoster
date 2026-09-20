# 📄 Dosya Yolu: E:\JHoster\TEST_REPORT.md
# 📌 Amac: JHoster v3.76.1 test raporu
# 📌 Modul - Markdown
# Version: 3.76.1
# Aciklama: Release cleanup, API route audit, Logs tab UI, Community plan gate ve temel static testleri kaydeder

Bagimli Oldugu Katman: Service | Tool | Config | View



## v3.76.1 Source Header ve Roadmap Tutarlilik Patch

- Desktop aktif Java source header path audit: basarili.
- Agent aktif Python source header path audit: basarili.
- Eski `desktop/bin` ve eksik `app/desktop` header path kayitlari duzeltildi.
- Roadmap icindeki `v3.76.0` tamamlandi/siradaki cakismasi giderildi; yeni fonksiyonel adim `v3.77.0` olarak ayrildi.
- Python compileall: basarili.
- FastAPI API surface audit: basarili.
- Desktop hedefli non-JavaFX javac compile: basarili.
- Tam JavaFX/Maven compile bu ortamda JavaFX/JNA bagimliliklari ve Maven olmadigi icin calistirilmadi.
- Release cleanliness: test sonrasi uretilen cache dosyalari temizlenerek basarili.

## v3.76.0 Release Cleanup ve API Audit

- Gereksiz dosya kontrolu: 156 adet `__pycache__/*.pyc` release paketinden temizlendi.
- Release cleanliness guard: basarili.
- Python compileall: basarili.
- FastAPI main import: basarili.
- FastAPI route sayisi: 149.
- `routes.txt` ile FastAPI route listesi: birebir uyumlu.
- DesktopApiConfig route sabitleri ile FastAPI route listesi: uyumlu.
- Kritik API smoke endpointleri: 45 kontrol, 0 hata.
- Hosts Auto inspect/repair dry-run endpointleri: basarili.
- Quick App stack plan/create dry-run endpointleri: basarili.
- LauncherView brace/parantez denge kontrolu: basarili.
- CSS brace denge kontrolu: basarili.
- Tam JavaFX/Maven compile bu ortamda calistirilamadi.

## v3.71.0 Modern Command Center UI

- LauncherView brace/parantez denge kontrolu: basarili.
- CSS brace denge kontrolu: basarili.
- Modern Command Center statik token kontrolu: basarili.
- LauncherView icinde `TabPane` / `new Tab` bulunmadigi kontrol edildi: basarili.
- Python compileall: basarili.
- FastAPI main import ve route kontrolu: basarili.
- Desktop License/HostsAuto servisleri onceki parcali javac kapsaminda korunmustur.
- Desktop JavaFX tam compile bu ortamda JavaFX kutuphaneleri olmadigi icin calistirilamadi.
- Maven tam compile bu ortamda mvn kurulu olmadigi icin calistirilamadi.

## v3.68.0 Hosts Auto UI

- Python compileall: basarili.
- FastAPI TestClient `/api/v1/hosts-auto/inspect?real_write=false`: basarili.
- FastAPI TestClient `/api/v1/hosts-auto/repair-plan?real_write=false`: basarili.
- FastAPI TestClient `/api/v1/hosts-auto/repair?real_write=false&dry_run=true`: basarili.
- Hosts auto inspect UI count alanlari: basarili.
- Desktop `HostsAutoSummary`, `HostsAutoResultFormatterService`, `HostsAutoDesktopService` parcali javac: basarili.
- Tam JavaFX compile bu ortamda JavaFX kutuphaneleri olmadigi icin calistirilamadi.
- Tam Maven compile bu ortamda `mvn` kurulu olmadigi icin calistirilamadi.

## v3.67.0 Hosts Auto Inspect ve Repair

- Python compileall: basarili.
- FastAPI main import: basarili.
- `/api/v1/hosts-auto/inspect` route kaydi: basarili.
- Snapshot inspect missing domain testi: basarili.
- Snapshot repair dry_run=false yazim testi: basarili.
- Repair sonrasi inspect repair_required=false testi: basarili.
- DesktopApiConfig hosts auto repair route parcali javac: basarili.
- Tam Maven compile bu ortamda mvn olmadigi icin calistirilamadi.

## v3.66.0 Hosts Auto Sync

- Python compileall: Basarili.
- FastAPI main import: Basarili.
- `/api/v1/hosts-auto` route kayitlari: Basarili.
- Hosts auto snapshot sync servis testi: Basarili.
- `data/jhoster/hosts_auto_registry.json` default registry eklendi.
- Desktop `LauncherView` version ve New Test Site label guncellemesi yapildi.
- DesktopApiConfig javac compile: Basarili.
- LauncherView brace/parantez denge kontrolu: Basarili.
- Tam Maven compile bu ortamda calistirilmadi; Maven kurulu degil.

## Testler

- Python compile: Basarili
- FastAPI import: Basarili
- FastAPI route sayisi: 149
- Folder layout endpointleri: Basarili
- Folder layout dry-run apply: Basarili
- Portable version summary: Basarili
- Project dry-run: Basarili
- Quick App dry-run: Basarili
- Desktop QuickActionTool compile: Basarili

## Not

Maven runtime testi bu ortamda calistirilmadi; Maven kurulu degil.


## v3.51.0 Static Review

- LauncherView setter coverage checked for all LauncherController handler calls.
- Java brace and parenthesis balance checked for updated Desktop files.
- Maven compile was not executed in this environment because Maven is not installed.
- Added `app/desktop/test-laragon-ui-compile.ps1` for local Maven verification.


## v3.52.0 Static Review

- LauncherView clean dashboard render akisi eklendi.
- Eski uzun dikey panel akisi ana dashboarddan kaldirildi.
- Java brace balance kontrolu basarili.
- Maven compile bu ortamda calistirilmadi; Maven kurulu degil.
- Lokal dogrulama icin `app/desktop/test-clean-dashboard-compile.ps1` eklendi.


## v3.53.0 Static Review

- LauncherView icindeki tum Button field alanlari icin setOnAction veya setButtonAction coverage kontrol edildi.
- LauncherController tarafindan cagrilan tum LauncherView setter metodlari bulundu.
- QuickActionDesktopService cagrilari icin eksik public method kontrolu yapildi.
- Java brace balance kontrolu basarili.
- Python adapter compile kontrolu basarili.
- Maven compile bu ortamda calistirilmadi; Maven kurulu degil.
- Lokal dogrulama icin `app/desktop/test-button-wiring-compile.ps1` eklendi.


## v3.53.1 Web Server Port Guard

- Apache ve Nginx 80/443 public portlarini ayni anda kullanamayacak sekilde guard eklendi.
- Start All Apache, MySQL, PHP ve Mailpit baslatir; Nginx otomatik baslatilmaz.
- Nginx kullanmak icin once Apache durdurulur, sonra Nginx baslatilir.


## v3.54.0 Active Web Server Mode Settings

- Python compile: Basarili.
- `app/agent/test-web-server-mode.py`: Basarili.
- Apache aktifken Nginx start istegi profile mismatch ile bloklandi.
- Nginx aktifken Apache start istegi profile mismatch ile bloklandi.
- Apache secimine geri donulunce Nginx stopped, Apache running durumuna gecti.
- Java brace/parenthesis balance kontrolu basarili.
- Maven compile bu ortamda calistirilmadi; Maven kurulu degil.

## v3.55.1 Settings Menu Service Selection

- DesktopServiceSelectionSettings, DesktopServiceSelectionRepository ve DesktopServiceSelectionService javac compile: Basarili.
- LauncherView ayar penceresi eklendi: General ve Services and Ports sekmeleri.
- Settings ve System Settings butonlari ayar penceresine baglandi.
- Start All akisi servis secim dosyasini okuyacak sekilde guncellendi.
- Secili olmayan veya disabled servislerin Start/Restart butonlari pasif hale getirildi.
- Java brace/parenthesis balance kontrolu basarili.
- Maven compile bu ortamda calistirilmadi; Maven kurulu degil.

## v3.55.1 Quick Actions Above Services

- LauncherView dashboard sirasi statik olarak kontrol edildi.
- Quick Actions panelinin Services panelinden once render edildigi dogrulandi.
- Bottom grid icinde Quick Actions tekrarinin kaldirildigi dogrulandi.
- Java brace/parantez denge kontrolu basarili.
## v3.56.0 UI Completion Check

- Java brace/parantez statik kontrolu basarili.
- Dashboard body dynamic page method coverage kontrolu basarili.
- Settings dialog service selection row kontrolu basarili.
- Log preservation kontrolu basarili.
- Maven bu ortamda yoksa yerelde NetBeans Maven ile calistirilmalidir.



## v3.58.0 Package Downloader

- Python syntax kontrolu hedeflendi.
- Package downloader plan/dry-run testi eklendi: `app/agent/test-package-downloads.ps1`.
- Desktop compile yardimci scripti eklendi: `app/desktop/test-package-downloader-compile.ps1`.
- Gercek download testi kullanici ortaminda internet baglantisi ile calistirilmalidir.

## v3.58.0 Compile Fix

- Statik kontrol: LauncherController icinde `appendPackageDownloadSummary` wrapper metodu mevcut.
- Hedeflenen Maven hatasi: `cannot find symbol appendPackageDownloadSummary` giderildi.


## v3.58.0 Dev Mode Gate

- DevModeTool Java syntax/parantez kontrolu hedeflendi.
- LauncherController dev mode constructor wiring kontrol edildi.
- LauncherView normal modda Developer Tools menusu gizli olacak sekilde guncellendi.
- Raw endpoint butonlari Developer Tools altina tasindi.
- Maven compile kullanici ortaminda tekrar calistirilmalidir.

## v3.60.0 Visible Dev Mode UX Patch

- Java source brace/parantez kontrolu basarili.
- CSS patch eklendi ve stil siniflari LauncherView ile eslestirildi.
- Normal modda Developer Tools menusu gizli kalacak sekilde kaynak kontrolu yapildi.
- Dev Mode acikken Developer Tools, DEV MODE ACTIVE rozeti ve Settings Developer sekmesi gorunur hale getirildi.
- Bu ortamda Maven bulunmadigi icin gercek Maven compile calistirilamadi.


## v3.60.0 JHoster Deck UI Static Checks

- Java brace, parenthesis and square bracket balance checked for LauncherView, LauncherController and FxApplication.
- Normal mode renders a single Web Server row for Apache/Nginx.
- Dev Mode keeps the advanced dashboard and raw API tools behind the startup gate.
- Apache and Nginx continue to use the same public ports in metadata while backend profile and port guards prevent concurrent ownership.


## v3.62.9 Static Test Notes

- Java brace kontrolu basarili.
- Yeni launcher bootstrap dosyalari eklendi.
- GitHub update check repo tanimsizken desktop acilisini bloke etmeyecek sekilde tasarlandi.
- Maven container ortaminda yoktu; kullanici tarafinda NetBeans/Maven ile compile dogrulanacak.

## v3.65.0 Static Test Notes

- Python compile: Basarili.
- License controller import ve direkt endpoint response testi: Basarili.
- `/api/v1/license` response alanlari: `plan_label`, `usage_label`, `upgrade_hint`, `feature_flags` basarili.
- Desktop LicensePlanSummary javac parcali compile: Basarili.
- Desktop LicenseResultFormatterService parser testi: Basarili.
- Desktop LicenseDesktopService javac parcali compile: Basarili.
- LauncherView uzerinde menu bozulmadan header rozeti ve Settings License sekmesi eklendi.
- Tam Maven compile: Bu ortamda `mvn` komutu kurulu olmadigi icin calistirilamadi.

## v3.65.0 Pro Feature Registry Static Test Notes

- Python compile: Basarili.
- PlanGateService `feature_registry` liste testi: Basarili.
- Community plan icin `site_limit=True`, Pro moduller icin `False` feature flag testi: Basarili.
- Desktop LicensePlanSummary javac parcali compile: Basarili.
- Desktop LicenseResultFormatterService feature flag parser smoke testi: Basarili.
- LauncherView brace/parantez denge kontrolu: Basarili.
- Tam Maven compile: Bu ortamda `mvn` komutu kurulu olmadigi icin calistirilamadi.


## v3.72.0 Test Notlari

- Python compileall calistirildi.
- FastAPI import ve quick-app stack query smoke testi calistirildi.
- Quick App plan response icinde stack_plan ve stack_label dogrulandi.
- Desktop QuickAppSummary, QuickAppResultFormatterService ve QuickAppDesktopService parcali javac testi calistirildi.
- LauncherView statik guard ile TabPane main deck kullanimi kaldirildigi dogrulandi.
- Tam JavaFX compile bu ortamda JavaFX kutuphaneleri olmadigi icin calistirilamadi.
- Tam Maven compile bu ortamda mvn kurulu olmadigi icin calistirilamadi.

## v3.73.1 Settings Tab Menu UI

- Sol sidebar ana menu korunarak Settings icinde TabPane yapisi geri alindi.
- General, Services, License, Hosts, Appearance ve Advanced sekmeleri statik olarak dogrulandi.
- Ana ekranda TabPane kullanimi geri getirilmedi; tab menu sadece Settings dialog icinde kullanildi.
- LauncherView brace/parantez denge kontrolu basarili.
- CSS brace denge kontrolu basarili.

## v3.73.1 Desktop API Route Compile Fix

- Hata: `DesktopApiConfig.QUICK_APP_PLAN_ROUTE` eksikti.
- Cozum: Sabit `DesktopApiConfig` icine eklendi.
- Test: `javac DesktopApiConfig.java` basarili.
- Not: Tam Maven compile bu ortamda `mvn` kurulu olmadigi icin calistirilamadi.

## v3.74.0 Logs Tabs UI

- LauncherView brace/parantez denge kontrolu: basarili.
- Logs tab token kontrolu: basarili.
- Logs klasor mapping kontrolu: basarili.
- CSS logs tab token kontrolu: basarili.
- Python compileall: basarili.
- Tam JavaFX/Maven compile bu ortamda calistirilamadi.

## v3.76.0 Modern Clean UI ve API Kontrol

- Modern clean UI guard: basarili.
- Python compileall: basarili.
- FastAPI main import: basarili.
- API surface audit: basarili.
- routes.txt uyumu: basarili.
- Release cleanliness: basarili.
- Tam Maven compile bu ortamda mvn kurulu olmadigi icin calistirilamadi.
