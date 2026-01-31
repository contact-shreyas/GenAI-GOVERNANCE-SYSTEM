#!/usr/bin/env python
"""
Standalone test: Verify policy compiler, enforcement, and ledger logging work.
Runs WITHOUT Docker—uses SQLite in-memory DB for testing.
"""

import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Add backend to path
sys.path.insert(0, "backend")

from models import (
    PolicyFormInput, PolicyJSON, GovernanceContext, DecisionEnum,
    PolicyMetadata, PolicyScope, RoleDefinition, AssessmentPhase,
    ActionsConfig, AllowedAction, ProhibitedAction,
    DisclosureRequirement, LoggingConfig, AIUseLogORM
)
from policy_compiler import compile_policy_from_form
from governance_middleware.enforcement import f
from transparency_ledger import log_to_transparency_ledger, get_student_transparency_logs

# Setup in-memory SQLite
Base = declarative_base()

class Policy(Base):
    __tablename__ = "policies"
    policy_id = Column(String, primary_key=True)
    institution_id = Column(String)
    course_id = Column(String)
    content = Column(JSON)
    version = Column(String)
    created_at = Column(DateTime)
    effective_from = Column(DateTime)
    deprecated_at = Column(DateTime, nullable=True)

class AIUseLog(Base):
    __tablename__ = "ai_use_logs"
    log_id = Column(String, primary_key=True)
    course_id = Column(String)
    actor_id_pseudonym = Column(String)
    action = Column(String)
    assessment_type = Column(String)
    policy_id = Column(String)
    decision = Column(String)
    timestamp = Column(DateTime)
    retention_until = Column(DateTime, nullable=True)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def test_policy_compiler():
    """Test 1: Policy Compilation"""
    print("\n✅ TEST 1: Policy Compiler")
    db = Session()
    
    form = PolicyFormInput(
        course_id="CS101",
        policy_title="CS101 GenAI Policy",
        description="Test policy",
        allowed_actions=["use_genai_brainstorm", "use_genai_code_review"],
        prohibited_actions=["submit_genai_as_own"],
        disclosure_required=True,
        assessment_types=["problem_set"],
        assessment_phases=["drafting", "submission"]
    )
    
    result = compile_policy_from_form(form, "test_inst", "prof_alice", db)
    
    assert result.success, f"Compilation failed: {result.errors}"
    assert result.policy is not None, "Policy not returned"
    assert result.policy.policy_id == "course_CS101_genai_v1.0"
    
    # Check DB
    stored = db.query(Policy).filter(Policy.course_id == "CS101").first()
    assert stored is not None, "Policy not stored in DB"
    
    print(f"  ✓ Policy compiled: {result.policy.policy_id}")
    print(f"  ✓ Stored in DB: {stored.policy_id}")
    db.close()

def test_enforcement_and_logging():
    """Test 2: Enforcement + Logging"""
    print("\n✅ TEST 2: Enforcement & Ledger Logging")
    db = Session()
    
    # Create a policy
    form = PolicyFormInput(
        course_id="CS101",
        policy_title="CS101 GenAI Policy",
        description="Test",
        allowed_actions=["use_genai_brainstorm"],
        prohibited_actions=["submit_genai_as_own"],
        disclosure_required=True,
        assessment_types=["problem_set"],
        assessment_phases=["drafting"]
    )
    compile_policy_from_form(form, "test_inst", "prof_alice", db)
    
    # Fetch policy from DB
    policy_db = db.query(Policy).filter(Policy.course_id == "CS101").first()
    policy = PolicyJSON(**policy_db.content)
    
    # Test enforcement
    context = GovernanceContext(
        course_id="CS101",
        actor_role="student",
        action="use_genai_brainstorm",
        assessment_type="problem_set",
        assessment_phase="drafting",
        actor_id_pseudonym="psud_student1"
    )
    
    decision = f([policy], context, "use_genai_brainstorm")
    assert decision.decision in [DecisionEnum.ALLOW, DecisionEnum.REQUIRE_JUSTIFICATION], \
        f"Unexpected decision: {decision.decision}"
    print(f"  ✓ Decision: {decision.decision.value}")
    
    # Log decision
    log = log_to_transparency_ledger(
        actor_id_pseudonym="psud_student1",
        action="use_genai_brainstorm",
        assessment_type="problem_set",
        policy_id="course_CS101_genai_v1.0",
        decision=decision.decision.value,
        course_id="CS101",
        db=db
    )
    assert log is not None, "Log not created"
    print(f"  ✓ Logged to ledger: {log.log_id}")
    
    # Test student view
    view = get_student_transparency_logs("psud_student1", "CS101", db)
    assert view.summary is not None, "View summary empty"
    assert len(view.aggregates) > 0, "No aggregates"
    print(f"  ✓ Student view summary: {view.summary}")
    print(f"  ✓ Aggregates: {len(view.aggregates)} action(s)")
    
    db.close()

def test_conflict_detection():
    """Test 3: Conflict Detection"""
    print("\n✅ TEST 3: Conflict Detection")
    db = Session()
    
    # Create first policy
    form1 = PolicyFormInput(
        course_id="CS102",
        policy_title="CS102 Policy v1",
        description="First policy",
        allowed_actions=["use_genai_brainstorm"],
        prohibited_actions=[],
        assessment_types=["problem_set"],
        assessment_phases=["drafting"]
    )
    result1 = compile_policy_from_form(form1, "test_inst", "prof_bob", db)
    assert result1.success, "First policy compilation failed"
    print(f"  ✓ First policy created: {result1.policy.policy_id}")
    
    # Try to create second policy for same course (should detect conflict)
    form2 = PolicyFormInput(
        course_id="CS102",
        policy_title="CS102 Policy v2",
        description="Second policy",
        allowed_actions=["use_genai_code_review"],
        prohibited_actions=[],
        assessment_types=["project"],
        assessment_phases=["submission"]
    )
    result2 = compile_policy_from_form(form2, "test_inst", "prof_bob", db)
    assert not result2.success, "Should have detected conflict"
    assert result2.conflicts is not None, "No conflicts returned"
    print(f"  ✓ Conflict detected: {result2.conflicts.get('blocking', [])}")
    print(f"  ✓ Error message: {result2.errors[0]}")
    
    db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("STANDALONE TEST SUITE (No Docker Required)")
    print("=" * 60)
    
    try:
        test_policy_compiler()
        test_enforcement_and_logging()
        test_conflict_detection()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run: docker compose up -d postgres redis --wait")
        print("  2. Run: docker compose run --rm backend alembic upgrade head")
        print("  3. Run: docker compose up -d")
        print("  4. Test API at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
