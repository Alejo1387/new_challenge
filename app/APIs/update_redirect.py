from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.models_py.models_apis import updateRedirectDataAPI
from app.models_py.models_services import updateRedirectData
from app.services.update_redirect import update_redirect_data
from app.utils.read_s3 import read_file
from app.core.security import check_api

router = APIRouter()

@router.post("/update")
async def update_redirect(data: updateRedirectDataAPI, company_id: int = Depends(check_api)):
    if not data.qr_id or not data.new_url:
        raise HTTPException(status_code=400, detail="Invalid input data")
    
    data_update = updateRedirectData(
        qr_id=data.qr_id,
        new_url=data.new_url,
        company_id=company_id
    )

    result = await update_redirect_data(data_update)

    if result:
        if result[1] == "S3":
            try:
                fileName = f"img/{result[0]}"
                file_byte = read_file(fileName)
                return StreamingResponse(
                    BytesIO(file_byte),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f"attachment; filename={result[0]}"}
                )
            except Exception as e:
                print(f"Error real de S3: {str(e)}")
                raise HTTPException(
                    status_code=404,
                    detail="File not found in S3"
                )
        elif result[1] == "local":
            try:
                file_path = f"app/img/{result[0]}"
                return FileResponse(path=file_path, filename=result[0], media_type='image/png')
            except Exception as e:
                return {"error": str(e)}
    else:
        raise HTTPException(status_code=404, detail="QR code not found")

    return {"message": "Redirect URL updated successfully"}