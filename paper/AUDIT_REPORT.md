# PAPER AUDIT REPORT
## Date: January 30, 2026

## SITUATION SUMMARY
**NO existing Paper.pdf found** — Will create IEEE conference paper FROM research artifacts:
- README.md (348 lines)
- docs/ARCHITECTURE.md (355 lines)
- docs/EVALUATION.md (413 lines)
- research_framework.ipynb (347 lines)
- docs/API.md (present but not yet fully analyzed)

---

## CONTENT INVENTORY

### Research Artifacts Present
✅ **System Architecture** — Complete diagrams, data flows, module specifications
✅ **Evaluation Methodology** — 3 datasets, baselines, metrics, experimental designs
✅ **Research Questions** — 3 clear RQs with measurable targets
✅ **Novel Contributions** — 4 identified contributions
✅ **Implementation** — Full backend (FastAPI/Python), frontend (Next.js), databases
✅ **Datasets** — Policy corpus (50 universities), Q&A benchmark (90 questions), scenarios (45 cases)

### Content Breakdown by Section

#### Abstract Components (Present)
- ✅ Problem statement: GenAI adoption outpaced policy infrastructure
- ✅ Gap: Policies as prose PDFs → inconsistent interpretation
- ✅ Solution: Policy-as-code + verified RAG + transparency ledger
- ✅ Key results: Targets defined (>90% accuracy, >95% citation correctness, <5% hallucination)

#### Introduction Content (Present)
- ✅ Motivation: Manual governance is brittle, untrustworthy
- ✅ Research questions (3)
- ✅ Contributions (4 novel claims)
- ✅ System overview (high-level architecture)

#### Related Work (NOT EXPLICITLY WRITTEN - TO BE SYNTHESIZED)
- ❌ Policy-as-code literature citations needed
- ❌ RAG/verification literature needed
- ❌ Educational AI governance literature needed
- ❌ Transparency/privacy-preserving systems needed

#### Methodology (Present)
- ✅ System architecture diagram
- ✅ Data structures (PolicyJSON, GovernanceContext, etc.)
- ✅ 4 core modules: Compiler, Enforcement, Ledger, RAG Copilot
- ✅ Formal model: f_policy(P, C) → (decision, obligations, trace)

#### Evaluation (Present)
- ✅ **3 Datasets**:
  1. Policy corpus: 50 universities, 40-60 policies
  2. Q&A benchmark: 90 expert-annotated questions (Cohen's κ >0.70)
  3. Scenario test suite: 45 cases (allowed, denied, conflicts, ambiguous)
- ✅ **4 Baselines**:
  1. Manual PDF interpretation (~95% acc, 30min/question)
  2. Naive keyword search (~60%)
  3. Naive RAG without verification (~65% answer correctness, 20% hallucination)
  4. Policy-as-code only (no RAG)
- ✅ **Metrics**:
  - Enforcement accuracy >90%
  - Conflict detection F1 >0.85
  - Citation correctness >95%
  - Answer correctness >90%
  - Hallucination rate <5%
  - Student trust (SUS) +15 points
- ✅ **3 User Studies**:
  1. Faculty usability (N=12, within-subject, authoring time reduction >50%)
  2. RAG benchmark (offline, 90 questions)
  3. Student transparency RCT (N=50, treatment vs control)

#### Results (NOT YET GENERATED - TARGETS DEFINED)
- ⚠️ **TODO**: System not yet evaluated against benchmarks
- ⚠️ Enforcement accuracy: Target >90% (no actual results yet)
- ⚠️ RAG metrics: Targets defined (>95% citation, <5% hallucination) but not measured
- ⚠️ User studies: Design complete, not yet run
- **ACTION**: Mark as TODO sections with placeholders for when evaluation runs

#### Discussion/Limitations (IMPLICIT - TO BE SYNTHESIZED)
- ✅ Privacy-preserving approach (metadata-only logging)
- ✅ Trust gaps addressed via verification
- ✅ Traceability via full decision trace
- ❌ Limitations not explicitly documented (need to infer and write)

#### Conclusion (IMPLICIT - TO BE WRITTEN)
- ✅ Contributions summary
- ✅ Future work implied (scale to 100+ universities, deploy in production)

---

## REPRODUCIBILITY INVENTORY

### What Exists
✅ **Architecture diagrams** (ASCII art in ARCHITECTURE.md)
✅ **Dataset specifications** (sizes, formats, curation time)
✅ **Code structure** (backend/frontend modules defined)
✅ **Evaluation protocol** (metrics, baselines, study designs)
✅ **Docker deployment** (docker-compose.yml, full stack)

### What's Missing (TO BE CREATED)
❌ **Actual experimental results** (system built but not evaluated)
❌ **Generated figures**: Architecture diagram (need vector PDF), metrics tables, comparison tables
❌ **LaTeX source**: IEEE paper not yet written
❌ **50+ verified references**: Need policy-as-code, RAG, edu-tech citations

---

## ESTIMATED WORD COUNTS (TARGETS FOR 9-PAGE IEEE PAPER)

### IEEE Conference Format Guidelines
- 9 pages TOTAL (including references)
- 2-column format
- ~400-450 words per column = ~800-900 words per page
- 9 pages = ~7,200-8,100 words TOTAL
- References section: ~2,000-2,500 words (50-60 refs @ 40-50 words each)
- Main content: ~5,000-5,500 words

### Proposed Section Word Counts (Main Content ~5,500 words)

| Section | Target Words | Priority |
|---------|-------------|----------|
| **Abstract** | 150-200 | HIGH |
| **I. Introduction** | 800-1,000 | HIGH |
| **II. Related Work** | 900-1,100 | HIGH |
| **III. Problem Formulation** | 400-500 | MEDIUM |
| **IV. System Design** | 1,200-1,400 | HIGH |
| **V. Evaluation Setup** | 800-1,000 | HIGH |
| **VI. Results** | 800-1,000 | HIGH |
| **VII. Discussion & Limitations** | 500-600 | MEDIUM |
| **VIII. Conclusion** | 200-300 | LOW |
| **References (50-60)** | 2,000-2,500 | HIGH |

**TOTAL**: ~8,000 words (fits 9 pages)

---

## CURRENT CONTENT AVAILABILITY ANALYSIS

### Section-by-Section Assessment

#### ✅ STRONG (can be written directly from artifacts)
1. **Abstract** — All components present
2. **Introduction** — Problem, RQs, contributions documented
3. **System Design** — Complete architecture, modules, data structures
4. **Evaluation Setup** — Datasets, baselines, metrics fully specified

#### ⚠️ MODERATE (needs synthesis/research)
5. **Related Work** — Need to research and cite 30-40 real papers
6. **Problem Formulation** — Formal model present, need to polish notation
7. **Results** — Targets defined, but actual results NOT yet generated

#### ⚠️ WEAK (needs creation)
8. **Discussion** — Implicit in docs, need to synthesize insights
9. **Limitations** — Not explicitly documented, need to infer
10. **Figures/Tables** — Diagrams present (ASCII), need vector graphics

---

## TOP 10 ISSUES FOUND

### CRITICAL (blocking publication)
1. **NO EXPERIMENTAL RESULTS** — Targets defined (>90% accuracy, etc.) but system not evaluated against benchmarks
   - **FIX**: Add TODO placeholders + exact steps to run evaluation when ready
   - **ALTERNATIVE**: Present as "system design + evaluation protocol" paper (acceptable for some venues)

2. **NO CITATIONS** — Zero references in current artifacts
   - **FIX**: Research and add 50+ real papers (policy-as-code, RAG, edu-tech, privacy)
   - **STATUS**: Will build refs.bib with verified DOIs/arXiv

3. **NO VECTOR FIGURES** — Only ASCII diagrams
   - **FIX**: Create architecture diagram, dataset flow, metrics tables
   - **STATUS**: Will generate programmatically where possible

### HIGH PRIORITY (quality issues)
4. **Related Work section missing** — No positioning vs. prior work
   - **FIX**: Synthesize from policy-as-code, RAG verification, educational governance literature

5. **Results section has NO data** — Only target metrics
   - **FIX**: Add TODO blocks with exact commands to generate results
   - **EXAMPLE**: "TODO: Run `pytest backend/tests/benchmark_evaluation.py` to generate Table II"

6. **Discussion/Limitations incomplete** — Implicit in docs
   - **FIX**: Explicitly state: (1) Evaluation not yet run, (2) Generalizability limited to US universities, (3) RAG verification depends on quality embeddings

### MEDIUM PRIORITY (polish issues)
7. **Notation inconsistency** — f_policy() vs evaluate_policy()
   - **FIX**: Standardize to f_policy(P, C) → D throughout paper

8. **Dataset sizes estimates** — "40-60 policies" lacks precision
   - **FIX**: Count actual JSON files in datasets/policies_corpus/policies_parsed/

9. **Comparison table missing** — No explicit table comparing to prior systems
   - **FIX**: Create Table comparing: Manual, Naive keyword, Naive RAG, Policy-as-code only, vs. OUR SYSTEM

10. **Word (.docx) version not planned** — Only LaTeX focus so far
    - **FIX**: Will use pandoc conversion after LaTeX finalized

---

## REPRODUCIBILITY CHECKLIST

| Item | Status | Location/Command |
|------|--------|------------------|
| **Code** | ✅ Present | `backend/`, `frontend/` |
| **Docker setup** | ✅ Complete | `docker-compose up` |
| **Dataset specs** | ✅ Documented | `docs/EVALUATION.md` |
| **Evaluation protocol** | ✅ Documented | `docs/EVALUATION.md`, `research_framework.ipynb` |
| **Actual datasets** | ⚠️ Partial | `datasets/policies_corpus/policies_parsed/` has 9 policies, need 40-60 |
| **Benchmark results** | ❌ Not generated | TODO: Run `pytest backend/tests/` |
| **User study data** | ❌ Not run | TODO: IRB approval + recruit N=12+50 |
| **LaTeX source** | ❌ Not created | TODO: Create `paper/main.tex` |
| **Figures (vector)** | ❌ Not created | TODO: Generate PDFs in `paper/figures/` |
| **Build commands** | ❌ Not documented | TODO: Add `paper/Makefile` |

---

## PLAN TO REACH EXACTLY 9 PAGES

### Strategy
1. **Start with full content** (~5,500 words main + 2,500 refs = 8,000 words total)
2. **Compile and measure** using IEEE template
3. **Adjust iteratively**:
   - If >9 pages: Tighten Related Work, reduce dataset details, merge Discussion into Results
   - If <9 pages: Add evaluation protocol details, expand limitations, add calibration analysis

### NO FORMATTING HACKS ALLOWED
- ✅ Use standard IEEEtran.cls
- ✅ 10pt font, standard margins
- ✅ 2-column format
- ❌ NO font size changes
- ❌ NO margin manipulation
- ❌ NO \vspace hacks

### Page Budget Allocation (Target)
- Pages 1-2: Abstract, Intro, Related Work (2,000 words)
- Pages 3-4: Problem Formulation, System Design (1,600 words)
- Pages 5-6: Evaluation Setup, Results (1,600 words)
- Pages 7-8: Discussion, Conclusion, Start References (1,300 words + refs)
- Page 9: Remaining References (~1,200 words)

---

## IMMEDIATE NEXT STEPS

### STEP 2A: Count existing datasets
```powershell
Get-ChildItem "datasets/policies_corpus/policies_parsed/*.json" | Measure-Object | Select-Object Count
```
**Expected**: 9 policies currently (need to scale to 40-60 or adjust paper claims)

### STEP 2B: Generate word count script
Create `paper/scripts/count_words.py` to measure LaTeX word counts per section

### STEP 2C: Start LaTeX structure
Create `paper/main.tex` with IEEEtran template and section stubs

### STEP 3: Build refs.bib (50+ references)
Research and add real papers:
- Policy-as-code: Guardrails, NeMo Guardrails, policy languages
- RAG: REALM, DPR, RETRO, self-RAG, verification methods
- Educational AI: AIED, SIGCSE, FAccT papers on AI in education
- Privacy: Differential privacy, transparency systems

### STEP 4: Create figures
- Figure 1: System architecture (convert ASCII to TikZ or draw in Inkscape)
- Table I: Dataset statistics
- Table II: Metrics comparison (targets vs baselines)
- Table III: System comparison matrix

---

## SUCCESS CRITERIA

### Mandatory (blocking submission)
- ✅ Exactly 9 pages (including references)
- ✅ 50+ verified references (DOI/arXiv checked)
- ✅ No fabricated results (all TODOs clearly marked)
- ✅ Reproducible builds (Makefile with `make paper` command)
- ✅ DOCX version matches PDF content
- ✅ CITATION_AUDIT.md logs all reference verification

### Desirable (quality markers)
- ✅ Vector figures (PDF/SVG, not PNG)
- ✅ Consistent notation (f_policy, not evaluate_policy)
- ✅ Clear reproducibility steps for TODOs
- ✅ Tables generated from scripts (not manual entry)
- ✅ Strong Related Work positioning

---

## RISK ASSESSMENT

### HIGH RISK
⚠️ **Results section is empty** — Paper presents system + protocol but NO evaluation data
   - **MITIGATION**: Frame as "design + methodology" paper acceptable for venues like CHI, CSCW, UIST
   - **ALTERNATIVE**: Add TODO blocks with exact reproduction steps

### MEDIUM RISK
⚠️ **9-page constraint** — Might need multiple compile iterations
   - **MITIGATION**: Start with 10-11 pages, then tighten iteratively

### LOW RISK
✅ **Citation verification** — Can use DOI APIs and manual checks
✅ **LaTeX compilation** — Standard IEEEtran template
✅ **DOCX generation** — Pandoc handles LaTeX→DOCX well

---

## ESTIMATED TIME TO COMPLETION

| Task | Estimated Hours |
|------|----------------|
| Create main.tex structure | 1h |
| Write Abstract + Intro | 2h |
| Research + add 50+ references | 4h |
| Write Related Work | 3h |
| Write System Design | 2h |
| Write Evaluation Setup | 2h |
| Write Results (with TODOs) | 2h |
| Write Discussion + Conclusion | 2h |
| Create figures (3-4 vector graphics) | 3h |
| Iterate to 9 pages exactly | 2h |
| Generate DOCX + verify | 1h |
| Create CITATION_AUDIT.md | 1h |
| Write build scripts | 1h |
| **TOTAL** | **26 hours** |

---

## PAPER TYPE RECOMMENDATION

Given that **results are not yet generated**, I recommend framing this as:

### Option 1: "System Design + Evaluation Protocol" Paper
**Target venues**: CHI, CSCW, UIST (systems/design focus)
**Emphasis**: Novel architecture, reproducible evaluation protocol, open-source implementation
**Results section**: Present targets and baselines, mark actual results as TODO

### Option 2: "In-Progress" / Workshop Paper
**Target venues**: AIED workshops, FAccT workshops, SIGCSE short papers
**Length**: 4-6 pages
**Status**: Partial results acceptable

### Option 3: Full Conference Paper (REQUIRES running evaluation)
**Target venues**: FAccT, AIED, SIGCSE, IEEE conferences
**Requirements**: Complete evaluation, user studies, statistical analysis
**Timeline**: +3 months (run studies, collect data, analyze)

**RECOMMENDATION**: Proceed with **Option 1** for this task, mark results as TODO with exact reproduction steps. This is acceptable for design-oriented venues and demonstrates rigor.

---

## OUTPUT FILES TO CREATE

### In paper/ directory:
- `main.tex` — IEEE conference paper (IEEEtran)
- `refs.bib` — 50+ verified references
- `figures/architecture.pdf` — System architecture diagram
- `figures/dataset_flow.pdf` — Data collection flow
- `scripts/count_words.py` — Word count per section
- `scripts/generate_tables.py` — Generate tables from data
- `Makefile` — Build automation

### In dist/ directory:
- `paper_IEEE_9pages.pdf` — Final PDF (exactly 9 pages)
- `paper_IEEE_9pages.docx` — Word version (matches PDF)

### In root directory:
- `CITATION_AUDIT.md` — Reference verification log

---

## CONCLUSION

**STATUS**: Ready to proceed with paper creation
**APPROACH**: IEEE 9-page conference paper based on existing research artifacts
**MAIN CHALLENGE**: Results section will have TODO placeholders (evaluation not yet run)
**ESTIMATED COMPLETION**: 26 hours of focused work

✅ All prerequisites met (architecture, datasets, methodology documented)
✅ Clear structure and targets defined
✅ Reproducibility path documented

**NEXT**: Begin creating LaTeX structure (main.tex) and refs.bib
