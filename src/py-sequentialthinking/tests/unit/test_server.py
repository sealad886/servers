import pytest
from sequentialthinking.think import SequentialThinkingServer, ThoughtData

def test_server_initialization():
    """Test that SequentialThinkingServer initializes correctly."""
    server = SequentialThinkingServer()
    assert server.thought_history == []
    assert server.branches == {}

def test_validate_thought_data():
    """Test thought data validation."""
    server = SequentialThinkingServer()
    data = {
        "thought": "Test thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }

    validated = server.validate_thought_data(data)
    assert isinstance(validated, ThoughtData)
    assert validated.thought == data["thought"]
    assert validated.thought_number == data["thought_number"]
    assert validated.total_thoughts == data["total_thoughts"]
    assert validated.next_thought_needed == data["next_thought_needed"]

def test_format_thought_regular():
    """Test formatting a regular thought."""
    server = SequentialThinkingServer()
    thought_data = ThoughtData(
        thought="Test thought",
        thought_number=1,
        total_thoughts=3,
        next_thought_needed=True
    )

    formatted = server.format_thought(thought_data)
    assert "💭 Thought 1/3" in formatted
    assert "Test thought" in formatted

def test_format_thought_revision():
    """Test formatting a revision thought."""
    server = SequentialThinkingServer()
    thought_data = ThoughtData(
        thought="Revision thought",
        thought_number=2,
        total_thoughts=3,
        next_thought_needed=True,
        is_revision=True,
        revises_thought=1
    )

    formatted = server.format_thought(thought_data)
    assert "🔄 Revision 2/3" in formatted
    assert "(revising thought 1)" in formatted
    assert "Revision thought" in formatted

def test_format_thought_branch():
    """Test formatting a branch thought."""
    server = SequentialThinkingServer()
    thought_data = ThoughtData(
        thought="Branch thought",
        thought_number=2,
        total_thoughts=3,
        next_thought_needed=True,
        branch_from_thought=1,
        branch_id="branch-1"
    )

    formatted = server.format_thought(thought_data)
    assert "🌿 Branch 2/3" in formatted
    assert "(from thought 1, ID: branch-1)" in formatted
    assert "Branch thought" in formatted

def test_process_thought_success():
    """Test successful thought processing."""
    server = SequentialThinkingServer()
    data = {
        "thought": "Test thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }

    result = server.process_thought(data)
    assert "content" in result
    assert len(result["content"]) == 1
    assert result["content"][0]["type"] == "text"

    response_data = eval(result["content"][0]["text"])
    assert response_data["thought_number"] == 1
    assert response_data["total_thoughts"] == 3
    assert response_data["next_thought_needed"] is True
    assert response_data["thought_history_length"] == 1

def test_process_thought_with_branch():
    """Test processing a thought with branching."""
    server = SequentialThinkingServer()

    # Add initial thought
    server.process_thought({
        "thought": "Initial thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    })

    # Add branch
    branch_data = {
        "thought": "Branch thought",
        "thought_number": 2,
        "total_thoughts": 3,
        "next_thought_needed": True,
        "branch_from_thought": 1,
        "branch_id": "branch-1"
    }

    result = server.process_thought(branch_data)
    response_data = eval(result["content"][0]["text"])
    assert "branch-1" in response_data["branches"]
    assert response_data["thought_history_length"] == 2

def test_process_thought_error_handling():
    """Test error handling in thought processing."""
    server = SequentialThinkingServer()
    invalid_data = {
        "thought": 123,  # Invalid type
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }

    result = server.process_thought(invalid_data)
    assert "content" in result
    assert "is_error" in result
    assert result["is_error"] is True

    error_data = eval(result["content"][0]["text"])
    assert "error" in error_data
    assert "status" in error_data
    assert error_data["status"] == "failed"
