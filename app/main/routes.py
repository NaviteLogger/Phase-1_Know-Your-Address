from flask import Blueprint, render_template, current_app, request
import requests

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/search", methods=["POST"])
def search():
    # Get the search address from the form
    address = request.form["address"]
