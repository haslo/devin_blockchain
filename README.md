# Blockchain WIP

The Developer's Blockchain.

Implementation in Python. Not yet efficient, but clear and extensible.

Work in Progress. I'll let you know if / when that changes.

## Overview

This project implements a basic blockchain and provides scripts to test the blockchain functionality. The blockchain supports adding transactions, mining new blocks, and verifying
the integrity of the chain.

## Setup

To get started with the haslo Blockchain, follow these steps:

Clone the repository:

```
git clone https://github.com/haslo/haslo_blockchain
```

Navigate to the project directory:

```
cd haslo_blockchain
```

Create a virtual environment (optional but recommended):

```
python3 -m venv /venv
```

Activate the virtual environment:

```
source /venv/bin/activate
```

Install the required packages:

```
pip install -r requirements.txt
```

Run the test script to see the blockchain in action:

```
python blockchain.py
```

## Testing

Unit tests are written using pytest. To run the tests, execute the following command:

```
pytest
```

## Node Communication Protocol

For details on the node communication protocol used in the Devin Blockchain, see the [protocol.md](protocol.md) file.

# Meta

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
