param()

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $root ".webapp.pid"

if (-not (Test-Path $pidFile)) {
  Write-Host "No PID file found ($pidFile). Nothing to stop."
  exit 0
}

try {
  $pid = [int](Get-Content $pidFile -Raw).Trim()
} catch {
  Remove-Item $pidFile -ErrorAction SilentlyContinue
  Write-Host "PID file was invalid; removed."
  exit 0
}

$p = Get-Process -Id $pid -ErrorAction SilentlyContinue
if (-not $p) {
  Remove-Item $pidFile -ErrorAction SilentlyContinue
  Write-Host "Process not found (pid=$pid); removed PID file."
  exit 0
}

Write-Host "Stopping webapp (pid=$pid) ..."
Stop-Process -Id $pid -Force
Start-Sleep -Milliseconds 250
Remove-Item $pidFile -ErrorAction SilentlyContinue
Write-Host "Stopped."

