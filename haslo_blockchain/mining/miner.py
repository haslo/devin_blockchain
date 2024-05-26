import random


# TODO this does nothing, make it do something

class Miner:
    @staticmethod
    def proof_of_work(blockchain, last_block):
        last_proof = last_block.proof
        proof = random.randint(0, 999999999)
        while not blockchain.valid_proof(last_proof, proof, blockchain.difficulty):
            proof = random.randint(0, 999999999)
        return proof
