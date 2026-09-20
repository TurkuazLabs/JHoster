# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_EXECUTABLE.md
# 📌 Amac: JHoster Nginx executable tespit katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 3.18.0
# Aciklama: Nginx real adapter oncesi nginx.exe path tespit endpointlerini ve guvenlik sinirlarini aciklar
# Bagimli Oldugu Katman: View

# Nginx Executable Detection

Bu modul Nginx real adapter icin `nginx.exe` dosyasinin nerede oldugunu shell komutu calistirmadan tespit eder.

## Guvenlik

- Varsayilan olarak shell komutu calistirilmaz.
- `nginx -v` ve `nginx -t` sadece command label olarak planlanir.
- Snapshot test adayi `snapshot/nginx/bin/nginx.exe` altindadir.
- Env path icin `JHOSTER_NGINX_EXE` okunur.
- Dosya adi `nginx.exe` degilse guvenli kabul edilmez.

## Endpointler

```text
GET  /api/v1/nginx-executable
GET  /api/v1/nginx-executable/latest
GET  /api/v1/nginx-executable/plan
POST /api/v1/nginx-executable/detect?dry_run=true
POST /api/v1/nginx-executable/detect?dry_run=false
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-executable.ps1
```

## Beklenen sonuc

- Plan sonucu `status: planned` doner.
- Detect sonucu `status: detected` doner.
- `shell_execution: false` kalir.
- `real_nginx_execution: false` kalir.
- Registry kaydi `data/jhoster/nginx_executable_registry.json` icinde tutulur.
