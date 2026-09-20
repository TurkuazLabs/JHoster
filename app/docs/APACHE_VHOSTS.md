# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_VHOSTS.md
# 📌 Amac: JHoster Apache virtual host generator dokumantasyonunu tutar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Apache vhost snapshot uretim akisini, endpointleri ve guvenlik davranisini aciklar
# Bagimli Oldugu Katman: View

# Apache Virtual Hosts

Apache virtual host generator, proje kaydindan Apache uyumlu `.conf` dosyasi uretir.

Bu surumde dosya sadece snapshot altina yazilir:

```text
snapshot/vhosts/apache/{project_code}.conf
```

Gercek Apache config klasorune publish, validate ve reload henuz bu katmanda yoktur.

## Endpointler

```text
GET  /api/v1/apache-vhosts
GET  /api/v1/apache-vhosts/{project_code}
GET  /api/v1/apache-vhosts/{project_code}/plan?domain=demo-site.localhost&port=80
POST /api/v1/apache-vhosts/{project_code}/generate?domain=demo-site.localhost&port=80&dry_run=true
POST /api/v1/apache-vhosts/{project_code}/generate?domain=demo-site.localhost&port=80&dry_run=false
```

## Guvenlik

- Domain icinde `/`, `\`, `:`, `..` engellenir.
- Document root sadece JHoster proje kokunun altinda olabilir.
- Config dosyasi sadece `snapshot/vhosts/apache` altina yazilir.
- Sistem Apache dosyalari degistirilmez.

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-apache-vhosts.ps1
```
