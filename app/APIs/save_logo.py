from fastapi import APIRouter, Request, HTTPException, Depends, UploadFile, File
from app.core.security import check_api
from app.services.local_storage import save_file
from app.services.save_logo_s3 import save_logo_s3

router = APIRouter()
storage = "Local"

@router.post("/save")
async def save_logo(file: UploadFile = File(...), tenant_id: int = Depends(check_api)):
    if not file:
        raise HTTPException(status_code=400, detail="File is required")
    
    filename = file.filename

    if storage == "Local":
        new_logoname = await save_file(file, filename, tenant_id)
        return {
            "message" : "Logo saved successfully",
            "name" : f"{new_logoname}"
        }
    else:
        new_logoname = await save_logo_s3(file, filename, tenant_id)
        return {
            "message" : "Logo saved successfully",
            "backup" : f"s3://my-test-bucket/{new_logoname}",
            "name": new_logoname
        }