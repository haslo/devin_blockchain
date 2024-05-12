import pytest
from wallet.wallet import Wallet

def test_wallet_creation():
    """
    Test the creation of a new wallet and the generation of a private and public key.
    """
    wallet = Wallet()
    assert wallet.private_key is not None
    assert wallet.public_key is not None

def test_sign_transaction():
    """
    Test the signing of a transaction by a wallet.
    """
    wallet = Wallet()
    transaction = {'sender': 'sender_public_key', 'recipient': 'recipient_public_key', 'amount': 10}
    signature = wallet.sign_transaction(transaction)
    assert signature is not None
    assert len(signature) > 0

def test_create_transaction():
    """
    Test the creation of a new transaction with valid parameters.
    """
    wallet = Wallet()
    recipient = 'recipient_public_key'
    amount = 10
    transaction = wallet.create_transaction(recipient, amount)
    assert transaction['sender'] == wallet.public_key.to_string().hex()
    assert transaction['recipient'] == recipient
    assert transaction['amount'] == amount
    assert 'signature' in transaction
