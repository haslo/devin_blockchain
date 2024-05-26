from haslo_blockchain.block import Block
from haslo_blockchain.blockchain import Blockchain


class Genesis:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(
            0,
            [],
            "0",
            0,
            self.difficulty,
            0,
        )

    def create_genesis_blockchain(self):
        return Blockchain(
            self.difficulty,
            [
                self.create_genesis_block(),
            ]
        )
