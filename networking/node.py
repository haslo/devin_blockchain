import socket
import threading
import json
from blockchain.blockchain import Blockchain
from blockchain.block import Block
from blockchain.transaction import Transaction


class Node:
    def __init__(self, port, bootstrap_node=None):
        self.host = '0.0.0.0'
        self.port = port
        self.bootstrap_node = bootstrap_node
        self.nodes = set()
        self.blockchain = Blockchain()
        self.mempool = []
        self.server_thread = None
        self.server_running = False

        if bootstrap_node:
            self.connect_to_node(bootstrap_node)

    def connect_to_node(self, node_info):
        with socket.create_connection(node_info) as sock:
            # TODO use protocol
            sock.sendall(b'Hello, node!')
            self.add_node(node_info)

    def add_node(self, node_info):
        self.nodes.add(node_info)

    def remove_node(self, node_info):
        if node_info in self.nodes:
            self.nodes.remove(node_info)

    def broadcast_block(self, block):
        for node in self.nodes:
            with socket.create_connection(node) as sock:
                sock.sendall(json.dumps(block).encode('utf-8'))

    def receive_block(self, block):
        self.blockchain.add_block(block)

    def handle_new_transaction(self, transaction):
        self.mempool.append(transaction)

    def start_server(self):
        self.server_running = True
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            try:
                while self.server_running:
                    client_socket, client_address = server_socket.accept()
                    client_handler = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, client_address)
                    )
                    client_handler.start()
            except Exception as e:
                server_socket.close()
                raise e

    def handle_client_connection(self, client_socket, client_address):
        with client_socket:
            while True:
                # TODO use header, delimiter, essentially everything a protocol needs because
                # TODO implement this entirely Devin just put a placeholder there AGAIN
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                if message['type'] == 'new_transaction':
                    self.handle_new_transaction(message['transaction'])
                elif message['type'] == 'new_block':
                    self.receive_block(message['block'])
                elif message['type'] == 'block_broadcast':
                    self.handle_block_broadcast(message)
                elif message['type'] == 'transaction_broadcast':
                    self.handle_transaction_broadcast(message)

    def stop_server(self):
        if self.server_thread:
            self.server_running = False
            self.server_thread.join()

    def handle_block_broadcast(self, message):
        block_data = message['block']
        block = Block(
            index=block_data['index'],
            transactions=Transaction.from_dict(block_data['transactions']),
            previous_hash=block_data['previous_hash'],
            proof=block_data['proof'],
            difficulty=block_data['difficulty'],
            timestamp=block_data['timestamp']
        )
        if self.blockchain.validate_block(block):
            self.blockchain.add_block(block)
            self.broadcast_block(block)  # Re-broadcast the block if needed

    def handle_transaction_broadcast(self, message):
        transaction = Transaction.from_dict(message['transaction'])
        if transaction.validate_transaction():
            self.mempool.append(transaction)
            self.broadcast_transaction(transaction)  # Re-broadcast the transaction if needed

    def broadcast_transaction(self, transaction):
        for node in self.nodes:
            # TODO avoid duplicates
            with socket.create_connection(node) as sock:
                sock.sendall(json.dumps(transaction).encode('utf-8'))

    def handle_find_nodes(self, message):
        new_node_info = (message['node']['address'], message['node']['port'])
        self.connect_to_node(new_node_info)
        self.broadcast_nodes()

    def handle_propagate_nodes(self, message):
        for node_info in message['nodes']:
            self.add_node((node_info['address'], node_info['port']))

    def broadcast_nodes(self):
        nodes_info = [{'address': node[0], 'port': node[1]} for node in self.nodes]
        message = {
            'type': 'propagate_nodes',
            'nodes': nodes_info
        }
        for node in self.nodes:
            # TODO use connection pool instead and keep connections open
            with socket.create_connection(node) as sock:
                sock.sendall(json.dumps(message).encode('utf-8'))
