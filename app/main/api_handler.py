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
            "result": {
                "address": address,
                "redirectionUrl": "/retrieve-public-transport-information-for-the-given-address",
            },
        }

        return jsonify({"serverResponse": server_response})


def suggest_the_correct_address(address):
    # Get the Google Maps 'Places API' API key stored in the configurtion file
    google_maps_places_new_api_key = current_app.config["GOOGLE_MAPS_PLACES_NEW_API_KEY"]

    # Build the payload for the Google Maps 'Places API'
    payload = {
        "textQuery": address,
    }

    # Build the headers for the Google Maps 'Places API'
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_maps_places_new_api_key,
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
            return jsonify({"status": "success", "message": "Request for location suggestions for the given address was successful", "response": response})

        except Exception as e:
            # If an exception was raised, print the exception
            print("Error while parsing the JSON response from the Google Maps 'Places API', exception: ", e)

            # Return the jsonified response
            return jsonify({"status": "error", "message": "Request for location suggestions for the given address was not successful"})

    else:
        # If the status code is not 200, the request was not successful
        print(f"Error while sending the request to the Google Maps 'Places API', status code: , {response.status_code}")
        return jsonify({"status": "error", "message": "Request for location suggestions for the given address was not successful"})


def retrieve_public_transport_information_for_the_given_address(address):
    # Get the Google Maps 'Places API' API key stored in the configurtion file
    google_maps_places_new_api_key = current_app.config["GOOGLE_MAPS_PLACES_NEW_API_KEY"]

    # Get the longitude and latitude of the given address - call the function responsible for sending the request to the Google Maps 'GeoCoding API'
    response = retrieve_geographical_coordinates_for_the_given_address(address)

    # Extract the longitude and latitude from the response
    latitude = response["latitude"]
    longitude = response["longitude"]

    # Build the payload for the Google Maps 'Places API'
    payload = {
        "includedTypes" : ["airport", "bus_station", "light_rail_station", "subway_station", "train_station", "transit_station"],
        "maxResults": 50,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radiusMeters": 10000,
            },
        },
    }

    # Build the headers for the Google Maps 'Places API'
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_maps_places_new_api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel",
    }

    

def retrieve_geographical_coordinates_for_the_given_address(address):
    # Get the Google Maps 'GeoCoding API' API key stored in the configurtion file
    google_maps_geocoding_api_key = current_app.config["GOOGLE_MAPS_GEOCODING_API_KEY"]

    # Build the url for the Google Maps 'GeoCoding API'
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_geocoding_api_key}"

    # Send the request to the Google Maps 'GeoCoding API'
    response = requests.get(url)

    # Check the status of the request
    if response.status_code == 200:
        # If the status code is 200, the request was successful
        try:
            # Parse the JSON response
            response = response.json()

            # Extract the latitude and longitude from the response
            latitude = response["results"][0]["geometry"]["location"]["lat"]
            longitude = response["results"][0]["geometry"]["location"]["lng"]

            # Pack the latitude and longitude into a dictionary
            response = {
                "latitude": latitude,
                "longitude": longitude,
            }

            # Return the jsonified response
            return jsonify({"status": "success", "message": "Request for geographical coordinates for the given address was successful", "response": response})

        except Exception as e:
            # If an exception was raised, print the exception
            print("Error while parsing the JSON response from the Google Maps 'GeoCoding API', exception: ", e)

            # Return the jsonified response
            return jsonify({"status": "error", "message": "Request for geographical coordinates for the given address was not successful"})

    else:
        # If the status code is not 200, the request was not successful
        print(f"Error while sending the request to the Google Maps 'GeoCoding API', status code: , {response.status_code}")
        return jsonify({"status": "error", "message": "Request for geographical coordinates for the given address was not successful"})