import unittest

from haslo_blockchain.block import Block


class TestBlock(unittest.TestCase):
    def test_constructor(self):
        block = Block(
            'index',
            'transactions',
            'previous_hash',
            'proof',
            'difficulty',
            'timestamp',
            'current_hash',
        )
        self.assertEqual(block.index, 'index')
        self.assertEqual(block.transactions, 'transactions')
        self.assertEqual(block.previous_hash, 'previous_hash')
        self.assertEqual(block.proof, 'proof')
        self.assertEqual(block.difficulty, 'difficulty')
        self.assertEqual(block.timestamp, 'timestamp')
        self.assertEqual(block.current_hash, 'current_hash')
