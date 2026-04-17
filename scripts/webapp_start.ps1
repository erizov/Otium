param(
  [int]$Port = 8000,
  [string]$BindHost = "127.0.0.1"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $root ".webapp.pid"

if (Test-Path $pidFile) {
  try {
    $existingPid = [int](Get-Content $pidFile -Raw).Trim()
    if ($existingPid -gt 0) {
      $p = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
      if ($p) {
        Write-Host "Webapp already running (pid=$existingPid)."
        exit 0
      }
    }
  } catch {
    # Ignore and continue.
  }
  Remove-Item $pidFile -ErrorAction SilentlyContinue
}

Write-Host "Starting webapp on http://$BindHost`:$Port ..."

$uvicornArgs = @(
  "-m",
  "uvicorn",
  "webapp.server.app:app",
  "--host",
  $BindHost,
  "--port",
  "$Port",
  "--reload"
)

$proc = Start-Process -FilePath "python" -ArgumentList $uvicornArgs -PassThru -WindowStyle Normal
$proc.Id | Out-File -FilePath $pidFile -Encoding ascii -Force

Write-Host "Started (pid=$($proc.Id)). PID file: $pidFile"

