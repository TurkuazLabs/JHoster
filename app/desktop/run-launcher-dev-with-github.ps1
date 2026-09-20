# 📄 Dosya Yolu: E:\JHoster\app\desktop\run-launcher-dev-with-github.ps1
# 📌 Amac: GitHub Release repo ayari ile launcher update check testini calistirir
# 📌 Modul - PowerShell
# Version: 3.61.0
# Aciklama: owner/repo parametresi ile latest release kontrolunu aktif ederek JHoster launcher baslatir
# Bagimli Oldugu Katman: Tool

param(
    [string]$Repository = "owner/repo"
)

$ErrorActionPreference = "Stop"

mvn --no-transfer-progress process-classes org.codehaus.mojo:exec-maven-plugin:3.5.1:exec `
    -Dexec.mainClass=com.jhoster.desktop.MainApp `
    -Dexec.classpathScope=runtime `
    -Djhoster.update.repo=$Repository
