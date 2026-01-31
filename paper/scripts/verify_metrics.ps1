# ============================================================================
# PAPER METRICS VERIFICATION SCRIPT
# ============================================================================

$paperDir = "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION\paper"
$texFile = Join-Path $paperDir "main.tex"
$pdfFile = Join-Path $paperDir "main.pdf"
$bibFile = Join-Path $paperDir "refs.bib"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PAPER METRICS VERIFICATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# PAGE COUNT
# ============================================================================
Write-Host "PDF PAGE COUNT:" -ForegroundColor Yellow
if (Test-Path $pdfFile) {
    $pageInfo = pdfinfo $pdfFile 2>$null | Select-String "Pages:"
    if ($pageInfo) {
        $pages = $pageInfo.ToString().Split(':')[1].Trim()
        Write-Host "  $pages pages" -ForegroundColor White
        
        if ($pages -eq "11" -or $pages -eq "12") {
            Write-Host "  ✓ Target achieved (11 pages required)" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Off target ($pages pages, need 11)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  ⚠ PDF not found. Run build_pdf.ps1 first." -ForegroundColor Red
}
Write-Host ""

# ============================================================================
# WORD COUNT
# ============================================================================
Write-Host "WORD COUNT:" -ForegroundColor Yellow
$totalWords = (Get-Content $texFile | Measure-Object -Word).Words
Write-Host "  Total words in .tex file: $totalWords" -ForegroundColor White

# Estimate body text (exclude LaTeX commands)
$bodyText = Get-Content $texFile | Where-Object { $_ -notmatch '^\\' -and $_ -notmatch '^%' }
$bodyWords = ($bodyText | Measure-Object -Word).Words
Write-Host "  Estimated body text: $bodyWords words" -ForegroundColor White
Write-Host ""

# ============================================================================
# REFERENCE COUNT
# ============================================================================
Write-Host "REFERENCES:" -ForegroundColor Yellow
$bibEntries = (Select-String '@(article|inproceedings|book|techreport|phdthesis|misc)' $bibFile).Count
Write-Host "  BibTeX entries: $bibEntries" -ForegroundColor White

if ($bibEntries -ge 50) {
    Write-Host "  ✓ Target achieved (50+ required)" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Below target ($bibEntries entries, need 50+)" -ForegroundColor Red
}

# Count citations in text
$citations = (Select-String '\\cite' $texFile).Count
Write-Host "  Citation commands in text: $citations" -ForegroundColor White
Write-Host ""

# ============================================================================
# TABLES AND FIGURES
# ============================================================================
Write-Host "TABLES & FIGURES:" -ForegroundColor Yellow
$tables = (Select-String '\\begin\{table' $texFile).Count
$figures = (Select-String '\\begin\{figure' $texFile).Count
$algorithms = (Select-String '\\begin\{algorithm' $texFile).Count
$listings = (Select-String '\\begin\{lstlisting' $texFile).Count

Write-Host "  Tables: $tables" -ForegroundColor White
Write-Host "  Figures: $figures" -ForegroundColor White
Write-Host "  Algorithms: $algorithms" -ForegroundColor White
Write-Host "  Code Listings: $listings" -ForegroundColor White
Write-Host ""

# ============================================================================
# SECTIONS
# ============================================================================
Write-Host "SECTIONS:" -ForegroundColor Yellow
$sections = Select-String "\\section" $texFile | ForEach-Object { $_.Line.Trim() }
$sectionCount = $sections.Count
Write-Host "  Total sections: $sectionCount" -ForegroundColor White
Write-Host ""

# ============================================================================
# SUMMARY
# ============================================================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$checks = @(
    @{ Name = "Page Count (11 pages)"; Status = ($pages -eq "11" -or $pages -eq "12") },
    @{ Name = "References (50+)"; Status = ($bibEntries -ge 50) },
    @{ Name = "Citations Present"; Status = ($citations -gt 0) },
    @{ Name = "Tables Present"; Status = ($tables -gt 0) }
)

foreach ($check in $checks) {
    if ($check.Status) {
        Write-Host "  ✓ $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $($check.Name)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
