# 📄 Dosya Yolu: E:\JHoster\README.md
# 📌 Amac: JHoster sade root layout ana okuma dosyasi
# 📌 Modul - Markdown
# Version: 3.76.1
# Aciklama: JHoster root klasorleri, agent, desktop, sol menu UI, Settings/Logs tablari, release cleanup, API audit ve source header path tutarlilik patch akisini aciklar

Bagimli Oldugu Katman: Service | Tool | Config | View

# JHoster

JHoster, Laragon benzeri ama API-first ve moduler bir local development manager hedefler.

## Root layout

```text
E:\JHoster\
├─ app\
├─ bin\
├─ data\
├─ etc\
├─ logs\
├─ tmp\
├─ www\
├─ backup\
└─ cache\
```

## Ana konumlar

- Agent: `E:\JHoster\app\agent`
- Desktop: `E:\JHoster\app\desktop`
- Portable araclar: `E:\JHoster\bin`
- Projeler: `E:\JHoster\www`
- State: `E:\JHoster\data\jhoster`
- Config: `E:\JHoster\etc`

## Calistirma

Agent:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\run-agent.ps1
```

Desktop:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\commands\run-desktop-javafx.ps1
```

## v3.76.1 Source Header ve Roadmap Patch

- Aktif Desktop Java ve Agent Python kaynaklari icin tam `E:\JHoster\...` header path standardi denetlenir.
- Desktop service/repository/tool katmaninda eski `bin` ve eksik `app` path header kayitlari duzeltildi.
- Roadmap icindeki tamamlanmis `v3.76.0` maddesinin yanlislikla Siradaki bolumunde tekrar etmesi duzeltildi.
- Yeni source header path guard release oncesi tekrar calistirilabilir.
