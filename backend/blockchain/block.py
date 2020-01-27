import time
from backend.config import MINE_RATE
from backend.util.convert import convert_hex_to_binary
from backend.util.make_hash_sha256 import make_hash_sha256

GENESIS_DATA = {"data": "first block data", "difficulty": 2, "nonce": 0}


class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, timestamp, block_hash, last_block_hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.block_hash = block_hash
        self.last_block_hash = last_block_hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        block = {
            "timestamp": self.timestamp,
            "block_hash": self.block_hash,
            "last_block_hash": self.last_block_hash,
            "data": f"'{self.data}'",
            "difficulty": self.difficulty,
            "nonce": self.nonce,
        }

        return f"Block: {{{', '.join([f'{k}: {v}' for k, v in block.items()])}}}"

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the `MINE_RATE`.
        Increase the difficulty for quickly mined blocks. Also decrease
        the difficulty for slowly mined blocks
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def make_genesis_block():
        """
        Make a first block also called genesis
        """
        timestamp = time.time_ns()
        binary_block_hash = convert_hex_to_binary(make_hash_sha256(timestamp))
        return Block(timestamp, binary_block_hash, None, **GENESIS_DATA)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until
        a block hash is found that meets the leading zeroes proof of
        work requirement
        """
        timestamp = time.time_ns()
        last_block_hash = last_block.block_hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0

        block_hash = make_hash_sha256(timestamp, last_block_hash, data, difficulty, nonce)
        binary_block_hash = convert_hex_to_binary(block_hash)
        while binary_block_hash[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            block_hash = make_hash_sha256(timestamp, last_block_hash, data, difficulty, nonce)
            binary_block_hash = convert_hex_to_binary(block_hash)

        return Block(timestamp, binary_block_hash, last_block_hash, data, difficulty, nonce)
