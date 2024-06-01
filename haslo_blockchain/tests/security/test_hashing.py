import unittest
from haslo_blockchain.security.hashing import Hashing


class TestHashing(unittest.TestCase):
    def test_compute_block_hash(self):
        class MockTransaction:
            def to_dict(self):
                return {"mock": "transaction"}

        class MockBlock:
            index = 1
            timestamp = 1234567890
            transactions = [MockTransaction()]
            previous_hash = "previous_hash"
            proof = "proof"
            difficulty = 1

        block = MockBlock()
        block_hash = Hashing.compute_block_hash(block)
        self.assertIsNotNone(block_hash)
        self.assertEqual(len(block_hash), 64)  # SHA-256 hash length is 64 characters


if __name__ == '__main__':
    unittest.main()
