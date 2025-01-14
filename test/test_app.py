import pytest
from src.app import app

@pytest.fixture
def client():
    """
    Create a test client for Flask application.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """
    Test the home route.
    """
    response = client.get("/index")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Check if HTML content is returned


def test_correct_text(client):
    """
    Test the `/correct_text` endpoint.
    """
    response = client.post("/correct_text", json={"text": "I is a grammar problem."})
    assert response.status_code == 200
    data = response.get_json()
    assert "corrected_text" in data
    assert data["corrected_text"] == "I have a grammar problem."


def test_upload_file(client):
    """
    Test the `/upload_file` endpoint.
    """
    data = {
        "file": (open("uploaded_files/sample.txt", "rb"), "sample.txt")
    }
    response = client.post("/upload_file", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    data = response.get_json()
    assert "corrected_file_url" in data
