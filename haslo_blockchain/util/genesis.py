import time

from haslo_blockchain.block import Block
from haslo_blockchain.blockchain import Blockchain
from haslo_blockchain.security.hashing import Hashing


class Genesis:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def create_block(self, index, transactions, previous_hash, proof):
        timestamp = time.time()
        block = Block(
            index,
            transactions,
            previous_hash,
            proof,
            self.difficulty,
            timestamp,
            None,
        )
        block.hash = Hashing.compute_block_hash(block)
        return block



    def create_genesis_block(self):
        return self.create_block(
            0,
            [],
            '0',
            0,
        )

    def create_genesis_blockchain(self):
        return Blockchain(
            self.difficulty,
            [
                self.create_genesis_block(),
            ]
        )
