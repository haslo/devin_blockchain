import socket
import threading
import json
import logging
from blockchain.blockchain import Blockchain
from blockchain.block import Block

# Initialize logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('node.log'), logging.StreamHandler()])

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
        # Connect to a new node
        # node_info is expected to be a tuple (host, port)
        try:
            # Create a new socket connection to the node
            with socket.create_connection(node_info) as sock:
                # Send a hello message, protocol not yet implemented
                sock.sendall(b'Hello, node!')
                # Add the node to the nodes set
                self.add_node(node_info)
        except Exception as e:
            logging.error(f"Connection to {node_info} failed: {e}")

    def add_node(self, node_info):
        # Add a new node to the list of nodes
        self.nodes.add(node_info)

    def remove_node(self, node_info):
        # Remove a node from the list of nodes
        if node_info in self.nodes:
            self.nodes.remove(node_info)

    def broadcast_block(self, block):
        # Broadcast a block to all connected nodes
        for node in self.nodes:
            try:
                with socket.create_connection(node) as sock:
                    sock.sendall(json.dumps(block).encode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to send block to {node}: {e}")

    def receive_block(self, block):
        # Handle receiving a block
        # For now, we'll just add it to the blockchain
        self.blockchain.add_block(block)

    def resolve_forks(self):
        # Implement a simple fork resolution algorithm
        # This is a placeholder for the actual implementation
        pass

    def handle_new_transaction(self, transaction):
        # Handle a new transaction
        # For now, we'll just add it to the mempool
        self.mempool.append(transaction)

    def start_server(self):
        # Start the node server to listen for incoming connections
        self.server_running = True
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def run_server(self):
        # This method will run in a separate thread to handle incoming connections
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logging.info(f"Node server listening on port {self.port}")

            try:
                while self.server_running:
                    client_socket, client_address = server_socket.accept()
                    logging.info(f"Accepted connection from {client_address}")
                    client_handler = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, client_address)
                    )
                    client_handler.start()
            except Exception as e:
                logging.error(f"Server error: {e}")
            finally:
                server_socket.close()

    def handle_client_connection(self, client_socket, client_address):
        with client_socket:
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    try:
                        message = json.loads(data.decode('utf-8'))
                        # Handle different message types based on protocol
                        if message['type'] == 'new_transaction':
                            self.handle_new_transaction(message['transaction'])
                        elif message['type'] == 'new_block':
                            self.receive_block(message['block'])
                        elif message['type'] == 'block_broadcast':
                            self.handle_block_broadcast(message)
                        elif message['type'] == 'transaction_broadcast':
                            self.handle_transaction_broadcast(message)
                    except json.JSONDecodeError as e:
                        logging.error(f"Invalid JSON received from {client_address}: {e}")
                    except KeyError as e:
                        logging.error(f"Missing key in message from {client_address}: {e}")
            except Exception as e:
                logging.error(f"Error handling client {client_address}: {e}")

    def stop_server(self):
        if self.server_thread:
            self.server_running = False
            self.server_thread.join()
            logging.info("Node server stopped.")

    def handle_block_broadcast(self, message):
        # Handle a block broadcast message
        # Validate and add block to blockchain
        block_data = message['block']
        block = Block(
            index=block_data['index'],
            transactions=block_data['transactions'],
            previous_hash=block_data['previous_hash'],
            proof=block_data['proof'],
            difficulty=block_data['difficulty'],
            timestamp=block_data['timestamp']
        )
        if self.blockchain.validate_block(block):
            self.blockchain.add_block(block)
            logging.info(f"Block {block.index} added to the blockchain")
            self.broadcast_block(block)  # Re-broadcast the block if needed
        else:
            logging.warning(f"Received invalid block {block.index}")

    def handle_transaction_broadcast(self, message):
        # Handle a transaction broadcast message
        # Validate and add transaction to mempool
        transaction = message['transaction']
        sender = transaction['sender']
        recipient = transaction['payload']['recipient']
        amount = transaction['payload']['amount']
        if self.blockchain.validate_transaction(sender, recipient, amount):
            self.mempool.append(transaction)
            self.broadcast_transaction(transaction)  # Re-broadcast the transaction if needed

    def broadcast_transaction(self, transaction):
        # Broadcast a transaction to all connected nodes
        for node in self.nodes:
            try:
                with socket.create_connection(node) as sock:
                    sock.sendall(json.dumps(transaction).encode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to send transaction to {node}: {e}")

    def handle_find_nodes(self, message):
        # Handle a find_nodes message
        # Attempt to connect to the new node and share known nodes
        new_node_info = (message['node']['address'], message['node']['port'])
        self.connect_to_node(new_node_info)
        self.broadcast_nodes()

    def handle_propagate_nodes(self, message):
        # Handle a propagate_nodes message
        # Update the node's list of known nodes with the new information
        for node_info in message['nodes']:
            self.add_node((node_info['address'], node_info['port']))

    def broadcast_nodes(self):
        # Broadcast the list of known nodes to all connected nodes
        nodes_info = [{'address': node[0], 'port': node[1]} for node in self.nodes]
        message = {
            'type': 'propagate_nodes',
            'nodes': nodes_info
        }
        for node in self.nodes:
            try:
                with socket.create_connection(node) as sock:
                    sock.sendall(json.dumps(message).encode('utf-8'))
            except Exception as e:
                logging.error(f"Failed to broadcast nodes to {node}: {e}")
