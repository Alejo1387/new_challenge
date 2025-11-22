import qrcode
from urllib.parse import urlparse

def validate_url(url):
    validate = urlparse(url)
    return validate.scheme in ("http", "https") and validate.netloc != ""

def qr(url, fileName):
    if(validate_url(url)):
        save_img = "img/" + (fileName + ".png")
        img = qrcode.make(url)
        img.save(save_img)
        print("qr generado")
    else:
        print("URL mal escrita")

qr("https://www.youtube.com/", "Youtube")
