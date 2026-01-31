# Quick Start Command Reference

## 🚀 Start Here (5 minutes)

### Setup Environment
```bash
# Copy environment template
cp .env.local.example .env.local

# Edit with your settings (add OPENAI_API_KEY at minimum)
# On Windows, use Notepad or VSCode
```

### Build & Run (2-3 minutes)
```bash
# Build and start all services
docker-compose up --build -d

# Verify all healthy
docker-compose ps

# Test endpoints
curl http://localhost:8000/health        # Backend API
curl http://localhost:3000               # Frontend
```

### Access Applications
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

### Stop Services
```bash
docker-compose down
```

---

## 🔧 Common Development Tasks

### View Logs
```bash
docker-compose logs -f backend      # Backend logs
docker-compose logs -f frontend     # Frontend logs
docker-compose logs -f postgres     # Database logs
docker-compose logs                 # All logs
```

### Run Tests
```bash
# Backend
docker-compose exec backend pytest tests/ -v

# Frontend
docker-compose exec frontend pnpm run test

# Or locally (after setup)
cd backend && pytest tests/ -v
cd frontend && pnpm run test
```

### Code Quality Checks
```bash
# Backend linting
docker-compose exec backend ruff check .
docker-compose exec backend black --check .

# Frontend linting
docker-compose exec frontend pnpm run lint
docker-compose exec frontend pnpm run format:check

# Or locally
cd backend && ruff check . && black --check .
cd frontend && pnpm run lint && pnpm run format:check
```

### Database Operations
```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Load sample data
docker-compose exec backend python -m scripts.load_sample_policies

# Access PostgreSQL CLI
docker-compose exec postgres psql -U genai_user -d genai_governance_db
```

### Rebuild After Changes
```bash
# Full rebuild (recommended after dependency changes)
docker-compose up --build -d

# Quick rebuild (code changes only, uses cache)
docker-compose up -d

# Force fresh build (no cache)
docker-compose up --build --no-cache -d
```

---

## 💻 Local Development (No Docker)

### Backend Setup
```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate          # macOS/Linux
# or
venv\Scripts\activate             # Windows

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000

# In separate terminal, run tests
pytest tests/ -v
```

### Frontend Setup
```bash
cd frontend

# Install pnpm (if needed)
npm install -g pnpm

# Install and run
pnpm install
pnpm run dev                       # http://localhost:3000

# In separate terminal, run linting
pnpm run lint
pnpm run lint:fix                  # Auto-fix issues
pnpm run format                    # Format code
```

---

## 📚 Important Files

| File | Purpose |
|------|---------|
| `BUILD_GUIDE.md` | Comprehensive build & deploy guide |
| `IMPROVEMENTS_SUMMARY.md` | Detailed list of all improvements |
| `IMPROVEMENTS_CHECKLIST.md` | Complete checklist of changes |
| `.env.local.example` | Configuration template |
| `docker-compose.yml` | Local development stack |
| `.github/workflows/test.yml` | CI/CD test pipeline |
| `.github/workflows/lint.yml` | CI/CD linting pipeline |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |
| `backend/config.py` | Backend configuration |
| `backend/models.py` | Pydantic data models |

---

## 🐛 Troubleshooting

### Docker Issues
```bash
# Port already in use
docker-compose down -v                    # Clean up everything

# Build fails
docker-compose up --build --no-cache -d   # Rebuild from scratch

# Services not starting
docker-compose logs                       # Check error messages

# Docker out of disk space
docker system prune -a                    # Clean up images
```

### Database Connection Errors
```bash
# Check if Postgres is healthy
docker-compose ps | grep postgres

# Restart Postgres
docker-compose restart postgres

# Clear database
docker-compose down -v                    # Delete volumes!
docker-compose up -d
```

### Module Not Found (Python)
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Or in Docker
docker-compose up --build backend
```

### pnpm Not Found
```bash
# Install globally
npm install -g pnpm

# Or use via npm
npx pnpm@latest install
```

---

## ✅ Verify Everything Works

```bash
# 1. Start services
docker-compose up --build -d

# 2. Wait for health checks
sleep 10
docker-compose ps

# 3. Test API
curl http://localhost:8000/health

# 4. Test frontend
curl http://localhost:3000

# 5. View logs
docker-compose logs

# 6. Run tests
docker-compose exec backend pytest tests/ -v --tb=short

# 7. Clean up
docker-compose down
```

---

## 📞 Getting Help

1. **Check logs**: `docker-compose logs`
2. **Read BUILD_GUIDE.md** for detailed troubleshooting
3. **Check GitHub Actions** for CI/CD failures: https://github.com/.../actions
4. **Review code**: See `backend/models.py` for data schemas

---

## 🎯 Key Commands Summary

| Task | Command |
|------|---------|
| Start all | `docker-compose up --build -d` |
| Stop all | `docker-compose down` |
| View status | `docker-compose ps` |
| View logs | `docker-compose logs -f` |
| Run tests | `docker-compose exec backend pytest tests/ -v` |
| Linting | `docker-compose exec backend ruff check .` |
| Format code | `docker-compose exec backend black .` |
| DB migrations | `docker-compose exec backend alembic upgrade head` |
| Backend shell | `docker-compose exec backend bash` |
| Frontend shell | `docker-compose exec frontend sh` |

---

**For more details, see `BUILD_GUIDE.md` 📚**
