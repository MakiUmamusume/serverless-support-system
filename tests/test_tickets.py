from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_ticket():
    response = client.post("/tickets", json={
        "title": "Test Ticket",
        "description": "Testing ticket creation"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Ticket created"
    assert data["ticket"]["title"] == "Test Ticket"

def test_get_all_tickets():
    response = client.get("/tickets")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_ticket_by_id():
    client.post("/tickets", json={
        "title": "Another Ticket",
        "description": "For ID test"
    })

    response = client.get("/tickets/1")

    assert response.status_code == 200
    assert "title" in response.json()

def test_ticket_not_found():
    response = client.get("/tickets/999")

    assert response.status_code == 404