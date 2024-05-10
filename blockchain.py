import hashlib
import json
import time
import logging
from block import Block


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        # Logging for debugging
        logging.info(f"Block created: {block}")
        logging.info(f"Block hash: {block.hash}")
        logging.info(f"Block's computed hash: {block.compute_hash()}")
        return block

    def add_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions after validating it.
        :param sender: The sender of the transaction.
        :param recipient: The recipient of the transaction.
        :param amount: The amount of the transaction.
        :raise ValueError: If sender or recipient is empty, or amount is not positive.
        """
        if not sender or not recipient:
            raise ValueError("Sender and recipient must be specified.")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

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
            # Check if the current block's hash is correct
            current_computed_hash = current_block.compute_hash()
            if current_block.hash != current_computed_hash:
                logging.error(f"Invalid block at index {i}: Stored hash {current_block.hash} does not match computed hash {current_computed_hash}.")
                return False
            # Check if the current block's previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                logging.error(f"Invalid link from block at index {i} to index {i-1}: Previous hash {current_block.previous_hash} does not match previous block's hash {previous_block.hash}.")
                return False
        logging.info("All blocks are valid and correctly linked.")
        return True

    @property
    def last_block(self):
        """
        Returns the last block in the current blockchain.
        """
        return self.chain[-1] if self.chain else None

    def __eq__(self, other):
        """
        Overloads the equality operator to compare two Blockchain instances.
        :param other: The other Blockchain instance to compare with.
        :return: True if both instances have the same chain and current transactions, False otherwise.
        """
        return self.chain == other.chain and self.current_transactions == other.current_transactions

    def __repr__(self):
        """
        A function to print out the blockchain contents in a readable format.
        """
        return (f"Blockchain("
                f"chain={self.chain}, "
                f"current_transactions={self.current_transactions})")

# End of the Blockchain class
