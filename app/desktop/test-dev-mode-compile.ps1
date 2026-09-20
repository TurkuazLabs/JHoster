# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-dev-mode-compile.ps1
# 📌 Amac: JHoster Desktop dev mode gate Maven compile testini calistirir
# 📌 Modul - PowerShell
# Version: 3.58.0
# Aciklama: Shift/dev mode UI degisikligi sonrasi desktop compile ve calistirma kontrolu icin yardimci script
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Set-Location "E:\JHoster\app\desktop"

$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
$mavenPath = "D:\Program Files\netbeans\java\maven\bin\mvn.cmd"
$javaPath = Join-Path $env:JAVA_HOME "bin\java.exe"

& $mavenPath `
    "-Dexec.executable=$javaPath" `
    "-Dexec.mainClass=com.jhoster.desktop.MainApp" `
    "-Dexec.classpathScope=runtime" `
    --no-transfer-progress `
    process-classes `
    org.codehaus.mojo:exec-maven-plugin:3.5.1:exec
