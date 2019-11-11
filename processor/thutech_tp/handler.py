import datetime
import time

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction

from thutech_addressing import addresser

from thutech_protobuf import payload_pb2

from thutech_tp.payload import ThutechPayload
from thutech_tp.state import ThutechState


# SYNC_TOLERANCE = 60 * 5
# MAX_LAT = 90 * 1e6
# MIN_LAT = -90 * 1e6
# MAX_LNG = 180 * 1e6
# MIN_LNG = -180 * 1e6


class ThutechHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def family_versions(self):
        return [addresser.FAMILY_VERSION]

    @property
    def namespaces(self):
        return [addresser.NAMESPACE]

    def apply(self, transaction, context):
        print("apply calling....")
        header = transaction.header
        payload = ThutechPayload(transaction.payload)
        state = ThutechState(context)
        crate_product_info(state, payload)


def crate_product_info(state, payload):
    """
        A method to store state data to validator
    """
    print("create product info....")
    product_id = payload.data.Id

    # call state method
    print("set state")
    state.set_product(product_id, payload)