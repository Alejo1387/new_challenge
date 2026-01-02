from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.models_apis import dataCreateQr
from app.models.models_services import QRCreate1
from app.core.security import check_api
from app.services.qr_generator import qrs
from app.services.verify_logo import ver_logo
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.utils.read_s3 import read_file

router = APIRouter()
storage = "S3"

@router.post("/create")
async def create_qr(CreateData: dataCreateQr, company_id: int = Depends(check_api)):
    
    if CreateData.logoname:
        logo_exist = ver_logo(CreateData.logoname)
        if not logo_exist:
            raise HTTPException(status_code=404, detail="Logo not found")
    
    Qrcreate = QRCreate1(
        company_id=company_id,
        url=CreateData.url,
        logoname=CreateData.logoname,
        storage=storage
    )

    
    result = qrs(Qrcreate)
    # print(url, name, logoname)

    if result[0] == "URL don't valid":
        raise HTTPException(status_code=400, detail="URL is not valid")
    else:
        if result[0] == "Local":
            file_relative_path = result[1]
            file_name = file_relative_path.split("/")[-1]
            file_path = f"app/{file_relative_path}"
            try:
                                                                                  # application/octet-stream
                return FileResponse(path=file_path, filename=file_name, media_type='image/png')
            except Exception as e:
                return {"error": str(e)}
        else:
            try:
                file_byte = read_file(result[1])
                return StreamingResponse(
                    BytesIO(file_byte),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f"attachment; filename={result[1]}"}
                )
            except Exception:
                raise HTTPException(
                    status_code=404,
                    detail="File not found in S3"
                )