import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_home_page_request(client):
    res = client.get("/")
    assert res.status_code == 200


def test_register_page_request(client):
    res = client.get("/register")
    assert res.status_code == 200