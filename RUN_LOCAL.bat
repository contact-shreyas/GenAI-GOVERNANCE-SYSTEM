@echo off
REM Local Development Startup (No Docker Required)
REM This script starts the backend (FastAPI) and frontend (Next.js) locally

setlocal enabledelayedexpansion
set "VENV_DIR=%CD%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

echo.
echo ================================================================
echo   GenAI Governance Layer - Local Development Setup
echo ================================================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)
echo OK: Python found

REM Create virtual environment if missing
if not exist "%VENV_PY%" (
    echo Creating virtual environment at %VENV_DIR% ...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment. Free disk space and retry.
        pause
        exit /b 1
    )
)

REM Check Node
echo [2/4] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 20+
    pause
    exit /b 1
)
echo OK: Node.js found

REM Install Backend Dependencies
echo [3/4] Installing Python dependencies (inside virtual env)...
cd backend
echo Installing requirements (no-cache; skipping pip upgrade)...
"%VENV_PY%" -m pip install --no-cache-dir -r requirements-minimal.txt
if errorlevel 1 (
    echo ERROR: Python dependencies failed to install. Common fixes:
    echo   - Free disk space (pip needs space to unpack wheels)
    echo   - Run: "%VENV_PY%" -m pip cache purge
    echo   - Ensure internet connectivity
    echo   - If build tools missing, install "Build Tools for Visual Studio"
    echo   - Re-run this script after fixing
    pause
    exit /b 1
)
echo Initializing SQLite database...
"%VENV_PY%" init_db.py
cd ..
echo OK: Backend dependencies installed

REM Install Frontend Dependencies
echo [4/4] Installing Node dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed. Please review the errors above.
    pause
    exit /b 1
)
cd ..
echo OK: Frontend dependencies installed

echo.
echo ================================================================
echo   Starting Services...
echo ================================================================
echo.
echo Backend URL:  http://localhost:8000
echo Frontend URL: http://localhost:3000
echo.
echo IMPORTANT: You'll see TWO command windows open. Keep both open!
echo.
pause

REM Start Backend in new window
echo Starting FastAPI backend...
start "GenAI Backend" cmd /k "cd backend && "%VENV_PY%" main.py"

REM Wait for backend to start
echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak

REM Start Frontend in new window
echo Starting Next.js frontend...
start "GenAI Frontend" cmd /k "cd frontend && npm run dev"

REM Wait for frontend to start
echo Waiting 3 seconds for frontend to initialize...
timeout /t 3 /nobreak

REM Open browser
echo Opening browser...
timeout /t 2 /nobreak
start http://localhost:3000

echo.
echo ================================================================
echo   ✓ Services Started!
echo ================================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs:     http://localhost:8000/docs
echo.
echo IMPORTANT:
echo - Two command windows should be open (backend + frontend)
echo - Keep both windows open while developing
echo - To stop: Close both command windows
echo.
pause
