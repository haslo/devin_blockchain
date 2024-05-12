import json
import os
import hashlib
from blockchain.block import Block


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
                    'transactions': o.transactions,
                    'previous_hash': o.previous_hash,
                    'proof': o.proof,
                    'difficulty': o.difficulty,
                    'hash': o.hash
                }
                return block_dict
            return json.JSONEncoder.default(self, o)

    @staticmethod
    def save(blockchain, filename="blockchain.json"):
        """
        Saves the blockchain to a file in JSON format using a custom encoder.
        :param blockchain: The blockchain to save.
        :param filename: The name of the file to save the blockchain to.
        """
        with open(filename, 'w') as file:
            json.dump(blockchain.chain, file, cls=Persister.BlockEncoder, indent=4, sort_keys=True)

    @staticmethod
    def load(filename="blockchain.json"):
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

                from blockchain.blockchain import Blockchain
                blockchain = Blockchain()
                blockchain.chain = []

                for block_data in chain_data:
                    block = Block(
                        block_data['index'],
                        block_data['transactions'],
                        block_data['previous_hash'],
                        block_data['proof'],
                        block_data['difficulty'],
                        block_data['timestamp']
                    )
                    blockchain.chain.append(block)

                return blockchain
        else:
            raise FileNotFoundError(f"The file {filename} does not exist.")
