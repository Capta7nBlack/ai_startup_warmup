import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
from db import DatabaseOperations

@pytest.fixture
def client():
    # Create a test client for the FastAPI app
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_ops():
    # Initialize the database operations
    db = DatabaseOperations()
    yield db
    # Clean up after tests (if needed)
