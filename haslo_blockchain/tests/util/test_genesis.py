import unittest
from haslo_blockchain.util.genesis import Genesis
from haslo_blockchain.blockchain import Block, Blockchain
from haslo_blockchain.security.hashing import Hashing

class TestGenesis(unittest.TestCase):
    def test_genesis_initialization(self):
        genesis = Genesis(difficulty=1)
        self.assertEqual(genesis.difficulty, 1)

    def test_create_block(self):
        genesis = Genesis(difficulty=1)
        block = genesis.create_block(0, [], '0', 0)
        self.assertIsInstance(block, Block)
        self.assertEqual(block.index, 0)
        self.assertEqual(block.transactions, [])
        self.assertEqual(block.previous_hash, '0')
        self.assertEqual(block.proof, 0)
        self.assertEqual(block.difficulty, 1)
        self.assertIsNotNone(block.current_hash)

    def test_create_genesis_block(self):
        genesis = Genesis(difficulty=1)
        block = genesis.create_genesis_block()
        self.assertIsInstance(block, Block)
        self.assertEqual(block.index, 0)
        self.assertEqual(block.transactions, [])
        self.assertEqual(block.previous_hash, '0')
        self.assertEqual(block.proof, 0)
        self.assertEqual(block.difficulty, 1)
        self.assertIsNotNone(block.current_hash)

    def test_create_genesis_blockchain(self):
        genesis = Genesis(difficulty=1)
        blockchain = genesis.create_genesis_blockchain()
        self.assertIsInstance(blockchain, Blockchain)
        self.assertEqual(len(blockchain.chain), 1)
        self.assertEqual(blockchain.chain[0].index, 0)
        self.assertEqual(blockchain.chain[0].transactions, [])
        self.assertEqual(blockchain.chain[0].previous_hash, '0')
        self.assertEqual(blockchain.chain[0].proof, 0)
        self.assertEqual(blockchain.chain[0].difficulty, 1)
        self.assertIsNotNone(blockchain.chain[0].current_hash)

if __name__ == '__main__':
    unittest.main()
