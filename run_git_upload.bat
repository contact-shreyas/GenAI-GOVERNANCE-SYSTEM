@echo off
setlocal enabledelayedexpansion

REM Start a completely fresh Python environment to run the upload script
cd /d "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"

REM Use system Python (not venv) to avoid any conflicts
python.exe git_upload.py

REM Keep window open to see results
pause
