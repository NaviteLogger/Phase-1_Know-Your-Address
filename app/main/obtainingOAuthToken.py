# This file will containt the code for obtaining the OAuth 2.0 access token from the Google Maps API.
# The following function will be exported to the routes.py file for obtaining the OAuth 2.0 access token:

# Path: app/main/obtainingOAuthToken.py
from flask import current_app
import requests


def obtainOAuthToken():
    # Get the Google Maps API key stored in the configurtion file
    google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]

    # Build the URL for the Google Maps API
    oauth_url = f"https://www.googleapis.com/oauth2/v4/token?client_id={google_maps_api_key}&client_secret={google_maps_api_key}&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer"

    # Send the request to the Google Maps API
    oauth_response = requests.post(oauth_url).json()

    # Extract the OAuth 2.0 access token from the response
    oauth_token = oauth_response["access_token"]

    return oauth_token
