import socket
import threading
import json
from blockchain import Blockchain

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
                # Send a hello message or similar handshake protocol
                sock.sendall(b'Hello, node!')
                # Add the node to the nodes set
                self.add_node(node_info)
        except Exception as e:
            print(f"Connection to {node_info} failed: {e}")

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
                    # Send the block data as a json string
                    sock.sendall(json.dumps(block).encode('utf-8'))
            except Exception as e:
                print(f"Failed to send block to {node}: {e}")

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
            print(f"Node server listening on port {self.port}")

            try:
                while self.server_running:
                    client_socket, client_address = server_socket.accept()
                    print(f"Accepted connection from {client_address}")
                    client_handler = threading.Thread(
                        target=self.handle_client_connection,
                        args=(client_socket, client_address)
                    )
                    client_handler.start()
            except Exception as e:
                print(f"Server error: {e}")
            finally:
                server_socket.close()

    def handle_client_connection(self, client_socket, client_address):
        # This method will handle the client connection
        with client_socket:
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    # Process the data from the client
                    # Assuming the data is in JSON format
                    try:
                        message = json.loads(data.decode('utf-8'))
                        # Check the type of message
                        if message['type'] == 'new_transaction':
                            # Handle new transaction
                            self.handle_new_transaction(message['transaction'])
                        elif message['type'] == 'new_block':
                            # Handle new block
                            self.receive_block(message['block'])
                        # Add more message types as needed
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON received from {client_address}: {e}")
                    except KeyError as e:
                        print(f"Missing key in message from {client_address}: {e}")
            except Exception as e:
                print(f"Error handling client {client_address}: {e}")

    def stop_server(self):
        # Stop the node server
        if self.server_thread:
            self.server_running = False
            self.server_thread.join()
            print("Node server stopped.")

# Implement additional methods as needed for p2p communication and node functionality
