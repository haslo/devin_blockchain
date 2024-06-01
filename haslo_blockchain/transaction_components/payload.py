from haslo_blockchain.transaction_components.payloads.transfer_payload import TransferPayload
from haslo_blockchain.util.magic_strings import MagicStrings


class Payload:
    @classmethod
    def from_type_and_dict(cls, transaction_type, data):
        #try:
        payload_class = {
            MagicStrings.TRANSACTION_TYPE_TRANSFER: TransferPayload,
        }[transaction_type]
        print(f'\nfound, {payload_class}')
        return payload_class.from_dict(data)
        #except KeyError:
        #    print('\nNOT found')
        #    return None
