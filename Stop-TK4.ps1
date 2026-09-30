#Requires -Version 5.1
# ============================================================
# MVS 3.8J TK4- Environment Stopper
# Stop Hercules + wc3270 + s3270 safely
# ============================================================
[CmdletBinding()]
param()

$ErrorActionPreference = 'Continue'

function Test-ProcessRunning {
    param([string]$Name)
    return [bool](Get-Process -Name $Name -ErrorAction SilentlyContinue)
}

Write-Host ''
Write-Host '============================================================'
Write-Host '  MVS 3.8J TK4-  Environment Stopper'
Write-Host '============================================================'
Write-Host ''

$stopped = $false

# --- wc3270 stop ---
if (Test-ProcessRunning 'wc3270') {
    Write-Host '[1/3] Stopping wc3270...'
    Get-Process -Name 'wc3270' -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 1
    $stopped = $true
} else {
    Write-Host '[1/3] wc3270 is not running.'
}

# --- s3270 stop ---
if (Test-ProcessRunning 's3270') {
    Write-Host '[2/3] Stopping s3270...'
    Get-Process -Name 's3270' -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 1
    $stopped = $true
} else {
    Write-Host '[2/3] s3270 is not running.'
}

# --- Hercules stop ---
if (Test-ProcessRunning 'hercules') {
    Write-Host '[3/3] Stopping Hercules...'
    Get-Process -Name 'hercules' -ErrorAction SilentlyContinue | Stop-Process -Force
    $stopped = $true
} else {
    Write-Host '[3/3] Hercules is not running.'
}

if ($stopped) {
    Start-Sleep -Seconds 2
    Write-Host ''
    Write-Host 'All processes stopped.'
} else {
    Write-Host ''
    Write-Host 'No processes to stop.'
}

Write-Host ''
Write-Host 'Press Enter to close...'
$null = Read-Host
