# 📄 Dosya Yolu: E:\JHoster\docs\SERVICE_MANAGER_PROCESS_INSPECTION.md
# 📌 Amac: Service Manager process inspection probe akislarini aciklar
# 📌 Modul - Markdown
# Version: 3.38.0
# Aciklama: Windows process probe ile gercek servis durumunun okunmasi icin teknik not
# Bagimli Oldugu Katman: Service

# Service Manager Process Inspection

JHoster v3.38.0 ile Service Manager sadece kaydedilmis simulated state bilgisini okumaz. `inspect` endpointi ile Windows uzerinde process adina gore gercek calisma durumunu da denetleyebilir.

## Endpointler

- `GET /api/v1/process/{component_code}/inspect`
- `GET /api/v1/process/{component_code}/status?prefer_real=true`
- `GET /api/v1/process/{component_code}/status`

## Davranis

- `inspect` her zaman real adapter tercih eder.
- `status?prefer_real=true` real adapter ile process probe dener.
- Normal `status` stored/simulated state bilgisini okumaya devam eder.
- Windows disinda probe calismaz ve `unsupported_os` benzeri guvenli mesaj doner.
- Shell kullanilmaz; process kontrolu `tasklist` argv listesi ile yapilir.

## Guvenlik

- Inspect isleminde servis baslatilmaz veya durdurulmaz.
- Real execution halen varsayilan olarak kapalidir.
- `real_process.enabled=false` ise start/stop gercek process calistirmaz.
- Desktop status butonu artik inspect endpointini cagirir; bu sadece okuma islemidir.
