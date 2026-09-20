# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-jhoster-deck-ui-compile.ps1
# 📌 Amac: JHoster Desktop v3.60.0 Deck UI icin Maven compile testi calistirir
# 📌 Modul - PowerShell
# Version: 3.60.0
# Aciklama: Normal mod Deck UI ve Dev Mode ayrimi sonrasi JavaFX desktop compile kontrolunu baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
Write-Host "JHoster Desktop v3.60.0 Deck UI Compile Test"
Set-Location "E:\JHoster\app\desktop"
$maven = "D:\Program Files\netbeans\java\maven\bin\mvn.cmd"
if (-not (Test-Path $maven)) {
    throw "Maven not found: $maven"
}
& $maven --no-transfer-progress process-classes
Write-Host "v3.60.0 Deck UI compile test completed."
