"""
Implements: Governance API router exposing POST /api/v1/policy/evaluate

How it satisfies constraints:
- Validates request with Pydantic (GovernanceContext)
- Evaluates policies with decision function and returns trace
- No PII in inputs/outputs (actor_id_pseudonym only)
- Logs decisions to transparency ledger
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..models import (
    GovernanceContext, GovernanceDecision, PolicyJSON,
    PolicyFormInput, CompileResult, StudentTransparencyView, CourseAnalytics
)
from .enforcement import f
from ..db import get_db
from ..transparency_ledger import log_to_transparency_ledger, get_student_transparency_logs, get_course_analytics
from ..policy_compiler import compile_policy_from_form

router = APIRouter()


@router.post("/api/v1/policy/evaluate", response_model=GovernanceDecision)
def evaluate_policy(
    policies: List[PolicyJSON],
    context: GovernanceContext,
    db: Session = Depends(get_db)
):
    if not policies:
        raise HTTPException(status_code=400, detail="No policies provided")
    if not context.action:
        raise HTTPException(status_code=400, detail="No action provided in context")
    
    decision = f(policies, context, context.action)
    
    # Log decision to transparency ledger
    try:
        log_to_transparency_ledger(
            actor_id_pseudonym=context.actor_id_pseudonym,
            action=context.action,
            assessment_type=context.assessment_type,
            policy_id=decision.policy_id or "unknown",
            decision=decision.decision.value,
            course_id=context.course_id,
            db=db
        )
    except Exception as e:
        # Log but don't fail the request
        print(f"Warning: Failed to log decision: {e}")
    
    return decision


# Alias route to match documented API path
@router.post("/api/governance/decide", response_model=GovernanceDecision)
def decide_alias(
    policies: List[PolicyJSON],
    context: GovernanceContext,
    db: Session = Depends(get_db)
):
    if not policies:
        raise HTTPException(status_code=400, detail="No policies provided")
    if not context.action:
        raise HTTPException(status_code=400, detail="No action provided in context")
    
    decision = f(policies, context, context.action)
    
    # Log decision to transparency ledger
    try:
        log_to_transparency_ledger(
            actor_id_pseudonym=context.actor_id_pseudonym,
            action=context.action,
            assessment_type=context.assessment_type,
            policy_id=decision.policy_id or "unknown",
            decision=decision.decision.value,
            course_id=context.course_id,
            db=db
        )
    except Exception as e:
        # Log but don't fail the request
        print(f"Warning: Failed to log decision: {e}")
    
    return decision


@router.post("/api/policies/compile", response_model=CompileResult)
def compile_policy(
    form_data: PolicyFormInput,
    institution_id: str = "default_institution",
    author_id: str = "default_author",
    db: Session = Depends(get_db)
):
    """
    Compile faculty form input to PolicyJSON.
    Validates, detects conflicts, and stores in DB.
    """
    result = compile_policy_from_form(
        form=form_data,
        institution_id=institution_id,
        author_id=author_id,
        db=db
    )
    return result


@router.get("/api/transparency/my-logs/{pseudonym}", response_model=StudentTransparencyView)
def get_my_logs(
    pseudonym: str,
    course_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Fetch aggregated AI-use logs for a student (by pseudonym).
    """
    return get_student_transparency_logs(pseudonym, course_id, db)


@router.get("/api/transparency/course-analytics/{course_id}", response_model=CourseAnalytics)
def get_analytics(
    course_id: str,
    db: Session = Depends(get_db)
):
    """
    Fetch aggregated, anonymized analytics for a course (instructors).
    """
    return get_course_analytics(course_id, db)


@router.post("/api/copilot/ask")
async def ask_copilot(
    question: str,
    course_id: str,
    db: Session = Depends(get_db)
):
    """
    Ask copilot a policy question for a course.
    Returns answer with citations and confidence.
    """
    from ..rag_copilot import ask_policy_question
    
    # In production: fetch from DB; for MVP: use dummy
    policies = []
    
    result = await ask_policy_question(
        question=question,
        course_id=course_id,
        policies=policies
    )
    
    return result.to_dict()
