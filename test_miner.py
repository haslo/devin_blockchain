import pytest
from blockchain import Blockchain
from miner import Miner

def test_proof_of_work():
    blockchain = Blockchain()
    miner = Miner(blockchain)
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    assert miner.valid_proof(last_block.proof, proof)

def test_mine_block():
    blockchain = Blockchain()
    miner = Miner(blockchain)
    recipient_address = "test_address"

    # Cache the last block before mining
    previous_last_block = blockchain.last_block

    block = miner.mine(recipient_address)

    # Print statements for debugging
    print(f"block.previous_hash: {block.previous_hash}")
    print(f"previous_last_block.hash: {previous_last_block.hash}")
    print(f"blockchain.last_block.hash: {blockchain.last_block.hash}")
    print(f"blockchain chain: {[block.hash for block in blockchain.chain]}")

    # Assert the newly mined block is the last block in the blockchain
    assert block == blockchain.last_block
    # Assert the previous_hash of the newly mined block matches the hash of the previously last block
    assert block.previous_hash == previous_last_block.hash, f"Expected previous_hash to be {previous_last_block.hash}, but got {block.previous_hash}"
    assert block.transactions[-1]['recipient'] == recipient_address
    assert block.transactions[-1]['amount'] == 1  # Mining reward
    assert block.proof is not None
    assert blockchain.valid_chain()
