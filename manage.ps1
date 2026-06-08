param(
    [string]$Command = "",
    [string]$Component = ""
)

$BASE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PID_DIR  = Join-Path $BASE_DIR ".manage_pids"
if (-not (Test-Path $PID_DIR)) { New-Item -ItemType Directory -Path $PID_DIR -Force | Out-Null }

$BACKEND_PID  = Join-Path $PID_DIR "backend.pid"
$FRONTEND_PID = Join-Path $PID_DIR "frontend.pid"
$NGINX_PID    = Join-Path $PID_DIR "nginx.pid"

function Write-Info   { Write-Host "[$($args[0])] $($args[1])" -ForegroundColor Cyan }
function Write-Ok     { Write-Host "[$($args[0])] $($args[1])" -ForegroundColor Green }
function Write-Warn   { Write-Host "[$($args[0])] $($args[1])" -ForegroundColor Yellow }
function Write-Err    { Write-Host "[$($args[0])] $($args[1])" -ForegroundColor Red }

function Read-Pid($file) {
    if (-not (Test-Path $file)) { return $null }
    $procId = (Get-Content $file -Raw).Trim()
    if (-not $procId) { return $null }
    return $procId
}

function Is-Running($file) {
    $procId = Read-Pid $file
    if (-not $procId) { return $false }
    $p = Get-Process -Id $procId -ErrorAction SilentlyContinue
    return ($p -ne $null)
}

function Kill-Proc($file) {
    $procId = Read-Pid $file
    if ($procId) {
        taskkill /F /T /PID $procId 2>$null
        Start-Sleep -Milliseconds 500
    }
    if (Test-Path $file) { Remove-Item $file -Force }
}

# ---- Port Check ----

function Get-BackendPort {
    $envFile = Join-Path $BASE_DIR "backend\.env"
    if (Test-Path $envFile) {
        $match = Select-String "^APP_PORT=(\d+)" $envFile
        if ($match) { return $match.Matches.Groups[1].Value }
    }
    return "8000"  # fallback: main.py default
}

function Test-PortInUse($port) {
    $conn = netstat -an | Select-String "LISTENING" | Select-String ":$port "
    return ($conn -ne $null)
}

# ---- Backend ----

function Start-Backend {
    if (Is-Running $BACKEND_PID) {
        Write-Info "backend" "already running (PID $(Read-Pid $BACKEND_PID))"
        return
    }
    $port = Get-BackendPort
    if (Test-PortInUse $port) {
        Write-Err "backend" "port $port is already in use — aborting startup"
        exit 1
    }
    $python = "E:\Users\April\miniforge3\envs\polyplex\python.exe"
    if (-not (Test-Path $python)) {
        $python = (Get-Command "python" -ErrorAction SilentlyContinue).Source
    }
    if (-not $python) {
        Write-Err "backend" "python not found"
        return
    }
    Push-Location "$BASE_DIR/backend"
    $proc = Start-Process -FilePath $python -ArgumentList "main.py" -WindowStyle Normal -PassThru
    $proc.Id | Out-File $BACKEND_PID -Encoding ASCII
    Pop-Location
    Write-Ok "backend" "started (PID $($proc.Id))"
}

function Stop-Backend {
    Kill-Proc $BACKEND_PID
    Write-Ok "backend" "stopped"
}

# ---- Frontend ----

# ---- Frontend Build ----

function Build-Frontend {
    $npm = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if (-not $npm) { $npm = Get-Command "npm" -ErrorAction SilentlyContinue }
    if (-not $npm) {
        Write-Err "frontend" "npm not found, please install Node.js"
        return $false
    }
    Push-Location "$BASE_DIR/frontend"
    Write-Info "frontend" "building..."
    $proc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm run build" -NoNewWindow -Wait -PassThru
    Pop-Location
    if ($proc.ExitCode -eq 0) {
        Write-Ok "frontend" "build succeeded"
        return $true
    } else {
        Write-Err "frontend" "build failed (exit $($proc.ExitCode))"
        return $false
    }
}

function Start-Frontend {
    if (Is-Running $FRONTEND_PID) {
        Write-Info "frontend" "already running (PID $(Read-Pid $FRONTEND_PID))"
        return
    }
    $npm = Get-Command "npm.cmd" -ErrorAction SilentlyContinue
    if (-not $npm) { $npm = Get-Command "npm" -ErrorAction SilentlyContinue }
    if (-not $npm) {
        Write-Err "frontend" "npm not found, please install Node.js"
        return
    }
    Push-Location "$BASE_DIR/frontend"
    $proc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c npm run dev" -WindowStyle Normal -PassThru
    $proc.Id | Out-File $FRONTEND_PID -Encoding ASCII
    Pop-Location
    Write-Ok "frontend" "started (PID $($proc.Id))"
}

function Stop-Frontend {
    Kill-Proc $FRONTEND_PID
    # 清理残留的 node 进程
    Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Ok "frontend" "stopped"
}

# ---- Nginx ----

function Start-Nginx {
    $nginx_exe = "$BASE_DIR/nginx/nginx.exe"
    if (-not (Test-Path $nginx_exe)) {
        Write-Err "nginx" "not found: $nginx_exe"
        return
    }
    # 确保 logs/ 和 temp/ 目录存在
    $logs_dir = "$BASE_DIR/nginx/logs"
    $temp_dir = "$BASE_DIR/nginx/temp"
    if (-not (Test-Path $logs_dir)) { New-Item -ItemType Directory -Path $logs_dir -Force | Out-Null }
    if (-not (Test-Path $temp_dir)) { New-Item -ItemType Directory -Path $temp_dir -Force | Out-Null }

    $proc = Start-Process -FilePath $nginx_exe -ArgumentList "-p `"$BASE_DIR/nginx`" -c conf/nginx.conf" -NoNewWindow -PassThru
    Start-Sleep -Milliseconds 500
    $lines = tasklist /NH /FO CSV /FI "IMAGENAME eq nginx.exe" 2>$null
    if ($lines) {
        foreach ($line in $lines) {
            if ($line -match "nginx") {
                $procId = ($line -split '","')[1] -replace '"', ''
                $procId = $procId.Trim()
                if ($procId) { $procId | Out-File $NGINX_PID -Encoding ASCII; break }
            }
        }
    }
    Write-Ok "nginx" "started"
}

function Stop-Nginx {
    $nginx_exe = "$BASE_DIR/nginx/nginx.exe"
    if (Test-Path $nginx_exe) {
        & $nginx_exe -s quit 2>$null
        Kill-Proc $NGINX_PID
        Write-Ok "nginx" "stopped"
    } else {
        Write-Info "nginx" "not running"
    }
}

# ---- Kill Port ----

function Invoke-KillPort($port) {
    $lines = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
    if (-not $lines) {
        Write-Info "kill-port" "no process is listening on port $port"
        return
    }
    foreach ($line in $lines) {
        $parts = $line -split '\s+'
        $procId = $parts[-1]
        if ($procId -and $procId -match '^\d+$') {
            taskkill /F /PID $procId 2>$null
            Write-Ok "kill-port" "killed PID $procId (was listening on port $port)"
        }
    }
}

# ---- Status ----

function Show-Status {
    $list = @(
        @{name="backend"; file=$BACKEND_PID},
        @{name="frontend"; file=$FRONTEND_PID},
        @{name="nginx"; file=$NGINX_PID}
    )
    foreach ($c in $list) {
        if (Is-Running $c.file) {
            $procId = Read-Pid $c.file
            Write-Ok $c.name "running (PID $procId)"
        } else {
            Write-Info $c.name "stopped"
        }
    }
}

# ---- Main ----

switch ($Command.ToLower()) {
    "start" {
        switch ($Component.ToLower()) {
            "backend"  { Start-Backend }
            "frontend" { Start-Frontend }
            "nginx"    { Start-Nginx }
            default {
                Start-Backend
                if (Build-Frontend) { Start-Nginx }
            }
        }
    }
    "stop" {
        switch ($Component.ToLower()) {
            "backend"  { Stop-Backend }
            "frontend" { Stop-Frontend }
            "nginx"    { Stop-Nginx }
            default {
                Stop-Nginx
                Stop-Frontend
                Stop-Backend
            }
        }
    }
    "restart" {
        if ($Component.ToLower() -eq "frontend") {
            # restart frontend → 开发模式重启（kill dev server + 重新启动）
            Stop-Frontend
            Start-Sleep 1
            Start-Frontend
        } elseif ($Component -ne "") {
            # restart backend / nginx
            & $MyInvocation.MyCommand.Path stop $Component
            Start-Sleep 1
            & $MyInvocation.MyCommand.Path start $Component
        } else {
            # restart → 生产模式：停止全部 + 构建 + 启动
            & $MyInvocation.MyCommand.Path stop
            Start-Sleep 1
            Start-Backend
            if (Build-Frontend) { Start-Nginx }
        }
    }
    "build" {
        switch ($Component.ToLower()) {
            "frontend" { Build-Frontend }
            default    { Build-Frontend }
        }
    }
    "rebuild" {
        switch ($Component.ToLower()) {
            "frontend" {
                Stop-Nginx
                Start-Sleep 1
                if (Build-Frontend) { Start-Nginx }
            }
        }
    }
    "kill-port" {
        if (-not $Component -or $Component -notmatch '^\d+$') {
            Write-Err "kill-port" "usage: manage.ps1 kill-port <port>"
            exit 1
        }
        Invoke-KillPort $Component
    }
    "status" {
        Show-Status
    }
    default {
        Write-Host "PolyPlex Manager"
        Write-Host ""
        Write-Host "Usage: manage.ps1 <command> [component]"
        Write-Host ""
        Write-Host "Commands:"
        Write-Host "  start [component]       Start all (build frontend, start backend + nginx)"
        Write-Host "                          or a specific component"
        Write-Host "  stop  [component]       Stop all or a specific component"
        Write-Host "  restart [component]     Restart:"
        Write-Host "    restart               stop all + build frontend + start backend + nginx"
        Write-Host "    restart frontend      kill dev server + restart dev server"
        Write-Host "    restart backend/nginx  stop + start 指定组件"
        Write-Host "  build frontend          Build frontend only (npm run build)"
        Write-Host "  rebuild frontend        Stop nginx + build frontend + start nginx"
        Write-Host "  kill-port <port>        Kill process occupying a port"
        Write-Host "  status                  Show running status of all components"
        Write-Host ""
        Write-Host "Components: backend, frontend, nginx"
        Write-Host "  'start frontend' runs the Vite dev server (for development)"
        Write-Host "  'start' (default) builds frontend + starts nginx (for production)"
        Write-Host "  'restart frontend' recycles the Vite dev server"
        Write-Host "  'rebuild frontend' rebuilds production bundle and reloads nginx"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  manage.ps1 start"
        Write-Host "  manage.ps1 start backend"
        Write-Host "  manage.ps1 stop"
        Write-Host "  manage.ps1 restart nginx"
        Write-Host "  manage.ps1 build frontend"
        Write-Host "  manage.ps1 rebuild frontend"
        Write-Host "  manage.ps1 kill-port 8000"
        Write-Host "  manage.ps1 status"
    }
}
