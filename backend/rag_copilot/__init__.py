"""
RAG Co-Pilot Module
Policy Q&A with verification pipeline
"""
from __future__ import annotations

from typing import Any, Optional


class CopilotResult:
    """Copilot answer with citations and verification."""
    
    def __init__(
        self,
        question: str,
        answer: str,
        citations: list[str],
        confidence: float,
        policy_ids: list[str],
        has_contradiction: bool = False
    ):
        self.question = question
        self.answer = answer
        self.citations = citations
        self.confidence = confidence
        self.policy_ids = policy_ids
        self.has_contradiction = has_contradiction
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer,
            "citations": self.citations,
            "confidence": self.confidence,
            "policy_ids": self.policy_ids,
            "has_contradiction": self.has_contradiction,
            "flag": "⚠️ Low confidence — ask admin" if self.confidence < 0.7 else "✅ High confidence"
        }


def retrieve_policy_text(
    course_id: str,
    policies: list[dict[str, Any]]
) -> dict[str, Any]:
    """Retrieve active policy for course."""
    for policy in policies:
        if policy.get("course_id") == course_id:
            return policy
    return {}


def generate_answer(
    question: str,
    policy_text: dict[str, Any]
) -> tuple[str, list[str], float]:
    """Generate answer from policy (rule-based for MVP)."""
    question_lower = question.lower()
    answer = ""
    citations = []
    confidence = 0.5
    
    allowed = policy_text.get("allowed_actions", [])
    prohibited = policy_text.get("prohibited_actions", [])
    
    if "brainstorm" in question_lower:
        for action in allowed:
            if action.get("action") == "brainstorm":
                answer = f"✅ Yes — Brainstorming is allowed. Disclosure required."
                citations.append(str(action))
                confidence = 0.95
                break
    
    if ("exam" in question_lower or "test" in question_lower) and not answer:
        for action in prohibited:
            if "exam" in action.get("assessment_type", "").lower():
                answer = f"❌ No — AI is banned in exams."
                citations.append(str(action))
                confidence = 0.98
                break
    
    if not answer:
        answer = "The policy doesn't explicitly address this. Ask your instructor."
        confidence = 0.4
    
    return answer, citations, confidence


async def ask_policy_question(
    question: str,
    course_id: Optional[str] = None,
    policies: Optional[list[dict[str, Any]]] = None
) -> CopilotResult:
    """Answer policy question with citations."""
    if not policies:
        policies = []
    
    if not course_id:
        return CopilotResult(
            question=question,
            answer="Course ID required.",
            citations=[],
            confidence=0.0,
            policy_ids=[]
        )
    
    policy = retrieve_policy_text(course_id, policies)
    
    if not policy:
        return CopilotResult(
            question=question,
            answer="No policy found. Contact instructor.",
            citations=[],
            confidence=0.0,
            policy_ids=[]
        )
    
    answer, citations, confidence = generate_answer(question, policy)
    
    return CopilotResult(
        human_contact="ai-governance@institution.edu"
    )
