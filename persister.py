import pickle
import os

class Persister:
    """
    The Persister class handles saving and loading blockchain data to and from .devinchain binary files.
    """

    @staticmethod
    def save(blockchain, filename="blockchain.devinchain"):
        """
        Saves the blockchain to a file.
        :param blockchain: The blockchain to save.
        :param filename: The name of the file to save the blockchain to.
        """
        with open(filename, 'wb') as file:
            pickle.dump(blockchain, file)

    @staticmethod
    def load(filename="blockchain.devinchain"):
        """
        Loads the blockchain from a file.
        :param filename: The name of the file to load the blockchain from.
        :return: The loaded blockchain.
        """
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return None
