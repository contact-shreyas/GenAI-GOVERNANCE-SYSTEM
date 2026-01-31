#!/usr/bin/env python3
"""
🎬 INTERACTIVE DEMO: GenAI Governance System
Shows the complete user journey without database dependencies
"""

from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Optional
import json

# ============================================================================
# CORE DATA MODELS (Simplified versions)
# ============================================================================

class DecisionEnum(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_JUSTIFICATION = "REQUIRE_JUSTIFICATION"

@dataclass
class PolicyRule:
    action: str
    assessment_type: str
    allowed: bool
    disclosure_required: bool = False

@dataclass  
class Policy:
    policy_id: str
    course_id: str
    title: str
    version: str
    rules: List[PolicyRule]
    created_at: datetime

@dataclass
class AIUseLog:
    log_id: str
    course_id: str
    student_pseudonym: str
    action: str
    decision: str
    timestamp: datetime

# ============================================================================
# DEMO DATA STORE (In-Memory)
# ============================================================================

policies_db = {}
logs_db = []
policy_counter = 0

# ============================================================================
# STEP 1: FACULTY CREATES POLICY (Policy Compilation)
# ============================================================================

def demo_faculty_creates_policy():
    """Faculty creates CS101 AI policy through form"""
    print("\n" + "="*80)
    print("📋 STEP 1: FACULTY CREATES POLICY (5 Minutes)")
    print("="*80)
    
    print("\n👩‍🏫 Faculty Dashboard → 'Create New Policy'")
    print("""
    ┌─────────────────────────────────────────────┐
    │ Create Policy: CS101                        │
    ├─────────────────────────────────────────────┤
    │                                             │
    │ Course: CS101                               │
    │ Title: CS101 AI Policy v1.0                 │
    │                                             │
    │ ALLOWED ACTIONS:                            │
    │ ☑ Use GenAI for Brainstorming               │
    │    ├─ Assessment Types: assignment          │
    │    └─ Disclosure: Required (inline comment) │
    │                                             │
    │ ☑ Use GenAI for Code Review                 │
    │    ├─ Assessment Types: assignment          │
    │    └─ Disclosure: Required                  │
    │                                             │
    │ PROHIBITED ACTIONS:                         │
    │ ☒ Submit GenAI Output As Own Work           │
    │    └─ Applies to: exam, assignment          │
    │                                             │
    │ [Validate] → ✅ No conflicts detected       │
    │ [Save Policy v1.0]                          │
    │                                             │
    └─────────────────────────────────────────────┘
    """)
    
    # Create policy
    rules = [
        PolicyRule("use_genai_brainstorm", "assignment", True, True),
        PolicyRule("use_genai_code_review", "assignment", True, True),
        PolicyRule("submit_genai_output_as_own", "exam", False, False),
        PolicyRule("submit_genai_output_as_own", "assignment", False, False),
    ]
    
    policy = Policy(
        policy_id="CS101_v1.0",
        course_id="CS101",
        title="CS101 AI Policy v1.0",
        version="1.0",
        rules=rules,
        created_at=datetime.now()
    )
    
    policies_db[policy.policy_id] = policy
    
    print("\n✅ BACKEND RESPONSE:")
    print(json.dumps({
        "success": True,
        "policy_id": policy.policy_id,
        "course_id": policy.course_id,
        "title": policy.title,
        "rules_count": len(rules),
        "conflicts_detected": 0,
        "created_at": policy.created_at.isoformat(),
        "status": "Policy saved and active"
    }, indent=2))
    
    return policy

# ============================================================================
# STEP 2: STUDENT ASKS COPILOT (Verified Q&A)
# ============================================================================

def demo_student_asks_copilot(policy: Policy):
    """Student asks copilot if brainstorming is allowed"""
    print("\n" + "="*80)
    print("🤖 STEP 2: STUDENT ASKS COPILOT (Instant Answer with Proof)")
    print("="*80)
    
    print("\n👨‍🎓 Student Chat Interface:")
    print("""
    ┌──────────────────────────────────────────────────┐
    │ CS101 AI Policy Helper                           │
    ├──────────────────────────────────────────────────┤
    │                                                  │
    │ You: "Sir, can I use ChatGPT for brainstorming   │
    │      my assignment ideas?"                       │
    │                                                  │
    │ 🤖 System (Retrieving policy...)                │
    │                                                  │
    └──────────────────────────────────────────────────┘
    """)
    
    # Find matching rule
    matching_rule = None
    for rule in policy.rules:
        if rule.action == "use_genai_brainstorm" and rule.assessment_type == "assignment":
            matching_rule = rule
            break
    
    if matching_rule and matching_rule.allowed:
        response = {
            "decision": "ALLOW",
            "answer": "✅ YES - You can use ChatGPT for brainstorming your assignment ideas",
            "policy_quote": "Use GenAI for Brainstorming in assignments is allowed during planning phase",
            "disclosure_required": matching_rule.disclosure_required,
            "disclosure_template": "I used ChatGPT to brainstorm ideas for this assignment.",
            "confidence_score": "98%",
            "policy_version": policy.version,
            "policy_id": policy.policy_id,
            "verification": {
                "rule_matched": True,
                "policy_active": True,
                "no_contradictions": True
            }
        }
    
    print("\n✅ COPILOT RESPONSE:")
    print(json.dumps(response, indent=2))
    
    print("\n📄 Additional Info:")
    print(f"  • Citation: Policy {policy.policy_id} (Active)")
    print(f"  • Verification: ✓ Rule exists ✓ No conflicts ✓ Disclosure required")
    print(f"  • Human review needed: No (High confidence)")
    
    return response

# ============================================================================
# STEP 3: STUDENT SUBMITS WORK → AUTO CHECK & LOG
# ============================================================================

def demo_governance_decision(policy: Policy):
    """Student submits assignment → backend auto-checks and logs"""
    print("\n" + "="*80)
    print("✍️  STEP 3: STUDENT SUBMITS WORK → AUTO-CHECK & LOG")
    print("="*80)
    
    print("\n📤 Student Submission Form:")
    print("""
    ┌─────────────────────────────────────────┐
    │ Assignment Submission                   │
    ├─────────────────────────────────────────┤
    │ Course: CS101                           │
    │ Assignment: Problem Set 1               │
    │ Used GenAI: Yes                         │
    │ How: Brainstorming ideas                │
    │ Disclosure: "I used ChatGPT to          │
    │ brainstorm ideas for Q1-Q3"             │
    │                                         │
    │ [Submit]                                │
    └─────────────────────────────────────────┘
    """)
    
    # Simulate governance decision
    print("\n⚙️  BACKEND GOVERNANCE DECISION ENGINE:")
    print("""
    1. Extract context:
       - Course: CS101 ✓
       - Action: use_genai_brainstorm ✓
       - Assessment: assignment ✓
       - Role: student ✓
       - Disclosure provided: Yes ✓
    
    2. Match against policy CS101_v1.0:
       - Find rule: "use_genai_brainstorm + assignment" ✓
       - Allowed: YES ✓
       - Obligations: disclosure_required ✓
    
    3. Decision: ALLOW ✓
    
    4. Log to transparency ledger:
       - Pseudonym: hash(student_id) 
       - Action: use_genai_brainstorm
       - Assessment: assignment
       - Timestamp: now
       - Policy: CS101_v1.0
    """)
    
    decision_response = {
        "decision": "ALLOW",
        "obligations": [
            {
                "type": "disclosure_required",
                "format": "inline_comment",
                "requirement": "Student has provided required disclosure"
            }
        ],
        "trace": {
            "steps": [
                "Checked policy CS101_v1.0",
                "Matched rule: use_genai_brainstorm",
                "Assessment type matches: assignment ✓",
                "Disclosure check: provided ✓"
            ],
            "matched_rules": ["use_genai_brainstorm"],
            "conflicts": []
        },
        "policy_id": policy.policy_id,
        "log_entry_created": True
    }
    
    # Log the decision
    log_entry = AIUseLog(
        log_id=f"LOG-{len(logs_db)+1}",
        course_id="CS101",
        student_pseudonym="student_xyz_hash_123",
        action="use_genai_brainstorm",
        decision="ALLOW",
        timestamp=datetime.now()
    )
    logs_db.append(log_entry)
    
    print("\n✅ SUBMISSION ACCEPTED:")
    print(json.dumps(decision_response, indent=2))
    print(f"\n✓ Logged to transparency ledger (Event ID: {log_entry.log_id})")
    
    return decision_response, log_entry

# ============================================================================
# STEP 4: STUDENT VIEWS THEIR PRIVATE LOG
# ============================================================================

def demo_student_views_logs(pseudonym: str):
    """Student checks their private AI-use record"""
    print("\n" + "="*80)
    print("👁️  STEP 4: STUDENT VIEWS THEIR AI-USE RECORD (PRIVACY SAFE)")
    print("="*80)
    
    print("\n👨‍🎓 Student Dashboard → 'My AI Use Record':")
    
    # Find logs for this pseudonym
    student_logs = [log for log in logs_db if log.student_pseudonym == pseudonym]
    
    print(f"""
    ┌──────────────────────────────────────────────────┐
    │ My AI Use Record (CS101)                         │
    ├──────────────────────────────────────────────────┤
    │                                                  │
    │ Summary:                                         │
    │ • Total events: {len(student_logs)}                                   │
    │ • Status: ✅ All compliant                       │
    │                                                  │
    │ Event Log:                                       │
    """)
    
    for i, log in enumerate(student_logs, 1):
        status_icon = "✓" if log.decision == "ALLOW" else "✗"
        print(f"""    │ {i}. {status_icon} {log.action}                          │
    │    Date: {log.timestamp.strftime('%Y-%m-%d %H:%M')}                   │
    │    Course: {log.course_id}                              │
    │    Decision: {log.decision}                            │
    │                                                  │""")
    
    print("""    │                                                  │
    │ Privacy Guarantee:                               │
    │ ✓ No personal data stored (no name, roll no)     │
    │ ✓ No assignment content stored                   │
    │ ✓ No AI tool output stored                       │
    │ ✓ Logs auto-delete after 90 days                 │
    │ ✓ Pseudonym rotates every 30 days                │
    │                                                  │
    │ [View Policy] [Ask Question] [Download Report]  │
    │                                                  │
    └──────────────────────────────────────────────────┘
    """)
    
    student_view = {
        "student_pseudonym": pseudonym,
        "course_id": "CS101",
        "summary": f"You have {len(student_logs)} AI-use events logged",
        "status": "✅ All compliant",
        "events": [asdict(log) for log in student_logs],
        "privacy_note": "No PII stored. Metadata only. Auto-delete after 90 days.",
        "last_updated": datetime.now().isoformat()
    }
    
    print("\n✅ API RESPONSE (/api/transparency/my-logs/{pseudonym}):")
    print(json.dumps(student_view, indent=2, default=str))

# ============================================================================
# STEP 5: ADMIN VIEWS COMPLIANCE ANALYTICS
# ============================================================================

def demo_admin_analytics():
    """Admin checks course compliance dashboard"""
    print("\n" + "="*80)
    print("📊 STEP 5: ADMIN VIEWS COMPLIANCE ANALYTICS (PROOF WITHOUT SPYING)")
    print("="*80)
    
    print("\n👩‍💼 Admin Dashboard → 'CS101 Compliance Report':")
    print("""
    ┌───────────────────────────────────────────────────────┐
    │ CS101 GenAI Policy Compliance Report                  │
    ├───────────────────────────────────────────────────────┤
    │                                                       │
    │ Policy: CS101_v1.0 (Active since 2026-01-20)         │
    │                                                       │
    │ 📈 Aggregate Statistics:                              │
    │                                                       │
    │ Unique Students: 150                                  │
    │ AI Use Events: 87 (58%)                               │
    │ No AI Use: 63 (42%)                                   │
    │                                                       │
    │ Compliance Breakdown:                                 │
    │ ✅ Allowed & Disclosed: 85 (98%)                      │
    │ ⚠️  Allowed but No Disclosure: 2 (2%)                 │
    │ ❌ Violations: 0 (0%)                                 │
    │                                                       │
    │ Disclosure Format:                                    │
    │ • Inline comments: 82 (96%)                           │
    │ • Separate document: 3 (4%)                           │
    │                                                       │
    │ Top Actions:                                          │
    │ 1. brainstorming: 52 events                           │
    │ 2. code_review: 25 events                             │
    │ 3. others: 10 events                                  │
    │                                                       │
    │ Audit Status: ✅ READY FOR COMPLIANCE REPORT          │
    │                                                       │
    │ [Export CSV] [View Details] [Drill Down]              │
    │                                                       │
    └───────────────────────────────────────────────────────┘
    """)
    
    analytics = {
        "course_id": "CS101",
        "policy_id": "CS101_v1.0",
        "reporting_period": "2026-01-20 to 2026-01-29",
        "aggregate_stats": {
            "unique_students": 150,
            "ai_use_events": 87,
            "compliance_rate": "98%",
            "violations": 0
        },
        "breakdown": {
            "allowed_and_disclosed": 85,
            "allowed_without_disclosure": 2,
            "violations": 0
        },
        "top_actions": {
            "brainstorming": 52,
            "code_review": 25,
            "other": 10
        },
        "audit_ready": True,
        "generated_at": datetime.now().isoformat()
    }
    
    print("\n✅ API RESPONSE (/api/transparency/course-analytics/CS101):")
    print(json.dumps(analytics, indent=2, default=str))
    
    print("\n🎯 Key Insight:")
    print("  → Admin has compliance proof WITHOUT seeing any student names,")
    print("    assignment content, or AI tool outputs.")
    print("  → Audit-ready metrics for institutional oversight.")

# ============================================================================
# QUICK TEST: Try different scenarios
# ============================================================================

def demo_denied_scenario():
    """Show what happens when action is prohibited"""
    print("\n" + "="*80)
    print("❌ BONUS: PROHIBITED ACTION SCENARIO")
    print("="*80)
    
    print("\n❓ Student asks: 'Can I submit ChatGPT's answer as my own on the exam?'")
    print("""
    ⚙️  Backend Governance Decision:
    
    1. Extract context:
       - Course: CS101 ✓
       - Action: submit_genai_output_as_own
       - Assessment: exam
    
    2. Match against policy CS101_v1.0:
       - Rule found: "submit_genai_output_as_own + exam"
       - Allowed: NO ✗
       - Status: PROHIBITED
    """)
    
    print("\n❌ RESPONSE:")
    denial = {
        "decision": "DENY",
        "reason": "This action violates CS101 Academic Integrity Policy",
        "explanation": "Submitting AI-generated content as your own work is prohibited on exams",
        "policy_quote": "Submit GenAI Output As Own Work is prohibited for exams",
        "obligations": [
            {
                "type": "contact_instructor",
                "message": "Contact Dr. Sharma before submitting AI-assisted work"
            }
        ],
        "escalation": "This event will be logged and flagged for instructor review",
        "policy_id": "CS101_v1.0"
    }
    print(json.dumps(denial, indent=2))
    
    print("\n📝 What gets logged:")
    print("  • Pseudonym (not name)")
    print("  • Action attempted (not assignment content)")
    print("  • Decision (not transcript of conversation)")
    print("  • Timestamp")
    print("  ✓ Privacy maintained even for violations")

# ============================================================================
# RUN COMPLETE DEMO
# ============================================================================

def run_complete_demo():
    """Run the full interactive demo"""
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║                                                                        ║
    ║    🎬 INTERACTIVE DEMO: GenAI Governance System                       ║
    ║    College AI Policy Enforcement + Transparency + Privacy             ║
    ║                                                                        ║
    ║    Real-time walkthrough of: Faculty → Students → Admin               ║
    ║    Shows: Policy Creation → Enforcement → Logging → Analytics         ║
    ║                                                                        ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run all demo steps
    policy = demo_faculty_creates_policy()
    input("\n⏭️  Press ENTER to continue to Step 2 (Student asks Copilot)...")
    
    copilot_response = demo_student_asks_copilot(policy)
    input("\n⏭️  Press ENTER to continue to Step 3 (Student submits work)...")
    
    decision, log_entry = demo_governance_decision(policy)
    input("\n⏭️  Press ENTER to continue to Step 4 (Student views logs)...")
    
    demo_student_views_logs("student_xyz_hash_123")
    input("\n⏭️  Press ENTER to continue to Step 5 (Admin views analytics)...")
    
    demo_admin_analytics()
    input("\n⏭️  Press ENTER to see bonus: Denied action scenario...")
    
    demo_denied_scenario()
    
    # Summary
    print("\n" + "="*80)
    print("🎯 DEMO COMPLETE - KEY TAKEAWAYS")
    print("="*80)
    
    print("""
    ✅ What Works:
    
    1. Policy Compilation (Faculty)
       → Form → JSON → DB (5 mins)
       → Conflict detection automatic
       → Version control built-in
    
    2. Verified Copilot (Students)
       → Policy Q&A with citations
       → Confidence scores
       → Human review flags
    
    3. Auto-Enforcement (System)
       → Decisions in <100ms
       → Obligations tracked
       → Reasoning transparent
    
    4. Privacy-Safe Logging (Students + Admins)
       → Pseudonyms only (not names)
       → Metadata only (not content)
       → Auto-delete after 90 days
       → Student sees own logs
       → Admin sees aggregates
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🎯 Why This Is Novel:
    
    ❌ Competitors (Turnitin, Canvas, ChatGPT Edu):
       • Only plagiarism detection
       • No governance enforcement
       • No student transparency
       • Content scanning (privacy issue)
    
    ✅ Our System:
       • Policy-as-code (executable, not advisory)
       • Verified answers (proof-backed)
       • Transparency dashboard (students see logs)
       • Privacy-first (pseudonyms + metadata only)
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    💰 Market Opportunity:
       • 20,000+ universities globally
       • $10K - 50K per institution per year
       • $5M+ ARR at 500 college adoption
    
    📅 Timeline:
       • Week 2: ✅ Policy compiler + enforcement + ledger (DONE)
       • Week 3: Verified copilot
       • Week 4: Auth + analytics + demo
       • Month 2: Mobile app + advanced features
    """)
    
    print("\n" + "="*80)
    print("🚀 System Architecture (Summary)")
    print("="*80)
    print("""
    Frontend (Next.js):
    ├─ /policies/create     → Faculty policy form
    ├─ /copilot             → Student Q&A chat
    ├─ /transparency        → Student log dashboard
    └─ /admin/analytics     → Compliance reports
    
    Backend (FastAPI):
    ├─ POST /api/policies/compile     → Policy JSON + validation
    ├─ POST /api/governance/decide    → ALLOW/DENY + log
    ├─ POST /api/governance/explain   → Human-readable answer
    ├─ GET /api/transparency/my-logs  → Student's own logs
    ├─ GET /api/transparency/course-analytics → Admin stats
    └─ POST /api/copilot/ask          → Verified Q&A
    
    Database (Postgres):
    ├─ Policies (JSON + versioning)
    ├─ AI Use Logs (pseudonym + metadata)
    └─ Compliance Metrics (aggregates)
    """)

if __name__ == "__main__":
    run_complete_demo()
