import logging
import hashlib
import zmq

from django.core.management.base import BaseCommand
from sawtooth_sdk.protobuf.client_event_pb2 import ClientEventsSubscribeRequest
from sawtooth_sdk.protobuf.client_event_pb2\
    import ClientEventsSubscribeResponse
from sawtooth_sdk.protobuf.events_pb2 import EventList
from sawtooth_sdk.protobuf.events_pb2 import EventSubscription
from sawtooth_sdk.protobuf.events_pb2 import EventFilter
from sawtooth_sdk.protobuf.validator_pb2 import Message
from sawtooth_sdk.messaging.stream import Stream
from google.protobuf.json_format import MessageToJson, MessageToDict
from subscriber.models import BlockInfo


FAMILY_NAME = 'thutech_subscriber'
FAMILY_VERSION = '1.0'
NAMESPACE = hashlib.sha512(FAMILY_NAME.encode('utf-8')).hexdigest()[:6]


logger = logging.getLogger(__name__)
NULL_BLOCK_ID = '0000000000000000'
validator_url = 'tcp://validator:4004'


def subscribe_event():
    """
     A custom management command to store block information of each block data by event subscription.
     this command is calling from docker-compose file
    """
    logger.info("event function start..")
    # Setup a connection to the validator
    ctx = zmq.Context()
    socket = ctx.socket(zmq.DEALER)
    socket.connect(validator_url)

    # -------------------------------#
    # Submit the Event Subscription  #
    # -------------------------------#

    # subscribe both both "block commit" and "state-delta" event
    block_sub = EventSubscription(event_type='sawtooth/block-commit')
    delta_sub = EventSubscription(
        event_type='sawtooth/state-delta',
        filters=[EventFilter(
            key='address',
            match_string='^{}.*'.format(NAMESPACE),
            filter_type=EventFilter.REGEX_ANY)])

    # Construct the request
    request = ClientEventsSubscribeRequest(
        subscriptions=[block_sub, delta_sub]).SerializeToString()

    # Construct the message wrapper
    correlation_id = "123" # This must be unique for all in-process requests
    msg = Message(
        correlation_id=correlation_id,
        message_type=Message.CLIENT_EVENTS_SUBSCRIBE_REQUEST,
        content=request)

    # Send the request
    socket.send_multipart([msg.SerializeToString()])

    #
    # -------------------------------#
    #     Receive the response       #
    # -------------------------------#

    resp = socket.recv_multipart()[-1]

    # Parse the message wrapper
    msg = Message()
    msg.ParseFromString(resp)

    # Validate the response type
    if msg.message_type != Message.CLIENT_EVENTS_SUBSCRIBE_RESPONSE:
        logger.error("Unexpected message type")
        return

    # Parse the response
    response = ClientEventsSubscribeResponse()
    response.ParseFromString(msg.content)

    # Validate the response status
    if response.status != ClientEventsSubscribeResponse.OK:
      return

    while True:
        resp = socket.recv_multipart()[-1]

        # Parse the message wrapper
        msg = Message()
        msg.ParseFromString(resp)

        # Validate the response type
        if msg.message_type != Message.CLIENT_EVENTS:
            return

        # Parse the response
        events = EventList()
        events.ParseFromString(msg.content)
        block_info = {
            "address": []
        }
        event_data = MessageToDict(events)
        events_list = event_data["events"]
        for event in events_list:
            attributes = event["attributes"]

            for attr in attributes:
                key = attr["key"]
                value = attr["value"]
                if key == 'address':
                    block_info["address"].append(value)
                else:
                    block_info[key] = value

        address_list = block_info["address"]
        for address in address_list:
            BlockInfo.objects.create(
                block_num=block_info["block_num"],
                block_id=block_info["block_id"],
                state_root_hash=block_info["state_root_hash"],
                previous_block_id=block_info["previous_block_id"],
                address=address,
            )
            logger.info("blockinfo subscription created..")


class Command(BaseCommand):
    help = 'Subscribe block event'

    def handle(self, *args, **kwargs):
        subscribe_event()