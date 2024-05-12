import hashlib
import json
from ecdsa import VerifyingKey, BadSignatureError, NIST384p
import random
from blockchain.block import Block
from util.logger import Logger


class Blockchain:
    """
    The Blockchain class is a wrapper around the chain of blocks and includes methods to add and validate blocks.
    """

    def __init__(self, chain=None):
        """
        The constructor for the `Blockchain` class.
        :param chain: An optional list of blocks to initialize the blockchain with.
        """
        self.current_transactions = []
        self.difficulty = 4  # Default difficulty level of 4 leading zeroes
        self.test_mode = False  # Test mode is off by default
        self.logger = Logger()
        if chain is not None:
            self.chain = chain
            self.logger.info(f"Initializing Blockchain with provided chain: {self.chain}")
            if not self.valid_chain():
                self.logger.error("Invalid chain provided during initialization.")
                raise ValueError("Invalid chain provided")
        else:
            self.chain = []
            self.logger.debug("No chain provided, initializing with empty chain.")

    def toggle_test_mode(self, mode: bool):
        """
        Toggle the test mode for the blockchain.
        :param mode: A boolean indicating whether to enable or disable test mode.
        """
        self.test_mode = mode
        self.difficulty = 2 if mode else 4  # Lower difficulty for testing

    def create_genesis_block(self, difficulty=0):
        """
        A function to generate genesis block and appends it to the chain.
        The block has index 0, an empty transaction list, and a previous hash of "0".
        """
        genesis_block = Block(0, [], "0", 0, difficulty, 0)
        self.chain.append(genesis_block)

    def create_block(self, transactions, previous_hash, proof, difficulty, adjust_diff=False):
        """
        A function that adds a block to the blockchain.
        :param transactions: The list of transactions.
        :param previous_hash: The hash of the previous block.
        :param proof: The proof of work for this block.
        :param difficulty: The difficulty level of the block.
        :param adjust_diff: A boolean indicating whether to adjust the difficulty after creating the block.
        :return: The new block.
        """
        block = Block(len(self.chain), transactions, previous_hash, proof, difficulty)
        self.chain.append(block)
        self.current_transactions = []  # Clear the current transactions after creating a new block

        if adjust_diff:
            # Adjust the difficulty for the next block based on the average mining time
            self.adjust_difficulty()

        # Logging for debugging
        self.logger.debug(f"Block created: {block}")
        self.logger.debug(f"Block hash: {block.hash}")
        self.logger.debug(f"Block's computed hash: {block.compute_hash()}")
        return block

    def add_block(self, block):
        self.chain.append(block)


    def validate_transaction(self, transaction):
        """
        Validates a transaction to ensure it follows the new protocol structure and that the signature is valid.
        :param transaction: The transaction to validate.
        :raise ValueError: If the transaction is invalid.
        """
        required_fields = ["type", "sender", "payload", "nonce", "chain", "gas", "signature"]
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Transaction is missing required field: {field}")

        # Validate payload structure
        if not isinstance(transaction['payload'], dict) or "recipient" not in transaction['payload'] or "amount" not in transaction['payload']:
            raise ValueError("Invalid payload structure")

        # Validate nonce
        if not isinstance(transaction['nonce'], int) or transaction['nonce'] < 0:
            raise ValueError("Invalid nonce")

        # Validate gas structure and values
        if not isinstance(transaction['gas'], dict) or "tip" not in transaction['gas'] or "max_fee" not in transaction['gas'] or "limit" not in transaction['gas']:
            raise ValueError("Invalid gas structure")
        if any(not isinstance(transaction['gas'][key], int) or transaction['gas'][key] < 0 for key in ["tip", "max_fee", "limit"]):
            raise ValueError("Invalid gas values")

        # Validate signature structure and values
        if not isinstance(transaction['signature'], dict) or "type" not in transaction['signature'] or "r" not in transaction['signature'] or "s" not in transaction['signature'] or "v" not in transaction['signature'] or "public_key" not in transaction['signature']:
            raise ValueError("Invalid signature structure")

        # Assuming validate_signature is a method to be implemented
        if not self.validate_signature(transaction):
            raise ValueError("Invalid signature")

    def validate_signature(self, transaction):
        """
        Validates the signature of a transaction.
        :param transaction: The transaction with the signature to validate.
        :return: True if the signature is valid, False otherwise.
        """
        signature = transaction['signature']
        message = json.dumps(transaction, sort_keys=True).encode()
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(signature['public_key']), curve=NIST384p)
            vk.verify(bytes.fromhex(signature['r'] + signature['s']), message)
            return True
        except BadSignatureError:
            return False

    def add_transaction(self, transaction):
        """
        Adds a new transaction to the list of transactions after validating it.
        :param transaction: The transaction dictionary.
        """
        # Validate the transaction
        self.validate_transaction(transaction)
        # If the transaction is valid, add it to the list of current transactions
        self.current_transactions.append(transaction)

    def proof_of_work(self, last_block):
        """
        Proof of Work Algorithm:
        - Find a number 'p' that when hashed with the previous block's proof a hash with a dynamic number of leading 0's is produced, based on the current difficulty level.
        :param last_block: The last block in the blockchain.
        :return: A new proof.
        """
        last_proof = last_block.proof
        proof = random.randint(0, 999999999)
        current_difficulty = self.difficulty if not self.test_mode else 2  # Use a lower difficulty if in test mode
        while not self.valid_proof(last_proof, proof, current_difficulty):
            proof = random.randint(0, 999999999)
        self.logger.debug(f"Proof found: {proof}, Difficulty: {current_difficulty}")
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
        Logger().debug(f"Validating proof: {proof}, Guess: {guess.decode()}, Guess hash: {guess_hash}, Required leading zeroes: {'0' * difficulty}, Valid: {valid}")
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

        self.logger.info(f"Difficulty adjusted to {self.difficulty}. Average block time: {average_block_time:.2f}s")

    def validate_block(self, block):
        """
        Validates a block by checking its hash, the proof of work, and the previous hash.
        :param block: The block to validate.
        :return: True if the block is valid, False otherwise.
        """
        # Check if the block's hash is correct
        if block.hash != block.compute_hash():
            self.logger.error(f"Invalid block: Computed hash does not match the block's hash.")
            return False

        # Check if the block's proof of work meets the difficulty criteria
        last_block_proof = self.last_block.proof if self.last_block else 0
        if not self.valid_proof(last_block_proof, block.proof, block.difficulty):
            self.logger.error(f"Invalid block: Proof of work does not meet difficulty criteria.")
            return False

        # Check if the block's previous hash matches the last block's hash
        if self.chain and block.previous_hash != self.last_block.hash:
            self.logger.error(f"Invalid block: Previous hash does not match the last block's hash.")
            return False

        return True

    def valid_chain(self):
        """
        Determine if a given blockchain is valid.
        :return: True if valid, False if not.
        """
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            self.logger.debug(f"Validating block at index {i} with hash {current_block.hash}")
            # Check if the current block's hash is correct
            current_computed_hash = current_block.compute_hash()
            self.logger.debug(f"Computed hash for block at index {i}: {current_computed_hash}, Difficulty used: {self.difficulty}")
            if current_block.hash != current_computed_hash:
                self.logger.error(f"Invalid block at index {i}: Stored hash {current_block.hash} does not match computed hash {current_computed_hash}.")
                return False
            # Check if the current block's previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                self.logger.error(
                    f"Invalid link from block at index {i} to index {i - 1}: Previous hash {current_block.previous_hash} does not match previous block's hash {previous_block.hash}.")
                return False
            # Verify the proof of work for each block
            block_difficulty = current_block.difficulty
            if not self.valid_proof(previous_block.proof, current_block.proof, block_difficulty):
                self.logger.error(f"Invalid proof of work at block index {i}: Proof {current_block.proof} does not meet difficulty criteria of {block_difficulty}.")
                return False
        self.logger.info("All blocks are valid and correctly linked.")
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
