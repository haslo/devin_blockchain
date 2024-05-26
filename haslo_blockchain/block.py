import json
import hashlib
import time


class Block:
    def __init__(self, index, transactions, previous_hash, proof, difficulty, timestamp=None):
        self.index = index
        self.timestamp = int(timestamp if timestamp is not None else time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.difficulty = difficulty
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [transaction.to_dict() for transaction in self.transactions],
            'previous_hash': self.previous_hash,
            'proof': self.proof,
            'difficulty': self.difficulty
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __eq__(self, other):
        return (self.index == other.index and
                self.timestamp == other.timestamp and
                self.transactions == other.transactions and
                self.previous_hash == other.previous_hash and
                self.proof == other.proof and
                self.difficulty == other.difficulty and
                self.hash == other.hash)
