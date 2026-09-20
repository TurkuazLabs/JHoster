# 📄 Dosya Yolu: E:\JHoster\docs\PROJECT_AUDIT_V3_31.md
# 📌 Amac: JHoster v3.31.0 rollback guard paket analizini tutar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Unified web server workflow rollback guard icin dosya, route ve test durumunu ozetler
# Bagimli Oldugu Katman: View

# Project Audit v3.31.0

## Kapsam

- Unified workflow servis katmani rollback guard ile genisletildi.
- Controller yeni `rollback_on_failure` parametresini service katmanina aktariyor.
- Manuel rollback endpointi eklendi.
- Rollback logic tool katmaninda izole edildi.

## Katman kontrolu

- Controller: request alir ve service cagirir.
- Service: workflow siralama, hata karari ve rollback kararini verir.
- Repo: workflow registry kaydini tutar.
- Tool: publish backup dosyasini geri yukler veya yeni publish dosyasini kaldirir.
- View: API response ve dokuman ciktisini tasir.

## Guvenlik kontrolu

- Rollback yalnizca JHoster snapshot publish klasorlerinde calisir.
- Backup yolu JHoster snapshot backup klasoru icinde degilse islem skipped olur.
- Varsayilan endpoint davranisi dry-run guvenligini korur.
- Real reload icin `allow_real_execution=true` izni hala zorunludur.

## Test ozeti

- Python compile: basarili.
- FastAPI import: basarili.
- Route sayisi: 107.
- Workflow plan/run smoke test: basarili.
- Rollback dry-run smoke test: basarili.
