from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from Qr_generator import qrs

app = FastAPI()

# it's the API-KEY
X_API_KEY = "G7pK3wQ9"

# funtion for check passwork api
def check_api(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != X_API_KEY:
        raise HTTPException(status_code=401, detail="API KEY inválida")
    return True

@app.post("/create_qr")
async def create_qr(request: Request):
    # verify api key
    check_api(request)

    # it's for get data
    data = await request.json()

    url = data.get("url")
    name = data.get("name")
    logoname = data.get("logoname")

    # check data
    if not url or not name:
        raise HTTPException(status_code=400, detail="url and name are requared")
    
    qrs(url, name, logoname)
    # print(url, name, logoname)

    return JSONResponse({
        "message" : "QR create"
    })