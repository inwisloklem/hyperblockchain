import time
from backend.wallet.errors import AmountExceedsBalanceError
from backend.util.generate_uuid import generate_uuid
from backend.wallet.wallet import Wallet


class Transaction():
    """
    Document of an exchange in currency from a sender to one or more
    recipients
    """
    def __init__(self, sender_wallet, recipient_address, amount):
        self.id = generate_uuid()
        self.output = self.make_output(sender_wallet, recipient_address, amount)
        self.input = self.make_input(sender_wallet, self.output)

    def make_input(self, sender_wallet, output):
        """
        Make the input data for the transaction.
        Send the transaction and include the sender's `public_key`
        and `address`
        """
        input = {
            "address": sender_wallet.address,
            "amount": sender_wallet.balance,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(output),
            "timestamp": time.time_ns(),
        }

        return input

    def make_output(self, sender_wallet, recipient_address, amount):
        """
        Make the output data for the transaction
        """
        if amount > sender_wallet.balance:
            raise AmountExceedsBalanceError("Amount exceeds sender's balance")
        output = {recipient_address: amount, sender_wallet.address: sender_wallet.balance - amount}

        return output

    def update(self, sender_wallet, recipient_address, amount):
        """
        Update the transaction with an existing or new recipient
        """
        if amount > self.output[sender_wallet.address]:
            raise AmountExceedsBalanceError

        if recipient_address in self.output:
            self.output[recipient_address] = self.output[recipient_address] + amount
        else:
            self.output[recipient_address] = amount

        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount
        self.input = self.make_input(sender_wallet, self.output)


if __name__ == "__main__":
    sender_wallet = Wallet()
    first_recipient_address = generate_uuid()
    transaction = Transaction(sender_wallet, first_recipient_address, 15)
    print(f"transaction: {transaction.__dict__}\n")

    transaction.update(sender_wallet, first_recipient_address, 10)
    print(f"transaction: {transaction.__dict__}\n")

    second_recipient_address = generate_uuid()
    transaction.update(sender_wallet, second_recipient_address, 10)
    print(f"transaction: {transaction.__dict__}")
