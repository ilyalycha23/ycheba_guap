# Batch fill demo data via /C FillDemoData
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = $PSScriptRoot
$settings = Get-Content (Join-Path $ScriptDir "settings.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$InfoBasePath = (Resolve-Path (Join-Path $ScriptDir "..\..\..")).Path
$V8Path = $settings.V8Path
$UserName = $settings.UserName
$LogFile = Join-Path $ScriptDir "build\fill-batch.log"
New-Item -ItemType Directory -Path (Split-Path $LogFile) -Force | Out-Null
if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

$runArg = "ENTERPRISE /F `"$InfoBasePath`" /N`"$UserName`" /C`"FillDemoData`" /DisableStartupDialogs /Out `"$LogFile`""
Write-Host "Running batch fill..."
Write-Host $runArg

$p = Start-Process -FilePath $V8Path -ArgumentList $runArg -PassThru -NoNewWindow

$timeoutSec = 600
$elapsed = 0
while (-not $p.HasExited -and $elapsed -lt $timeoutSec) {
    Start-Sleep -Seconds 2
    $elapsed += 2
}

if (-not $p.HasExited) {
    Write-Host "Timeout after ${timeoutSec}s, stopping 1C..."
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
    Get-Process 1cv8* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    exit 2
}

Write-Host "Exit code: $($p.ExitCode)"
if (Test-Path $LogFile) {
    Write-Host "=== Log ==="
    Get-Content $LogFile -Encoding UTF8
}
exit $p.ExitCode
