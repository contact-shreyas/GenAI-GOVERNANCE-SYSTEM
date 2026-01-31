# Evaluation Plan & Methodology

## Overview

This document outlines the complete evaluation strategy for the GenAI Governance system, including datasets, baselines, metrics, and experimental designs. All evaluation is designed for reproducibility and publication in peer-reviewed venues.

## Datasets

### Dataset 1: Public University GenAI Policies Corpus

**Source**: Top 50 US universities (MIT, Stanford, Berkeley, Cornell, Michigan, etc.) + open repositories (EDUCAUSE, HEA Ireland)

**Scope**: N = 40–60 institutional and course-level policies

**Format**: 
- Raw: Original PDFs (policies_corpus/policies_raw/)
- Parsed: OCR text (policies_corpus/policies_parsed/)
- Canonical: Schemaified JSON (policies_corpus/policies_canonical.json)

**Contents per Policy**:
- policy_id: Unique identifier
- institution: University name
- policy_type: "institutional" or "course-level"
- assessment_scope: Which assessments covered
- allowed_actions: List of permitted AI use patterns
- prohibited_actions: Forbidden patterns
- disclosure_requirements: What must students disclose?
- logging_level: What's logged?

**Effort**: ~40 hours (2–4 hours per policy: scraping, OCR cleanup, schemaification)

**Output**: `datasets/policies_corpus/policies_canonical.json` (published for reproducibility)

---

### Dataset 2: Expert-Annotated Policy Q&A Benchmark

**Purpose**: Evaluate RAG co-pilot accuracy (citations, hallucination, faithfulness)

**Annotation Task**:
- Q: 80–100 policy questions covering diverse scenarios
- Gold answer: Correct answer (yes/no/depends) + exact citing clauses
- Annotators: 2 experts (faculty + AI policy administrator)
- Agreement: Cohen's kappa >0.70 on yes/no labels

**Question Types**:
- Role-specific: "As a TA, can I use ChatGPT to generate feedback?"
- Assessment-specific: "Is AI allowed in take-home exams?"
- Action-specific: "Does 'substantial modification' mean >50%?"
- Ambiguous/edge-case: "What counts as 'own work'?"

**Gold Label Structure**:
```json
{
  "question_id": "q001",
  "question": "Can a student use ChatGPT to brainstorm ideas for a problem set?",
  "policy_id": "course_cs101_genai_v2.1",
  "gold_answer": "yes",
  "citing_clauses": [
    {
      "policy_id": "course_cs101_genai_v2.1",
      "section": "Allowed Actions > use_genai_brainstorm",
      "exact_quote": "Use GenAI for ideation, brainstorming, outlining... applies_to_assessment_types: [problem_set]"
    }
  ],
  "caveats": ["Disclosure required via inline comment"],
  "annotation_experts": ["expert_alice", "expert_bob"],
  "inter_rater_agreement": "kappa=0.92"
}
```

**Effort**: ~40–60 hours (30 mins per question including discussion)

**Output**: `datasets/benchmark_qa.json` (published)

---

### Dataset 3: Policy Enforcement Scenario Test Suite

**Purpose**: Evaluate policy compiler + decision function accuracy

**Scenario Structure**: N = 40–50 scenarios
```json
{
  "scenario_id": "s001",
  "description": "CS101 student submits problem set with ChatGPT brainstorming disclosed",
  "context": {
    "course_id": "CS101",
    "actor_role": "student",
    "action": "use_genai_brainstorm",
    "assessment_type": "problem_set",
    "assessment_phase": "submission"
  },
  "policy_id": "course_cs101_genai_v2.1",
  "gold_decision": "ALLOW",
  "gold_obligations": [
    {"type": "disclosure_required", "format": "inline_comment"}
  ]
}
```

**Coverage**:
- Allowed cases: 10–15 (baseline expectations)
- Denied cases: 8–10 (clear violations)
- Override cases: 5 (disability accommodations, appeals)
- Conflict cases: 5–8 (allowed by one rule, denied by another)
- Ambiguous cases: 5 (action not mentioned; test default behavior)

**Effort**: ~20 hours (systematic curation)

**Output**: `datasets/benchmark_scenarios.json` (published)

---

## Baselines

### Baseline 0: Manual PDF Interpretation
- **Method**: Human (faculty member) reads policy PDF, answers question manually
- **Accuracy**: Ground truth but time-prohibitive at scale (~95% but 30 mins per question)
- **Time**: ~30 mins per question

### Baseline 1: Naive Keyword Search
- **Method**: Simple string matching on policy PDFs (e.g., grep "brainstorm")
- **Accuracy**: Returns matching sections; high false positives
- **Expected**: ~60% citation correctness, poor for nuanced questions

### Baseline 2: Naive RAG Without Verification
- **Method**: LangChain/LlamaIndex with no verification step
- **Outputs**: Answer + basic citations, no verification score
- **Expected**: ~65% answer correctness, ~20% hallucination rate, ~75% citation correctness

### Baseline 3: Policy-as-Code Enforcement Only (No RAG)
- **Method**: System without co-pilot; only decision function
- **Measures**: Enforcement accuracy vs scenario gold decisions
- **Expected**: ~85% accuracy (decision engine alone without RAG)

---

## Metrics & Operationalization

### A. Enforcement Accuracy

```
Accuracy_enforce = (# correct decisions) / |Test Set|
```

**Breakdown**:
- Precision per decision type (ALLOW, DENY, REQUIRE_JUSTIFICATION)
- F1 per scenario type (allowed, denied, override, conflict, ambiguous)
- Confusion matrix

**Target**: >90%

---

### B. Conflict Detection

```
Precision = (# correctly flagged conflicts) / (# total flagged)
Recall = (# correctly flagged conflicts) / (# true conflicts in test set)
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

**Conflict types**:
1. Action contradiction (action both allowed and denied)
2. Scope overlap (two policies for same course/assessment)
3. Temporal conflict (version ordering)
4. Role/phase ambiguity

**Test set**: 15–20 policy pairs with manual gold labels

**Target**: F1 >0.85

---

### C. RAG Factuality & Citation Correctness

```
Citation_Correctness = (# correctly cited clauses) / (# total citations)
```

Citation is "correct" if:
1. Quoted text exists in policy (fuzzy match ≥0.85 similarity)
2. Quote meaning-preserving (semantic equivalence)

```
Faithfulness = (# claims supported by retrieved context) / (# total claims)
```

Measured via:
1. NLI model: entailment scorer on (context, claim)
2. Manual expert review: is claim supported?

```
Hallucination_Rate = (# hallucinated claims) / (# total claims)
```

Claim is hallucinated if it doesn't appear in or follow from context.

```
Answer_Correctness = (# correct answers) / |Q&A Benchmark|
```

Correct if answer matches gold label + reasoning sound.

**Targets**:
- Citation correctness: >95%
- Faithfulness: >90%
- Hallucination rate: <5%
- Answer correctness: >90%

---

### D. Usability: Policy Authoring

```
T_template = minutes to author policy via template form
T_freeform = minutes to same policy via free-form JSON

Improvement = (T_freeform - T_template) / T_freeform * 100%
```

```
Errors_template = (# policies with validation errors) / |template group|
Errors_freeform = (# policies with validation errors) / |freeform group|

Error_Rate_Improvement = (Errors_freeform - Errors_template) / Errors_freeform * 100%
```

**Targets**:
- Time improvement: >50%
- Error rate improvement: >70%

---

### E. Student Trust & Perceived Fairness

**System Usability Scale (SUS)**:
- 10-item validated scale (0–100 range)
- Treatment group target: ≥75 (acceptable usability)
- Comparison: Treatment (with logs) vs Control (no logs)
- Expected difference: +15 pts

**Perceived Fairness**:
- 3–4 item Likert: "The AI policy is fair to me" (1–5 scale)
- Target: >4 / 5

**Privacy Comfort**:
- "I am comfortable with how the institution logs my AI use" (1–5)
- Target: No degradation (should be positive given transparency)

---

### F. Verification Score Calibration

```
Verification_Score_mean = mean(V(answer_i, context_i))
Correlation(verification_score, answer_correctness) = Pearson ρ
```

**Target**: High positive correlation (ρ >0.70)
- High score (≥0.85) → answer likely correct
- Low score (<0.70) → answer should be reviewed

---

## Experimental Design

### Study 1: Faculty Usability Study (N=12)

**Participants**:
- 12 faculty from 3–4 institutions
- Mix: 4 AI-familiar, 4 skeptical, 4 neutral
- Disciplines: STEM, humanities, social sciences
- Incentive: $50 gift card

**Protocol (within-subject, ~60 mins)**:

1. **Introduction** (10 min): Explain system, show demo
2. **Task 1 – Template-based authoring** (20 min):
   - Scenario: "Create a GenAI policy for your course"
   - Measure: time, # errors, # refinements
3. **Think-aloud** (15 min):
   - Faculty verbalize reasoning while authoring
   - Moderator probes: "What made you choose that option?"
4. **Task 2 – Review conflict detection** (10 min):
   - System shows detected conflicts
   - Faculty resolves or dismisses
   - Measure: agreement with conflict detection
5. **Interview** (15 min):
   - Satisfaction, perceived usefulness, barriers
   - Open-ended feedback
6. **Usability questionnaire** (5 min): System Usability Scale (SUS)

**Analysis**:
- Descriptive stats: mean time ± std dev, error counts
- Qualitative coding: barriers, trust factors, use cases (Cohen's kappa >0.70)
- SUS score distribution

**Artifact**: Usability study report (5–10 pages)

---

### Study 2: Policy Q&A Benchmark Evaluation (Offline)

**Protocol**:

1. Run copilot on 80–100 benchmark questions
2. Collect: answer, citations, verification score
3. Manual annotation (2 experts):
   - Is answer correct? (yes/no/partial)
   - Is each citation correct? (yes/no)
   - Is answer hallucinating? (yes/no)
4. NLI model: entailment scoring on (context, claim)
5. Metrics calculation + correlation analysis

**Artifact**: Benchmark evaluation report (3–5 pages) + CSV results

---

### Study 3: Student Transparency Study (N=50, RCT)

**Design**: Randomized controlled trial

**Condition 1 (Treatment, N=25)**:
- GenAI policy enforced at submission
- Transparency logs visible to student (aggregated, non-PII)
- Student-facing explanation: "What this log means"

**Condition 2 (Control, N=25)**:
- Same course, same policy enforcement
- NO transparency logs visible
- Standard institutional communication

**Protocol**:

1. **Enrollment**: Random assignment (stratified by prior GPA?)
2. **Mid-semester (Week 7)**:
   - Treatment group views their logs
   - Brief tutorial (2 min video): "What this log means"
3. **End of semester**:
   - Survey (10 mins): SUS, fairness, privacy, trust
   - Optional: interview (5 volunteers per condition)

**Survey**:
- SUS (10 items, 0–100 scale)
- Fairness (3 items, 1–5 Likert)
- Privacy (2 items, 1–5 Likert)
- Open-ended: "What would improve AI governance?"

**Artifact**: Student study report (5–8 pages) + statistical tables

---

## Data Analysis Plan

### Quantitative

```
Descriptive stats:
  - Enforcement accuracy: mean, 95% CI
  - Citation correctness: binomial proportion + Wilson CI
  - SUS score: mean ± std dev, by condition
  - Authoring time: median (min, max)

Inferential stats:
  - t-test: Treatment vs Control SUS
  - Chi-square: Accuracy across scenario types
  - Spearman ρ: Verification score vs Answer correctness
  - Cohen's d: Effect size for SUS difference

Visualization:
  - Confusion matrix (decisions vs gold)
  - Scatter: verification score vs correctness
  - Box plot: SUS by condition
  - Heatmap: conflict types vs detection accuracy
```

### Qualitative

```
Coding scheme (think-aloud + interviews):
  Categories:
    - Usability barriers (complexity, clarity, trust, time)
    - Perceived fairness (transparency, consistency, voice)
    - Privacy comfort (data minimization, access, control)
    - Improvement suggestions (features, communication, governance)

Analysis:
  - Thematic coding (two independent coders, kappa >0.70)
  - Consensus codebook & themes
  - Exemplary quotes
```

---

## Reproducibility Checklist

✓ Datasets published (corpus, Q&A benchmark, scenarios)
✓ Evaluation scripts released (runnable offline)
✓ Study protocols documented
✓ Survey instruments provided
✓ Raw data (de-identified) available upon request
✓ Analysis code (Jupyter, Python, R) included
✓ Results reported with effect sizes + confidence intervals
✓ Limitations clearly documented

**Time to reproduce**: 4–8 hours setup | 1–2 hours key results

---

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for step-by-step instructions.
