import pytest
from flask import url_for
from app import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "input_address, expected_status_code, expected_returned_content",
    [
        ("sample_address", 200, b"ExpectedContent1"),
        ("sample_address2", 200, b"ExpectedContent2"),
    ],
)
def test_search_route(client, input_address, expected_status_code, expected_returned_content):
    response = client.post("/search", data={"address": input_address})
    assert response.status_code == expected_status_code
    assert expected_returned_content in response.data
