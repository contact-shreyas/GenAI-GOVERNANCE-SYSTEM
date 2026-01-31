# GenAI Governance System - Startup Script
# This script ensures both services stay running

function Start-System {
    Write-Host "`n╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  GenAI Governance System - Auto Start    ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    
    # Kill any existing processes
    Write-Host "Cleaning up existing processes..." -ForegroundColor Yellow
    Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "[1] Starting Backend API (Port 8000)..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; & '..\.venv_new\Scripts\python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000" -WindowStyle Normal
    
    Start-Sleep -Seconds 3
    
    Write-Host "[2] Starting Frontend (Port 3000)..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev -- --hostname 127.0.0.1 --port 3000" -WindowStyle Normal
    
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  SERVICES STARTED - CHECK NEW WINDOWS    ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "ENDPOINTS:" -ForegroundColor Yellow
    Write-Host "  Frontend:    http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  Backend:     http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "DO NOT CLOSE THE NEW WINDOWS!" -ForegroundColor Red
    Write-Host "Services will stop when you close those windows." -ForegroundColor Red
    Write-Host ""
    
    # Keep monitoring
    Write-Host "Monitoring services..." -ForegroundColor Yellow
    while ($true) {
        $backendRunning = (netstat -ano 2>$null | Select-String ":8000.*LISTENING") -ne $null
        $frontendRunning = (netstat -ano 2>$null | Select-String ":3000.*LISTENING") -ne $null
        
        if (-not $backendRunning -or -not $frontendRunning) {
            Write-Host "[$(Get-Date)] WARNING: One or more services stopped!" -ForegroundColor Red
            Write-Host "  Backend: $(if($backendRunning) {'RUNNING'} else {'STOPPED'})"
            Write-Host "  Frontend: $(if($frontendRunning) {'RUNNING'} else {'STOPPED'})"
        } else {
            Write-Host "[$(Get-Date)] Services OK - Backend: 8000, Frontend: 3000" -ForegroundColor Green
        }
        
        Start-Sleep -Seconds 10
    }
}

# Run the startup function
Start-System
