import pytest
from app import app

@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_get_weather(client):
    """Test the GET /api/weather endpoint without filters (default pagination)."""
    response = client.get('/api/weather')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_get_weather_with_filters(client):
    """Test the GET /api/weather endpoint with station_id and date filters."""
    response = client.get('/api/weather?station_id=USC00110072&date=1985-01-01')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_get_weather_stats(client):
    """Test the GET /api/weather/stats endpoint."""
    response = client.get('/api/weather/stats')
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)

def test_pagination(client):
    """Test pagination on the /api/weather endpoint."""
    response = client.get('/api/weather?page=2&per_page=5')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) <= 5  # Test per_page size is respected
