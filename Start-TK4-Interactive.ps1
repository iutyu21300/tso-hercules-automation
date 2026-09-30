#Requires -Version 5.1
# ============================================================
# MVS 3.8J TK4- Environment Launcher
# Hercules startup -> IPL wait -> wx3270 with PCOMM keymap
# ============================================================
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$Tk4Dir       = 'C:\Mainframe\TK4-'
$Wx3270Exe    = 'C:\Mainframe\wx3270\wx3270.exe'
$LogFile      = Join-Path $Tk4Dir 'log\3033.log'
$ReadyMarker  = 'Script 5: file scripts/tk4-.rc processing ended'
$MaxWaitMin   = 5

function Write-Status {
    param([string]$Message)
    $ts = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$ts] $Message"
}

function Test-HerculesRunning {
    return [bool](Get-Process -Name 'hercules' -ErrorAction SilentlyContinue)
}

function Test-MvsReady {
    if (-not (Test-Path $LogFile)) { return $false }
    try {
        $raw = Get-Content $LogFile -Raw -ErrorAction SilentlyContinue
        return $raw -and $raw.Contains($ReadyMarker)
    } catch { return $false }
}

function Test-Port3270 {
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $client.Connect('127.0.0.1', 3270)
        $client.Close()
        return $true
    } catch { return $false }
}

Write-Host ''
Write-Host '============================================================'
Write-Host '  MVS 3.8J TK4-  Environment Launcher'
Write-Host '============================================================'
Write-Host ''

# --- 1. Check Hercules process ---
if (Test-HerculesRunning) {
    Write-Status 'Hercules is already running.'

    if (Test-MvsReady) {
        Write-Status 'MVS IPL is already complete.'
    } else {
        Write-Status 'Waiting for MVS IPL to finish...'
        $deadline = (Get-Date).AddMinutes($MaxWaitMin)
        while (-not (Test-MvsReady)) {
            if ((Get-Date) -gt $deadline) {
                Write-Host ''
                Write-Warning 'Timeout waiting for MVS IPL.'
                Write-Host 'Check log: C:\Mainframe\TK4-\log\3033.log'
                exit 1
            }
            Start-Sleep -Seconds 3
        }
        Write-Status 'MVS IPL complete.'
    }
} else {
    Write-Status 'Starting Hercules...'

    $null = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', 'mvs.bat' `
        -WorkingDirectory $Tk4Dir -WindowStyle Hidden

    Start-Sleep -Seconds 5

    if (-not (Test-HerculesRunning)) {
        Write-Error 'Failed to start Hercules.'
        exit 1
    }

    Write-Status 'Hercules started. Waiting for MVS IPL... (about 2 min)'
    Write-Status 'Progress will be shown below.'
    Write-Host ''

    $deadline      = (Get-Date).AddMinutes($MaxWaitMin)
    $lastLineCount = 0
    $lastReport    = Get-Date

    while (-not (Test-MvsReady)) {
        if ((Get-Date) -gt $deadline) {
            Write-Host ''
            Write-Warning 'Timeout waiting for MVS IPL.'
            Write-Host 'Check log: C:\Mainframe\TK4-\log\3033.log'
            exit 1
        }

        if (Test-Path $LogFile) {
            $lines = @(Get-Content $LogFile -ErrorAction SilentlyContinue)
            if ($lines.Count -gt $lastLineCount) {
                $lastLineCount = $lines.Count
                $tail = $lines[-1].Trim()
                if (((Get-Date) - $lastReport).TotalSeconds -ge 20 -and $tail) {
                    $lastReport = Get-Date
                    Write-Status "  IPL in progress... $tail"
                }
            }
        }

        if (-not (Test-HerculesRunning)) {
            Write-Error 'Hercules exited unexpectedly.'
            exit 1
        }

        Start-Sleep -Seconds 3
    }

    Write-Status 'MVS IPL complete!'
    Write-Host ''
}

# --- 2. Verify TCP port 3270 ---
Write-Status 'Checking TN3270 port (3270)...'
$portOk = $false
for ($i = 0; $i -lt 5; $i++) {
    if (Test-Port3270) { $portOk = $true; break }
    Start-Sleep -Seconds 1
}
if (-not $portOk) {
    Write-Error 'Port 3270 is not listening.'
    exit 1
}
Write-Status 'Port 3270 OK.'
Write-Host ''

# --- 3. Launch wx3270 ---
if (-not (Test-Path $Wx3270Exe)) {
    Write-Error "wx3270 not found: $Wx3270Exe"
    exit 1
}

Write-Status 'Launching wx3270 (3278-2, 24x80)...'
Write-Host ''

Start-Process -FilePath $Wx3270Exe -ArgumentList '127.0.0.1', '3270'

Write-Status 'wx3270 launched.'
Write-Host ''
Write-Host '------------------------------------------------------------'
Write-Host '  TSO Logon Instructions (inside wx3270 window)'
Write-Host '------------------------------------------------------------'
Write-Host ''
Write-Host '  1. Press [Enter] on the first screen'
Write-Host '     -> Logon ===> prompt appears'
Write-Host ''
Write-Host '  2. Type "tso" and press [Enter]'
Write-Host '  3. At USERID prompt, type "herc01" and press [Enter]'
Write-Host '  4. At PASSWORD prompt, type "cul8tr" and press [Enter]'
Write-Host ''
Write-Host '  5. When TSO Applications menu appears,'
Write-Host '     press PF3 or type "X" then Enter to exit to READY'
Write-Host ''
Write-Host '  6. At READY prompt, enter TSO commands:'
Write-Host '     e.g. TIME, LISTDS, STATUS, etc.'
Write-Host ''
Write-Host '  7. To end session: type "logoff" and press [Enter]'
Write-Host '     (Always logoff to free the session)'
Write-Host ''
Write-Host '============================================================'
Write-Host ''

Write-Host 'Press Enter to close this window...'
$null = Read-Host
