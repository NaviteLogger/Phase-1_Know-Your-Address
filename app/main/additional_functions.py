import urllib.parse


def is_url_encoded(address):
    decoded = urllib.parse.unquote(address)
    encoded = urllib.parse.quote(decoded)

    if encoded == address:
        return True
    else:
        return False


"""
There is another way to check whether the address is already URL encoded:
def is_url_encoded(address):
    try:
        decoded = urllib.parse.unquote(address)
        encoded = urllib.parse.quote(decoded)
        return encoded == address
    except Exception as e:
        # An exception might occur if the input is not a valid URL-encoded string
        return False
"""
