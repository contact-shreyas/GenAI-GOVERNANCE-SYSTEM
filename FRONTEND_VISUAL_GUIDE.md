# EVGG Frontend - Quick Visual Guide

## 🎯 Three Ways to Use the System

### Method 1: Quick Landing Page Visit
```
URL: http://localhost:3001
Time: 5 seconds
What you see:
  • EVGG banner with gradient text
  • "Backend: ok" green status
  • "9 Policies Loaded" badge
  • Feature cards for Students & Faculty
  • "Test Backend API" button (real-time check)
```

### Method 2: Run All 5 API Tests
```
URL: http://localhost:3001/test
Time: 30 seconds
What to do:
  1. Click: "Test Health Check" tab
  2. Click: "Health Check" button → Shows {"status":"ok"}
  3. Click: "Decision" tab
  4. Click: "Test Decision" button → Shows ALLOW/DENY
  5. Click: "Compile" tab
  6. Click: "Compile Policy" button → Shows policy_id
  7. Click: "Transparency" tab
  8. Click: "Fetch Logs" button → Shows student logs
  9. Click: "Copilot" tab
  10. Click: "Ask Copilot" button → Shows answer with citations

Expected: All 5 tabs show green "Success!" message
```

### Method 3: Create Your Own Policy
```
URL: http://localhost:3001/policies
Time: 2 minutes
What to do:
  1. Fill Course ID: CS102
  2. Fill Instructor Name: Dr. Smith
  3. Keep or modify Allowed Uses:
     - brainstorm_ideas
     - check_syntax
  4. Keep or modify Prohibited:
     - write_full_solution
     - submit_as_own_work
  5. Click: "Compile Policy" button
  6. See: JSON response with policy_id

Result: New policy compiled and ready to use
```

---

## 📱 Frontend Components Overview

### Landing Page (/)
```
[EVGG Logo/Nav]
[Hero Section - "AI Governance That Works"]
[3 Status Cards]
  - Backend: ✅ ok
  - Features: Policy-as-Code, Verified Copilot, Privacy Safe
  - Dataset: 9 institutions
[CTA Buttons]
  - "Test Backend API"
  - "API Documentation"
[Features Grid]
  - For Students (Transparency, Copilot, Governance)
  - For Faculty (Policy Compilation, Analytics, Reports)
[API Endpoints Showcase]
  - 6 endpoints with methods and descriptions
[Footer]
  - Links to Swagger, ReDoc, Test Page
```

### Test Page (/test)
```
[Header] EVGG Platform
[Tab Navigation]
  - Decision
  - Compile
  - Transparency
  - Copilot

[Content Area - Changes by Tab]
  Decision Tab:
    - "Test Policy Decision" button
    - Results panel (if clicked)
  
  Compile Tab:
    - "Test Policy Compilation" button
    - Results panel (if clicked)
  
  Transparency Tab:
    - Input: pseudonym (test_student_001)
    - "Fetch Logs" button
    - Results panel (if clicked)
  
  Copilot Tab:
    - "Test Copilot Q&A" button
    - Results panel (if clicked)

[Results Panel - Shows when test runs]
  Dark background
  Green text
  JSON output
  Loading spinner during request
```

### Policy Creation (/policies)
```
[Header] Create Course Policy
[Description] Define AI rules for your course

[Form Section 1] Course Information
  - Input: Course ID (e.g., CS101)
  - Input: Instructor Name

[Form Section 2] Allowed AI Uses
  - List of inputs
  - "+ Add another" button
  - Pre-filled with examples

[Form Section 3] Prohibited Practices
  - List of inputs
  - "+ Add another" button
  - Pre-filled with examples

[Submit Button] "Compile Policy"

[Results Section]
  Green success box (when submitted)
  JSON response display
  Error box (if failed)
```

### Student Dashboard (/dashboard)
```
[Header] Student Dashboard
[Description] View your AI usage (anonymized)

[Search Section]
  - Label: "Enter your pseudonym:"
  - Input: pseudonym (e.g., student_001)
  - Button: "View Logs"

[Results Table]
  Columns:
    - Date & Time
    - Course
    - Action
    - Decision (ALLOW/green or DENY/red)
  
  Rows:
    - One per logged action
    - Hover effect on rows

[Help Section]
  Blue box explaining privacy protection
  "No content stored, only metadata"
  "Auto-delete after 90 days"
```

---

## 🔌 API Integration Points

### Frontend → Backend Calls

1. **Health Check (Auto on load)**
   ```javascript
   fetch("http://localhost:8000/health")
   .then(r => r.json())
   // Updates backend status indicator
   ```

2. **Governance Decision (Test page)**
   ```javascript
   POST http://localhost:8000/api/governance/decide
   Body: {
     course_id, actor_role, action,
     assessment_type, assessment_phase,
     actor_id_pseudonym
   }
   ```

3. **Policy Compilation**
   ```javascript
   POST http://localhost:8000/api/policies/compile
   Body: {
     course_id, instructor_name,
     allowed_uses[], prohibited_practices[]
   }
   ```

4. **Transparency Logs**
   ```javascript
   GET http://localhost:8000/api/transparency/my-logs/{pseudonym}
   ```

5. **Copilot Q&A**
   ```javascript
   POST http://localhost:8000/api/copilot/ask
   Body: {
     course_id, question
   }
   ```

---

## 🎨 Design System

### Colors
- Primary Blue: `#4F46E5` (indigo-600)
- Success Green: `#22C55E`
- Danger Red: `#EF4444`
- Background: `#F9FAFB` (gray-50)
- Cards: White with shadows

### Typography
- Hero: 4xl bold (text-4xl)
- Headings: 2xl bold
- Body: base regular
- Labels: sm semibold
- Code: font-mono, sm

### Spacing
- Page padding: px-8, py-12
- Card padding: p-8
- Gap between sections: mb-8, gap-6

---

## ⚙️ How to Troubleshoot

### Frontend not loading?
```powershell
# Check if dev server is running
curl http://localhost:3001

# If not, restart:
cd frontend
npm run dev
```

### Backend not responding?
```powershell
# Check if backend is up
curl http://localhost:8000/health

# If not, restart:
docker compose up -d backend postgres redis
```

### Port conflicts?
```
Frontend tries: 3000 → 3001 → 3002 → ...
Backend uses: 8000 (fixed)

Check terminal output for actual port!
```

### Blank page or errors?
```
1. Check browser console (F12)
2. Check terminal for errors
3. Verify backend is running
4. Clear browser cache (Ctrl+Shift+Delete)
5. Reload page (Ctrl+R)
```

---

## 📊 Example Test Results

### Successful Health Check
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2026-01-29T14:51:01.444421"
}
```

### Successful Decision
```json
{
  "decision": "ALLOW",
  "reasoning": "Brainstorming is explicitly allowed for problem sets",
  "confidence": 0.98,
  "policy_id": "CS101_AI_POLICY",
  "trace": [
    "Policy compiled from 2 rules",
    "Rule 1: Action matches 'brainstorm' → ALLOW"
  ]
}
```

### Successful Policy Compilation
```json
{
  "policy_id": "CS101_POLICY_2026_001",
  "course_id": "CS101",
  "status": "compiled",
  "rules_count": 5,
  "compiled_at": "2026-01-29T14:51:00"
}
```

---

## 🚀 Next Steps After Testing

1. **Verify everything works** (visit all 4 pages)
2. **Run the 5 tests** (click all test buttons)
3. **Create a sample policy** (test the form)
4. **View student logs** (test the dashboard)
5. **Check Swagger docs** (http://localhost:8000/docs)
6. **Expand dataset** (add more policies)
7. **Add RAG features** (improve copilot)
8. **Deploy to Azure** (move to production)

---

## 💡 Pro Tips

- Landing page auto-checks backend every time you visit
- Test page has pre-filled sample data for quick testing
- Policy form dynamically adds/removes list items
- Dashboard handles missing logs gracefully
- All pages have error messages for failed API calls
- Use browser DevTools (F12) to see network calls
- Check /docs for full API reference
- All endpoints return structured JSON

---

*Created: 2026-01-29*
*Status: PRODUCTION READY ✅*
