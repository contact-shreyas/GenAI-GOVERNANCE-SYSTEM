#!/usr/bin/env pwsh
# Automated startup script for GenAI Governance Platform

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Write-Host "`n=== GenAI Governance Platform Startup ===" -ForegroundColor Cyan

# Check if Docker daemon is running
Write-Host "`n[1/5] Checking Docker daemon..." -ForegroundColor Yellow
$dockerInfo = docker info 2>&1 | Out-String
if ($dockerInfo -notmatch "Server Version") {
    Write-Host "Docker daemon not running. Starting Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe" -ErrorAction SilentlyContinue
    
    Write-Host "Waiting for Docker daemon to start (max 60s)..." -ForegroundColor Yellow
    $timeout = 60
    $elapsed = 0
    while ($elapsed -lt $timeout) {
        Start-Sleep -Seconds 3
        $elapsed += 3
        $dockerInfo = docker info 2>&1 | Out-String
        if ($dockerInfo -match "Server Version") {
            Write-Host "Docker daemon is ready!" -ForegroundColor Green
            break
        }
        Write-Host "  Still waiting... ($elapsed/$timeout seconds)" -ForegroundColor Gray
    }
    
    if ($elapsed -ge $timeout) {
        Write-Host "`nERROR: Docker daemon did not start within $timeout seconds." -ForegroundColor Red
        Write-Host "Please start Docker Desktop manually and run this script again." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Docker daemon is running." -ForegroundColor Green
}

# Build images
Write-Host "`n[2/5] Building Docker images..." -ForegroundColor Yellow
docker compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker build failed." -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "`n[3/5] Starting services..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to start services." -ForegroundColor Red
    exit 1
}

# Wait for services to be healthy
Write-Host "`n[4/5] Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run migrations
Write-Host "`n[5/5] Running database migrations..." -ForegroundColor Yellow
docker compose exec -T backend alembic -c /app/alembic.ini upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Migration failed. Services may not be fully ready yet." -ForegroundColor Yellow
}

# Show status
Write-Host "`n=== Service Status ===" -ForegroundColor Cyan
docker compose ps

Write-Host "`n=== Access Points ===" -ForegroundColor Cyan
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Green
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Green
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  Postgres:  localhost:15432" -ForegroundColor Green
Write-Host "  Redis:     localhost:16379" -ForegroundColor Green

Write-Host "`n=== View Logs ===" -ForegroundColor Cyan
Write-Host "  All:       docker compose logs -f" -ForegroundColor Gray
Write-Host "  Backend:   docker compose logs -f backend" -ForegroundColor Gray
Write-Host "  Frontend:  docker compose logs -f frontend" -ForegroundColor Gray

Write-Host "`n=== Stop Services ===" -ForegroundColor Cyan
Write-Host "  docker compose down" -ForegroundColor Gray

Write-Host "`nStartup complete! `n" -ForegroundColor Green
