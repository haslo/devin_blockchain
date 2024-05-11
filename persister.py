import json
import os
import datetime
import hashlib
from block import Block

class Persister:
    """
    The Persister class handles saving and loading blockchain data to and from .devinchain files in JSON format.
    """

    class InvalidJSONError(Exception):
        """Exception raised for errors in the JSON decoding process."""
        pass

    class BlockEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Block):
                # Create a copy of the block's data for serialization
                block_dict = {
                    'index': o.index,
                    'timestamp': o.timestamp,
                    'transactions': [txn.__dict__ for txn in o.transactions],
                    'previous_hash': o.previous_hash,
                    'proof': o.proof,
                    'hash': o.hash
                }
                return block_dict
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
                try:
                    chain_data = json.load(file)
                except json.JSONDecodeError:
                    raise Persister.InvalidJSONError("File is not valid JSON.")

                blockchain = Blockchain()
                blockchain.chain = []

                for block_data in chain_data:
                    block = Block(
                        block_data['index'],
                        block_data['transactions'],
                        block_data['previous_hash'],
                        block_data['proof'],
                        block_data['timestamp']
                    )
                    blockchain.chain.append(block)

                return blockchain
        else:
            raise FileNotFoundError(f"The file {filename} does not exist.")


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
