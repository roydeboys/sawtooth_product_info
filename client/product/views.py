import os
import logging
from google.protobuf.json_format import MessageToJson, MessageToDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .thutech_client import ThutechClient
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)

KEY_NAME = 'my_key'
DEFAULT_URL = 'http://rest-api:8008'


def _get_private_keyfile(key_name):
    '''Get the private key for key_name.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, key_name)


class InsertProduct(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            product_list = serializer.data
            print(product_list)
            priv_key_file = _get_private_keyfile(KEY_NAME)
            client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
            created, response = client.add_product(product_list)
            if created:
                return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
            return Response({"status": "failed to create block"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckProduct(APIView):
    def get(self, request, product_id):
        priv_key_file = _get_private_keyfile(KEY_NAME)
        client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
        try:
            product_data = client.get_product(product_id)
            print(product_data)
            data = MessageToDict(product_data, preserving_proto_field_name=True)
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error: ", e)
            return Response({'status': 'No data found'}, status=status.HTTP_404_NOT_FOUND)




#@app.route('/api/v1/add-product/', methods=['POST'])
def add_product(request):
    if request.method == 'POST':
        product_list = request.get_json()
        if not isinstance(product_list, list):
            return {"status": "invalid data"}
        print(product_list)
        priv_key_file = _get_private_keyfile(KEY_NAME)
        client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
        created, response = client.add_product(product_list)
        logger.info(response)
        print(response)
        if created:
            return {"status": "block created successfully"}
        else:
            return {"status": "failed to create block"}
    return {"status": "get method not allowed"}


#@app.route('/api/v1/get-product/<product_id>/', methods=['GET'])
def get_product(product_id):
    priv_key_file = _get_private_keyfile(KEY_NAME)
    client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
    try:
        product_data = client.get_product(product_id)
        print(product_data)
        data = MessageToDict(product_data, preserving_proto_field_name=True)
        print(data)
        return data
    except Exception as e:
        print("error: ", e)
        return "data not found"
