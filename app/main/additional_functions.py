import urllib.parse


def is_url_encoded(address):
    decoded = urllib.parse.unquote(address)
    encoded = urllib.parse.quote(decoded)

    if encoded == address:
        return True
    else:
        return False
