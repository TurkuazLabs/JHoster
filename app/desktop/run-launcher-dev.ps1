# 📄 Dosya Yolu: E:\JHoster\app\desktop\run-launcher-dev.ps1
# 📌 Amac: JHoster launcher bootstrap akisini Maven ile test eder
# 📌 Modul - PowerShell
# Version: 3.61.0
# Aciklama: Splash ve GitHub Release check iceren MainApp baslangic akisini calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

mvn --no-transfer-progress process-classes org.codehaus.mojo:exec-maven-plugin:3.5.1:exec `
    -Dexec.mainClass=com.jhoster.desktop.MainApp `
    -Dexec.classpathScope=runtime
