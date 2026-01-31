# PAPER EXPANSION PLAN TO 11 PAGES

## Current Status (BASELINE)
- **Pages:** 4 (IEEE format)
- **Word Count:** 1,742 words in LaTeX
- **References:** 53 entries in refs.bib (GOOD - meets 50+ requirement)
- **Sections:** 9 sections + references
- **Tables:** 8
- **Algorithms:** 2
- **Figures:** 0 (CRITICAL GAP)

## Target Status (11 PAGES)
- **Pages:** 11 exactly (including references)
- **Word Count:** ~5,500-6,000 words
- **Word Deficit:** +3,758 to +4,258 words needed
- **References:** 50+ (ALREADY MET with 53)
- **Figures:** Add 3-4 key figures (architecture, results, comparison)

## Expansion Strategy (NO FAKE DATA)

### Section 1: Introduction (+400 words)
**Current:** Brief problem statement
**Add:**
- Detailed motivation with real university policy examples (MIT, Stanford)
- Concrete scenarios showing governance failures
- Research questions explicitly stated
- Contributions rewritten as detailed bullets with technical specifics

### Section 2: Related Work (+600 words)
**Current:** Minimal subsections
**Add:**
- **2.1 AI Ethics Frameworks** - IEEE, EU AI Act, ACM principles
- **2.2 Policy-as-Code Systems** - OPA, AWS IAM, comparison table
- **2.3 RAG Systems** - Lewis et al., Karpukhin DPR, cite more
- **2.4 Educational AI Governance** - Recent AIED/SIGCSE papers
- **2.5 Privacy & Trust** - Differential privacy, k-anonymity
- **Comparison Table:** Our system vs prior work (5-6 dimensions)

### Section 3: Problem Formulation (+300 words) **NEW SECTION**
**Add before System Architecture:**
- Formal problem definition
- Stakeholders: students, faculty, administrators
- Requirements: R1-R6 enumerated (consistency, privacy, transparency, etc.)
- Threat model: what attacks/misuse we prevent
- Design principles

### Section 4: System Architecture (+500 words)
**Current:** Basic layer description
**Add:**
- **Architecture diagram** (Figure 1: system components, data flow)
- Component interaction protocol
- Detailed data schemas for each layer
- Security properties (cryptographic details)
- Deployment architecture (Docker, cloud-ready)

### Section 5: Implementation (+400 words)
**Current:** Tech stack table
**Add:**
- Code organization (module structure)
- API design decisions
- Database schema details
- Testing strategy (unit, integration, system tests)
- CI/CD pipeline
- **Figure 2:** ER diagram or API sequence diagram

### Section 6: Evaluation (+800 words)
**Current:** Basic metrics tables
**Add:**
- **6.1 Experimental Setup** - Detailed evaluation protocol
- **6.2 Dataset Description** - 9 university policies (when collected, how parsed)
- **6.3 Conflict Detection Results** - Expand with examples, confusion matrix
- **6.4 Performance Benchmarks** - Latency under load, throughput tests
- **6.5 Privacy Validation** - Audit methodology, PII detection tests
- **6.6 Usability** - (TODO: Add placeholder for future user study, mark as limitation)
- **Figure 3:** Results plots (latency distribution, conflict detection accuracy)
- **Figure 4:** Comparison bar chart vs baselines

### Section 7: Case Study (+600 words) **NEW SECTION**
**Add after Evaluation:**
- Real deployment scenario walkthrough
- Example: CS101 course sets policy → student query → decision logged
- Step-by-step execution trace
- Screenshots/logs (anonymized) from actual system run
- Lessons learned from implementation

### Section 8: Discussion (+300 words)
**Current:** Brief key findings
**Expand:**
- Implications for institutions
- Generalization to other domains (healthcare, finance)
- Technical trade-offs made
- When our system is appropriate vs when it isn't

### Section 9: Threats to Validity (+200 words) **NEW SUBSECTION**
**Add to Limitations:**
- Internal validity: evaluation coverage
- External validity: generalization limits
- Construct validity: metric appropriateness

### Section 10: Ethical Considerations (+200 words)
**Current:** Good structure
**Expand:** Real-world ethical dilemmas, power dynamics

### Section 11: Conclusion (+200 words)
**Current:** Good
**Expand:** Future research directions more concretely

## Figures to Create (REPRODUCIBLE)

### Figure 1: System Architecture Diagram
**Tool:** Python + Graphviz / draw.io
**Content:** Three-layer architecture with data flows
**Script:** `scripts/generate_architecture.py`
**Status:** TODO - create from system description

### Figure 2: Policy Conflict Detection Example
**Tool:** Python matplotlib
**Content:** Visualize conflict in policy rules
**Script:** `scripts/plot_conflicts.py`
**Status:** TODO - use real policy data from datasets/

### Figure 3: Performance Results
**Tool:** Python matplotlib/seaborn
**Content:** Latency boxplots, throughput over time
**Script:** `scripts/plot_performance.py`
**Data:** backend/tests/ results (if available), else TODO

### Figure 4: Comparison Table (Visual)
**Tool:** LaTeX table → can be figure
**Content:** Our system vs OPA, AWS IAM, NeMo Guardrails
**Status:** Can add immediately (factual comparison)

## Word Count Allocation (Total +3,800)
- Introduction: +400
- Related Work: +600
- Problem Formulation (NEW): +300
- Architecture: +500
- Implementation: +400
- Evaluation: +800
- Case Study (NEW): +600
- Discussion: +300
- Threats to Validity (NEW): +200
- Ethical: +200
- Conclusion: +200
- Misc (transitions, captions): +300

**Total: +4,800 words → Estimated final: ~6,500 words → ~11 pages**

## References - Already Sufficient
**Current:** 53 entries (GOOD)
**Action:** Verify all are cited, create audit log
**No additional refs needed unless new sections require them**

## Timeline
1. ✅ Audit complete
2. Add Problem Formulation section
3. Expand Related Work with comparison table
4. Expand Evaluation with more metrics
5. Add Case Study section
6. Create architecture diagram script
7. Create performance plots script
8. Expand all other sections per plan
9. Compile and verify 11 pages
10. Generate DOCX
11. Create citation audit

## Risk Mitigation
- **If figures can't be generated:** Use TODO placeholders with exact generation steps
- **If word count exceeds 11 pages:** Tighten prose, reduce redundancy
- **If word count under 11 pages:** Add more evaluation detail, expand case study
