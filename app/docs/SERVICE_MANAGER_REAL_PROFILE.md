# 📄 Dosya Yolu: E:\JHoster\docs\SERVICE_MANAGER_REAL_PROFILE.md
# 📌 Amac: Service Manager real process profil yonetimi dokumani
# 📌 Modul - Markdown
# Version: 3.40.0
# Aciklama: JHoster servislerinin gercek executable path ve real execution enable ayarlarini aciklar
# Bagimli Oldugu Katman: Service

# Service Manager Real Profile

JHoster v3.40.0 ile Service Manager icin real process profil katmani eklendi.
Bu katman, servisleri gercek Windows process olarak calistirmadan once executable path ve enable bilgisini guvenli sekilde yonetir.

## Endpointler

- `GET /api/v1/process/{component_code}/real-profile`
- `GET /api/v1/process/{component_code}/real-profile/plan?install_path=apps/apache&enabled=true`
- `POST /api/v1/process/{component_code}/real-profile/apply?install_path=apps/apache&enabled=true&dry_run=true`
- `POST /api/v1/process/{component_code}/real-profile/apply?install_path=apps/apache&enabled=true&dry_run=false`

## Guvenlik Kurallari

- Path, JHoster root klasoru icinde kalmalidir.
- `dry_run=true` varsayilandir.
- Real start/stop icin ayrica `allow_real_execution=true` gerekir.
- `real_process.enabled=false` ise executable bulunsa bile real start/stop bloklanir.
- Shell komutu kullanilmaz.

## Ornek Akis

1. Servisin profilini gor.
2. Yeni install path ve enabled durumunu planla.
3. Dry-run apply ile sonucu incele.
4. Gerekirse `dry_run=false` ile profili kaydet.
5. Preflight ile executable varligini dogrula.
6. Sonra real start/stop guard parametresiyle denenebilir.
