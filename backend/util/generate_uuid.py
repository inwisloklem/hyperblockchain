from uuid import uuid4

UUID_LENGTH = 8


def generate_uuid(uuid_length=UUID_LENGTH):
    """
    Generate first `uuid_length` digits of uuid4
    """
    uuid = str(uuid4())
    return uuid[:uuid_length]
