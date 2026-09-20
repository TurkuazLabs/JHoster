# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-quick-actions-compile.ps1
# 📌 Amac: Desktop Quick Action siniflarini Maven olmadan derler
# 📌 Modul - PowerShell
# Version: 3.45.0
# Aciklama: HeidiSQL Portable, Root, Projects, Logs ve Terminal quick action baglanti siniflarini javac ile kontrol eder
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

$OutDir = Join-Path $ScriptDir "target\quick-actions-test"
$TempDir = Join-Path $ScriptDir "target\quick-actions-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestQuickActionTool.java"
$TestSource = @'
import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.tools.QuickActionTool;

public class TestQuickActionTool {
    public static void main(String[] args) {
        QuickActionTool tool = new QuickActionTool();
        String result = tool.openHeidiSqlPortable();
        if (result == null || result.isBlank()) {
            throw new IllegalStateException("HeidiSQL result bos dondu");
        }
        if (!result.contains("heidisql")) {
            throw new IllegalStateException("HeidiSQL path sonuc icinde yok");
        }
        System.out.println("Quick Action Tool OK");
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

java -cp $OutDir TestQuickActionTool

Write-Host "Desktop Quick Action compile tamamlandi."
