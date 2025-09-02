import requests
from config.env import CMC_KEY


url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"



def get_crypto_data():
    headers = {
        "X-CMC_PRO_API_KEY": CMC_KEY,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return response.text