# Prevent sleep/hibernate while long build tasks run.
# Stop with: Stop-Process -Id (Get-Content scripts/keep_awake.pid)

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class KeepAwake {
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
    public const uint ES_CONTINUOUS = 0x80000000;
    public const uint ES_SYSTEM_REQUIRED = 0x00000001;
    public const uint ES_DISPLAY_REQUIRED = 0x00000002;
    public const uint ES_AWAYMODE_REQUIRED = 0x00000040;
}
"@

$root = Split-Path -Parent $PSScriptRoot
$log = Join-Path $root "scripts\keep_awake.log"
$pidFile = Join-Path $root "scripts\keep_awake.pid"
$flags = [KeepAwake]::ES_CONTINUOUS `
    -bor [KeepAwake]::ES_SYSTEM_REQUIRED `
    -bor [KeepAwake]::ES_DISPLAY_REQUIRED `
    -bor [KeepAwake]::ES_AWAYMODE_REQUIRED

$PID | Out-File -FilePath $pidFile -Encoding ascii -Force
"[$(Get-Date -Format o)] Keep-awake started (PID $PID)" |
    Out-File -FilePath $log -Encoding utf8 -Force

try {
    while ($true) {
        [void][KeepAwake]::SetThreadExecutionState($flags)
        shutdown /a 2>$null | Out-Null
        Start-Sleep -Seconds 30
    }
}
finally {
    [void][KeepAwake]::SetThreadExecutionState([KeepAwake]::ES_CONTINUOUS)
    if (Test-Path $pidFile) {
        Remove-Item $pidFile -Force
    }
    "[$(Get-Date -Format o)] Keep-awake stopped" |
        Add-Content -Path $log -Encoding utf8
}
