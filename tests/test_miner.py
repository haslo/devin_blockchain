from blockchain.blockchain import Blockchain
from mining.miner import Miner


def test_proof_of_work():
    blockchain = Blockchain()
    blockchain.create_genesis_block()
    miner = Miner(blockchain)
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    assert miner.valid_proof(last_block.proof, proof, last_block.difficulty)


def test_mine_block():
    blockchain = Blockchain()
    blockchain.create_genesis_block(difficulty=4)
    miner = Miner(blockchain)
    recipient_address = "test_address"

    previous_last_block = blockchain.last_block

    block = miner.mine(recipient_address)

    assert block == blockchain.last_block
    assert block.previous_hash == previous_last_block.hash, f"Expected previous_hash to be {previous_last_block.hash}, but got {block.previous_hash}"
    assert block.transactions[-1]['recipient'] == recipient_address
    assert block.transactions[-1]['amount'] == 1  # Mining reward
    assert block.proof is not None
    assert blockchain.valid_chain()
