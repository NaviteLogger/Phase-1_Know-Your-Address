import pytest
from flask import url_for
from app import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "address, expected_content",
    [
        ("sample_address", b"ExpectedContent1"),
        ("sample_address2", b"ExpectedContent2"),
    ],
)
def test_search_route(client, address, expected_content):
    response = client.get(url_for("main.search"), data={"address": address})
    assert response.status_code == 200
    assert expected_content in response.data
