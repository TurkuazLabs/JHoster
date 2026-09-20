# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-css-syntax-guard.ps1
# 📌 Amac: JavaFX CSS tema dosyasindaki desteklenmeyen font-weight degerlerini yakalar
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: -fx-font-weight icin JavaFX uyumlu keyword ve 100-900 arasi yuzluk agirlik degerlerini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$cssPath = "E:\JHoster\app\desktop\src\main\resources\styles\jhoster-modern.css"
$allowedKeywords = @("normal", "bold", "bolder", "lighter")
$allowedNumericValues = @(100, 200, 300, 400, 500, 600, 700, 800, 900)
$errors = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path $cssPath)) {
    throw "CSS dosyasi bulunamadi: $cssPath"
}

$lineNumber = 0
Get-Content $cssPath | ForEach-Object {
    $lineNumber++
    $line = $_.Trim()
    if ($line -match "^-fx-font-weight\s*:\s*([^;]+);") {
        $value = $Matches[1].Trim().ToLowerInvariant()
        $isKeywordAllowed = $allowedKeywords -contains $value
        $isNumeric = $value -match "^\d+$"
        $isNumericAllowed = $false

        if ($isNumeric) {
            $isNumericAllowed = $allowedNumericValues -contains [int]$value
        }

        if (-not $isKeywordAllowed -and -not $isNumericAllowed) {
            $errors.Add("Line $lineNumber invalid -fx-font-weight: $value")
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Host $_ }
    throw "JavaFX CSS font-weight guard failed."
}

Write-Host "JavaFX CSS font-weight guard passed."
