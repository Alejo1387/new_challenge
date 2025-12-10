import requests
import geoip2.database

def get_geo_ip(ip):
    try:
        """ Geolocation with apapi.co API """
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url, timeout=5)
        data_ipapi = response.json()

        """ Geolocation with GeoLite2 database """
        reader = geoip2.database.Reader("app/resources/GeoLite2-City.mmdb")
        data_geolite = reader.city(ip)

        """ Geolocation with ip-api.com API """
        url2 = f"http://ip-api.com/json/{ip}"
        data_ip_api = requests.get(url2, timeout=5).json()

        return {
            "country_ipapi": data_ipapi.get("country_name"),
            "city_ipapi": data_ipapi.get("city"),
            "latitude_ipapi": data_ipapi.get("latitude"),
            "longitude_ipapi": data_ipapi.get("longitude"),

            "country_geolite": data_geolite.country.name,
            "city_geolite": data_geolite.city.name,
            "latitude_geolite": data_geolite.location.latitude,
            "longitude_geolite": data_geolite.location.longitude,

            "country_ip_api": data_ip_api.get("country"),
            "city_ip_api": data_ip_api.get("city"),
            "latitude_ip_api": data_ip_api.get("lat"),
            "longitude_ip_api": data_ip_api.get("lon"),
        }

    except:
        return None