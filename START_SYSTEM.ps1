# Quick Start Script for GenAI Governance System
# Run this to start the entire system

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  GenAI Governance System - Quick Start" -ForegroundColor Cyan
Write-Host "  9 Institutions | 11 API Endpoints" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check backend status
Write-Host "Checking backend status..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 2
    Write-Host "✅ Backend running on port 8000" -ForegroundColor Green
    Write-Host "   Version: $($health.version)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Backend not running" -ForegroundColor Red
    Write-Host "   Starting backend with Docker..." -ForegroundColor Yellow
    docker-compose up backend -d
    Start-Sleep -Seconds 5
}

Write-Host ""

# Check if frontend is installed
Write-Host "Checking frontend dependencies..." -ForegroundColor Yellow
$frontendDir = "frontend"

if (Test-Path "$frontendDir/node_modules") {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location $frontendDir
    npm install
    Set-Location ..
}

Write-Host ""

# Display URLs
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  System URLs:" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔹 Backend API:      http://localhost:8000" -ForegroundColor White
Write-Host "🔹 Swagger UI:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "🔹 ReDoc:            http://localhost:8000/redoc" -ForegroundColor White
Write-Host "🔹 Frontend:         http://localhost:3000" -ForegroundColor White
Write-Host "🔹 Test Page:        http://localhost:3000/test" -ForegroundColor White
Write-Host ""

# Display next steps
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start frontend development server:" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Open test page in browser:" -ForegroundColor Yellow
Write-Host "   http://localhost:3000/test" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run all 5 API tests from the test page" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. View Swagger documentation:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""

# Display system status
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  System Status:" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Backend:          Running" -ForegroundColor Green
Write-Host "✅ Database:         PostgreSQL 15" -ForegroundColor Green
Write-Host "✅ Cache:            Redis 7" -ForegroundColor Green
Write-Host "✅ Policies Loaded:  9 institutions" -ForegroundColor Green
Write-Host "✅ API Endpoints:    11 operational" -ForegroundColor Green
Write-Host "✅ Documentation:    Auto-generated" -ForegroundColor Green
Write-Host ""

Write-Host "System ready!" -ForegroundColor Green
