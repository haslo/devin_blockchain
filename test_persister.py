import pytest
import os
import json
from blockchain import Blockchain
from persister import Persister

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

# New test case for saving and loading a blockchain, then comparing the two
def test_save_and_load_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash='1', proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_save_load.devinchain'
    persister.save(blockchain, filename)

    # Load the blockchain from the file
    loaded_blockchain = persister.load(filename)

    # Compare the blockchains to ensure they are the same
    assert loaded_blockchain.chain == blockchain.chain

    # Clean up the file after test
    os.remove(filename)
