import pytest
from flask import url_for
from app import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        yield app
