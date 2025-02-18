import pytest
from pydantic import ValidationError
from sequentialthinking.think import ThoughtData

def test_thought_data_required_fields():
    """Test that ThoughtData validates required fields."""
    data = {
        "thought": "Test thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }
    thought = ThoughtData(**data)
    assert thought.thought == data["thought"]
    assert thought.thought_number == data["thought_number"]
    assert thought.total_thoughts == data["total_thoughts"]
    assert thought.next_thought_needed == data["next_thought_needed"]

def test_thought_data_optional_fields():
    """Test that ThoughtData handles optional fields correctly."""
    data = {
        "thought": "Test thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True,
        "is_revision": True,
        "revises_thought": 1,
        "branch_from_thought": None,
        "branch_id": None,
        "needs_more_thoughts": True
    }
    thought = ThoughtData(**data)
    assert thought.is_revision == data["is_revision"]
    assert thought.revises_thought == data["revises_thought"]
    assert thought.branch_from_thought == data["branch_from_thought"]
    assert thought.branch_id == data["branch_id"]
    assert thought.needs_more_thoughts == data["needs_more_thoughts"]

def test_thought_data_missing_required_fields():
    """Test that ThoughtData raises ValidationError when required fields are missing."""
    with pytest.raises(ValidationError):
        ThoughtData(
            thought="Test thought",
            thought_number=1
        )

def test_thought_data_invalid_types():
    """Test that ThoughtData validates field types."""
    with pytest.raises(ValidationError):
        ThoughtData(
            thought=123,  # should be string
            thought_number="1",  # should be int
            total_thoughts=3.14,  # should be int
            next_thought_needed="true"  # should be bool
        )

def test_thought_data_invalid_values():
    """Test that ThoughtData validates field values."""
    with pytest.raises(ValidationError):
        ThoughtData(
            thought="Test thought",
            thought_number=0,  # should be >= 1
            total_thoughts=0,  # should be >= 1
            next_thought_needed=True
        )
