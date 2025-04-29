from fastapi.testclient import TestClient
from random_server_fastapi_async import app

client = TestClient(app)

def test_get_random_integer():
    response = client.get("/random?type=int")
    assert response.status_code == 200
    data = response.json()
    assert "number" in data
    assert isinstance(data["number"], int)

def test_get_random_float():
    response = client.get("/random?type=float")
    assert response.status_code == 200
    data = response.json()
    assert "number" in data
    assert isinstance(data["number"], float)

def test_multiple_requests():
    numbers = set()
    for _ in range(1000):  # 1000 random numbers
        response = client.get("/random?type=int")
        assert response.status_code == 200
        data = response.json()
        num = data["number"]
        assert num not in numbers  # Ensure no duplicates
        numbers.add(num)
