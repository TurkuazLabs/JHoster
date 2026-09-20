# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-launcher-bootstrap-compile.ps1
# 📌 Amac: JHoster launcher bootstrap surumunun Maven compile testini calistirir
# 📌 Modul - PowerShell
# Version: 3.61.1
# Aciklama: MainApp uzerinden splash ve update check akisinin compile edilebilir oldugunu dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Set-Location "E:\JHoster\app\desktop"

mvn --no-transfer-progress process-classes org.codehaus.mojo:exec-maven-plugin:3.5.1:exec `
    -Dexec.mainClass=com.jhoster.desktop.MainApp `
    -Dexec.classpathScope=runtime
