import hashlib
import json
import time

class Block:
    """
    A Block represents each 'item' in the blockchain.
    """
    def __init__(self, index, transactions, previous_hash, proof):
        """
        Constructor for the `Block` class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions.
        :param previous_hash: Hash of the previous block in the chain.
        :param proof: The proof of work for this block.
        """
        self.index = index
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        """
        A function to print out the block contents in a readable format.
        """
        return (f"Block("
                f"index={self.index}, "
                f"timestamp={self.timestamp}, "
                f"transactions={self.transactions}, "
                f"previous_hash={self.previous_hash}, "
                f"hash={self.hash})")

class Blockchain:
    """
    The Blockchain class is a wrapper around the chain of blocks and includes methods to add and validate blocks.
    """
    def __init__(self):
        """
        The constructor for the `Blockchain` class.
        """
        self.chain = []
        self.current_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to the chain.
        The block has index 0, an empty transaction list, and a previous hash of "0".
        """
        genesis_block = Block(0, [], "0", 0)
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash, proof):
        """
        A function that adds a block to the blockchain.
        :param transactions: The list of transactions.
        :param previous_hash: The hash of the previous block.
        :param proof: The proof of work for this block.
        :return: The new block.
        """
        block = Block(len(self.chain), transactions, previous_hash, proof)
        self.chain.append(block)
        self.current_transactions = []  # Clear the current transactions after creating a new block
        return block

    def add_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions.
        :param sender: The sender of the transaction.
        :param recipient: The recipient of the transaction.
        :param amount: The amount of the transaction.
        """
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)

    def proof_of_work(self, last_proof):
        """
        Proof of Work Algorithm:
        - Find a number 'p' that when hashed with the previous block's solution a hash with 4 leading 0's is produced.
        :param last_proof: The proof of the previous block.
        :return: A new proof.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: Previous proof.
        :param proof: Current proof.
        :return: True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def valid_chain(self):
        """
        Determine if a given blockchain is valid.
        :return: True if valid, False if not.
        """
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            # Print statements for debugging
            print(f"Previous block's hash: {previous_block.hash}")
            print(f"Current block's hash: {current_block.hash}")
            print(f"Computed hash for current block: {current_block.compute_hash()}")
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    @property
    def last_block(self):
        """
        Returns the last block in the current blockchain.
        """
        return self.chain[-1] if self.chain else None

    def __repr__(self):
        """
        A function to print out the blockchain contents in a readable format.
        """
        return (f"Blockchain("
                f"chain={self.chain}, "
                f"current_transactions={self.current_transactions})")

# Test the blockchain implementation
if __name__ == '__main__':
    # Create a blockchain
    blockchain = Blockchain()

    # Add a transaction
    blockchain.add_transaction("Alice pays Bob 5 HDC")

    # Mine a block
    last_block = blockchain.chain[-1]
    last_proof = last_block.hash
    proof = blockchain.proof_of_work(last_proof)

    # Reward for finding the proof (For simplicity, the sender is "0" to signify that this node has mined a new coin)
    blockchain.add_transaction("0 pays Devin 1 HDC")

    # Forge the new Block by adding it to the chain
    previous_hash = last_block.hash
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof)

    print(f"Block has been added to the blockchain: {block}")
    print(f"The blockchain now contains {len(blockchain.chain)} blocks")
