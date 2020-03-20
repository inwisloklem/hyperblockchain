import pytest
from backend.util.generate_uuid import generate_uuid
from backend.wallet.errors import AmountExceedsBalanceError
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


@pytest.fixture
def recipient_address_sender_wallet_pair():
    """
    Generate `recipient_address`, `sender_wallet` pair for tests
    """
    recipient_address = generate_uuid()
    sender_wallet = Wallet()

    return recipient_address, sender_wallet


def test_transaction(recipient_address_sender_wallet_pair):
    amount = 75
    recipient_address, sender_wallet = recipient_address_sender_wallet_pair
    transaction = Transaction(sender_wallet, recipient_address, amount)
    input, output = transaction.input, transaction.output
    left = sender_wallet.balance - amount

    assert transaction.output[recipient_address] == amount
    assert transaction.output[sender_wallet.address] == left

    assert transaction.input["address"] == sender_wallet.address
    assert transaction.input["amount"] == sender_wallet.balance
    assert transaction.input["public_key"] == sender_wallet.public_key
    assert type(transaction.input["timestamp"]) is int

    assert Wallet.verify(input["public_key"], output, input["signature"])


def test_transaction_amount_exceeds_balance(recipient_address_sender_wallet_pair):
    amount = 150
    recipient_address, sender_wallet = recipient_address_sender_wallet_pair

    with pytest.raises(AmountExceedsBalanceError):
        Transaction(sender_wallet, recipient_address, amount)
