# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-quick-app-compile.ps1
# 📌 Amac: Desktop Quick App baglanti siniflarini Maven olmadan derleme ve parser testi yapar
# 📌 Modul - PowerShell
# Version: 3.42.0
# Aciklama: Quick App model, formatter ve service siniflarini javac ile kontrol eder
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

$OutDir = Join-Path $ScriptDir "target\quick-app-test"
$TempDir = Join-Path $ScriptDir "target\quick-app-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestQuickAppFormatter.java"
$TestSource = @'
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.QuickAppSummary;
import com.jhoster.desktop.services.QuickAppResultFormatterService;

public class TestQuickAppFormatter {
    public static void main(String[] args) {
        String body = "{\"success\":true,\"status\":\"planned\",\"project_code\":\"demo-quick-app\",\"template_code\":\"opencart-3\",\"runtime_family\":\"php\",\"file_count\":5}";
        QuickAppSummary summary = new QuickAppResultFormatterService().formatPlan("demo-quick-app", "opencart-3", DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("success parse failed");
        }
        if (!"demo-quick-app".equals(summary.getProjectCode())) {
            throw new IllegalStateException("project parse failed");
        }
        if (!"opencart-3".equals(summary.getTemplateCode())) {
            throw new IllegalStateException("template parse failed");
        }
        if (summary.getFileCount() != 5) {
            throw new IllegalStateException("file count parse failed");
        }
        System.out.println("Quick App parser OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\QuickAppSummary.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\bin\QuickAppResultFormatterService.java `
    src\main\java\com\jhoster\desktop\bin\QuickAppDesktopService.java `
    $TestFile

java -cp $OutDir TestQuickAppFormatter

Write-Host "Desktop Quick App compile tamamlandi."
