from blockchain.transaction_components.gas import Gas
from blockchain.transaction_components.payload import Payload
from blockchain.transaction_components.signature import Signature


# TODO add validation, but ffs without Devin's utter BS

class Transaction:
    TYPE_TRANSFER = 'transfer'

    def __init__(self, transaction_type, sender, payload, nonce, chain, gas, signature):
        self.transaction_type = transaction_type
        self.sender = sender
        self.payload = Payload.from_type_and_dict(transaction_type, payload)
        self.nonce = nonce
        self.chain = chain
        self.gas = Gas.from_dict(gas)
        self.signature = Signature.from_dict(signature)

    @classmethod
    def from_dict(cls, data):
        return Transaction(
            transaction_type=data['type'],
            sender=data['sender'],
            payload=data['payload'],
            nonce=data['nonce'],
            chain=data['chain'],
            gas=data['gas'],
            signature=data['signature'],
        )

    def to_dict(self):
        self.validate_transaction()
        return {
            "type": self.transaction_type,
            "sender": self.sender,
            "payload": self.payload,
            "nonce": self.nonce,
            "chain": self.chain,
            "gas": self.gas,
            "signature": self.signature
        }
