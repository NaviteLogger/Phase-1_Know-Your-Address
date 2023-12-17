from flask import jsonify
import requests


def send_api_request(address_validation_result):
    # Check what the validation verdict is
    if address_validation_result["result"]["verdict"]["addressComplete"] == False or address_validation_result.get["result"]["verdict"]["validationGranularity"] == "OTHER":
        # The address requires further input from the user - prompt the user to select the correct address from the list of suggestions

        # Return to the user the info about the address being invalid
        return jsonify({"addresValidationResult": "invalid"})

    elif address_validation_result["result"]["verdict"]["addressComplete"] == True and address_validation_result["result"]["verdict"]["validationGranularity"] != "OTHER" and (address_validation_result["result"]["verdict"]["hasInferredComponents"] == True or address_validation_result["result"]["verdict"]["hasReplacesComponents"] == True):
        # The address is valid but requires the confirmations from the user - prompt the user to select the desired address from the list of suggestions

        # Return to the user the info about the address being valid but requiring the confirmation from the user
        return jsonify({"addressValidationResult": "validButFurtherUserInputIsRequired"})

    elif (address_validation_result["result"]["verdict"]["validationGranularity"] != "PREMISE" or address_validation_result["result"]["verdict"]["validationGranularity"] != "SUB_PREMISE") and address_validation_result["result"]["verdict"]["addressComplete"] == True:
        # The address is valid and does not require any further input from the user

        # Return to the user the info about the address being valid
        return jsonify({"addressValidationResult": "valid"})

    else:
        # The address's status is unknown

        # Return to the user the info about the address being invalid
        return jsonify({"addressValidationResult": "unknownStatus"})
