from flask import Blueprint, render_template, current_app, request, jsonify, session
from app.main.api_handler import send_api_request
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


# The following route is used to initially save the address in the session
@main_bp.route("/save-the-given-address-to-session", methods=["POST"])
def save_the_given_address_to_session():
    # Get the search address from the form
    address = request.json["address"]

    # Save the address in the session
    session["address"] = address

    # Return the jsonified response
    return jsonify("status": "success")

# The following route is used to manage the address validation result and sending the appropriate response back to the client
# Function will return the jsonified response containing the info about the address validation result
@main_bp.route("/manage-the-address-validation-result", methods=["POST"])
def manage_the_address_validation_result():
    # Pass the received json data to the function that will send the request to the Google Maps API
    response = send_api_request(request.json)


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
