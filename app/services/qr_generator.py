import qrcode
from PIL import Image
from app.core.va_url import validate_url
from app.utils.create_uuid import create_unique
from app.core.database import SessionLocal
from sqlalchemy import text
from app.utils.create_name_file import create_unique as create_name_file
from app.utils.qr_create import create_qr
from app.models.models_services import QRCreate1
from app.models.models_utils import QRCreate2

def qrs(qr_data: QRCreate1):
    if(validate_url(qr_data.url)):
        db = SessionLocal()
        get_storage = db.execute(text("""
            SELECT storage FROM logos WHERE id = :logo_id
        """), {"logo_id" : qr_data.logoname})

        row = get_storage.fetchone()

        fileName = create_name_file()

        unique_id = create_unique()
        server_url = f"http://127.0.0.1:8000/scam/{unique_id}"

        Qrcreate2 = QRCreate2(
            company_id=qr_data.company_id,
            url=qr_data.url,
            logoname=qr_data.logoname,
            storage=qr_data.storage,
            fileName=fileName,
            server_url=server_url,
            logo_storage=row[0]
        )
        
        create_qr(Qrcreate2)

        try:
            db.execute(text("""
                INSERT INTO qrs (tenant_id, logo_name, qr_name, destination_url, server_url, unique_id, storage)
                VALUES (:tenant_id, :logo_name, :qr_name, :destination_url, :server_url, :unique_id, :storage)
            """), {
                "tenant_id" : qr_data.company_id,
                "logo_name" : qr_data.logoname,
                "qr_name" : f"{fileName}.png",
                "destination_url" : qr_data.url,
                "server_url" : server_url,
                "unique_id" : unique_id,
                "storage" : qr_data.storage
            })
            db.commit()
            print(f"qr generado para el id de la company: {qr_data.company_id}")
            return [qr_data.storage, f"img/{fileName}.png"]
        finally:
            db.close()
    else:
        return ["URL don't valid"]