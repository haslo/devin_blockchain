import hashlib

from haslo_blockchain.block import Block
from haslo_blockchain.util.difficulty_manager import DifficultyManager


class Blockchain:
    def __init__(self, difficulty, chain):
        self.difficulty = difficulty
        self.chain = chain
        if not self.valid_chain():
            raise ValueError("Invalid chain provided")

    def create_block(self, transactions, previous_hash, proof, difficulty, adjust_difficulty):
        block = Block(len(self.chain), transactions, previous_hash, proof, difficulty)
        self.chain.append(block)
        if adjust_difficulty:
            self.difficulty = DifficultyManager(self).adjusted_difficulty(DifficultyManager.DEFAULT_TARGET_BLOCK_TIME)
        return block

    def add_block(self, block):
        self.chain.append(block)

    def validate_block(self, block):
        if block.hash != block.compute_hash():
            return False
        last_block_proof = self.last_block.proof if self.last_block else 0
        if not self.valid_proof(last_block_proof, block.proof, block.difficulty):
            return False
        if self.chain and block.previous_hash != self.last_block.hash:
            return False
        return True

    @staticmethod
    def valid_proof(last_proof, proof, difficulty=4):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        valid = guess_hash[:difficulty] == "0" * difficulty
        return valid

    def valid_chain(self):
        if not isinstance(self.chain, list):
            return False
        if not all(isinstance(block, Block) for block in self.chain):
            return False
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            current_computed_hash = current_block.compute_hash()
            if current_block.hash != current_computed_hash:
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            block_difficulty = current_block.difficulty
            if not self.valid_proof(previous_block.proof, current_block.proof, block_difficulty):
                return False
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def __eq__(self, other):
        return self.chain == other.chain and self.last_block == other.last_block
