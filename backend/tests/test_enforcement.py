import pytest
from datetime import datetime

from backend.models import (
    GovernanceContext,
    PolicyJSON,
    PolicyMetadata,
    PolicyScope,
    RoleDefinition,
    ActionsConfig,
    AllowedAction,
    ProhibitedAction,
    DisclosureRequirement,
    LoggingConfig,
)
from backend.governance_middleware.enforcement import decide


def make_policy(policy_id: str) -> PolicyJSON:
    return PolicyJSON(
        policy_id=policy_id,
        institution_id="inst-1",
        course_id="CS101",
        academic_year="2025-2026",
        created_at=datetime.utcnow(),
        effective_from=datetime.utcnow(),
        version="1.0.0",
        metadata=PolicyMetadata(title="Test", author_id="admin", description="desc"),
        scope=PolicyScope(
            applies_to=["students"],
            assessment_types=["project"],
            assessment_phases=["submission"],
            roles=[RoleDefinition(role="student", description="")],
            course_id="CS101",
        ),
        actions=ActionsConfig(
            allowed_actions=[
                AllowedAction(
                    action="use_genai_brainstorm",
                    description="",
                    applies_to_roles=["student"],
                    applies_to_assessment_types=["project"],
                    applies_to_assessment_phases=["submission"],
                    disclosure_required=True,
                    disclosure_format="inline_comment",
                )
            ],
            prohibited_actions=[
                ProhibitedAction(
                    action="use_genai_cheat",
                    description="",
                    applies_to_roles=["student"],
                    applies_to_assessment_types=["project"],
                    applies_to_assessment_phases=["submission"],
                )
            ],
        ),
        disclosure_requirements=[
            DisclosureRequirement(
                req_id="d1",
                trigger_action="use_genai_brainstorm",
                required_disclosure={"format": "inline_comment"},
            )
        ],
        logging=LoggingConfig(),
    )


def test_decide_allow_with_disclosure():
    policy = make_policy("p1")
    ctx = GovernanceContext(
        course_id="CS101",
        actor_role="student",
        action="use_genai_brainstorm",
        assessment_type="project",
        assessment_phase="submission",
        actor_id_pseudonym="stu_x",
    )
    decision = decide([policy], ctx)
    assert decision.decision.value in ("ALLOW", "REQUIRE_JUSTIFICATION")
    assert decision.trace


def test_decide_deny():
    policy = make_policy("p2")
    ctx = GovernanceContext(
        course_id="CS101",
        actor_role="student",
        action="use_genai_cheat",
        assessment_type="project",
        assessment_phase="submission",
        actor_id_pseudonym="stu_x",
    )
    decision = decide([policy], ctx)
    assert decision.decision.value == "DENY"
