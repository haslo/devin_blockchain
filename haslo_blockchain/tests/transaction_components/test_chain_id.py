import unittest
from haslo_blockchain.transaction_components.chain_id import ChainId


class TestChainId(unittest.TestCase):
    def test_chain_id_initialization(self):
        chain_id = ChainId(chain_id=1, version=2)
        self.assertEqual(chain_id.chain_id, 1)
        self.assertEqual(chain_id.version, 2)

    def test_chain_id_from_dict(self):
        chain_id_dict = {
            "chain_id": 2,
            "version": 3,
        }
        chain_id = ChainId.from_dict(chain_id_dict)
        self.assertEqual(chain_id.chain_id, 2)
        self.assertEqual(chain_id.version, 3)

    def test_chain_id_to_dict(self):
        chain_id = ChainId(chain_id=1, version=4)
        chain_id_dict = chain_id.to_dict()
        expected_dict = {
            "chain_id": 1,
            "version": 4,
        }
        self.assertEqual(chain_id_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
