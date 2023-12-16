from flask import Blueprint, render_template, current_app, request, jsonify
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/retrieveCoordinatesForAnAddress", methods=["POST"])
def retrieveCoordinatesForAnAddress():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Get the search address from the form
    address = request.form["address"]

    # Step 1: Get the latitude and longitude of the address
    # Build the URL for the Google Maps API
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"

    # Send the request to the Google Maps API
    geocoding_response = requests.get(geocoding_url).json()

    # Check the status code of the response
    if geocoding_response["status"] == "OK":
        # Get the latitude and longitude of the address
        latitude = geocoding_response["results"][0]["geometry"]["location"]["lat"]
        longitude = geocoding_response["results"][0]["geometry"]["location"]["lng"]

        # Step 2: Using the latitude and longitude, get the nearby public transport stops
        # Build the request for the Google Maps API
        payload = {
            "includedTypes": "bus_station|subway_station|train_station|transit_station",
            "maxResultsCount": 10,
            "locationRestriction": {
                "circle": {"center": {"latitude": latitude, "longitude": longitude}, "radiusMeters": 1000}
            },
        }

        # Define the headers for the request
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": google_maps_api_key,
            "X-Goog-FieldMask": "places.displayName",
        }

        # Make the POST request to the Google Maps API
        url = "https://places.googleapis.com/v1/places:searchNearby"
        response = requests.post(url, json=payload, headers=headers)

        # Check the status code of the response
        if response.status_code == 200:
            # Process the response JSON as needed
            result_data = response.json()
            return jsonify(result_data)

        else:
            # Return an error message if the nearby stops are not found
            error_message = f"Error {response.status_code}: {response.text}"
            return jsonify({"error": error_message})

    else:
        # Return an error message if the address is not found
        return jsonify({"error": "There was an error while fetching the address."}), 404
    
@main_bp.route("/retrievePublicTransportInformationForTheGivenAddress", methods=["POST"])
def retrievePublicTransportInformationForTheGivenAddress():
