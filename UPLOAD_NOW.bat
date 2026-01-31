@echo off
setlocal enabledelayedexpansion

cd /d "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

echo ========================================
echo GenAI Governance System - GitHub Upload
echo ========================================
echo.

echo [1/8] Initializing repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo Git not found or error occurred
    pause
    exit /b 1
)
echo.

echo [2/8] Configuring user...
git config user.name "contact-shreyas"
git config user.email "governance@example.com"
echo.

echo [3/8] Adding files...
git add .
echo.

echo [4/8] Creating commit...
git commit -m "Add: GenAI Governance System - Paper, Code, Datasets, Tests"
echo.

echo [5/8] Adding remote...
git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git
echo.

echo [6/8] Setting main branch...
git branch -M main
echo.

echo [7/8] Pushing to GitHub...
echo When prompted, use:
echo   Username: contact-shreyas
echo   Password: [your PAT token]
echo.

git push -u origin main

echo.
echo [8/8] Done!
echo.
echo ========================================
echo https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM
echo ========================================
echo.

pause
