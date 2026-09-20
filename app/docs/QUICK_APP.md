# 📄 Dosya Yolu: E:\JHoster\docs\QUICK_APP.md
# 📌 Amac: JHoster Quick App scaffold akisinin kullanimini anlatir
# 📌 Modul - Markdown
# Version: 3.42.0
# Aciklama: Quick App template listesi, plan ve create endpointleri icin teknik dokuman
# Bagimli Oldugu Katman: View

# Quick App v1

Quick App v1, Laragon'daki Quick App deneyiminin guvenli JHoster karsiligidir.
Bu surum **scaffold-only** calisir. Internetten paket indirmez, Composer/NPM calistirmaz ve sistem PATH ayari degistirmez.

## Template listesi

- `php-empty`
- `laravel`
- `wordpress`
- `opencart-3`
- `node-vite`

## Endpointler

```text
GET  /api/v1/quick-apps
GET  /api/v1/quick-apps/templates
GET  /api/v1/quick-apps/templates/{template_code}
GET  /api/v1/quick-apps/{project_code}
GET  /api/v1/quick-apps/{project_code}/plan
POST /api/v1/quick-apps/{project_code}/create
```

## Plan ornegi

```powershell
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8751/api/v1/quick-apps/demo-quick-app/plan?template_code=opencart-3&project_name=Demo%20OpenCart&domain=demo-quick-app.test&port=80"
```

## Create dry-run ornegi

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8751/api/v1/quick-apps/demo-quick-app/create?template_code=php-empty&project_name=Demo%20Quick%20App&domain=demo-quick-app.test&port=80&dry_run=true"
```

## Create real scaffold ornegi

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8751/api/v1/quick-apps/demo-quick-app/create?template_code=php-empty&project_name=Demo%20Quick%20App&domain=demo-quick-app.test&port=80&dry_run=false"
```

## Guvenlik

- Projeler sadece `user_www` altinda olusturulur.
- Path traversal engellenir.
- Download yoktur.
- Shell komutu yoktur.
- `dry_run=true` varsayilan guvenli onizlemedir.
- OpenCart template'i OpenCart 3.x developer scaffold olarak tasarlanmistir.
