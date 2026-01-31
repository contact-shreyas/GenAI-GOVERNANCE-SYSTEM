"""
DATA PROVENANCE SYSTEM
=====================
Ensures every API response shows:
✅ Where data comes from (Public/Synthetic/Real with Consent)
✅ What personal data is stored (NONE for synthetic)
✅ Privacy guarantees (No PII, no content)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class DataSourceType(str, Enum):
    """Where data originates from"""
    PUBLIC_POLICY = "public_university_policy"  # Cornell, Stanford PDFs
    SYNTHETIC_TEST = "synthetic_test_scenario"  # Fake student + action
    PILOT_REAL_COURSES = "pilot_real_courses_synthetic_students"  # Month 2 (optional)
    PRODUCTION = "production_real_students_opted_in"  # Future with consent

class PrivacyStatus(str, Enum):
    """Privacy guarantees"""
    ZERO_PII = "zero_pii"  # No names, emails, roll nos
    METADATA_ONLY = "metadata_only"  # Action + decision + timestamp
    CONTENT_FREE = "content_free"  # No assignment text stored

@dataclass
class DataProvenance:
    """Metadata about where data comes from"""
    source_type: DataSourceType
    source_name: str  # "Cornell Policy 2025", "Synthetic Test 001"
    real_pii_stored: bool = False
    real_content_stored: bool = False
    privacy_status: PrivacyStatus = PrivacyStatus.ZERO_PII
    student_consent: bool = False
    data_retention_days: int = 90
    
    def to_dict(self):
        return {
            "source_type": self.source_type.value,
            "source_name": self.source_name,
            "real_pii_stored": self.real_pii_stored,
            "real_content_stored": self.real_content_stored,
            "privacy_status": self.privacy_status.value,
            "student_consent": self.student_consent,
            "data_retention_days": self.data_retention_days,
            "privacy_summary": self._privacy_summary()
        }
    
    def _privacy_summary(self) -> str:
        """Human-readable privacy status"""
        if not self.real_pii_stored and not self.real_content_stored:
            return "✅ 100% Safe - No real PII, no content"
        elif self.student_consent:
            return "✅ Consented - Student opted-in to tracking"
        else:
            return "⚠️ Review needed"

# ============================================================================
# POLICY METADATA (Shows Source for Every Decision)
# ============================================================================

@dataclass
class PolicyMetadata:
    """Every policy includes provenance info"""
    policy_id: str
    course_id: str
    
    # Source of this policy
    source_dataset: str  # "cornell_public_2025" or "synthetic_cs101_test"
    is_public_policy: bool  # True = from university website
    is_synthetic: bool  # True = test data
    
    # Privacy info
    data_provenance: DataProvenance
    
    def to_dict(self):
        return {
            "policy_id": self.policy_id,
            "source_dataset": self.source_dataset,
            "is_public_policy": self.is_public_policy,
            "is_synthetic": self.is_synthetic,
            "provenance": self.data_provenance.to_dict()
        }

# ============================================================================
# API RESPONSE WITH DATA TRANSPARENCY
# ============================================================================

@dataclass
class GovernanceDecisionWithProvenance:
    """Decision + explicit data source info"""
    decision: str  # ALLOW, DENY, REQUIRE_JUSTIFICATION
    policy_id: str
    
    # WHAT GETS LOGGED
    log_created: bool
    log_pseudonym: str  # "test_001" (never real name)
    log_content: str  # "metadata_only: action+decision+timestamp"
    
    # WHERE THIS DATA COMES FROM
    data_source: DataProvenance
    
    # WHAT TRANSPARENCY TO SHOW USER
    transparency_message: str
    
    def to_api_response(self):
        """Format for API response"""
        return {
            "decision": self.decision,
            "policy_id": self.policy_id,
            
            # CORE DECISION INFO
            "reasoning": "Rule matched: brainstorm_allowed_assignment",
            
            # DATA TRANSPARENCY (KEY!)
            "data_source": self.data_source.to_dict(),
            "log_status": {
                "created": self.log_created,
                "student_pseudonym": self.log_pseudonym,
                "content_logged": self.log_content,
                "pii_logged": "ZERO"
            },
            
            # USER-FACING MESSAGE
            "privacy_note": self.transparency_message
        }

# ============================================================================
# SAMPLE DATA SOURCES
# ============================================================================

# Real World Example 1: PUBLIC POLICY
CORNELL_POLICY_SYNTHETIC_TEST = DataProvenance(
    source_type=DataSourceType.PUBLIC_POLICY,
    source_name="Cornell University GenAI Policy 2025 (Public PDF)",
    real_pii_stored=False,
    real_content_stored=False,
    privacy_status=PrivacyStatus.ZERO_PII,
    student_consent=False,  # No student involved - just policy
    data_retention_days=999999  # Policy stays forever
)

# Real World Example 2: SYNTHETIC TEST
SYNTHETIC_TEST_SCENARIO = DataProvenance(
    source_type=DataSourceType.SYNTHETIC_TEST,
    source_name="Synthetic Test Student #001 (Fake Data)",
    real_pii_stored=False,
    real_content_stored=False,
    privacy_status=PrivacyStatus.METADATA_ONLY,
    student_consent=False,  # Test data, no consent needed
    data_retention_days=90
)

# Real World Example 3: PILOT (FUTURE - Month 2)
PILOT_REAL_COURSE_SYNTHETIC_STUDENT = DataProvenance(
    source_type=DataSourceType.PILOT_REAL_COURSES,
    source_name="IIT Delhi CS101 (Real Course) + Synthetic Student",
    real_pii_stored=False,
    real_content_stored=False,
    privacy_status=PrivacyStatus.METADATA_ONLY,
    student_consent=False,  # Real course, but fake student ID
    data_retention_days=90
)

# ============================================================================
# EXAMPLE API RESPONSES (WITH DATA SOURCES)
# ============================================================================

def example_synthetic_test_response():
    """What API returns for synthetic test"""
    decision = GovernanceDecisionWithProvenance(
        decision="ALLOW",
        policy_id="CS101_v1.0",
        log_created=True,
        log_pseudonym="test_student_001",
        log_content="metadata_only: action, decision, timestamp",
        data_source=SYNTHETIC_TEST_SCENARIO,
        transparency_message="✅ Test data only - No real students involved"
    )
    return decision.to_api_response()

def example_public_policy_response():
    """What API returns for public policy test"""
    decision = GovernanceDecisionWithProvenance(
        decision="ALLOW",
        policy_id="Cornell_CS101_Public",
        log_created=False,  # No log for policy-only test
        log_pseudonym="N/A",
        log_content="N/A",
        data_source=CORNELL_POLICY_SYNTHETIC_TEST,
        transparency_message="📄 Using Cornell University public policy (from their website)"
    )
    response = decision.to_api_response()
    response["log_status"] = "No student involved - policy source only"
    return response

def example_pilot_response():
    """What API returns for pilot (Month 2)"""
    decision = GovernanceDecisionWithProvenance(
        decision="ALLOW",
        policy_id="IITD_CS101_v1.0",
        log_created=True,
        log_pseudonym="iitd_pilot_student_consented_001",
        log_content="metadata_only: action, decision, timestamp",
        data_source=PILOT_REAL_COURSE_SYNTHETIC_STUDENT,
        transparency_message="✅ Real course (IIT Delhi) + Consented synthetic student"
    )
    return decision.to_api_response()

# ============================================================================
# DATA SOURCE REGISTRY (Track all data)
# ============================================================================

DATA_SOURCES_IN_USE = {
    "public_policies": [
        {
            "name": "Cornell GenAI Policy 2025",
            "source_url": "cornell.edu/policies/genai",
            "data_type": "public",
            "real_pii": False,
            "real_content": False
        },
        {
            "name": "Stanford AI Guidelines",
            "source_url": "stanford.edu/ai-guidelines",
            "data_type": "public",
            "real_pii": False,
            "real_content": False
        },
        {
            "name": "IIT Delhi GenAI Rules",
            "source_url": "iitd.ac.in/policies",
            "data_type": "public",
            "real_pii": False,
            "real_content": False
        }
    ],
    "synthetic_test_data": [
        {
            "id": "test_001_to_100",
            "description": "Fake students with synthetic actions",
            "real_pii": False,
            "real_content": False,
            "purpose": "System validation"
        }
    ],
    "pilot_data": [
        {
            "status": "Not active yet",
            "description": "Real universities (with consent) + fake student IDs",
            "month": "February 2026",
            "real_pii": False,
            "real_content": False
        }
    ]
}

if __name__ == "__main__":
    import json
    
    print("="*80)
    print("DATA PROVENANCE - API RESPONSE EXAMPLES")
    print("="*80)
    
    print("\n1. SYNTHETIC TEST RESPONSE (MVP)")
    print(json.dumps(example_synthetic_test_response(), indent=2))
    
    print("\n2. PUBLIC POLICY RESPONSE")
    print(json.dumps(example_public_policy_response(), indent=2))
    
    print("\n3. PILOT RESPONSE (Future)")
    print(json.dumps(example_pilot_response(), indent=2))
    
    print("\n4. DATA SOURCES REGISTRY")
    print(json.dumps(DATA_SOURCES_IN_USE, indent=2))
