# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-workflow-summary-compile.ps1
# 📌 Amac: Desktop workflow summary parser siniflarini Maven olmadan javac ile test eder
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Json extractor, formatter service ve summary model icin hizli compile ve smoke test calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================"
Write-Host "JHoster Desktop Workflow Summary Compile"
Write-Host "========================================"

$javac = Get-Command javac -ErrorAction SilentlyContinue
$java = Get-Command java -ErrorAction SilentlyContinue

if ($null -eq $javac -or $null -eq $java) {
    Write-Host "Java JDK bulunamadi. JAVA_HOME veya PATH ayarini kontrol edin."
    exit 1
}

$OutDir = Join-Path $ScriptDir "target\workflow-summary-test"
$TempDir = Join-Path $ScriptDir "target\workflow-summary-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestWorkflowFormatter.java"
$TestSource = @'
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.WorkflowDesktopSummary;
import com.jhoster.desktop.services.WorkflowResultFormatterService;

public class TestWorkflowFormatter {
    public static void main(String[] args) {
        String body = "{\"success\":true,\"status\":\"planned\",\"message\":\"dry run\",\"run_id\":\"jhw-demo-123\",\"workflow\":{\"project_code\":\"demo-site\",\"web_server\":\"nginx\",\"step_count\":5,\"steps\":[{\"name\":\"profile\"}]}}";
        WorkflowDesktopSummary summary = new WorkflowResultFormatterService().formatPlan(DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("success parse failed");
        }
        if (!"planned".equals(summary.getStatus())) {
            throw new IllegalStateException("status parse failed");
        }
        if (!"jhw-demo-123".equals(summary.getRunId())) {
            throw new IllegalStateException("run id parse failed");
        }
        if (!"nginx".equals(summary.getWebServer())) {
            throw new IllegalStateException("web server parse failed");
        }
        if (summary.getStepCount() != 5) {
            throw new IllegalStateException("step count parse failed");
        }
        System.out.println("Workflow summary parser OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\WebServerWorkflowRequest.java `
    src\main\java\com\jhoster\desktop\models\WorkflowDesktopSummary.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\bin\WorkflowResultFormatterService.java `
    src\main\java\com\jhoster\desktop\bin\WebServerWorkflowDesktopService.java `
    $TestFile

java -cp $OutDir TestWorkflowFormatter

Write-Host "Desktop workflow summary compile tamamlandi."
