# 📄 Dosya Yolu: E:\JHoster\docs\PROJECT_AUDIT_V3_36.md
# 📌 Amac: JHoster v3.36.0 desktop service manager audit sonucunu kaydeder
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Service Manager UI, process registry ve guvenli state kontrolu kapsam kontrolu
# Bagimli Oldugu Katman: View

# Project Audit v3.36.0

## Kapsam

v3.36.0 surumu Laragon eksiklerinin ilk ana parcasi olan Service Manager deneyimini Desktop tarafina tasir. Bu surumde Apache, Nginx, MySQL ve PHP icin status/start/stop/restart aksiyonlari tek panelden kullanilabilir hale gelir.

## Mimari kontrol

- Controller: `LauncherController` sadece UI eventlerini service katmanina aktarir.
- Service: `ServiceManagerDesktopService` ve `ServiceResultFormatterService` is akisini ve HTTP sonuc ozetlemeyi yonetir.
- Repo/Model: `ServiceManagerSummary` Desktop sonuc modelidir.
- Tool: `HttpRequestTool` ve `JsonTextExtractorTool` kullanilir.
- View: `LauncherView` Service Manager panelini ve durum pill alanlarini olusturur.
- Config: `DesktopApiConfig` service code ve guvenli state varsayilanlarini merkezi tutar.

## Guvenlik notu

Service Manager v1 gercek Windows servislerini baslatmaz. Agent tarafindaki varsayilan kayitlar `runtime_adapter=simulated` ile tutulur. Bu sayede start/stop aksiyonlari local state uzerinden calisir ve sistem servislerine dokunmaz.

## Sonraki riskli alan

Real process adapter acilirken su guardlar zorunlu olmalidir:

- Runtime executable path detection.
- Admin privilege preflight.
- Port conflict check.
- Process PID tracking.
- Failed start rollback.
- Active web server profile ile Apache/Nginx cakisma kontrolu.
