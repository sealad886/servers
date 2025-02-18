import pytest
from fastapi.testclient import TestClient
from sequentialthinking import app

@pytest.fixture
def client():
    """Fixture that creates a FastAPI TestClient instance."""
    return TestClient(app)

@pytest.fixture
def sample_thought_data():
    """Fixture that provides sample thought data for testing."""
    return {
        "thought": "This is a test thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }

@pytest.fixture
def sample_revision_data():
    """Fixture that provides sample revision data for testing."""
    return {
        "thought": "This is a revision of thought 1",
        "thought_number": 2,
        "total_thoughts": 3,
        "next_thought_needed": True,
        "is_revision": True,
        "revises_thought": 1
    }

@pytest.fixture
def sample_branch_data():
    """Fixture that provides sample branch data for testing."""
    return {
        "thought": "This is a branch from thought 1",
        "thought_number": 2,
        "total_thoughts": 3,
        "next_thought_needed": True,
        "branch_from_thought": 1,
        "branch_id": "branch-1"
    }
