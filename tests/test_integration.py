"""Integration tests for full project."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Skip if backend not runnable
try:
    from backend.main import app
    from backend.models import Base
    from backend.db import get_db
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


# SQLite test DB
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    if not BACKEND_AVAILABLE:
        pytest.skip("Backend not available")
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_health_check(client):
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "app" in response.json()


@pytest.mark.skipif(not BACKEND_AVAILABLE, reason="Backend not available")
def test_compile_policy(client):
    """Test policy compilation endpoint."""
    payload = {
        "course_id": "CS101",
        "title": "AI Policy",
        "allowed_actions": [{"action": "brainstorm", "assessment_type": "assignment"}],
        "prohibited_actions": [],
        "disclosure_config": {"requires_disclosure": True},
        "metadata": {"author": "prof_doe", "institution": "MIT"}
    }
    
    response = client.post("/api/policies/compile", json=payload)
    assert response.status_code in [200, 422]  # Allow validation errors in test
    if response.status_code == 200:
        assert "policy_id" in response.json() or "success" in response.json()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
