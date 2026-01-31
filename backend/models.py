"""
Implements: Core data models (policy compiler, enforcement, RAG, ledger)

How it satisfies constraints:
- Defines strict Pydantic v2 schemas for policies, governance context,
  decisions, and transparency ledger (no PII, only pseudonyms and metadata).
- Decision outcomes use the required enum {ALLOW, DENY, REQUIRE_JUSTIFICATION}.
- Models include fields per spec: course_id, assessment_type, role,
  allowed/prohibited actions, disclosure requirements, logging, override rules,
  version, and decision trace support.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# POLICY SCHEMA MODELS (Section 2.2.1)
# ============================================================================

class DecisionEnum(str, Enum):
    """Policy decision outcomes."""
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_JUSTIFICATION = "REQUIRE_JUSTIFICATION"


class RoleDefinition(BaseModel):
    """Role within a policy scope."""
    role: str = Field(..., description="Role identifier (e.g., 'student', 'instructor')")
    description: str
    condition: Optional[str] = Field(None, description="Condition to match this role")


class AssessmentPhase(str, Enum):
    """Phases of assessment lifecycle."""
    PLANNING = "planning"
    DRAFTING = "drafting"
    SUBMISSION = "submission"
    PRE_SUBMISSION = "pre_submission"
    POST_SUBMISSION = "post_submission"
    COLLABORATION = "collaboration"


class AllowedAction(BaseModel):
    """Permitted action under policy."""
    action: str = Field(..., description="Action identifier (e.g., 'use_genai_brainstorm')")
    description: str
    applies_to_roles: List[str]
    applies_to_assessment_types: List[str]
    applies_to_assessment_phases: List[AssessmentPhase]
    disclosure_required: bool = False
    disclosure_format: Optional[str] = None  # e.g., "inline_comment"
    logging_level: str = "log_action_only"


class ProhibitedAction(BaseModel):
    """Forbidden action under policy."""
    action: str
    description: str
    applies_to_roles: List[str]
    applies_to_assessment_types: List[str]
    applies_to_assessment_phases: List[AssessmentPhase]
    consequence: str = "violation"  # "violation" or "require_justification"
    logging_level: str = "log_action_and_context"


class ActionsConfig(BaseModel):
    """Allowed and prohibited actions in a policy."""
    allowed_actions: List[AllowedAction]
    prohibited_actions: List[ProhibitedAction]


class DisclosureRequirement(BaseModel):
    """Disclosure requirement tied to an action."""
    req_id: str
    trigger_action: str
    required_disclosure: Dict[str, Any]  # format, template, placement, timing
    consequence_if_missing: str = "none"  # "none", "penalty", "required_before_submission"


class LoggingConfig(BaseModel):
    """Logging configuration for policy."""
    default_level: str = "log_action_only"  # or "log_action_and_context", "log_nothing"
    retention_days: int = 90
    student_visible: bool = True
    aggregation_threshold: int = 2
    pseudonym_rotation: bool = True
    pseudonym_rotation_days: int = 30
    metadata_fields: List[str] = Field(
        default_factory=lambda: ["action", "timestamp", "assessment_type", "policy_version"]
    )
    excluded_fields: List[str] = Field(
        default_factory=lambda: ["content", "student_id", "learning_outcome"]
    )


class OverrideRule(BaseModel):
    """Exception to policy (e.g., disability accommodations)."""
    override_id: str
    description: str
    condition: str  # e.g., "has_approved_accommodation('genai_use')"
    effect: str  # "allow_all_actions", "deny_all_actions"
    requires_disclosure: Optional[str] = None


class PolicyScope(BaseModel):
    """Scope of policy applicability."""
    applies_to: List[str]  # "students", "faculty", etc.
    assessment_types: List[str]  # "problem_set", "exam", "project", "peer_review"
    assessment_phases: List[AssessmentPhase]
    roles: List[RoleDefinition]
    course_id: Optional[str] = None


class PolicyMetadata(BaseModel):
    """Metadata about a policy."""
    title: str
    author_id: str
    description: str
    tags: List[str] = Field(default_factory=list)
    institution_contact: Optional[str] = None


class PolicyJSON(BaseModel):
    """
    Complete policy document schema.
    Immutable once published; new versions are separate documents.
    """
    policy_id: str
    institution_id: str
    course_id: str
    academic_year: str
    created_at: datetime
    effective_from: datetime
    deprecated_at: Optional[datetime] = None
    version: str
    previous_version_id: Optional[str] = None

    metadata: PolicyMetadata
    scope: PolicyScope
    actions: ActionsConfig
    disclosure_requirements: List[DisclosureRequirement]
    logging: LoggingConfig
    override_rules: List[OverrideRule] = Field(default_factory=list)
    conflict_resolution: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# FORM INPUT MODELS (Section 2.2.2)
# ============================================================================

class PolicyFormInput(BaseModel):
    """Form input from faculty for policy authoring."""
    course_id: str
    policy_title: str
    description: str
    allowed_actions: List[str]  # ["use_genai_brainstorm", "use_genai_code_review", ...]
    prohibited_actions: List[str]
    disclosure_required: bool = True
    logging_level: str = "log_action_only"
    assessment_types: List[str] = Field(default_factory=lambda: ["problem_set", "project"])
    assessment_phases: List[str] = Field(
        default_factory=lambda: ["planning", "drafting", "submission"]
    )


class CompileResult(BaseModel):
    """Result of policy compilation."""
    success: bool
    policy: Optional[PolicyJSON] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    conflicts: Optional[Dict[str, Any]] = None


class ConflictReport(BaseModel):
    """Report of detected policy conflicts."""
    blocking: List[Dict[str, Any]] = Field(default_factory=list)
    non_blocking: List[Dict[str, Any]] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


# ============================================================================
# GOVERNANCE & ENFORCEMENT MODELS (Section 2.2.3)
# ============================================================================

class GovernanceContext(BaseModel):
    """Request context for policy decision endpoint."""
    course_id: str
    actor_role: str  # "student", "instructor", "ta"
    action: str  # "use_genai_brainstorm", etc.
    assessment_type: str
    assessment_phase: str
    actor_id_pseudonym: str  # Pseudonym, NOT real student ID


class Obligation(BaseModel):
    """Obligation attached to a decision (e.g., disclosure requirement)."""
    type: str  # "disclosure_required", "justification_required"
    format: Optional[str] = None  # "inline_comment", "email", etc.
    template: Optional[str] = None
    requirement_id: Optional[str] = None


class GovernanceDecision(BaseModel):
    """Output of policy decision endpoint."""
    decision: DecisionEnum
    obligations: List[Obligation] = Field(default_factory=list)
    trace: Dict[str, Any]  # Decision reasoning
    policy_id: Optional[str] = None
    applied_rules: List[str] = Field(default_factory=list)


class ExplainResult(BaseModel):
    """Explanation of policy rule for UI."""
    action: str
    allowed: bool
    explanation: str
    disclosure_required: bool = False
    disclosure_format: Optional[str] = None
    policy_id: Optional[str] = None
    policy_version: Optional[str] = None


# ============================================================================
# TRANSPARENCY LEDGER MODELS (Section 2.2.4)
# ============================================================================

class AIUseLog(BaseModel):
    """Metadata-only log of AI use."""
    log_id: Optional[str] = None
    course_id: str
    actor_id_pseudonym: str
    action: str  # "use_genai_brainstorm", etc.
    assessment_type: str
    policy_id: str
    decision: DecisionEnum
    timestamp: datetime
    retention_until: Optional[datetime] = None


class AggregatedMetrics(BaseModel):
    """Aggregated AI-use metrics for display."""
    action: Optional[str] = None
    assessment_type: Optional[str] = None
    count: int
    last_event_timestamp: datetime
    policy_id: str


class StudentTransparencyView(BaseModel):
    """Student-facing transparency disclosure."""
    summary: str
    aggregates: List[AggregatedMetrics]
    disclosure_instructions: str
    policy_link_template: str
    privacy_commitment: str


class CourseAnalytics(BaseModel):
    """Instructor-facing anonymized analytics."""
    course_id: str
    period: str
    total_unique_students: int
    total_events: int
    by_action: List[Dict[str, Any]]
    policy_active: Optional[PolicyJSON] = None


# ============================================================================
# RAG CO-PILOT MODELS (Section 2.2.5)
# ============================================================================

class PolicyDoc(BaseModel):
    """Policy document chunk for retrieval."""
    doc_id: str
    policy_id: str
    version: str
    section: str
    text: str
    embedding: Optional[List[float]] = None


class Citation(BaseModel):
    """Citation in a RAG answer."""
    quoted_text: str
    source_policy_id: str
    source_section: str
    confidence: float  # 0-1


class VerificationMetrics(BaseModel):
    """Verification scores for RAG answer."""
    citation_correctness: float
    entailment: float
    consistency: float
    overall_score: float


class CopilotAnswer(BaseModel):
    """Answer from verified RAG co-pilot."""
    direct_answer: str  # "Yes", "No", "Yes, with conditions"
    explanation: str
    citations: List[Citation]
    verification: VerificationMetrics
    confidence: str  # "high", "medium", "low"
    uncertainty_caveats: Optional[List[str]] = None
    requires_human_review: bool
    human_contact: str


# ============================================================================
# REQUEST/RESPONSE MODELS FOR API
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime


# ============================================================================
# SQLALCHEMY ORM (Persistence)
# ============================================================================

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid

Base = declarative_base()


class Policy(Base):
    __tablename__ = "policies"

    policy_id = Column(String, primary_key=True)
    institution_id = Column(String, nullable=False)
    course_id = Column(String, nullable=False)
    content = Column(JSONB, nullable=False)  # Full PolicyJSON
    version = Column(String, nullable=False)
    previous_version_id = Column(String, ForeignKey("policies.policy_id"), nullable=True)
    created_at = Column(DateTime, nullable=False)
    effective_from = Column(DateTime, nullable=False)
    deprecated_at = Column(DateTime, nullable=True)


class AIUseLogORM(Base):
    __tablename__ = "ai_use_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(String, nullable=False)
    actor_id_pseudonym = Column(String, nullable=False)
    action = Column(String, nullable=False)
    assessment_type = Column(String, nullable=False)
    policy_id = Column(String, ForeignKey("policies.policy_id"), nullable=False)
    decision = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    retention_until = Column(DateTime, nullable=True)
