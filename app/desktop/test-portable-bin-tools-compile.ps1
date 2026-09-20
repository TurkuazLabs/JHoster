# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-portable-bin-tools-compile.ps1
# 📌 Amac: Portable bin quick action siniflarini Maven olmadan derler
# 📌 Modul - PowerShell
# Version: 3.47.0
# Aciklama: QuickActionTool ve QuickActionDesktopService icin hizli javac smoke testi calistirir
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

$OutDir = Join-Path $ScriptDir "target\portable-bin-tools-test"
$TempDir = Join-Path $ScriptDir "target\portable-bin-tools-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestPortableBinTools.java"
Set-Content -Path $TestFile -Encoding UTF8 -Value @'
import com.jhoster.desktop.tools.QuickActionTool;

public class TestPortableBinTools {
    public static void main(String[] args) {
        QuickActionTool tool = new QuickActionTool();
        if (tool == null) {
            throw new IllegalStateException("QuickActionTool olusmadi");
        }
        System.out.println("Portable bin tools compile OK");
    }
}
'@

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\tools\QuickActionTool.java `
    $TestFile

java -cp $OutDir TestPortableBinTools

Write-Host "Portable bin tools compile tamamlandi."
