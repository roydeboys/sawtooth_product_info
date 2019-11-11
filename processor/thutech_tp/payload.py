from sawtooth_sdk.processor.exceptions import InvalidTransaction

from thutech_protobuf import payload_pb2


class ThutechPayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.ProductInfoPayload()
        self._transaction.ParseFromString(payload)

    @property
    def data(self):
            return self._transaction

    @property
    def timestamp(self):
        return self._transaction.timestamp