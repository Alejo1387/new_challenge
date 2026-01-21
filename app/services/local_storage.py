from fastapi import UploadFile
from sqlalchemy import text

from app.utils.create_name_file import create_unique
from app.core.database import SessionLocal

upload_dir = "app/logos"

async def save_file(file: UploadFile, filename: str, tenant_id: str):
    unique_id = create_unique()

    extencion = filename.split(".")[-1]

    new_name = f"{unique_id}.{extencion}"

    file_location = f"{upload_dir}/{new_name}"

    content = await file.read()

    with open(file_location, "wb+") as f:
        f.write(content)
    
    db = SessionLocal()
    
    try:
        db.execute(text("""
            INSERT INTO logos (id, tenant_id, storage) VALUES (:id, :tenant_id, :storage)
        """), {"id": new_name, "tenant_id": tenant_id, "storage": "Local"})
        db.commit()
    finally:
        db.close()

    return new_name