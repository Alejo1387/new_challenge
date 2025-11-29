import requests

url_api = "http://127.0.0.1:8000/create"
api_key = "G7pK3wQ9"

data = {
    "url" : "https://www.youtube.com/",
    "name" : "Youtube",
    "logoname" : "logoYoutube.png"
}

headers = {
    "X-API-KEY" : api_key,
    "Content-Type": "application/json"
}

response = requests.post(url_api, json=data, headers=headers)

print("Código:", response.status_code)
print("Respuesta:", response.json())