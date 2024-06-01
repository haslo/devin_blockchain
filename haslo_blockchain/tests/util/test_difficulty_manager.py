import unittest
from haslo_blockchain.util.difficulty_manager import DifficultyManager


class MockBlock:
    def __init__(self, timestamp):
        self.timestamp = timestamp


class MockBlockchain:
    def __init__(self, difficulty, chain):
        self.difficulty = difficulty
        self.chain = chain


class TestDifficultyManager(unittest.TestCase):
    def test_initialization(self):
        blockchain = MockBlockchain(difficulty=1, chain=[])
        difficulty_manager = DifficultyManager(blockchain)
        self.assertEqual(difficulty_manager.blockchain, blockchain)

    def test_adjusted_difficulty(self):
        original_difficulty = 5
        blockchain = MockBlockchain(difficulty=original_difficulty, chain=[
            MockBlock(timestamp=1),
            MockBlock(timestamp=2),
            MockBlock(timestamp=3),
            MockBlock(timestamp=4),
            MockBlock(timestamp=5),
            MockBlock(timestamp=6),
            MockBlock(timestamp=7),
            MockBlock(timestamp=8),
            MockBlock(timestamp=9),
            MockBlock(timestamp=10),
            MockBlock(timestamp=11),
        ])
        difficulty_manager = DifficultyManager(blockchain)
        self.assertEqual(original_difficulty, difficulty_manager.adjusted_difficulty(1))
        self.assertEqual(original_difficulty + 1, difficulty_manager.adjusted_difficulty(10))
        self.assertEqual(original_difficulty + 1, difficulty_manager.adjusted_difficulty(100))
        self.assertEqual(original_difficulty - 1, difficulty_manager.adjusted_difficulty(0.5))

    def test_unchanged_short_difficulty(self):
        original_difficulty = 5
        blockchain = MockBlockchain(difficulty=original_difficulty, chain=[
            MockBlock(timestamp=1),
            MockBlock(timestamp=2),
            MockBlock(timestamp=3),
            MockBlock(timestamp=4),
        ])
        difficulty_manager = DifficultyManager(blockchain)
        self.assertEqual(original_difficulty, difficulty_manager.adjusted_difficulty(1))
        self.assertEqual(original_difficulty, difficulty_manager.adjusted_difficulty(10))
        self.assertEqual(original_difficulty, difficulty_manager.adjusted_difficulty(100))
        self.assertEqual(original_difficulty, difficulty_manager.adjusted_difficulty(0.5))


if __name__ == '__main__':
    unittest.main()
