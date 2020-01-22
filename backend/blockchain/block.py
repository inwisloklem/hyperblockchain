import time
from backend.util.make_hash_sha256 import make_hash_sha256

GENESIS_DATA = {"data": "first block data", "difficulty": 4, "nonce": "first block nonce"}


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
    def mine_block(last_block, data, difficulty=4, nonce="default nonce"):
        """
        Mine a block based on the given last_block and data
        """
        timestamp = time.time_ns()
        last_block_hash = last_block.block_hash
        block_hash = make_hash_sha256(timestamp, last_block_hash, data)

        return Block(timestamp, block_hash, last_block_hash, data, difficulty, nonce)


if __name__ == "__main__":
    genesis_block = Block.make_genesis_block()
    block = Block.mine_block(genesis_block, "second block data")

    print(block.__repr__())
