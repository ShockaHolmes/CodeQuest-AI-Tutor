param(
    [int]$IdleShutdownSeconds = 45,
    [int]$IdlePollSeconds = 5
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AppDir = Join-Path $ScriptDir 'codequest-ai-tutor'
$RootVenvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
$AppVenvPython = Join-Path $AppDir '.venv\Scripts\python.exe'
$AppUrl = 'http://127.0.0.1:8501'
$HealthUrl = "$AppUrl/_stcore/health"
$AppPort = 8501

function Get-PythonCommand {
    if (Test-Path $RootVenvPython) { return $RootVenvPython }
    if (Test-Path $AppVenvPython) { return $AppVenvPython }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) { return $python.Source }

    throw 'Python was not found. Create a virtual environment and install dependencies first.'
}

function Open-Dashboard {
    param([string]$Url)
    Start-Process $Url | Out-Null
}

function Test-ServerReady {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -ge 200 -and $response.StatusCode -lt 300
    }
    catch {
        return $false
    }
}

function Get-ActiveClientCount {
    param(
        [int]$Port,
        [int]$ServerPid
    )

    if (-not (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue)) {
        return -1
    }

    try {
        $connections = Get-NetTCPConnection -State Established -LocalPort $Port -ErrorAction Stop |
            Where-Object {
                $_.OwningProcess -eq $ServerPid -and (
                    $_.RemoteAddress -eq '127.0.0.1' -or
                    $_.RemoteAddress -eq '::1' -or
                    $_.RemoteAddress -eq '::ffff:127.0.0.1'
                )
            }
        return @($connections).Count
    }
    catch {
        return -1
    }
}

if (-not (Test-Path $AppDir)) {
    throw "App folder not found: $AppDir"
}

$pythonCmd = Get-PythonCommand
Set-Location $AppDir

$streamlitCheck = & $pythonCmd -c "import streamlit" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Streamlit is not installed for $pythonCmd. Run: $pythonCmd -m pip install -r requirements.txt"
}

if (Test-ServerReady -Url $HealthUrl) {
    Write-Host 'CodeQuest AI Tutor is already running. Opening dashboard...'
    Open-Dashboard -Url $AppUrl
    exit 0
}

Write-Host 'Starting CodeQuest AI Tutor...'
$serverProcess = Start-Process -FilePath $pythonCmd -ArgumentList '-m streamlit run app/main.py --server.headless true' -PassThru -WindowStyle Hidden

for ($attempt = 1; $attempt -le 30; $attempt++) {
    if (Test-ServerReady -Url $HealthUrl) {
        Write-Host 'Dashboard is ready. Opening browser...'
        Open-Dashboard -Url $AppUrl
        break
    }

    if ($serverProcess.HasExited) {
        throw "The app server exited early with code $($serverProcess.ExitCode)."
    }

    Start-Sleep -Seconds 1
}

if (-not (Test-ServerReady -Url $HealthUrl)) {
    throw 'The app server did not become ready in time.'
}

if ($IdleShutdownSeconds -le 0) {
    Write-Host 'Idle auto-shutdown disabled. Streamlit server will keep running.'
    exit 0
}

if ($IdlePollSeconds -le 0) {
    $IdlePollSeconds = 5
}

Write-Host "Monitoring dashboard activity. Server will stop after $IdleShutdownSeconds seconds with no active dashboard connections."
$idleForSeconds = 0

while (-not $serverProcess.HasExited) {
    $activeClients = Get-ActiveClientCount -Port $AppPort -ServerPid $serverProcess.Id

    if ($activeClients -lt 0) {
        Write-Warning 'Could not detect dashboard connections on this system. Leaving server running.'
        exit 0
    }

    if ($activeClients -gt 0) {
        $idleForSeconds = 0
    }
    else {
        $idleForSeconds += $IdlePollSeconds
    }

    if ($idleForSeconds -ge $IdleShutdownSeconds) {
        Write-Host 'No active dashboard connections detected. Stopping Streamlit server...'
        Stop-Process -Id $serverProcess.Id -Force
        Write-Host 'Streamlit server stopped.'
        exit 0
    }

    Start-Sleep -Seconds $IdlePollSeconds
}

Write-Host 'Streamlit server exited.'
