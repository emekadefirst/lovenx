import orjson
import requests
from config.env import PAYSTACK_KEY 




def initialize_payment(email, amount):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_KEY}",
        "Content-Type": "application/json"
    }

    data  = {
        "email": email,
        "amount": amount * 100
    }

    response = requests.post(url, data=orjson.dumps(data), headers=headers)
    if response.status_code == 200:
        data = response.json()
        url = data['data']['authorization_url']
        reference = data['data']['reference']
        return url, reference
    return response.text



print(initialize_payment("davidumasor18@gmail.com", 5000))