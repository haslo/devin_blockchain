class Block:
    def __init__(self, index, transactions, previous_hash, proof, difficulty, timestamp, hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.difficulty = difficulty
        self.hash = hash

    def __eq__(self, other):
        return (self.index == other.index and
                self.timestamp == other.timestamp and
                self.transactions == other.transactions and
                self.previous_hash == other.previous_hash and
                self.proof == other.proof and
                self.difficulty == other.difficulty and
                self.hash == other.hash)
