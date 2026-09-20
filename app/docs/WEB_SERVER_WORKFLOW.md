# 📄 Dosya Yolu: E:\JHoster\docs\WEB_SERVER_WORKFLOW.md
# 📌 Amac: Unified web server workflow API kullanimini dokumante eder
# 📌 Modul - Markdown
# Version: 1.2.0
# Aciklama: Active web server profile secimine gore generate, publish, validate, reload, rollback guard ve run tracking akisini aciklar
# Bagimli Oldugu Katman: View

# Web Server Workflow

## Amac

`/api/v1/web-server-workflow` endpoint grubu, secili active web server profile degerine gore Nginx veya Apache akislarini tek noktadan calistirir.

## Endpointler

```text
GET  /api/v1/web-server-workflow
GET  /api/v1/web-server-workflow/{project_code}
GET  /api/v1/web-server-workflow/runs
GET  /api/v1/web-server-workflow/runs?project_code=demo-site
GET  /api/v1/web-server-workflow/runs?status=completed
GET  /api/v1/web-server-workflow/runs/{run_id}
GET  /api/v1/web-server-workflow/{project_code}/runs
GET  /api/v1/web-server-workflow/{project_code}/plan?domain=demo-site.localhost&port=80&reload=true&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/run?domain=demo-site.localhost&port=80&dry_run=true&reload=true&allow_real_execution=false&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/run?domain=demo-site.localhost&port=80&dry_run=false&reload=true&allow_real_execution=false&rollback_on_failure=true
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=true
POST /api/v1/web-server-workflow/{project_code}/rollback?dry_run=false
```

## Akis

1. Active web server profile okunur.
2. Profile `nginx` ise Nginx vhost generator kullanilir.
3. Profile `apache` ise Apache vhost generator kullanilir.
4. Config publish edilir.
5. Static validate calisir.
6. Reload istenir ise:
   - Nginx icin `allow_real_execution=false` durumunda simulated reload calisir.
   - Apache icin `allow_real_execution=false` durumunda reload guvenli sekilde skipped olur.
   - `allow_real_execution=true` durumunda ilgili real validate ve real reload adapter zinciri kullanilir.
7. `rollback_on_failure=true` ise publish sonrasi validate veya reload adiminda hata olusursa publish edilen config geri alinir.

## Rollback Guard

Rollback guard sadece publish adimindan sonra devreye girer. Publish adiminda hedef dosya daha once varsa backup dosyasi geri yuklenir. Hedef dosya ilk kez olusturulduysa ve backup yoksa yeni dosya kaldirilir.

Manuel rollback endpointi son workflow kaydindaki publish adimini baz alir. Varsayilan olarak `dry_run=true` calisir.

## Guvenlik

Varsayilan olarak `dry_run=true`, `allow_real_execution=false` ve `rollback_on_failure=true` gelir. Gercek web server reload islemi acik izin verilmeden calismaz.


## Run Tracking

Her workflow cevabi `run_id` tasir. Run kaydi `steps`, `step_count`, `started_at` ve `finished_at` alanlariyla saklanir. Panel tarafinda son workflow sonucunu okumak icin proje bazli endpoint, gecmis calismalari okumak icin run tracking endpointleri kullanilir.


## v3.33.0 Lock Guard

`dry_run=false` workflow calismasi proje bazli lock alir. Aktif lock varsa yeni calisma engellenir. Workflow bittiginde lock otomatik release edilir.

```text
GET  /api/v1/web-server-workflow/locks
GET  /api/v1/web-server-workflow/{project_code}/lock
POST /api/v1/web-server-workflow/{project_code}/unlock?force=true
```
