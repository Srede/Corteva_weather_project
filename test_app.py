import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture to initialize Flask test client.
    This allows us to simulate HTTP requests to the Flask app without running the server.
    """
    with app.test_client() as client:
        yield client

def test_get_weather(client):
    """
    Test the GET /api/weather endpoint without filters.
    This test checks the default pagination and ensures the response is a list of weather data.
    """
    response = client.get('/api/weather')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_weather_with_filters(client):
    """
    Test the GET /api/weather endpoint with station_id and date filters.
    This ensures that filtering by station_id and date works correctly.
    """
    response = client.get('/api/weather?station_id=USC00110072&date=1985-01-01')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
    # Ensure the filtered data matches the provided station_id and date
    for weather_data in response.json:
        assert weather_data['station_id'] == 'USC00110072'
        assert weather_data['date'] == '1985-01-01'

def test_get_weather_stats(client):
    """
    Test the GET /api/weather/stats endpoint.
    This test checks if the weather statistics are returned as expected.
    """
    response = client.get('/api/weather/stats')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_pagination(client):
    """
    Test pagination on the /api/weather endpoint.
    This ensures that pagination is working correctly by specifying page and per_page parameters.
    """
    response = client.get('/api/weather?page=2&per_page=5')
    assert response.status_code == 200
    assert isinstance(response.json, list)
