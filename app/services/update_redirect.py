from sqlalchemy import text

from app.models_py.models_services import updateRedirectData
from app.core.database import SessionLocal

async def update_redirect_data(data: updateRedirectData):
    db = SessionLocal()
    try:
        db.execute(text("""
            UPDATE qrs SET destination_url = :new_url WHERE tenant_id = :tenant_id AND unique_id = :qr_id
        """), {"new_url": data.new_url, "tenant_id": data.company_id, "qr_id": data.qr_id})

        search = db.execute(text("""
            SELECT qr_name, storage FROM qrs WHERE tenant_id = :tenant_id AND unique_id = :qr_id
        """), {"tenant_id": data.company_id, "qr_id": data.qr_id})

        row = search.fetchone()
        db.commit()
    finally:
        db.close()
    
    return row