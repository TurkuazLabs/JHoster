# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-portable-version-manager-compile.ps1
# 📌 Amac: Desktop Portable Version Manager baglanti siniflarini derler
# 📌 Modul - PowerShell
# Version: 3.49.0
# Aciklama: Runtime manager service, formatter ve portable version manager sabitlerini javac ile kontrol eder
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

$OutDir = Join-Path $ScriptDir "target\portable-version-manager-test"
$TempDir = Join-Path $ScriptDir "target\portable-version-manager-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestPortableVersionManager.java"
$TestSource = @'
import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.services.RuntimeManagerDesktopService;
import com.jhoster.desktop.services.RuntimeResultFormatterService;

public class TestPortableVersionManager {
    public static void main(String[] args) {
        if (!"apache".equals(DesktopApiConfig.RUNTIME_FAMILY_APACHE)) {
            throw new IllegalStateException("Apache family constant hatali");
        }
        if (!DesktopApiConfig.DEFAULT_APACHE_RUNTIME_FOLDER.startsWith("httpd-")) {
            throw new IllegalStateException("Apache default folder hatali");
        }
        RuntimeManagerDesktopService service = new RuntimeManagerDesktopService();
        if (service == null) {
            throw new IllegalStateException("service olusmadi");
        }
        String body = "{\"success\":true,\"message\":\"portable version summary ready\",\"count\":9}";
        RuntimeManagerSummary summary = new RuntimeResultFormatterService().formatPortableScan(DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("summary parse failed");
        }
        System.out.println("Portable version manager compile OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\RuntimeManagerSummary.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\bin\RuntimeResultFormatterService.java `
    src\main\java\com\jhoster\desktop\bin\RuntimeManagerDesktopService.java `
    $TestFile

java -cp $OutDir TestPortableVersionManager

Write-Host "Desktop portable version manager compile tamamlandi."
