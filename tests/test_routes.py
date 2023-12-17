import pytest


@pytest.mark.parametrize(
    "input_address, expected_status",
    [
        ("Mazowiecka 15/3", "success"),
        ("Aleja KEN 115", "success"),
    ],
)
def test_save_the_given_address_to_session(client, input_address, expected_status):
    response = client.post("/save-the-given-address-to-session", data={"address": input_address})
    assert response.status == "success"
