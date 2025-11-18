import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_signup_and_unregister():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@mergington.edu"

    # Signup
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert dup_resp.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert f"Unregistered {email}" in unregister_resp.json()["message"]

    # Unregister again should fail
    unregister_again = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_again.status_code == 400
