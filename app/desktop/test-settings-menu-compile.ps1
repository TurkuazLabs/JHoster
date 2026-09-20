# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-settings-menu-compile.ps1
# 📌 Amac: Desktop settings menu revizyonu icin Maven compile testi calistirir
# 📌 Modul - PowerShell
# Version: 3.55.1
# Aciklama: JHoster Desktop servis secim ayarlari ve JavaFX settings menu baglantisini yerelde dogrular
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
    mvn --no-transfer-progress clean process-classes
    Write-Host "JHoster Desktop settings menu compile test completed."
} finally {
    Pop-Location
}
