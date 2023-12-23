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
def is_url_encoded(s):
    try:
        decoded = urllib.parse.unquote(s)
        encoded = urllib.parse.quote(decoded)
        return encoded == s
    except Exception as e:
        # An exception might occur if the input is not a valid URL-encoded string
        return False
"""
