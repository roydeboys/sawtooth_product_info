from django.conf import settings
from celery import shared_task
from .saleforce import Product

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
refresh_token = settings.REFRESH_TOKEN


@shared_task
def collect_and_store_products():
    product_obj = Product(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
    products = product_obj.get_products()
    print(products)

