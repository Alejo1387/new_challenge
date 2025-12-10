from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, HTTPException
from app.core.database import SessionLocal
from sqlalchemy import text

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def check_api(api_key: str = Depends(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API KEY requerida")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT id FROM companies WHERE api_key = :api_key"), {"api_key": api_key})

        row = result.fetchone()
        if row:
            return row[0]
        else:
            raise HTTPException(status_code=401, detail="API KEY inválida")
    finally:
        db.close()