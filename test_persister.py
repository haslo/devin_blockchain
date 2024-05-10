import pytest
import os
import base64
import json
from blockchain import Blockchain
from persister import Persister, binascii

def test_save_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash='1', proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_save.devinchain'
    persister.save(blockchain, filename)

    # Check that the file exists
    assert os.path.isfile(filename)

    # Clean up the file after test
    os.remove(filename)

def test_load_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash='1', proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_load.devinchain'
    persister.save(blockchain, filename)

    # Load the blockchain from the file
    loaded_blockchain = persister.load(filename)

    # Check that the loaded blockchain matches the saved one
    assert loaded_blockchain == blockchain

    # Clean up the file after test
    os.remove(filename)

def test_load_nonexistent_blockchain():
    # Attempt to load a blockchain from a non-existent file
    persister = Persister()
    with pytest.raises(FileNotFoundError):
        persister.load('nonexistent.devinchain')

def test_load_blockchain_invalid_json():
    # Attempt to load a blockchain from a file with invalid JSON
    persister = Persister()
    filename = 'test_invalid_json.devinchain'
    with open(filename, 'w') as file:
        file.write("This is not valid JSON")

    with pytest.raises(Persister.InvalidJSONError):
        persister.load(filename)

    # Clean up the file after test
    os.remove(filename)

def test_load_blockchain_invalid_base64():
    # Create a blockchain and add a block with invalid base64 in transactions
    blockchain = Blockchain()
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash='1', proof=100)

    # Manually corrupt the transaction data to simulate invalid base64
    blockchain.chain[1].transactions = ["not_base64"]

    # Save the corrupted blockchain to a file
    persister = Persister()
    filename = 'test_invalid_base64.devinchain'
    with open(filename, 'w') as file:
        json.dump(blockchain.chain, file, cls=Persister.BlockEncoder, indent=4, sort_keys=True)

    with pytest.raises(Persister.InvalidBase64Error):
        persister.load(filename)

    # Clean up the file after test
    os.remove(filename)
