from pydantic import BaseModel

# for get data on body request
class QRData(BaseModel):
    url: str
    name: str
    logoname: str = None