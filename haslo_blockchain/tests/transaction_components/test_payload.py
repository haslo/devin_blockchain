import unittest
from haslo_blockchain.transaction_components.payload import Payload


class TestPayload(unittest.TestCase):
    def test_transfer_payload_from_dict(self):
        payload_dict = {
            "recipient": "recipient",
            "amount": "amount",
        }
        payload = Payload.from_type_and_dict("transfer", payload_dict)
        self.assertEqual(payload.__class__.__name__, "TransferPayload")
        self.assertEqual(payload.recipient, "recipient")
        self.assertEqual(payload.amount, "amount")


if __name__ == '__main__':
    unittest.main()
