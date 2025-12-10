from app.core.database import SessionLocal
from sqlalchemy import text
from app.utils.create_uuid import create_unique

def save_data_user(qr_id, ip_client, user_agent, present_date, geo):
    db = SessionLocal()
    unique_id = create_unique()
    try:
        exists = db.execute(text("""
            SELECT id FROM users_scam
            WHERE id_unique = :qr_id AND ip = :ip
            ORDER BY datetime DESC
            LIMIT 1
        """), {
            "qr_id": qr_id,
            "ip": ip_client
        }).fetchone()

        if exists:
             return
        else:
            db.execute(text("""
                INSERT INTO users_scam (id_unique, ip, device, datetime, unique_id)
                VALUES (:id_unique, :ip, :device, :datetime, :unique_id)
            """), {
                "id_unique": qr_id,
                "ip": ip_client,
                "device": user_agent,
                "datetime": present_date,
                "unique_id": unique_id
            })

            get_user = db.execute(text("""
                SELECT id FROM users_scam WHERE unique_id = :unique_id
            """), {"unique_id": unique_id})
            row = get_user.fetchone()
            id_users_scam = row[0]

            db.execute(text("""
                INSERT INTO geo_registers (id_users_scam, geo_name, country, city, latitude, longitude)
                VALUES (:id_users_scam, :geo_name, :country, :city, :latitude, :longitude)
            """), {
                "id_users_scam": id_users_scam,
                "geo_name": "ipapi.co",
                "country": geo["country_ipapi"] if geo else None,
                "city": geo["city_ipapi"] if geo else None,
                "latitude": geo["latitude_ipapi"] if geo else None,
                "longitude": geo["longitude_ipapi"] if geo else None,
            })

            db.execute(text("""
                INSERT INTO geo_registers (id_users_scam, geo_name, country, city, latitude, longitude)
                VALUES (:id_users_scam, :geo_name, :country, :city, :latitude, :longitude)
            """), {
                "id_users_scam": id_users_scam,
                "geo_name": "GeoLite2",
                "country": geo["country_geolite"] if geo else None,
                "city": geo["city_geolite"] if geo else None,
                "latitude": geo["latitude_geolite"] if geo else None,
                "longitude": geo["longitude_geolite"] if geo else None,
            })

            db.execute(text("""
                INSERT INTO geo_registers (id_users_scam, geo_name, country, city, latitude, longitude)
                VALUES (:id_users_scam, :geo_name, :country, :city, :latitude, :longitude)
            """), {
                "id_users_scam": id_users_scam,
                "geo_name": "ip-api.com",
                "country": geo["country_ip_api"] if geo else None,
                "city": geo["city_ip_api"] if geo else None,
                "latitude": geo["latitude_ip_api"] if geo else None,
                "longitude": geo["longitude_ip_api"] if geo else None,
            })
        db.commit()
    finally:
            db.close()