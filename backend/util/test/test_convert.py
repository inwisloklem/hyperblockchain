from backend.util.convert import convert_binary_to_hex, convert_hex_to_binary


def test_convert_binary_to_hex():
    assert convert_binary_to_hex("0000000110111110") == "01be"


def test_convert_hex_to_binary():
    assert convert_hex_to_binary("01be") == "0000000110111110"
