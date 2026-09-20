# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_REAL_RELOAD.md
# 📌 Amac: Apache real reload adapter davranisini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: httpd restart/reload guard, dry-run ve explicit execution politikasini belgeler
# Bagimli Oldugu Katman: Tool

# Apache Real Reload Adapter

Bu modul Apache tarafinda gercek reload/restart komutunu dogrudan acmaz.
Once publish, executable detect ve real validate kaydi kontrol edilir.

## Guvenlik Kurallari

- Varsayilan `dry_run=true`.
- Varsayilan `allow_real_execution=false`.
- Shell kullanilmaz.
- Son Apache real validate kaydi `valid` degilse reload reddedilir.
- `execution_skipped` validate kaydi reload icin yeterli degildir.

## Komut Plani

```text
httpd -k restart -f <main httpd.conf>
```

## Endpointler

- `GET /api/v1/apache-real-reload`
- `GET /api/v1/apache-real-reload/{project_code}`
- `GET /api/v1/apache-real-reload/{project_code}/plan`
- `POST /api/v1/apache-real-reload/{project_code}/reload?dry_run=true`
- `POST /api/v1/apache-real-reload/{project_code}/reload?dry_run=false&allow_real_execution=false`

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-apache-real-reload.ps1
```
