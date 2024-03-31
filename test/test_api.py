from starlette.testclient import TestClient

from apicast.api import app

client = TestClient(app)


def test_api_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "Apicast acquires bee flight forecast information" in response.text


def test_api_robots():
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "Disallow: /beeflight/" in response.text


def test_api_stations():
    response = client.get("/beeflight/stations/germany")
    assert response.status_code == 200

    items = response.json()["data"]
    assert len(items) > 50, "Something went wrong, there should be at least 50 results"


def test_api_data():
    response = client.get("/beeflight/forecast/germany/brandenburg/potsdam")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3, "Something went wrong, the data response should have three items"
