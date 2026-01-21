from pydantic import BaseModel

class updateRedirectDataAPI(BaseModel):
    qr_id: str
    new_url: str

class dataCreateQr(BaseModel):
    url: str
    logoname: str = None