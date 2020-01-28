class BlockValidationError(Exception):
    """
    Throw if the block validation has failed
    """
    def __init__(self, *args, **kwargs):
        Exception(*args, **kwargs)
