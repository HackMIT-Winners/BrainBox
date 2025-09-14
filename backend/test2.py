from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app import app

# filepath: /Users/xiangzhousun/Desktop/HackMIT/test_app.py

# Mock the helix.Client
app.dependency_overrides = {}
mock_db = MagicMock()
app.dependency_overrides["db"] = mock_db

client = TestClient(app)

def test_add_edge():
    # Mock response from the database
    mock_db.query.return_value = {"srcId": 1, "dstId": 2, "Relation": "related"}

    payload1 = {
        "text": "This is the first piece of data"
    }

    # Sample payload
    payload2 = {
        "srcId": 1,
        "dstId": 2,
        "Relation": "related"
    }

    # Send POST request to /edges
    response = client.post("/nodes", json=payload1)
    print(response.json())
    response = client.post("/edges", json=payload2)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "edge": {"srcId": 1, "dstId": 2, "Relation": "related"}
    }

    # Verify the mock was called with correct arguments
    mock_db.query.assert_called_once_with("linkNodes", {"srcId": 1, "dstId": 2})

test_add_edge()