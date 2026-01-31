# Deployment & Completion Guide

## Project Status: 95% COMPLETE (Week 4 Ready)

### What's Built

#### Week 1-2: Core Backend ✅
- [x] Database schema (Postgres + SQLAlchemy ORM)
- [x] Policy compiler (form → JSON → DB)
- [x] Enforcement engine (auto-check + decision)
- [x] Transparency ledger (privacy-safe logging)
- [x] API endpoints (5 routes)

#### Week 3: Frontend & Copilot ✅
- [x] Faculty policy form (Create Policy page)
- [x] Student copilot Q&A (Ask Copilot page)
- [x] Student transparency dashboard (My Logs page)
- [x] Admin analytics (Analytics page)
- [x] Landing page
- [x] Basic copilot (keyword matching MVP)

#### Week 4: Auth & Testing ✅
- [x] JWT authentication module
- [x] Role-based access control
- [x] Integration test suite
- [x] Deployment guide (this file)

---

## 🚀 How to Run (End-to-End)

### Option 1: Full Docker Stack (Recommended)
```bash
cd "d:\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"
.\start.bat
```

Then:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development (Faster)

#### Backend
```bash
cd backend

# Install deps
pip install -r requirements-minimal.txt

# Run migrations (first time)
alembic upgrade head

# Start server
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend

# Install deps
pnpm install

# Start dev server
pnpm run dev
```

Then:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 📝 User Flows (Test These)

### Flow 1: Faculty Creates Policy (2 mins)
1. Go to http://localhost:3000
2. Click "Create Policy"
3. Fill form:
   - Course: CS101
   - Allowed: brainstorm (assignment)
   - Prohibited: full_solution (exam)
4. Click "Create Policy"
5. **Expected:** ✅ Policy created

### Flow 2: Student Asks Copilot (1 min)
1. Go to http://localhost:3000
2. Click "Ask Copilot"
3. Type: "Can I use ChatGPT for brainstorming?"
4. Click "Ask Copilot"
5. **Expected:** ✅ Answer with citations + confidence

### Flow 3: Student Checks Logs (1 min)
1. Go to http://localhost:3000
2. Click "My Logs"
3. Enter pseudonym: student_123
4. Click "View My Logs"
5. **Expected:** ✅ Aggregated AI-use events

### Flow 4: Admin Sees Analytics (1 min)
1. Go to http://localhost:3000
2. Click "Analytics"
3. Enter course: CS101
4. Click "View Analytics"
5. **Expected:** ✅ Compliance stats + breakdown

---

## 🧪 API Testing (Curl Commands)

### 1. Create Policy
```bash
curl -X POST http://localhost:8000/api/policies/compile \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": "CS101",
    "title": "AI Policy",
    "allowed_actions": [{"action": "brainstorm", "assessment_type": "assignment"}],
    "prohibited_actions": [],
    "disclosure_config": {"requires_disclosure": true},
    "metadata": {"author": "prof", "institution": "MIT"}
  }'
```
**Expected:** `{"success": true, "policy_id": "CS101_genai_v1.0"}`

### 2. Check Enforcement
```bash
curl -X POST http://localhost:8000/api/governance/decide \
  -H "Content-Type: application/json" \
  -d '{
    "policies": [{...policy from step 1...}],
    "context": {
      "course_id": "CS101",
      "actor_id_pseudonym": "student_123",
      "action": "brainstorm",
      "assessment_type": "assignment",
      "assessment_phase": "drafting"
    }
  }'
```
**Expected:** `{"decision": "ALLOW", "obligations": [...], "trace": [...]}`

### 3. Get Student Logs
```bash
curl http://localhost:8000/api/transparency/my-logs/student_123?course_id=CS101
```
**Expected:** `{"summary": "You have X events logged", "aggregates": [...]}`

### 4. Get Admin Analytics
```bash
curl http://localhost:8000/api/transparency/course-analytics/CS101
```
**Expected:** `{"course_id": "CS101", "unique_students": 120, ...}`

---

## 🔐 Adding Authentication (Optional—Week 4)

### 1. Generate a Token
```bash
python -c "
from backend.auth import create_access_token
token = create_access_token(subject='prof_123', role='faculty', course_id='CS101')
print(f'Bearer {token}')
"
```

### 2. Use Token in Request
```bash
curl -X POST http://localhost:8000/api/policies/compile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

---

## 📊 Database Schema (Verify It Exists)

### Check Tables
```bash
# If Postgres running
docker exec postgres psql -U genai_user -d genai_governance -c "\dt"

# Should show:
# - ai_use_logs (student logs)
# - policies (policy documents)
```

### Sample Query
```sql
SELECT COUNT(*) FROM ai_use_logs;  -- Should increase as decisions logged
SELECT COUNT(*) FROM policies;      -- Should see compiled policies
```

---

## 🎯 Success Criteria (All Must Pass)

| Criterion | How to Test | Expected |
|-----------|------------|----------|
| Policy Compile | POST /api/policies/compile | 200 OK, policy saved |
| Enforcement | POST /api/governance/decide | ALLOW/DENY + logged |
| Student Logs | GET /api/transparency/my-logs | Aggregated events |
| Admin Analytics | GET /api/transparency/course-analytics | Compliance stats |
| Frontend Create | Policy form submit | ✅ Policy created |
| Frontend Copilot | Ask question | Answer + citations |
| Frontend Logs | View my logs | Events listed |
| Frontend Admin | View analytics | Stats rendered |
| Health Check | GET /health | 200 OK, healthy |

---

## 📦 Deployment to Production

### Docker Compose (Recommended)
1. Set `ENVIRONMENT=production` in `.env`
2. Set `SECRET_KEY` to 32+ char random string
3. Run: `docker compose -f docker-compose.prod.yml up -d`

### Manual VM Deployment
1. Install Python 3.11, Node 20, Postgres 15, Redis 7
2. Clone repo
3. Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   gunicorn main:app --workers 4 --bind 0.0.0.0:8000
   ```
4. Frontend:
   ```bash
   cd frontend
   pnpm install --prod
   pnpm run build
   pnpm start
   ```

### Environment Variables
```env
# .env.production
DATABASE_URL=postgresql://user:pass@postgres-host:5432/genai_governance_db
REDIS_URL=redis://redis-host:6379/0
SECRET_KEY=your-secret-key-32-chars-min
ENVIRONMENT=production
OPENAI_API_KEY=sk-...
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Docker build stuck" | Skip Docker; run locally (pip + pnpm) |
| "Port already in use" | Change docker-compose.yml ports |
| "DB connection failed" | Check `DATABASE_URL` env var |
| "Migrations failed" | Run manually: `docker compose exec backend alembic upgrade head` |
| "Policy compile 422" | Check payload matches `PolicyFormInput` schema |
| "API returns 401" | Add `Authorization: Bearer TOKEN` header |
| "Frontend shows no API data" | Check `NEXT_PUBLIC_API_BASE_URL` env var |

---

## 📈 Next Steps (Beyond MVP)

1. **Advanced Copilot** (Week 5):
   - Vector embeddings (policy search)
   - LLM generation (GPT-4)
   - Citation verification (NLI)

2. **Full Auth** (Week 6):
   - OAuth2 (college SSO)
   - Multi-institution support
   - Audit logs

3. **Mobile App** (Week 7):
   - React Native
   - Quick-check interface
   - Push notifications

4. **Analytics Dashboard** (Week 8):
   - Charts (compliance trends)
   - Export (CSV/PDF)
   - Custom reports

---

## 📞 Support

- **Issues:** GitHub Issues
- **Docs:** docs/ARCHITECTURE.md
- **API:** http://localhost:8000/docs (Swagger)
- **Demo:** See demo video in experiments/

---

## ✅ Project Complete!

**Weeks 1-4 DONE. Ready for deployment or further enhancements.**

Run: `start.bat` and visit http://localhost:3000 to see it live!
