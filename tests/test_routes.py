import pytest
from flask import url_for
from app import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        yield app


def test_search_route(client):
    response = client.get(url_for("main.search"), data={"address": "Singapore"})
    assert response.status_code == 200
