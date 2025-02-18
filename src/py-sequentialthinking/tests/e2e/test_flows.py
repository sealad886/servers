import json
import pytest
from fastapi.testclient import TestClient

def test_complete_thought_flow(client: TestClient):
    """Test a complete flow of thoughts, including a revision and a branch."""
    # Initial thought
    thought1 = {
        "thought": "Initial problem analysis",
        "thought_number": 1,
        "total_thoughts": 4,
        "next_thought_needed": True
    }
    response1 = client.post("/tools/sequentialthinking", json=thought1)
    assert response1.status_code == 200
    result1 = json.loads(response1.json()["content"][0]["text"])
    assert result1["thought_history_length"] == 1

    # Second thought
    thought2 = {
        "thought": "Proposed solution approach",
        "thought_number": 2,
        "total_thoughts": 4,
        "next_thought_needed": True
    }
    response2 = client.post("/tools/sequentialthinking", json=thought2)
    assert response2.status_code == 200
    result2 = json.loads(response2.json()["content"][0]["text"])
    assert result2["thought_history_length"] == 2

    # Revision of first thought
    revision = {
        "thought": "Revised problem analysis with new insights",
        "thought_number": 3,
        "total_thoughts": 4,
        "next_thought_needed": True,
        "is_revision": True,
        "revises_thought": 1
    }
    response_revision = client.post("/tools/sequentialthinking", json=revision)
    assert response_revision.status_code == 200
    result_revision = json.loads(response_revision.json()["content"][0]["text"])
    assert result_revision["thought_history_length"] == 3

    # Branch from second thought
    branch = {
        "thought": "Alternative solution approach",
        "thought_number": 4,
        "total_thoughts": 4,
        "next_thought_needed": False,
        "branch_from_thought": 2,
        "branch_id": "alternative-1"
    }
    response_branch = client.post("/tools/sequentialthinking", json=branch)
    assert response_branch.status_code == 200
    result_branch = json.loads(response_branch.json()["content"][0]["text"])
    assert result_branch["thought_history_length"] == 4
    assert "alternative-1" in result_branch["branches"]

def test_dynamic_total_thoughts(client: TestClient):
    """Test adjusting total_thoughts as the thinking process evolves."""
    # Start with 2 planned thoughts
    thought1 = {
        "thought": "Initial analysis",
        "thought_number": 1,
        "total_thoughts": 2,
        "next_thought_needed": True
    }
    response1 = client.post("/tools/sequentialthinking", json=thought1)
    result1 = json.loads(response1.json()["content"][0]["text"])
    assert result1["total_thoughts"] == 2

    # Realize we need more thoughts
    thought2 = {
        "thought": "Intermediate step",
        "thought_number": 2,
        "total_thoughts": 3,  # Increased from 2
        "next_thought_needed": True,
        "needs_more_thoughts": True
    }
    response2 = client.post("/tools/sequentialthinking", json=thought2)
    result2 = json.loads(response2.json()["content"][0]["text"])
    assert result2["total_thoughts"] == 3

    # Complete with third thought
    thought3 = {
        "thought": "Final conclusion",
        "thought_number": 3,
        "total_thoughts": 3,
        "next_thought_needed": False
    }
    response3 = client.post("/tools/sequentialthinking", json=thought3)
    result3 = json.loads(response3.json()["content"][0]["text"])
    assert result3["total_thoughts"] == 3
    assert result3["next_thought_needed"] is False

def test_error_recovery_flow(client: TestClient):
    """Test recovery from errors in the thought process."""
    # Start with invalid data
    invalid_thought = {
        "thought": "Invalid thought",
        "thought_number": 0,  # Invalid
        "total_thoughts": 2,
        "next_thought_needed": True
    }
    response_invalid = client.post("/tools/sequentialthinking", json=invalid_thought)
    assert response_invalid.status_code == 200
    result_invalid = response_invalid.json()
    assert result_invalid["is_error"] is True

    # Recover with valid data
    valid_thought = {
        "thought": "Valid thought after error",
        "thought_number": 1,
        "total_thoughts": 2,
        "next_thought_needed": True
    }
    response_valid = client.post("/tools/sequentialthinking", json=valid_thought)
    assert response_valid.status_code == 200
    result_valid = json.loads(response_valid.json()["content"][0]["text"])
    assert result_valid["thought_number"] == 1
    assert "is_error" not in response_valid.json()

    # Complete the flow
    final_thought = {
        "thought": "Final thought",
        "thought_number": 2,
        "total_thoughts": 2,
        "next_thought_needed": False
    }
    response_final = client.post("/tools/sequentialthinking", json=final_thought)
    assert response_final.status_code == 200
    result_final = json.loads(response_final.json()["content"][0]["text"])
    assert result_final["next_thought_needed"] is False
