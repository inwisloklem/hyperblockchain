import time
from backend.config import MINE_RATE
from backend.blockchain.errors import BlockValidationError
from backend.util.convert import convert_hex_to_binary
from backend.util.make_hash_sha256 import make_hash_sha256

GENESIS_DATA = {
    "timestamp": time.time_ns(),
    "last_block_hash": None,
    "data": "first block data",
    "difficulty": 10,
    "nonce": 0
}


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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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

    def to_json(self):
        """
        Serialize the block into a dict of its attributes
        """
        return self.__dict__

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
    def from_json(block_json):
        """
        Deserialize a block JSON representation into a block object
        """
        return Block(**block_json)

    @staticmethod
    def make_genesis_block():
        """
        Make a first block also called genesis
        """
        genesis_data = GENESIS_DATA.copy()
        genesis_data["block_hash"] = make_hash_sha256(GENESIS_DATA)

        return Block(**genesis_data)

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block based on the given `last_block` and `data`, until
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

        return Block(timestamp, block_hash, last_block_hash, data, difficulty, nonce)

    @staticmethod
    def validate_block(last_block, block):
        """
        Validate the block by following rules:
            - must have proper `last_block_hash` reference
            - must meet the proof of work requirement of leading zeroes
            - difficulty must only be adjusted by one
            - block hash must be valid combination of the block fields
        """
        if block.last_block_hash != last_block.block_hash:
            raise BlockValidationError("Last hash reference of block is invalid")

        if convert_hex_to_binary(block.block_hash)[0:block.difficulty] != "0" * block.difficulty:
            raise BlockValidationError("Proof of work requirement is not met")

        if abs(block.difficulty - last_block.difficulty) > 1:
            raise BlockValidationError("Difference in blocks difficulty is greater than one")

        block_args = [
            block.timestamp,
            block.last_block_hash,
            block.data,
            block.difficulty,
            block.nonce,
        ]
        reconstructed_block_hash = make_hash_sha256(*block_args)
        if reconstructed_block_hash != block.block_hash:
            raise BlockValidationError("Block hash must be correct")
