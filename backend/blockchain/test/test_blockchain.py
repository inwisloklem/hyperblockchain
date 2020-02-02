import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.errors import BlockchainValidationError
from pydash import head, last

DATA = "second block data"
MALICIOUS_DATA = "malicious data"


@pytest.fixture
def two_blocks_blockchain():
    """
    Generate blockchain of two blocks for tests
    """
    blockchain = Blockchain()
    blockchain.add_block(DATA)

    return blockchain


def test_add_block(two_blocks_blockchain):
    assert last(two_blocks_blockchain.chain).data == DATA


def test_blockchain_instance():
    blockchain = Blockchain()
    genesis_block = head(blockchain.chain)

    assert isinstance(blockchain, Blockchain)
    assert genesis_block.data == GENESIS_DATA["data"]


def test_validate_blockchain(two_blocks_blockchain):
    assert Blockchain.validate_blockchain(two_blocks_blockchain.chain) is None


def test_validate_blockchain_genesis_block_is_invalid(two_blocks_blockchain):
    two_blocks_blockchain.chain[0].data = MALICIOUS_DATA

    with pytest.raises(BlockchainValidationError):
        Blockchain.validate_blockchain(two_blocks_blockchain.chain)


def test_validate_blockchain_block_is_invalid(two_blocks_blockchain):
    two_blocks_blockchain.chain[1].data = MALICIOUS_DATA

    with pytest.raises(BlockchainValidationError):
        Blockchain.validate_blockchain(two_blocks_blockchain.chain)
