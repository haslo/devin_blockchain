import json
import hashlib
import json


class Hashing:
    @staticmethod
    def compute_block_hash(block):
        block_string = json.dumps({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': [transaction.to_dict() for transaction in block.transactions],
            'previous_hash': block.previous_hash,
            'proof': block.proof,
            'difficulty': block.difficulty,
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
