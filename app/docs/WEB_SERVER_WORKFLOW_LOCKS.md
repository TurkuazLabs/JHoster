# 📄 Dosya Yolu: E:\JHoster\docs\WEB_SERVER_WORKFLOW_LOCKS.md
# 📌 Amac: Unified web server workflow lock guard kullanimini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Ayni proje icin es zamanli workflow calismalarini engelleyen lock katmanini dokumante eder
# Bagimli Oldugu Katman: View

# Web Server Workflow Lock Guard

## Amac

Unified workflow `dry_run=false` calistiginda proje bazli aktif lock alir. Boylece ayni proje icin ikinci bir generate -> publish -> validate -> reload akisi ayni anda baslatilmaz.

## Davranis

- `dry_run=true` ve plan endpointleri lock kullanmaz.
- `dry_run=false` run baslarken lock alir.
- Workflow bitince lock otomatik release edilir.
- Aktif lock varsa yeni run `web_server_workflow_locked` hatasi ile engellenir.
- Sistem takilmis lock icin manuel `force=true` unlock endpointi sunar.

## Endpointler

```text
GET  /api/v1/web-server-workflow/locks
GET  /api/v1/web-server-workflow/{project_code}/lock
POST /api/v1/web-server-workflow/{project_code}/unlock?run_id=manual-lock-001&force=false
POST /api/v1/web-server-workflow/{project_code}/unlock?force=true
```

## Lock Kaydi

```text
project_code
run_id
web_server
status
locked_at
```

## Guvenlik Notu

`force=true` sadece takilmis lock kurtarmak icin kullanilmalidir. Normal workflow sonunda release islemi servis tarafinda otomatik yapilir.
