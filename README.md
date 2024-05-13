# Blockchain WIP

The Developer's Blockchain.

Implementation in Python, assisted by [Devin](https://www.cognition.ai/introducing-devin).

Work in Progress. I'll let you know if / when that changes.

## Overview

This project implements a basic blockchain and provides scripts to test the blockchain functionality. The blockchain supports adding transactions, mining new blocks, and verifying the integrity of the chain.

## Setup

To get started with the Devin Blockchain, follow these steps:

1. Clone the repository:
```
git clone https://github.com/haslo/devin_blockchain
```

2. Navigate to the project directory:
```
cd devin_blockchain
```

3. Create a virtual environment (optional but recommended):
```
python3 -m venv /venv
```

4. Activate the virtual environment:
```
source /venv/bin/activate
```

5. Install the required packages:
```
pip install -r requirements.txt
```

6. Run the test script to see the blockchain in action:
```
python blockchain.py
```

## Testing

Unit tests are written using pytest. To run the tests, execute the following command:
```
pytest
```

## Persistence

The blockchain can be saved to and loaded from `.json` files, allowing for persistence across sessions. To save the current state of the blockchain, use the `save` method from the `Persister` class. To load an existing blockchain, use the `load` method.

## Mining

The blockchain includes a proof-of-work algorithm for mining new blocks. To mine a new block, use the `mine` method from the `Miner` class. Rewards for mining are added as transactions in the mined block, rewarding the miner with 1 HDC (haslo devin coin).

## Node Communication Protocol

For details on the node communication protocol used in the Devin Blockchain, see the [protocol.md](protocol.md) file.

# Meta

## Contributing

At the moment, I'm still building the basics. Contributions don't really make sense yet.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Guido Gloor / haslo (2024)
