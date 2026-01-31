# Makefile for IEEE Conference Paper
# Usage: make pdf, make count, make docx, make clean

PAPER = main
BIBFILE = refs
DIST_DIR = ../dist
OUTPUT_NAME = paper_IEEE_9pages

.PHONY: all pdf clean count docx verify help

# Default target
all: pdf

# Compile PDF (full LaTeX build with bibtex)
pdf:
	@echo "==> Compiling LaTeX to PDF..."
	pdflatex $(PAPER).tex
	bibtex $(PAPER)
	pdflatex $(PAPER).tex
	pdflatex $(PAPER).tex
	@echo "==> PDF generated: $(PAPER).pdf"
	@echo "==> Checking page count..."
	@python scripts/count_pages.py $(PAPER).pdf

# Quick compile (no bibtex)
quick:
	@echo "==> Quick compile (no bibtex)..."
	pdflatex $(PAPER).tex
	@python scripts/count_pages.py $(PAPER).pdf

# Count words per section
count:
	@echo "==> Counting words per section..."
	@python scripts/count_words.py $(PAPER).tex

# Generate DOCX from LaTeX
docx: pdf
	@echo "==> Converting PDF to DOCX..."
	@pandoc $(PAPER).tex -o $(PAPER).docx --bibliography=$(BIBFILE).bib --citeproc
	@echo "==> DOCX generated: $(PAPER).docx"

# Verify page count is exactly 9
verify: pdf
	@echo "==> Verifying page count is exactly 9..."
	@python scripts/verify_9pages.py $(PAPER).pdf

# Copy final outputs to dist/
dist: pdf docx
	@echo "==> Copying outputs to $(DIST_DIR)..."
	@mkdir -p $(DIST_DIR)
	@cp $(PAPER).pdf $(DIST_DIR)/$(OUTPUT_NAME).pdf
	@cp $(PAPER).docx $(DIST_DIR)/$(OUTPUT_NAME).docx
	@echo "==> Final outputs in $(DIST_DIR)/"

# Clean auxiliary files
clean:
	@echo "==> Cleaning auxiliary files..."
	rm -f *.aux *.log *.bbl *.blg *.out *.toc *.synctex.gz
	@echo "==> Cleaned."

# Deep clean (including PDF/DOCX)
distclean: clean
	@echo "==> Deep clean (removing PDF/DOCX)..."
	rm -f $(PAPER).pdf $(PAPER).docx
	@echo "==> Deep cleaned."

# Help
help:
	@echo "Available targets:"
	@echo "  make pdf       - Compile LaTeX to PDF (full build with bibtex)"
	@echo "  make quick     - Quick compile (no bibtex)"
	@echo "  make count     - Count words per section"
	@echo "  make docx      - Generate DOCX from LaTeX"
	@echo "  make verify    - Verify page count is exactly 9"
	@echo "  make dist      - Copy final outputs to dist/"
	@echo "  make clean     - Remove auxiliary files"
	@echo "  make distclean - Remove all generated files"
	@echo "  make help      - Show this help message"
