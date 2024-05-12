import pytest
from unittest.mock import patch, PropertyMock
from blockchain.block import Block
from blockchain.blockchain import Blockchain


@pytest.fixture(autouse=True)
def blockchain():
    blockchain = Blockchain()
    blockchain.toggle_test_mode(True)
    blockchain.create_genesis_block()
    yield blockchain
    blockchain.toggle_test_mode(False)


def test_block_initialization():
    block = Block(5, [], "0123", 100, 10)
    assert block.index == 5
    assert block.transactions == []
    assert block.previous_hash == "0123"
    assert block.difficulty == 10
    assert block.hash is not None


def test_blockchain_initialization(blockchain):
    assert len(blockchain.chain) == 1  # Genesis block


def test_add_transaction(blockchain):
    transaction = {
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
        }
    }
    blockchain.add_transaction(transaction)
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == transaction


def test_add_transaction_invalid_sender(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction({
            "type": "transfer",
            "sender": "",
            "payload": {
                "recipient": "Bob",
                "amount": 5
            },
            "nonce": 0,
            "chain": {
                "chain_id": "HDC",
                "version": 1
            },
            "gas": {
                "tip": 1,
                "max_fee": 1000,
                "limit": 2000
            },
            "signature": {
                "type": "ECDSA",
                "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
                "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
                "v": "1b",
                "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
            }
        })


def test_proof_of_work(blockchain):
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    # The proof should be valid for the current difficulty level of the blockchain
    assert blockchain.valid_proof(last_block.proof, proof, blockchain.difficulty) is True


def test_valid_chain(blockchain):
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
        }
    })
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "0",
        "payload": {
            "recipient": "Devin",
            "amount": 1
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
    })
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    _new_block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof, previous_difficulty, adjust_diff=False)
    assert blockchain.valid_chain() is True, "The blockchain should be valid"


def test_chain_with_invalid_block(blockchain):
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
        }
    })  # Added closing parenthesis
    # Redundant transaction variable removed
    # This block was redundant and has been removed to clean up the test function


def test_add_transaction_invalid_recipient(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="", amount=5)


def test_add_transaction_invalid_amount(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="Bob", amount=-5)


def test_proof_of_work(blockchain):
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    # The proof should be valid for the current difficulty level of the blockchain
    assert blockchain.valid_proof(last_block.proof, proof, blockchain.difficulty) is True


def test_valid_chain(blockchain):
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
        }
    })
    blockchain.add_transaction(transaction)
    assert len(blockchain.current_transactions) == 1
    assert blockchain.current_transactions[0] == transaction


def test_add_transaction_invalid_sender(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="", recipient="Bob", amount=5)


def test_add_transaction_invalid_recipient(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="", amount=5)


def test_add_transaction_invalid_amount(blockchain):
    with pytest.raises(ValueError):
        blockchain.add_transaction(sender="Alice", recipient="Bob", amount=-5)


def test_proof_of_work(blockchain):
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    # The proof should be valid for the current difficulty level of the blockchain
    assert blockchain.valid_proof(last_block.proof, proof, blockchain.difficulty) is True


def test_valid_chain(blockchain):
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "00"*96
        }
    })
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "0",
        "payload": {
            "recipient": "Devin",
            "amount": 1
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "7fa6b9a6e0e27e9b9e1e95fc173fbec9f95a2ec3e6a4a12d327e3b2b6fcb60da",
            "s": "5e173f3d0e36a5f2c3c5e461c9ac5e3c9e5e9f5e3c5e9e7e5e3e9f2c5e2e8c5d",
            "v": "1b",
            "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
            "public_key": "00"*96
        }
    })
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    _new_block = blockchain.create_block(blockchain.current_transactions, previous_hash, proof, previous_difficulty, adjust_diff=False)
    assert blockchain.valid_chain() is True, "The blockchain should be valid"


def test_chain_with_invalid_block(blockchain):
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "Alice",
        "payload": {
            "recipient": "Bob",
            "amount": 5
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "00"*32,
            "s": "00"*32,
            "v": "00",
            "public_key": "00"*96
        }
    })
    last_block = blockchain.chain[-1]
    proof = blockchain.proof_of_work(last_block)
    blockchain.add_transaction({
        "type": "transfer",
        "sender": "0",
        "payload": {
            "recipient": "Devin",
            "amount": 1
        },
        "nonce": 0,
        "chain": {
            "chain_id": "HDC",
            "version": 1
        },
        "gas": {
            "tip": 1,
            "max_fee": 1000,
            "limit": 2000
        },
        "signature": {
            "type": "ECDSA",
            "r": "00"*32,
            "s": "00"*32,
            "v": "00",
            "public_key": "00"*96
        }
    })
    previous_hash = last_block.hash
    previous_difficulty = last_block.difficulty
    block = blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    block.transactions.append({"sender": "Eve", "recipient": "Mallory", "amount": 10})
    assert blockchain.valid_chain() is False, "The blockchain was tampered with"


def test_difficulty_adjustment_with_fewer_than_10_blocks(blockchain):
    original_difficulty = blockchain.difficulty
    for i in range(9):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction({
            "type": "transfer",
            "sender": "0",
            "payload": {
                "recipient": "Devin",
                "amount": 1
            },
            "nonce": 0,
            "chain": {
                "chain_id": "HDC",
                "version": 1
            },
            "gas": {
                "tip": 1,
                "max_fee": 1000,
                "limit": 2000
            },
            "signature": {
                "type": "ECDSA",
                "r": "00"*32,
                "s": "00"*32,
                "v": "00",
                "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
            }
        })
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty == original_difficulty  # Difficulty should not change


def test_difficulty_increases(blockchain):
    # Simulate quick block mining to decrease average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction({
            "type": "transfer",
            "sender": "0",
            "payload": {
                "recipient": "Devin",
                "amount": 1
            },
            "nonce": 0,
            "chain": {
                "chain_id": "HDC",
                "version": 1
            },
            "gas": {
                "tip": 1,
                "max_fee": 1000,
                "limit": 2000
            },
            "signature": {
                "type": "ECDSA",
                "r": "00"*32,
                "s": "00"*32,
                "v": "00",
                "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
            }
        })
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        new_timestamp = last_block.timestamp + 5
        with patch.object(last_block, 'timestamp', new=PropertyMock(return_value=new_timestamp)):
            blockchain.create_block(blockchain.current_transactions, previous_hash, previous_difficulty, proof)
    assert blockchain.difficulty > 1  # Difficulty should increase


def test_difficulty_decreases(blockchain):
    # Set initial difficulty to a higher value for testing
    blockchain.difficulty = 5
    # Simulate slow block mining to increase average block time
    for i in range(10):
        last_block = blockchain.chain[-1]
        proof = blockchain.proof_of_work(last_block)
        blockchain.add_transaction({
            "type": "transfer",
            "sender": "0",
            "payload": {
                "recipient": "Devin",
                "amount": 1
            },
            "nonce": 0,
            "chain": {
                "chain_id": "HDC",
                "version": 1
            },
            "gas": {
                "tip": 1,
                "max_fee": 1000,
                "limit": 2000
            },
            "signature": {
                "type": "ECDSA",
                "r": "00"*32,
                "s": "00"*32,
                "v": "00",
                "public_key": "4f3b6846489b905e424a3e98d8cb79adc76f14ac5c0a416ffb3ee24bbb4eb7978cc537cdea80f2bab21ef60a8071edf42a690490339623ffbd7ce5a29d14182cee7549fdf3d8e09b6376bcfb86ebb68040699a869b33f889ebe3dbfff7badd49"
            }
        })
        previous_hash = last_block.hash
        previous_difficulty = last_block.difficulty
        new_timestamp = blockchain.chain[-1].timestamp + 20
        new_block = Block(index=last_block.index + 1,
                          transactions=blockchain.current_transactions,
                          previous_hash=previous_hash,
                          proof=proof,
                          difficulty=previous_difficulty,
                          timestamp=new_timestamp)
        blockchain.chain.append(new_block)
        blockchain.current_transactions = []
    blockchain.adjust_difficulty()
    assert blockchain.difficulty < 5, "Difficulty should decrease after simulating slow block mining"
