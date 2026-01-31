# GitHub Upload Script - PowerShell Version
# GenAI Governance System

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "GitHub Upload Script - GenAI Governance System" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $PSScriptRoot

# Check if git is available
$gitExists = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitExists) {
    Write-Host "[ERROR] Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win"
    Write-Host "Or use the web interface method in GITHUB_UPLOAD_GUIDE.md"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/6] Git version:" -ForegroundColor Green
git --version
Write-Host ""

Write-Host "[2/6] Initializing Git repository..." -ForegroundColor Green
if (-not (Test-Path .git)) {
    git init
    Write-Host "✓ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[3/6] Configuring Git..." -ForegroundColor Green
$userName = git config user.name 2>$null
if (-not $userName) {
    $userName = Read-Host "Enter your name"
    git config --global user.name $userName
}

$userEmail = git config user.email 2>$null
if (-not $userEmail) {
    $userEmail = Read-Host "Enter your email"
    git config --global user.email $userEmail
}
Write-Host "✓ Git configured" -ForegroundColor Green
Write-Host ""

Write-Host "[4/6] Adding files to Git..." -ForegroundColor Green
git add .
Write-Host "✓ All files staged" -ForegroundColor Green
Write-Host ""

Write-Host "[5/6] Creating commit..." -ForegroundColor Green
$commitResult = git commit -m "Add: GenAI Governance System - paper + implementation + datasets" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit created successfully" -ForegroundColor Green
} else {
    Write-Host "⊙ Commit may already exist or no changes detected" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[6/6] Setting up remote..." -ForegroundColor Green
git remote remove origin 2>$null
git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git
git branch -M main
Write-Host "✓ Remote configured" -ForegroundColor Green
Write-Host ""

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "READY TO PUSH TO GITHUB!" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Command: git push -u origin main" -ForegroundColor White
Write-Host ""
Write-Host "When prompted for credentials:" -ForegroundColor Yellow
Write-Host "  Username: contact-shreyas" -ForegroundColor White
Write-Host "  Password: [Your GitHub Personal Access Token]" -ForegroundColor White
Write-Host ""
Write-Host "Don't have a token with write access?" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/settings/tokens" -ForegroundColor White
Write-Host "2. Click 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Select scope: [x] repo (full control)" -ForegroundColor White
Write-Host "4. Generate and copy the token" -ForegroundColor White
Write-Host "5. Use it as your password below" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to push to GitHub (or Ctrl+C to cancel)"

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host "✓ SUCCESS! Files uploaded to GitHub" -ForegroundColor Green
    Write-Host "=========================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "View your repository at:" -ForegroundColor White
    Write-Host "https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Paper: /blob/main/paper/main.tex" -ForegroundColor White
    Write-Host "Code: /tree/main/backend" -ForegroundColor White
    Write-Host "Datasets: /tree/main/datasets" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "=========================================================" -ForegroundColor Red
    Write-Host "✗ PUSH FAILED" -ForegroundColor Red
    Write-Host "=========================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Create a new token at https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Make sure the token has 'repo' scope checked" -ForegroundColor White
    Write-Host "3. Use the new token as your password" -ForegroundColor White
    Write-Host "4. Alternative: Use GitHub Desktop (https://desktop.github.com)" -ForegroundColor White
    Write-Host "5. Alternative: Upload via web interface (see GITHUB_UPLOAD_GUIDE.md)" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Read-Host "Press Enter to exit"
