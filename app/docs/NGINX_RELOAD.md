# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_RELOAD.md
# 📌 Amac: JHoster Nginx reload katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 3.15.0
# Aciklama: Validate sonrasi guvenli simulated reload akisinin endpointlerini ve test komutunu aciklar
# Bagimli Oldugu Katman: View

# Nginx Reload

Bu modul publish ve validate islemleri tamamlanan Nginx virtual host config dosyasi icin reload plani uretir.

## Guvenlik

- Gercek shell komutu calistirilmaz.
- Gercek `nginx -s reload` islemi yapilmaz.
- Sadece `snapshot/vhosts/nginx-published` altindaki `.conf` dosyalari kabul edilir.
- Reload icin once basarili validate kaydi gerekir.
- `dry_run=true` varsayilan davranistir.

## Endpointler

```text
GET  /api/v1/nginx-reload
GET  /api/v1/nginx-reload/{project_code}
GET  /api/v1/nginx-reload/{project_code}/plan
POST /api/v1/nginx-reload/{project_code}/reload?dry_run=true
POST /api/v1/nginx-reload/{project_code}/reload?dry_run=false
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-reload.ps1
```

## Beklenen sonuc

- Plan sonucu `status: planned` doner.
- Simulated reload sonucu `status: reloaded` doner.
- `shell_execution: false` kalir.
- Registry kaydi `data/jhoster/nginx_reload_registry.json` icinde tutulur.
