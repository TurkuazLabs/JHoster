# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-runtime-manager-compile.ps1
# 📌 Amac: Desktop Runtime Manager baglanti siniflarini Maven olmadan derleme ve parser testi yapar
# 📌 Modul - PowerShell
# Version: 3.48.0
# Aciklama: Runtime manager model, formatter, service ve portable bin parser siniflarini javac ile kontrol eder
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

$OutDir = Join-Path $ScriptDir "target\runtime-manager-test"
$TempDir = Join-Path $ScriptDir "target\runtime-manager-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestRuntimeFormatter.java"
$TestSource = @'
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.services.RuntimeResultFormatterService;

public class TestRuntimeFormatter {
    public static void main(String[] args) {
        String body = "{\"success\":true,\"family\":\"php\",\"status\":\"active\",\"component_code\":\"php-8.3.30\",\"version\":\"8.3.30\",\"folder_name\":\"php-8.3.30-Win32-vs16-x64\"}";
        RuntimeManagerSummary summary = new RuntimeResultFormatterService().formatPortableActivate("php", "php-8.3.30-Win32-vs16-x64", DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("success parse failed");
        }
        if (!"php".equals(summary.getFamily())) {
            throw new IllegalStateException("family parse failed");
        }
        if (!"php-8.3.30".equals(summary.getComponentCode())) {
            throw new IllegalStateException("component parse failed");
        }
        if (!"8.3.30".equals(summary.getVersion())) {
            throw new IllegalStateException("version parse failed");
        }
        System.out.println("Runtime summary parser OK");
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

java -cp $OutDir TestRuntimeFormatter

Write-Host "Desktop runtime manager compile tamamlandi."
