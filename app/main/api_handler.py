from flask import jsonify
import requests

def send_api_request(address_validation_result):
    # Check which json is incoming: the one from the client or the one from the Google Maps API
    if "responseId" in address_validation_result:
        # The incoming json is the one from the Google Maps API

    else:
        # The incoming json is the one from the client