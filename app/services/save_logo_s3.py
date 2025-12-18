from app.core.s3 import get_s3_client
from app.utils.create_name_file import create_unique
from app.core.database import SessionLocal
from sqlalchemy import text

async def save_logo_s3(file, filename, tenant_id):
    s3 = get_s3_client()
    db = SessionLocal()

    unique_id = create_unique()
    extencion = filename.split(".")[-1]
    new_name = f"logos/{unique_id}.{extencion}"

    content = await file.read()

    s3.put_object(
        Bucket="my-test-bucket",
        Key=new_name,
        Body=content
    )

    try:
        db.execute(text("""
            INSERT INTO logos (id, tenant_id, storage) VALUES (:id, :tenant_id, :storage)
        """), {"id": new_name, "tenant_id": tenant_id, "storage": "S3"})
        db.commit()
    finally:
        db.close()

    return new_name