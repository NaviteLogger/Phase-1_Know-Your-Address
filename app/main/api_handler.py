from flask import jsonify, current_app
import requests


def send_request_to_valide_address(address):
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]
