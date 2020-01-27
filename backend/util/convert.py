HEX_TO_BINARY = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "a": "1010",
    "b": "1011",
    "c": "1100",
    "d": "1101",
    "e": "1110",
    "f": "1111"
}


def convert_binary_to_hex(binary):
    """
    Convert binary string to hexidecimal string.
    Preserve leading zeroes
    """
    return "{:0{}x}".format(int(binary, 2), len(binary) // 4)


def convert_hex_to_binary(hex):
    """
    Convert hexidecimal string to binary string.
    Preserve leading zeroes
    """
    return "".join([HEX_TO_BINARY[char] for char in hex])
