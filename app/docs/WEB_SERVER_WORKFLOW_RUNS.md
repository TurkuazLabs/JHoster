# 📄 Dosya Yolu: E:\JHoster\docs\WEB_SERVER_WORKFLOW_RUNS.md
# 📌 Amac: Unified web server workflow run tracking kullanimini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Run id, run listesi, proje bazli gecmis ve run detay endpointlerini dokumante eder
# Bagimli Oldugu Katman: View

# Web Server Workflow Run Tracking

## Amac

Unified workflow artik her calisma icin `run_id` uretir. Bu sayede JavaFX veya PHP panel tarafinda sonucun tek seferlik cevap olarak kaybolmasi engellenir.

## Endpointler

```text
GET /api/v1/web-server-workflow/runs
GET /api/v1/web-server-workflow/runs?project_code=demo-site
GET /api/v1/web-server-workflow/runs?status=completed
GET /api/v1/web-server-workflow/runs/{run_id}
GET /api/v1/web-server-workflow/{project_code}/runs
```

## Run Kaydi

Her run kaydi su alanlari tasir:

```text
run_id
project_code
web_server
status
message
reload_requested
allow_real_execution
rollback_on_failure
target_dir
steps
step_count
started_at
finished_at
stored_at
```

## Step Log

Her step su alanlarla saklanir:

```text
step_index
name
success
status
message
recorded_at
result
```

## Guvenlik

Bu katman sadece workflow kayitlarini okur. Gercek web server reload islemi yine `allow_real_execution=true` olmadan yapilmaz.
