# GenAI Governance System - Startup Guide

## Status: ✅ SYSTEM RUNNING

Both services are now running in persistent Windows that will NOT close automatically.

---

## Current Running Services

| Service | Port | Status | URL |
|---------|------|--------|-----|
| **Backend API** | 8000 | 🟢 LISTENING | http://localhost:8000 |
| **Frontend UI** | 3000 | 🟢 LISTENING | http://localhost:3000 |
| **API Docs** | 8000 | 🟢 RUNNING | http://localhost:8000/docs |

---

## How to Access

### Frontend Application
**Open in browser:** http://localhost:3000

### Backend API
**API Documentation:** http://localhost:8000/docs
**Health Check:** http://localhost:8000/health
**Base URL:** http://localhost:8000

---

## Important Notes

### ⚠️ DO NOT CLOSE THE WINDOWS!
- Two new PowerShell windows opened automatically
- One runs Backend (FastAPI)
- One runs Frontend (Next.js)
- **If you close these windows, the services STOP**

### Restarting Services
If services crash or you close the windows:

**Option 1: Use the startup script**
```powershell
cd "C:\transfer\GenAI GOVERNANCE LAYER FOR HIGHER EDUCATION"
powershell -ExecutionPolicy Bypass -File RUN_SYSTEM.ps1
```

**Option 2: Manual restart**
```powershell
# Terminal 1 - Backend
cd backend
..\\.venv_new\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend  
cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3000
```

---

## Troubleshooting

### Issue: Port 3000 not responding
**Solution:**
```powershell
# Kill any orphaned processes
taskkill /IM node.exe /F

# Restart frontend
cd frontend
npm run dev -- --hostname 127.0.0.1 --port 3000
```

### Issue: Port 8000 not responding
**Solution:**
```powershell
# Kill any orphaned Python processes
taskkill /IM python.exe /F

# Restart backend
cd backend
..\.venv_new\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Issue: "Cannot connect to localhost"
**Check if services are listening:**
```powershell
netstat -ano | Select-String ":8000|:3000"
```

Should show both ports in LISTENING state.

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `RUN_SYSTEM.ps1` | Start both services (recommended) |
| `RUN_SYSTEM.bat` | Batch file version of launcher |
| `netstat -ano \| Select-String ":8000\|:3000"` | Check if ports listening |
| `taskkill /IM node.exe /F` | Force close Node.js |
| `taskkill /IM python.exe /F` | Force close Python |

---

## What's Running

### Backend (Port 8000)
- **Framework:** FastAPI 0.104
- **Language:** Python 3.11
- **Features:** Policy compilation, enforcement, API endpoints
- **Status:** Running with auto-reload

### Frontend (Port 3000)
- **Framework:** Next.js 14.2
- **Language:** TypeScript/React
- **Features:** Web UI for policy management
- **Status:** Running in development mode

---

## System Files Created

- `RUN_SYSTEM.ps1` - PowerShell startup script
- `RUN_SYSTEM.bat` - Batch startup script
- This guide file

---

**Last Updated:** 2026-01-31  
**Status:** ✅ Both services running and responding  
**Do NOT close the service windows!**
