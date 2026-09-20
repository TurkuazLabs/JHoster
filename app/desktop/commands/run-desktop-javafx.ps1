# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\run-desktop-javafx.ps1
# 📌 Amac: JHoster Desktop JavaFX uygulamasini Maven JavaFX plugin ile temiz module-path uzerinden calistirir
# 📌 Modul - PowerShell
# Version: 1.0.3
# Aciklama: JAVA_HOME degerini Maven baslamadan once ayarlar ve OpenJFX unnamed module uyarisini azaltmak icin javafx:run hedefini kullanir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Set-Location "E:\JHoster\app\desktop"

$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
$maven = "D:\Program Files\netbeans\java\maven\bin\mvn.cmd"

if (Test-Path $maven) {
    & $maven --no-transfer-progress clean javafx:run
    exit $LASTEXITCODE
}

mvn --no-transfer-progress clean javafx:run
exit $LASTEXITCODE
