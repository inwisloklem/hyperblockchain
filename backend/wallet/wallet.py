from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from uuid import uuid4


class Wallet:
    """
    Individual cryptocurrency wallet.
    Keeps track of user's balance and allows to authorize transactions
    """
    def __init__(self):
        self.address = Wallet.generate_uuid()
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    @staticmethod
    def generate_uuid():
        """
        Generate first eight digits of uuid4
        """
        uuid = str(uuid4())
        return uuid[0:8]


if __name__ == "__main__":
    wallet = Wallet()
    print(wallet.__dict__)
