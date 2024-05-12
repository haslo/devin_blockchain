import pytest
import json
from unittest.mock import patch, MagicMock, call
from networking.node import Node


@pytest.fixture
def node():
    return Node(port=5000)


def test_node_initialization(node):
    assert node.port == 5000
    assert node.bootstrap_node is None
    assert isinstance(node.nodes, set)
    assert node.nodes == set()
    assert node.mempool == []


@patch('socket.create_connection')
def test_connect_to_node(mock_create_connection, node):
    node.connect_to_node(('127.0.0.1', 5001))
    mock_create_connection.assert_called_with(('127.0.0.1', 5001))
    assert ('127.0.0.1', 5001) in node.nodes


def test_add_node(node):
    node.add_node(('127.0.0.1', 5001))
    assert ('127.0.0.1', 5001) in node.nodes


def test_remove_node(node):
    node.add_node(('127.0.0.1', 5001))
    node.remove_node(('127.0.0.1', 5001))
    assert ('127.0.0.1', 5001) not in node.nodes


@patch('socket.create_connection')
def test_broadcast_block(mock_create_connection, node):
    mock_socket = MagicMock()
    mock_create_connection.return_value = mock_socket
    mock_socket.__enter__.return_value = mock_socket
    node.add_node(('127.0.0.1', 5001))
    block_data = {'data': 'block'}
    node.broadcast_block(block_data)
    mock_create_connection.assert_called_with(('127.0.0.1', 5001))
    mock_socket.sendall.assert_called_with(json.dumps(block_data).encode('utf-8'))


def test_receive_block(node):
    block_data = {'data': 'block'}
    node.receive_block(block_data)
    # Assuming the blockchain has an add_block method that was called with the block data
    assert block_data in node.blockchain.chain


def test_resolve_forks(node):
    # Placeholder test for resolve_forks method
    assert node.resolve_forks() is None


def test_handle_new_transaction(node):
    transaction_data = {'data': 'transaction'}
    node.handle_new_transaction(transaction_data)
    assert transaction_data in node.mempool


@patch("threading.Thread")
def test_start_server(mock_thread, node):
    mock_thread.assert_not_called()
    node.start_server()
    mock_thread.assert_called_with(target=node.run_server)


def test_stop_server(node):
    assert node.stop_server() is None

# New tests for node's implementation of the protocol based on protocol.md
def test_node_handles_block_broadcast_correctly(node):
    # Test that node correctly handles a block broadcast message
    # Toggle test mode on to ensure the proof of work is validated against a lower difficulty
    node.blockchain.toggle_test_mode(True)

    block_broadcast_message = {
        "type": "block_broadcast",
        "uuid": "unique-uuid",
        "version": 1,
        "block": {
            "index": 1,
            "timestamp": 1638307200,
            "transactions": [
                # ... list of transactions ...
            ],
            "proof": 35293,
            "previous_hash": "hash_of_previous_block",
            "difficulty": 3  # Added difficulty key with a sample value
        },
        "signature": {
            "type": "ECDSA",
            "r": "r_value",
            "s": "s_value",
            "v": "recovery_id",
            "public_key": "public_key"
        }
    }
    # Assuming the node has a method to handle block broadcasts
    node.handle_block_broadcast(block_broadcast_message)
    # Verify that the block is added to the blockchain
    assert block_broadcast_message['block'] in node.blockchain.chain
    # Toggle test mode off after the test
    node.blockchain.toggle_test_mode(False)

def test_node_handles_transaction_broadcast_correctly(node):
    # Test that node correctly handles a transaction broadcast message
    transaction_broadcast_message = {
        "type": "transaction_broadcast",
        "uuid": "unique-uuid",
        "version": 1,
        "transaction": {
            "type": "transfer",
            "sender": "sender_address",
            "payload": {
                "recipient": "recipient_address",
                "amount": 123
            },
            "nonce": 1,
            "chain": {
                "chain_id": "dhc",
                "version": 1
            },
            "gas": {
                "tip": 0,
                "max_fee": 50,
                "limit": 100
            },
            "signature": {
                "type": "ECDSA",
                "r": "r_value",
                "s": "s_value",
                "v": "recovery_id",
                "public_key": "public_key"
            }
        }
    }
    # Assuming the node has a method to handle transaction broadcasts
    node.handle_transaction_broadcast(transaction_broadcast_message)
    # Verify that the entire transaction is added to the mempool
    assert transaction_broadcast_message['transaction'] in node.mempool

@patch('networking.node.Node.connect_to_node')
@patch('networking.node.Node.broadcast_nodes')
def test_handle_find_nodes(mock_broadcast_nodes, mock_connect_to_node, node):
    # Simulate receiving a find_nodes message
    find_nodes_message = {
        "type": "find_nodes",
        "node": {
            "address": "192.168.1.2",
            "port": 5002
        }
    }
    node.handle_find_nodes(find_nodes_message)
    # Verify that the node attempts to connect to the new node
    mock_connect_to_node.assert_called_with(('192.168.1.2', 5002))
    # Verify that the node broadcasts its list of known nodes
    mock_broadcast_nodes.assert_called_once()

@patch('networking.node.Node.add_node')
def test_handle_propagate_nodes(mock_add_node, node):
    # Simulate receiving a propagate_nodes message
    propagate_nodes_message = {
        "type": "propagate_nodes",
        "nodes": [
            {"address": "192.168.1.3", "port": 5003},
            {"address": "192.168.1.4", "port": 5004}
        ]
    }
    node.handle_propagate_nodes(propagate_nodes_message)
    # Verify that the node updates its list of known nodes
    calls = [call(('192.168.1.3', 5003)), call(('192.168.1.4', 5004))]
    mock_add_node.assert_has_calls(calls, any_order=True)
