# GenAI Governance System Architecture

## Overview Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      POLICY AUTHORSHIP LAYER                     │
├──────────────────────────────────────────────────────────────────┤
│  Faculty UI (Next.js)                                             │
│  ├─ Policy Template Form (dropdowns, checkboxes)                  │
│  ├─ Free-form JSON Editor                                         │
│  └─ Conflict Detection Preview                                    │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ (POST /api/policies/compile)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                    POLICY COMPILATION SERVICE                     │
├──────────────────────────────────────────────────────────────────┤
│  Python (Pydantic models + rule engine)                           │
│  ├─ Parse template form → JSON schema                             │
│  ├─ Validate & canonicalize (normalize roles, actions)            │
│  ├─ Conflict detection:                                           │
│  │  ├─ Scope overlap (course A ⊂ course B)                        │
│  │  ├─ Rule contradictions (allow X, deny X)                      │
│  │  └─ Temporal conflicts (v1 vs v2)                              │
│  └─ Version & store in Postgres                                   │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ (Policy JSON + metadata)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│               RUNTIME ENFORCEMENT MIDDLEWARE                      │
├──────────────────────────────────────────────────────────────────┤
│  Next.js API Routes / Python FastAPI                              │
│  ├─ Endpoint: POST /api/governance/decide                         │
│  │  ├─ Input: {context: action, actor, resource, phase}           │
│  │  ├─ Lookup: Active policy for course                           │
│  │  ├─ Evaluate: Policy rules → ALLOW/DENY/REQUIRE_JUSTIFICATION  │
│  │  ├─ Generate: Decision trace (matched rules, obligations)      │
│  │  └─ Log: Metadata to transparency ledger                       │
│  └─ Endpoint: POST /api/governance/explain                        │
│     └─ Return: decision trace + reasoning (for UI)                │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ (decisions + logs)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│            TRANSPARENCY LEDGER (Postgres + Aggregation)           │
├──────────────────────────────────────────────────────────────────┤
│  ├─ Write: Log entries (pseudonym, action, policy_id, timestamp)  │
│  ├─ Aggregate: by student, by course, by policy_version           │
│  ├─ Student View: "You used AI in assessment (1x logged v2.1)"    │
│  └─ Instructor Analytics: "GenAI use: 45 students, 3 assessments"  │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ (/api/transparency/logs)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│         VERIFIED RAG COPILOT (Policy Q&A with Verification)      │
├──────────────────────────────────────────────────────────────────┤
│  Python service (LangChain / LlamaIndex + custom verification)    │
│  ├─ Retrieval: Vector embedding of policy documents               │
│  ├─ Generation: LLM Q&A over retrieved context                    │
│  ├─ Verification:                                                 │
│  │  ├─ Citation check: each claim → extract quoted clause         │
│  │  ├─ Entailment: claim ⊨ context? (NLI model)                   │
│  │  ├─ Consistency: does answer contradict other docs?            │
│  │  └─ Uncertainty: flag weak evidence (<0.7 confidence)          │
│  ├─ Output: {answer, citations, verification_score, confidence}   │
│  └─ Fallback: "I'm uncertain about this policy. Ask your admin."  │
└─────────────────────────────┬──────────────────────────────────────┘
                              │ (/api/copilot/ask)
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│          ADMIN & STUDENT DASHBOARDS (Next.js)                     │
├──────────────────────────────────────────────────────────────────┤
│  Admin:                         Student:                           │
│  ├─ Policy versions + audit log ├─ My AI-use logs (aggregated)     │
│  ├─ Enforcement analytics       ├─ Transparency legend             │
│  ├─ Conflict reports            ├─ Policy search + QA copilot      │
│  └─ Compliance summary          └─ Privacy settings (opt-out)       │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow Example: Student Uses GenAI

```
1. Faculty defines policy (template or free-form JSON)
   ↓
2. System compiles policy → PolicyJSON
   ├─ Validates schema
   ├─ Detects conflicts
   └─ Stores versioned copy
   ↓
3. At assessment submission, system enforces policy
   ├─ Receive: {action, actor_role, assessment_type, phase}
   ├─ Lookup: Active policy for course
   ├─ Evaluate: f_policy(policy, context) → decision
   └─ Generate: Trace + obligations
   ↓
4. Log to transparency ledger (metadata only)
   ├─ actor_id_pseudonym, action, policy_version, timestamp
   └─ NO content, NO PII, NO learning outcomes
   ↓
5. Student sees aggregated log
   ├─ "You used AI in assessment (1x logged)"
   ├─ "Under v2.1 policy"
   └─ [Link to policy details]
   ↓
6. Instructor sees anonymized analytics
   ├─ "45 students, 3 assessments with GenAI use"
   ├─ No student identities
   └─ Aggregates only
```

## Module Descriptions

### 1. Policy Compiler (`backend/policy_compiler/`)

**Purpose**: Convert faculty form input → machine-executable policy JSON

**Key Components**:
- `models.py`: Pydantic schemas (PolicyJSON, AllowedAction, ProhibitedAction, etc.)
- `compiler.py`: Form input → JSON compilation + validation
- `conflict_detector.py`: Scope overlap, action contradictions, version conflicts
- `tests/`: Unit tests for each component

**Key Functions**:
- `compile_policy_from_form(form) → CompileResult`
- `detect_conflicts(new_policy, existing_policies) → ConflictReport`
- `validate_policy_schema(policy) → List[ValidationError]`

**Data Structures**:
- Input: `PolicyFormInput` (faculty form)
- Output: `PolicyJSON` (machine-executable policy) + `ConflictReport`

**Constraints**:
- All policies immutable once published
- Version ancestry tracked (previous_version_id)
- Conflict detection must be <1 second for UX

---

### 2. Governance Middleware (`backend/governance_middleware/`)

**Purpose**: Runtime policy enforcement at assessment submission

**Key Components**:
- `decision_engine.py`: Core f_policy(P, C) → (decision, obligations, trace)
- `api.py`: FastAPI routes (decide, explain, etc.)
- `tests/`: Unit + integration tests

**Key Functions**:
- `evaluate_policy(policy, context) → (DecisionEnum, List[Obligation], Dict[trace])`
- `make_decision(context) → GovernanceDecision`
- `check_override_rules(context) → bool`
- `resolve_conflicts(allowed_rule, prohibited_rule) → DecisionEnum`

**Data Structures**:
- Input: `GovernanceContext` {course_id, actor_role, action, assessment_type, phase}
- Output: `GovernanceDecision` {decision, obligations, trace, policy_id}

**Constraints**:
- Stateless (no side effects)
- Deterministic (same input → same output)
- <100ms latency target
- Full trace for auditing

---

### 3. Transparency Ledger (`backend/transparency_ledger/`)

**Purpose**: Privacy-preserving logging and student-facing analytics

**Key Components**:
- `models.py`: Postgres schema (ai_use_logs, ai_use_aggregates, student_transparency_view)
- `db.py`: Database operations + nightly aggregation
- `api.py`: Ledger endpoints (my-logs, course-analytics, etc.)
- `tests/`: Tests for privacy guarantees

**Key Functions**:
- `log_to_transparency_ledger(actor_id_pseudonym, action, ...) → None`
- `get_student_transparency_logs(actor_id_pseudonym) → StudentTransparencyView`
- `get_course_analytics(course_id) → CourseAnalytics`
- `nightly_aggregate_logs() → None` (scheduled job)

**Data Structures**:
- Log: `AIUseLog` {pseudonym, action, policy_id, decision, timestamp}
- Student view: `StudentTransparencyView` {summary, aggregates, instructions}
- Analytics: `CourseAnalytics` {unique_students, events_by_action}

**Constraints**:
- NO student_id (only pseudonym hash)
- NO content (no policy text, no interaction)
- NO learning outcome inference
- 90-day retention default
- Pseudonym rotation every 30 days

---

### 4. Verified RAG Co-Pilot (`backend/rag_copilot/`)

**Purpose**: Policy Q&A with verified citations and low hallucination

**Key Components**:
- `retrieval.py`: Vector embedding + semantic search
- `generation.py`: LLM answer generation
- `verification.py`: Citation + entailment + consistency checks
- `api.py`: Co-pilot endpoint
- `tests/`: Benchmark evaluation

**Key Functions**:
- `retrieve_policy_documents(question, course_id) → List[PolicyDoc]`
- `generate_answer(question, context) → str`
- `verify_citations(answer, context) → float` (citation_correctness)
- `score_entailment(answer, context) → float` (NLI)
- `check_consistency(answer, other_policies) → float`
- `ask_policy_question(question, course_id) → CopilotAnswer`

**Data Structures**:
- Input: Question (string), course_id (optional)
- Output: `CopilotAnswer` {answer, citations, verification, confidence}
- Citation: `Citation` {quoted_text, source_policy_id, section, confidence}

**Constraints**:
- Citation correctness >95% target
- Hallucination rate <5%
- Entailment score calibrated
- Low confidence (<0.7) → flag for human review

---

### 5. Frontend (`frontend/`)

**Purpose**: Faculty policy authoring, student transparency, admin analytics

**Structure**:
```
app/
├── policies/         # Policy list, detail, creation
├── copilot/          # Q&A chat interface
├── transparency/     # Student logs dashboard
├── admin/            # Instructor analytics
└── api/              # API proxy routes

components/
├── PolicyForm.tsx    # Template form for faculty
├── ConflictReview.tsx
├── CopilotChat.tsx
├── TransparencyLog.tsx
└── ...

lib/
├── api.ts            # Client-side API calls
├── types.ts          # TypeScript interfaces
└── validators.ts     # Zod schemas for validation
```

**Key Pages**:
- `/policies/create`: Faculty policy authoring (template form)
- `/policies/{id}`: Policy detail view + history
- `/copilot`: Q&A interface (student/faculty use)
- `/transparency`: Student AI-use logs + disclosure
- `/admin/analytics`: Instructor analytics + enforcement reports

---

## Database Schema (Postgres)

### Core Tables

#### `policies`
```sql
CREATE TABLE policies (
    policy_id VARCHAR(100) PRIMARY KEY,
    institution_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,  -- Full PolicyJSON
    version VARCHAR(10) NOT NULL,
    previous_version_id VARCHAR(100) REFERENCES policies(policy_id),
    created_at TIMESTAMP DEFAULT NOW(),
    effective_from TIMESTAMP NOT NULL,
    deprecated_at TIMESTAMP,
    INDEX idx_course_active (course_id, deprecated_at)
);
```

#### `ai_use_logs` (Transparency Ledger)
```sql
CREATE TABLE ai_use_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id VARCHAR(50) NOT NULL,
    actor_id_pseudonym VARCHAR(64) NOT NULL,  -- salted hash
    action VARCHAR(100) NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    policy_id VARCHAR(100) NOT NULL REFERENCES policies(policy_id),
    decision VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    retention_until TIMESTAMP,
    INDEX idx_student_time (actor_id_pseudonym, timestamp)
);
```

---

## Request-Response Flow

### Example: Policy Decision
```
Request:
  POST /api/governance/decide
  {
    "course_id": "CS101",
    "actor_role": "student",
    "action": "use_genai_brainstorm",
    "assessment_type": "problem_set",
    "assessment_phase": "drafting",
    "actor_id_pseudonym": "psud_abc123"
  }

Response:
  {
    "decision": "ALLOW",
    "obligations": [
      {
        "type": "disclosure_required",
        "format": "inline_comment",
        "template": "I used [Tool] to brainstorm ideas for this problem."
      }
    ],
    "trace": {
      "steps": ["Matched allowed rule: use_genai_brainstorm"],
      "rules_matched": ["use_genai_brainstorm"],
      "conflicts": []
    },
    "policy_id": "course_cs101_genai_v2.1",
    "applied_rules": ["use_genai_brainstorm"]
  }
```

---

## Testing Strategy

See [docs/TESTING.md](TESTING.md) for complete test coverage, including:
- Unit tests for policy compiler, decision engine, verification pipeline
- Property-based tests for rule consistency
- Integration tests for end-to-end flows
- RAG benchmark evaluation
- Scenario-based enforcement tests

---

For more details, see:
- [API.md](API.md): Complete endpoint specifications
- [POLICY_SCHEMA.md](POLICY_SCHEMA.md): Full JSON schema documentation
- [EVALUATION.md](EVALUATION.md): Evaluation methodology and metrics
