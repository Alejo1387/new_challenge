from pydantic import BaseModel

# for get data on body request
class QRData(BaseModel):
    url: str
    logoname: str = None