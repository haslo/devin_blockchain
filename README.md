# Devin Blockchain

A simple blockchain implementation in Python to demonstrate the core concepts of blockchain technology.

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
python3 -m venv blockchain-env
```

4. Activate the virtual environment:
```
source blockchain-env/bin/activate
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

The blockchain can be saved to and loaded from `.devinchain` files, allowing for persistence across sessions.

## Mining

The blockchain includes a proof-of-work algorithm for mining new blocks. Rewards for mining are added as transactions in the mined block.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Guido Gloor / haslo (2024)