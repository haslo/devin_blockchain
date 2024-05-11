import pytest
from unittest.mock import patch, PropertyMock
from blockchain import Block, Blockchain

def test_block_initialization():
    block = Block(0, [], "0", 100)  # Added a dummy proof value
    assert block.index == 0
    assert block.transactions == []
    assert block.previous_hash == "0"
    assert block.hash is not None

def test_blockchain_initialization():
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1  # Genesis block

def test_add_transaction():
    blockchain = Blockchain()
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == {"sender": "Alice", "recipient": "Bob", "amount": 5}

def test_add_transaction_invalid_sender():
    blockchain = Blockchain()
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="", recipient="Bob", amount=5)

def test_add_transaction_invalid_recipient():
    blockchain = Blockchain()
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="", amount=5)

def test_add_transaction_invalid_amount():
    blockchain = Blockchain()
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="Bob", amount=-5)

def test_proof_of_work():
    blockchain = Blockchain()
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    assert blockchain.valid_proof(last_block.proof, proof) is True

import logging

def test_valid_chain():
    # Set up logging to capture info-level logs
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Changed from ERROR to INFO
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)  # Changed from ERROR to INFO
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    blockchain = Blockchain()
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    # Log the state of the blockchain before creating a new block
    logging.info(f"Before creating a new block: last_proof={last_block.proof}, proof={proof}, difficulty={blockchain.difficulty}, previous_hash={previous_hash}")
    # Pass adjust_diff as False to prevent difficulty adjustment during the test
    new_block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof, adjust_diff=False)
    # Log the state of the blockchain after creating a new block
    logging.info(f"After creating a new block: new_block_hash={new_block.hash}, difficulty={blockchain.difficulty}, previous_hash={new_block.previous_hash}")

    assert blockchain.valid_chain() is True, "The blockchain should be valid"

def test_chain_with_invalid_block():
    blockchain = Blockchain()
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof)  # Added the proof argument
    # Tamper with the block
    block.transactions.append({"sender": "Eve", "recipient": "Mallory", "amount": 10})
    assert blockchain.valid_chain() is False

# New test cases for dynamic difficulty adjustment
def test_difficulty_adjustment_with_fewer_than_10_blocks():
    blockchain = Blockchain()
    original_difficulty = blockchain.difficulty
    for i in range(9):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        blockchain.create_block(blockchain.current_transactions, previous_hash, proof)
    assert blockchain.difficulty == original_difficulty  # Difficulty should not change

def test_difficulty_increases():
    blockchain = Blockchain()
    # Simulate quick block mining to decrease average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        # Calculate new timestamp
        new_timestamp = last_block.timestamp + 5
        with patch.object(last_block, 'timestamp', new=PropertyMock(return_value=new_timestamp)):
            blockchain.create_block(blockchain.current_transactions, previous_hash, proof)
    assert blockchain.difficulty > 1  # Difficulty should increase

def test_difficulty_decreases():
    blockchain = Blockchain()
    # Set initial difficulty to a higher value for testing
    blockchain.difficulty = 5
    # Simulate slow block mining to increase average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        # Calculate new timestamp
        new_timestamp = last_block.timestamp + 20
        with patch.object(last_block, 'timestamp', new=PropertyMock(return_value=new_timestamp)):
            blockchain.create_block(blockchain.current_transactions, previous_hash, proof)
    assert blockchain.difficulty < 5  # Difficulty should decrease
