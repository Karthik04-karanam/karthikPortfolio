"""
Tests for Health and Root Status Endpoints
"""
from unittest.mock import MagicMock
from fastapi import status
from app.database import get_db
from app.main import app


def test_root_status(client):
    """Test that GET / returns API status, environment info, and docs link."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "online"
    assert "Karthik Portfolio" in data["service"]
    assert data["docs_url"] == "/docs"


def test_app_health(client):
    """Test that GET /api/health confirms backend service is healthy."""
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "portfolio-backend"
    assert "timestamp" in data


def test_db_health(client):
    """Test that GET /api/health/db executes query and confirms database is connected."""
    response = client.get("/api/health/db")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "timestamp" in data


def test_db_health_failure_handled(client):
    """Test that database failure safely returns 503 without leaking credentials or stack trace."""
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Simulated connection timeout to database server")

    def override_broken_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_broken_db
    try:
        response = client.get("/api/health/db")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        # Verify no stack trace or raw exception text leaked in response
        assert "Simulated connection" not in response.text
    finally:
        app.dependency_overrides.clear()
