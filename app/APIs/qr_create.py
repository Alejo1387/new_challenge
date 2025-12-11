from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.Qr_model import QRData
from app.core.security import check_api
from app.services.qr_generator import qrs

router = APIRouter()

@router.post("/create")
async def create_qr(CreateData: QRData, company_id: int = Depends(check_api)):
    if not CreateData.url or not CreateData.name:
        raise HTTPException(status_code=400, detail="url and name are requared")
    
    qrs(company_id, CreateData.url, CreateData.name, CreateData.logoname)
    # print(url, name, logoname)

    return {
        "message" : "QR create"
    }