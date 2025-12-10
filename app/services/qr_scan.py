from fastapi import HTTPException
import asyncio
from app.utils.get_data import get_data_user
from app.core.database import SessionLocal
from sqlalchemy import text
from fastapi.responses import RedirectResponse

async def scan_service(qr_id, request):
    try:
        ip_client = request.client.host

        user_agent = request.headers.get("user-agent")

        asyncio.create_task(asyncio.to_thread(
            get_data_user, qr_id, ip_client, user_agent
        ))

        db = SessionLocal()

        try:
            get_url = db.execute(text("""
                SELECT destination_url FROM qrs WHERE unique_id = :qr_id
            """), {"qr_id": qr_id})

            row = get_url.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="QR no encontrado")
            
            url_destinate = row[0]

            return RedirectResponse(url=url_destinate)
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))