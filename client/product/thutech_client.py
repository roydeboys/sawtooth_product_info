import hashlib
import base64
import random
import time
import requests
import yaml
from os import sys, path

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch

# get project path (thutech_subscriber)
TOP_DIR = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))

# set folder to python-path for relative import
sys.path.insert(0, path.join(TOP_DIR, 'addressing'))
sys.path.insert(0, path.join(TOP_DIR, 'protobuf'))

from thutech_addressing import addresser
from thutech_protobuf import payload_pb2


# custom exception
class TransactionNotFound(Exception):
    pass


# The Transaction Family Name
FAMILY_NAME = 'thutech_subscriber'
FAMILY_VERSION = '1.0'
# TF Prefix is first 6 characters of SHA-512("cookiejar"), a4d219


def _hash(data):
    return hashlib.sha512(data).hexdigest()


class ThutechClient(object):
    """Client Thutech class
    Supports -- functions.
    """

    def __init__(self, base_url, key_file=None):
        """Initialize the rest_api class.
           This is mainly getting the key pair and computing the address.
        """
        self._base_url = base_url

        if key_file is None:
            self._signer = None
            return

        try:
            with open(key_file) as key_fd:
                private_key_str = key_fd.read().strip()
        except OSError as err:
            raise Exception(
                'Failed to read private key {}: {}'.format(
                    key_file, str(err)))

        try:
            private_key = Secp256k1PrivateKey.from_hex(private_key_str)
        except ParseError as err:
            raise Exception( \
                'Failed to load private key: {}'.format(str(err)))

        self._signer = CryptoFactory(create_context('secp256k1')) \
            .new_signer(private_key)
        self._public_key = self._signer.get_public_key().as_hex()

        # Address is 6-char TF prefix + hash of "mycookiejar"'s public key
        self._client_address = _hash(FAMILY_NAME.encode('utf-8'))[0:6] + \
            _hash(self._public_key.encode('utf-8'))[0:64]

    def is_product_already_exist(self, product_address):
        url = "{}/state/{}".format(self._base_url, product_address)
        response = requests.get(url)
        print('......... check product status')
        print(response.json())
        if not response.ok:
            if response.json()['error']['code'] == 75:
                return False
        return True

    # ------------------------------------------------------------ #
    #                   Action method                              #
    # ------------------------------------------------------------ #
    def add_product(self, product_list):
        """ Create new account """
        try:
            status = self._wrap_and_send(product_list, 10)
            # state_status = yaml.safe_load(result)['data'][0]['status']

            # if state url send 'COMMITTED' message, return True
            if status == 'COMMITTED':
                return True, "BLOCK_COMMITED"
            else:
                print("state status", status)
                # TODO: add logger
                return False, "BLOCK_COMMIT_FAILED"
        # If network problem
        except ConnectionRefusedError as err:
            # TODO: add logger
            return False, "CONNECTION_REFUSED"
        except TransactionNotFound as e:
            return False, str(e)

    def get_product(self, product_id):
        try:
            address = addresser.get_product_address(product_id)
            result = self._send_to_rest_api("state/{}".format(address))
            print("result: -----------")
            print(result)
            data = base64.b64decode(yaml.safe_load(result)["data"])
            pb_obj = payload_pb2.ProductInfoPayload()
            pb_obj.ParseFromString(data)
            return pb_obj
        except Exception as e:
            raise Exception(e)

    # ------------------------------------------------------------ #
    #                   Network method                             #
    # ------------------------------------------------------------ #
    def _send_to_rest_api(self, suffix, data=None, content_type=None):
        """Send a REST command to the Validator via the REST API.
           Called by count() &  _wrap_and_send().
           The latter caller is made on the behalf of create() & check().
        """
        url = "{}/{}".format(self._base_url, suffix)
        print("URL to send to REST API is {}".format(url))

        headers = {}

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
                print("result if data")
                print(result.json(), result.status_code)
            else:
                result = requests.get(url, headers=headers)
                print("result if no data: ")
                print(result.json(), result.status_code)
                # print(dir(result))

            if not result.ok:
                if result.status_code == 404:
                    raise Exception("Error {}: {}".format(
                        result.status_code, result.reason))

            return result.text

        except requests.ConnectionError as err:
            raise ConnectionRefusedError('Failed to connect to {}: {}'.format(url, str(err)))

    def _wait_for_status(self, batch_id, wait, result):
        """
            Wait until transaction status is not PENDING (COMMITTED or error).
           'wait' is time to wait for status, in seconds.
        """
        if wait and wait > 0:
            waited = 0
            start_time = time.time()
            while waited < wait:
                result = self._send_to_rest_api("batch_statuses?id={}&wait={}"
                                                .format(batch_id, wait))

                status = yaml.safe_load(result)['data'][0]['status']
                print("status:174:", status)
                waited = time.time() - start_time

                if status != 'PENDING':
                    return status
            return "Transaction timed out after waiting {} seconds." \
                .format(wait)
        else:
            return result.text

    def _wrap_and_send(self, payload_data, wait=None):
        """
        Create a transaction, then wrap it in a batch.
        Even single transactions must be wrapped into a batch.
        Called by create() and check().
        """
        transaction_list = []

        # Create a transaction list from payload data
        print(payload_data)
        for data in payload_data:
            print("................payload data............")
            print(data)
            # Construct the address where we'll store our state.
            # We just have one input and output address (the same one).
            product_id = data["Id"]
            # generate product address hash with Id
            product_address = addresser.get_product_address(product_id)

            # if product already exist with this ID, go next
            # TODO: remove in final version
            if self.is_product_already_exist(product_address):
                print("............product already exists")
                continue

            # create proto-buff object and encode data
            payload = payload_pb2.ProductInfoPayload(**data)
            payload_bytes = payload.SerializeToString()

            # Create a TransactionHeader.
            header = TransactionHeader(
                signer_public_key=self._public_key,
                family_name=FAMILY_NAME,
                family_version=FAMILY_VERSION,
                inputs=[product_address],
                outputs=[product_address],
                dependencies=[],
                payload_sha512=_hash(payload_bytes),
                batcher_public_key=self._public_key,
                nonce=random.random().hex().encode()
            ).SerializeToString()

            # Create a Transaction from the header and payload above.
            transaction = Transaction(
                header=header,
                payload=payload_bytes,
                header_signature=self._signer.sign(header)
            )
            # Append all transaction to transaction_list
            transaction_list.append(transaction)

        # Create a BatchHeader from transaction_list above.
        print("....Total {} transaction found".format(transaction_list))
        if len(transaction_list) == 0:
            print("..........no transaction found. existing...")
            raise TransactionNotFound("Data Already exists.")

        header = BatchHeader(
            signer_public_key=self._public_key,
            transaction_ids=[txn.header_signature for txn in transaction_list]
        ).SerializeToString()

        # Create Batch using the BatchHeader and transaction_list above.
        batch = Batch(
            header=header,
            transactions=transaction_list,
            header_signature=self._signer.sign(header))

        # Create a Batch List from Batch above
        batch_list = BatchList(batches=[batch])
        batch_id = batch_list.batches[0].header_signature

        # Send batch_list to the REST API
        result = self._send_to_rest_api("batches",
                                        batch_list.SerializeToString(),
                                        'application/octet-stream')

        # # Wait until transaction status is COMMITTED, error, or timed out
        return self._wait_for_status(batch_id, wait, result)