from fastapi import FastAPI, Request, HTTPException, Depends
from app.models.Qr_model import QRData
from app.core.security import check_api
from fastapi.responses import JSONResponse
from app.services.qr_generator import qrs
from app.services.qr_scan import scan_service

app = FastAPI()

@app.post("/create")
async def create_qr(CreateData: QRData, company_id: int = Depends(check_api)):
    if not CreateData.url or not CreateData.name:
        raise HTTPException(status_code=400, detail="url and name are requared")
    
    qrs(company_id, CreateData.url, CreateData.name, CreateData.logoname)
    # print(url, name, logoname)

    return {
        "message" : "QR create"
    }

@app.get("/scam/{qr_id}")
async def scan_qr(qr_id: str, request: Request):
    if not qr_id:
        raise HTTPException(status_code=400, detail="QR don't exist")
    
    return await scan_service(qr_id, request)