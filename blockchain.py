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

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Genesis block has index 0, an empty transaction list, and "0" as the previous hash
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash):
        block = Block(len(self.chain), transactions, previous_hash)
        self.chain.append(block)
        return block

    def add_transaction(self, transaction):
        self.current_transactions.append(transaction)

    def proof_of_work(self, last_proof):
        # This is a simple Proof of Work Algorithm:
        # - Find a number p' such that hash(pp') contains 4 leading zeroes
        # - Where p is the previous proof, and p' is the new proof
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def valid_chain(self):
        # Check if a blockchain is valid
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            # Check if the block's hash is correct
            if current_block.hash != current_block.compute_hash():
                return False
            # Check if the block points to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def __repr__(self):
        return (f"Blockchain("
                f"chain={self.chain}, "
                f"current_transactions={self.current_transactions})")
