# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-splash-ui-polish-compile.ps1
# 📌 Amac: JHoster splash ve deck UI polish surumunun Maven compile testini calistirir
# 📌 Modul - PowerShell
# Version: 3.61.1
# Aciklama: Launcher bootstrap, splash delay, version title ve deck UI polish akisinin compile edilebilir oldugunu dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Set-Location "E:\JHoster\app\desktop"

mvn --no-transfer-progress process-classes org.codehaus.mojo:exec-maven-plugin:3.5.1:exec `
    -Dexec.mainClass=com.jhoster.desktop.MainApp `
    -Dexec.classpathScope=runtime
