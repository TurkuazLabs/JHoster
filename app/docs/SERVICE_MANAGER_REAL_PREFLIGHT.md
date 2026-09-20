# 📄 Dosya Yolu: E:\JHoster\docs\SERVICE_MANAGER_REAL_PREFLIGHT.md
# 📌 Amac: Service Manager real execution preflight akisini aciklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache, Nginx, MySQL ve PHP icin gercek process calistirma oncesi guard kurallarini dokumante eder
# Bagimli Oldugu Katman: View

# Service Manager Real Preflight

## Varsayilan Mod

JHoster v3.37.0 icinde Desktop Service Manager varsayilan olarak simulated state modunda calisir. Bu sayede UI, status, start, stop ve restart akislari test edilebilir; fakat Windows process otomatik baslatilmaz.

## Preflight Endpoint

```text
GET /api/v1/process/{component_code}/preflight
```

Bu endpoint su kontrolleri raporlar:

- install path
- install path exists
- real process enabled
- real executable path
- real executable exists
- start command
- stop command
- status command

## Real Execution Guard

Gercek process denemesi icin iki kosul birlikte saglanmalidir:

```text
allow_real_execution=true
real_process.enabled=true
```

Ayrica executable path bulunmalidir.

## Guvenlik

- Shell komutu kullanilmaz.
- Komutlar liste argv olarak calistirilir.
- Windows disinda real execution bloklanir.
- Desktop tarafinda `SERVICE_MANAGER_REAL_EXECUTION=false` gelir.
- App registry icindeki `real_process.enabled=false` gelir.

## Ornek

```text
POST /api/v1/process/nginx/start?dry_run=false&allow_real_execution=true
```

Bu istek sadece Nginx app config icinde `real_process.enabled=true` ise ve `nginx.exe` bulunursa gercek process baslatmayi dener.
