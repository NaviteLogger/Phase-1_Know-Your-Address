from flask import Blueprint, render_template, current_app, request
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
