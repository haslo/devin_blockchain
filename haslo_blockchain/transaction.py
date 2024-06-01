from haslo_blockchain.transaction_components.gas import Gas
from haslo_blockchain.transaction_components.payload import Payload
from haslo_blockchain.transaction_components.signature import Signature


class Transaction:
    def __init__(self, transaction_type, sender, payload, nonce, chain_id, gas, signature):
        self.transaction_type = transaction_type
        self.sender = sender
        self.payload = Payload.from_type_and_dict(transaction_type, payload)
        self.nonce = nonce
        self.chain_id = chain_id
        self.gas = Gas.from_dict(gas)
        self.signature = Signature.from_dict(signature)

    @classmethod
    def from_dict(cls, data):
        return Transaction(
            transaction_type=data['type'],
            sender=data['sender'],
            payload=data['payload'],
            nonce=data['nonce'],
            chain_id=data['chain_id'],
            gas=data['gas'],
            signature=data['signature'],
        )

    def to_dict(self):
        return {
            "type": self.transaction_type,
            "sender": self.sender,
            "payload": self.payload.to_dict(),
            "nonce": self.nonce,
            "chain_id": self.chain_id,
            "gas": self.gas.to_dict(),
            "signature": self.signature.to_dict(),
        }
