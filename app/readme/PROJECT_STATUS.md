# 📄 Dosya Yolu: E:\JHoster\readme\PROJECT_STATUS.md
# 📌 Amac: JHoster mevcut proje durumunu ozetler
# 📌 Modul - Markdown
# Version: 3.40.0
# Aciklama: Aktif ozellikler ve desktop service manager UI sonrasi adimi listeler
# Bagimli Oldugu Katman: View

# Project Status

## Aktif ozellikler

- Python FastAPI agent
- JavaFX launcher
- Component manifest catalog
- Safe plan executor
- Cache, checksum, safe extract
- App registry
- Process manager iskeleti
- Service adapter layer
- Local package installer
- Runtime version manager
- Project manager
- Virtual host generator
- Nginx publish/validate/reload
- Nginx real validate/reload adapter guard
- Nginx execution preflight
- Hosts publish snapshot
- Hosts apply admin/backup/rollback
- Web server profile selector
- Apache vhost/publish/validate/real reload foundation
- Unified web server workflow
- Unified workflow rollback guard
- Unified workflow run tracking
- Unified workflow lock guard
- JavaFX desktop workflow bridge
- JavaFX desktop workflow summary UI
- JavaFX desktop service manager UI
- Apache, Nginx, MySQL ve PHP safe state control

## Guncel endpoint

```text
/api/v1/web-server-workflow
/api/v1/web-server-workflow/{project_code}/run
/api/v1/web-server-workflow/{project_code}/rollback
/api/v1/web-server-workflow/runs
/api/v1/web-server-workflow/locks
```

## Sonraki adim

Service Manager icin real Windows process adapter katmani ve runtime path detection baglanacak.

## v3.31.0

- `rollback_on_failure=true` varsayilan guard olarak eklendi.
- Publish sonrasi validate veya reload hatasinda config geri alinabilir hale geldi.
- Manuel rollback endpointi eklendi.


## v3.34.0 Desktop Workflow Bridge

- JavaFX Desktop ana ekrana unified workflow bridge karti eklendi.
- Active profile, plan, dry-run, runs ve locks aksiyonlari Desktop uzerinden calisir hale geldi.
- Desktop API config, HTTP tool ve workflow modelleri eklendi.
- Guvenli varsayilanlar korundu: `dry_run=true`, `allow_real_execution=false`.

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\test-workflow-bridge-compile.ps1
```


## v3.34.1 Desktop CSS Warning Patch

- JavaFX CSS parser uyarisina neden olan font weight degeri duzeltildi.
- Desktop CSS guard testi eklendi.
- `run-desktop-javafx.ps1` scriptinde `JAVA_HOME` ayarlama sirasi duzeltildi.

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\test-css-syntax-guard.ps1
```


## v3.35.0 Desktop Workflow Summary UI

- Workflow bridge kartina profile, status, run count, lock count, step count ve last run ozetleri eklendi.
- `WorkflowDesktopSummary` modeli eklendi.
- `JsonTextExtractorTool` ile agent cevaplari dis bagimlilik olmadan okunur hale geldi.
- `WorkflowResultFormatterService` ile ham API cevaplari okunabilir summary loga donusturuldu.

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\test-workflow-summary-compile.ps1
```


## v3.36.0 Desktop Service Manager UI

- Desktop ana ekrana Service Manager paneli eklendi.
- Apache, Nginx, MySQL ve PHP icin status/start/stop/restart aksiyonlari eklendi.
- Agent app registry icine varsayilan service kayitlari eklendi.
- Bu surum real process calistirmaz; guvenli simulated state ile Laragon benzeri kontrol deneyimi baslatir.

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\test-service-manager-compile.ps1
```


## v3.37.0 Process Real Preflight Guard

Durum: tamamlandi.

Bu surum Service Manager'i gercek process yonetimine hazirlar. Varsayilan operasyon simulated state olarak kalir. Real execution icin hem `allow_real_execution=true` hem de app registry icinde `real_process.enabled=true` gerekir.


## v3.40.0 Real Process Profile

Service Manager status akisi real process inspection ile guclendirildi. Desktop status butonu artik inspect endpointini kullanir. Real execution default kapali kalmaya devam eder.

## v3.40.0 Service Manager Real Process Profile

- Real process profil endpointleri eklendi.
- Servis install path ve enable ayari dry-run guard ile yonetilir.
- Real start/stop hala ayrica allow guard ister.
