# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-license-status-compile.ps1
# 📌 Amac: Desktop license status formatter ve service siniflarini Maven olmadan derler
# 📌 Modul - PowerShell
# Version: 3.65.0
# Aciklama: LicensePlanSummary ve LicenseResultFormatterService parser akisinin javac ile dogrulanmasini saglar
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

$OutDir = Join-Path $ScriptDir "target\license-status-test"
$TempDir = Join-Path $ScriptDir "target\license-status-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$TestFile = Join-Path $TempDir "TestLicenseFormatter.java"
$TestSource = @'
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.LicensePlanSummary;
import com.jhoster.desktop.services.LicenseResultFormatterService;

public class TestLicenseFormatter {
    public static void main(String[] args) {
        String body = "{\"success\":true,\"plan_key\":\"community\",\"plan_label\":\"Community\",\"active_project_count\":4,\"max_active_projects\":5,\"usage_label\":\"4 / 5\",\"can_create_project\":true,\"message\":\"project create allowed\",\"upgrade_hint\":\"Pro unlocks more\"}";
        LicensePlanSummary summary = new LicenseResultFormatterService().format(DesktopHttpResult.success(200, body));
        if (!summary.isSuccess()) {
            throw new IllegalStateException("success parse failed");
        }
        if (!"Community".equals(summary.getPlanLabel())) {
            throw new IllegalStateException("plan label parse failed");
        }
        if (!"4 / 5".equals(summary.getUsageLabel())) {
            throw new IllegalStateException("usage parse failed");
        }
        if (!summary.canCreateProject()) {
            throw new IllegalStateException("can create parse failed");
        }
        System.out.println("License formatter OK");
    }
}
'@

Set-Content -Path $TestFile -Value $TestSource -Encoding UTF8

javac -encoding UTF-8 -d $OutDir `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\LicensePlanSummary.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\services\LicenseResultFormatterService.java `
    src\main\java\com\jhoster\desktop\services\LicenseDesktopService.java `
    $TestFile

java -cp $OutDir TestLicenseFormatter

Write-Host "Desktop license status compile tamamlandi."
