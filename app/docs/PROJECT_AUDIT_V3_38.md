# 📄 Dosya Yolu: E:\JHoster\docs\PROJECT_AUDIT_V3_38.md
# 📌 Amac: JHoster v3.38.0 process inspection audit sonucunu kaydeder
# 📌 Modul - Markdown
# Version: 3.38.0
# Aciklama: Service Manager real process inspection probe audit raporu
# Bagimli Oldugu Katman: Service

# Project Audit v3.38.0

v3.38.0 surumu Service Manager'i Laragon benzeri gercek servis durum okuma deneyimine yaklastirir. Bu surumda start/stop real execution halen default kapali tutulur; ancak status tarafinda Windows process probe eklenir.

## Eklenenler

- `GET /api/v1/process/{component_code}/inspect`
- `GET /api/v1/process/{component_code}/status?prefer_real=true`
- `WindowsProcessProbeTool`
- Guarded adapter icin real process status probe
- Preflight sonucunda `real_process_probe` alani
- Desktop status butonunun inspect endpointine baglanmasi

## Guvenlik Kontrolu

- Shell kullanilmadi.
- Real start/stop default acilmadi.
- Windows disi ortamda probe guvenli sekilde bloklandi.
- `allow_real_execution` halen start/stop icin zorunlu.

## Sonuc

Service Manager artik kayitli durum ile gercek process durumunu ayirabilecek seviyeye geldi. Bir sonraki adim, runtime paketleri indirildikten sonra `real_process.enabled` degerini kontrollu olarak profile bazli acmak olabilir.
