@echo off
REM GitHub Upload Script for GenAI Governance System
REM This script will help you upload all files to GitHub

echo =========================================================
echo GitHub Upload Script - GenAI Governance System
echo =========================================================
echo.

cd /d "%~dp0"

REM Check if git is available
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Or use Method 1 in GITHUB_UPLOAD_GUIDE.md
    pause
    exit /b 1
)

echo [1/6] Checking Git version...
git --version
echo.

echo [2/6] Initializing Git repository...
if not exist .git (
    git init
    echo Git repository initialized
) else (
    echo Git repository already exists
)
echo.

echo [3/6] Configuring Git (if needed)...
git config user.name >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Enter your name:
    set /p username="Your Name: "
    git config --global user.name "!username!"
)

git config user.email >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Enter your email:
    set /p useremail="Your Email: "
    git config --global user.email "!useremail!"
)
echo Git configured
echo.

echo [4/6] Adding files...
git add .
echo Files staged for commit
echo.

echo [5/6] Creating commit...
git commit -m "Add: GenAI Governance System - paper + implementation + datasets" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Commit created successfully
) else (
    echo Commit may already exist or no changes detected
)
echo.

echo [6/6] Setting up remote and pushing...
git remote remove origin 2>nul
git remote add origin https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM.git
git branch -M main

echo.
echo =========================================================
echo READY TO PUSH!
echo =========================================================
echo.
echo The repository is configured and ready.
echo Now running: git push -u origin main
echo.
echo You will be prompted for credentials:
echo   Username: contact-shreyas
echo   Password: [Use your GitHub Personal Access Token]
echo.
echo If you don't have a token with write access, create one at:
echo https://github.com/settings/tokens
echo   - Click "Generate new token (classic)"
echo   - Select scope: [x] repo
echo   - Copy the token and use it as password
echo.
pause

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================================
    echo SUCCESS! Files uploaded to GitHub
    echo =========================================================
    echo.
    echo View your repository at:
    echo https://github.com/contact-shreyas/GenAI-GOVERNANCE-SYSTEM
    echo.
) else (
    echo.
    echo =========================================================
    echo PUSH FAILED
    echo =========================================================
    echo.
    echo Common solutions:
    echo 1. Create a new token at https://github.com/settings/tokens
    echo 2. Make sure the token has 'repo' scope selected
    echo 3. Use the token as your password when prompted
    echo 4. Or use GitHub Desktop: https://desktop.github.com
    echo.
)

pause
