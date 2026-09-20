# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-quick-actions-layout-compile.ps1
# 📌 Amac: JHoster Desktop v3.55.1 quick actions layout ve Maven compile kontrolunu calistirir
# 📌 Modul - PowerShell
# Version: 3.55.1
# Aciklama: Quick Actions panelinin Services ustunde oldugunu statik kontrol eder ve Maven compile calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$viewFile = Join-Path $root "src\main\java\com\jhoster\desktop\views\LauncherView.java"

if (!(Test-Path $viewFile)) {
    throw "LauncherView.java bulunamadi: $viewFile"
}

$content = Get-Content $viewFile -Raw
$quickIndex = $content.IndexOf("buildCleanQuickActionsPanel(),")
$serviceIndex = $content.IndexOf("buildCleanServiceOverview(),")
$bottomGridIndex = $content.IndexOf("private Parent buildDashboardBottomGrid()")

if ($quickIndex -lt 0) {
    throw "Quick Actions render cagrisi bulunamadi."
}

if ($serviceIndex -lt 0) {
    throw "Services render cagrisi bulunamadi."
}

if ($quickIndex -gt $serviceIndex) {
    throw "Quick Actions, Services panelinden sonra render ediliyor."
}

$bottomGridBody = $content.Substring($bottomGridIndex, [Math]::Min(700, $content.Length - $bottomGridIndex))
if ($bottomGridBody.Contains("buildCleanQuickActionsPanel()")) {
    throw "Bottom grid icinde Quick Actions tekrari bulundu."
}

Write-Host "OK: Quick Actions, Services ustunde render ediliyor."
Write-Host "OK: Bottom grid Quick Actions tekrarindan temizlendi."

mvn --no-transfer-progress process-classes
