import hashlib


FAMILY_NAME = 'thutech_subscriber'
FAMILY_VERSION = '1.0'
NAMESPACE = hashlib.sha512(FAMILY_NAME.encode('utf-8')).hexdigest()[:6]
# AGENT_PREFIX = '00'
# RECORD_PREFIX = '01'


def get_product_address(product_id):
    return NAMESPACE + hashlib.sha512(
        product_id.encode('utf-8')).hexdigest()[:64]
    # address = "1cf126" + hashlib.sha512('name'.encode('utf-8')).hexdigest()[-64:]
    # return address