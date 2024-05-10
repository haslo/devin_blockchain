import pytest
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

def test_proof_of_work():
    blockchain = Blockchain()
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    assert blockchain.valid_proof(last_proof, proof) is True

def test_valid_chain():
    blockchain = Blockchain()
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    blockchain.create_block(blockchain.current_transactions, previous_hash, proof)  # Added the proof argument
    assert blockchain.valid_chain() is True

def test_chain_with_invalid_block():
    blockchain = Blockchain()
    blockchain.add_transaction(sender="Alice", recipient="Bob", amount=5)
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    blockchain.add_transaction(sender="0", recipient="Devin", amount=1)
    previous_hash = last_block.hash
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof)  # Added the proof argument
    # Tamper with the block
    block.transactions.append({"sender": "Eve", "recipient": "Mallory", "amount": 10})
    assert blockchain.valid_chain() is False
