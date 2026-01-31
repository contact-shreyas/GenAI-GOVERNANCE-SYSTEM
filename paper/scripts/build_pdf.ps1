# ============================================================================
# IEEE CONFERENCE PAPER - BUILD AND VERIFICATION SCRIPTS
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "IEEE PAPER BUILD SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$paperDir = "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION\paper"
$distDir = "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION\dist"

# Change to paper directory
Set-Location $paperDir

# ============================================================================
# STEP 1: Clean build artifacts
# ============================================================================
Write-Host "[1/7] Cleaning build artifacts..." -ForegroundColor Yellow
Remove-Item -ErrorAction SilentlyContinue main.aux, main.bbl, main.blg, main.log, main.out, main.toc

# ============================================================================
# STEP 2: First LaTeX pass
# ============================================================================
Write-Host "[2/7] Running pdflatex (pass 1)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex | Out-Null

# ============================================================================
# STEP 3: BibTeX for references
# ============================================================================
Write-Host "[3/7] Processing references with bibtex..." -ForegroundColor Yellow
bibtex main 2>$null | Out-Null

# ============================================================================
# STEP 4: Second LaTeX pass
# ============================================================================
Write-Host "[4/7] Running pdflatex (pass 2)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex | Out-Null

# ============================================================================
# STEP 5: Third LaTeX pass (resolve cross-references)
# ============================================================================
Write-Host "[5/7] Running pdflatex (pass 3 - final)..." -ForegroundColor Yellow
pdflatex -interaction=nonstopmode main.tex | Out-Null

# ============================================================================
# STEP 6: Verify page count
# ============================================================================
Write-Host "[6/7] Verifying page count..." -ForegroundColor Yellow
$pageCount = (pdfinfo main.pdf 2>$null | Select-String "Pages:").ToString().Split(':')[1].Trim()
Write-Host "  Page count: $pageCount" -ForegroundColor White

if ($pageCount -eq "11" -or $pageCount -eq "12") {
    Write-Host "  ✓ Page count OK ($pageCount pages including references)" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Warning: Expected 11 pages, got $pageCount" -ForegroundColor Red
}

# ============================================================================
# STEP 7: Copy to dist folder
# ============================================================================
Write-Host "[7/7] Copying to dist folder..." -ForegroundColor Yellow
Copy-Item main.pdf -Destination "$distDir\paper_IEEE_11pages.pdf" -Force
Write-Host "  ✓ Copied to $distDir\paper_IEEE_11pages.pdf" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BUILD COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Output: $distDir\paper_IEEE_11pages.pdf" -ForegroundColor White
Write-Host "Pages: $pageCount" -ForegroundColor White
Write-Host ""
