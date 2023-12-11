from flask import render_template
from . import main


# Handle the GET request for the root url
@main.route("/")
def index():
    return render_template("index.html")
