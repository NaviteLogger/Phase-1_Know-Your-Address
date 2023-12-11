from flask import render_template
from flask import request
from . import main


# Handle the GET request for the '/' url
@main.route("/")
def index():
    return render_template("index.html")


# Handle the POST request for the '/search' url
@main.route("/search", methods=["POST"])
def search():
    address = request.form[address]
