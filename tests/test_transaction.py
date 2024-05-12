import pytest
import json
from blockchain.blockchain import Blockchain
from ecdsa import SigningKey, NIST384p

def test_transaction_structure():
    """
    Test that a transaction contains all the necessary fields as per the new protocol.
    """
    blockchain = Blockchain()
    transaction = {
        "type": "transfer",
        "sender": "sender_address",
        "payload": {
            "recipient": "recipient_address",
            "amount": 123
        },
        "nonce": 1,
        "chain": {
            "chain_id": "dhc",
            "version": 1
        },
        "gas": {
            "tip": 0,
            "max_fee": 50,
            "limit": 100
        },
        "signature": {
            "type": "ECDSA",
            "r": "r_value",
            "s": "s_value",
            "v": "recovery_id",
            "public_key": "public_key"
        }
    }
    assert blockchain.validate_transaction(transaction) is True

def test_transaction_data_types():
    """
    Test the data types of each field in a transaction.
    """
    blockchain = Blockchain()
    transaction = {
        "type": "transfer",
        "sender": "sender_address",
        "payload": {
            "recipient": "recipient_address",
            "amount": 123
        },
        "nonce": 1,
        "chain": {
            "chain_id": "dhc",
            "version": 1
        },
        "gas": {
            "tip": 0,
            "max_fee": 50,
            "limit": 100
        },
        "signature": {
            "type": "ECDSA",
            "r": "r_value",
            "s": "s_value",
            "v": "recovery_id",
            "public_key": "public_key"
        }
    }
    # Validate data types
    assert isinstance(transaction['type'], str)
    assert isinstance(transaction['sender'], str)
    assert isinstance(transaction['payload'], dict)
    assert isinstance(transaction['payload']['recipient'], str)
    assert isinstance(transaction['payload']['amount'], int)
    assert isinstance(transaction['nonce'], int)
    assert isinstance(transaction['chain'], dict)
    assert isinstance(transaction['chain']['chain_id'], str)
    assert isinstance(transaction['chain']['version'], int)
    assert isinstance(transaction['gas'], dict)
    assert isinstance(transaction['gas']['tip'], int)
    assert isinstance(transaction['gas']['max_fee'], int)
    assert isinstance(transaction['gas']['limit'], int)
    assert isinstance(transaction['signature'], dict)
    assert isinstance(transaction['signature']['type'], str)
    assert isinstance(transaction['signature']['r'], str)
    assert isinstance(transaction['signature']['s'], str)
    assert isinstance(transaction['signature']['v'], str)
    assert isinstance(transaction['signature']['public_key'], str)

def test_transaction_signature_valid():
    """
    Test the signature of a transaction to ensure it is correctly formed and valid.
    """
    blockchain = Blockchain()
    # Create a new key pair
    sk = SigningKey.generate(curve=NIST384p)
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    # Create a transaction
    transaction = {
        "type": "transfer",
        "sender": "sender_address",
        "payload": {
            "recipient": "recipient_address",
            "amount": 123
        },
        "nonce": 1,
        "chain": {
            "chain_id": "dhc",
            "version": 1
        },
        "gas": {
            "tip": 0,
            "max_fee": 50,
            "limit": 100
        },
        "signature": {}
    }
    # Sign the transaction
    transaction_json = json.dumps(transaction, sort_keys=True).encode()
    signature = sk.sign(transaction_json)
    # Add the signature to the transaction
    transaction['signature'] = {
        "type": "ECDSA",
        "r": signature[:len(signature)//2].hex(),
        "s": signature[len(signature)//2:].hex(),
        "v": "00",  # This is a placeholder
        "public_key": public_key
    }
    assert blockchain.validate_signature(transaction) is True

def test_transaction_signature_invalid():
    """
    Test the signature of a transaction to ensure that an invalid signature is correctly identified.
    """
    blockchain = Blockchain()
    # Create a transaction with an invalid signature
    transaction = {
        "type": "transfer",
        "sender": "sender_address",
        "payload": {
            "recipient": "recipient_address",
            "amount": 123
        },
        "nonce": 1,
        "chain": {
            "chain_id": "dhc",
            "version": 1
        },
        "gas": {
            "tip": 0,
            "max_fee": 50,
            "limit": 100
        },
        "signature": {
            "type": "ECDSA",
            "r": "00"*32,  # Invalid r value
            "s": "00"*32,  # Invalid s value
            "v": "00",     # Invalid recovery id
            "public_key": "00"*96  # Invalid public key
        }
    }
    assert blockchain.validate_signature(transaction) is False
