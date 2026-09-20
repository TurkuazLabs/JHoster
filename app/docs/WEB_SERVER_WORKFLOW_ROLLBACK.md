# 📄 Dosya Yolu: E:\JHoster\docs\WEB_SERVER_WORKFLOW_ROLLBACK.md
# 📌 Amac: Unified web server workflow rollback guard davranisini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Publish sonrasi hata durumunda eski config dosyasina guvenli donus mekanizmasini dokumante eder
# Bagimli Oldugu Katman: View

# Web Server Workflow Rollback Guard

## Amac

Rollback guard, unified web server workflow icinde publish basarili olduktan sonra validate veya reload adiminda hata olusursa sistemi onceki publish durumuna dondurmek icin kullanilir.

## Davranis

- Publish hedefinde eski dosya varsa publisher once backup alir.
- Hata olusursa rollback guard backup dosyasini hedefe geri kopyalar.
- Publish hedefinde eski dosya yoksa ve yeni dosya olusturulmussa rollback guard bu yeni dosyayi kaldirir.
- Rollback sadece JHoster snapshot publish klasorleri icinde calisir.
- Guvensiz path durumunda rollback skipped olur.

## Endpoint

```text
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=true
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=false
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-web-server-workflow-rollback.ps1
```
