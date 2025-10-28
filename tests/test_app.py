import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_ping_endpoint(client):
    """Test secure ping endpoint"""
    response = client.post(
        '/api/ping',
        json={'host': 'google.com'},
        content_type='application/json'
    )
    assert response.status_code == 200

def test_ping_invalid_host(client):
    """Test ping with invalid host"""
    response = client.post(
        '/api/ping',
        json={'host': 'google.com; ls'},  # Should be rejected
        content_type='application/json'
    )
    assert response.status_code == 400