from flask import Blueprint, render_template, current_app, request, jsonify, session
from app.main.api_handler import send_request_to_initially_valide_the_address
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
    return jsonify({"status": "success", "message": "Address saved to session", "address": address, "redirect": "/validate-the-address"})


# The following route is used to call the Google Maps API and initially validate the address
@main_bp.route("/validate-the-address", methods=["POST"])
def validate_the_address():
    # Get the address from the session
    address = session["address"]

    # Call the function responsible for sending the request to the Google Maps API
    response = send_request_to_initially_valide_the_address(address)

    # Store the Google Maps API response in the session
    session["google_maps_api_response"] = response

    # Check the status of the request
    if response.status_code == 200:
        # If the status code is 200, the request was successful
        return jsonify({"status": "success", "message": "Request for address validation was successful", "redirect": "/assess-the-validity-of-the-address"})

    else:
        # If the status code is not 200, the request was not successful
        print(f"Error while sending the request to the Google Maps API, status code: , {response.status_code}")
        return jsonify({"status": "error", "message": "Request for address validation was not successful"})


@main_bp.route("/asses-the-validity-of-the-address", methods=["POST"])
def assess_the_validity_of_the_address():
    # Get the Google Maps API response from the session
    response = session["google_maps_api_response"]

    


@main_bp.route("/retrieve-public-transport-information-for-the-given-address", methods=["POST"])
def retrieve_public_transport_information_for_the_given_address():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Extract the longitude and latitude from the json data
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
