import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.errors import BlockchainReplacementError, BlockchainValidationError
from copy import deepcopy
from pydash import head, last

ADDITIONAL_DATA = "third block data"
DATA = "second block data"
MALICIOUS_DATA = "malicious data"


@pytest.fixture
def blockchain():
    """
    Generate blockchain of two blocks for tests
    """
    blockchain = Blockchain()
    blockchain.add_block(DATA)

    return blockchain


def test_add_block(blockchain):
    assert last(blockchain.chain).data == DATA


def test_replace_chain(blockchain):
    longer_blockhain = deepcopy(blockchain)
    longer_blockhain.add_block(ADDITIONAL_DATA)
    blockchain.replace_chain(longer_blockhain.chain)

    assert len(blockchain.chain) == 3


def test_replace_chain_not_longer(blockchain):
    not_longer_blockchain = Blockchain()

    with pytest.raises(BlockchainReplacementError):
        blockchain.replace_chain(not_longer_blockchain.chain)


def test_replace_chain_is_incorrect(blockchain):
    incorrect_blockchain = deepcopy(blockchain)
    incorrect_blockchain.add_block(ADDITIONAL_DATA)
    incorrect_blockchain.chain[0].data = MALICIOUS_DATA

    with pytest.raises(BlockchainReplacementError):
        blockchain.replace_chain(incorrect_blockchain.chain)


def test_blockchain_instance():
    blockchain = Blockchain()
    genesis_block = head(blockchain.chain)

    assert isinstance(blockchain, Blockchain)
    assert genesis_block.data == GENESIS_DATA["data"]


def test_validate_blockchain(blockchain):
    assert Blockchain.validate_blockchain(blockchain.chain) is None


def test_validate_blockchain_genesis_block_is_invalid(blockchain):
    blockchain.chain[0].data = MALICIOUS_DATA

    with pytest.raises(BlockchainValidationError):
        Blockchain.validate_blockchain(blockchain.chain)


def test_validate_blockchain_block_is_invalid(blockchain):
    blockchain.chain[1].data = MALICIOUS_DATA

    with pytest.raises(BlockchainValidationError):
        Blockchain.validate_blockchain(blockchain.chain)
