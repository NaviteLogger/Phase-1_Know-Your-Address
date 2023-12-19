from flask import current_app, jsonify
import requests


def send_request_to_initially_valide_the_address(address):
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_ADDRESS_VALIDATION_API_KEY"]

    # Build the request for the Google Maps API
    payload = {
        "address": {
            "addressLines": [address],
        }
    }

    # Build the headers for the Google Maps API
    headers = {
        "Content-Type": "application/json",
    }

    # Set the URL for the Google Maps API
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={google_maps_api_key}"

    # Send the request to the Google Maps API
    response = requests.post(url, json=payload, headers=headers)

    # Return the response
    return response


def assess_the_quality_of_the_address(response):
    # Assess the quality of the address
    if response["result"]["verdict"]["validationGranularity"] == "OTHER" or response["result"]["verdict"]["addressComplete"] == False:
        # The address is not valid and requires fixing
        # Check which components of the address are missing/invalid
        missing_or_invalid_components = {}

        for component in response["result"]["address"]["addressComponents"]:
            if component["confirmationLevel"] != "CONFIRMED":
                component_name = component["componentName"]["text"]  # Use the actual component name
                confirmation_level = component["confirmationLevel"]
                missing_or_invalid_components[component_name] = confirmation_level

        return jsonify({"status": "fix", "message": "The address is not valid and requires fixing"})
    elif response["result"]["verdict"]["validationGranularity"] != "OTHER" and response["result"]["verdict"]["addressComplete"] == True and (response["result"]["verdict"]["hasInferredComponents"] == True or response["result"]["verdict"]["hasReplacedComponents"] == True):
        # The address is valid, but requires confirmation from the user
        return jsonify({"status": "confirm", "message": "The address is valid, but requires confirmation from the user"})
    elif (response["result"]["verdict"]["validationGranularity"] == "PREMISE" or response["result"]["verdict"]["validationGranularity"] == "SUB_PREMISE") and response["result"]["verdict"]["addressComplete"] == True and response["result"]["verdict"]["hasInferredComponents"] == False and response["result"]["verdict"]["hasReplacedComponents"] == False:
        # The address is valid
        return jsonify({"status": "valid", "message": "The address is valid"})
