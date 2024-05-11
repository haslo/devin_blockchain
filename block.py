import json
import hashlib
import time

class Block:
    """
    A Block represents each 'item' in the blockchain.
    """
    def __init__(self, index, transactions, previous_hash, proof, difficulty, timestamp=None):
        """
        Constructor for the `Block` class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions.
        :param previous_hash: Hash of the previous block in the chain.
        :param proof: The proof of work for this block.
        :param difficulty: The difficulty level at which the block was mined.
        :param timestamp: The timestamp when the block is created. Defaults to current time if not provided.
        """
        self.index = index
        self.timestamp = int(timestamp if timestamp is not None else time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.difficulty = difficulty
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'proof': self.proof,
            'difficulty': self.difficulty
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __eq__(self, other):
        """
        Overloads the equality operator to compare two Block instances.
        :param other: The other Block instance to compare with.
        :return: True if both instances have the same index, timestamp, transactions, previous_hash, proof, difficulty, and hash, False otherwise.
        """
        return (self.index == other.index and
                self.timestamp == other.timestamp and
                self.transactions == other.transactions and
                self.previous_hash == other.previous_hash and
                self.proof == other.proof and
                self.difficulty == other.difficulty and
                self.hash == other.hash)

    def __repr__(self):
        """
        A function to print out the block contents in a readable format.
        """
        return (f"Block("
                f"index={self.index}, "
                f"timestamp={self.timestamp}, "
                f"transactions={self.transactions}, "
                f"previous_hash={self.previous_hash}, "
                f"difficulty={self.difficulty}, "
                f"hash={self.hash})")
