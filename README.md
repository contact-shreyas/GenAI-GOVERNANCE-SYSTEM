# GenAI Governance Layer for Higher Education

**Executable & Verifiable Governance for Generative AI in Higher Education: A Policy-as-Code Framework with Transparent Ledger and Verified Copilot**

## Overview

This is a production-ready, research-grade system that makes AI governance in higher education **executable, trustworthy, and transparent**. It combines:

1. **Policy-as-Code**: Faculty author machine-executable policies via templates; system detects conflicts automatically
2. **Verified RAG Co-Pilot**: Answers policy questions with citation-level correctness and low hallucination rates
3. **Privacy-Preserving Transparency**: Logs student AI use (metadata only) and shows aggregated, non-PII disclosure to students

## Quick Start

### Docker: how to run + common pitfalls

1) Prereqs: Docker Desktop running (daemon healthy) and ports 8000, 3000, 15432, 16379 free.
2) Build + start: `make build` then `make up` (uses docker compose).
3) Migrate DB: `make backend-migrate` (runs Alembic inside the container).
4) Logs: `make logs` or `docker compose logs -f backend frontend postgres`.
5) Stop: `make down`.

Pitfalls / fixes:
- Docker daemon not running → start Docker Desktop; `docker info` must show a Server section.
- Stale volumes or bad migration → `make backend-reset` (drops volumes, re-applies Alembic).
- Env missing → backend entrypoint fails fast via `scripts/sanity_check.py` (requires DATABASE_URL, SECRET_KEY, BACKEND_HOST, BACKEND_PORT).
- DB not ready yet → entrypoint waits up to 30s; healthchecks gate startup; compose uses Postgres on host port 15432 to avoid local conflicts.


### Option 1: Docker Compose (Recommended)

```bash
# Clone and navigate
git clone <repo-url>
cd "GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

# Start all services (backend, frontend, Postgres, Redis)
docker-compose up --build -d

# Initialize database
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m scripts.load_sample_policies

# Access
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down
```

### Option 2: Local Development

**Backend (Python 3.11+)**:
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```

**Frontend (Node 20+, pnpm)**:
```bash
cd frontend

# Install pnpm (if not already installed)
npm install -g pnpm

# Install dependencies
pnpm install

# Start dev server
pnpm run dev  # http://localhost:3000
```

## Key Features

### 1. Policy Authorship & Compilation
- **Template-based form**: Dropdowns, checkboxes, clear guidance
- **Conflict detection**: Automatically identifies overlapping, contradictory, or version-conflicting policies
- **Schema validation**: Ensures policies meet JSON schema before deployment
- **Version control**: All policies immutable once published; new versions are new documents

### 2. Runtime Enforcement
- **Decision endpoint** (`POST /api/governance/decide`): 
  - Takes action context (course, role, action, assessment type, phase)
  - Returns: decision (ALLOW/DENY/REQUIRE_JUSTIFICATION) + obligations + reasoning trace
  - Stateless, deterministic, fully traceable

- **Explain endpoint** (`POST /api/governance/explain`):
  - Human-readable explanation of why an action is allowed/denied
  - For student UI: quick feedback before submission

### 3. Transparency Ledger
- **Metadata-only logging**: action type, timestamp, policy version—never content, never PII
- **Pseudonymization**: Student identifiers rotated every 30 days
- **Student-facing dashboard**: "You used AI in assessments (2 events logged under v2.1 policy) [link to policy]"
- **Instructor analytics**: Aggregated counts, no student identities
- **Privacy controls**: Optional opt-out logging; 90-day retention by default

### 4. Verified RAG Co-Pilot
- **Retrieval**: Vector embedding of policy documents
- **Generation**: LLM answers policy questions
- **Verification pipeline**:
  - Citation correctness: Does quoted text exist in policy? (>95% accuracy target)
  - Entailment scoring: Does answer logically follow from policy? (NLI model)
  - Consistency checking: Does answer contradict other policies?
  - Uncertainty flagging: Low confidence → "Ask your admin"
- **Output**: `{answer, citations, verification_score, confidence}`

## Architecture

```
Faculty UI (Next.js) 
    ↓ (policy form)
Policy Compiler (Python)
    ↓ (compiled JSON + conflicts)
Storage (Postgres)
    ↓ (fetch active policy)
Runtime Enforcement Middleware (FastAPI)
    ├─ Decision endpoint (ALLOW/DENY/REQUIRE_JUSTIFICATION)
    ├─ Explain endpoint (human-readable)
    └─ Log to Transparency Ledger (metadata only)
    
Separate: Verified RAG Co-Pilot (Python service)
    ├─ Vector retrieval (policy docs)
    ├─ LLM generation (answer)
    └─ Verification (citation, entailment, consistency)
    
Student-Facing: Transparency Dashboard (Next.js)
    ├─ "My AI-use logs" (aggregated, non-PII)
    ├─ Policy search + Q&A copilot
    └─ Privacy settings (opt-out)
```

## Project Structure

```
genai-governance/
├── backend/
│   ├── policy_compiler/          # Form→JSON compilation, conflict detection
│   ├── governance_middleware/    # Runtime decision engine, API routes
│   ├── transparency_ledger/      # Metadata logging, aggregation, student views
│   ├── rag_copilot/             # Retrieval, generation, verification
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Environment configuration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── policies/             # Policy authoring, detail view
│   │   ├── copilot/              # Q&A interface
│   │   ├── transparency/         # Student logs dashboard
│   │   └── admin/                # Instructor analytics
│   ├── components/               # Reusable UI components
│   ├── lib/                      # Utilities, API client, types
│   ├── package.json
│   └── tsconfig.json
├── datasets/
│   ├── policies_corpus/          # 40-60 curated public university policies
│   ├── benchmark_qa.json         # 80-100 expert-annotated Q&A
│   └── benchmark_scenarios.json  # 40-50 enforcement test cases
├── experiments/
│   ├── usability_study/          # Faculty study (N=12)
│   ├── rag_benchmark.py          # Offline RAG evaluation
│   ├── scenario_test.py          # Enforcement accuracy testing
│   └── results/                  # Output: tables, plots, reports
├── docs/
│   ├── ARCHITECTURE.md           # System design details
│   ├── POLICY_SCHEMA.md          # JSON schema documentation
│   ├── API.md                    # Endpoint specs with examples
│   ├── EVALUATION.md             # Metrics, experimental protocols
│   └── REPRODUCIBILITY.md        # Step-by-step reproduction
├── migrations/                   # Postgres schema (Alembic)
├── tests/                        # Integration tests
├── docker-compose.yml
├── .env.local.example
└── LICENSE
```

## Evaluation & Research

### Datasets (Public Release)
- **Policy Corpus**: 40–60 policies from top US universities (MIT, Stanford, UC Berkeley, etc.)
  - Cleaned, schemaified, with attribution
  - Retrieval URLs documented
  
- **Q&A Benchmark**: 80–100 policy questions with expert gold answers
  - Expert-annotated (2 raters, Cohen's kappa >0.70)
  - Includes citing clauses for each answer
  - Train/test split for evaluation
  
- **Scenario Test Suite**: 40–50 enforcement scenarios
  - Covers: allowed, denied, override, conflict, ambiguous cases
  - Gold decisions for accuracy testing

### Key Metrics & Targets

| Metric | Target | Baseline | This Work |
|--------|--------|----------|-----------|
| Enforcement Accuracy | >90% | Manual: 70–80% | TBD |
| Conflict Detection F1 | >0.85 | None (manual) | TBD |
| Citation Correctness | >95% | Naive RAG: ~75% | TBD |
| Answer Correctness | >90% | Manual: 95%*, Naive RAG: 65% | TBD |
| Hallucination Rate | <5% | Naive RAG: ~20% | TBD |
| Authoring Time Reduction | >50% | Freeform baseline | TBD |
| Student Trust (SUS Score) | >75 (Δ+15) | Control: ~60 | TBD |

### Experimental Design
1. **Faculty Usability Study** (N=12, within-subject): Policy authoring time, errors, SUS score
2. **RAG Benchmark Evaluation** (offline): Citation correctness, hallucination rate, verification calibration
3. **Student Transparency Study** (N=50, RCT): Trust, fairness, privacy comfort with transparency logs

## API Endpoints (Summary)

### Governance Middleware
```
POST /api/governance/decide
  Input: {course_id, actor_role, action, assessment_type, assessment_phase, actor_id_pseudonym}
  Output: {decision, obligations, trace, policy_id, applied_rules}

POST /api/governance/explain
  Input: {course_id, action, assessment_type}
  Output: {action, allowed, explanation, disclosure_required, ...}
```

### Policy Management
```
POST /api/policies/compile
  Input: {course_id, policy_title, allowed_actions, prohibited_actions, ...}
  Output: {success, policy, errors, conflicts}

GET /api/policies/{policy_id}
GET /api/policies?course_id=CS101
```

### Transparency Ledger
```
GET /api/transparency/my-logs/{actor_id_pseudonym}?course_id=CS101
  Output: {summary, aggregates, disclosure_instructions, privacy_commitment}

GET /api/transparency/course-analytics/{course_id}
  Output: {course_id, unique_students, events_by_action, policy_active}
```

### RAG Co-Pilot
```
POST /api/copilot/ask
  Input: {question, course_id}
  Output: {direct_answer, explanation, citations, verification, confidence, requires_human_review}
```

See [docs/API.md](docs/API.md) for complete specifications.

## Testing

```bash
# Backend unit tests
cd backend
pytest tests/ -v

# Frontend component tests
cd frontend
npm run test

# Integration tests (requires services running)
cd tests
pytest test_e2e_*.py -v

# RAG benchmark (offline evaluation)
python experiments/rag_benchmark.py

# Scenario enforcement testing
python experiments/scenario_test.py
```

## Ethics & Privacy

- **No student PII**: Logging uses salted hash pseudonyms, not student IDs
- **Content-free logging**: Only action type, timestamp, policy version—never assessment content
- **Student transparency**: Students see their own aggregated logs
- **Opt-out capability**: Students can disable logging (policy still enforced, just not logged)
- **Data retention**: 90 days by default; configurable per institution
- **Access controls**: Only institution admins can view aggregated analytics
- **Bias audit**: Synthetic demographic-neutral test cases; disparate impact analysis in appendix

See [docs/ETHICS.md](docs/ETHICS.md) for full privacy, fairness, and responsible AI commitments.

## Reproducibility

This project is designed for **maximum reproducibility**:

✅ Code: Open-source (MIT/Apache 2.0), all dependencies free/open  
✅ Datasets: Public policy corpus + expert-annotated benchmarks  
✅ Tests: Complete unit, integration, and property-based test suite  
✅ CI/CD: GitHub Actions for continuous testing  
✅ Documentation: Full API specs, architectural diagrams, methodology  
✅ Results: Evaluation scripts, statistical analysis code, raw data (de-identified)  

**Time to reproduce: 4–8 hours (setup) | 1–2 hours (key results with pre-cached models)**

See [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) for step-by-step instructions.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Citation

If you use this work, please cite:

```bibtex
@article{genai_governance_2024,
  title={Executable \& Verifiable Governance for Generative AI in Higher Education: 
          A Policy-as-Code Framework with Transparent Ledger and Verified Copilot},
  author={[Authors]},
  year={2024},
  note={Open-source software and datasets available at: [github-url]}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Support & Contact

- **Issues & feature requests**: GitHub Issues
- **Research questions**: [ai-governance@institution.edu]
- **Documentation**: [docs/](docs/)

## Acknowledgments

- EDUCAUSE, HEA Ireland for policy landscape research
- Cornell, MIT, Stanford, and other institutions for policy contributions
- Participants in usability and transparency studies

---

**Made with ❤️ for trustworthy AI governance in education**
