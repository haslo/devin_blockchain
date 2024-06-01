import unittest
from haslo_blockchain.transaction import Transaction
from haslo_blockchain.transaction_components.payloads.transfer_payload import TransferPayload
from haslo_blockchain.transaction_components.signature import Signature
from haslo_blockchain.transaction_components.gas import Gas

class TestTransaction(unittest.TestCase):
    def test_initialization(self):
        payload = {"recipient": "recipient_address", "amount": 100}
        gas = {"tip": 10, "max_fee": 50, "limit": 21000}
        signature = {"type": "type", "v": 27, "r": "r_value", "s": "s_value", "public_key": "public_key"}
        transaction = Transaction(
            transaction_type="transfer",
            sender="sender_address",
            payload=payload,
            nonce=1,
            chain_id=1,
            gas=gas,
            signature=signature
        )
        self.assertEqual(transaction.transaction_type, "transfer")
        self.assertEqual(transaction.sender, "sender_address")
        self.assertEqual(transaction.payload.recipient, "recipient_address")
        self.assertEqual(transaction.payload.amount, 100)
        self.assertEqual(transaction.nonce, 1)
        self.assertEqual(transaction.chain_id, 1)
        self.assertEqual(transaction.gas.tip, 10)
        self.assertEqual(transaction.gas.max_fee, 50)
        self.assertEqual(transaction.gas.limit, 21000)
        self.assertEqual(transaction.signature.v, 27)
        self.assertEqual(transaction.signature.r, "r_value")
        self.assertEqual(transaction.signature.s, "s_value")
        self.assertEqual(transaction.signature.public_key, "public_key")

    def test_from_dict(self):
        data = {
            "type": "transfer",
            "sender": "sender_address",
            "payload": {
                "recipient": "recipient_address",
                "amount": 100
            },
            "nonce": 1,
            "chain_id": 1,
            "gas": {
                "tip": 10,
                "max_fee": 50,
                "limit": 21000
            },
            "signature": {
                "type": "type",
                "v": 27,
                "r": "r_value",
                "s": "s_value",
                "public_key": "public_key"
            }
        }
        transaction = Transaction.from_dict(data)
        self.assertEqual(transaction.transaction_type, "transfer")
        self.assertEqual(transaction.sender, "sender_address")
        self.assertEqual(transaction.payload.recipient, "recipient_address")
        self.assertEqual(transaction.payload.amount, 100)
        self.assertEqual(transaction.nonce, 1)
        self.assertEqual(transaction.chain_id, 1)
        self.assertEqual(transaction.gas.tip, 10)
        self.assertEqual(transaction.gas.max_fee, 50)
        self.assertEqual(transaction.gas.limit, 21000)
        self.assertEqual(transaction.signature.v, 27)
        self.assertEqual(transaction.signature.r, "r_value")
        self.assertEqual(transaction.signature.s, "s_value")
        self.assertEqual(transaction.signature.public_key, "public_key")

    def test_to_dict(self):
        payload = {"recipient": "recipient_address", "amount": 100}
        gas = {"tip": 10, "max_fee": 50, "limit": 21000}
        signature = {"type": "type", "v": 27, "r": "r_value", "s": "s_value", "public_key": "public_key"}
        transaction = Transaction(
            transaction_type="transfer",
            sender="sender_address",
            payload=payload,
            nonce=1,
            chain_id=1,
            gas=gas,
            signature=signature
        )
        transaction_dict = transaction.to_dict()
        expected_dict = {
            "type": "transfer",
            "sender": "sender_address",
            "payload": {
                "recipient": "recipient_address",
                "amount": 100
            },
            "nonce": 1,
            "chain_id": 1,
            "gas": {
                "tip": 10,
                "max_fee": 50,
                "limit": 21000
            },
            "signature": {
                "type": "type",
                "v": 27,
                "r": "r_value",
                "s": "s_value",
                "public_key": "public_key"
            }
        }
        self.assertEqual(transaction_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
