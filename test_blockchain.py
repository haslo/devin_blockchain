import pytest
from blockchain import Block, Blockchain

def test_block_initialization():
    block = Block(0, [], "0")
    assert block.index == 0
    assert block.transactions == []
    assert block.previous_hash == "0"
    assert block.hash is not None

def test_blockchain_initialization():
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1  # Genesis block

def test_add_transaction():
    blockchain = Blockchain()
    blockchain.add_transaction("Alice pays Bob 5 BTC")
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == "Alice pays Bob 5 BTC"

def test_proof_of_work():
    blockchain = Blockchain()
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    assert blockchain.valid_proof(last_proof, proof) is True

def test_valid_chain():
    blockchain = Blockchain()
    blockchain.add_transaction("Alice pays Bob 5 BTC")
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    blockchain.add_transaction("0 pays Devin 1 BTC")
    previous_hash = last_block.hash
    blockchain.create_block(blockchain.current_transactions, previous_hash)
    assert blockchain.valid_chain() is True

def test_chain_with_invalid_block():
    blockchain = Blockchain()
    blockchain.add_transaction("Alice pays Bob 5 BTC")
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)
    blockchain.add_transaction("0 pays Devin 1 BTC")
    previous_hash = last_block.hash
    block = blockchain.create_block(blockchain.current_transactions, previous_hash)
    # Tamper with the block
    block.transactions.append("Eve pays Mallory 10 BTC")
    assert blockchain.valid_chain() is False
