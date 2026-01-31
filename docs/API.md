# API Specification

## Base URL

- Development: `http://localhost:8000`
- Production: `https://api.institution.edu`

## Authentication

All endpoints require Bearer token authentication (JWT):

```
Authorization: Bearer <token>
```

---

## Endpoints

### 1. Health & Status

#### `GET /health`

Health check endpoint.

**Response** (200):
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

---

### 2. Policy Management

#### `POST /api/policies/compile`

Compile faculty form input to machine-executable policy JSON. Includes conflict detection.

**Request**:
```json
{
  "course_id": "CS101",
  "policy_title": "CS101 Generative AI Policy v1.0",
  "description": "Governs student use of GenAI in CS101.",
  "allowed_actions": ["use_genai_brainstorm", "use_genai_code_review"],
  "prohibited_actions": ["submit_genai_as_own"],
  "disclosure_required": true,
  "logging_level": "log_action_only",
  "assessment_types": ["problem_set", "project"],
  "assessment_phases": ["planning", "drafting", "submission"]
}
```

**Response** (200):
```json
{
  "success": true,
  "policy": {
    "policy_id": "course_cs101_genai_v1.0",
    "course_id": "CS101",
    "version": "1.0",
    "metadata": { ... },
    "scope": { ... },
    "actions": { ... }
  },
  "errors": [],
  "warnings": [],
  "conflicts": []
}
```

**Response** (400 - validation error):
```json
{
  "success": false,
  "policy": null,
  "errors": ["Course ID is required", "At least one allowed action must be specified"],
  "warnings": [],
  "conflicts": []
}
```

---

#### `GET /api/policies/{policy_id}`

Fetch a specific policy version.

**Response** (200):
```json
{
  "policy_id": "course_cs101_genai_v2.1",
  "course_id": "CS101",
  "version": "2.1",
  "created_at": "2024-01-15T10:00:00Z",
  "effective_from": "2024-01-20T00:00:00Z",
  "deprecated_at": null,
  ...
}
```

---

#### `GET /api/policies?course_id={course_id}&active_only={true|false}`

List policies for a course.

**Query Parameters**:
- `course_id` (required): Course identifier
- `active_only` (optional, default=true): Only return non-deprecated policies

**Response** (200):
```json
{
  "course_id": "CS101",
  "policies": [
    {
      "policy_id": "course_cs101_genai_v2.1",
      "version": "2.1",
      "created_at": "2024-01-15T10:00:00Z",
      "effective_from": "2024-01-20T00:00:00Z",
      "deprecated_at": null
    }
  ],
  "total": 1
}
```

---

### 3. Governance & Enforcement

#### `POST /api/governance/decide`

Make a policy decision based on context.

**Request**:
```json
{
  "course_id": "CS101",
  "actor_role": "student",
  "action": "use_genai_brainstorm",
  "assessment_type": "problem_set",
  "assessment_phase": "drafting",
  "actor_id_pseudonym": "psud_abc123xyz"
}
```

**Response** (200):
```json
{
  "decision": "ALLOW",
  "obligations": [
    {
      "type": "disclosure_required",
      "format": "inline_comment",
      "template": "I used [Tool] to brainstorm ideas for this problem.",
      "requirement_id": "disclose_brainstorm"
    }
  ],
  "trace": {
    "steps": [
      "Checked override rules: none matched",
      "Matched allowed rule: use_genai_brainstorm",
      "Assessment type matches: problem_set ✓",
      "Assessment phase matches: drafting ✓",
      "Role matches: student ✓"
    ],
    "rules_matched": ["use_genai_brainstorm"],
    "conflicts": [],
    "decision": "ALLOW"
  },
  "policy_id": "course_cs101_genai_v2.1",
  "applied_rules": ["use_genai_brainstorm"]
}
```

**Decision Values**:
- `"ALLOW"`: Action is permitted
- `"DENY"`: Action is forbidden
- `"REQUIRE_JUSTIFICATION"`: Action is allowed but requires student justification

---

#### `POST /api/governance/explain`

Get human-readable explanation of a policy rule (non-enforcing).

**Request**:
```json
{
  "course_id": "CS101",
  "action": "use_genai_brainstorm",
  "assessment_type": "problem_set"
}
```

**Response** (200):
```json
{
  "action": "use_genai_brainstorm",
  "allowed": true,
  "explanation": "You can use GenAI tools (ChatGPT, Claude, etc.) to brainstorm ideas, outline, or plan your problem sets. This applies during the planning and drafting phases.",
  "disclosure_required": true,
  "disclosure_format": "inline_comment",
  "policy_id": "course_cs101_genai_v2.1",
  "policy_version": "2.1"
}
```

---

### 4. Transparency & Analytics

#### `GET /api/transparency/my-logs/{actor_id_pseudonym}?course_id={course_id}`

Fetch student's aggregated AI-use logs (privacy-preserving).

**Response** (200):
```json
{
  "summary": "You have 3 AI-use events logged (last event: 2024-01-20)",
  "aggregates": [
    {
      "action": "use_genai_brainstorm",
      "assessment_type": "problem_set",
      "count": 2,
      "last_event_timestamp": "2024-01-20T14:30:00Z",
      "policy_id": "course_cs101_genai_v2.1"
    },
    {
      "action": "use_genai_code_review",
      "assessment_type": "problem_set",
      "count": 1,
      "last_event_timestamp": "2024-01-19T09:15:00Z",
      "policy_id": "course_cs101_genai_v2.1"
    }
  ],
  "disclosure_instructions": "This log shows when you used AI tools in your coursework. The institution logs metadata only (action, time, policy version)—not content. You can review the policy at [link].",
  "policy_link_template": "/policies/{policy_id}",
  "privacy_commitment": "We do not store your identity with these logs. Logs are deleted 90 days after creation. You can opt out of logging at any time."
}
```

---

#### `GET /api/transparency/course-analytics/{course_id}`

Fetch aggregated, anonymized AI-use analytics for instructors.

**Requires**: Instructor role for the course

**Response** (200):
```json
{
  "course_id": "CS101",
  "period": "last 7 days",
  "total_unique_students": 42,
  "total_events": 87,
  "by_action": [
    {
      "action": "use_genai_brainstorm",
      "assessment_type": "problem_set",
      "unique_students": 35,
      "total_events": 52,
      "last_event": "2024-01-26T14:30:00Z"
    },
    {
      "action": "use_genai_code_review",
      "assessment_type": "problem_set",
      "unique_students": 18,
      "total_events": 35,
      "last_event": "2024-01-26T13:45:00Z"
    }
  ],
  "policy_active": {
    "policy_id": "course_cs101_genai_v2.1",
    "version": "2.1",
    "effective_from": "2024-01-20T00:00:00Z"
  }
}
```

**Note**: No student identities. Counts only. Aggregated over past 7 days by default.

---

### 5. RAG Co-Pilot

#### `POST /api/copilot/ask`

Ask a policy question and get a verified answer.

**Request**:
```json
{
  "question": "Can I use ChatGPT to brainstorm ideas for my problem set?",
  "course_id": "CS101"
}
```

**Response** (200):
```json
{
  "direct_answer": "Yes, with disclosure",
  "explanation": "According to the CS101 GenAI Policy v2.1, you can use ChatGPT, Claude, and other GenAI tools to brainstorm ideas, outline, and plan your problem sets during the planning and drafting phases. However, you must disclose this use in an inline comment.",
  "citations": [
    {
      "quoted_text": "Use GenAI for ideation, brainstorming, outlining applies_to_assessment_types: [problem_set]",
      "source_policy_id": "course_cs101_genai_v2.1",
      "source_section": "Allowed Actions > use_genai_brainstorm",
      "confidence": 0.95
    }
  ],
  "verification": {
    "citation_correctness": 1.0,
    "entailment": 0.92,
    "consistency": 1.0,
    "overall_score": 0.97
  },
  "confidence": "high",
  "uncertainty_caveats": null,
  "requires_human_review": false,
  "human_contact": "ai-governance@institution.edu"
}
```

**Response** (200 - low confidence):
```json
{
  "direct_answer": "Uncertain",
  "explanation": "I found limited information about this policy in the course materials. Please ask your instructor or contact the AI governance office for clarification.",
  "citations": [],
  "verification": {
    "citation_correctness": 0,
    "entailment": 0.4,
    "consistency": 0.5,
    "overall_score": 0.3
  },
  "confidence": "low",
  "uncertainty_caveats": [
    "No clear policy clause found",
    "Limited context to answer with confidence"
  ],
  "requires_human_review": true,
  "human_contact": "ai-governance@institution.edu"
}
```

**Confidence Levels**:
- `"high"`: Overall verification score ≥ 0.85 (recommended for reliance)
- `"medium"`: 0.70–0.85 (should be double-checked)
- `"low"`: < 0.70 (flag for human review; recommend direct contact)

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "detail": "Missing required field: 'course_id'",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "detail": "Invalid or missing authentication token",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "detail": "You do not have permission to view analytics for this course",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "detail": "Policy 'course_cs101_genai_v2.1' not found",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred. Please contact support.",
  "timestamp": "2024-01-26T10:00:00Z"
}
```

---

## Rate Limiting

- Standard endpoints: 100 requests/minute per user
- Heavy computation (RAG verification): 10 requests/minute per user

Response headers include:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1706256060
```

---

## Pagination

List endpoints support pagination:

```
GET /api/policies?course_id=CS101&limit=20&offset=0
```

**Response**:
```json
{
  "items": [...],
  "total": 45,
  "limit": 20,
  "offset": 0,
  "next_offset": 20
}
```

---

## Testing Endpoints

Use these curl examples to test:

```bash
# Health check
curl http://localhost:8000/health

# Compile a policy
curl -X POST http://localhost:8000/api/policies/compile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "course_id": "CS101",
    "policy_title": "Test Policy",
    "allowed_actions": ["use_genai_brainstorm"],
    "prohibited_actions": []
  }'

# Make a governance decision
curl -X POST http://localhost:8000/api/governance/decide \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "course_id": "CS101",
    "actor_role": "student",
    "action": "use_genai_brainstorm",
    "assessment_type": "problem_set",
    "assessment_phase": "drafting",
    "actor_id_pseudonym": "psud_test123"
  }'

# Ask copilot a question
curl -X POST http://localhost:8000/api/copilot/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "question": "Can I use ChatGPT for my problem set?",
    "course_id": "CS101"
  }'
```

---

For WebSocket endpoints and streaming responses, see [Advanced Usage Guide](ADVANCED.md).
