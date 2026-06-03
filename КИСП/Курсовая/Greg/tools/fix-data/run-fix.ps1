# Fix broken task addressing references in cinema center infobase
$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = $PSScriptRoot
$InfoBasePath = (Resolve-Path (Join-Path $ScriptDir "..\..\..")).Path
$V8Path = "C:\Program Files (x86)\1cv8t\8.5.1.1150\bin\1cv8t.exe"
$UserName = "Администратор"
$SrcFile = (Get-ChildItem -Path (Join-Path $ScriptDir "src") -Filter "*.xml" | Select-Object -First 1).FullName
$BuildDir = Join-Path $ScriptDir "build"
$EpfFile = Join-Path $BuildDir "FixData.epf"
$LogFile = Join-Path $BuildDir "fix-log.txt"
$DtFile = (Resolve-Path (Join-Path $ScriptDir "..\..\КурсоваяИТОГ.dt")).Path

New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null
Get-Process 1cv8* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "=== UpdateDBCfg ===" -ForegroundColor Cyan
$updateArg = @(
    "DESIGNER",
    "/F", $InfoBasePath,
    "/N$UserName",
    "/UpdateDBCfg",
    "/DisableStartupDialogs",
    "/Out", (Join-Path $BuildDir "update-log.txt")
)
$p0 = Start-Process -FilePath $V8Path -ArgumentList $updateArg -NoNewWindow -Wait -PassThru
Write-Host "UpdateDBCfg exit: $($p0.ExitCode)"

Write-Host "=== Build fix EPF ===" -ForegroundColor Cyan
$buildArg = @(
    "DESIGNER",
    "/LoadExternalDataProcessorOrReportFromFiles", $SrcFile, $EpfFile,
    "/DisableStartupDialogs",
    "/Out", (Join-Path $BuildDir "build-log.txt")
)
$p1 = Start-Process -FilePath $V8Path -ArgumentList $buildArg -NoNewWindow -Wait -PassThru
if ($p1.ExitCode -ne 0 -or -not (Test-Path $EpfFile)) {
    $buildLog = Join-Path $BuildDir "build-log.txt"
    if (Test-Path $buildLog) { Get-Content $buildLog -Encoding UTF8 }
    throw "EPF build failed"
}

if (Test-Path $LogFile) { Remove-Item $LogFile -Force }

Write-Host "=== Run fix ===" -ForegroundColor Cyan
$runArg = @(
    "ENTERPRISE",
    "/F", $InfoBasePath,
    "/N$UserName",
    "/Execute", $EpfFile,
    "/DisableStartupDialogs",
    "/Out", $LogFile
)
$p2 = Start-Process -FilePath $V8Path -ArgumentList $runArg -NoNewWindow -Wait -PassThru
Write-Host "Fix exit: $($p2.ExitCode)"
if (Test-Path $LogFile) { Get-Content $LogFile -Encoding UTF8 }

Write-Host "=== Dump IB ===" -ForegroundColor Cyan
Get-Process 1cv8* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$dumpArg = @(
    "DESIGNER",
    "/F", $InfoBasePath,
    "/N$UserName",
    "/DumpIB", $DtFile,
    "/DisableStartupDialogs",
    "/Out", (Join-Path $BuildDir "dump-log.txt")
)
$p3 = Start-Process -FilePath $V8Path -ArgumentList $dumpArg -NoNewWindow -Wait -PassThru
Write-Host "Dump exit: $($p3.ExitCode)"

exit $p2.ExitCode
