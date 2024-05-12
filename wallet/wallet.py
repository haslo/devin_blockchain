import hashlib
import json
from ecdsa import SigningKey, NIST384p

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=NIST384p)
        self.public_key = self.private_key.get_verifying_key()

    def sign_transaction(self, transaction):
        """
        Sign a transaction with the private key of this wallet.
        :param transaction: The transaction to sign.
        :return: The signature of the transaction.
        """
        transaction_json = json.dumps(transaction, sort_keys=True).encode()
        signature = self.private_key.sign(transaction_json)
        return signature.hex()

    def create_transaction(self, recipient, amount):
        """
        Create a new transaction to be sent to another wallet.
        :param recipient: The public key of the recipient wallet.
        :param amount: The amount of HDC to send.
        :return: The created transaction with the signature.
        """
        transaction = {
            'sender': self.public_key.to_string().hex(),
            'recipient': recipient,
            'amount': amount
        }
        signature = self.sign_transaction(transaction)
        transaction['signature'] = signature
        return transaction
