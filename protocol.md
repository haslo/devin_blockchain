# Node Communication Protocol

This document outlines the protocol for inter-node communication within the blockchain network. The protocol is designed to be simple, extensible, and JSON-based to facilitate easy parsing and generation by nodes written in any language that supports JSON.

## Message Types

### Block Broadcast
When a new block is mined, it is broadcast to all nodes in the network using the following message format:

```json
{
  "type": "block_broadcast",
  "block": {
    "index": 1,
    "timestamp": 1638307200,
    "transactions": [
      {
        "sender": "sender_public_key",
        "recipient": "recipient_public_key",
        "amount": 1
      }
    ],
    "proof": 35293,
    "previous_hash": "hash_of_previous_block"
  }
}
```

### Transaction Broadcast
When a new transaction is created, it is broadcast to all nodes in the network using the following message format:

```json
{
  "type": "transaction_broadcast",
  "transaction": {
    "sender": "sender_public_key",
    "recipient": "recipient_public_key",
    "amount": 1
  }
}
```

### Node Discovery
Nodes can discover other nodes in the network using the following message format:

```json
{
  "type": "node_discovery",
  "node": {
    "address": "ip_address_or_hostname",
    "port": 5000
  }
}
```

### Node Propagation
When a node receives information about another node, it propagates this information to the rest of the network:

```json
{
  "type": "node_propagation",
  "node": {
    "address": "ip_address_or_hostname",
    "port": 5000
  }
}
```

## Handling Messages

Each node must be able to handle the above message types according to the following rules:

- Upon receiving a `block_broadcast` message, validate the block and add it to the blockchain if it is valid.
- Upon receiving a `transaction_broadcast` message, validate the transaction and add it to the mempool if it is valid.
- Upon receiving a `node_discovery` message, attempt to connect to the new node and share information about known nodes.
- Upon receiving a `node_propagation` message, update the node's list of known nodes with the new information.

Nodes should also implement additional message types as needed to support other functionalities such as consensus algorithms and synchronization of chains.
