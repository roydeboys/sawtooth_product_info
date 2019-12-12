import os
import logging
import hashlib
from google.protobuf.json_format import MessageToJson, MessageToDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from subscriber.models import BlockInfo
from .thutech_client import ThutechClient
from .serializers import ProductSerializer
from subscriber.serializers import BlockInfoSerializer

logger = logging.getLogger(__name__)

KEY_NAME = 'my_key'
DEFAULT_URL = 'http://rest-api:8008'

FAMILY_NAME = 'thutech_subscriber'
FAMILY_VERSION = '1.0'
NAMESPACE = hashlib.sha512(FAMILY_NAME.encode('utf-8')).hexdigest()[:6]


def get_product_address(product_id):
    return NAMESPACE + hashlib.sha512(
        product_id.encode('utf-8')).hexdigest()[:64]


def _get_private_keyfile(key_name):
    '''Get the private key for key_name.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, key_name)


def insert_product_to_blockchain(product_list):
    priv_key_file = _get_private_keyfile(KEY_NAME)
    client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
    # remove CreatedDate from product info
    return client.add_product(product_list)


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
    permission_classes = ()

    def get(self, request, product_id):
        priv_key_file = _get_private_keyfile(KEY_NAME)
        client = ThutechClient(base_url=DEFAULT_URL, key_file=priv_key_file)
        try:
            product_data = client.get_product(product_id)
            product_data = MessageToDict(product_data, preserving_proto_field_name=True)
            product_address = get_product_address(product_id)
            try:
                block_obj = BlockInfo.objects.get(address=product_address)
                serializer = BlockInfoSerializer(block_obj)
                block_data = serializer.data
            except:
                block_data = None
            data = {
                "block_data": block_data,
                "product_data": product_data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({'status': 'No data found'}, status=status.HTTP_404_NOT_FOUND)


