# Data Transparency & Provenance Guide

**🔒 Privacy Guarantee**: This system uses ONLY synthetic and public data. NO real student PII is ever stored.

---

## 📊 Data Sources by Component

### 1. **Policies Module** 
**Source**: Public university policy documents (no PII)

```
✅ SAFE SOURCES:
- Cornell University GenAI Policy 2025 (Public PDF)
- Stanford University AI in Education Guidelines (Public)
- MIT OpenCourseWare Policy (Public)
- IIT Delhi Academic Integrity Code (Public)

❌ NEVER USED:
- Real student names ❌
- Real student IDs ❌  
- Real course rosters ❌
- Real student submissions ❌
```

**Data In API Response**:
```json
{
  "policy": {...},
  "data_source": {
    "type": "PUBLIC_POLICY",
    "source_name": "Cornell University GenAI Policy 2025",
    "origin": "https://academicaffairs.cornell.edu/...",
    "real_pii_stored": false,
    "retention_days": 999999  // Archive forever
  }
}
```

---

### 2. **Governance Enforcement Module**
**Source**: Synthetic test cases (100% fake data)

```
✅ SYNTHETIC STUDENTS USED FOR TESTING:
- test_student_001 (FAKE)
- test_student_002 (FAKE)
- test_student_003 (FAKE)
- psud_dave_001 (pseudonym, FAKE)
- psud_jane_002 (pseudonym, FAKE)

✅ SYNTHETIC COURSES:
- CS101_2025_spring (FAKE)
- DATA201_2025_fall (FAKE)
- MATH150_2025_spring (FAKE)

❌ NEVER USED:
- Real student names ❌
- Real course enrollments ❌
- Real assignment submissions ❌
- Real student behavior ❌
```

**Data In API Response**:
```json
{
  "decision": "ALLOW",
  "reasoning": "...",
  "student_id": "test_student_001",  // FAKE
  "data_source": {
    "type": "SYNTHETIC_TEST",
    "source_name": "Synthetic Test Scenario #001",
    "real_pii_stored": false,
    "real_content_stored": false,
    "privacy_status": "ZERO_PII",
    "log_storage": "metadata_only",
    "logged_fields": ["action", "decision", "timestamp"],
    "not_logged": ["student_real_name", "student_content"],
    "retention_days": 90
  }
}
```

---

### 3. **Transparency Ledger (Student Logs)**
**Source**: Pseudonymous synthetic interactions

```
✅ WHAT IS LOGGED (metadata only):
- Timestamp: when decision was made
- Action type: what was requested (e.g., "brainstorm")
- Decision: ALLOW/DENY/NEED_CONTEXT
- Policy used: which policy was consulted

❌ WHAT IS NEVER LOGGED:
- Real student name ❌
- Real course content ❌
- AI response text ❌
- Student submission content ❌
```

**Data In API Response**:
```json
{
  "logs": [
    {
      "log_id": "log_001",
      "timestamp": "2025-01-26T10:30:00Z",
      "action": "brainstorm",
      "decision": "ALLOW",
      "student_pseudonym": "psud_001",  // Not real name
      "data_source": {
        "type": "SYNTHETIC_TEST",
        "real_pii_stored": false,
        "real_content_stored": false,
        "logged_fields_only": ["action", "decision", "timestamp"],
        "privacy_summary": "✅ 100% Safe - No real PII, no content"
      }
    }
  ]
}
```

---

### 4. **RAG Copilot Module**
**Source**: Public policies + FAQ database (no PII)

```
✅ KNOWLEDGE BASE SOURCES:
- Public university policies
- FAQ entries created by faculty
- Academic integrity guidelines

❌ NEVER INCLUDED IN KNOWLEDGE BASE:
- Real student submissions ❌
- Real student names ❌
- Real student data ❌
- Confidential course materials ❌
```

**Data In API Response**:
```json
{
  "answer": "Yes, you can use ChatGPT to brainstorm...",
  "confidence": 98,
  "policy_citation": "Cornell GenAI Policy 2025, Section 3.1",
  "data_source": {
    "type": "PUBLIC_POLICY",
    "source_name": "Public University Policies + Faculty FAQs",
    "sources_used": [
      "Cornell University GenAI Policy 2025",
      "Stanford AI Ethics Guidelines"
    ],
    "real_pii_stored": false,
    "real_content_stored": false,
    "privacy_summary": "✅ Safe - Answers cite public sources only"
  }
}
```

---

### 5. **Admin Analytics Module**
**Source**: Aggregated synthetic data (no individual PII)

```
✅ ANALYTICS COMPUTED FROM:
- Synthetic test decision counts
- Policy compliance rates
- FAQ usage patterns
- Course-level aggregations only

❌ NEVER SHOWN IN ANALYTICS:
- Individual student names ❌
- Individual student actions ❌
- Real course data ❌
- Identifying information ❌
```

**Data In API Response**:
```json
{
  "analytics": {
    "total_decisions": 1250,
    "allow_rate": 73.2,
    "deny_rate": 26.8,
    "top_policies": ["CS101_v1.0", "DATA201_v1.0"],
    "data_source": {
      "type": "SYNTHETIC_TEST",
      "aggregation_level": "course_level",
      "no_individual_pii": true,
      "data_period": "2025-01-01 to 2025-01-26",
      "privacy_summary": "✅ 100% Aggregated - No individual data exposed"
    }
  }
}
```

---

## 🔐 Privacy Guarantees

| Guarantee | Status | Where Enforced |
|-----------|--------|-----------------|
| NO Real Student Names | ✅ Enforced | Pseudonyms only (test_001, psud_001) |
| NO Student Content Logging | ✅ Enforced | Metadata-only logging (action+decision+timestamp) |
| NO Real Course Data | ✅ Enforced | Synthetic courses only (CS101_2025_spring) |
| NO PII in Analytics | ✅ Enforced | Aggregation only, course-level |
| Auto-Delete Logs | ✅ Enforced | 90-day retention, then purge |
| Transparent Data Sources | ✅ Enforced | `data_source` field in every API response |
| Student Can See Own Logs | ✅ Enforced | Transparency dashboard shows what's logged |

---

## 📱 How Users See Data Transparency

### Faculty Creating Policy:
```
API Request:
POST /policies/compile
{
  "course": "CS101",
  "allowed_actions": ["brainstorm"],
  "prohibited_actions": ["full_solution_as_own"]
}

API Response:
{
  "policy_id": "CS101_v1.0",
  "status": "compiled",
  "data_source": {
    "type": "PUBLIC_POLICY",
    "source_name": "Policy based on public guidelines",
    "real_pii_stored": false,
    "privacy_summary": "✅ This policy uses NO real student data"
  }
}
```

### Student Asking Copilot:
```
User: "Can I use ChatGPT to brainstorm?"

Copilot Response:
{
  "answer": "Yes, brainstorming is allowed in CS101...",
  "policy_source": "Cornell GenAI Policy 2025",
  "confidence": 98,
  "data_source": {
    "type": "PUBLIC_POLICY",
    "sources_used": ["Cornell Policy (Public PDF)"],
    "real_pii_stored": false,
    "privacy_summary": "✅ Answer based on public sources only"
  }
}
```

### Student Viewing Their Logs:
```
GET /transparency/my-logs
Response:
{
  "logs": [
    {
      "timestamp": "2025-01-26T10:30:00Z",
      "action": "brainstorm",
      "decision": "ALLOW",
      "data_logged": ["action", "decision", "timestamp only"],
      "data_NOT_logged": [
        "your_real_name",
        "your_content",
        "your_submission"
      ],
      "data_source": {
        "type": "SYNTHETIC_TEST_SCENARIO",
        "real_pii_stored": false,
        "privacy_summary": "✅ Only metadata logged, your content is safe"
      }
    }
  ]
}
```

### Admin Viewing Analytics:
```
GET /admin/analytics
Response:
{
  "compliance_metrics": {
    "total_decisions_made": 1250,
    "percentage_allowed": 73.2,
    "policies_used": ["CS101", "DATA201"]
  },
  "data_source": {
    "type": "SYNTHETIC_TEST",
    "aggregation_level": "COURSE_LEVEL",
    "individual_pii_included": false,
    "privacy_summary": "✅ Only aggregated metrics shown, no individual student data"
  }
}
```

---

## ✅ Transparency at Each Step

| Step | Data Used | Data Sources | Privacy |
|------|-----------|--------------|---------|
| 1️⃣ Policy Creation | Public Guidelines | Cornell, Stanford PDFs | ✅ No PII |
| 2️⃣ Governance Check | Synthetic Test Case | test_student_001 (FAKE) | ✅ No PII |
| 3️⃣ Decision Made | Course Policy | From step 1 | ✅ No PII |
| 4️⃣ Log Stored | Metadata Only | action+decision+timestamp | ✅ No Content |
| 5️⃣ Student Sees Log | Their Own Decision Log | From step 4 | ✅ Safe View |
| 6️⃣ Admin Sees Stats | Aggregated Counts | All logs summed | ✅ No Names |

---

## 🚀 MVP Timeline (Current Phase)

**Phase 1: Synthetic Testing (NOW - Week 1)**
- ✅ Use only fake students (test_001, test_002, etc.)
- ✅ Use only public policies
- ✅ Test all features with safe data
- ✅ Show in API responses: `data_source.real_pii_stored = false`

**Phase 2: Pilot Colleges (Month 2)**
- 🔐 Real course data (IIT Delhi CS101)
- 🔐 Synthetic students (psud_001, psud_002) - fake names
- 🔐 Same privacy guarantees (metadata-only logging)
- 🔐 API responses will show: `data_source.type = "PILOT_REAL_COURSES"`

**Phase 3: Production (Month 3+)**
- 🔐 Real course data from multiple colleges
- 🔐 Real student logins (with consent)
- 🔐 Pseudonymous logging
- 🔐 API responses will show: `data_source.type = "PRODUCTION"`

---

## 📋 Data Provenance Checklist

Every API response includes this structure to show data sources:

```python
class DataProvenance:
    source_type: str  # PUBLIC_POLICY | SYNTHETIC_TEST | PILOT_REAL_COURSES | PRODUCTION
    source_name: str  # Where data came from
    real_pii_stored: bool = False  # Always false for MVP
    real_content_stored: bool = False  # Always false for MVP
    logged_fields: list = ["action", "decision", "timestamp"]  # What's logged
    retention_days: int  # How long kept (90 for test, 999999 for policy)
    privacy_summary: str = "✅ 100% Safe - No real PII, no content"
```

Every response will show:
- ✅ **Data Source**: Where the data comes from
- ✅ **PII Status**: Whether real names are stored
- ✅ **Content Status**: Whether real submissions are stored
- ✅ **Privacy Summary**: Human-readable safety statement

---

## 🎯 Bottom Line

**In every API response, you will CLEARLY see:**

```json
{
  "data_source": {
    "source_type": "SYNTHETIC_TEST or PUBLIC_POLICY or PILOT or PRODUCTION",
    "source_name": "Exact description of where data came from",
    "real_pii_stored": false,
    "real_content_stored": false,
    "privacy_summary": "✅ 100% Safe - No real PII, no content"
  }
}
```

**Students will see**: "✅ Your data is safe - only your decisions are logged, never your content or name"

**Faculty will see**: "✅ This policy is based on [Public University] guidelines, no real student data used"

**Admins will see**: "✅ These metrics are from course-level aggregations, no individual student data"

**Auditors will see**: "✅ Every API call shows its data sources - full transparency"
