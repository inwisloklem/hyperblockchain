from backend.blockchain.block import GENESIS_DATA, Block


def test_make_genesis_block():
    genesis_block = Block.make_genesis_block()

    assert isinstance(genesis_block, Block)
    assert genesis_block.data == GENESIS_DATA
    assert genesis_block.last_block_hash is None


def test_mine_block():
    last_block = Block.make_genesis_block()
    data = "second block data"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_block_hash == last_block.block_hash
