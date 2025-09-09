import requests
from config.env import CMC_KEY
from django.contrib.auth.models import User

url1 = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

url2 = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"



def get_crypto_data():
    headers = {
        "X-CMC_PRO_API_KEY": CMC_KEY,
        "Accept": "application/json"
    }
    response = requests.get(url1, headers=headers)
    if response.status_code == 200:
        listing = []
        data = response.json()
        for i in data['data']:
            rank = i['cmc_rank'] 
            name = i['name'] 
            id = i['id'] 
            symbol = i['symbol']
            price = float(i['quote']['USD']['price']) * 1600
            market_cap = float(i['quote']['USD']['market_cap']) * 1600
            day_ch =  i['quote']['USD']['volume_change_24h']
            single = {"id":id, "name":name, "rank":rank, "price":price, "market_cap":market_cap, "day_ch":day_ch, "symbol":symbol}
            listing.append(single)
        return listing


def get_coin_data(coin_id):
    headers = {
        "X-CMC_PRO_API_KEY": CMC_KEY,
        "Accept": "application/json"
    }
    response = requests.get(f"{url2}?id={coin_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Data is nested under coin ID string
        coin_data = data["data"][str(coin_id)]
        quote = coin_data["quote"]["USD"]

        naira_rate = 1600  # conversion factor

        return {
            "id": coin_data["id"],
            "name": coin_data["name"],
            "symbol": coin_data["symbol"],
            "price": quote["price"] * naira_rate,
            "market_cap": quote["market_cap"] * naira_rate,
            "24h_volume": quote["volume_24h"] * naira_rate,
            # Approximated high/low since this endpoint doesn't provide OHLCV
            "24h_high": (quote["price"] * (1 + (quote["percent_change_24h"] / 100))) * naira_rate,
            "24h_low": (quote["price"] * (1 - (quote["percent_change_24h"] / 100))) * naira_rate,
        }
    
    return response.text