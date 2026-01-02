from pydantic import BaseModel
from typing import Optional

class QRCreate2(BaseModel):
    company_id: int
    url: str
    logoname: Optional[str] = None
    storage: str
    fileName: str
    server_url: str
    logo_storage: str