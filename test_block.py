import unittest
from block import Block

class TestBlock(unittest.TestCase):

    def test_block_creation(self):
        """Test the creation of a block and its attributes."""
        transactions = [{'sender': 'a', 'recipient': 'b', 'amount': 1}]
        previous_hash = 'abc'
        proof = 12345
        block = Block(index=1, transactions=transactions, previous_hash=previous_hash, proof=proof)

        self.assertEqual(block.index, 1)
        self.assertEqual(block.transactions, transactions)
        self.assertEqual(block.previous_hash, previous_hash)
        self.assertEqual(block.proof, proof)
        self.assertIsNotNone(block.timestamp)

    def test_compute_hash(self):
        """Test the compute_hash method."""
        transactions = [{'sender': 'a', 'recipient': 'b', 'amount': 1}]
        previous_hash = 'abc'
        proof = 12345
        block = Block(index=1, transactions=transactions, previous_hash=previous_hash, proof=proof)
        computed_hash = block.compute_hash()

        self.assertIsInstance(computed_hash, str)
        self.assertEqual(len(computed_hash), 64)  # Assuming SHA-256 is used

if __name__ == '__main__':
    unittest.main()
