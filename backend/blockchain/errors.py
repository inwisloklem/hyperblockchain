class BlockchainReplacementError(Exception):
    """
    Throw if the chain replacement has failed
    """
    def __init__(self, *args, **kwargs):
        Exception(*args, **kwargs)


class BlockchainValidationError(Exception):
    """
    Throw if the blockchain validation has failed
    """
    def __init__(self, *args, **kwargs):
        Exception(*args, **kwargs)


class BlockValidationError(Exception):
    """
    Throw if the block validation has failed
    """
    def __init__(self, *args, **kwargs):
        Exception(*args, **kwargs)
