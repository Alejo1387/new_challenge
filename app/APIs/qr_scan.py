from fastapi import APIRouter, Request, HTTPException

from app.services.qr_scan import scan_service

router = APIRouter()

@router.get("/scam/{qr_id}")
async def scan_qr(qr_id: str, request: Request):
    if not qr_id:
        raise HTTPException(status_code=400, detail="QR don't exist")
    
    return await scan_service(qr_id, request)