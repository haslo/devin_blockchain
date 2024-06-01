import unittest
from haslo_blockchain.transaction_components.gas import Gas


class TestGas(unittest.TestCase):
    def test_gas_initialization(self):
        gas = Gas(tip=1, max_fee=5, limit=12345)
        self.assertEqual(gas.tip, 1)
        self.assertEqual(gas.max_fee, 5)
        self.assertEqual(gas.limit, 12345)

    def test_gas_from_dict(self):
        gas_dict = {
            "tip": 1,
            "max_fee": 5,
            "limit": 12345,
        }
        gas = Gas.from_dict(gas_dict)
        self.assertEqual(gas.tip, 1)
        self.assertEqual(gas.max_fee, 5)
        self.assertEqual(gas.limit, 12345)

    def test_gas_to_dict(self):
        gas = Gas(tip=1, max_fee=5, limit=12345)
        gas_dict = gas.to_dict()
        expected_dict = {
            "tip": 1,
            "max_fee": 5,
            "limit": 12345,
        }
        self.assertEqual(gas_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
