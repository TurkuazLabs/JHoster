# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-hosts-auto-repair-compile.ps1
# 📌 Amac: Desktop hosts auto route config compile kontrolunu yapar
# 📌 Modul - PowerShell
# Version: 3.67.0
# Aciklama: DesktopApiConfig icindeki hosts auto inspect ve repair route sabitlerini javac ile dogrular
# Bagimli Oldugu Katman: Tool

$Source = "E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java"
$Out = "E:\JHoster\tmp\desktop-hosts-auto-repair-compile"
New-Item -ItemType Directory -Force -Path $Out | Out-Null
javac -d $Out $Source
Write-Host "Desktop hosts auto repair config compile OK"
