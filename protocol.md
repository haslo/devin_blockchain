# Protocol

This is the high-level protocol, JSON layer. There is also a [low-level protocol spec](lowlevel_protocol.md).

## Transactions

Each transaction is a json structure with the following two keys:

* `"type"`
* `"payload"`

This allows for simple as well as complex data structures for smart contracts and on-blockchain code in the future.

### Transaction Types

#### Transfer Transactions

This is the most common and basic transaction type.

```json
{
  "type": "transfer",
  "sender": "sender_address",
  "payload": {
    "recipient": "recipient_address",
    "amount": 123
  },
  "nonce": 1,
  "chain_id": {
    "chain_id": "main",
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
```

### Future Types

The following types will also be implemented:

* contracted_transfer
* contract_create
* contract_call
* contract_cross_call
* state_variable

### Meta Types

These types are wrappers for other types with added data:

* conditional_transaction
* batch_transaction

Batch transactions can support different rollback mechanisms (or explicit lack thereof).

## Signatures

ECDSA signatures are used, like for ETH. Details to follow.

## Node Communication Protocol

The inter-node protocol is designed to be simple, extensible, and JSON-based to facilitate easy parsing and generation.
Nodes can be written in any language that supports JSON.

### Message Types

These message types must be supported:

* `block_broadcast`
* `transaction_broadcast`
* `find_nodes`
* `propagate_nodes`

#### Block Broadcast

When a new block is mined, it is broadcast to all nodes in the network using the following message format:

```json
{
  "type": "block_broadcast",
  "uuid": "uuid",
  "version": 1,
  "block": {
    "index": 1,
    "timestamp": 1638307200,
    "transactions": [
      "transaction",
      "transaction",
      "transaction"
    ],
    "proof": 35293,
    "previous_hash": "hash_of_previous_block"
  },
  "signature": {
    "type": "ECDSA",
    "r": "r_value",
    "s": "s_value",
    "v": "recovery_id",
    "public_key": "public_key"
  }
}
```

Note that the transactions follow the transaction spec from earlier in this document.

#### Transaction Broadcast

When a new transaction is created, it is broadcast to all nodes in the network using the following message format:

```json
{
  "type": "transaction_broadcast",
  "uuid": "uuid",
  "version": 1,
  "transaction": "transaction",
  "signature": {
    "type": "ECDSA",
    "r": "r_value",
    "s": "s_value",
    "v": "recovery_id",
    "public_key": "public_key"
  }
}
```

Note that the transaction follows the transaction spec from earlier in this document.

#### Find Nodes

Nodes can discover other nodes in the network using the following message format:

```json
{
  "type": "find_nodes",
  "uuid": "uuid",
  "version": 1,
  "node": {
    "address": "ip_address_or_hostname",
    "port": 5000,
    "public_key": "public_key"
  },
  "signature": {
    "type": "ECDSA",
    "r": "r_value",
    "s": "s_value",
    "v": "recovery_id",
    "public_key": "public_key"
  }
}
```

This includes the node's own (redundant) address and (non redundant) public key, for the node that wants to receive node data.

#### Propagate Nodes

A node can answer a find_nodes message or want to propagate itself with this message:

```json
{
  "type": "propagate_nodes",
  "uuid": "uuid",
  "version": 1,
  "nodes": [ {
      "address": "ip_address_or_hostname",
      "port": 5000,
      "public_key": "public_key"
    }, {
      "address": "ip_address_or_hostname",
      "port": 5000,
      "public_key": "public_key"
    }
  ],
  "signature": {
    "type": "ECDSA",
    "r": "r_value",
    "s": "s_value",
    "v": "recovery_id",
    "public_key": "public_key"
  }
}
```

The node format is identical to the `find_nodes` message's, but propagating the sending node itself does not make sense since the
recipient already has an open socket with it. Nodes are expected to send a sample of their most trustworthy peers.

### Handling Messages

Each node must be able to handle the above message types according to the following rules:

* Upon receiving a `block_broadcast` message, validate the block and add it to the blockchain if it is valid.
* Upon receiving a `transaction_broadcast` message, validate the transaction and add it to the mempool if it is valid.
* Upon receiving a `find_nodes` message, attempt to connect to the new node and share information about known nodes.
* Upon receiving a `propagate_nodes` message, update the node's list of known nodes with the new information.

#### Additional messages

More message types will be defined during development. Probably:

* version
* version_ack
* get_blocks
* get_data
* ping
* pong
* reject

#### Message Type Codes

For the low level protocol:

| Type                  | Code |
|-----------------------|------|
| ack                   | 0x01 |
| find_nodes            | 0xa1 |
| propagate_nodes       | 0xa2 |
| transaction_broadcast | 0xa3 |
| block_broadcast       | 0xa4 |
| get_blocks            | 0xb1 |
| get_data              | 0xb2 |
| ping                  | 0xc1 |
| pong                  | 0xc2 |
| version               | 0xf1 |
| version_ack           | 0xf2 |
| reject                | 0xf8 |

### Future Extensions

These will be defined when they are necessary (before the release of the blockchain, but not right now).

#### Gossip Protocol

In the future, a gossip protocol will be added. The above message types are ready for that and the protocol will mostly impact which nodes propagate what to which other nodes.

## Signatures

This signature structure:

```json
{
  "signature": {
    "type": "ECDSA",
    "r": "r_value",
    "s": "s_value",
    "v": "recovery_id",
    "public_key": "public_key"
  }
}
```

Will be fully defined at a later time. For now, we just fill placeholder values.
