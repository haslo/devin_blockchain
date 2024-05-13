import pytest
from unittest.mock import patch, PropertyMock
from blockchain.block import Block
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction


@pytest.fixture(autouse=True)
def blockchain():
    blockchain = Blockchain()
    blockchain.toggle_test_mode(True)
    blockchain.create_genesis_block()
    yield blockchain
    blockchain.toggle_test_mode(False)


@pytest.fixture
def valid_transaction():
    return Transaction("transfer",
                       "sender_address",
                       {
                           "recipient": "recipient_address",
                           "amount": 1
                       },
                       0,
                       {
                           "chain_id": "HDC",
                           "version": 1
                       },
                       {
                           "tip": 1,
                           "max_fee": 1000,
                           "limit": 2000
                       },
                       {
                           "type": "ECDSA",
                           "r": "r_value",
                           "s": "s_value",
                           "v": "recovery_id",
                           "public_key": "public_key"
                       })


@pytest.fixture
def invalid_transaction():
    return Transaction(None, None, None, None, None, None)


def test_block_initialization():
    block = Block(5, [], "0123", 100, 10)
    assert block.index == 5
    assert block.transactions == []
    assert block.previous_hash == "0123"
    assert block.difficulty == 10
    assert block.hash is not None


def test_blockchain_initialization(blockchain):
    assert len(blockchain.chain) == 1  # Genesis block


def test_add_transaction(blockchain, valid_transaction):
    blockchain.add_transaction(valid_transaction)
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == valid_transaction


def test_add_transaction_invalid_transaction(blockchain, invalid_transaction):
    with pytest.raises(ValueError):
        blockchain.add_transaction(invalid_transaction)


def test_proof_of_work(blockchain):
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    # The proof should be valid for the current difficulty level of the blockchain
    assert blockchain.valid_proof(last_block.proof, proof, blockchain.difficulty) is True


def test_valid_chain(blockchain, valid_transaction):
    blockchain.add_transaction(valid_transaction)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(valid_transaction)
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    _new_block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof, previous_difficulty, adjust_diff=False)
    assert blockchain.valid_chain() is True, "The blockchain should be valid"


def test_chain_with_invalid_block(blockchain, valid_transaction):
    blockchain.add_transaction(valid_transaction)
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction(valid_transaction)
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    block.transactions.append(valid_transaction)
    assert blockchain.valid_chain() is False, "The blockchain was tampered with"


def test_difficulty_adjustment_with_fewer_than_10_blocks(blockchain, valid_transaction):
    original_difficulty = blockchain.difficulty
    for i in range(9):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(valid_transaction)
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty == original_difficulty  # Difficulty should not change


def test_difficulty_increases(blockchain, valid_transaction):
    # Simulate quick block mining to decrease average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(valid_transaction)
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        new_timestamp = last_block.timestamp + 5
        with patch.object(last_block, 'timestamp', new=PropertyMock(return_value=new_timestamp)):
            blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty > 1  # Difficulty should increase


def test_difficulty_decreases(blockchain, valid_transaction):
    # Set initial difficulty to a higher value for testing
    blockchain.difficulty = 5
    # Simulate slow block mining to increase average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction(valid_transaction)
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
