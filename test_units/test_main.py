import pytest
from fastapi import status
from entities import RentInstrumentRequest, ReturnInstrumentRequest, CreateInstrumentRequest
from db import DatabaseOperations

db = DatabaseOperations()



# Test the /init endpoint
def test_init_user(client):
    response = client.get("/init")
    assert response.status_code == status.HTTP_200_OK
    assert "user_id" in response.cookies
    assert "message" in response.json()

# Test the /rent endpoint
def test_rent_instrument(client):
    db.get_all()
    # Initialize a user
    init_response = client.get("/init")
    user_id = str(init_response.cookies.get("user_id"))

    # Create an instrument first
    create_request = CreateInstrumentRequest(instrument_name="Guitar")
    client.post("/instruments", json=create_request.model_dump())

    # Rent the instrument
    rent_request = RentInstrumentRequest(
        user_id=user_id,
        instrument_id=1,
        instrument_name="Guitar"
    )
    db.get_all()
    response = client.post("/rent", json=rent_request.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

# Test the /return endpoint
def test_return_instrument(client):
    db.get_all()
    # Initialize a user
    init_response = client.get("/init")
    user_id = init_response.cookies.get("user_id")

    # Create and rent an instrument first
    create_request = CreateInstrumentRequest(instrument_name="Piano")
    client.post("/instruments", json=create_request.model_dump())

    return_request = ReturnInstrumentRequest(
        user_id=user_id,
        instrument_id=2
    )
    db.get_all()
    response = client.post("/return", json=return_request.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

# Test the /instruments endpoint
def test_create_instrument(client):
    request = CreateInstrumentRequest(instrument_name="Violin")
    response = client.post("/instruments", json=request.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

# Test the /instruments/{instrument_id}/status endpoint
def test_get_instrument_status(client):
    # Create an instrument first
    create_request = CreateInstrumentRequest(instrument_name="Drums")
    client.post("/instruments", json=create_request.model_dump())

    # Check the status of the instrument
    response = client.get("/instruments/1/status")
    assert response.status_code == status.HTTP_200_OK
    assert "instrument_id" in response.json()
    assert "available" in response.json()

# Test the /instruments/available endpoint
def test_get_instruments_available(client):
    # Create an available instrument
    create_request = CreateInstrumentRequest(instrument_name="Flute")
    client.post("/instruments", json=create_request.model_dump())

    # Get available instruments
    response = client.get("/instruments/available")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0 
