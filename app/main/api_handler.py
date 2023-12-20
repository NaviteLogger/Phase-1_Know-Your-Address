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

        # Assign the responseId to a variable for further use
        response_id = response["responseId"]

        # Pack the returned function elements into a dictionary
        server_response = {
            "status": "fix",
            "message": "The address is not valid and requires fixing",
            "result": {
                "missingOrInvalidComponents": missing_or_invalid_components,
            },
            "responseId": response_id,
        }

        return jsonify({"serverResponse": server_response})

    elif response["result"]["verdict"]["validationGranularity"] != "OTHER" and response["result"]["verdict"]["addressComplete"] == True and (response["result"]["verdict"]["hasInferredComponents"] == True or response["result"]["verdict"]["hasReplacedComponents"] == True):
        # The address is valid, but requires confirmation from the user
        # Check which components of the address were unconfirmed
        unconfirmed_components = {}

        for component in response["result"]["address"]["addressComponents"]:
            if component["confirmationLevel"] == "UNCONFIRMED_BUT_PLAUSIBLE":
                component_name = component["componentName"]["text"]
                component_type = component["componentType"]
                unconfirmed_components[component_name] = component_type

        # Check which components of the address were corrected
        corrected_components = {}

        for component in response["result"]["address"]["addressComponents"]:
            if component["replaced"] == True:
                component_name = component["componentName"]["text"]
                component_type = component["componentType"]
                corrected_components[component_name] = component_type

        # Assign the responseId to a variable for further use
        response_id = response["responseId"]

        # Pack the returned function elements into a dictionary
        server_response = {
            "status": "confirm",
            "message": "The address is valid, but requires confirmation from the user",
            "result": {
                "unconfirmedComponents": unconfirmed_components,
                "correctedComponents": corrected_components,
            },
            "responseId": response_id,
        }

        return jsonify({"serverResponse": server_response})

    elif (response["result"]["verdict"]["validationGranularity"] == "PREMISE" or response["result"]["verdict"]["validationGranularity"] == "SUB_PREMISE") and response["result"]["verdict"]["addressComplete"] == True and response["result"]["verdict"]["hasInferredComponents"] == False and response["result"]["verdict"]["hasReplacedComponents"] == False:
        # The address is valid
        # Return the jsonified response containing the address
        address = response["result"]["address"]["formattedAddress"]

        # Pack the returned function elements into a dictionary
        server_response = {
            "status": "valid",
            "message": "The address is valid",
            "address": address,
        }

        return jsonify({"serverResponse": server_response})

def provide_location_suggestions_for_an_address(address):
    # Get the Google Maps 'Places API' API key stored in the configurtion file
    google_maps_places_api_key = current_app.config["GOOGLE_MAPS_PLACES_API_KEY"]

    # Build the payload for the Google Maps 'Places API'
    payload = {
        "textQuery": address,
    }

    # Build the headers for the Google Maps 'Places API'
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_maps_places_api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel",
    }

    # Build the url for the Google Maps 'Places API'
    url = f"https://places.googleapis.com/v1/places:searchText"

    # Send the request to the Google Maps 'Places API'
    response = requests.post(url, json=payload, headers=headers)

    # Check the status of the request
    if response.status_code == 200:
        # If the status code is 200, the request was successful
        try:
            # Parse the JSON response
            response = response.json()

            # Return the jsonified response
            return jsonify({"status": "success", "message": "Request for location suggestions was successful", "response": response})

        except Exception as e:
            # If an exception was raised, print the exception
            print("Error while parsing the JSON response from the Google Maps 'Places API', exception: ", e)

            # Return the jsonified response
            return jsonify({"status": "error", "message": "Request for location suggestions was not successful"})

    else:
        # If the status code is not 200, the request was not successful
        print(f"Error while sending the request to the Google Maps 'Places API', status code: , {response.status_code}")
        return jsonify({"status": "error", "message": "Request for location suggestions for the given address was not successful"})