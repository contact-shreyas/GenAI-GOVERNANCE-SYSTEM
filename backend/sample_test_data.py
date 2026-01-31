"""
SAMPLE SYNTHETIC TEST DATA
==========================
100% Fake student data for testing
✅ No real PII
✅ No real content  
✅ Shows data sources in every response
"""

# Sample Test Policies (Can be from public universities or synthetic)
SAMPLE_POLICIES = [
    {
        "policy_id": "CS101_v1.0",
        "course_id": "CS101",
        "title": "Computer Science 101 - AI Policy (Synthetic Test)",
        "source": "synthetic_test",
        "allowed_actions": [
            "brainstorm",
            "code_review"
        ],
        "prohibited_actions": [
            "full_solution_as_own",
            "exam_submission_ai"
        ],
        "disclosure_required": True
    },
    {
        "policy_id": "DATA201_v1.0",
        "course_id": "DATA201",
        "title": "Data Science 201 - GenAI Guidelines (Cornell-inspired Public)",
        "source": "public_policy_cornell",
        "allowed_actions": [
            "data_analysis_ai",
            "visualization_generation",
            "literature_search_ai"
        ],
        "prohibited_actions": [
            "model_training_as_own",
            "research_publication_ai"
        ],
        "disclosure_required": True
    }
]

# Synthetic Test Scenarios (Fake students, fake actions)
SYNTHETIC_TEST_SCENARIOS = [
    # Test Case 1: Brainstorming allowed
    {
        "test_id": "TEST_001",
        "course_id": "CS101",
        "student_pseudonym": "test_student_001",
        "action": "brainstorm",
        "assessment": "assignment",
        "phase": "drafting",
        "expected_decision": "ALLOW",
        "description": "Student brainstorming in drafting phase - SHOULD BE ALLOWED"
    },
    
    # Test Case 2: Full solution banned
    {
        "test_id": "TEST_002",
        "course_id": "CS101",
        "student_pseudonym": "test_student_002",
        "action": "full_solution_as_own",
        "assessment": "exam",
        "phase": "submission",
        "expected_decision": "DENY",
        "description": "Student submitting AI solution as own on exam - SHOULD BE DENIED"
    },
    
    # Test Case 3: Code review allowed
    {
        "test_id": "TEST_003",
        "course_id": "CS101",
        "student_pseudonym": "test_student_003",
        "action": "code_review",
        "assessment": "assignment",
        "phase": "feedback",
        "expected_decision": "ALLOW",
        "description": "Student reviewing code with AI help - SHOULD BE ALLOWED"
    },
    
    # Test Case 4: Data analysis allowed (DATA201)
    {
        "test_id": "TEST_004",
        "course_id": "DATA201",
        "student_pseudonym": "test_student_004",
        "action": "data_analysis_ai",
        "assessment": "project",
        "phase": "analysis",
        "expected_decision": "ALLOW",
        "description": "Data science student using AI for analysis - SHOULD BE ALLOWED"
    },
    
    # Test Case 5: Visualization generation allowed
    {
        "test_id": "TEST_005",
        "course_id": "DATA201",
        "student_pseudonym": "test_student_005",
        "action": "visualization_generation",
        "assessment": "project",
        "phase": "analysis",
        "expected_decision": "ALLOW",
        "description": "AI-generated charts for data project - SHOULD BE ALLOWED"
    }
]

# Sample FAQ Questions for Copilot Testing
SAMPLE_FAQ = [
    {
        "question": "Can I use ChatGPT to brainstorm ideas for my assignment?",
        "course": "CS101",
        "expected_answer": "YES - brainstorming allowed with disclosure",
        "expected_confidence": "98%"
    },
    {
        "question": "Can I submit AI code as my own work?",
        "course": "CS101",
        "expected_answer": "NO - prohibited",
        "expected_confidence": "100%"
    },
    {
        "question": "Do I need to disclose AI use?",
        "course": "CS101",
        "expected_answer": "YES - required by policy",
        "expected_confidence": "99%"
    },
    {
        "question": "Can I use AI to analyze data for my project?",
        "course": "DATA201",
        "expected_answer": "YES - data analysis allowed",
        "expected_confidence": "98%"
    },
    {
        "question": "What counts as disclosure?",
        "course": "CS101",
        "expected_answer": "Inline comment: 'I used [tool] for [purpose]'",
        "expected_confidence": "97%"
    }
]

if __name__ == "__main__":
    import json
    
    print("="*80)
    print("SYNTHETIC TEST DATA (100% Fake - Privacy Safe)")
    print("="*80)
    
    print("\nSAMPLE POLICIES:")
    for policy in SAMPLE_POLICIES:
        print(f"\n📋 {policy['title']}")
        print(f"   Source: {policy['source']}")
        print(f"   Allowed: {', '.join(policy['allowed_actions'])}")
        print(f"   Banned: {', '.join(policy['prohibited_actions'])}")
    
    print("\n" + "="*80)
    print("SYNTHETIC TEST SCENARIOS:")
    for test in SYNTHETIC_TEST_SCENARIOS:
        print(f"\n🧪 {test['test_id']}: {test['description']}")
        print(f"   Course: {test['course_id']}")
        print(f"   Student Pseudonym: {test['student_pseudonym']} (FAKE)")
        print(f"   Action: {test['action']}")
        print(f"   Expected: {test['expected_decision']}")
    
    print("\n" + "="*80)
    print("SAMPLE COPILOT FAQ QUESTIONS:")
    for i, faq in enumerate(SAMPLE_FAQ, 1):
        print(f"\n❓ Q{i}: {faq['question']}")
        print(f"   Course: {faq['course']}")
        print(f"   Expected: {faq['expected_answer']}")
        print(f"   Confidence: {faq['expected_confidence']}")
    
    print("\n" + "="*80)
    print("\n✅ ALL DATA IS SYNTHETIC/PUBLIC - NO REAL PII")
    print("✅ Each response includes data source info")
    print("✅ Ready for MVP testing & future pilot colleges\n")
