# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_REAL_RELOAD.md
# 📌 Amac: Nginx real reload adapter dokumantasyonunu tutar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: nginx.exe tespiti ve real validate sonrasinda nginx -s reload plan/dry-run akisini aciklar
# Bagimli Oldugu Katman: Language

# JHoster Nginx Real Reload

Bu modul, daha once tespit edilen `nginx.exe` kaydi ve real validate kaydi ile `nginx -s reload` adapter akisini hazirlar.

Varsayilan guvenlik davranisi:

- `dry_run=true` ise sadece plan doner.
- `allow_real_execution=false` ise komut calistirilmaz.
- `shell_execution=false` sabittir.
- Gercek reload sadece son real validate kaydi `valid` ise calisabilir.
- Son real validate `execution_skipped`, `invalid` veya `rejected` ise reload reddedilir.
- Komut liste argumanlari ile calistirilir.
- Main config varsayilan yolu: `snapshot\nginx\conf\nginx.conf`
- Main config override icin env key: `JHOSTER_NGINX_MAIN_CONF`

## Endpointler

- `GET /api/v1/nginx-real-reload`
- `GET /api/v1/nginx-real-reload/{project_code}`
- `GET /api/v1/nginx-real-reload/{project_code}/plan`
- `POST /api/v1/nginx-real-reload/{project_code}/reload?dry_run=true&allow_real_execution=false`

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-reload.ps1
```

## Real Calistirma Notu

Gercek calistirma icin su kosullar gerekir:

1. `nginx.exe` daha once detect edilmis olmali.
2. Publish edilmis vhost config dosyasi mevcut olmali.
3. Main `nginx.conf` mevcut olmali.
4. Son real validate kaydi `valid` olmali.
5. `dry_run=false` olmali.
6. `allow_real_execution=true` olmali.

Bu surumde varsayilan test akisi real execution yapmaz.
