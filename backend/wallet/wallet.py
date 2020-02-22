import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
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

    def sign(self, data):
        """
        Generate a signature based on the data using private key
        """
        encoded_data = json.dumps(data).encode("utf-8")
        return self.private_key.sign(encoded_data, ec.ECDSA(hashes.SHA256()))

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

    data = {"test": "message"}
    signature = wallet.sign(data)

    print(f"Signature: {signature}")
