# Fill demo data into cinema center infobase
param(
    [string]$UserName
)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$settingsPath = Join-Path $ScriptDir "settings.json"
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $UserName) { $UserName = $settings.UserName }
}
$InfoBasePath = (Resolve-Path (Join-Path $ScriptDir "..\..\..")).Path
$V8Path = "C:\Program Files (x86)\1cv8t\8.5.1.1150\bin\1cv8t.exe"
$V8Designer = $V8Path

$SrcFile = (Get-ChildItem -Path (Join-Path $ScriptDir "src") -Filter "*.xml" | Select-Object -First 1).FullName
$BuildDir = Join-Path $ScriptDir "build"
$EpfFile = Join-Path $BuildDir "FillDemoData.epf"
$LogFile = Join-Path $BuildDir "fill-log.txt"

New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

Write-Host "=== Build EPF ===" -ForegroundColor Cyan
$buildArg = "DESIGNER /LoadExternalDataProcessorOrReportFromFiles `"$SrcFile`" `"$EpfFile`" /DisableStartupDialogs /Out `"$BuildDir\build-log.txt`""
Write-Host $buildArg
$bp = Start-Process -FilePath $V8Designer -ArgumentList $buildArg -NoNewWindow -Wait -PassThru
if ($bp.ExitCode -ne 0 -or -not (Test-Path $EpfFile)) {
    if (Test-Path "$BuildDir\build-log.txt") { Get-Content "$BuildDir\build-log.txt" -Encoding UTF8 }
    throw "EPF build failed (code $($bp.ExitCode))"
}

if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

Write-Host "=== Run fill ===" -ForegroundColor Cyan
Write-Host "InfoBase: $InfoBasePath"
Write-Host "User: $UserName"

$runArg = "ENTERPRISE /F `"$InfoBasePath`""
if ($UserName) { $runArg += " /N`"$UserName`"" }
$runArg += " /Execute `"$EpfFile`" /DisableStartupDialogs /Out `"$LogFile`""
Write-Host $runArg
$p = Start-Process -FilePath $V8Path -ArgumentList $runArg -NoNewWindow -Wait -PassThru

Write-Host "Exit code: $($p.ExitCode)"
if (Test-Path $LogFile) {
    Write-Host "=== Log ===" -ForegroundColor Cyan
    Get-Content $LogFile -Encoding UTF8
}

exit $p.ExitCode
