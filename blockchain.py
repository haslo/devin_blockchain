import hashlib
import json
import time
import logging
import os
from block import Block

# Create a module-level logger object
logger = logging.getLogger(__name__)

# Set up logging configuration
log_level = os.getenv('BLOCKCHAIN_LOG_LEVEL', 'INFO')
logger.setLevel(logging.getLevelName(log_level))

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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
        self.difficulty = 4  # Default difficulty level of 4 leading zeroes
        self.test_mode = False  # Test mode is off by default
        # self.create_genesis_block()  # Genesis block creation is now handled externally

    def toggle_test_mode(self, mode: bool):
        """
        Toggle the test mode for the blockchain.
        :param mode: A boolean indicating whether to enable or disable test mode.
        """
        self.test_mode = mode
        self.difficulty = 2 if mode else 4  # Lower difficulty for testing

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to the chain.
        The block has index 0, an empty transaction list, and a previous hash of "0".
        """
        genesis_block = Block(0, [], "0", 0)
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash, proof, adjust_diff=False):
        """
        A function that adds a block to the blockchain.
        :param transactions: The list of transactions.
        :param previous_hash: The hash of the previous block.
        :param proof: The proof of work for this block.
        :param adjust_diff: A boolean indicating whether to adjust the difficulty after creating the block.
        :return: The new block.
        """
        block = Block(len(self.chain), transactions, previous_hash, proof)
        self.chain.append(block)
        self.current_transactions = []  # Clear the current transactions after creating a new block

        if adjust_diff:
            # Adjust the difficulty for the next block based on the average mining time
            self.adjust_difficulty()

        # Logging for debugging
        logger.info(f"Block created: {block}")
        logger.info(f"Block hash: {block.hash}")
        logger.info(f"Block's computed hash: {block.compute_hash()}")
        return block

    def validate_transaction(self, sender, recipient, amount):
        """
        Validates a transaction to ensure the sender and recipient are specified and the amount is positive.
        :param sender: The sender of the transaction.
        :param recipient: The recipient of the transaction.
        :param amount: The amount of the transaction.
        :raise ValueError: If sender or recipient is empty, or amount is not positive.
        """
        if not sender or not recipient:
            raise ValueError("Sender and recipient must be specified.")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

    def add_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions after validating it.
        :param sender: The sender of the transaction.
        :param recipient: The recipient of the transaction.
        :param amount: The amount of the transaction.
        """
        self.validate_transaction(sender, recipient, amount)
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)

    def proof_of_work(self, last_block):
        """
        Proof of Work Algorithm:
        - Find a number 'p' that when hashed with the previous block's proof a hash with a dynamic number of leading 0's is produced, based on the current difficulty level.
        :param last_block: The last block in the blockchain.
        :return: A new proof.
        """
        last_proof = last_block.proof
        proof = 0
        current_difficulty = self.difficulty if not self.test_mode else 2  # Use a lower difficulty if in test mode
        while not self.valid_proof(last_proof, proof, current_difficulty):
            proof += 1
        logger.info(f"Proof found: {proof}, Difficulty: {current_difficulty}")
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, difficulty=4):
        """
        Validates the Proof: Does hash(last_proof, proof) contain a certain number of leading zeroes defined by difficulty?
        :param last_proof: Previous proof.
        :param proof: Current proof.
        :param difficulty: The difficulty level of the proof of work required.
        :return: True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        valid = guess_hash[:difficulty] == "0" * difficulty
        logger.info(f"Validating proof: {proof}, Guess: {guess.decode()}, Guess hash: {guess_hash}, Required leading zeroes: {'0' * difficulty}, Valid: {valid}")
        return valid

    def adjust_difficulty(self, target_block_time=10):
        """
        Adjusts the difficulty of the proof of work algorithm dynamically to maintain a consistent block creation rate.
        :param target_block_time: The desired time (in seconds) between blocks.
        """
        if len(self.chain) <= 10:
            # Not enough blocks to calculate the average mining time, keep the current difficulty
            return

        # Calculate the average time taken to mine the last 10 blocks
        last_10_blocks = self.chain[-10:]
        total_time = sum(last_10_blocks[i].timestamp - last_10_blocks[i - 1].timestamp for i in range(1, 10))
        average_block_time = total_time / 9  # There are 9 intervals between 10 blocks

        # Adjust difficulty based on the average block time
        if average_block_time < target_block_time:
            self.difficulty += 1
        elif average_block_time > target_block_time:
            self.difficulty = max(1, self.difficulty - 1)  # Ensure difficulty does not go below 1

        logger.info(f"Difficulty adjusted to {self.difficulty}. Average block time: {average_block_time:.2f}s")

    def valid_chain(self):
        """
        Determine if a given blockchain is valid.
        :return: True if valid, False if not.
        """
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            logger.debug(f"Validating block at index {i} with hash {current_block.hash}")
            # Check if the current block's hash is correct
            current_computed_hash = current_block.compute_hash()
            logger.debug(f"Computed hash for block at index {i}: {current_computed_hash}, Difficulty used: {self.difficulty}")
            if current_block.hash != current_computed_hash:
                logger.error(f"Invalid block at index {i}: Stored hash {current_block.hash} does not match computed hash {current_computed_hash}.")
                return False
            # Check if the current block's previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"Invalid link from block at index {i} to index {i-1}: Previous hash {current_block.previous_hash} does not match previous block's hash {previous_block.hash}.")
                return False
            # Verify the proof of work for each block
            if not self.valid_proof(previous_block.proof, current_block.proof, self.difficulty):
                logger.error(f"Invalid proof of work at block index {i}: Proof {current_block.proof} does not meet difficulty criteria of {self.difficulty}.")
                return False
        logger.info("All blocks are valid and correctly linked.")
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
