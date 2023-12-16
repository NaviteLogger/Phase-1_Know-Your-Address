from flask import Blueprint, render_template, current_app, request, jsonify
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/validateTheGivenAddress", methods=["POST"])
def validateTheGivenAddress():
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
    response = requests.post(autocomplete_url, json=payload, headers=headers)


@main_bp.route("/retrieveCoordinatesForTheAddress", methods=["POST"])
def retrieveCoordinatesForTheAddress():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Get the search address from the form
    address = request.json["address"]

    # Step 1: Get the latitude and longitude of the address
    # Build the URL for the Google Maps API
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"

    # Send the request to the Google Maps API
    geocoding_response = requests.get(geocoding_url).json()


@main_bp.route("/retrievePublicTransportInformationForTheGivenAddress", methods=["POST"])
def retrievePublicTransportInformationForTheGivenAddress():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Extract the longitude and latitude from the json data
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
