import unittest
from haslo_blockchain.transaction_components.payloads.transfer_payload import TransferPayload


class TestTransferPayload(unittest.TestCase):
    def test_transfer_payload_initialization(self):
        payload = TransferPayload(recipient="recipient_address", amount=100)
        self.assertEqual(payload.recipient, "recipient_address")
        self.assertEqual(payload.amount, 100)

    def test_transfer_payload_from_dict(self):
        payload_dict = {
            "recipient": "recipient_address",
            "amount": 100
        }
        payload = TransferPayload.from_dict(payload_dict)
        self.assertEqual(payload.recipient, "recipient_address")
        self.assertEqual(payload.amount, 100)

    def test_transfer_payload_to_dict(self):
        payload = TransferPayload(recipient="recipient_address", amount=100)
        payload_dict = payload.to_dict()
        expected_dict = {
            "recipient": "recipient_address",
            "amount": 100
        }
        self.assertEqual(payload_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
