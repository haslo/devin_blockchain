import json
import os

class Persister:
    """
    The Persister class handles saving and loading blockchain data to and from .devinchain files in JSON format.
    """

    @staticmethod
    def save(blockchain, filename="blockchain.devinchain"):
        """
        Saves the blockchain to a file in JSON format.
        :param blockchain: The blockchain to save.
        :param filename: The name of the file to save the blockchain to.
        """
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)

        with open(filename, 'w') as file:
            json.dump(chain_data, file, indent=4, sort_keys=True, default=str)

    @staticmethod
    def load(filename="blockchain.devinchain"):
        """
        Loads the blockchain from a file in JSON format.
        :param filename: The name of the file to load the blockchain from.
        :return: The loaded blockchain if successful, None otherwise.
        """
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                chain_data = json.load(file)
                blockchain = Blockchain()
                blockchain.chain = []

                for block_data in chain_data:
                    block = Block(
                        block_data['index'],
                        block_data['transactions'],
                        block_data['previous_hash'],
                        block_data['timestamp'],
                        block_data['hash']
                    )
                    blockchain.chain.append(block)

                return blockchain
        return None
```
class Block:
    """
    A Block represents each 'item' in the blockchain.
    """
    def __init__(self, index, transactions, previous_hash):
        """
        Constructor for the `Block` class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions.
        :param previous_hash: Hash of the previous block in the chain.
        """
        self.index = index
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
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
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash):
        """
        A function that adds a block to the blockchain.
        :param transactions: The list of transactions.
        :param previous_hash: The hash of the previous block.
        :return: The new block.
        """
        block = Block(len(self.chain), transactions, previous_hash)
        self.chain.append(block)
        return block

    def add_transaction(self, transaction):
        """
        Adds a new transaction to the list of transactions.
        :param transaction: The transaction to add.
        """
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
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def __repr__(self):
        """
        A function to print out the blockchain contents in a readable format.
        """
        return (f"Blockchain("
                f"chain={self.chain}, "
                f"current_transactions={self.current_transactions})")
