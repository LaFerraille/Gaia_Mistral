import requests

data = {
    "grant_type": "client_credentials",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}

response = requests.post("https://sandbox-oauth.piste.gouv.fr/api/oauth/token", json=data)

print(response.json())
