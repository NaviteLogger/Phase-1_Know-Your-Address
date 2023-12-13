from flask import Blueprint, render_template, current_app, request, jsonify
import requests

main_bp = Blueprint("main_bp", __name__)

# Get the Google Maps API key stored in the configurtion file
google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/search", methods=["POST"])
def search():
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
        # Build the URL for the Google Maps API
        nearby_stops_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=500&type=bus_station&key={google_maps_api_key}"

        # Send the request to the Google Maps API
        nearby_stops_response = requests.get(nearby_stops_url).json()

        # Check the status code of the response
        if nearby_stops_response["status"] == "OK":
            # Process the response to get the list of nearby stops
            transport_stops = nearby_stops_response["results"]

        else:
            # Return an error message if the nearby stops are not found
            return jsonify({"error": "There was an error while fetching the nearby stops for the given address."}), 404

    else:
        # Return an error message if the address is not found
        return jsonify({"error": "There was an error while fetching the address."}), 404
