from app.core.database import SessionLocal
from sqlalchemy import text

def ver_logo(logo_name: str):
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT tenant_id FROM logos WHERE id = :logo_name"), {"logo_name": logo_name})
        row = result.fetchone()
        if row:
            return True
    finally:
        db.close()