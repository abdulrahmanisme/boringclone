import pytest
from fastapi.testclient import TestClient

def test_create_startup(client: TestClient):
    """Test creating a new startup"""
    startup_data = {
        "name": "Test Startup",
        "description": "A test startup",
        "website": "https://teststartup.com",
        "linkedin_url": "https://linkedin.com/company/teststartup"
    }
    
    response = client.post("/api/startups/", json=startup_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == startup_data["name"]
    assert data["description"] == startup_data["description"]
    assert "id" in data

def test_get_startups(client: TestClient):
    """Test retrieving all startups"""
    response = client.get("/api/startups/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_startup_by_id(client: TestClient):
    """Test retrieving a specific startup by ID"""
    # First create a startup
    startup_data = {
        "name": "Test Startup 2",
        "description": "Another test startup",
        "website": "https://teststartup2.com",
        "linkedin_url": "https://linkedin.com/company/teststartup2"
    }
    create_response = client.post("/api/startups/", json=startup_data)
    startup_id = create_response.json()["id"]
    
    # Then retrieve it
    response = client.get(f"/api/startups/{startup_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == startup_data["name"]
    assert data["id"] == startup_id

def test_invalid_startup_data(client: TestClient):
    """Test validation for invalid startup data"""
    invalid_data = {
        "name": "",  # Empty name should be invalid
        "description": "Test description",
        "website": "not-a-valid-url",  # Invalid URL
        "linkedin_url": "not-a-valid-url"  # Invalid URL
    }
    
    response = client.post("/api/startups/", json=invalid_data)
    assert response.status_code == 422  # Validation error 