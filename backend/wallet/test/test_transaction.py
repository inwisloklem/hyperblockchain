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
    balance_left = sender_wallet.balance - amount
    transaction = Transaction(sender_wallet, recipient_address, amount)
    input, output = transaction.input, transaction.output

    assert transaction.output[recipient_address] == amount
    assert transaction.output[sender_wallet.address] == balance_left

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


def test_transaction_update(recipient_address_sender_wallet_pair):
    amount_before_update, amount_after_update = 10, 15
    recipient_address, sender_wallet = recipient_address_sender_wallet_pair
    transaction = Transaction(sender_wallet, recipient_address, amount_before_update)

    balance_left = sender_wallet.balance - amount_before_update - amount_after_update
    transaction.update(sender_wallet, recipient_address, amount_after_update)

    assert transaction.output[sender_wallet.address] == balance_left
    assert transaction.output[recipient_address] == amount_before_update + amount_after_update


def test_transaction_update_another_recipient(recipient_address_sender_wallet_pair):
    amount_before_update, amount_after_update = 10, 15
    another_recipient_address = generate_uuid()
    recipient_address, sender_wallet = recipient_address_sender_wallet_pair
    transaction = Transaction(sender_wallet, recipient_address, amount_before_update)

    balance_left = sender_wallet.balance - amount_before_update - amount_after_update
    transaction.update(sender_wallet, another_recipient_address, amount_after_update)

    assert transaction.output[sender_wallet.address] == balance_left
    assert transaction.output[recipient_address] == amount_before_update
    assert transaction.output[another_recipient_address] == amount_after_update


def test_transaction_update_amount_exceeds_balance(recipient_address_sender_wallet_pair):
    amount_before_update, amount_after_update = 10, 150
    recipient_address, sender_wallet = recipient_address_sender_wallet_pair
    transaction = Transaction(sender_wallet, recipient_address, amount_before_update)

    with pytest.raises(AmountExceedsBalanceError):
        transaction.update(sender_wallet, recipient_address, amount_after_update)
