# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-compact-dashboard-compile.ps1
# 📌 Amac: Desktop compact dashboard quick action ve service manager siniflarini derler
# 📌 Modul - PowerShell
# Version: 3.45.0
# Aciklama: Compact dashboard quick action baglantilari icin javac smoke testi calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$javac = Get-Command javac -ErrorAction SilentlyContinue
$java = Get-Command java -ErrorAction SilentlyContinue

if ($null -eq $javac -or $null -eq $java) {
    Write-Host "Java JDK bulunamadi. JAVA_HOME veya PATH ayarini kontrol edin."
    exit 1
}

$OutDir = Join-Path $ScriptDir "target\compact-dashboard-test"
$TempDir = Join-Path $ScriptDir "target\compact-dashboard-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestCompactDashboard.java"
$TestSource = @'
import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.services.QuickActionDesktopService;

public class TestCompactDashboard {
    public static void main(String[] args) {
        if (!"mailpit".equals(DesktopApiConfig.SERVICE_CODE_MAILPIT)) {
            throw new IllegalStateException("Mailpit service code hatali");
        }
        if (!DesktopApiConfig.QUICK_ACTION_MAILPIT_URL.contains("8025")) {
            throw new IllegalStateException("Mailpit URL port hatali");
        }
        QuickActionDesktopService service = new QuickActionDesktopService();
        String result = service.openMailpit();
        if (result == null || !result.contains("Mailpit")) {
            throw new IllegalStateException("Mailpit quick action sonucu hatali");
        }
        System.out.println("Compact dashboard quick action OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\tools\BrowserTool.java `
    src\main\java\com\jhoster\desktop\tools\QuickActionTool.java `
    src\main\java\com\jhoster\desktop\bin\QuickActionDesktopService.java `
    $TestFile

java -cp $OutDir TestCompactDashboard

Write-Host "Desktop compact dashboard compile tamamlandi."
