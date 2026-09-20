# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-release-cleanliness-guard.ps1
# 📌 Amac: Release paketinde gereksiz uretilmis dosya kalmadigini denetler
# 📌 Modul - PowerShell
# Version: 3.75.0
# Aciklama: __pycache__, pyc, tmp, bak, class, target ve log dosyalarini engeller
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "../..")
$files = Get-ChildItem -Path $RootPath -Recurse -Force -File -ErrorAction SilentlyContinue
$matches = @()

foreach ($file in $files) {
    $relativePath = $file.FullName.Substring($RootPath.Path.Length).TrimStart("\\", "/")
    $normalizedPath = $relativePath.Replace("/", "\\")

    $isBlocked = $false
    if ($normalizedPath -like "*__pycache__*") { $isBlocked = $true }
    if ($normalizedPath -like "*\target\*") { $isBlocked = $true }
    if ($file.Name -in @(".DS_Store", "Thumbs.db")) { $isBlocked = $true }
    if ($file.Extension -in @(".pyc", ".tmp", ".bak", ".class", ".log")) { $isBlocked = $true }

    if ($isBlocked) {
        $matches += $file.FullName
    }
}

if ($matches.Count -gt 0) {
    $uniqueMatches = $matches | Sort-Object -Unique
    throw "Gereksiz release dosyalari bulundu:`n$($uniqueMatches -join "`n")"
}

Write-Host "Release cleanliness guard passed."
