import pytest
from blockchain import Blockchain
from miner import Miner

def test_proof_of_work():
    blockchain = Blockchain()
    miner = Miner(blockchain)
    last_proof = blockchain.last_block['proof']
    proof = miner.proof_of_work(last_proof)
    assert miner.valid_proof(last_proof, proof)

def test_mine_block():
    blockchain = Blockchain()
    miner = Miner(blockchain)
    recipient_address = "test_address"
    block = miner.mine(recipient_address)

    assert block['previous_hash'] == Blockchain.hash(blockchain.last_block)
    assert block['transactions'][-1]['recipient'] == recipient_address
    assert block['transactions'][-1]['amount'] == 1  # Mining reward
    assert block['proof'] is not None
    assert blockchain.valid_chain()
