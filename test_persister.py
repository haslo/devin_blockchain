import pytest
import os
from blockchain import Blockchain
from persister import Persister

def test_save_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.new_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(previous_hash='1', proof=100)

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
    blockchain.new_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(previous_hash='1', proof=100)

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
