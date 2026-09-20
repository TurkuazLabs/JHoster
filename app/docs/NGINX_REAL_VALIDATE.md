# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_REAL_VALIDATE.md
# 📌 Amac: Nginx real validate adapter dokumantasyonunu tutar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: nginx.exe tespiti sonrasi nginx -t plan, dry-run ve izinli calistirma akisini aciklar
# Bagimli Oldugu Katman: Language

# JHoster Nginx Real Validate

Bu modul, daha once tespit edilen `nginx.exe` kaydi ile publish edilmis virtual host config dosyasini gercek `nginx -t` adapter akisi icin hazirlar.

Varsayilan guvenlik davranisi:

- `dry_run=true` ise sadece plan doner.
- `allow_real_execution=false` ise komut calistirilmaz.
- `shell_execution=false` sabittir.
- Komut liste argumanlari ile calistirilir.
- Main config varsayilan yolu: `snapshot\nginx\conf\nginx.conf`
- Main config override icin env key: `JHOSTER_NGINX_MAIN_CONF`

## Endpointler

- `GET /api/v1/nginx-real-validate`
- `GET /api/v1/nginx-real-validate/{project_code}`
- `GET /api/v1/nginx-real-validate/{project_code}/plan`
- `POST /api/v1/nginx-real-validate/{project_code}/validate?dry_run=true&allow_real_execution=false`

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-validate.ps1
```

## Real Calistirma Notu

Gercek calistirma icin su kosullar gerekir:

1. `nginx.exe` daha once detect edilmis olmali.
2. Publish edilmis vhost config dosyasi mevcut olmali.
3. Main `nginx.conf` mevcut olmali.
4. `dry_run=false` olmali.
5. `allow_real_execution=true` olmali.

Bu surumde varsayilan test akisi real execution yapmaz.
