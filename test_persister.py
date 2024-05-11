import pytest
import os
import json
from blockchain import Blockchain
from persister import Persister


def test_save_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.create_genesis_block()  # Ensure the genesis block is created
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash=blockchain.last_block.hash, difficulty=blockchain.last_block.difficulty, proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_save.json'
    persister.save(blockchain, filename)

    # Check that the file exists
    assert os.path.isfile(filename)

    # Clean up the file after test
    os.remove(filename)


def test_load_blockchain():
    # Create a blockchain and add a block
    blockchain = Blockchain()
    blockchain.create_genesis_block()  # Ensure the genesis block is created
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash=blockchain.last_block.hash, difficulty=blockchain.last_block.difficulty, proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_load.json'
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
        persister.load('nonexistent.json')


def test_load_blockchain_invalid_json():
    # Attempt to load a blockchain from a file with invalid JSON
    persister = Persister()
    filename = 'test_invalid_json.json'
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
    blockchain.create_genesis_block()  # Ensure the genesis block is created
    blockchain.add_transaction(sender="a", recipient="b", amount=1)
    blockchain.create_block(transactions=blockchain.current_transactions, previous_hash=blockchain.last_block.hash, difficulty=blockchain.last_block.difficulty, proof=100)

    # Save the blockchain to a file
    persister = Persister()
    filename = 'test_save_load.json'
    persister.save(blockchain, filename)

    # Load the blockchain from the file
    loaded_blockchain = persister.load(filename)

    # Compare the blockchains to ensure they are the same
    assert loaded_blockchain.chain == blockchain.chain

    # Explicitly test hashes and transactions
    for original_block, loaded_block in zip(blockchain.chain, loaded_blockchain.chain):
        assert original_block.hash == loaded_block.hash
        assert original_block.transactions == loaded_block.transactions

    # Clean up the file after test
    os.remove(filename)


# New test case for loading a blockchain from a pre-saved file in the fixtures folder
def test_load_blockchain_from_fixture():
    # Load the blockchain from the pre-saved fixture file
    persister = Persister()
    fixture_filename = 'fixtures/test_blockchain.json'
    loaded_blockchain = persister.load(fixture_filename)

    # Manually create a blockchain instance that matches the expected data from the fixture
    expected_blockchain = Blockchain()
    expected_blockchain.create_genesis_block()  # Ensure the genesis block is created
    expected_blockchain.add_transaction(sender="a", recipient="b", amount=1)
    # Use the correct hash of the genesis block for the previous_hash of the second block
    expected_blockchain.create_block(transactions=expected_blockchain.current_transactions,
                                     previous_hash="feb534fe03366345fe7b6ed8e5367ac9a4e219ead99b690d9f73cbff1687d904",
                                     proof=100,
                                     difficulty=1)

    # Compare the loaded blockchain to the expected blockchain
    # Ensure that the structure and content of the blocks are consistent
    for expected_block, loaded_block in zip(expected_blockchain.chain, loaded_blockchain.chain):
        assert expected_block.index == loaded_block.index
        assert expected_block.transactions == loaded_block.transactions
        assert expected_block.previous_hash == loaded_block.previous_hash
        assert expected_block.difficulty == loaded_block.difficulty
