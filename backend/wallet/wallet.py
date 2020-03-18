import json
from backend.config import STARTING_BALANCE
from backend.util.generate_uuid import generate_uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Individual cryptocurrency wallet.
    Keeps track of user's balance and allows to authorize transactions
    """
    def __init__(self):
        self.address = generate_uuid()
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """
        Generate a signature based on the `data` using `private_key`
        """
        encoded_data = json.dumps(data).encode("utf-8")
        return self.private_key.sign(encoded_data, ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original `public_key` and `data`
        """
        encoded_data = json.dumps(data).encode("utf-8")

        try:
            public_key.verify(signature, encoded_data, ec.ECDSA(hashes.SHA256()))
        except InvalidSignature:
            return False
        return True
