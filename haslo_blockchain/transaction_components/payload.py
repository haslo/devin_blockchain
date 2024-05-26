from haslo_blockchain.transaction import Transaction
from haslo_blockchain.transaction_components.payloads.transfer_payload import TransferPayload


class Payload:
    @classmethod
    def from_type_and_dict(cls, transaction_type, data):
        try:
            payload_class = {
                Transaction.TYPE_TRANSFER: TransferPayload,
            }[transaction_type]
            return payload_class.from_dict(data)
        except KeyError:
            return None
