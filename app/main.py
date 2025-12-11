from fastapi import FastAPI
from app.APIs.qr_create import router as qr_create_router
from app.APIs.qr_scan import router as qr_scan_router


app = FastAPI()

# For create QR codes
app.include_router(qr_create_router, prefix="/qr", tags=["QR Create"])

# for scan QR codes
app.include_router(qr_scan_router, prefix="/qr", tags=["QR Scan"])