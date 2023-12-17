from flask import jsonify, current_app
import requests


def send_request_to_valide_address(address):
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Build the request for the Google Maps API
    payload = {
        "address": {
            "addressLine1": address,
        }
    }

    # Build the headers for the Google Maps API
    headers = {
        "Content-Type": "application/json",
    }

    # Set the URL for the Google Maps API
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={google_maps_api_key}"

    # Send the request to the Google Maps API
    response = requests.post(url, json=payload, headers=headers).json()

    # Check if the request was successful
    if response.status_code == 200:
        # The requets was successful
        return jsonify({"status": "success", "message": "Address validation request was successful", "response": response})
    else:
        # The request was not successful
        print("Error while sending the request to the Google Maps API for address validation, response:" + response)
        return jsonify({"status": "error", "message": "Address validation request was not successful", "response": response})
