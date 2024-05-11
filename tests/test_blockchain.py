import pytest
from unittest.mock import patch, PropertyMock
from blockchain.block import Block
from blockchain.blockchain import Blockchain


@pytest.fixture(autouse=True)
def blockchain():
    blockchain = Blockchain()
    blockchain.toggle_test_mode(True)
    blockchain.create_genesis_block()
    yield blockchain
    blockchain.toggle_test_mode(False)


def test_block_initialization():
    block = Block(5, [], "0123", 100, 10)
    assert block.index == 5
    assert block.transactions == []
    assert block.previous_hash == "0123"
    assert block.difficulty == 10
    assert block.hash is not None


def test_blockchain_initialization(blockchain):
    assert len(blockchain.chain) == 1  # Genesis block


def test_add_transaction(blockchain):
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == {"sender": "Alice", "recipient": "Bob", "amount": 5}


def test_add_transaction_invalid_sender(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="", recipient="Bob", amount=5)


def test_add_transaction_invalid_recipient(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="", amount=5)


def test_add_transaction_invalid_amount(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="Bob", amount=-5)


def test_proof_of_work(blockchain):
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    # The proof should be valid for the current difficulty level of the blockchain
    assert blockchain.valid_proof(last_block.proof, proof, blockchain.difficulty) is True


def test_valid_chain(blockchain):
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    _new_block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof, previous_difficulty, adjust_diff=False)
    assert blockchain.valid_chain() is True, "The blockchain should be valid"


def test_chain_with_invalid_block(blockchain):
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    block.transactions.append({"sender": "Eve", "recipient": "Mallory", "amount": 10})
    assert blockchain.valid_chain() is False, "The blockchain was tampered with"


def test_difficulty_adjustment_with_fewer_than_10_blocks(blockchain):
    original_difficulty = blockchain.difficulty
    for i in range(9):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty == original_difficulty  # Difficulty should not change


def test_difficulty_increases(blockchain):
    # Simulate quick block mining to decrease average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        new_timestamp = last_block.timestamp + 5
        with patch.object(last_block, 'timestamp', new=PropertyMock(return_value=new_timestamp)):
            blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty > 1  # Difficulty should increase


def test_difficulty_decreases(blockchain):
    # Set initial difficulty to a higher value for testing
    blockchain.difficulty = 5
    # Simulate slow block mining to increase average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        new_timestamp = blockchain.chain[-1].timestamp + 20
        new_block = Block(index=last_block.index + 1,
                          transactions=blockchain.current_transactions,
                          previous_hash=previous_hash,
                          proof=proof,
                          difficulty=previous_difficulty,
                          timestamp=new_timestamp)
        blockchain.chain.append(new_block)
        blockchain.current_transactions = []
    blockchain.adjust_difficulty()
    assert blockchain.difficulty < 5, "Difficulty should decrease after simulating slow block mining"
