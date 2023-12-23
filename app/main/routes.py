from flask import Blueprint, render_template, current_app, request, jsonify, session
from app.main.api_handler import send_request_to_initially_valide_the_address, assess_the_quality_of_the_address_function
from app.main.additional_functions import is_url_encoded
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


# The following route is used to initially save the address in the session
# Actually this function was created to test whether the communication between the client and the server works
@main_bp.route("/save-the-given-address-to-session", methods=["POST"])
def save_the_given_address_to_session():
    # Get the search address from the form
    address = request.json["address"]

    # Return the jsonified response
    return jsonify({"status": "success", "message": "Address saved to session", "address": address, "redirect": "/validate-the-address"})


# The following route is used to call the Google Maps API and initially validate the address
@main_bp.route("/validate-the-address", methods=["POST"])
def validate_the_address():
    # Get the address from the request
    address = request.json["address"]

    # Call the function responsible for sending the validation request to the Google Maps API
    response = send_request_to_initially_valide_the_address(address)

    # Check the status of the request
    if response.status_code == 200:
        # If the status code is 200, the request was successful
        try:
            # Parse the JSON response
            response = response.json()

            return jsonify({"status": "success", "message": "Request for address validation was successful", "redirect": "/assess-the-quality-of-the-address", "response": response})

        except Exception as e:
            # If an exception was raised, print the exception
            print("Error while parsing the JSON response from the Google Maps Address Validation API, exception: ", e)

            # Return the jsonified response
            return jsonify({"status": "error", "message": "Request for address validation was not successful"})

    else:
        # If the status code is not 200, the request was not successful
        print(f"Error while sending the request to the Google Maps Address Validation API, status code: , {response.status_code}")
        return jsonify({"status": "error", "message": "Request for address validation was not successful"})


@main_bp.route("/assess-the-quality-of-the-address", methods=["POST"])
def assess_the_quality_of_the_address():
    # Get the Google Maps API response from the request
    response = request.json["response"]

    # Asses the quality of the address
    addressQuality = assess_the_quality_of_the_address_function(response)

    # Forward the function response to the client
    return addressQuality


@main_bp.route("/retrieve-public-transport-information-for-the-given-address", methods=["POST"])
def retrieve_public_transport_information_for_the_given_address():
    # Get the address from the request
    address = request.json["address"]

    # For the 'Places API' to work, the address must be URL encoded due to the middleware function 'Geocoding API'
    # Check whether the address is already URL encoded
    if is_url_encoded(address):
        # If the address is already URL encoded, do nothing
        pass
    else:
        # If the address is not URL encoded, return an error message, as the server should not accept the address in this form
        return jsonify({"status": "error", "message": "The address is not URL encoded"})

    # Now that the address is URL encoded, send the request to the function responsible for retrieving the public transport information
    
