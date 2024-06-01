import unittest
from unittest.mock import Mock
from haslo_blockchain.mining.miner import Miner

class TestMiner(unittest.TestCase):
    def test_proof_of_work(self):
        # Create a mock blockchain with a valid_proof method
        mock_blockchain = Mock()
        mock_blockchain.difficulty = 4
        mock_blockchain.valid_proof = Mock(side_effect=lambda last_proof, proof, difficulty: proof % 10000 == 0)

        # Create a mock last_block with a proof attribute
        mock_last_block = Mock()
        mock_last_block.proof = 12345

        # Call the proof_of_work method
        proof = Miner.proof_of_work(mock_blockchain, mock_last_block)

        # Verify that the proof is valid
        self.assertTrue(mock_blockchain.valid_proof(mock_last_block.proof, proof, mock_blockchain.difficulty))

if __name__ == '__main__':
    unittest.main()
