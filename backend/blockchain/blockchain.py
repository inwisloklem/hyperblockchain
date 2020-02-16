from backend.blockchain.block import Block
from backend.blockchain.errors import (
    BlockchainReplacementError,
    BlockchainValidationError,
    BlockValidationError,
)
from pydash import head, last


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.make_genesis_block()]

    def __repr__(self):
        return f"Blockchain: {self.chain}"

    def add_block(self, data):
        """
        Mine block then add new block to the chain
        """
        block = Block.mine_block(last(self.chain), data)
        self.chain.append(block)

    def get_last_block(self):
        """
        Return the last block in the chain
        """
        return last(self.chain)

    def replace_chain(self, incoming_chain):
        """
        Replace this chain with incoming chain by the following rules:
            - must be longer than the local chain
            - blocks of incoming chain must be formatted correctly
        """
        if len(incoming_chain) <= len(self.chain):
            raise BlockchainReplacementError("Incoming chain must be longer than the local one")

        try:
            Blockchain.validate_blockchain(incoming_chain)
        except BlockchainValidationError as e:
            raise BlockchainReplacementError(f"Incoming chain is invalid: {e}")

        self.chain = incoming_chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def validate_blockchain(chain):
        """
        Validate the incoming chain by the following rules:
            - must start with the genesis block
            - blocks must be formatted correctly
        """
        if head(chain) != Block.make_genesis_block():
            raise BlockchainValidationError("Genesis block in the head of chain is invalid")

        try:
            for i, block in enumerate(chain[1:], start=1):
                last_block = chain[i - 1]
                Block.validate_block(last_block, block)
        except BlockValidationError as e:
            raise BlockchainValidationError(f"Blocks are not formatted correctly: {e}")
