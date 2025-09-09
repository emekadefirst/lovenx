import orjson
import requests
from config.env import PAYSTACK_KEY 




def initialize_payment(email, amount):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "amount": int(amount) * 100  # Paystack expects amount in kobo
    }

    response = requests.post(url, data=orjson.dumps(data), headers=headers)

    try:
        data = response.json()
    except Exception:
        return {"error": "Invalid response from Paystack", "details": response.text}

    if response.status_code == 200 and data.get("status") is True:
        return {
            "url": data['data']['authorization_url'],
            "reference": data['data']['reference']
        }

    # Always return dict with error
    return {
        "error": "Failed to initialize payment",
        "details": data
    }


def verify_payment(reference):
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        "Authorization": f"Bearer {PAYSTACK_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url,  headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            'status': data['data']['status'],
            'reference': data['data']['reference']
        }
    return data['message']