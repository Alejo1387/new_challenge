from fastapi import APIRouter, Request, HTTPException, Depends, UploadFile, File
from app.core.security import check_api
from app.services.local_storage import save_file

router = APIRouter()

@router.post("/save")
async def save_logo(file: UploadFile = File(...), tenant_id: int = Depends(check_api)):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")
    
    filename = file.filename

    new_logoname = await save_file(file, filename, tenant_id)

    return {
        "message" : "Logo saved successfully",
        "name": new_logoname
    }