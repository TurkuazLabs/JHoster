# 📄 Dosya Yolu: E:\JHoster\docs\SERVICE_MANAGER_REAL_LIFECYCLE.md
# 📌 Amac: Service Manager real process lifecycle guard dokumani
# 📌 Modul - Markdown
# Version: 3.40.0
# Aciklama: Start, stop, restart islemlerinde real process verification ve safe guard akisini aciklar
# Bagimli Oldugu Katman: View

# Service Manager Real Lifecycle

## Amac

Bu katman Service Manager icinde real process start, stop ve restart akisini guvenli hale getirir.

## Guvenlik kurallari

- Real execution varsayilan kapali kalir.
- `allow_real_execution=true` verilmeden real process calismaz.
- `real_process.enabled=true` olmadan real process calismaz.
- Executable yoksa real process calismaz.
- Shell komutu kullanilmaz.
- Komutlar argv listesi olarak calistirilir.
- Stop komutu olmayan servislerde stop islemi bloklanir.
- Start/stop sonrasinda process probe ile verification yapilir.

## Akis

1. App registry icinden servis okunur.
2. Runtime context uretilir.
3. Executable candidate bulunur.
4. Real adapter guard kontrolu yapar.
5. Komut shell kullanmadan calistirilir.
6. Process probe ile beklenen status dogrulanir.
7. Sadece dogrulama basariliysa process state guncellenir.

## Endpointler

```text
POST /api/v1/process/{component_code}/start?dry_run=false&allow_real_execution=true
POST /api/v1/process/{component_code}/stop?dry_run=false&allow_real_execution=true
POST /api/v1/process/{component_code}/restart?dry_run=false&allow_real_execution=true
GET  /api/v1/process/{component_code}/inspect
```

## Not

Desktop tarafinda real execution halen kapali tutulur. Real start/stop sonraki UI surumunde ayri bir advanced switch ile acilmalidir.
