from urllib.parse import urlparse

def validate_url(url):
    validate = urlparse(url)
    # validate if contain http or https
    return validate.scheme in ("http", "https") and validate.netloc != ""