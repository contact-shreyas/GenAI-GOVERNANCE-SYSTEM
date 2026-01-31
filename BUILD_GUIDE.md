# Build & Deployment Guide

## Overview

This guide covers building, running, and deploying the GenAI Governance Layer project. The project has been optimized for fast, reliable builds using Docker multi-stage builds, binary wheel caching, and modern tooling (Node 20, pnpm, ESLint, Prettier).

## Prerequisites

### Docker Compose Method (Recommended)
- Docker Desktop 24.0+ or Docker Engine 24.0+
- Docker Compose 2.20+
- 8GB RAM available
- Internet connection for pulling base images

### Local Development
- Python 3.11 with venv
- Node.js 20.0+ and pnpm 8.0+
- PostgreSQL 15 (if running locally, optional with Docker)
- Redis 7 (if running locally, optional with Docker)

## Quick Start (Docker Compose)

### 1. Build and Start All Services

```bash
cd "GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

# First build (pulls images, compiles wheels, builds containers)
docker-compose up --build -d

# Expected output:
# [+] Building 120s (25/25) FINISHED
# [+] Running 4/4
#  ✔ Container postgres-1  Healthy
#  ✔ Container redis-1     Healthy
#  ✔ Container backend-1   Healthy
#  ✔ Container frontend-1  Healthy
```

**Build Time Estimates:**
- First build: **2-3 minutes** (downloads base images, compiles wheels)
- Subsequent builds (code changes): **30-60 seconds** (uses cached layers)
- Production rebuild from scratch: **1-2 minutes**

### 2. Verify Health Status

```bash
# Check all services are healthy
docker-compose ps

# Expected: All services show "healthy" or "Up" status
CONTAINER ID   IMAGE         STATUS
...backend...  ...           Up (healthy)
...frontend... ...           Up (healthy)
...postgres... ...           Up (healthy)
...redis...    ...           Up (healthy)

# Test API health
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "0.1.0", "timestamp": "..."}

# Test frontend
curl http://localhost:3000
# Expected: HTML response from Next.js
```

### 3. Access Applications

- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc (alternative API docs)**: http://localhost:8000/redoc
- **PostgreSQL**: localhost:5432 (genai_user / genai_password)
- **Redis**: localhost:6379

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# (Optional) Load sample policies
docker-compose exec backend python -m scripts.load_sample_policies
```

### 5. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
docker-compose logs -f redis

# Recent logs with timestamps
docker-compose logs --timestamps backend
```

### 6. Stop Services

```bash
# Stop (keep volumes/data)
docker-compose stop

# Restart
docker-compose start

# Stop and remove containers/networks (keep volumes/data)
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

---

## Local Development Setup

### Backend (Python 3.11)

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows PowerShell

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Type checking
mypy .

# Formatting
black .

# Linting
ruff check .
```

### Frontend (Node 20 + pnpm)

```bash
cd frontend

# Install pnpm globally (one-time)
npm install -g pnpm

# Install dependencies with pnpm
pnpm install

# Start dev server
pnpm run dev
# Frontend available at http://localhost:3000

# Build for production
pnpm run build
pnpm run start

# Linting
pnpm run lint
pnpm run lint:fix

# Formatting
pnpm run format
pnpm run format:check

# Type checking
pnpm run type-check

# Tests
pnpm run test
pnpm run test:watch
pnpm run test:coverage
```

---

## Configuration

### Environment Variables

Copy `.env.local.example` to `.env.local` and update:

```bash
cp .env.local.example .env.local
```

**Required for full functionality:**
```env
# OpenAI API key for RAG
OPENAI_API_KEY=sk-...

# Database (auto-configured in docker-compose, change if using external DB)
DATABASE_URL=postgresql://genai_user:genai_password@localhost:5432/genai_governance_db

# Redis (auto-configured in docker-compose)
REDIS_URL=redis://localhost:6379/0

# Security (change in production!)
SECRET_KEY=dev-secret-key-change-in-production-minimum-32-chars
```

**Optional:**
```env
# Use local LLM (Ollama) instead of OpenAI
USE_LOCAL_LLM=false
LOCAL_LLM_URL=http://localhost:11434

# Logging
LOG_RETENTION_DAYS=90
PSEUDONYM_ROTATION_DAYS=30
ENABLE_DETAILED_TRACES=true
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run async tests
pytest tests/ -v -m asyncio
```

### Frontend Tests

```bash
cd frontend

# Run all tests
pnpm run test

# Watch mode
pnpm run test:watch

# With coverage
pnpm run test:coverage
```

### CI/CD (GitHub Actions)

Tests run automatically on:
- Push to `main` or `develop` branches
- All pull requests

View results: **GitHub → Actions tab**

```bash
# Simulate local CI/CD
# Backend
cd backend && pytest tests/ -v && ruff check . && black --check . && mypy .

# Frontend
cd frontend && pnpm install && pnpm run lint && pnpm run format:check && pnpm run type-check && pnpm run test:coverage
```

---

## Troubleshooting

### Docker Issues

**"Port 8000 already in use"**
```bash
# Find and stop service using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
# Modify docker-compose.yml ports section
```

**"Image not found" or connection errors**
```bash
# Force rebuild
docker-compose up --build --force-recreate -d

# Clear dangling images
docker image prune

# Full clean (warning: removes all volumes)
docker-compose down -v
docker system prune -a
```

**Build hanging on "pip install"**
```bash
# Check Docker disk space
docker system df

# If low on space, prune
docker system prune -a --volumes

# Check network connectivity
docker run --rm curlimages/curl http://pypi.org/pypi  # should work
```

### Backend Issues

**"ModuleNotFoundError" after adding packages**
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Or in Docker
docker-compose up --build --no-cache backend
```

**Database connection errors**
```bash
# Check if postgres is running
docker-compose ps | grep postgres

# If not healthy, restart
docker-compose restart postgres

# Verify connection
psql -h localhost -U genai_user -d genai_governance_db
```

### Frontend Issues

**"pnpm: command not found"**
```bash
npm install -g pnpm

# Or use npm directly (fallback)
npm install && npm run dev
```

**".next folder not found" after build**
```bash
# Rebuild Next.js
pnpm run build

# Or in Docker
docker-compose up --build --force-recreate frontend
```

---

## Performance Tips

### Docker Builds

1. **Cache warming**: First build is slow, subsequent builds use layer caching
2. **Multi-stage builds**: Frontend and backend use separate builder/runtime stages to minimize final image size
3. **Buildkit caching**: Docker BuildKit automatically caches pip and pnpm artifacts

### Local Development

1. **Use virtual environments**: Keeps dependencies isolated
2. **Use pnpm**: ~3x faster than npm, better dependency resolution
3. **Enable type checking**: Catches errors before runtime

### Production

1. **Use production docker-compose profile** (create `docker-compose.prod.yml`)
2. **Use managed databases** instead of containerized Postgres/Redis
3. **Enable database connection pooling** with PgBouncer
4. **Use CDN for frontend assets**
5. **Set proper resource limits** in Docker

---

## Key Improvements Made

✅ **Backend Dockerfile**: Multi-stage build with binary wheel caching, non-root user, smaller final image
✅ **Frontend Dockerfile**: Multi-stage Node 20, pnpm, production-ready, non-root user
✅ **Requirements**: Pinned versions, removed conflicts, added pytest-cov
✅ **Package.json**: Node 20, pnpm support, ESLint + Prettier, proper dev/prod scripts
✅ **.dockerignore**: Proper ignore patterns to reduce build context
✅ **docker-compose.yml**: Health checks, explicit networking, volume caching
✅ **GitHub Actions**: Node 20, pnpm, proper caching, pip upgrade before install
✅ **Configuration**: Pydantic v2 proper Field definitions, .env.example updated
✅ **Code Quality**: ESLint, Prettier, Black, Ruff, MyPy configs

---

## Support & Next Steps

For issues:
1. Check logs: `docker-compose logs`
2. See "Troubleshooting" section above
3. Verify prerequisites are met
4. Review GitHub Actions workflows for CI/CD details

Next steps:
1. Configure `.env.local` with your settings
2. Run `docker-compose up --build -d`
3. Visit http://localhost:3000
4. Begin development!
