# 📄 Dosya Yolu: E:\JHoster\docs\DESKTOP_WORKFLOW_BRIDGE.md
# 📌 Amac: JavaFX Desktop unified web server workflow bridge kullanimini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Desktop tarafindan active profile, plan, dry-run, run listesi ve lock listesi endpointlerinin nasil kullanildigini dokumante eder
# Bagimli Oldugu Katman: View

# Desktop Workflow Bridge

## Amac

v3.34.0 ile JavaFX Desktop paneline unified web server workflow bridge eklendi.

Bu katman agent tarafindaki su endpointleri desktop arayuzunden kullanir:

- `GET /api/v1/web-server-profiles/current`
- `GET /api/v1/web-server-workflow/{project_code}/plan`
- `POST /api/v1/web-server-workflow/{project_code}/run`
- `GET /api/v1/web-server-workflow/runs`
- `GET /api/v1/web-server-workflow/locks`

## Guvenli Varsayilanlar

Desktop uzerinden calisan workflow aksiyonu varsayilan olarak guvenli modda kalir:

- `dry_run=true`
- `allow_real_execution=false`
- `reload=true`
- `rollback_on_failure=true`

Bu nedenle Desktop tarafindaki `Dry Run Workflow` butonu gercek Nginx veya Apache reload islemi calistirmaz.

## Yeni Desktop Katmanlari

- `desktop/src/main/java/com/jhoster/desktop/config/DesktopApiConfig.java`
- `desktop/src/main/java/com/jhoster/desktop/models/DesktopHttpResult.java`
- `desktop/src/main/java/com/jhoster/desktop/models/WebServerWorkflowRequest.java`
- `desktop/src/main/java/com/jhoster/desktop/tools/HttpRequestTool.java`
- `desktop/src/main/java/com/jhoster/desktop/bin/WebServerWorkflowDesktopService.java`
- `desktop/test-workflow-bridge-compile.ps1`

## UI Alanlari

Desktop ana ekrana yeni `Unified Workflow Bridge` karti eklendi.

Kart alanlari:

- Project Code
- Domain
- Port
- Target Dir

Kart aksiyonlari:

- Dry Run Workflow
- Plan Workflow
- Active Profile
- Workflow Runs
- Workflow Locks

## Sonraki Adim

Bir sonraki surumde bu bridge uzerine async UI task katmani eklenebilir. Boylece HTTP istekleri JavaFX UI thread uzerinde bloklama yapmadan calisir.
