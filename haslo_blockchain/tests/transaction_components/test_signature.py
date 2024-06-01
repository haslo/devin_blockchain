import unittest
from haslo_blockchain.transaction_components.signature import Signature


class TestSignature(unittest.TestCase):
    def test_signature_initialization(self):
        signature = Signature(signature_type="type", r="r_value", s="s_value", v="v_value", public_key="public_key_value")
        self.assertEqual(signature.signature_type, "type")
        self.assertEqual(signature.r, "r_value")
        self.assertEqual(signature.s, "s_value")
        self.assertEqual(signature.v, "v_value")
        self.assertEqual(signature.public_key, "public_key_value")

    def test_signature_from_dict(self):
        signature_dict = {
            "type": "type",
            "r": "r_value",
            "s": "s_value",
            "v": "v_value",
            "public_key": "public_key_value"
        }
        signature = Signature.from_dict(signature_dict)
        self.assertEqual(signature.signature_type, "type")
        self.assertEqual(signature.r, "r_value")
        self.assertEqual(signature.s, "s_value")
        self.assertEqual(signature.v, "v_value")
        self.assertEqual(signature.public_key, "public_key_value")

    def test_signature_to_dict(self):
        signature = Signature(signature_type="type", r="r_value", s="s_value", v="v_value", public_key="public_key_value")
        signature_dict = signature.to_dict()
        expected_dict = {
            "type": "type",
            "r": "r_value",
            "s": "s_value",
            "v": "v_value",
            "public_key": "public_key_value"
        }
        self.assertEqual(signature_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
