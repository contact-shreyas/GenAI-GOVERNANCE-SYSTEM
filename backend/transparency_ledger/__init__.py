"""
Transparency Ledger Module
Metadata-only logging and privacy-preserving analytics
"""

from models import AIUseLog, StudentTransparencyView, CourseAnalytics, AIUseLogORM, AggregatedMetrics
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func


def log_to_transparency_ledger(
    actor_id_pseudonym: str,
    action: str,
    assessment_type: str,
    policy_id: str,
    decision: str,
    course_id: str,
    db: Session
) -> AIUseLogORM:
    """
    Append-only log of AI use (metadata only, no PII).
    """
    now = datetime.utcnow()
    retention_until = now + timedelta(days=90)

    log = AIUseLogORM(
        course_id=course_id,
        actor_id_pseudonym=actor_id_pseudonym,
        action=action,
        assessment_type=assessment_type,
        policy_id=policy_id,
        decision=decision,
        timestamp=now,
        retention_until=retention_until
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_student_transparency_logs(
    actor_id_pseudonym: str,
    course_id: Optional[str],
    db: Session
) -> StudentTransparencyView:
    """
    Fetch aggregated, anonymized AI-use logs for student.
    """
    query = db.query(AIUseLogORM).filter(
        AIUseLogORM.actor_id_pseudonym == actor_id_pseudonym
    )
    if course_id:
        query = query.filter(AIUseLogORM.course_id == course_id)

    logs = query.all()

    # Aggregate by action and assessment type
    aggregates = []
    action_groups = {}
    for log in logs:
        key = (log.action, log.assessment_type)
        if key not in action_groups:
            action_groups[key] = {
                "action": log.action,
                "assessment_type": log.assessment_type,
                "count": 0,
                "last_timestamp": log.timestamp,
                "policy_id": log.policy_id
            }
        action_groups[key]["count"] += 1
        if log.timestamp > action_groups[key]["last_timestamp"]:
            action_groups[key]["last_timestamp"] = log.timestamp

    for data in action_groups.values():
        aggregates.append(AggregatedMetrics(
            action=data["action"],
            assessment_type=data["assessment_type"],
            count=data["count"],
            last_event_timestamp=data["last_timestamp"],
            policy_id=data["policy_id"]
        ))

    summary = f"You have {len(logs)} AI-use events logged"
    if logs:
        summary += f" (last event: {logs[-1].timestamp.strftime('%Y-%m-%d')})";

    return StudentTransparencyView(
        summary=summary,
        aggregates=aggregates,
        disclosure_instructions="This log shows when you used AI tools in your coursework. The institution logs metadata only (action, time, policy version)—not content.",
        policy_link_template="/policies/{policy_id}",
        privacy_commitment="We do not store your identity with these logs. Logs are deleted 90 days after creation. You can opt out of logging at any time."
    )


def get_course_analytics(
    course_id: str,
    db: Session
) -> CourseAnalytics:
    """
    Aggregated, anonymized analytics for instructors.
    """
    # Last 7 days
    since = datetime.utcnow() - timedelta(days=7)
    logs = db.query(AIUseLogORM).filter(
        AIUseLogORM.course_id == course_id,
        AIUseLogORM.timestamp >= since
    ).all()

    unique_students = len(set(log.actor_id_pseudonym for log in logs))
    total_events = len(logs)

    # Group by action
    by_action = {}
    for log in logs:
        key = (log.action, log.assessment_type)
        if key not in by_action:
            by_action[key] = {
                "action": log.action,
                "assessment_type": log.assessment_type,
                "unique_students": set(),
                "total_events": 0,
                "last_event": log.timestamp
            }
        by_action[key]["unique_students"].add(log.actor_id_pseudonym)
        by_action[key]["total_events"] += 1
        if log.timestamp > by_action[key]["last_event"]:
            by_action[key]["last_event"] = log.timestamp

    by_action_list = [
        {
            "action": data["action"],
            "assessment_type": data["assessment_type"],
            "unique_students": len(data["unique_students"]),
            "total_events": data["total_events"],
            "last_event": data["last_event"].isoformat()
        }
        for data in by_action.values()
    ]

    return CourseAnalytics(
        course_id=course_id,
        period="last 7 days",
        total_unique_students=unique_students,
        total_events=total_events,
        by_action=by_action_list
    )
