# 📄 Dosya Yolu: E:\JHoster\docs\HOSTS_PUBLISH.md
# 📌 Amac: JHoster hosts publish katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 3.16.0
# Aciklama: Virtual host domainini guvenli snapshot hosts dosyasina yazma akisinin endpointlerini ve test komutunu aciklar
# Bagimli Oldugu Katman: View

# Hosts Publish

Bu modul uretilmis virtual host kaydindaki domain bilgisini guvenli snapshot hosts dosyasina yazar.

## Guvenlik

- Gercek Windows hosts dosyasina yazmaz.
- Hedef dosya `snapshot/hosts/hosts-published/hosts.jhoster` altindadir.
- Var olan satir ayni proje marker'i ile replace edilir.
- Eski snapshot hosts dosyasi varsa backup alinir.
- IP adresi `ipaddress` ile dogrulanir.
- Domain icinde `/`, `\`, `:`, `..` tokenlari kabul edilmez.
- `dry_run=true` varsayilan davranistir.

## Endpointler

```text
GET  /api/v1/hosts-publish
GET  /api/v1/hosts-publish/{project_code}
GET  /api/v1/hosts-publish/{project_code}/plan?ip=127.0.0.1
POST /api/v1/hosts-publish/{project_code}/publish?ip=127.0.0.1&dry_run=true
POST /api/v1/hosts-publish/{project_code}/publish?ip=127.0.0.1&dry_run=false
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-hosts-publish.ps1
```

## Beklenen sonuc

- Plan sonucu `status: planned` doner.
- Publish sonucu `status: published` doner.
- `real_hosts_file_write: false` kalir.
- Snapshot hosts dosyasi `snapshot/hosts/hosts-published/hosts.jhoster` olarak olusur.
- Registry kaydi `data/jhoster/hosts_publish_registry.json` icinde tutulur.
