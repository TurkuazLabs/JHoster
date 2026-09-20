# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-service-manager-compile.ps1
# 📌 Amac: Desktop service manager parser ve service siniflarini Maven olmadan javac ile test eder
# 📌 Modul - PowerShell
# Version: 1.1.0
# Aciklama: Service manager summary, formatter ve desktop service katmanlari icin hizli compile ve smoke test calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================"
Write-Host "JHoster Desktop Service Manager Compile"
Write-Host "========================================"

$javac = Get-Command javac -ErrorAction SilentlyContinue
$java = Get-Command java -ErrorAction SilentlyContinue

if ($null -eq $javac -or $null -eq $java) {
    Write-Host "Java JDK bulunamadi. JAVA_HOME veya PATH ayarini kontrol edin."
    exit 1
}

$OutDir = Join-Path $ScriptDir "target\service-manager-test"
$TempDir = Join-Path $ScriptDir "target\service-manager-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestServiceFormatter.java"
$TestSource = @'
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.services.ServiceResultFormatterService;

public class TestServiceFormatter {
    public static void main(String[] args) {
        String body = "{\"success\":true,\"operation\":\"start\",\"message\":\"process marked as running\",\"process\":{\"code\":\"apache\",\"status\":\"running\"}}";
        String preflightBody = "{\"success\":true,\"operation\":\"preflight\",\"message\":\"process preflight ready\",\"process\":{\"code\":\"apache\",\"status\":\"stopped\"}}";
        ServiceManagerSummary preflightSummary = new ServiceResultFormatterService().formatPreflight("apache", DesktopHttpResult.success(200, preflightBody));
        if (!preflightSummary.isSuccess()) {
            throw new IllegalStateException("preflight success parse failed");
        }
        ServiceManagerSummary summary = new ServiceResultFormatterService().formatStart("apache", DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("success parse failed");
        }
        if (!"apache".equals(summary.getServiceCode())) {
            throw new IllegalStateException("service code parse failed");
        }
        if (!"start".equals(summary.getOperation())) {
            throw new IllegalStateException("operation parse failed");
        }
        if (!"running".equals(summary.getStatus())) {
            throw new IllegalStateException("status parse failed");
        }
        System.out.println("Service manager parser OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\ServiceManagerSummary.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\bin\ServiceResultFormatterService.java `
    src\main\java\com\jhoster\desktop\bin\ServiceManagerDesktopService.java `
    $TestFile

java -cp $OutDir TestServiceFormatter

Write-Host "Desktop service manager compile tamamlandi."
