from pydantic import BaseModel
from typing import Optional

# for get data on body request
class QRData(BaseModel):
    url: str
    logoname: str = None

class QRCreate1(BaseModel):
    company_id: int
    url: str
    logoname: Optional[str] = None
    storage: str

class QRCreate2(BaseModel):
    company_id: int
    url: str
    logoname: Optional[str] = None
    storage: str
    fileName: str
    server_url: str
    logo_storage: str