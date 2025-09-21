from fastapi.testclient import TestClient
from APP1.main import app

client = TestClient(app)

"""
Тесты запускать из терминала с помощью:   python -m pytest
"""


def test_get_users_all_api() -> None:
    response = client.get("/users/")
    assert response.status_code == 200
