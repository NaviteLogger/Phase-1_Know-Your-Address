import pytest


@pytest.mark.parametrize(
    "input_address, expected_status_code",
    [
        ("", 400),
        ("Aleja KEN 115", 200),
    ],
)
def test_save_the_given_address_to_session(client, input_address, expected_status_code):
    response = client.post("/save-the-given-address-to-session", data={"address": input_address})
    assert response.status_code == expected_status_code
