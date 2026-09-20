# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\run-desktop-netbeans-fixed.ps1
# 📌 Amac: JHoster Desktop uygulamasini NetBeans placeholder kullanmadan Maven exec ile calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: exec.mainClass degerini dogrudan MainApp olarak vererek packageClassName hatasini asar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Set-Location "E:\JHoster\app\desktop"

$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot"
$maven = "D:\Program Files\netbeans\java\maven\bin\mvn.cmd"

& $maven --no-transfer-progress process-classes org.codehaus.mojo:exec-maven-plugin:3.5.1:exec `
    "-Dexec.executable=$env:JAVA_HOME\bin\java.exe" `
    "-Dexec.mainClass=com.jhoster.desktop.MainApp" `
    "-Dexec.classpathScope=runtime" `
    "-Dexec.vmArgs=" `
    "-Dexec.appArgs=" `
    "-Dexec.args=`${exec.vmArgs} -classpath %classpath `${exec.mainClass} `${exec.appArgs}"
