class AmountExceedsBalanceError(Exception):
    """
    Throw if the amount exceeds sender's balance
    """
    def __init__(self, *args, **kwargs):
        Exception(*args, **kwargs)
