from PIL import Image
from io import BytesIO
import qrcode

from app.models_py.models_utils import QRCreate2
from app.utils.read_s3 import read_file
from app.services.save_img_s3 import upload_qr

def create_qr(qr_data: QRCreate2):
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
    qr_code.add_data(qr_data.server_url)
    qr_code.make(fit=True)
    qr_img = qr_code.make_image(fill_color="black", back_color="white").convert("RGB")

    if qr_data.logoname is not None:
        if qr_data.logo_storage == "S3":
            try:
                logo_bytes = read_file(qr_data.logoname)

                logo = Image.open(BytesIO(logo_bytes))

                qr_width, qr_height = qr_img.size
                logo_size = int(qr_width * 0.25)

                logo = logo.resize((logo_size, logo_size))
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                
                qr_img.paste(logo, pos)
            except Exception as e:
                print("⚠ Error loading logo from S3")
                print("Details:", e)
            
            if qr_data.storage == "S3":
                img_bytes = BytesIO()
                qr_img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                qr_filename = f"{qr_data.fileName}.png"
                upload_qr(img_bytes.read(), qr_filename)
            else:
                save_img = f"app/img/{qr_data.fileName}.png"
                qr_img.save(save_img)
        else:
            logoA = f"app/logos/{qr_data.logoname}"
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

            if qr_data.storage == "S3":
                img_bytes = BytesIO()
                qr_img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                qr_filename = f"{qr_data.fileName}.png"
                upload_qr(img_bytes.read(), qr_filename)
            else:
                save_img = f"app/img/{qr_data.fileName}.png"
                qr_img.save(save_img)
    else:
        if qr_data.storage == "S3":
            img_bytes = BytesIO()
            qr_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            qr_filename = f"{qr_data.fileName}.png"
            upload_qr(img_bytes.read(), qr_filename)
        else:
            save_img = f"app/img/{qr_data.fileName}.png"
            qr_img.save(save_img)