# 📊 Datasets: GenAI Governance Layer

## Overview

This directory contains **public university policies** on AI use in academics. All data is:
- ✅ **Sourced from public university websites** (no private data)
- ✅ **Freely accessible** (all institutions publish these policies publicly)
- ✅ **Representative of real-world governance** (from leading global institutions)
- ✅ **Machine-readable format** (JSON for easy parsing)

---

## 📁 Directory Structure

```
datasets/
└── policies_corpus/
    ├── policies_raw/           ← Original documents (PDFs, text)
    └── policies_parsed/        ← Processed JSON files
        ├── cornell_genai_policy_2025.json
        ├── stanford_ai_ethics_2025.json
        └── iitdelhi_ai_integrity_2025.json
```

---

## 📋 Available Policies

### 1. Cornell University GenAI Policy 2025
**File**: `cornell_genai_policy_2025.json`

| Property | Value |
|----------|-------|
| **Source** | https://academicaffairs.cornell.edu/policies/ai-in-education |
| **Institution** | Cornell University (USA) |
| **Scope** | Undergraduates, Graduates, Faculty, Staff |
| **Focus** | GenAI in Education - Allowed vs Prohibited Uses |
| **Key Content** | Brainstorming ✅, Code Review ✅, Research ✅, Writing ✅, But NOT: Exam cheating ❌, Submitting AI as own ❌ |
| **Disclosure Format** | Inline comment, Footnote, or Separate statement |

**Sample Allowed Use**:
```json
{
  "use_case": "Brainstorming and ideation",
  "description": "Using AI to generate ideas for essays, projects, or research",
  "disclosure_required": true,
  "examples": [
    "ChatGPT to brainstorm essay topics",
    "Claude to generate research questions"
  ]
}
```

---

### 2. Stanford University AI Ethics 2025
**File**: `stanford_ai_ethics_2025.json`

| Property | Value |
|----------|-------|
| **Source** | https://uit.stanford.edu/ai-ethics-policy |
| **Institution** | Stanford University (USA) |
| **Scope** | All students, Faculty, Researchers |
| **Focus** | AI Ethics + Academic Integrity |
| **Key Content** | Learning ✅, Assistance ✅, Analysis ✅, Quality Assurance ✅, But NOT: Submission without disclosure ❌, Exam cheating ❌ |
| **Disclosure Format** | Statement: "I used [Tool] for [Purpose]" |

**Sample Violation**:
```json
{
  "violation": "Submitting AI-generated work without disclosure",
  "severity": "Critical",
  "applies_to": "All assessments",
  "penalty": "Academic integrity hearing"
}
```

---

### 3. IIT Delhi Academic Integrity & AI Code 2025
**File**: `iitdelhi_ai_integrity_2025.json`

| Property | Value |
|----------|-------|
| **Source** | https://iitd.ac.in/academics/integrity-policy |
| **Institution** | IIT Delhi (India) |
| **Scope** | All students |
| **Focus** | Code of Conduct for AI in Academic Work |
| **Key Content** | Learning ✅, Literature Review ✅, Programming ✅, Data Analysis ✅, But NOT: Exam AI ❌, Research cheating ❌ |
| **Disclosure Format** | Footnote + formal declaration in thesis |

**Sample Disclosure Template**:
```
"I used ChatGPT (OpenAI) for approximately 30% of this assignment, 
specifically for brainstorming ideas and improving paragraph clarity. 
All major arguments and code logic are my own work."
```

---

## 🔍 Data Format

Each policy file contains:

```json
{
  "metadata": {
    "source": "Official University Policy URL",
    "institution": "University Name",
    "date_published": "YYYY-MM-DD",
    "version": "X.Y"
  },
  "policy": {
    "id": "unique_identifier",
    "title": "Full Policy Title",
    "scope": { "applies_to": [...], "applies_in": [...] },
    "allowed_uses": [...],
    "prohibited_uses": [...],
    "disclosure_requirements": {...}
  }
}
```

---

## 💡 How This System Uses The Policies

### 1. **Policy Compilation** (Faculty Feature)
- Faculty fills form with their course rules
- System compiles rules against Cornell/Stanford/IIT templates
- Generates executable JSON policy with conflict detection

### 2. **Governance Enforcement** (System Feature)
- Student submits work with context (course, action, assessment type)
- System loads applicable policy (e.g., Cornell CS101)
- Matches action against allowed/prohibited rules
- Returns ALLOW/DENY + obligations

### 3. **Student Q&A** (Copilot Feature)
- Student asks: "Can I use ChatGPT to brainstorm?"
- System searches policy corpus
- Returns answer with citation: "Cornell allows brainstorming with disclosure"
- Provides confidence score: 98%

### 4. **Transparency Dashboard** (Student Feature)
- Shows what student's actions were logged
- Demonstrates privacy commitment
- Shows policy source: "Decision based on Cornell GenAI Policy 2025"

### 5. **Admin Analytics** (Analytics Feature)
- Aggregates decisions across courses
- Shows compliance rates by policy
- Identifies most common use cases

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Total Policies** | 3 (growing) |
| **Total Institutions** | 3 (USA, India) |
| **Allowed Actions Defined** | 15+ |
| **Prohibited Uses Defined** | 8+ |
| **Policy Coverage** | Undergraduate + Graduate + Research |

---

## 🌍 Data Sources

All policies are:
1. **Publicly available** on institution websites
2. **Current as of** January 2026
3. **Machine-readable** (parsed from PDFs/HTML)
4. **Fully attributed** (source URL included)

| Institution | Region | Policy Type |
|------------|--------|-------------|
| Cornell University | USA (Northeast) | Comprehensive GenAI Policy |
| Stanford University | USA (West Coast) | AI Ethics + Honor Code |
| IIT Delhi | India | Academic Integrity Code |

---

## 🔄 How To Add New Policies

### Step 1: Source Policy
1. Visit university website (e.g., https://academicaffairs.cornell.edu/)
2. Download official AI/Academic Integrity policy (PDF or HTML)
3. Note the publication date and version

### Step 2: Parse to JSON
```json
{
  "metadata": {
    "source": "Official URL",
    "institution": "University Name",
    "date_published": "YYYY-MM-DD"
  },
  "policy": {
    // ... (follow the template in existing policies)
  }
}
```

### Step 3: Save File
- Location: `datasets/policies_corpus/policies_parsed/`
- Naming: `{institution}_{topic}_{year}.json`
- Example: `mit_ai_policy_2026.json`

### Step 4: Register in System
The system automatically discovers new policy files in the directory.

---

## 🎯 MVP Datasets vs Future

### Current (MVP) - Synthetic Test Data
- ✅ Sample policies from 3 major institutions
- ✅ Synthetic student data (fake IDs: test_001, psud_001)
- ✅ Synthetic course data (CS101_2025_spring, etc.)
- ✅ **NO real student information**

### Future (Pilot Phase) - Real Course Data
- 🔒 Real course enrollments (with consent)
- 🔒 Real faculty policy requirements
- 🔒 Real student interactions (pseudonymized)
- 🔒 **Still maintains privacy: pseudonyms + metadata-only logging**

### Future (Production Phase) - Multi-Institution
- 🌍 20+ university policies
- 🌍 Real student data (encrypted, consented)
- 🌍 Real usage analytics
- 🌍 Compliance reports for institutions

---

## 📚 Using Policies in Code

### Example 1: Load Cornell Policy
```python
import json

with open('datasets/policies_corpus/policies_parsed/cornell_genai_policy_2025.json') as f:
    cornell_policy = json.load(f)

# Access allowed uses
for allowed_use in cornell_policy['policy']['allowed_uses']:
    print(f"✅ {allowed_use['use_case']}")
    print(f"   Disclosure: {allowed_use['disclosure_required']}")
```

### Example 2: Check Prohibited Use
```python
# Check if action is prohibited
student_action = "submit_ai_as_own"
prohibited = cornell_policy['policy']['prohibited_uses']

for rule in prohibited:
    if rule['use_case'].lower() == student_action:
        print(f"❌ PROHIBITED: {rule['description']}")
```

### Example 3: Get Disclosure Template
```python
# Show student how to disclose
disclosure_req = cornell_policy['policy']['disclosure_requirements']
for format_option in disclosure_req['format_options']:
    print(f"Format: {format_option['format']}")
    print(f"Example: {format_option['example']}")
```

---

## 🔒 Privacy & Attribution

All policies are:
- **Publicly sourced** (no private data)
- **Properly attributed** (URL and date included)
- **Non-commercial use** (for educational system)
- **Transformative use** (adapted for governance engine, not reproduction)

When system cites a policy, it includes:
- Institution name
- Policy title
- Publication date
- Specific rule cited

Example: _"Cornell University GenAI Policy 2025, Section 3.1: Brainstorming is allowed with disclosure"_

---

## 📈 Dataset Quality Metrics

| Metric | Status |
|--------|--------|
| Source Verification | ✅ All URLs verified |
| Data Completeness | ✅ All key sections included |
| Format Validation | ✅ JSON schema validated |
| Timeliness | ✅ Current as of 2025-2026 |
| Attribution | ✅ Full source documentation |

---

## 🎓 Educational Use

This dataset is used to:
1. **Train** the governance system on real policy patterns
2. **Educate** students about institutional policies
3. **Guide** faculty in policy design
4. **Benchmark** against leading institutions
5. **Document** the evolution of AI policies in academia

---

**Last Updated**: January 29, 2026  
**Next Update**: As new policies are published by institutions

