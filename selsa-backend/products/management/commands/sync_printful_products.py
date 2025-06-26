# products/management/commands/sync_printful_products.py

import requests
from django.core.management.base import BaseCommand
from products.models import Product, Variant

API_KEY = 'your_printful_api_key_here'

class Command(BaseCommand):
    help = 'Sync Printful products to local DB'

    def handle(self, *args, **kwargs):
        headers = {'Authorization': f'Bearer {API_KEY}'}
        response = requests.get('https://api.printful.com/sync/products', headers=headers)

        if response.status_code == 200:
            data = response.json().get('result', [])
            for item in data:
                external_id = item['id']
                name = item['name']
                thumbnail = item['thumbnail_url']
                product, created = Product.objects.update_or_create(
                    printful_id=external_id,
                    defaults={'name': name, 'thumbnail': thumbnail, 'currency': 'USD'}
                )

                # Fetch variants
                variant_resp = requests.get(f'https://api.printful.com/sync/products/{external_id}', headers=headers)
                if variant_resp.status_code == 200:
                    variants = variant_resp.json().get('result', {}).get('variants', [])
                    Variant.objects.filter(product=product).delete()
                    for var in variants:
                        Variant.objects.create(
                            product=product,
                            variant_id=var['id'],
                            name=var['name'],
                            sku=var['sku'],
                            price=var['retail_price'],
                        )
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch products'))
