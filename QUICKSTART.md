# Quick Start Instructions

## Prerequisites
1. Docker Desktop installed and running
2. Ports available: 3000, 8000, 15432, 16379

## Start Project (One Command)
```cmd
start.bat
```

This will:
- Clean old containers
- Build images with minimal dependencies (fast build ~2-3 min)
- Start all services
- Run database migrations
- Show access URLs

## Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Postgres: localhost:15432
- Redis: localhost:16379

## View Logs
```cmd
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
```

## Stop Services
```cmd
docker compose down
```

## Troubleshooting

### Docker Daemon Not Running
Start Docker Desktop from Start Menu and wait 30 seconds

### Build Hangs
The minimal build excludes heavy ML libraries (torch, transformers).
Full AI features require: `pip install -r requirements.txt` inside container

### Port Conflicts
If ports are in use, edit docker-compose.yml:
- Change `15432:5432` to `25432:5432` (Postgres)
- Change `16379:6379` to `26379:6379` (Redis)

### Migration Fails
Run manually:
```cmd
docker compose run --rm backend alembic -c /app/alembic.ini upgrade head
```

### Reset Everything
```cmd
docker compose down -v
start.bat
```
