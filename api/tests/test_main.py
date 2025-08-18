import pytest

from main import app


@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data and "endpoints" in data


def test_info(client):
    resp = client.get("/info")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "supported_data_types" in data
    assert "supported_output_formats" in data


def test_generate_json(client):
    payload = {
        "count": 5,
        "format": "json",
        "id": {"type": "int", "min": 1, "max": 10},
        "name": {"type": "string"}
    }
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list) and len(data) == 5


def test_generate_csv(client):
    payload = {
        "count": 3,
        "format": "csv",
        "id": {"type": "int", "min": 1, "max": 10},
        "name": {"type": "string"}
    }
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 200
    assert resp.mimetype == 'text/csv'
    text = resp.get_data(as_text=True)
    assert "id,name" in text.splitlines()[0]


def test_error_when_count_missing_schema(client):
    payload = {"count": 5, "format": "json"}
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 400
    assert "No schema fields provided" in resp.get_json().get("error", "")


def test_error_when_count_exceeds_limit(client):
    payload = {"count": 10001, "format": "json", "id": {"type": "int", "min": 1, "max": 10}}
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 400
    assert "exceed 10000" in resp.get_json().get("error", "")


def test_error_when_invalid_count_type(client):
    payload = {"count": "ten", "format": "json", "id": {"type": "int", "min": 1, "max": 10}}
    resp = client.post("/generate", json=payload)
    assert resp.status_code == 400
    assert "Count must be a positive integer" in resp.get_json().get("error", "")


