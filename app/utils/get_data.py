from app.utils.get_geo import get_geo_ip
from datetime import datetime
from app.services.save_data import save_data_user

def get_data_user(qr_id, ip_client, user_agent):
    geo = get_geo_ip(ip_client)
    present_date = datetime.now()

    save_data_user(qr_id, ip_client, user_agent, present_date, geo)
    
