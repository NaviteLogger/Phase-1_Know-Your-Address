from flask import render_template, request, current_app
from . import main

google_maps_api_key = current_app.config["GOOGLE_MAPS_API_KEY"]


# Handle the GET request for the '/' url
@main.route("/")
def index():
    return render_template("index.html")


# Handle the POST request for the '/search' url
@main.route("/search", methods=["POST"])
def search():
    address = request.form[address]
