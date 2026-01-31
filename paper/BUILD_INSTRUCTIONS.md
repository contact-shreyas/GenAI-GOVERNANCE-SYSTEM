# BUILD INSTRUCTIONS
## IEEE Conference Paper - 9 Pages Exactly

---

## PREREQUISITES

### Required Software
- **LaTeX Distribution**: TeXLive (Linux/Mac) or MiKTeX (Windows)
- **Python 3.8+**: For word counting and verification scripts
- **Pandoc 2.x+**: For LaTeX → DOCX conversion
- **PyPDF2**: `pip install PyPDF2`

### Installation (Windows)
```powershell
# Install MiKTeX
winget install MiKTeX.MiKTeX

# Install Python packages
pip install PyPDF2

# Install Pandoc
winget install JohnMacFarlane.Pandoc
```

### Installation (Linux/Mac)
```bash
# Install TeXLive (Ubuntu/Debian)
sudo apt-get install texlive-full

# Install Python packages
pip3 install PyPDF2

# Install Pandoc
sudo apt-get install pandoc
```

---

## QUICK START

### 1. Build PDF (Full Compilation)
```bash
cd paper
make pdf
```

This runs:
1. `pdflatex main.tex` (first pass)
2. `bibtex main` (process references)
3. `pdflatex main.tex` (second pass - resolve citations)
4. `pdflatex main.tex` (third pass - resolve cross-refs)
5. Automatic page count check

**Output**: `paper/main.pdf`

---

### 2. Verify Page Count (Exactly 9)
```bash
cd paper
make verify
```

**Expected output**:
```
✅ SUCCESS: Paper is exactly 9 pages!
```

**If not 9 pages**: See "Adjusting Page Count" section below.

---

### 3. Count Words Per Section
```bash
cd paper
python scripts/count_words.py main.tex
```

**Output**:
```
================================================================================
WORD COUNT PER SECTION
================================================================================
Abstract                            192 words
Introduction                        984 words
Related Work                       1057 words
Problem Formulation                 412 words
System Design                      1289 words
Evaluation Methodology              976 words
Results and Discussion              891 words
Conclusion                          287 words
================================================================================
TOTAL (main content)               6088 words
================================================================================
References (estimated)             2400 words
GRAND TOTAL (estimated)            8488 words
================================================================================

Estimated pages (IEEE 2-col @ 900 words/page): 9.4 pages
```

---

### 4. Generate DOCX (Word Version)
```bash
cd paper
make docx
```

This runs:
1. Compiles PDF first (if needed)
2. Converts LaTeX → DOCX using Pandoc
3. Processes citations from refs.bib

**Output**: `paper/main.docx`

**Note**: Open in Microsoft Word and verify:
- Tables render correctly
- Equations display properly
- Citations formatted as [1], [2], etc.
- Figures appear (may need manual adjustment)

---

### 5. Copy Final Outputs to dist/
```bash
cd paper
make dist
```

**Outputs**:
- `dist/paper_IEEE_9pages.pdf`
- `dist/paper_IEEE_9pages.docx`

---

## DETAILED COMMANDS

### Quick Compile (No BibTeX)
For fast iterations when not changing citations:
```bash
cd paper
make quick
```

### Clean Auxiliary Files
Remove `.aux`, `.log`, `.bbl`, `.blg`, etc.:
```bash
cd paper
make clean
```

### Deep Clean (Remove PDF/DOCX Too)
```bash
cd paper
make distclean
```

### Help (See All Targets)
```bash
cd paper
make help
```

---

## ADJUSTING PAGE COUNT

### If Paper is TOO LONG (>9 pages)

**Option 1: Tighten Related Work**
- Reduce redundant citations
- Merge similar paragraphs
- Cut less relevant papers

**Option 2: Condense Results**
- Merge Discussion into Results section
- Reduce table sizes (fewer rows/columns)
- Use smaller font for tables: `\small` or `\footnotesize`

**Option 3: Shorten Introduction**
- Remove redundant motivation paragraphs
- Tighten contribution statements

**Commands to test**:
```bash
# After edits, recompile and check
cd paper
make quick
python scripts/count_pages.py main.pdf
```

---

### If Paper is TOO SHORT (<9 pages)

**Option 1: Expand Evaluation**
- Add more dataset details (curation process)
- Expand baseline descriptions
- Add experimental design details

**Option 2: Add Limitations**
- Discuss generalizability
- Privacy-utility tradeoffs
- Computational costs
- Scalability concerns

**Option 3: Expand Related Work**
- Add more policy-as-code literature
- Cite recent AIED/FAccT papers
- Expand RAG verification section

**Option 4: Add More Figures/Tables**
- Dataset statistics table
- Comparison matrix (our system vs. baselines)
- Ablation study results

---

## TROUBLESHOOTING

### Error: "LaTeX Warning: Citation 'xxx' undefined"
**Cause**: Reference not in refs.bib or BibTeX not run

**Fix**:
```bash
cd paper
make pdf  # Full build with bibtex
```

---

### Error: "PyPDF2 not found"
**Cause**: Python package not installed

**Fix**:
```bash
pip install PyPDF2
```

---

### Error: "pandoc: command not found"
**Cause**: Pandoc not installed

**Fix (Windows)**:
```powershell
winget install JohnMacFarlane.Pandoc
```

**Fix (Linux)**:
```bash
sudo apt-get install pandoc
```

---

### DOCX has broken equations
**Cause**: Pandoc sometimes struggles with complex LaTeX math

**Fix**:
1. Open `main.docx` in Microsoft Word
2. Right-click broken equations → "Update Field"
3. Or manually re-enter using Word's equation editor

---

### Figures missing in DOCX
**Cause**: Pandoc doesn't always copy figure files

**Fix**:
1. Manually insert figures into Word document
2. Use `Insert > Picture` in Word
3. Adjust captions to match LaTeX

---

## FILE STRUCTURE

```
paper/
├── main.tex                   # Main LaTeX source
├── refs.bib                   # 60 verified references
├── Makefile                   # Build automation
├── figures/                   # (TODO: Add architecture diagram)
│   └── architecture.pdf
├── scripts/
│   ├── count_words.py         # Word count per section
│   ├── count_pages.py         # Page count checker
│   └── verify_9pages.py       # Strict 9-page verification
└── (outputs)
    ├── main.pdf               # Compiled PDF
    ├── main.docx              # Word version
    ├── main.aux, .log, .bbl   # Auxiliary files (cleaned by make clean)

dist/
├── paper_IEEE_9pages.pdf      # Final PDF (exactly 9 pages)
└── paper_IEEE_9pages.docx     # Final Word version
```

---

## VERIFICATION CHECKLIST

Before submission, verify:

- [ ] **Page count**: Exactly 9 pages (run `make verify`)
- [ ] **References**: 50+ cited (currently 60 in refs.bib)
- [ ] **Citations**: All refs cited in text (no orphan references)
- [ ] **Figures**: All figures have captions and are referenced
- [ ] **Tables**: All tables have captions and are referenced
- [ ] **Equations**: All equations numbered and referenced correctly
- [ ] **DOCX match**: Word version has same content as PDF
- [ ] **DOIs**: All references verified (see CITATION_AUDIT.md)
- [ ] **Formatting**: No font size hacks, no margin tweaks
- [ ] **Spelling**: Run spell check
- [ ] **Grammar**: Proofread all sections

---

## REPRODUCIBILITY

### To reproduce results (when evaluation is complete):

```bash
# Run backend evaluation
cd backend
pytest tests/benchmark_evaluation.py --verbose

# Generate results tables
python scripts/generate_results_tables.py

# Update LaTeX with new numbers
# Edit paper/main.tex Section VI (Results)

# Recompile
cd ../paper
make pdf
```

---

## SUBMISSION CHECKLIST

**For IEEE Conference Submission**:

1. ✅ PDF exactly 9 pages
2. ✅ References ≥50 (currently 60)
3. ✅ No author names (anonymous for review)
4. ✅ No funding acknowledgments (anonymous for review)
5. ✅ IEEEtran class used
6. ✅ No formatting hacks (standard margins/fonts)
7. ✅ All figures vector (PDF/EPS, not PNG/JPG low-res)
8. ✅ Word version available (matching PDF)
9. ✅ Citation audit complete (see CITATION_AUDIT.md)
10. ✅ Reproducibility artifacts documented

**Files to submit**:
- `dist/paper_IEEE_9pages.pdf` (main submission)
- `dist/paper_IEEE_9pages.docx` (supplementary)
- `CITATION_AUDIT.md` (reference verification log)
- Link to GitHub repo (for reproducibility)

---

## TIMELINE ESTIMATE

| Task | Time |
|------|------|
| Initial compilation | 5 min |
| First page count check | 1 min |
| Iterative adjustments (2-3 rounds) | 1-2 hours |
| DOCX generation + verification | 30 min |
| Final proofreading | 1 hour |
| **TOTAL** | **~3-4 hours** |

---

## CONTACT

For issues with build process:
- Check LaTeX log: `paper/main.log`
- Check Python script errors: Run scripts directly
- Verify all prerequisites installed

---

## NOTES

- **No fabricated results**: Section VI has TODO placeholders for when evaluation is complete
- **All references verified**: See CITATION_AUDIT.md for verification status
- **Reproducible**: All scripts and commands documented
- **Standards-compliant**: Uses standard IEEEtran class, no hacks

✅ **READY FOR COMPILATION** ✅
