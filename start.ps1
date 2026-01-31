# Docker Quick Start Script for Windows PowerShell

Write-Host "===============================================" -ForegroundColor Green
Write-Host "GenAI Governance - Docker Startup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

$project = "d:\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"
cd $project

# Step 1: Check Docker is running
Write-Host "`n[1/6] Checking Docker daemon..." -ForegroundColor Cyan
$dockerInfo = docker info 2>$null
if (-not $dockerInfo) {
    Write-Host "❌ Docker daemon not running. Please start Docker Desktop and retry." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker daemon is running" -ForegroundColor Green

# Step 2: Kill local Postgres/Redis on old ports (if they exist)
Write-Host "`n[2/6] Checking for port conflicts..." -ForegroundColor Cyan
$postgres = netstat -ano 2>$null | Select-String ":5432"
$redis = netstat -ano 2>$null | Select-String ":6379"

if ($postgres) {
    Write-Host "  ⚠️  Port 5432 in use (local Postgres). Will use 15432 instead." -ForegroundColor Yellow
}
if ($redis) {
    Write-Host "  ⚠️  Port 6379 in use (local Redis). Will use 16379 instead." -ForegroundColor Yellow
}
Write-Host "✅ Port mapping configured" -ForegroundColor Green

# Step 3: Start Postgres and Redis
Write-Host "`n[3/6] Starting Postgres and Redis..." -ForegroundColor Cyan
docker compose up -d postgres redis --wait
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    docker compose logs postgres
    exit 1
}
Write-Host "✅ Services started (postgres: 15432, redis: 16379)" -ForegroundColor Green

# Step 4: Wait for DB to be healthy
Write-Host "`n[4/6] Waiting for Postgres to be ready..." -ForegroundColor Cyan
$ready = $false
$attempts = 0
while (-not $ready -and $attempts -lt 30) {
    try {
        $result = docker compose exec postgres pg_isready -U genai_user -d genai_governance_db 2>$null
        if ($result -match "accepting") {
            $ready = $true
        }
    } catch {}
    $attempts++
    Start-Sleep -Seconds 1
}

if (-not $ready) {
    Write-Host "❌ Postgres did not become ready" -ForegroundColor Red
    docker compose logs postgres
    exit 1
}
Write-Host "✅ Postgres is healthy" -ForegroundColor Green

# Step 5: Run migrations
Write-Host "`n[5/6] Running database migrations..." -ForegroundColor Cyan
docker compose run --rm backend alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Migrations failed" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Migrations completed" -ForegroundColor Green

# Step 6: Start all services
Write-Host "`n[6/6] Starting Backend and Frontend..." -ForegroundColor Cyan
docker compose up -d backend frontend
Start-Sleep -Seconds 5

Write-Host "`n===============================================" -ForegroundColor Green
Write-Host "✅ STARTUP COMPLETE!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host "`nServices running:" -ForegroundColor Cyan
docker compose ps

Write-Host "`nAccess points:" -ForegroundColor Cyan
Write-Host "  📱 Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  🔌 Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  📖 API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  🗄️  Postgres: localhost:15432 (user: genai_user)" -ForegroundColor White
Write-Host "  ⚡ Redis: localhost:16379" -ForegroundColor White

Write-Host "`nTest the API:" -ForegroundColor Cyan
Write-Host "  curl http://localhost:8000/health" -ForegroundColor Gray

Write-Host "`nView logs:" -ForegroundColor Cyan
Write-Host "  docker compose logs -f backend" -ForegroundColor Gray
Write-Host "  docker compose logs -f frontend" -ForegroundColor Gray

Write-Host "`nStop services:" -ForegroundColor Cyan
Write-Host "  docker compose down" -ForegroundColor Gray

Write-Host ""
