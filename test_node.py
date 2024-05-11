import pytest
import json
import socket
from unittest.mock import patch, MagicMock
from node import Node


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
    print(json.dumps(block_data).encode('utf-8'))
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
