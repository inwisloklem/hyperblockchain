from backend.blockchain.block import Block
from more_itertools import last


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
