# 📄 Dosya Yolu: E:\JHoster\docs\HOSTS_APPLY.md
# 📌 Amac: JHoster hosts apply ve rollback katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 3.17.0
# Aciklama: Snapshot ve gercek Windows hosts apply icin admin, backup ve rollback akisini aciklar
# Bagimli Oldugu Katman: View

# Hosts Apply

Bu modul virtual host domain bilgisini hosts dosyasina uygulamak icin hazirlanmistir.

Varsayilan mod guvenlidir ve gercek Windows hosts dosyasina yazmaz.

## Modlar

### Snapshot apply

`real_write=false` varsayilan moddur.

Hedef dosya:

```text
E:\JHoster\snapshot\hosts\hosts-applied\hosts.jhoster
```

### Real Windows hosts apply

`real_write=true` verildiginde hedef dosya:

```text
C:\Windows\System32\drivers\etc\hosts
```

Bu mod icin:

- Windows platform gerekir.
- Agent admin olarak calismalidir.
- Plan guvenli degilse yazma islemi reddedilir.
- Yazmadan once backup alinir.
- Rollback sadece registrydeki backup kaydindan yapilir.

## Endpointler

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

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-hosts-apply.ps1
```

## Beklenen sonuc

- Plan sonucu `status: planned` doner.
- Apply sonucu `status: applied` doner.
- Ikinci apply oncesi backup uretilir.
- Rollback plan sonucu `status: rollback_planned` doner.
- Rollback sonucu `status: rolled_back` doner.
- Snapshot modunda `real_hosts_file_write: false` kalir.

## Guvenlik notu

Gercek Windows hosts dosyasi icin API kullanimi bilincli sekilde `real_write=true` ister. Bu parametre verilmeden sistem dosyasina yazilmaz.
