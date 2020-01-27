import time
from backend.config import MINE_RATE, SECONDS_MULTIPLIER
from backend.blockchain.block import GENESIS_DATA, Block
from backend.util.convert import convert_hex_to_binary

DATA = "second block data"


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
