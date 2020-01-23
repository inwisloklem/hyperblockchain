import time
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

        return f"Block: {', '.join([f'{k}: {v}' for k, v in block.items()])}"

    @staticmethod
    def make_genesis_block():
        """
        Make a first block also called genesis
        """
        timestamp = time.time_ns()
        return Block(timestamp, make_hash_sha256(timestamp), None, **GENESIS_DATA)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given last_block and data, until
        a block hash is found that meets the leading zeroes proof of
        work requirement
        """
        timestamp = time.time_ns()
        last_block_hash = last_block.block_hash
        difficulty = last_block.difficulty
        nonce = 0

        block_hash = make_hash_sha256(timestamp, last_block_hash, data, difficulty, nonce)
        while block_hash[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            block_hash = make_hash_sha256(timestamp, last_block_hash, data, difficulty, nonce)

        return Block(timestamp, block_hash, last_block_hash, data, difficulty, nonce)
