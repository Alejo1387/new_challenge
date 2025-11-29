"""
FastAPI for create servidor
Request for read information of client
HTTPException for throw errors with HTTP codes
"""
from fastapi import FastAPI, Request, HTTPException
# for redirect to other URL
from fastapi.responses import RedirectResponse, JSONResponse
# for connect with DB
import sqlite3
# for get results of others APIs
import requests
# for get the time
from datetime import datetime
# archive for create Qr
from Qr_generator import qrs

app = FastAPI()

def get_db():
    # check_same_thread=False this is for don't have error in diferents conexions
    conn = sqlite3.connect("mi_base.db", check_same_thread=False)
    # this is for get rows by name 
    conn.row_factory = sqlite3.Row
    return conn

# for get the data
def get_geo_ip(ip):
    try:

        # https://ipapi.com/pricing 100 free requests per month (We need a different)
        url = f"https://ipapi.co/{ip}/json/"
        # timeout=5 avoid error in the API
        response = requests.get(url, timeout=5)
        data = response.json()

        return {
            "country": data.get("country_name"),
            "city": data.get("city"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    except:
        return None
    
# it's the API-KEY
X_API_KEY = "G7pK3wQ9"

# funtion for check passwork api
def check_api(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != X_API_KEY:
        raise HTTPException(status_code=401, detail="API KEY inválida")
    return True


""" ---------- APIs ---------- """
@app.get("/scam/{qr_id}")
async def scan_qr(qr_id: str, request: Request):
    try:
        # 1. get IP
        ip_client = request.client.host

        # print(ip_client)

        # 2. get User-Agent (type of device)
        user_agent = request.headers.get("user-agent")

        # 3. get geolocation for IP
        geo = get_geo_ip(ip_client)

        # 4. Conexión BD
        db = get_db()
        cursor = db.cursor()

        # 5. get original URL
        cursor.execute("SELECT destination_url FROM qrs WHERE unique_id = ?", (qr_id,))
        # return first row
        data = cursor.fetchone()

        if not data:
            raise HTTPException(status_code=404, detail="QR no encontrado")

        url_destino = data["destination_url"]
        present_date = datetime.now()

        # 6. Guardar los datos del escaneo
        cursor.execute("""
            INSERT INTO users_scam (qr_id, ip, device, country, city, latitude, longitude, datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            qr_id,
            ip_client,
            user_agent,
            geo["country"] if geo else None,
            geo["city"] if geo else None,
            geo["latitude"] if geo else None,
            geo["longitude"] if geo else None,
            present_date
        ))

        db.commit()
        db.close()

        # 7. Redirigir
        return RedirectResponse(url=url_destino)

    except Exception as e:
        # return error
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/create")
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