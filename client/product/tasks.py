import datetime
from django.conf import settings
from celery import shared_task
from .saleforce import SaleforceProduct
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
        ProductQue.objects.create(date=datetime.datetime.now())
        print("que created")
    except Exception as e:
        print(str(e))
        pass

    # Get all unresolved que, including today's que
    que_list = ProductQue.objects.filter(is_resolved=False)
    print("Que list is: ", que_list)

    for que in que_list:
        print(que.date)
        # get product list from saleforces api
        try:
            product_obj = SaleforceProduct(client_id=client_id, client_secret=client_secret,
                                           refresh_token=refresh_token)
            products = product_obj.get_products(que.date)
            print("products: ", products)
            if products:
                # insert products to blockchanin
                is_inserted, response = insert_product_to_blockchain(products)
                if is_inserted:
                    que.mark_resolved(response)
                else:
                    # store blockchain error status to db
                    que.mark_unresolved(response)
            else:
                # If no data found, mark as resolved
                que.mark_resolved(status="No data Found in saleforce")
        except ConnectionError as e:
            # mark unresolved with status
            que.mark_unresolved(e)
        except Exception as e:
            que.mark_unresolved(e)

