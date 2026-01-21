from fastapi import FastAPI

from app.APIs.qr_create import router as qr_create_router
from app.APIs.qr_scan import router as qr_scan_router
from app.APIs.save_logo import router as save_logo_router
from app.APIs.update_redirect import router as update_redirect_router


app = FastAPI()

# For create QR codes
app.include_router(qr_create_router)

# for scan QR codes
app.include_router(qr_scan_router)

# for save logo files
app.include_router(save_logo_router)

# for update redirect URLs
app.include_router(update_redirect_router)

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok"}