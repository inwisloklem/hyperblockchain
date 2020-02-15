import random


def generate_port(is_peer, default_port, min_port=4444, max_port=8888):
    """
    Generate port number from `min_port` to `max_port` if in peer mode.
    Else use default port number
    """
    return random.randint(min_port, max_port) if is_peer else default_port
