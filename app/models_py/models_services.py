from pydantic import BaseModel
from typing import Optional

class updateRedirectData(BaseModel):
    qr_id: str
    new_url: str
    company_id: int

class QRCreate1(BaseModel):
    company_id: int
    url: str
    logoname: Optional[str] = None
    storage: str