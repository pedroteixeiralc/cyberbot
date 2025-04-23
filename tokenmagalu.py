import requests

url = "https://api.magalu.com/oauth/token"
client_id = "223a23af-c0b3-4ee9-a2b4-2c2eb3cc19ef"
client_secret = "40b7162f-aec3-4147-9dac-4947c24e4dd5"

payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "open:portfolio-skus-seller:read"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    token = response.json()["access_token"]
    print("TOKEN:", token)
else:
    print("Erro ao gerar token:", response.status_code, response.text)
