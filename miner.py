import hashlib
import json
from time import time

class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def mine(self, recipient_address):
        """
        This function is where you do the mining:
        - Run the proof of work algorithm to get the next proof
        - Reward for finding the proof is 1 HDC (haslo devin coin)
        - Forge the new Block by adding it to the chain
        """
        last_block = self.blockchain.last_block
        last_proof = last_block.proof
        proof = self.proof_of_work(last_proof)

        # Reward for finding the proof
        self.blockchain.add_transaction(
            sender="0",  # indicates that this node has mined a new block
            recipient=recipient_address,
            amount=1  # mining reward is 1 HDC
        )

        # The previous hash must be computed after any new transactions are added
        # but before the new block is created to ensure it reflects the state of the blockchain
        # just before the new block is added.
        previous_hash = self.blockchain.last_block.hash

        block = self.blockchain.create_block(self.blockchain.current_transactions, previous_hash, proof)

        return block
