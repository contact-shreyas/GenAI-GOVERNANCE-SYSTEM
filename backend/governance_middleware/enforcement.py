"""
Implements: Enforcement engine (runtime policy decision function)

How it satisfies constraints:
- Provides f(policies, context, action) -> (decision, obligations, trace)
- Uses required decision types {ALLOW, DENY, REQUIRE_JUSTIFICATION}
- Performs minimal conflict detection (allowed vs prohibited overlap and overrides)
- Returns a detailed evaluation trace for explainability
- Avoids PII; uses actor_id_pseudonym only in traces/log hooks
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime

from pydantic import BaseModel

from ..models import (
    GovernanceContext,
    GovernanceDecision,
    DecisionEnum,
    Obligation,
    PolicyJSON,
)

# Simple precedence: override > prohibited > allowed
PRECEDENCE = ["override", "prohibited", "allowed"]


class Conflict(BaseModel):
    type: str  # "allowed_vs_prohibited" | "override_applies"
    details: Dict[str, Any]


def _matches_context(policy: PolicyJSON, ctx: GovernanceContext) -> bool:
    scope = policy.scope
    # Course must match if provided
    if scope.course_id and scope.course_id != ctx.course_id:
        return False
    # Assessment type
    if ctx.assessment_type not in scope.assessment_types:
        return False
    # Phase
    if ctx.assessment_phase not in [p.value if hasattr(p, "value") else p for p in scope.assessment_phases]:
        return False
    # Role
    if ctx.actor_role not in [r.role for r in scope.roles]:
        return False
    return True


def _policy_effect(policy: PolicyJSON, ctx: GovernanceContext) -> Tuple[str, List[Obligation], Dict[str, Any]]:
    """Return one of "allowed" | "prohibited" | "override" with obligations and rule trace."""
    trace: Dict[str, Any] = {"policy_id": policy.policy_id, "version": policy.version}
    obligations: List[Obligation] = []

    # Overrides
    for orule in (policy.override_rules or []):
        # naive condition check placeholder; replace with real expr engine later
        if orule.condition and orule.effect in ("allow_all_actions", "deny_all_actions"):
            trace.setdefault("overrides_checked", []).append(orule.override_id)
            # Assume overrides apply when condition is present; in production evaluate condition
            trace["override_applied"] = orule.override_id
            if orule.effect == "allow_all_actions":
                if orule.requires_disclosure:
                    obligations.append(Obligation(type="disclosure_required", format=orule.requires_disclosure))
                return "override", obligations, {**trace, "override_effect": "allow_all_actions"}
            else:
                return "override", obligations, {**trace, "override_effect": "deny_all_actions"}

    # Prohibited actions
    for pa in policy.actions.prohibited_actions:
        if pa.action == ctx.action and ctx.actor_role in pa.applies_to_roles and ctx.assessment_type in pa.applies_to_assessment_types:
            trace.setdefault("prohibited_rules_matched", []).append(pa.action)
            return "prohibited", obligations, trace

    # Allowed actions
    for aa in policy.actions.allowed_actions:
        if aa.action == ctx.action and ctx.actor_role in aa.applies_to_roles and ctx.assessment_type in aa.applies_to_assessment_types:
            trace.setdefault("allowed_rules_matched", []).append(aa.action)
            if aa.disclosure_required:
                obligations.append(Obligation(type="disclosure_required", format=aa.disclosure_format))
            return "allowed", obligations, trace

    # No rule matched
    return "none", obligations, {**trace, "no_rule": True}


def detect_conflicts(effects: List[str]) -> List[Conflict]:
    conflicts: List[Conflict] = []
    if "allowed" in effects and "prohibited" in effects:
        conflicts.append(Conflict(type="allowed_vs_prohibited", details={"message": "Same action both allowed and prohibited"}))
    if effects.count("override") > 1:
        conflicts.append(Conflict(type="override_applies", details={"message": "Multiple overrides detected"}))
    return conflicts


def decide(policies: List[PolicyJSON], ctx: GovernanceContext) -> GovernanceDecision:
    matched: List[Dict[str, Any]] = []
    for p in policies:
        if _matches_context(p, ctx):
            eff, obligations, ptrace = _policy_effect(p, ctx)
            matched.append({
                "policy": p,
                "effect": eff,
                "obligations": obligations,
                "trace": ptrace,
            })

    effects = [m["effect"] for m in matched if m["effect"] != "none"]
    conflicts = detect_conflicts(effects)

    # Precedence resolution
    resolved_effect: str = "none"
    applied_policy_id: str | None = None
    applied_rules: List[str] = []
    obligations: List[Obligation] = []

    for tier in PRECEDENCE:
        for m in matched:
            if m["effect"] == tier:
                resolved_effect = tier
                applied_policy_id = m["policy"].policy_id
                obligations = m["obligations"]
                applied_rules.extend(m["trace"].get("allowed_rules_matched", []))
                applied_rules.extend(m["trace"].get("prohibited_rules_matched", []))
                break
        if resolved_effect != "none":
            break

    # Map to DecisionEnum
    decision = DecisionEnum.ALLOW
    if resolved_effect == "none":
        decision = DecisionEnum.REQUIRE_JUSTIFICATION  # default conservative
    elif resolved_effect == "prohibited":
        decision = DecisionEnum.DENY
    elif resolved_effect == "override":
        # Assume override deny takes precedence; if override allows, we've still decided ALLOW via obligations
        # Keep ALLOW unless specific deny override present in trace
        override_effect = None
        for m in matched:
            if m["effect"] == "override":
                override_effect = m["trace"].get("override_effect")
                break
        if override_effect == "deny_all_actions":
            decision = DecisionEnum.DENY
        else:
            decision = DecisionEnum.ALLOW

    # If conflicts present and effect is ALLOW, escalate to REQUIRE_JUSTIFICATION
    if conflicts and decision == DecisionEnum.ALLOW:
        decision = DecisionEnum.REQUIRE_JUSTIFICATION
        obligations.append(Obligation(type="justification_required"))

    trace: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat(),
        "context": ctx.model_dump(),
        "matched_policies": [
            {
                "policy_id": m["policy"].policy_id,
                "version": m["policy"].version,
                "effect": m["effect"],
                "trace": m["trace"],
            }
            for m in matched
        ],
        "conflicts": [c.model_dump() for c in conflicts],
        "resolved_effect": resolved_effect,
    }

    return GovernanceDecision(
        decision=decision,
        obligations=obligations,
        trace=trace,
        policy_id=applied_policy_id,
        applied_rules=applied_rules,
    )


def f(policies: List[PolicyJSON], context: GovernanceContext, action: str) -> GovernanceDecision:
    # Ensure action in context for compatibility with spec signature
    ctx = GovernanceContext(**{**context.model_dump(), "action": action})
    return decide(policies, ctx)
