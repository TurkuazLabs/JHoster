# 📄 Dosya Yolu: E:\JHoster\docs\API_ENDPOINTS.md
# 📌 Amac: JHoster API endpointlerini dokumante eder
# 📌 Modul - Markdown
# Version: 3.31.0
# Aciklama: Agent endpoint listesini ve project manager, nginx publish, nginx validate, nginx reload, nginx real reload, Apache vhost, hosts publish, hosts apply ve unified web server workflow ve rollback guard API adreslerini tanimlar
# Bagimli Oldugu Katman: View

# API Endpoints

## Core

```text
GET /api/v1/health
GET /api/v1/components
GET /api/v1/cache
GET /api/v1/apps
GET /api/v1/install/history
```

## Runtime

```text
GET  /api/v1/local-packages
POST /api/v1/local-cache/packages/{component_code}/install
GET  /api/v1/runtime-versions
POST /api/v1/runtime-versions/{component_code}/activate
```

## Projects

```text
GET  /api/v1/www
POST /api/v1/www?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=true
GET  /api/v1/www/{project_code}
```

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## Nginx Publish

- GET /api/v1/nginx-publish
- GET /api/v1/nginx-publish/{project_code}
- GET /api/v1/nginx-publish/{project_code}/plan
- POST /api/v1/nginx-publish/{project_code}/publish?dry_run=true
- POST /api/v1/nginx-publish/{project_code}/publish?dry_run=false


## Nginx Validate

```text
GET  /api/v1/nginx-validate
GET  /api/v1/nginx-validate/{project_code}
GET  /api/v1/nginx-validate/{project_code}/plan
POST /api/v1/nginx-validate/{project_code}/validate?dry_run=true
POST /api/v1/nginx-validate/{project_code}/validate?dry_run=false
```


## Nginx Reload

```text
GET  /api/v1/nginx-reload
GET  /api/v1/nginx-reload/{project_code}
GET  /api/v1/nginx-reload/{project_code}/plan
POST /api/v1/nginx-reload/{project_code}/reload?dry_run=true
POST /api/v1/nginx-reload/{project_code}/reload?dry_run=false
```


## Hosts Publish

```text
GET  /api/v1/hosts-publish
GET  /api/v1/hosts-publish/{project_code}
GET  /api/v1/hosts-publish/{project_code}/plan?ip=127.0.0.1
POST /api/v1/hosts-publish/{project_code}/publish?ip=127.0.0.1&dry_run=true
POST /api/v1/hosts-publish/{project_code}/publish?ip=127.0.0.1&dry_run=false
```


## Hosts Apply

```text
GET  /api/v1/hosts-apply
GET  /api/v1/hosts-apply/{project_code}
GET  /api/v1/hosts-apply/{project_code}/plan?ip=127.0.0.1&real_write=false
POST /api/v1/hosts-apply/{project_code}/apply?ip=127.0.0.1&real_write=false&dry_run=true
POST /api/v1/hosts-apply/{project_code}/apply?ip=127.0.0.1&real_write=false&dry_run=false
GET  /api/v1/hosts-apply/{project_code}/rollback-plan
POST /api/v1/hosts-apply/{project_code}/rollback?dry_run=true
POST /api/v1/hosts-apply/{project_code}/rollback?dry_run=false
```


## v3.18.0 Nginx Executable

```text
GET  /api/v1/nginx-executable
GET  /api/v1/nginx-executable/latest
GET  /api/v1/nginx-executable/plan
POST /api/v1/nginx-executable/detect?dry_run=true
POST /api/v1/nginx-executable/detect?dry_run=false
```


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.

## v3.19.0 Nginx Real Validate

- `GET /api/v1/nginx-real-validate`
- `GET /api/v1/nginx-real-validate/{project_code}`
- `GET /api/v1/nginx-real-validate/{project_code}/plan`
- `POST /api/v1/nginx-real-validate/{project_code}/validate?dry_run=true&allow_real_execution=false`


## v3.20.0 Nginx Real Reload

- `GET /api/v1/nginx-real-reload`
- `GET /api/v1/nginx-real-reload/{project_code}`
- `GET /api/v1/nginx-real-reload/{project_code}/plan`
- `POST /api/v1/nginx-real-reload/{project_code}/reload?dry_run=true&allow_real_execution=false`


## v3.23.0 - Derin Analiz ve Temizlik

- Paket temizligi, audit raporu ve Apache profile guard eklendi.


## v3.24.0 Apache Virtual Hosts

```text
GET  /api/v1/apache-vhosts
GET  /api/v1/apache-vhosts/{project_code}
GET  /api/v1/apache-vhosts/{project_code}/plan?domain=demo-site.localhost&port=80
POST /api/v1/apache-vhosts/{project_code}/generate?domain=demo-site.localhost&port=80&dry_run=true
POST /api/v1/apache-vhosts/{project_code}/generate?domain=demo-site.localhost&port=80&dry_run=false
```


## v3.31.0 Web Server Workflow

```text
GET  /api/v1/web-server-workflow
GET  /api/v1/web-server-workflow/{project_code}
GET  /api/v1/web-server-workflow/{project_code}/plan?domain=demo-site.localhost&port=80&reload=true&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/run?domain=demo-site.localhost&port=80&dry_run=true&reload=true&allow_real_execution=false&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/run?domain=demo-site.localhost&port=80&dry_run=false&reload=true&allow_real_execution=false&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=true
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=false
```


## v3.33.0 Web Server Workflow Locks

```text
GET  /api/v1/web-server-workflow/locks
GET  /api/v1/web-server-workflow/{project_code}/lock
POST /api/v1/web-server-workflow/{project_code}/unlock?run_id=manual-lock-001&force=false
POST /api/v1/web-server-workflow/{project_code}/unlock?force=true
```
