import json
import pytest
from fastapi.testclient import TestClient

def test_list_tools(client: TestClient):
    """Test the /tools endpoint returns the correct tool information."""
    response = client.get("/tools")
    assert response.status_code == 200

    data = response.json()
    assert "tools" in data
    assert len(data["tools"]) == 1

    tool = data["tools"][0]
    assert tool["name"] == "sequentialthinking"
    assert "description" in tool
    assert "input_schema" in tool

def test_process_thought_success(client: TestClient, sample_thought_data):
    """Test successful thought processing."""
    response = client.post("/tools/sequentialthinking", json=sample_thought_data)
    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert len(data["content"]) == 1
    assert data["content"][0]["type"] == "text"

    result = json.loads(data["content"][0]["text"])
    assert result["thought_number"] == sample_thought_data["thought_number"]
    assert result["total_thoughts"] == sample_thought_data["total_thoughts"]
    assert result["next_thought_needed"] == sample_thought_data["next_thought_needed"]
    assert "branches" in result
    assert "thought_history_length" in result

def test_process_thought_revision(client: TestClient, sample_revision_data):
    """Test processing a thought revision."""
    response = client.post("/tools/sequentialthinking", json=sample_revision_data)
    assert response.status_code == 200

    data = response.json()
    result = json.loads(data["content"][0]["text"])
    assert result["thought_number"] == sample_revision_data["thought_number"]
    assert result["thought_history_length"] == 1

def test_process_thought_branch(client: TestClient, sample_branch_data):
    """Test processing a thought branch."""
    response = client.post("/tools/sequentialthinking", json=sample_branch_data)
    assert response.status_code == 200

    data = response.json()
    result = json.loads(data["content"][0]["text"])
    assert result["thought_number"] == sample_branch_data["thought_number"]
    assert sample_branch_data["branch_id"] in result["branches"]

def test_process_thought_invalid_data(client: TestClient):
    """Test processing with invalid thought data."""
    invalid_data = {
        "thought": "Invalid thought",
        "thought_number": 0,  # Invalid: should be >= 1
        "total_thoughts": 3,
        "next_thought_needed": True
    }

    response = client.post("/tools/sequentialthinking", json=invalid_data)
    assert response.status_code == 200  # API always returns 200, even for errors

    data = response.json()
    assert "is_error" in data
    assert data["is_error"] is True

    error_content = json.loads(data["content"][0]["text"])
    assert "error" in error_content
    assert "status" in error_content
    assert error_content["status"] == "failed"

def test_process_thought_sequence(client: TestClient):
    """Test processing a sequence of thoughts."""
    # First thought
    thought1 = {
        "thought": "First thought",
        "thought_number": 1,
        "total_thoughts": 3,
        "next_thought_needed": True
    }
    response1 = client.post("/tools/sequentialthinking", json=thought1)
    assert response1.status_code == 200
    result1 = json.loads(response1.json()["content"][0]["text"])
    assert result1["thought_history_length"] == 1

    # Second thought
    thought2 = {
        "thought": "Second thought",
        "thought_number": 2,
        "total_thoughts": 3,
        "next_thought_needed": True
    }
    response2 = client.post("/tools/sequentialthinking", json=thought2)
    assert response2.status_code == 200
    result2 = json.loads(response2.json()["content"][0]["text"])
    assert result2["thought_history_length"] == 2

    # Final thought
    thought3 = {
        "thought": "Final thought",
        "thought_number": 3,
        "total_thoughts": 3,
        "next_thought_needed": False
    }
    response3 = client.post("/tools/sequentialthinking", json=thought3)
    assert response3.status_code == 200
    result3 = json.loads(response3.json()["content"][0]["text"])
    assert result3["thought_history_length"] == 3
