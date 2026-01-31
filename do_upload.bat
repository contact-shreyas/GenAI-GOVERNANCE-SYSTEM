@echo off
REM Upload to GitHub with new PAT token
cd /d "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

REM Check if git is installed
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Git is not installed. Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ======================================
echo GitHub Upload Script
echo ======================================
echo.

REM Initialize git if not already done
if not exist .git (
    echo [1/6] Initializing repository...
    git init
    echo.
)

REM Configure git user (one-time)
echo [2/6] Configuring git user...
git config --global user.name "GenAI Governance" 2>nul
git config --global user.email "governance@example.com" 2>nul
echo.

REM Add all files
echo [3/6] Adding all files...
git add .
echo.

REM Create commit
echo [4/6] Creating commit...
git commit -m "Add: GenAI Governance System - Paper, Code, Datasets" 2>nul
echo.

REM Add remote if not exists
echo [5/6] Setting up remote...
git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git 2>nul
git branch -M main 2>nul
echo.

REM Push to GitHub
echo [6/6] Pushing to GitHub...
echo.
echo When prompted, enter:
echo Username: contact-shreyas
echo Password: [Your new GitHub token]
echo.
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================
    echo SUCCESS! Files uploaded to GitHub
    echo ======================================
    echo.
    echo Repository: https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM
    echo.
) else (
    echo.
    echo Upload failed. Please check your credentials.
    echo.
)

pause
