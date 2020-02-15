from backend.util.generate_port import generate_port

DEFAULT_PORT = 4444
MAX_PORT = 8888
MIN_PORT = 4444


def test_generate_port():
    assert generate_port(True, DEFAULT_PORT, max_port=MAX_PORT) <= MAX_PORT
    assert generate_port(True, DEFAULT_PORT, min_port=MIN_PORT) >= MIN_PORT
    assert generate_port(False, DEFAULT_PORT) == DEFAULT_PORT
