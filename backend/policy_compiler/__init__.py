"""
Policy Compiler Module
Converts faculty form input → machine-executable policy JSON
Detects conflicts with existing policies
"""

from models import (
    PolicyFormInput, PolicyJSON, CompileResult, ConflictReport,
    PolicyMetadata, PolicyScope, ActionsConfig, AllowedAction, ProhibitedAction,
    AssessmentPhase, DisclosureRequirement, LoggingConfig, RoleDefinition,
    Policy
)
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session


def compile_policy_from_form(
    form: PolicyFormInput,
    institution_id: str,
    author_id: str,
    db: Session
) -> CompileResult:
    """
    Compile faculty form input to PolicyJSON.
    Validate schema, detect conflicts, and store in DB.
    """
    try:
        # 1. Generate policy ID and version
        policy_id = f"course_{form.course_id}_genai_v1.0"
        version = "1.0"
        now = datetime.utcnow()

        # 2. Build PolicyJSON from form
        metadata = PolicyMetadata(
            title=form.policy_title,
            author_id=author_id,
            description=form.description,
            tags=[]
        )

        roles = [RoleDefinition(role="student", description="Student role")]
        scope = PolicyScope(
            applies_to=["students"],
            assessment_types=form.assessment_types,
            assessment_phases=[AssessmentPhase(p) for p in form.assessment_phases],
            roles=roles,
            course_id=form.course_id
        )

        allowed_actions = [
            AllowedAction(
                action=a,
                description=f"Action: {a}",
                applies_to_roles=["student"],
                applies_to_assessment_types=form.assessment_types,
                applies_to_assessment_phases=[AssessmentPhase(p) for p in form.assessment_phases],
                disclosure_required=form.disclosure_required,
                disclosure_format="inline_comment" if form.disclosure_required else None
            )
            for a in form.allowed_actions
        ]

        prohibited_actions = [
            ProhibitedAction(
                action=a,
                description=f"Prohibited: {a}",
                applies_to_roles=["student"],
                applies_to_assessment_types=form.assessment_types,
                applies_to_assessment_phases=[AssessmentPhase(p) for p in form.assessment_phases]
            )
            for a in form.prohibited_actions
        ]

        actions = ActionsConfig(
            allowed_actions=allowed_actions,
            prohibited_actions=prohibited_actions
        )

        disclosure_requirements = [
            DisclosureRequirement(
                req_id=f"req_{a}",
                trigger_action=a,
                required_disclosure={"format": "inline_comment"}
            )
            for a in form.allowed_actions if form.disclosure_required
        ]

        logging_config = LoggingConfig(default_level=form.logging_level)

        policy = PolicyJSON(
            policy_id=policy_id,
            institution_id=institution_id,
            course_id=form.course_id,
            academic_year="2025-2026",
            created_at=now,
            effective_from=now,
            version=version,
            metadata=metadata,
            scope=scope,
            actions=actions,
            disclosure_requirements=disclosure_requirements,
            logging=logging_config
        )

        # 3. Conflict detection (simple: check existing course policies)
        existing = db.query(Policy).filter(
            Policy.course_id == form.course_id,
            Policy.deprecated_at.is_(None)
        ).all()

        conflicts = []
        for p in existing:
            if p.policy_id != policy.policy_id:
                conflicts.append({
                    "policy_id": p.policy_id,
                    "version": p.version,
                    "reason": "Active policy already exists for this course"
                })

        if conflicts:
            return CompileResult(
                success=False,
                errors=["Course already has an active policy"],
                conflicts={"blocking": conflicts}
            )

        # 4. Store in DB
        db_policy = Policy(
            policy_id=policy.policy_id,
            institution_id=policy.institution_id,
            course_id=policy.course_id,
            content=policy.model_dump(),
            version=policy.version,
            created_at=policy.created_at,
            effective_from=policy.effective_from
        )
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)

        return CompileResult(
            success=True,
            policy=policy,
            errors=[],
            warnings=[]
        )

    except Exception as e:
        db.rollback()
        return CompileResult(
            success=False,
            errors=[f"Compilation failed: {str(e)}"]
        )


def detect_conflicts(
    new_policy: PolicyJSON,
    existing_policies: List[PolicyJSON],
    course_id: str
) -> ConflictReport:
    """
    Detect overlaps, contradictions, and version conflicts.
    """
    blocking = []
    non_blocking = []
    suggestions = []

    for existing in existing_policies:
        # Check for course overlap
        if existing.course_id == course_id:
            blocking.append({
                "policy_id": existing.policy_id,
                "reason": "Course ID overlap",
                "severity": "high"
            })

    if blocking:
        suggestions.append("Deprecate existing policy before creating new one")

    return ConflictReport(
        blocking=blocking,
        non_blocking=non_blocking,
        suggestions=suggestions
    )
