import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

valid_headers = {
    "Authorization": "Bearer dummy_token"  # Replace with a valid token during real test
}

@pytest.mark.parametrize("review_content, expected_status", [
    ("This is a great place to study!", 200),
    ("' OR '1'='1", 400),
    ("1234567890", 400),
    ("     ", 400),
    ("a" * 1001, 400)
])
def test_review_input_validation(review_content, expected_status):
    response = client.post(
        "/reviews",
        headers=valid_headers,
        json={
            "spot_id": 1,
            "rating": 4,
            "review_content": review_content,
            "review_tags": ""
        }
    )
    assert response.status_code == expected_status
