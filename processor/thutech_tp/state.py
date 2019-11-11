from thutech_addressing import addresser


class ThutechState(object):
    def __init__(self, context, timeout=2):
        self._context = context
        self._timeout = timeout

    def set_product(self, product_id, payload):
        """
        Create new product state
        """
        # generate product address hash with serial number
        product_address = addresser.get_product_address(product_id)

        # decrypt payload data with protobuf
        state_data = payload.data.SerializeToString()

        # assign key value state data
        state_update = {}
        state_update[product_address] = state_data

        # set state data to validator
        self._context.set_state(state_update, timeout=self._timeout)
        print("state set successfully")

