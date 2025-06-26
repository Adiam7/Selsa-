# printful_sync/views.py

from django.http import JsonResponse
from .services import fetch_printful_products
from .services import get_stores
from django.conf import settings
import requests
from django.http import JsonResponse

def list_stores_view(request):
    try:
        stores = get_stores()
        return JsonResponse(stores, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def sync_printful_view(request):
    try:
        store_id = 13074277  # ⬅️ Replace with your actual store ID (as an integer)
        products = fetch_printful_products(store_id)
        return JsonResponse(products, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def debug_store_view(request):
    store_id = 13074277  # Replace with your actual native/API store ID
    url = f"https://api.printful.com/stores/{store_id}"
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    try:
        return JsonResponse(response.json(), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.http import JsonResponse
from .services import test_store_exists

# printful_sync/services.py

def test_store_exists(store_id):
    url = f"https://api.printful.com/stores/{store_id}"
    headers = {
        "Authorization": f"Bearer {settings.PRINTFUL_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Printful API error {response.status_code}: {response.text}")
