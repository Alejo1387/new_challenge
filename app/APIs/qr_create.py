from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.Qr_model import QRData
from app.core.security import check_api
from app.services.qr_generator import qrs
from app.services.verify_logo import ver_logo

router = APIRouter()

@router.post("/create")
async def create_qr(CreateData: QRData, company_id: int = Depends(check_api)):
    
    if CreateData.logoname:
        logo_exist = ver_logo(CreateData.logoname)
        if not logo_exist:
            raise HTTPException(status_code=404, detail="Logo not found")
    
    result = qrs(company_id, CreateData.url, CreateData.logoname)
    # print(url, name, logoname)

    if result == "URL don't valid":
        raise HTTPException(status_code=400, detail="URL is not valid")

    return {
        "message" : "QR create"
    }