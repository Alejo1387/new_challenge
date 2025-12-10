import qrcode
from PIL import Image
from app.core.va_url import validate_url
from app.utils.create_uuid import create_unique
from app.core.database import SessionLocal
from sqlalchemy import text

def qrs(company_id, url, fileName, logo_archive=None):
    if(validate_url(url)):
        db = SessionLocal()

        unique_id = create_unique()
        server_url = f"http://127.0.0.1:8000/scam/{unique_id}"

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

        qr_code.add_data(server_url)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo_archive is not None:
            logoA = f"app/logos/{logo_archive}"
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

        save_img = "app/img/" + (fileName + ".png")
        qr_img.save(save_img)

        try:
            db.execute(text("""
                INSERT INTO qrs (tenant_id, logo_name, qr_name, destination_url, server_url, unique_id)
                VALUES (:tenant_id, :logo_name, :qr_name, :destination_url, :server_url, :unique_id)
            """), {
                "tenant_id" : company_id,
                "logo_name" : logo_archive,
                "qr_name" : f"{fileName}.png",
                "destination_url" : url,
                "server_url" : server_url,
                "unique_id" : unique_id
            })
            db.commit()
            print(f"qr generado para el id de la company: {company_id}")
        finally:
            db.close()
    else:
        print("URL mal escrita")