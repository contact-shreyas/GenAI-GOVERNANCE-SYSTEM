# ============================================================================
# PAPER AUDIT SCRIPT - IEEE Conference Paper Metrics
# ============================================================================

$paperPath = Split-Path -Parent $PSScriptRoot
$texFile = Join-Path $paperPath "main.tex"
$pdfFile = Join-Path $paperPath "main.pdf"
$bibFile = Join-Path $paperPath "refs.bib"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PAPER AUDIT REPORT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Page count
if (Test-Path $pdfFile) {
    Write-Host "PDF PAGE COUNT:" -ForegroundColor Yellow
    $pageInfo = pdfinfo $pdfFile 2>$null | Select-String "Pages:"
    if ($pageInfo) {
        Write-Host "  $pageInfo"
    } else {
        Write-Host "  (pdfinfo not available, checking PDF manually...)"
        $pdfContent = Get-Content $pdfFile -Raw -ErrorAction SilentlyContinue
        Write-Host "  PDF exists at: $pdfFile"
    }
    Write-Host ""
}

# Word count
Write-Host "WORD COUNT:" -ForegroundColor Yellow
$totalWords = (Get-Content $texFile | Measure-Object -Word).Words
Write-Host "  Total words in .tex file: $totalWords"
Write-Host ""

# Section analysis
Write-Host "SECTIONS:" -ForegroundColor Yellow
$sections = Select-String "\\section" $texFile | ForEach-Object { $_.Line.Trim() }
$sections | ForEach-Object { Write-Host "  $_" }
Write-Host "  Total sections: $($sections.Count)"
Write-Host ""

# Reference count
Write-Host "REFERENCES:" -ForegroundColor Yellow
$bibEntries = (Select-String '@(article|inproceedings|book|techreport|phdthesis|misc)' $bibFile).Count
Write-Host "  BibTeX entries in refs.bib: $bibEntries"
Write-Host ""

# Citations in text
$citations = Select-String '\\cite' $texFile
Write-Host "  Citations in main.tex: $($citations.Count) cite commands"
Write-Host ""

# Tables and figures
$tables = (Select-String '\\begin\{table' $texFile).Count
$figures = (Select-String '\\begin\{figure' $texFile).Count
$algorithms = (Select-String '\\begin\{algorithm' $texFile).Count
Write-Host "FIGURES & TABLES:" -ForegroundColor Yellow
Write-Host "  Tables: $tables"
Write-Host "  Figures: $figures"
Write-Host "  Algorithms: $algorithms"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "END OF AUDIT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
