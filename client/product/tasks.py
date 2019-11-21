from django.conf import settings
from celery import shared_task
from .saleforce import Product
from .models import ProductQue
from .views import insert_product_to_blockchain

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
refresh_token = settings.REFRESH_TOKEN


@shared_task
def collect_and_store_products():
    """
    A celery task that will run every day at 11.59 pm, collect product data from saleforce API
    and store to blockchain
    algorithm:
        1. Create a blank QUE first
        2. filter all Que that is not resolved
        3. Call saleforce API with que date
        4. If no product found with particular date, resolve the que
        5. If product list found, store data to blockchain
        6. if blockchain data store success, resolve the que
    :return:
    """
    try:
        # Create new que first for today's que
        ProductQue.objects.create()
        print("que created")
    except:
        print("que already exists, passing....")
        pass

    # Get all unresolved que, including today's que
    que_list = ProductQue.objects.filter(is_resolved=False)
    print("Que list is: ", que_list)
    try:
        # Init saleforce product api
        product_obj = Product(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
        if que_list:
            print("in if que")
            for que in que_list:
                print(que.date)
                # get product list from saleforces api
                products = product_obj.get_products(que.date)
                print("products: ", products)
                if products:
                    # insert products to blockchanin
                    response = insert_product_to_blockchain(products)
                    print("response")
                    if response == "SUCCESS":
                        que.mark_resolved()
                    pass
                else:
                    que.mark_resolved()
        else:
            print("No que found..")
    except ConnectionError as e:
        print(e)
        pass
    except Exception as e:
        print(e)
        # TODO: use logger
        pass
