import hashlib
import datetime

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return (f"Block("
                f"index={self.index}, "
                f"timestamp={self.timestamp}, "
                f"transactions={self.transactions}, "
                f"previous_hash={self.previous_hash}, "
                f"hash={self.hash})")
