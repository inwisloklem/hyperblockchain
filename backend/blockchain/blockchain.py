from backend.blockchain.block import Block
from backend.blockchain.errors import BlockchainValidationError, BlockValidationError
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
        block = Block.mine_block(last(self.chain), data)
        self.chain.append(block)

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
        except BlockValidationError:
            raise BlockchainValidationError("Blocks are not formatted correctly")
