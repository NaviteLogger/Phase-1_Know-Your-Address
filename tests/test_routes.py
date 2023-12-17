import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app("config.TestingConfig")
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize()
def test_save_the_given_address_to_session(client, input_address, expected_status_code):
    response = client.post("/save-the-given-address-to-session", data={"address": input_address})
    assert response.status_code == expected_status_code
