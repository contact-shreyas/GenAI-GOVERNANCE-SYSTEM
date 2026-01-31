@echo off
REM Simple startup script - skip cleanup, build fresh

echo ===============================================
echo GenAI Governance - Quick Start
echo ===============================================

cd /d "d:\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

echo.
echo [1/3] Building images (this takes 2-3 minutes)...
docker compose build --no-cache

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Build failed. Check if Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting all services...
docker compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to start services
    pause
    exit /b 1
)

echo.
echo [3/3] Waiting for services (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo ===============================================
echo SERVICES STARTED!
echo ===============================================
echo.
docker compose ps
echo.
echo === Access Points ===
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo === Next Steps ===
echo   Run migrations: docker compose exec backend alembic -c /app/alembic.ini upgrade head
echo   View logs:      docker compose logs -f
echo   Stop services:  docker compose down
echo.
pause
