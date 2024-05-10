import json
import os
import base64
import datetime
import hashlib

class Persister:
    """
    The Persister class handles saving and loading blockchain data to and from .devinchain files in JSON format.
    """

    class BlockEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Block):
                # Convert datetime to Unix timestamp
                if isinstance(o.timestamp, datetime.datetime):
                    o.timestamp = o.timestamp.timestamp()
                # Encode the block's attributes as a dictionary
                block_dict = {
                    'index': o.index,
                    'timestamp': o.timestamp,
                    'transactions': o.transactions,
                    'previous_hash': o.previous_hash,
                    'proof': o.proof,  # Include the proof attribute
                    'hash': o.hash
                }
                # Encode binary data as base64
                if isinstance(o.data, bytes):
                    block_dict['data'] = base64.b64encode(o.data).decode('utf-8')
                return block_dict
            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, o)

    @staticmethod
    def save(blockchain, filename="blockchain.devinchain"):
        """
        Saves the blockchain to a file in JSON format using a custom encoder.
        :param blockchain: The blockchain to save.
        :param filename: The name of the file to save the blockchain to.
        """
        with open(filename, 'w') as file:
            json.dump(blockchain.chain, file, cls=Persister.BlockEncoder, indent=4, sort_keys=True)

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
                        [base64.b64decode(txn) if isinstance(txn, str) and txn.endswith('=') else txn for txn in block_data['transactions']],
                        block_data['previous_hash'],
                        datetime.datetime.fromtimestamp(block_data['timestamp']),
                        block_data['proof']  # Correctly deserialize the proof attribute
                    )
                    blockchain.chain.append(block)

                return blockchain
        return None

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
        self.timestamp = datetime.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.proof = proof
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.proof}"
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
                f"proof={self.proof}, "
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
        genesis_block = Block(0, [], "0", 1)
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
