import unittest
from haslo_blockchain.util.magic_strings import MagicStrings

class TestMagicStrings(unittest.TestCase):
    def test_transaction_type_transfer(self):
        self.assertEqual(MagicStrings.TRANSACTION_TYPE_TRANSFER, 'transfer')

if __name__ == '__main__':
    unittest.main()
