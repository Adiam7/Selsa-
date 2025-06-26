# printful_sync/services.py

import requests
from django.conf import settings
# printful_sync/services.py

def get_stores():
    url = "https://api.printful.com/stores"
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        raise Exception(f"Error getting stores: {response.text}")


# printful_sync/services.py

def fetch_printful_products(store_id):  # ✅ Make sure store_id is included here
    url = f"https://api.printful.com/stores/{store_id}/products"
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        raise Exception(f"Printful API error {response.status_code}: {response.text}")

def test_store_exists(store_id):
    url = f"https://api.printful.com/store/products?store_id='{store_id}'"
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    print(response.status_code, response.text)