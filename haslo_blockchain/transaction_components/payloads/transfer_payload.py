class TransferPayload:
    def __init__(self, recipient, amount):
        self.recipient = recipient
        self.amount = amount

    @classmethod
    def from_dict(cls, payload_dict):
        return cls(
            recipient=payload_dict['recipient'],
            amount=payload_dict['amount'],
        )
