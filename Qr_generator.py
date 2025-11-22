import qrcode
from urllib.parse import urlparse
from PIL import Image

# function for validate url
def validate_url(url):
    validate = urlparse(url)
    # validate if contain http or https
    return validate.scheme in ("http", "https") and validate.netloc != ""

# function for make qrs
def qrs(url, fileName, logo_archive=None):
    if(validate_url(url)):
        # advanced settings
        qr_code = qrcode.QRCode(
            # size of qr
            version=1,
            # for qr with logo
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            # size of each QR code
            box_size=10,
            # size of border
            border=4,
        )

        # insert URL to image
        qr_code.add_data(url)
        # adjust the size
        qr_code.make(fit=True)

        # make image of qr
        qr_img = qr_code.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo_archive is not None:
            logoA = f"logos/{logo_archive}"
            try:
                # open the image with pollow
                logo = Image.open(logoA)

                # resize the logo
                qr_width, qr_height = qr_img.size
                logo_size = int(qr_width * 0.25)

                logo = logo.resize((logo_size, logo_size))

                # center the logo
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

                # paste the logo
                qr_img.paste(logo, pos)

            except Exception as e:
                print("⚠ Hubo un error cargando el logo, se generará sin logo.")
                print("Detalles:", e)

        # save img
        save_img = "img/" + (fileName + ".png")
        qr_img.save(save_img)

        # img = qrcode.make(url)
        # img.save(save_img)
        print("qr generado")
    else:
        print("URL mal escrita")


# url = "https://www.youtube.com/"
# name = "Youtube"
# logoName = "logoYoutube.png"

# qrs(url, name, logoName)

url = "https://www.speedtest.net/"
name = "Speedtest"
qrs(url, name)