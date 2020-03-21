import pytest
from backend.wallet.wallet import Wallet

DATA = {"test": "message"}


@pytest.fixture
def wallet_signature_pair():
    """
    Generate `wallet`, `signature` pair for tests
    """
    wallet = Wallet()
    signature = wallet.sign(DATA)

    return wallet, signature


def test_verify_signature(wallet_signature_pair):
    wallet, signature = wallet_signature_pair
    assert Wallet.verify_signature(wallet.public_key, DATA, signature) is True


def test_verify_signature_is_invalid(wallet_signature_pair):
    wallet, signature = wallet_signature_pair
    assert Wallet.verify_signature(Wallet().public_key, DATA, signature) is False
