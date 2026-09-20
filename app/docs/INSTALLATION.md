# 📄 Dosya Yolu: E:\JHoster\docs\INSTALLATION.md
# 📌 Amac: JHoster kurulum adimlarini tanimlar
# 📌 Modul - Markdown
# Version: 3.11.0
# Aciklama: Agent kurulum, baslatma ve test komutlarini listeler
# Bagimli Oldugu Katman: View

# Installation

## Ilk kurulum

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\install-agent-deps.ps1
```

## Baslatma

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\run-agent.ps1
```

## Project manager testi

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-www.ps1
```
