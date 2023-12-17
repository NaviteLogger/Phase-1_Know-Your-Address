from flask import Blueprint, render_template, current_app, request, jsonify, session
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


# The following route is used to validate the given address by making a POST request to the Google Maps API
# The Google Maps API will return a JSON response containing the validation result
@main_bp.route("/validate-the-given-address", methods=["POST"])
def validate_the_given_address():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Get the search address from the form
    address = request.json["address"]
    region_code = request.json["regionCode"]

    # Step 1: Build the JSON request body for the Google Maps API
    payload = {
        "address": {
            "regionCode": region_code,
            "addressLine1": address,
        }
    }

    # Step 2: Build the headers for the Google Maps API
    headers = {
        "Content-Type": "application/json",
    }

    # Step 3: Build the URL for the Google Maps API
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={google_maps_api_key}"

    # Step 4: Send the request to the Google Maps API
    response = requests.post(url, json=payload, headers=headers)

    # Step 5: Deal with the incoming response from the Google Maps API
    # Check if the request was successful
    if response.status_code == 200:
        # Store the result in the session
        session["address_validation_result"] = response.json()
        return response.status_code
    else:
        # Console log the error message
        print(f"Error while fetching Google Maps API for the inital address validation: {response.status_code}: {response.text}")
        return response.status_code


# The following route is used to manage the address validation result and sending the appropriate response back to the client
# Function will return the jsonified response containing the info about the address validation result
@main_bp.route("/manage-the-address-validation-result", methods=["POST"])
def manage_the_address_validation_result():
    # Get the address validation result from the session
    address_validation_result = session["address_validation_result"]

    # Deal with the address validation result


@main_bp.route("/retrieve-coordinates-for-the-address", methods=["POST"])
def retrieve_coordinates_for_the_address():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Get the search address from the form
    address = request.json["address"]

    # Step 1: Get the latitude and longitude of the address
    # Build the URL for the Google Maps API
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"

    # Send the request to the Google Maps API
    geocoding_response = requests.get(geocoding_url).json()


@main_bp.route("/retrieve-public-transport-information-for-the-given-address", methods=["POST"])
def retrieve_public_transport_information_for_the_given_address():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Extract the longitude and latitude from the json data
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
