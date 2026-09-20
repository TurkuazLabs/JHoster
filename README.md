# 📄 Dosya Yolu: E:\JHoster\README.md
# 📌 Amac: JHoster sade root layout ana okuma dosyasi
# 📌 Modul - Markdown
# Version: 3.76.1
# Aciklama: JHoster root klasorleri, agent, desktop, sol menu UI, Settings/Logs tablari, release cleanup, API audit ve source header path tutarlilik patch akisini aciklar

Bagimli Oldugu Katman: Service | Tool | Config | View

# JHoster

JHoster, Laragon benzeri ama API-first ve moduler bir local development manager hedefler.

## Root layout

```text
E:\JHoster\
├─ app\
├─ bin\
├─ data\
├─ etc\
├─ logs\
├─ tmp\
├─ www\
├─ backup\
└─ cache\
```

## Ana konumlar

- Agent: `E:\JHoster\app\agent`
- Desktop: `E:\JHoster\app\desktop`
- Portable araclar: `E:\JHoster\bin`
- Projeler: `E:\JHoster\www`
- State: `E:\JHoster\data\jhoster`
- Config: `E:\JHoster\etc`

## Calistirma

Agent:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\run-agent.ps1
```

Desktop:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\commands\run-desktop-javafx.ps1
```



## v3.76.1 Source Header ve Roadmap Patch

- Aktif Desktop Java ve Agent Python kaynaklari icin tam `E:\JHoster\...` header path standardi denetlenir.
- Desktop service/repository/tool katmaninda eski `bin` ve eksik `app` path header kayitlari duzeltildi.
- Roadmap icindeki tamamlanmis `v3.76.0` maddesinin yanlislikla Siradaki bolumunde tekrar etmesi duzeltildi.
- Yeni source header path guard release oncesi tekrar calistirilabilir.

## v3.73.1 Modern Command Center UI

- JHoster normal acilis akisi modern Command Center yapisina cevrildi.
- Tab menu kaldirma karari korunmustur; normal UI tek akisli fullscreen paneldir.
- Ust bolume modern hero alani, Environment Snapshot kartlari ve preset bilgi kartlari eklendi.
- New Site Wizard bolumu daha premium kart/pill gorunumuyle guncellendi.
- Apache/Nginx, MySQL, PHP ve Mailpit stack secimleri korunarak daha okunur hale getirildi.
- License, hosts auto, package center ve service manager akislarina dokunulmadan UI/UX katmani iyilestirildi.
- Light tema korunmustur.

## v3.68.0 Hosts Auto UI

- New Test Site kartina hosts auto saglik rozeti ve Inspect Hosts butonu eklendi.
- Settings penceresine yeni `Hosts` sekmesi eklendi.
- Desktop artik `/api/v1/hosts-auto/inspect`, `/repair-plan` ve `/repair` endpointlerini UI uzerinden cagirabilir.
- Repair Hosts gercek Windows hosts dosyasi icin `real_write=true&dry_run=false` kullanir; Windows admin yetkisi yoksa agent rejected sonucu dondurur.
- Inspect cevabina UI icin `missing_count`, `stale_count`, `wrong_ip_count` ve `duplicate_count` alanlari eklendi.

## v3.67.0 Hosts Auto Inspect ve Repair

- Hosts auto artik sadece yazma yapmaz; mevcut managed blok ile proje registry arasindaki farki denetler.
- Yeni endpointler:
  - `GET /api/v1/hosts-auto/inspect`
  - `GET /api/v1/hosts-auto/repair-plan`
  - `POST /api/v1/hosts-auto/repair`
- Inspect sonucu missing, stale, wrong IP, duplicate ve external conflict listelerini dondurur.
- Repair akisi once inspect yapar; eksik veya eski kayit varsa sadece JHoster managed blokunu yeniden yazar.
- Laragon, Docker veya manuel hosts kayitlari managed blok disinda korunur.

## v3.66.0 Hosts Auto Sync ve New Test Site

- Quick App karti New Test Site akisi olarak sadeleştirildi.
- Site olusturma sonrasi domain bilgisi JHoster managed hosts blok planina baglandi.
- Yeni endpointler:
  - `GET /api/v1/hosts-auto`
  - `GET /api/v1/hosts-auto/latest`
  - `GET /api/v1/hosts-auto/plan`
  - `POST /api/v1/hosts-auto/sync`
- Varsayilan snapshot test modu `snapshot/hosts/hosts-auto/hosts.jhoster` dosyasina yazar.
- Gercek Windows hosts yazimi icin Windows + admin yetkisi gerekir.
- Gercek dosya yaziminda once backup alinir, sonra sadece `# BEGIN JHOSTER AUTO HOSTS` ve `# END JHOSTER AUTO HOSTS` arasindaki blok degistirilir.

Ornek managed blok:

```text
# BEGIN JHOSTER AUTO HOSTS
127.0.0.1      demo-quick-app.test      #jhoster:auto:demo-quick-app
# END JHOSTER AUTO HOSTS
```

## v3.51.0 Desktop Laragon UI

- Compact service rows include Start, Stop and Restart.
- Quick Actions now appear as a dashboard dock.
- Portable Tools dock includes Bin, Cmder, Git Bash, Notepad++, Ngrok, Composer and Yarn.
- Database action keeps opening HeidiSQL Portable from `bin/heidisql/heidisql.exe`.


## v3.52.0 Clean Desktop Dashboard

- Ana dashboard tek ekranda sade bilgi mimarisine cekildi.
- Uzun dikey panel kalabaligi kaldirildi; ileri moduller tab navigasyonuna tasindi.
- Services alani tablo duzenine alindi: servis, rol, durum, versiyon, port ve kontroller tek satirda gosterilir.
- Quick Actions, Activity Log ve System Overview alt bolumde yan yana toplandi.
- Veritabani butonu HeidiSQL Portable davranisini korur.

## v3.53.0 Button Wiring Revision

- Clean dashboard tablari ve sol menu artik action handler ile calisir.
- Services refresh, manage services, start, stop ve restart aksiyonlari agent process API akisi ile baglidir.
- Quick Actions alanindaki Web, Database, Terminal, Root, Logs ve Settings aksiyonlari desktop tool katmanina baglandi.
- Planned runtime servisleri safe state-control modunda start/stop/restart ile durum guncelleyebilir.


## v3.53.1 Web Server Port Guard

- Apache ve Nginx 80/443 public portlarini ayni anda kullanamayacak sekilde guard eklendi.
- Start All Apache, MySQL, PHP ve Mailpit baslatir; Nginx otomatik baslatilmaz.
- Nginx kullanmak icin once Apache durdurulur, sonra Nginx baslatilir.


## v3.54.0 Active Web Server Mode Settings

- Apache/Nginx secimi Ayarlar/System Overview alanindan yapilabilir hale getirildi.
- Secili web server calisir; diger web server 80/443 icin otomatik disarida kalir.
- Start All artik secili web server profilini okur ve sadece onu baslatir.
- Apache ve Nginx ortak proje kokunu kullanir: `E:\JHoster\www`.
- Backend process guard, secili profil disindaki web server start/restart isteklerini bloke eder.
- Profil secimi `data/jhoster/web_server_profile_registry.json` icinde saklanir.

## v3.55.1 Settings Menu Service Selection

- Settings butonu artik klasor acmak yerine Laragon benzeri ayar penceresi acar.
- Ayar penceresinde General ve Services and Ports sekmeleri bulunur.
- Apache veya Nginx aktif web server olarak secilebilir; ikisi ayni anda 80/443 icin baslatilmaz.
- Start All kapsaminda Apache, Nginx, MySQL, PHP ve Mailpit servislerinin calisip calismayacagi secilebilir.
- Secimler `data/jhoster/desktop_service_selection_settings.json` dosyasinda saklanir.
- Secili web server ortak `E:\JHoster\www` dokuman kokunu kullanir.

## v3.55.1 Quick Actions Above Services

- Quick Actions paneli Services tablosunun ustune tasindi.
- Dashboard akis sirasi artik: Topbar, Summary, Tabs, Quick Actions, Services, Activity Log, System Overview.
- Sik kullanilan Start All, Stop All, Web, Database, Terminal, Root ve Logs aksiyonlari daha erken gorunur.
- Laragon benzeri Settings penceresi ve servis secim ayarlari korunur.
## v3.56.0 UI Completion and Dynamic Pages

Bu surumde dashboard artik tek uzun sayfa gibi davranmaz. Sol menu ve ust tablar gorunen icerigi degistirir. Settings penceresi Laragon benzeri General / Services and Ports yapisina guncellendi. Quick Actions, Services ustunde kalir. Activity Log sayfalar arasinda korunur.



## v3.58.0 Package Downloader

JHoster artik paketleri once `cache/downloads` altina indirebilir ve sonra hedef `bin` klasorune kurabilir. Ilk akista `Runtime Versions` sayfasindaki `Package Downloader` paneli kullanilir.

Temel endpointler:

- `GET /api/v1/package-downloads`
- `GET /api/v1/package-downloads/{package_code}/plan`
- `POST /api/v1/package-downloads/{package_code}/download?dry_run=false`
- `POST /api/v1/package-downloads/{package_code}/install?dry_run=false`

Registry dosyasi:

- `E:\JHoster\data\jhoster\package_download_registry.json`

Indirme hedefi:

- `E:\JHoster\cache\downloads`

Kurulum hedefi:

- `E:\JHoster\bin`

## v3.58.0 Package Downloader Controller Fix

- Package Downloader UI butonlari icin Controller wrapper eksigi giderildi.
- Maven compile hatasi `appendPackageDownloadSummary` duzeltildi.


## v3.58.0 Dev Mode Gate

- Normal acilista raw API endpoint butonlari gizlidir.
- Developer Tools menusu sadece Dev Mode aktifken gorunur.
- Dev Mode acmak icin JHoster acilirken Shift basili tutulabilir.
- Alternatif acilislar: `--dev`, `-Djhoster.dev=true`, `JHOSTER_DEV_MODE=1`.
- Bu sayede `api/v1/web-server-profiles` gibi dahili endpoint kisayollari normal kullanici panelini kalabaliklastirmaz.

## v3.60.0 Visible Dev Mode UX Patch

- Normal mod sade kalir.
- Shift basili acilista sol menude `Developer Tools` ayri `DEVELOPER` grubu altinda gorunur.
- Ust barda `DEV MODE ACTIVE` rozeti gorunur.
- Settings penceresinde sadece Dev Mode acikken `Developer` sekmesi gorunur.
- Raw agent endpoint butonlari normal kullanici ekraninda gizli kalir.


## v3.60.0 JHoster Deck UI

- Normal mode now uses a compact JHoster Deck layout instead of the full developer dashboard.
- Apache and Nginx are represented as one Web Server row in normal mode.
- The selected web server owns the shared 80/443 ports and the shared www folder.
- The inactive web server stays hidden from normal daily control and remains available through settings or Dev Mode.
- Dev Mode keeps the advanced dashboard, package downloader, workflow, diagnostics and raw endpoint buttons.


## v3.62.9 Launcher Bootstrap

JHoster artik once splash launcher akisi ile baslar. GitHub latest release kontrolu icin `-Djhoster.update.repo=owner/repo` veya `JHOSTER_UPDATE_REPO=owner/repo` kullanilabilir. Repo tanimli degilse kontrol atlanir ve desktop acilir.

## v3.63.0 Community Plan Gate

- Community plan icin 5 aktif proje/site limiti eklendi.
- Pro plan icin sinirsiz proje altyapisi merkezi plan gate servisine hazirlandi.
- Agent tarafinda `/api/v1/license` endpointi eklendi.
- Quick App create ve Project create akislarinda servis katmaninda limit kontrolu eklendi.
- Mevcut menu ve ana UI akisi korunarak sadece create akisi guvenlik kapisina baglandi.
- `data/jhoster/license_state.json` varsayilan olarak Community plan ile gelir.

## v3.64.0 License Status UI

- Desktop tarafina LicensePlanSummary modeli eklendi.
- Agent `/api/v1/license` cevabi plan etiketi, kullanim etiketi, upgrade hint ve Pro feature flag alanlariyla genisletildi.
- Normal JHoster Deck header icinde `Community | Sites 0 / 5` benzeri kullanim rozeti gorunur hale getirildi.
- Settings penceresine ana menu bozulmadan `License` sekmesi eklendi.
- Dashboard refresh ve Check Status aksiyonlari lisans durumunu da yeniler.
- Pro gecis mesaji UI tarafinda merkezi license ozetinden okunur.

## v3.65.0 Pro Feature Registry UI

- Agent `/api/v1/license` cevabi `feature_registry` listesiyle genisletildi.
- Feature registry icinde Core ve Pro Module ayrimi yapildi.
- Community icin 5 aktif site Core ozellik olarak `Included` doner.
- Advanced SSL, Automated Backup, Advanced DNS ve AI / Ollama modulleri Community planda `Pro Locked` olarak isaretlenir.
- Desktop Settings > License sekmesine feature registry satirlari eklendi.
- Mevcut ana menu ve JHoster Deck akisi korunur; yeni kalabalik menu eklenmez.


## v3.73.1 - Fullscreen No-Tab Stack Wizard

- JHoster Desktop artik acilista maximized/fullscreen panel gibi acilir.
- Normal moddaki ana tab menu kaldirildi; New Site, Services, Package Center ve Logs tek sayfa akista gosterilir.
- New Site Wizard icine stack secimi eklendi: Apache veya Nginx, MySQL, PHP ve Mailpit.
- Quick App plan/create endpointleri `web_server`, `include_mysql`, `include_php`, `include_mailpit` parametrelerini kabul eder.
- Secilen stack `stack_plan`, `stack_label`, proje registry ve `.jhoster.yml` scaffold metadata alanlarina yazilir.
- Bu surum runtime download/installer baglantisini baslatmaz; stack secimini UI + API + registry katmanina baglar.

## v3.73.1 Left Sidebar UI

- Normal mod sol sidebar menu ile acilir.
- Kalabalik Command Center hero akisi kaldirildi.
- New Site sol menude ana giris noktasi oldu.
- Sag icerik alani sadece secilen bolumu gosterir.
- Stack secimli New Site wizard korunur.

## v3.73.1 Settings Tab Menu UI

Bu surumde ana sol sidebar menu korunmustur. Settings penceresi icinde tab menu tekrar kullanilmistir. General, Services, License, Hosts, Appearance ve Advanced ayarlari birbirinden ayrilarak ayar penceresi daha okunur hale getirilmistir.


## v3.76.0 - Release Cleanup ve API Audit

- Release paketinden gereksiz `__pycache__` ve `.pyc` dosyalari temizlendi.
- `app/agent/routes.txt` FastAPI route yuzeyinden yeniden uretildi.
- Agent API, `routes.txt` ve DesktopApiConfig endpoint sabitleri icin audit testi eklendi.
- Kritik GET/POST endpointleri FastAPI TestClient ile smoke test edildi.
- Sol sidebar ana UI, Settings tablari ve Logs tablari korunmustur.

## v3.74.0 - Logs Tabs UI

- Ana sol menu korunmustur.
- Logs bolumu uygulama bazli tab menu yapisina alinmistir.
- Apache, Nginx, MySQL, PHP, Mailpit, Agent, Desktop ve System loglari ayri tablarda gosterilir.
- Secili tab icin Clear ve Open File aksiyonlari desteklenir.

## v3.76.0 - Modern Clean UI ve API Kontrol

- Sol menu daha okunur gruplara ayrildi: Create, Operate, Resources, Observe.
- Calismayan topbar arama, fake alert ve profil pill kaldirildi.
- Topbar artik Plan, Sites, Hosts ve Engine durumlarini gosterir.
- Projects, Virtual Hosts ve Apps sayfalari calisan aksiyon kartlariyla guncellendi.
- API surface audit ve gereksiz dosya temizligi tekrar kontrol edildi.
