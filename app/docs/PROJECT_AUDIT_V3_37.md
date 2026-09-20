# 📄 Dosya Yolu: E:\JHoster\docs\PROJECT_AUDIT_V3_37.md
# 📌 Amac: JHoster v3.37.0 process real preflight audit sonucunu kaydeder
# 📌 Modul - FileType
# Version: 3.37.0
# Aciklama: Process preflight, restart ve guarded real execution kapsam kontrolu
# Bagimli Oldugu Katman: View

# Project Audit v3.37.0

## Kapsam

v3.37.0 surumu Service Manager'i Laragon benzeri gercek servis calistirma deneyimine hazirlar. Bu surumda gercek process calistirma otomatik acilmaz; once preflight, executable path ve izin guard akisi eklenir.

## Katman Kontrolu

- Controller: `process_controller.py` sadece HTTP request alir ve service katmanini cagirir.
- Service: `process_service.py` start, stop, restart, preflight ve is kurallarini yonetir.
- Repo: `process_state_repository.py` kalici state saklar.
- Tool: `process_guard_tool.py`, `local_process_command_tool.py` ve service adapter'lar dis dunya/process adaptorudur.
- View: `ApiResponseView` response render eder.

## Guvenlik Kontrolu

- Default desktop operasyonlari simulated state olarak kalir.
- Real execution icin `allow_real_execution=true` gerekir.
- App config icinde `real_process.enabled=true` olmadan process calismaz.
- Executable path yoksa process calismaz.
- Shell komutu kullanilmaz.
- Windows disinda real execution bloklanir.

## Sonuc

Surum guvenli ve genisletilebilir kabul edildi. Sonraki adim, runtime paketleri indirildikten sonra app registry real process config'i kullanici onayi ile aktif etmek olmalidir.
