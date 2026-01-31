@echo off
REM GenAI Governance System Startup Script
REM This script starts both backend and frontend services in persistent windows

title GenAI Governance System Launcher
color 0A

echo.
echo ========================================
echo  GenAI Governance System Launcher
echo ========================================
echo.
echo Starting services...
echo.

REM Kill any existing Node/npm processes
taskkill /IM node.exe /F 2>nul

REM Start Backend in new window (persistent)
echo [1/2] Starting Backend API (FastAPI - Port 8000)...
start "GenAI Backend API" cmd /k "cd backend && ..\.venv_new\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

REM Start Frontend in new window (persistent)
echo [2/2] Starting Frontend (Next.js - Port 3000)...
start "GenAI Frontend" cmd /k "cd frontend && npm run dev -- --hostname 127.0.0.1 --port 3000"

REM Wait a moment for services to initialize
timeout /t 5 /nobreak

echo.
echo ========================================
echo  SYSTEM STARTING UP
echo ========================================
echo.
echo Both services should now be starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs:     http://localhost:8000/docs
echo.
echo DO NOT CLOSE THESE WINDOWS!
echo The windows will stay open as long as services are running.
echo.
echo Press any key to monitor connections...
pause

REM Keep main window open
:loop
echo.
echo [%date% %time%] System Status: RUNNING
timeout /t 10 /nobreak
goto loop
