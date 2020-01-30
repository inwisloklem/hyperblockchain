import pytest
import time
from backend.config import MINE_RATE, SECONDS_MULTIPLIER
from backend.blockchain.block import GENESIS_DATA, Block
from backend.blockchain.errors import BlockValidationError
from backend.util.convert import convert_binary_to_hex, convert_hex_to_binary
from backend.util.make_hash_sha256 import make_hash_sha256

DATA = "second block data"
MALICIOUS_DATA = "malicious data"


def generate_block():
    """
    Generate `last_block`, `block` pair for tests
    """
    last_block = Block.make_genesis_block()
    return last_block, Block.mine_block(last_block, DATA)


def test_make_genesis_block():
    genesis_block = Block.make_genesis_block()

    assert isinstance(genesis_block, Block)
    assert genesis_block.data == GENESIS_DATA["data"]
    assert genesis_block.nonce == GENESIS_DATA["nonce"]
    assert genesis_block.last_block_hash is None


def test_mine_block():
    last_block = Block.make_genesis_block()
    block = Block.mine_block(last_block, DATA)

    assert isinstance(block, Block)
    assert block.data == DATA
    assert block.last_block_hash == last_block.block_hash

    binary_block_hash = convert_hex_to_binary(block.block_hash)
    assert binary_block_hash[0:block.difficulty] == "0" * block.difficulty


def test_mine_block_quickly_adjust_difficulty():
    last_block = Block.make_genesis_block()
    block = Block.mine_block(last_block, DATA)

    assert block.difficulty > last_block.difficulty


def test_mine_block_slowly_adjust_difficulty():
    last_block = Block.make_genesis_block()
    time.sleep(MINE_RATE / SECONDS_MULTIPLIER)
    block = Block.mine_block(last_block, DATA)

    assert block.difficulty < last_block.difficulty


def test_validate_block():
    last_block, block = generate_block()
    assert Block.validate_block(last_block, block) is None


def test_validate_block_last_block_hash_invalid():
    last_block, block_last_block_hash_invalid = generate_block()
    block_last_block_hash_invalid.last_block_hash = MALICIOUS_DATA

    with pytest.raises(BlockValidationError):
        Block.validate_block(last_block, block_last_block_hash_invalid)


def test_validate_block_proof_of_work_invalid():
    last_block, block_proof_of_work_invalid = generate_block()
    binary_block_hash = convert_hex_to_binary(block_proof_of_work_invalid.block_hash)
    block_proof_of_work_invalid.block_hash = convert_binary_to_hex("1" + binary_block_hash[1:])

    with pytest.raises(BlockValidationError):
        Block.validate_block(last_block, block_proof_of_work_invalid)


def test_validate_block_block_difficulty_invalid():
    last_block, block_block_difficulty_invalid = generate_block()
    block_block_difficulty_invalid.difficulty = 42

    with pytest.raises(BlockValidationError):
        Block.validate_block(last_block, block_block_difficulty_invalid)


def test_validate_block_block_hash_invalid():
    last_block, block_block_hash_invalid = generate_block()
    block_block_hash_invalid.block_hash = make_hash_sha256(MALICIOUS_DATA)

    with pytest.raises(BlockValidationError):
        Block.validate_block(last_block, block_block_hash_invalid)
