import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object("config.TestingConfig")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize(
    "input_address, expected_status",
    [
        ("Mazowiecka 15/3", "success"),
        ("Aleja KEN 115", "success"),
    ],
)
def test_save_the_given_address_to_session(client, input_address, expected_status):
    response = client.post("/save-the-given-address-to-session", json={"address": input_address})

    assert response.status_code == 200  # Check the HTTP status code

    data = response.json
    assert data["status"] == expected_status


@pytest.mark.parametrize(
    "input_address, expected_api_response_status_code",
    [
        ("Mazowiecka 15/3", 200),
        ("Aleja KEN 115", 200),
    ],
)
def test_validate_the_address(client, input_address, expected_api_response_status_code):
    response = client.post("/validate-the-address", json={"address": input_address})

    assert response.status_code == 200
    assert response.status_code == expected_api_response_status_code


def test_assess_the_quality_of_the_address(client):
    response = client.post("/assess-the-quality-of-the-address")

    assert response.status_code == 200

    data = response.json
    assert data["status"] == "success"
    assert data["message"] == "Request for address validation was successful"
    assert data["redirect"] == "/assess-the-quality-of-the-address"
