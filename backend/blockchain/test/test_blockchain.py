from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from pydash import head, last


def test_add_block():
    blockchain = Blockchain()
    data = "second block data"
    blockchain.add_block(data)

    assert last(blockchain.chain).data == data


def test_blockchain_instance():
    blockchain = Blockchain()
    genesis_block = head(blockchain.chain)

    assert isinstance(blockchain, Blockchain)
    assert genesis_block.data == GENESIS_DATA["data"]
