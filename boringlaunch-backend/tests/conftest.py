import pytest
from fastapi.testclient import TestClient
from main import app
from database import db
import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(".env.test", override=True)

@pytest.fixture
def client():
    """Create a test client for the FastAPI application"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Create a test database connection"""
    # Use test database URL from environment
    original_url = os.getenv("SUPABASE_URL")
    try:
        yield db
    finally:
        # Cleanup after tests
        db.close()
        os.environ["SUPABASE_URL"] = original_url 