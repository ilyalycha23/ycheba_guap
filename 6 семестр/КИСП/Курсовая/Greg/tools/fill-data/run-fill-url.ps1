# Open demo data processor in 1C (auto-fills on form open)
param([string]$UserName)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = $PSScriptRoot
$settings = Get-Content (Join-Path $ScriptDir "settings.json") -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $UserName) { $UserName = $settings.UserName }

$InfoBasePath = (Resolve-Path (Join-Path $ScriptDir "..\..\..")).Path
$V8Path = $settings.V8Path
$url = $settings.FillDataProcessorUrl
$LogFile = Join-Path $ScriptDir "build\fill-url-log.txt"
if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

$arguments = @(
    "ENTERPRISE",
    "/F", "`"$InfoBasePath`"",
    "/N`"$UserName`"",
    "/URL", "`"$url`"",
    "/DisableStartupDialogs",
    "/Out", "`"$LogFile`""
)

Write-Host "Opening URL from settings.json"
Write-Host "InfoBase: $InfoBasePath"
$p = Start-Process -FilePath $V8Path -ArgumentList $arguments -NoNewWindow -Wait -PassThru
Write-Host "Exit code: $($p.ExitCode)"
if (Test-Path $LogFile) { Get-Content $LogFile -Encoding UTF8 }
exit $p.ExitCode
