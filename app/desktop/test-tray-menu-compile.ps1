# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-tray-menu-compile.ps1
# 📌 Amac: Desktop tray menu siniflarini JavaFX stub ile Maven olmadan derler
# 📌 Modul - PowerShell
# Version: 3.47.0
# Aciklama: TrayMenuTool ve TrayMenuDesktopService icin hizli javac smoke testi calistirir
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

$OutDir = Join-Path $ScriptDir "target\tray-menu-test"
$StubDir = Join-Path $ScriptDir "target\tray-menu-stub"
$TempDir = Join-Path $ScriptDir "target\tray-menu-temp"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
New-Item -ItemType Directory -Force -Path $StubDir | Out-Null
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $StubDir "javafx\application") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $StubDir "javafx\stage") | Out-Null

Set-Content -Path (Join-Path $StubDir "javafx\application\Platform.java") -Encoding UTF8 -Value @'
package javafx.application;
public final class Platform {
    private Platform() {}
    public static void setImplicitExit(boolean value) {}
    public static void runLater(Runnable runnable) { if (runnable != null) runnable.run(); }
    public static void exit() {}
}
'@

Set-Content -Path (Join-Path $StubDir "javafx\stage\WindowEvent.java") -Encoding UTF8 -Value @'
package javafx.stage;
public class WindowEvent {
    public void consume() {}
}
'@

Set-Content -Path (Join-Path $StubDir "javafx\stage\Stage.java") -Encoding UTF8 -Value @'
package javafx.stage;
import java.util.function.Consumer;
public class Stage {
    public void setOnCloseRequest(Consumer<WindowEvent> handler) {}
    public void hide() {}
    public boolean isShowing() { return true; }
    public void show() {}
    public void toFront() {}
    public void requestFocus() {}
    public void close() {}
}
'@

$TestFile = Join-Path $TempDir "TestTrayMenu.java"
Set-Content -Path $TestFile -Encoding UTF8 -Value @'
import com.jhoster.desktop.tools.TrayMenuTool;

public class TestTrayMenu {
    public static void main(String[] args) {
        TrayMenuTool tool = new TrayMenuTool();
        if (tool == null) {
            throw new IllegalStateException("TrayMenuTool olusmadi");
        }
        System.out.println("Tray menu compile OK");
    }
}
'@

javac -encoding UTF-8 -d $OutDir `
    $StubDir\javafx\application\Platform.java `
    $StubDir\javafx\stage\WindowEvent.java `
    $StubDir\javafx\stage\Stage.java `
    src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java `
    src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java `
    src\main\java\com\jhoster\desktop\models\ServiceManagerSummary.java `
    src\main\java\com\jhoster\desktop\tools\BrowserTool.java `
    src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java `
    src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java `
    src\main\java\com\jhoster\desktop\tools\QuickActionTool.java `
    src\main\java\com\jhoster\desktop\tools\TrayMenuTool.java `
    src\main\java\com\jhoster\desktop\bin\QuickActionDesktopService.java `
    src\main\java\com\jhoster\desktop\bin\ServiceResultFormatterService.java `
    src\main\java\com\jhoster\desktop\bin\ServiceManagerDesktopService.java `
    src\main\java\com\jhoster\desktop\bin\TrayMenuDesktopService.java `
    $TestFile

java -cp $OutDir TestTrayMenu

Write-Host "Desktop tray menu compile tamamlandi."
